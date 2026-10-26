"""Synthetic positive and negative controls for NE-EXP-001, on the protocol's primary runs.

Inputs: the eligible development runs of sub-ALD002 (count-matched VolumeTiming, no holdout).
Real wheel, eye and pupil series are used so regressor statistics are realistic. The fUS signal is
simulated with known truth. The holdout run is excluded by name and never read.

Procedure under test is the protocol's: frames within 6 s after a VolumeTiming interval gap are
masked, leave-one-calendar-date-out, and a block-permutation null of the wheel (120 s blocks).
Consistency criterion: Δ > 0 on at least 5 of the primary dates.

Scenarios (per replicate):
  zero_effect          AR(1) noise, no effect                  -> false-positive rate
  ar_null_strong       AR(1), phi=0.99, no effect              -> calibration under strong memory
  known_effect         wheel effect, R2 gain ~0.05 in truth    -> power
  misaligned_effect    true effect delayed 2.1 s, protocol unchanged -> power loss only
  correlated_nuisance  signal driven by eye only, wheel correlated with eye -> leakage check

Usage: uv run python scripts/run_nex001_controls.py [N_REPS] [N_PERM]
"""

from __future__ import annotations

import json
import struct
import sys
import zipfile
import zlib
from pathlib import Path

import numpy as np

from neural_echo.exp001 import (
    N_LAGS,
    RunDesign,
    aligned_target,
    block_permute,
    lagged_matrix,
    leave_one_group_out_delta,
    window_mean,
)

ZIP = Path("data/raw/landemard2026/sub-ALD002.zip")
HOLDOUT = "sub-ALD002_task-awake_acq-ref10_run-2"
OUT = Path("experiments/20261026-ne-exp-001-fusi-measurement-ceiling/controls_results.json")
SEED = 20261026
N_REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 60
N_PERM = int(sys.argv[2]) if len(sys.argv) > 2 else 50
PHI_DEFAULT = 0.96
PHI_STRONG = 0.99
EFFECT_R2 = 0.05
MISALIGN_FRAMES = 7  # 2.1 s at 0.3 s per frame
GAP_S = 0.45
MASK_FRAMES = N_LAGS  # 6 s after each gap
MIN_CONSISTENT_DATES = 5  # of the primary development dates
KERNEL = np.array([k**2 * np.exp(-k / 2.0) for k in range(N_LAGS)])
KERNEL = KERNEL / KERNEL.sum()
SCENARIOS = [
    "zero_effect",
    "ar_null_strong",
    "known_effect",
    "misaligned_effect",
    "correlated_nuisance",
]


def _tsv(zf: zipfile.ZipFile, base: str, kind: str) -> tuple[dict, np.ndarray]:
    side = json.loads(zf.read(f"{base}_recording-{kind}_physio.json"))
    text = zlib.decompress(
        zf.read(f"{base}_recording-{kind}_physio.tsv.gz"), 16 + zlib.MAX_WBITS
    ).decode()
    data = np.array([[float(v) for v in line.split("\t")] for line in text.splitlines()])
    return side, data


def _physio_frames(zf: zipfile.ZipFile, base: str, vt: np.ndarray) -> dict[str, np.ndarray]:
    side_w, data_w = _tsv(zf, base, "wheel")
    side_e, data_e = _tsv(zf, base, "eye")
    return {
        "wheel": window_mean(
            data_w[:, side_w["Columns"].index("wheel_velocity")],
            side_w["SamplingFrequency"],
            side_w["StartTime"],
            vt,
        ),
        "eye": window_mean(
            data_e[:, side_e["Columns"].index("eye_movement")],
            side_e["SamplingFrequency"],
            side_e["StartTime"],
            vt,
        ),
        "pupil": window_mean(
            data_e[:, side_e["Columns"].index("pupil_size")],
            side_e["SamplingFrequency"],
            side_e["StartTime"],
            vt,
        ),
    }


def _trim(series: dict[str, np.ndarray], invalid: np.ndarray, name: str):
    """Drop leading/trailing frames with missing physio; an interior gap excludes the run."""
    valid = np.all([np.isfinite(v) for v in series.values()], axis=0)
    idx = np.flatnonzero(valid)
    lo, hi = int(idx[0]), int(idx[-1]) + 1
    if not valid[lo:hi].all():
        raise ValueError(f"{name}: interior physio gap; excluded by coverage rule")
    return {k: v[lo:hi] for k, v in series.items()}, invalid[lo:hi]


def read_primary_runs() -> tuple[list[dict], list[str]]:
    """Return eligible runs (count-matched, not holdout) and the names excluded for mismatch."""
    zf = zipfile.ZipFile(ZIP)
    lines = zf.read("sub-ALD002/sub-ALD002_scans.tsv").decode().splitlines()[1:]
    date_of: dict[str, str] = {}
    for line in lines:
        fn, acq, _ = line.split("\t")
        if fn.startswith("fusi/") and fn.endswith("_pwd.nii.gz"):
            date_of[fn.rsplit("/", 1)[-1].replace("_pwd.nii.gz", "")] = acq[:10]
    runs, excluded = [], []
    for name in sorted(date_of):
        if name == HOLDOUT:
            continue
        base = f"sub-ALD002/fusi/{name}"
        head = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(
            zf.read(base + "_pwd.nii.gz"), 352
        )
        t = struct.unpack("<8h", head[40:56])[4]
        vt_full = np.array(json.loads(zf.read(base + "_pwd.json"))["VolumeTiming"], dtype=float)
        if len(vt_full) != t:
            excluded.append(name)
            continue
        vt = vt_full
        gaps = np.flatnonzero(np.diff(vt) > GAP_S)
        invalid = np.zeros(t, dtype=int)
        for g in gaps:
            invalid[g + 1 : g + 1 + MASK_FRAMES] = 1
        series, invalid = _trim(_physio_frames(zf, base, vt), invalid, name)
        runs.append(
            {
                "name": name,
                "date": date_of[name],
                "gaps": int(len(gaps)),
                "invalid": invalid,
                **series,
            }
        )
    return runs, excluded


def ar1(T: int, phi: float, rng: np.random.Generator) -> np.ndarray:
    e = rng.normal(size=T)
    y = np.empty(T)
    y[0] = e[0] / np.sqrt(1 - phi * phi)
    for t in range(1, T):
        y[t] = phi * y[t - 1] + e[t]
    return y


def causal_conv(x: np.ndarray, kernel: np.ndarray, shift: int = 0) -> np.ndarray:
    out = np.zeros_like(x)
    for k, h in enumerate(kernel):
        s = k + shift
        if s == 0:
            out += h * x
        else:
            out[s:] += h * x[:-s]
    return out


def build_runs(runs: list[dict], ys: list[np.ndarray], wheels: list[np.ndarray]) -> list[RunDesign]:
    """Lagged designs with gap-masked rows removed (rows need no invalid frame in their window)."""
    out = []
    for r, y, w in zip(runs, ys, wheels, strict=True):
        keep = np.convolve(r["invalid"], np.ones(N_LAGS, dtype=int), mode="valid") == 0
        Xn = np.hstack([lagged_matrix(r["eye"]), lagged_matrix(r["pupil"])])[keep]
        Xw = lagged_matrix(w)[keep]
        yy = aligned_target(y)[keep]
        out.append(RunDesign(X_nuis=Xn, X_wheel=Xw, y=yy, group=r["date"]))
    return out


def scenario_series(
    name: str, runs: list[dict], rng: np.random.Generator
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    wheels = [r["wheel"] for r in runs]
    eyes = [r["eye"] for r in runs]
    phi = PHI_STRONG if name == "ar_null_strong" else PHI_DEFAULT
    noise = [ar1(len(w), phi, rng) for w in wheels]
    if name in ("zero_effect", "ar_null_strong"):
        return noise, wheels
    if name == "known_effect":
        eff = [causal_conv(w, KERNEL) for w in wheels]
    elif name == "misaligned_effect":
        eff = [causal_conv(w, KERNEL, shift=MISALIGN_FRAMES) for w in wheels]
    elif name == "correlated_nuisance":
        eff = [causal_conv(e, KERNEL) for e in eyes]
    else:
        raise ValueError(name)
    pooled = np.concatenate(eff)
    scale = np.sqrt((EFFECT_R2 / (1 - EFFECT_R2)) / pooled.var())
    return [n + scale * e for n, e in zip(noise, eff, strict=True)], wheels


def one_replicate(name: str, runs: list[dict], rng: np.random.Generator) -> dict:
    ys, wheels = scenario_series(name, runs, rng)
    obs = leave_one_group_out_delta(build_runs(runs, ys, wheels))
    null = []
    for _ in range(N_PERM):
        perm = [block_permute(w, rng) for w in wheels]
        null.append(leave_one_group_out_delta(build_runs(runs, ys, perm))["delta_pooled"])
    q95 = float(np.quantile(null, 0.95))
    return {
        "delta_obs": obs["delta_pooled"],
        "q95_null": q95,
        "detected": bool(obs["delta_pooled"] > q95),
        "date_criterion_met": bool(obs["n_groups_positive"] >= MIN_CONSISTENT_DATES),
    }


def main() -> None:
    runs, excluded = read_primary_runs()
    dates = sorted({r["date"] for r in runs})
    rng = np.random.default_rng(SEED)
    corr = float(np.mean([np.corrcoef(r["wheel"], r["eye"])[0, 1] for r in runs]))
    results: dict[str, dict] = {}
    for name in SCENARIOS:
        reps = [one_replicate(name, runs, rng) for _ in range(N_REPS)]
        det = np.array([r["detected"] for r in reps], dtype=float)
        rate = float(det.mean())
        results[name] = {
            "detection_rate": rate,
            "monte_carlo_se": float(np.sqrt(rate * (1 - rate) / N_REPS)),
            "mean_delta_obs": float(np.mean([r["delta_obs"] for r in reps])),
            "mean_q95_null": float(np.mean([r["q95_null"] for r in reps])),
            "date_criterion_rate": float(np.mean([r["date_criterion_met"] for r in reps])),
            "n_replicates": N_REPS,
            "n_permutations": N_PERM,
        }
        print(name, {k: round(v, 4) for k, v in results[name].items()}, flush=True)
    payload = {
        "seed": SEED,
        "data": "eligible development runs only (count-matched; holdout excluded by name)",
        "primary_runs": [r["name"] for r in runs],
        "primary_run_gaps": {r["name"]: r["gaps"] for r in runs},
        "excluded_mismatched": excluded,
        "primary_dates": dates,
        "consistency_rule": f">= {MIN_CONSISTENT_DATES} of {len(dates)} dates",
        "mean_wheel_eye_correlation": round(corr, 4),
        "ar_phi_default": PHI_DEFAULT,
        "ar_phi_strong": PHI_STRONG,
        "effect_r2_target": EFFECT_R2,
        "misalign_seconds": round(MISALIGN_FRAMES * 0.3, 2),
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
