"""Investigation of CRT v2 diagnostic failures on development runs. Read-only, no fUS outcome used.

Questions:
  A. Is the ~87% zero-step fraction the animal being stationary (exact zeros), or an artefact?
  B. Where does the residual variance sit: wheel-active vs wheel-stationary frames?
  C. Which blocks give the extreme block-variance ratio, and what is in them?
  D. Where does the junction jump of 27.9 occur (run, frame, neighbouring values, mask)?
"""

import importlib.util
from pathlib import Path

import numpy as np

from neural_echo.crt import RawRun, nuisance_lags, quarter_profile, scale_vector
from neural_echo.exp001 import BLOCK_FRAMES, N_LAGS, aligned_target

spec = importlib.util.spec_from_file_location(
    "controls", Path("E:/РАБОИЕ ПРОЕКТЫ👌/A-9  Neural Echo/scripts/run_nex001_controls.py")
)
assert spec is not None and spec.loader is not None
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
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
X = np.vstack([np.column_stack([np.ones(len(Z)), Z]) for Z in Zs])
beta, *_ = np.linalg.lstsq(X, np.concatenate(ws), rcond=None)
raw = [w - np.column_stack([np.ones(len(Z)), Z]) @ beta for w, Z in zip(ws, Zs, strict=True)]

print("== A. wheel stationarity")
for r in runs:
    w = r.wheel
    zero_frac = float(np.mean(w == 0))
    step_zero = float(np.mean(np.diff(w) == 0))
    nonzero_steps = np.diff(w) != 0
    print(
        f"{r.group} n={len(w)} exact-zero frac={zero_frac:.3f} zero-step frac={step_zero:.3f} "
        f"min={w.min():.4g} max={w.max():.4g} uniq={len(np.unique(w))} "
        f"invalid={int(r.invalid.sum())}"
    )

print("\n== B. residual variance: active vs stationary aligned frames")
for i, r in enumerate(runs):
    active = aligned_target(r.wheel) != 0  # frames where the aligned wheel value is nonzero
    res = raw[i]
    act = active[: len(res)]
    if act.any() and (~act).any():
        print(
            f"{r.group} var_active={res[act].var():.4f} var_stationary={res[~act].var():.4f} "
            f"ratio={res[act].var() / max(res[~act].var(), 1e-12):.2f} frac_active={act.mean():.3f}"
        )

print("\n== C. extreme block variance ratio, leave-one-run-out profile")
for i, r in enumerate(runs):
    others = [raw[j] for j in range(len(runs)) if j != i]
    prof = quarter_profile(others)
    std = raw[i] / scale_vector(prof, len(raw[i]))
    n = len(std)
    edges = np.linspace(0, n, max(n // BLOCK_FRAMES, 1) + 1).astype(int)
    bvars = np.array([std[edges[k] : edges[k + 1]].var() for k in range(len(edges) - 1)])
    if len(bvars) and bvars.max() / max(bvars.min(), 1e-12) > 1000:
        k_lo = int(np.argmin(bvars))
        k_hi = int(np.argmax(bvars))
        aw = aligned_target(r.wheel)
        for k in (k_lo, k_hi):
            seg = slice(edges[k], edges[k + 1])
            print(
                f"{r.group} block {k}/{len(bvars)} len={edges[k + 1] - edges[k]} "
                f"var={bvars[k]:.3e} mean={std[seg].mean():.4f} "
                f"wheel_nonzero={np.mean(aw[seg] != 0):.3f} wheel_max={aw[seg].max():.4g}"
            )

print("\n== D. junction steps")
for r in runs:
    w = r.wheel
    d = np.abs(np.diff(w))
    mean_step = d.mean()
    j = N_LAGS - 1  # head/aligned junction: frames j and j+1
    ratio = abs(w[j + 1] - w[j]) / mean_step if mean_step > 0 else float("nan")
    if ratio > 5:
        k = int(np.argmax(d))
        print(
            f"{r.group} junction ratio={ratio:.2f} "
            f"w[{j - 1}:{j + 3}]={np.round(w[j - 1 : j + 3], 4)} "
            f"mean_step={mean_step:.4g} largest_step_frame={k} step={d[k]:.4g} "
            f"masked_near_junction={int(r.invalid[max(j - 5, 0) : j + 5].sum())}"
        )
    # Largest step anywhere, to see whether the 27.9 value is a junction or a general spike.
    k_max = int(np.argmax(d))
    print(
        f"{r.group} max step/mean={d[k_max] / mean_step:.2f} at frame {k_max} "
        f"(junction frame {j}) masked_at_max={int(r.invalid[k_max])}"
    )
