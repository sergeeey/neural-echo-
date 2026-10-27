"""Minimal discriminating synthetic set for NE-EXP-001: implementation error vs non-identifiability.

Three scenarios, all with NO wheel effect in the truth:
  null_no_confound   no arousal, no effect             -> must be null (implementation check)
  hidden_arousal     arousal r=0.5 NOT in the design    -> detection expected (confounding)
  measured_arousal   same arousal ADDED to nuisance     -> must return to null if code is right

If null_no_confound is null, hidden_arousal is detected, and measured_arousal is null, the
failure in the earlier controls is non-identifiability rather than an implementation error.

Usage: uv run python scripts/run_nex001_discriminate.py [N_REPS] [N_PERM]

Usage: uv run python scripts/run_nex001_discriminate.py [N_REPS] [N_PERM]
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from neural_echo.exp001 import (
    N_LAGS,
    RunDesign,
    aligned_target,
    block_permute,
    lagged_matrix,
    leave_one_group_out_delta,
)

_spec = importlib.util.spec_from_file_location(
    "controls", Path(__file__).resolve().parent / "run_nex001_controls.py"
)
assert _spec is not None and _spec.loader is not None
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

N_REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 40
N_PERM = int(sys.argv[2]) if len(sys.argv) > 2 else 50
SEED = 20261027
OUT = Path("experiments/20261026-ne-exp-001-fusi-measurement-ceiling/discriminate_results.json")
ROLE = {
    "null_no_confound": "no confound, no effect",
    "hidden_arousal": "arousal correlated with wheel, not in design",
    "measured_arousal": "same arousal, included in nuisance",
}


def arousal_for(wheels: list[np.ndarray], rng: np.random.Generator) -> list[np.ndarray]:
    out = []
    for w in wheels:
        z = (w - w.mean()) / w.std()
        out.append(0.5 * z + np.sqrt(0.75) * rng.normal(size=len(w)))
    return out


def run_once(scenario: str, runs: list[dict], rng: np.random.Generator) -> dict:
    wheels = [r["wheel"] for r in runs]
    noise = [C.ar1_unit(len(w), C.PHI_DEFAULT, rng) for w in wheels]
    if scenario == "null_no_confound":
        arousal: list[np.ndarray] = []
        ys = noise
    else:
        arousal = arousal_for(wheels, rng)
        eff = [C.causal_conv(a, C.KERNEL) for a in arousal]
        pooled = np.concatenate(eff)
        scale = np.sqrt((C.EFFECT_R2 / (1 - C.EFFECT_R2)) / pooled.var())
        ys = [n + scale * e for n, e in zip(noise, eff, strict=True)]

    def designs(perm: list[np.ndarray] | None) -> list[RunDesign]:
        out = []
        for i, r in enumerate(runs):
            w = wheels[i] if perm is None else perm[i]
            keep = np.convolve(r["invalid"], np.ones(N_LAGS, dtype=int), mode="valid") == 0
            cols = [lagged_matrix(r["eye"]), lagged_matrix(r["pupil"])]
            if scenario == "measured_arousal":
                cols.append(lagged_matrix(arousal[i]))
            Xn = np.hstack(cols)[keep]
            Xw = lagged_matrix(w)[keep]
            out.append(
                RunDesign(X_nuis=Xn, X_wheel=Xw, y=aligned_target(ys[i])[keep], group=r["date"])
            )
        return out

    obs = leave_one_group_out_delta(designs(None))
    null = []
    for _ in range(N_PERM):
        perm = [block_permute(w, rng) for w in wheels]
        null.append(leave_one_group_out_delta(designs(perm))["delta_pooled"])
    q95 = float(np.quantile(null, 0.95))
    margin = obs["delta_pooled"] > q95
    dates = obs["n_groups_positive"] >= C.MIN_CONSISTENT_DATES
    return {"margin": bool(margin), "full": bool(margin and dates), "delta": obs["delta_pooled"]}


def main() -> None:
    runs, _ = C.read_primary_runs()
    rng = np.random.default_rng(SEED)
    results = {}
    for scenario in ROLE:
        reps = [run_once(scenario, runs, rng) for _ in range(N_REPS)]
        full = np.array([r["full"] for r in reps], dtype=float)
        results[scenario] = {
            "role": ROLE[scenario],
            "detection_rate_full_rule": float(full.mean()),
            "detected": int(full.sum()),
            "n_replicates": N_REPS,
            "n_permutations": N_PERM,
            "mean_delta": float(np.mean([r["delta"] for r in reps])),
        }
        print(scenario, results[scenario], flush=True)
    payload = {
        "seed": SEED,
        "data": "eligible development runs only (holdout excluded by name)",
        "truth": "no wheel effect in any scenario",
        "results": results,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
