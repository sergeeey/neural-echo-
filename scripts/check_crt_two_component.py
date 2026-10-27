"""Surrogate fidelity of a two-component wheel generator (no fUS outcome used).

Component 1, activity state: a two-state Markov chain (exact zero vs non-zero) with transition
probabilities estimated on the TRAINING dates only.
Component 2, amplitude: on active frames, mu(Z) + scale * r, where r is a block permutation of the
held-out run's own standardised residuals from active frames (the same resampling idea as the CRT,
restricted to active frames). Inactive frames are exactly zero.

Compared with the observed held-out wheel and with the independent block permutation, on the
statistics that the CRT v2 failure concerns: active fraction, episode count and length, residual
variance by state, and corr(|residual|, ||Z||). This is a fidelity check only, not a test.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from neural_echo.crt import RawRun, build_plans, nuisance_lags
from neural_echo.exp001 import aligned_target, block_permute

spec = importlib.util.spec_from_file_location(
    "controls", Path(__file__).resolve().parent / "run_nex001_controls.py"
)
assert spec is not None and spec.loader is not None
assert spec is not None and spec.loader is not None
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

N_DRAWS = 19


def episodes(x: np.ndarray) -> tuple[int, float]:
    act = (x != 0).astype(int)
    d = np.diff(np.concatenate([[0], act, [0]]))
    lens = np.where(d == -1)[0] - np.where(d == 1)[0]
    return len(lens), float(lens.mean()) if len(lens) else 0.0


def stats(w: np.ndarray, mu: np.ndarray, scale: np.ndarray, Z: np.ndarray) -> dict:
    n_ep, mean_len = episodes(w)
    res = (w - mu) / scale
    act = w != 0
    return {
        "active_frac": float(act.mean()),
        "episodes": float(n_ep),
        "mean_episode_len": mean_len,
        "resid_var_active": float(res[act].var()) if act.any() else float("nan"),
        "resid_var_stationary": float(res[~act].var()) if (~act).any() else float("nan"),
        "corr_abs_resid_Zmag": float(np.corrcoef(np.abs(res), np.linalg.norm(Z, axis=1))[0, 1]),
    }


def transition_probs(runs: list[RawRun]) -> tuple[float, float]:
    """P(active | inactive) and P(inactive | active), pooled over training runs."""
    a01 = a00 = a10 = a11 = 0
    for r in runs:
        s = (aligned_target(r.wheel) != 0).astype(int)
        prev, cur = s[:-1], s[1:]
        a00 += int(np.sum((prev == 0) & (cur == 0)))
        a01 += int(np.sum((prev == 0) & (cur == 1)))
        a10 += int(np.sum((prev == 1) & (cur == 0)))
        a11 += int(np.sum((prev == 1) & (cur == 1)))
    p01 = a01 / max(a00 + a01, 1)
    p10 = a10 / max(a10 + a11, 1)
    return p01, p10


def simulate_states(
    s0: int, n: int, p01: float, p10: float, rng: np.random.Generator
) -> np.ndarray:
    u = rng.random(n)
    s = np.empty(n, dtype=int)
    state = s0
    for t in range(n):
        p = p01 if state == 0 else 1 - p10
        state = int(u[t] < p)
        s[t] = state
    return s


def two_component_draw(pr, p01: float, p10: float, rng: np.random.Generator) -> np.ndarray:
    """Kept-row draw of the wheel: Markov activity, amplitude from permuted active residuals."""
    obs_state = (pr.aligned_wheel[pr.keep] != 0).astype(int)
    s = simulate_states(int(obs_state[0]), len(obs_state), p01, p10, rng)
    resid_act = pr.resid[pr.keep][obs_state == 1]
    out = np.zeros(len(obs_state))
    k = int(s.sum())
    if k and len(resid_act):
        perm = block_permute(resid_act, rng)
        reps = np.resize(perm, k)
        active_idx = np.flatnonzero(s)
        out[active_idx] = pr.mu[pr.keep][active_idx] + pr.scale[pr.keep][active_idx] * reps
    return out


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
    plans = build_plans(runs, conditional=True, standardise=True, edge_frames=40)
    rng = np.random.default_rng(11)
    summary: dict[str, list[float]] = {}
    for plan in plans:
        train = [r for r in runs if r.group != plan.date]
        p01, p10 = transition_probs(train)
        test_runs = [r for r in runs if r.group == plan.date]
        for pr, r in zip(plan.test, test_runs, strict=True):
            Z = nuisance_lags(r)[pr.keep]
            assert pr.mu is not None and pr.scale is not None
            mu = pr.mu[pr.keep]
            scale = pr.scale[pr.keep]
            obs = stats(aligned_target(r.wheel)[pr.keep], mu, scale, Z)
            tc, ind = [], []
            for _ in range(N_DRAWS):
                w_tc = two_component_draw(pr, p01, p10, rng)
                tc.append(stats(w_tc, mu, scale, Z))
                w_ind = block_permute(aligned_target(r.wheel)[pr.keep], rng)
                ind.append(stats(w_ind, mu, scale, Z))
            line = [f"{plan.date} p01={p01:.3f} p10={p10:.3f}"]
            for key in obs:
                med_tc = float(np.nanmedian([x[key] for x in tc]))
                med_ind = float(np.nanmedian([x[key] for x in ind]))
                summary.setdefault(f"{key}|obs", []).append(obs[key])
                summary.setdefault(f"{key}|two_component", []).append(med_tc)
                summary.setdefault(f"{key}|independent", []).append(med_ind)
                line.append(f"{key}: obs={obs[key]:.4g} tc={med_tc:.4g} ind={med_ind:.4g}")
            print(" | ".join(line))
    print("\nmedian across runs:")
    for key in sorted(summary):
        print(key, round(float(np.nanmedian(summary[key])), 5))


if __name__ == "__main__":
    main()
