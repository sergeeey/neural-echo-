"""Diagnostics for the CRT v2 conditional null, development runs only (no fUS outcome used).

Checks on the wheel-on-Z residual that the conditional draw permutes:
  1. heteroskedasticity: quarter variance ratio, raw vs standardised (leave-one-run-out profile)
  2. covariate dependence: corr(|standardised residual|, ||Z|| per physiology block)
  3. block exchangeability: block means/variances and lag-1 correlation of block means
  4. boundary: observed head/aligned junction jump and run-start residual mean
  5. mask counts and scored rows per run, v1 (edge 20) and v2 (edge 40)

The wheel-on-Z mu is a pooled OLS here (diagnostic only); the test itself fits mu on training dates.
Writes experiments/20261027-ne-exp-002-temporal-latent-confounding/crt_diagnostics.json.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import numpy as np

from neural_echo.crt import (
    EDGE_FRAMES,
    N_QUARTERS,
    RawRun,
    keep_rows,
    nuisance_lags,
    quarter_profile,
    scale_vector,
)
from neural_echo.exp001 import BLOCK_FRAMES, N_LAGS, aligned_target

_spec = importlib.util.spec_from_file_location(
    "controls", Path(__file__).resolve().parent / "run_nex001_controls.py"
)
assert _spec is not None and _spec.loader is not None
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

OUT = Path("experiments/20261027-ne-exp-002-temporal-latent-confounding/crt_diagnostics.json")


def commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def corr(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.corrcoef(a, b)[0, 1])


def block_edges(n: int) -> np.ndarray:
    """Same block boundaries as exp001.block_permute."""
    return np.linspace(0, n, max(n // BLOCK_FRAMES, 1) + 1).astype(int)


def quarter_ratio(x: np.ndarray) -> float:
    n = len(x)
    v = [
        np.mean(x[k * n // N_QUARTERS : (k + 1) * n // N_QUARTERS] ** 2) for k in range(N_QUARTERS)
    ]
    return float(max(v) / min(v))


def main() -> None:
    dev, _ = C.read_primary_runs()
    runs = [
        RawRun(
            eye=r["eye"],
            pupil=r["pupil"],
            wheel=r["wheel"],
            y=r["wheel"],
            invalid=r["invalid"],
            group=r["date"],
        )
        for r in dev
    ]
    Zs = [nuisance_lags(r) for r in runs]
    ws = [aligned_target(r.wheel) for r in runs]

    # Pooled OLS mu (diagnostic only), then raw residuals per run.
    X_all = np.vstack([np.column_stack([np.ones(len(Z)), Z]) for Z in Zs])
    w_all = np.concatenate(ws)
    beta, *_ = np.linalg.lstsq(X_all, w_all, rcond=None)
    raw = [w - np.column_stack([np.ones(len(Z)), Z]) @ beta for w, Z in zip(ws, Zs, strict=True)]

    rows = []
    std_all = []
    for i, r in enumerate(runs):
        others = [raw[j] for j in range(len(runs)) if j != i]
        prof = quarter_profile(others)  # leave-one-run-out profile: no tautology
        std = raw[i] / scale_vector(prof, len(raw[i]))
        std_all.append(std)
        absz_eye = np.linalg.norm(Zs[i][:, :N_LAGS], axis=1)
        absz_pup = np.linalg.norm(Zs[i][:, N_LAGS:], axis=1)
        edges = block_edges(len(std))
        bmeans = np.array([std[edges[k] : edges[k + 1]].mean() for k in range(len(edges) - 1)])
        bvars = np.array([std[edges[k] : edges[k + 1]].var() for k in range(len(edges) - 1)])
        lag1 = corr(bmeans[:-1], bmeans[1:]) if len(bmeans) > 3 else float("nan")
        n_mask = int(r.invalid.sum())
        rows.append(
            {
                "run": r.group,
                "quarter_var_ratio_raw": round(quarter_ratio(raw[i]), 3),
                "quarter_var_ratio_std": round(quarter_ratio(std), 3),
                "corr_abs_std_eyeZ": round(corr(np.abs(std), absz_eye), 3),
                "corr_abs_std_pupilZ": round(corr(np.abs(std), absz_pup), 3),
                "n_blocks": len(bmeans),
                # For unit-variance white residuals this is ~1; above 1 means block means move more.
                "block_mean_sd_over_expected": round(
                    float(bmeans.std() * np.sqrt(np.mean(np.diff(edges)))), 3
                ),
                "block_var_ratio_max_min": round(float(bvars.max() / bvars.min()), 3),
                "block_mean_lag1": round(lag1, 3),
                "run_start_mean_first40": round(float(std[:40].mean()), 4),
                # Step across the head/aligned junction relative to the mean absolute step.
                "junction_jump_over_mean_step": round(
                    float(
                        abs(r.wheel[N_LAGS] - r.wheel[N_LAGS - 1])
                        / np.mean(np.abs(np.diff(r.wheel)))
                    ),
                    3,
                ),
                "wheel_zero_step_fraction": round(float(np.mean(np.diff(r.wheel) == 0)), 3),
                "block_var_min": round(float(bvars.min()), 6),
                "masked_frames": n_mask,
                "rows_v1_edge20": int(keep_rows(r, edge_frames=20).sum()),
                "rows_v2_edge40": int(keep_rows(r, edge_frames=EDGE_FRAMES).sum()),
            }
        )

    def summary(key: str) -> dict:
        v = np.array([row[key] for row in rows], dtype=float)
        return {"median": round(float(np.nanmedian(v)), 3), "max": round(float(np.nanmax(v)), 3)}

    keys = [
        "quarter_var_ratio_raw",
        "quarter_var_ratio_std",
        "corr_abs_std_eyeZ",
        "corr_abs_std_pupilZ",
        "block_var_ratio_max_min",
        "block_mean_lag1",
        "run_start_mean_first40",
        "junction_jump_over_mean_step",
        "wheel_zero_step_fraction",
        "block_var_min",
    ]
    payload = {
        "code_version": commit(),
        "data": "eligible development runs only; holdout excluded by name",
        "per_run": rows,
        "summary": {k: summary(k) for k in keys},
        "rows_total_v1": int(sum(row["rows_v1_edge20"] for row in rows)),
        "rows_total_v2": int(sum(row["rows_v2_edge40"] for row in rows)),
        "limitations": [
            "mu is a pooled OLS over all dev runs (diagnostic); the test fits mu on training dates",
            "the standardised residual uses a leave-one-run-out scale profile",
            "block exchangeability is checked with the same linspace blocks as block_permute",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    for k in keys:
        print(k, payload["summary"][k])
    print("rows v1", payload["rows_total_v1"], "v2", payload["rows_total_v2"])
    print("saved", OUT)


if __name__ == "__main__":
    main()
