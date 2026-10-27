"""Pilot: independent vs eye-conditional block-permutation tests on the same synthetic data.

Synthetic fUS; real wheel, eye, pupil from the eight primary development runs.
  zero_effect          no effect                                   -> size
  ar_null_strong       no effect, AR phi=0.99                      -> size under strong memory
  hidden_arousal       arousal r~0.5 with wheel, NOT in nuisance   -> rejections expected
  measured_arousal     same arousal, IN nuisance                   -> size near nominal expected
  lead_misalignment    true wheel effect advanced 2.1 s            -> sync violation
  known_added_info     true wheel effect, no confounder            -> power

VERSION 1: raw residual permutation, no edge exclusion (first pilot).
VERSION 2: standardised residuals, frames < 40 not scored (boundary and heteroskedasticity fixes).

Rejection at alpha = 0.05 with B = 99 draws (p = (1 + #null >= obs) / 100).
Intervals: Wilson 95% on rejection rates. Seeds are fixed; the code version is recorded.
The holdout run is excluded by name and never read.

Usage: uv run python scripts/run_nex001_crt_pilot.py [N_REPS] [N_DRAWS] [VERSION]
"""

from __future__ import annotations

import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

from neural_echo.crt import RawRun, build_plans, run_test

_spec = importlib.util.spec_from_file_location(
    "controls", Path(__file__).resolve().parent / "run_nex001_controls.py"
)
assert _spec is not None and _spec.loader is not None
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

N_REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 100
N_DRAWS = int(sys.argv[2]) if len(sys.argv) > 2 else 99
VERSION = int(sys.argv[3]) if len(sys.argv) > 3 else 2
ALPHA = 0.05
SEED = 20261027
FLAGS = {
    1: {"standardise": False, "edge_frames": 20},  # v1 reproduced by flags (see plan)
    2: {"standardise": True, "edge_frames": 40},
}[VERSION]
OUT = Path(
    f"experiments/20261027-ne-exp-002-temporal-latent-confounding/crt_pilot_v{VERSION}_n{N_REPS}.json"
)
Z95 = 1.959963984540054
SCENARIOS = [
    "zero_effect",
    "ar_null_strong",
    "hidden_arousal",
    "measured_arousal",
    "lead_misalignment",
    "known_added_info",
]


def wilson(k: int, n: int) -> tuple[float, float]:
    p = k / n
    denom = 1 + Z95 * Z95 / n
    centre = (p + Z95 * Z95 / (2 * n)) / denom
    half = Z95 * math.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / denom
    return centre - half, centre + half


def commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def arousal_series(wheels: list[np.ndarray], rng: np.random.Generator) -> list[np.ndarray]:
    out = []
    for w in wheels:
        z = (w - w.mean()) / w.std()
        out.append(0.5 * z + np.sqrt(0.75) * rng.normal(size=len(w)))
    return out


def synth(name: str, dev: list[dict], rng: np.random.Generator) -> tuple[list[RawRun], dict]:
    wheels = [r["wheel"] for r in dev]
    phi = C.PHI_STRONG if name == "ar_null_strong" else C.PHI_DEFAULT
    noise = [C.ar1_unit(len(w), phi, rng) for w in wheels]
    extra = None
    if name in ("zero_effect", "ar_null_strong"):
        ys = noise
    elif name in ("hidden_arousal", "measured_arousal"):
        arousal = arousal_series(wheels, rng)
        eff = [C.causal_conv(a, C.KERNEL) for a in arousal]
        ys = _scaled(noise, eff)
        if name == "measured_arousal":
            extra = arousal
    elif name == "lead_misalignment":
        eff = [C.causal_conv(w, C.KERNEL, shift=C.SHIFT_ADVANCE) for w in wheels]
        ys = _scaled(noise, eff)
    elif name == "known_added_info":
        eff = [C.causal_conv(w, C.KERNEL) for w in wheels]
        ys = _scaled(noise, eff)
    else:
        raise ValueError(name)
    runs = [
        RawRun(
            eye=r["eye"],
            pupil=r["pupil"],
            wheel=r["wheel"],
            y=y,
            invalid=r["invalid"],
            group=r["date"],
            extra=None if extra is None else extra[i],
        )
        for i, (r, y) in enumerate(zip(dev, ys, strict=True))
    ]
    return runs, {}


def _scaled(noise: list[np.ndarray], eff: list[np.ndarray]) -> list[np.ndarray]:
    pooled = np.concatenate(eff)
    scale = np.sqrt((C.EFFECT_R2 / (1 - C.EFFECT_R2)) / pooled.var())
    return [n + scale * e for n, e in zip(noise, eff, strict=True)]


def main() -> None:
    dev, excluded = C.read_primary_runs()
    rng = np.random.default_rng(SEED)
    results: dict[str, dict] = {}
    for name in SCENARIOS:
        rej = {"independent": [], "conditional": []}
        pvals = {"independent": [], "conditional": []}
        q95 = {"independent": [], "conditional": []}
        for _ in range(N_REPS):
            runs, _ = synth(name, dev, rng)
            plans = build_plans(
                runs,
                conditional=True,
                standardise=FLAGS["standardise"],
                edge_frames=FLAGS["edge_frames"],
            )
            for kind, cond in (("independent", False), ("conditional", True)):
                res = run_test(plans, runs, N_DRAWS, rng, conditional=cond)
                rej[kind].append(res.p <= ALPHA)
                pvals[kind].append(res.p)
                q95[kind].append(float(np.quantile(res.null, 1 - ALPHA)))
        row = {}
        for kind in ("independent", "conditional"):
            k = int(np.sum(rej[kind]))
            lo, hi = wilson(k, N_REPS)
            row[kind] = {
                "rejections": k,
                "rate": k / N_REPS,
                "wilson95": [round(lo, 4), round(hi, 4)],
                "mean_p": float(np.mean(pvals[kind])),
                "mean_q95_null": float(np.mean(q95[kind])),
            }
        row["p_values"] = {k: [float(x) for x in v] for k, v in pvals.items()}
        results[name] = row
        print(name, json.dumps({k: row[k] for k in ("independent", "conditional")}), flush=True)
    payload = {
        "code_version": commit(),
        "version": VERSION,
        "flags": FLAGS,
        "seed": SEED,
        "n_reps": N_REPS,
        "n_draws": N_DRAWS,
        "alpha": ALPHA,
        "data": "eligible development runs only; holdout excluded by name",
        "primary_runs": [r["name"] for r in dev],
        "excluded_mismatched": excluded,
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
