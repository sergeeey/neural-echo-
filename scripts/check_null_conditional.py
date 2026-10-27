"""Null-validity check for NE-EXP-001: independent vs eye-conditional block permutation.

H0 under test: "wheel adds nothing beyond eye and pupil". An independent wheel permutation destroys
the wheel-eye dependence that the nuisance set partly explains, so its null can differ from H0.
The conditional null permutes wheel residuals after an in-run OLS on the wheel-free nuisance lags,
then adds the fitted part back, so the eye-explained part is preserved.

Small by design (default 10 replicates, 50 permutations, zero-effect truth) to compare thresholds,
not to certify calibration.

Usage: uv run python scripts/check_null_conditional.py [N_REPS] [N_PERM]
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from neural_echo.exp001 import block_permute, leave_one_group_out_delta

_spec = importlib.util.spec_from_file_location(
    "controls", Path(__file__).resolve().parent / "run_nex001_controls.py"
)
assert _spec is not None and _spec.loader is not None
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

N_REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
N_PERM = int(sys.argv[2]) if len(sys.argv) > 2 else 50
SEED = 20261027
OUT = Path("experiments/20261026-ne-exp-001-fusi-measurement-ceiling/null_conditional_check.json")


def conditional_wheel_null(
    wheel: np.ndarray, nuis_lags: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    """Permute blocks of wheel residuals given wheel-free nuisance lags; add the fit back."""
    X = np.column_stack([np.ones(len(wheel)), nuis_lags])
    beta, *_ = np.linalg.lstsq(X, wheel, rcond=None)
    fitted = X @ beta
    resid = wheel - fitted
    return fitted + block_permute(resid, rng)


def designs(runs, ys, wheels_for_analysis):
    out = []
    for r, y, w in zip(runs, ys, wheels_for_analysis, strict=True):
        from neural_echo.exp001 import RunDesign, aligned_target, lagged_matrix

        keep = np.convolve(r["invalid"], np.ones(C.N_LAGS, dtype=int), mode="valid") == 0
        Xn = np.hstack([lagged_matrix(r["eye"]), lagged_matrix(r["pupil"])])
        Xw = lagged_matrix(w)
        out.append(
            RunDesign(
                X_nuis=Xn[keep],
                X_wheel=Xw[keep],
                y=aligned_target(y)[keep],
                group=r["date"],
            )
        )
    return out


def main() -> None:
    runs, _ = C.read_primary_runs()
    rng = np.random.default_rng(SEED)
    stats = {"independent": [], "conditional": []}
    obs_margin = {"independent": [], "conditional": []}
    for _ in range(N_REPS):
        ys, wheels = C.scenario_series("zero_effect", runs, rng)
        from neural_echo.exp001 import lagged_matrix

        nuis_lags = [np.hstack([lagged_matrix(r["eye"]), lagged_matrix(r["pupil"])]) for r in runs]
        # Align the residual regression with the lagged rows used by the design.
        for kind in ("independent", "conditional"):
            null = []
            for _p in range(N_PERM):
                if kind == "independent":
                    perm = [block_permute(w, rng) for w in wheels]
                else:
                    perm = []
                    for w, nl in zip(wheels, nuis_lags, strict=True):
                        n = len(w)
                        lag = nl.shape[0]
                        # nuis_lags has rows for frames lag_idx..; use the frames it covers.
                        w_al = w[n - lag :]
                        p = conditional_wheel_null(w_al, nl, rng)
                        full = w.copy()
                        full[n - lag :] = p
                        perm.append(full)
                null.append(leave_one_group_out_delta(designs(runs, ys, perm))["delta_pooled"])
            obs = leave_one_group_out_delta(designs(runs, ys, wheels))["delta_pooled"]
            q95 = float(np.quantile(null, 0.95))
            stats[kind].append(q95)
            obs_margin[kind].append(bool(obs > q95))
    summary = {
        k: {
            "mean_q95": float(np.mean(v)),
            "margin_false_positive_rate": float(np.mean(obs_margin[k])),
            "n_replicates": N_REPS,
            "n_permutations": N_PERM,
        }
        for k, v in stats.items()
    }
    print(json.dumps(summary, indent=2))
    OUT.write_text(json.dumps({"seed": SEED, "summary": summary}, indent=2), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
