"""Synthetic positive and negative controls for NE-EXP-001 on the protocol's primary runs.

Inputs: the eligible development runs of sub-ALD002 (count-matched VolumeTiming, no holdout).
Real wheel, eye and pupil series are used, so regressor statistics are realistic. The fUS signal
is simulated with known truth. The holdout run is excluded by name and never read.

Procedure under test is the protocol's: rows whose lag window or target falls within 6 s after a
VolumeTiming interval gap are removed; leave-one-calendar-date-out; a block-permutation null of
the wheel (blocks of about 120 s). Detection is the full rule: observed Δ above the null 95th
percentile AND Δ > 0 on at least 5 of the primary dates.

Scenarios (per replicate; noise has unit variance, so the stated R² is the true R² in expectation):
  zero_effect          AR(1) noise, no effect                  -> false-positive rate
  ar_null_strong       AR(1), phi=0.99, no effect              -> calibration under strong memory
  known_effect         wheel effect, R² ~0.05 in truth         -> power
  delayed_outside      wheel effect delayed 6 s (outside lags) -> power when the model cannot see it
  lead_misalignment    wheel effect advanced 2.1 s             -> sensitivity to the wrong direction
  eye_driven           signal driven by the measured eye only  -> nuisance adequacy
  hidden_confound      signal driven by an UNMEASURED arousal correlated with the wheel (r~0.5)
                       -> whether the wheel gains from a confound it cannot see

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
SHIFT_ADVANCE = -7  # 2.1 s, wheel advanced relative to fUS
SHIFT_OUTSIDE = 20  # 6 s, delay beyond the 0-6 s lag window
GAP_S = 0.45
MASK_FRAMES = 20  # 6 s after each gap, in frames
MIN_CONSISTENT_DATES = 5  # of the primary development dates
KERNEL = np.array([k**2 * np.exp(-k / 2.0) for k in range(N_LAGS)])
KERNEL = KERNEL / KERNEL.sum()
SCENARIOS = [
    "zero_effect",
    "ar_null_strong",
    "known_effect",
    "delayed_outside",
    "lead_misalignment",
    "eye_driven",
    "hidden_confound",
]


def _tsv(zf: zipfile.ZipFile, base: str, kind: str) -> tuple[dict, np.ndarray]:
    side = json.loads(zf.read(f"{base}_recording-{kind}_physio.json"))
    text = zlib.decompress(
        zf.read(f"{base}_recording-{kind}_physio.tsv.gz"), 16 + zlib.MAX_WBITS
    ).decode()
    data = np.array([[float(v) for v in line.split("\t")] for line in text.splitlines()])
    return side, data


def _column(zf: zipfile.ZipFile, base: str, kind: str, col: str, vt: np.ndarray) -> np.ndarray:
    side, data = _tsv(zf, base, kind)
    return window_mean(
        data[:, side["Columns"].index(col)],
        side["SamplingFrequency"],
        side["StartTime"],
        vt,
    )


def _trim(series: dict[str, np.ndarray], invalid: np.ndarray, name: str):
    """Drop leading/trailing frames with missing physio; an interior gap excludes the run."""
    valid = np.all([np.isfinite(v) for v in series.values()], axis=0)
    idx = np.flatnonzero(valid)
    lo, hi = int(idx[0]), int(idx[-1]) + 1
    if not valid[lo:hi].all():
        raise ValueError(f"{name}: interior physio gap; excluded by coverage rule")
    return {k: v[lo:hi] for k, v in series.items()}, invalid[lo:hi]


def read_primary_runs() -> tuple[list[dict], list[str]]:
    """Eligible runs (count-matched, not holdout) and the names excluded for count mismatch."""
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
        vt = np.array(json.loads(zf.read(base + "_pwd.json"))["VolumeTiming"], dtype=float)
        if len(vt) != t:
            excluded.append(name)
            continue
        gaps = np.flatnonzero(np.diff(vt) > GAP_S)
        invalid = np.zeros(t, dtype=int)
        for g in gaps:
            invalid[g + 1 : g + 1 + MASK_FRAMES] = 1
        series = {
            "wheel": _column(zf, base, "wheel", "wheel_velocity", vt),
            "eye": _column(zf, base, "eye", "eye_movement", vt),
            # Pupil is already normalised by the recording median (sidecar); no further step.
            "pupil": _column(zf, base, "eye", "pupil_size", vt),
        }
        series, invalid = _trim(series, invalid, name)
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


def ar1_unit(T: int, phi: float, rng: np.random.Generator) -> np.ndarray:
    """Stationary AR(1) scaled to unit marginal variance."""
    e = rng.normal(size=T)
    y = np.empty(T)
    y[0] = e[0]
    for t in range(1, T):
        y[t] = phi * y[t - 1] + e[t]
    return y * np.sqrt(1 - phi * phi)


def shifted(x: np.ndarray, s: int) -> np.ndarray:
    """Delay by s frames (s>0) or advance by -s frames (s<0), zero-filled."""
    out = np.zeros_like(x)
    if s > 0:
        out[s:] = x[:-s]
    elif s < 0:
        out[:s] = x[-s:]
    else:
        out[:] = x
    return out


def causal_conv(x: np.ndarray, kernel: np.ndarray, shift: int = 0) -> np.ndarray:
    base = shifted(x, shift)
    out = np.zeros_like(x)
    for k, h in enumerate(kernel):
        out += h * shifted(base, k)
    return out


def build_runs(runs: list[dict], ys: list[np.ndarray], wheels: list[np.ndarray]) -> list[RunDesign]:
    """Lagged designs with gap-masked rows removed (a row is dropped if its window hits a gap)."""
    out = []
    for r, y, w in zip(runs, ys, wheels, strict=True):
        keep = np.convolve(r["invalid"], np.ones(N_LAGS, dtype=int), mode="valid") == 0
        Xn = np.hstack([lagged_matrix(r["eye"]), lagged_matrix(r["pupil"])])[keep]
        Xw = lagged_matrix(w)[keep]
        out.append(RunDesign(X_nuis=Xn, X_wheel=Xw, y=aligned_target(y)[keep], group=r["date"]))
    return out


def scenario_series(
    name: str, runs: list[dict], rng: np.random.Generator
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Return (synthetic fUS per run, wheel per run that the analysis uses)."""
    wheels = [r["wheel"] for r in runs]
    eyes = [r["eye"] for r in runs]
    phi = PHI_STRONG if name == "ar_null_strong" else PHI_DEFAULT
    noise = [ar1_unit(len(w), phi, rng) for w in wheels]
    if name in ("zero_effect", "ar_null_strong"):
        return noise, wheels
    if name == "known_effect":
        eff = [causal_conv(w, KERNEL) for w in wheels]
    elif name == "delayed_outside":
        eff = [causal_conv(w, KERNEL, shift=SHIFT_OUTSIDE) for w in wheels]
    elif name == "lead_misalignment":
        eff = [causal_conv(w, KERNEL, shift=SHIFT_ADVANCE) for w in wheels]
    elif name == "eye_driven":
        eff = [causal_conv(e, KERNEL) for e in eyes]
    elif name == "hidden_confound":
        # Unmeasured arousal A: correlated with the wheel (r ~ 0.5) but not in the analysis design.
        arousal = []
        for w in wheels:
            z = (w - w.mean()) / w.std()
            arousal.append(0.5 * z + np.sqrt(1 - 0.25) * rng.normal(size=len(w)))
        eff = [causal_conv(a, KERNEL) for a in arousal]
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
    margin_ok = obs["delta_pooled"] > q95
    dates_ok = obs["n_groups_positive"] >= MIN_CONSISTENT_DATES
    return {
        "delta_obs": obs["delta_pooled"],
        "q95_null": q95,
        "detected_margin_only": bool(margin_ok),
        "detected_full_rule": bool(margin_ok and dates_ok),
        "date_criterion_met": bool(dates_ok),
    }


def main() -> None:
    runs, excluded = read_primary_runs()
    dates = sorted({r["date"] for r in runs})
    rng = np.random.default_rng(SEED)
    corr = float(np.mean([np.corrcoef(r["wheel"], r["eye"])[0, 1] for r in runs]))
    results: dict[str, dict] = {}
    for name in SCENARIOS:
        reps = [one_replicate(name, runs, rng) for _ in range(N_REPS)]
        full = np.array([r["detected_full_rule"] for r in reps], dtype=float)
        margin = np.array([r["detected_margin_only"] for r in reps], dtype=float)
        rate = float(full.mean())
        results[name] = {
            "detection_rate_full_rule": rate,
            "monte_carlo_se_full_rule": float(np.sqrt(rate * (1 - rate) / N_REPS)),
            "detection_rate_margin_only": float(margin.mean()),
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
        "shift_advance_s": round(SHIFT_ADVANCE * 0.3, 2),
        "shift_outside_s": round(SHIFT_OUTSIDE * 0.3, 2),
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
