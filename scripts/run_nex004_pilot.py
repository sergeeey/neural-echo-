"""NE-EXP-004 diagnostic pilot, executed under the accepted contract (abe5dec).

Block A (candidate A, contract C1 and C2): training-only two-component generator, nested
out-of-sample transferability check, rest / movement / transition diagnostics, and the oracle C6
descriptive check. Test-wheel statistics appear ONLY in the oracle block (C6); they never enter a
fit or an admissibility decision.

Block B (candidate B, contract C3-B): 60 independent zero-effect replicates;
the Layer 1 decision rule
(pooled delta > 0 AND date-level bootstrap lower bound > 0) is evaluated on each; K = number of
replicates that declare support. K >= 8 -> INFLATION FLAG; K <= 7 -> NO GROSS INFLATION DETECTED,
which is not a demonstration of calibration.

CPU budget: total process CPU time must stay within 0.3 CPU-hours.
Partial results are saved after each
unit, and the run stops if the budget is reached.

Usage: uv run python scripts/run_nex004_pilot.py [A|B|all]
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from neural_echo.crt import (
    RawRun,
    keep_rows,
    nuisance_lags,
    quarter_profile,
    scale_vector,
)
from neural_echo.exp001 import aligned_target, block_permute

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"
SEED_SYNTH = 20261027
SEED_BOOT = 20261028
N_DRAWS_A = 99
N_REPS_B = 60
K_FLAG = 8
BUDGET_CPU_S = 0.3 * 3600.0


def _load(path: Path, name: str, argv: list[str] | None = None):
    if argv is not None:
        sys.argv = argv
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ORIG_ARGV = list(sys.argv)
C = _load(REPO / "scripts" / "run_nex001_controls.py", "controls", ["controls"])
P = _load(REPO / "scripts" / "run_nex001_crt_pilot.py", "pilot", ["pilot", "1", "19", "2"])
CP = _load(
    REPO / "scripts" / "check_prediction_comparison.py",
    "check_prediction_comparison",
    ["pilot", "1", "19", "2"],
)


def git_head() -> str:
    head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd=REPO
    ).stdout
    # WHY: counting lines of the stripped output; "count('\\n') + 1" reported 1 on a clean tree.
    dirty = len(status.splitlines())
    return f"{head} (status entries at run time: {dirty})"


def cpu_used() -> float:
    return time.process_time()


# ---------------------------------------------------------------------------
# Block A: candidate A generator (training dates only)
# ---------------------------------------------------------------------------


def episodes(x: np.ndarray) -> tuple[int, np.ndarray]:
    act = (x != 0).astype(int)
    d = np.diff(np.concatenate([[0], act, [0]]))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    return len(starts), ends - starts


def rest_episode_lengths(x: np.ndarray) -> np.ndarray:
    _, lens = episodes(np.where(x != 0, 0, 1))
    return lens


def transitions(x: np.ndarray) -> tuple[float, float]:
    s = (x != 0).astype(int)
    prev, cur = s[:-1], s[1:]
    a00 = int(np.sum((prev == 0) & (cur == 0)))
    a01 = int(np.sum((prev == 0) & (cur == 1)))
    a10 = int(np.sum((prev == 1) & (cur == 0)))
    a11 = int(np.sum((prev == 1) & (cur == 1)))
    return a01 / max(a00 + a01, 1), a10 / max(a10 + a11, 1)


def fit_generator(runs: list[RawRun]) -> dict:
    """Two-component generator parameters from the given runs only (no held-out data)."""
    a00 = a01 = a10 = a11 = 0
    xs, ws = [], []
    for r in runs:
        w = aligned_target(r.wheel)
        s = (w != 0).astype(int)
        prev, cur = s[:-1], s[1:]
        a00 += int(np.sum((prev == 0) & (cur == 0)))
        a01 += int(np.sum((prev == 0) & (cur == 1)))
        a10 += int(np.sum((prev == 1) & (cur == 0)))
        a11 += int(np.sum((prev == 1) & (cur == 1)))
        Z = nuisance_lags(r)
        keep = keep_rows(r)
        xs.append(np.column_stack([np.ones(len(Z)), Z])[keep])
        ws.append(w[keep])
    p01 = a01 / max(a00 + a01, 1)
    p10 = a10 / max(a10 + a11, 1)
    coef, *_ = np.linalg.lstsq(np.vstack(xs), np.concatenate(ws), rcond=None)
    raw_all = []
    for r in runs:
        Z = nuisance_lags(r)
        w = aligned_target(r.wheel)
        raw_all.append(w - np.column_stack([np.ones(len(Z)), Z]) @ coef)
    profile = quarter_profile(raw_all)
    pool = []
    for r in runs:
        Z = nuisance_lags(r)
        w = aligned_target(r.wheel)
        mu = np.column_stack([np.ones(len(Z)), Z]) @ coef
        scale = scale_vector(profile, len(w))
        res = (w - mu) / scale
        act = (w != 0) & keep_rows(r)
        pool.append(res[act])
    return {
        "p01": p01,
        "p10": p10,
        "coef": coef,
        "profile": profile,
        "pool": np.concatenate(pool),
        "n_fit_runs": len(runs),
    }


def markov_states(n: int, p01: float, p10: float, rng: np.random.Generator) -> np.ndarray:
    pi1 = p01 / (p01 + p10)
    u = rng.random(n)
    s = np.empty(n, dtype=int)
    state = int(rng.random() < pi1)
    for t in range(n):
        p = p01 if state == 0 else 1.0 - p10
        state = int(u[t] < p)
        s[t] = state
    return s


def draw_surrogate(
    gen: dict, run: RawRun, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    Z = nuisance_lags(run)
    n = len(Z)
    mu = np.column_stack([np.ones(n), Z]) @ gen["coef"]
    scale = scale_vector(gen["profile"], n)
    s = markov_states(n, gen["p01"], gen["p10"], rng)
    k = int(s.sum())
    out = np.zeros(n)
    if k:
        amp = np.resize(block_permute(gen["pool"], rng), k)
        idx = np.flatnonzero(s)
        out[idx] = mu[idx] + scale[idx] * amp
    return out, mu, scale, Z


def stats_for(
    w: np.ndarray, mu: np.ndarray, scale: np.ndarray, Z: np.ndarray, keep: np.ndarray
) -> dict:
    n_ep, lens = episodes(w)
    res = (w - mu) / scale
    act_keep = (w != 0) & keep
    rk = res[keep]
    zk = np.linalg.norm(Z[keep], axis=1)
    s6 = float(np.corrcoef(np.abs(rk), zk)[0, 1]) if len(rk) > 2 else float("nan")
    return {
        "S1": float(np.mean(w != 0)),
        "S3": float(n_ep),
        "S4": float(lens.mean()) if len(lens) else 0.0,
        "S5": float(res[act_keep].var()) if act_keep.any() else float("nan"),
        "S6": s6,
    }


def run_block_A(out: dict, t0: float) -> None:
    dev, _ = C.read_primary_runs()
    dates = sorted({r["date"] for r in dev})
    runs_by_date: dict[str, list[RawRun]] = {}
    for r in dev:
        runs_by_date.setdefault(r["date"], []).append(
            RawRun(
                eye=r["eye"],
                pupil=r["pupil"],
                wheel=r["wheel"],
                y=r["wheel"],
                invalid=r["invalid"],
                group=r["date"],
            )
        )
    out["A"] = {
        "dates": dates,
        "code": git_head(),
        "seed": SEED_SYNTH,
        "n_draws": N_DRAWS_A,
        "per_date": {},
        "admissible": {},
        "oracle_C6": {},
    }
    rng = np.random.default_rng(SEED_SYNTH)
    tol_stats = ("S1", "S3", "S4", "S5", "S6")
    for d in dates:
        if cpu_used() > BUDGET_CPU_S:
            out["A"]["stopped"] = "CPU budget reached before completing held-out date " + d
            return
        train_dates = [x for x in dates if x != d]
        OBS: dict[str, dict] = {}
        M: dict[str, dict] = {}
        diag: dict[str, dict] = {}
        for j in train_dates:
            fit_dates = [x for x in train_dates if x != j]
            gen = fit_generator([r for x in fit_dates for r in runs_by_date[x]])
            obs_rows, sur_rows = [], []
            diag_j = {
                "obs_trans": None,
                "sur_trans": [],
                "obs_rest_q": None,
                "sur_rest_q": [],
                "obs_act_q": None,
                "sur_act_q": [],
                "obs_amp_q": None,
                "sur_amp": [],
            }
            for run in runs_by_date[j]:
                w_obs = aligned_target(run.wheel)
                Z = nuisance_lags(run)
                keep = keep_rows(run)
                mu = np.column_stack([np.ones(len(Z)), Z]) @ gen["coef"]
                scale = scale_vector(gen["profile"], len(Z))
                obs_rows.append(stats_for(w_obs, mu, scale, Z, keep))
                draws = [draw_surrogate(gen, run, rng) for _ in range(N_DRAWS_A)]
                sur_rows.append([stats_for(wd, m, sc, z, keep) for wd, m, sc, z in draws])
                # rest / movement / transition diagnostics
                diag_j["obs_trans"] = transitions(w_obs)
                diag_j["sur_trans"] += [transitions(wd) for wd, _, _, _ in draws]
                _, obs_act_lens = episodes(w_obs)
                _, obs_rest_lens = episodes(np.where(w_obs != 0, 0, 1))
                diag_j["obs_act_q"] = (
                    [float(x) for x in np.quantile(obs_act_lens, [0.5, 0.9])]
                    if len(obs_act_lens)
                    else [0.0, 0.0]
                )
                diag_j["obs_rest_q"] = (
                    [float(x) for x in np.quantile(obs_rest_lens, [0.5, 0.9])]
                    if len(obs_rest_lens)
                    else [0.0, 0.0]
                )
                diag_j["sur_act_q"] += [
                    [float(x) for x in np.quantile(episodes(wd)[1], [0.5, 0.9])]
                    if episodes(wd)[0]
                    else [0.0, 0.0]
                    for wd, _, _, _ in draws
                ]
                diag_j["sur_rest_q"] += [
                    [float(x) for x in np.quantile(rest_episode_lengths(wd), [0.5, 0.9])]
                    if len(rest_episode_lengths(wd))
                    else [0.0, 0.0]
                    for wd, _, _, _ in draws
                ]
                act_obs = w_obs[w_obs != 0]
                diag_j["obs_amp_q"] = (
                    [float(x) for x in np.quantile(act_obs, [0.05, 0.5, 0.95])]
                    if len(act_obs)
                    else [0.0, 0.0, 0.0]
                )
                diag_j["sur_amp"] += [
                    [float(x) for x in np.quantile(wd[wd != 0], [0.05, 0.5, 0.95])]
                    if (wd != 0).any()
                    else [0.0, 0.0, 0.0]
                    for wd, _, _, _ in draws
                ]
            # per-date: mean over runs of observed; mean over runs of per-run median over draws
            OBS[j] = {t: float(np.mean([o[t] for o in obs_rows])) for t in tol_stats}
            M[j] = {
                t: float(np.mean([np.median([s[t] for s in rows]) for rows in sur_rows]))
                for t in tol_stats
            }
            diag[j] = {
                "fit_dates": fit_dates,
                "p01_fit": gen["p01"],
                "p10_fit": gen["p10"],
                "obs_p01_p10": diag_j["obs_trans"],
                "sur_p01_median": float(np.median([x[0] for x in diag_j["sur_trans"]])),
                "sur_p10_median": float(np.median([x[1] for x in diag_j["sur_trans"]])),
                "obs_rest_len_q50_q90": diag_j["obs_rest_q"],
                "sur_rest_len_q50_median": float(np.median([x[0] for x in diag_j["sur_rest_q"]])),
                "sur_rest_len_q90_median": float(np.median([x[1] for x in diag_j["sur_rest_q"]])),
                "obs_act_len_q50_q90": diag_j["obs_act_q"],
                "sur_act_len_q50_median": float(np.median([x[0] for x in diag_j["sur_act_q"]])),
                "sur_act_len_q90_median": float(np.median([x[1] for x in diag_j["sur_act_q"]])),
                "obs_amp_q05_q50_q95": diag_j["obs_amp_q"],
                "sur_amp_q50_median": [
                    float(np.median([x[k] for x in diag_j["sur_amp"]])) for k in range(3)
                ],
            }
        # C1 for held-out date d
        s_T = {t: float(np.std([OBS[j][t] for j in train_dates], ddof=1)) for t in tol_stats}
        checks = {}
        for j in train_dates:
            checks[j] = {
                t: {
                    "OBS": OBS[j][t],
                    "m": M[j][t],
                    "abs_dev": abs(OBS[j][t] - M[j][t]),
                    "limit_2s": 2 * s_T[t],
                    "pass": bool(abs(OBS[j][t] - M[j][t]) <= 2 * s_T[t]),
                }
                for t in tol_stats
            }
        admissible = all(checks[j][t]["pass"] for j in train_dates for t in tol_stats)
        out["A"]["per_date"][d] = {
            "s_T": s_T,
            "checks": checks,
            "diagnostics": diag,
            "cpu_seconds_so_far": round(cpu_used(), 2),
        }
        out["A"]["admissible"][d] = bool(admissible)
        _save(out)
        print(f"[A] held-out {d}: admissible={admissible} cpu={cpu_used():.1f}s", flush=True)

    # Oracle C6: uses test-date wheel statistics; descriptive only; never changes admissibility.
    for d in dates:
        if cpu_used() > BUDGET_CPU_S:
            out["A"]["oracle_stopped"] = "CPU budget reached in oracle block"
            return
        train_dates = [x for x in dates if x != d]
        gen = fit_generator([r for x in train_dates for r in runs_by_date[x]])
        o_rows, s_rows = [], []
        for run in runs_by_date[d]:
            w_obs = aligned_target(run.wheel)
            Z = nuisance_lags(run)
            keep = keep_rows(run)
            mu = np.column_stack([np.ones(len(Z)), Z]) @ gen["coef"]
            scale = scale_vector(gen["profile"], len(Z))
            o_rows.append(stats_for(w_obs, mu, scale, Z, keep))
            draws = [draw_surrogate(gen, run, rng) for _ in range(N_DRAWS_A)]
            s_rows.append([stats_for(wd, m, sc, z, keep) for wd, m, sc, z in draws])
        sT = out["A"]["per_date"][d]["s_T"]
        z = {}
        for t in ("S1", "S3", "S4", "S5", "S6"):
            O_d = float(np.mean([o[t] for o in o_rows]))
            m_d = float(np.mean([np.median([s[t] for s in rows]) for rows in s_rows]))
            z[t] = {
                "O_test": O_d,
                "m_surrogate": m_d,
                "z": (O_d - m_d) / sT[t] if sT[t] > 0 else None,
            }
        out["A"]["oracle_C6"][d] = z
        _save(out)
        print(f"[A] oracle {d} done cpu={cpu_used():.1f}s", flush=True)


# ---------------------------------------------------------------------------
# Block B: candidate B, C3-B
# ---------------------------------------------------------------------------


def run_block_B(out: dict) -> None:
    dev, _ = C.read_primary_runs()
    rng = np.random.default_rng(SEED_SYNTH)
    boot_rng = np.random.default_rng(SEED_BOOT)
    reps = []
    k = 0
    for rep in range(N_REPS_B):
        if cpu_used() > BUDGET_CPU_S:
            out["B"] = {**out.get("B", {}), "stopped": f"CPU budget reached after {rep} replicates"}
            break
        synth_runs, _ = P.synth("zero_effect", dev, rng)
        dates, deltas, counts = CP.date_deltas(synth_runs)
        s = CP.summarise(deltas, counts, boot_rng)
        support = bool(s["pooled_delta"] > 0 and s["boot95"][0] > 0)
        k += int(support)
        reps.append(
            {
                "rep": rep,
                "pooled_delta": s["pooled_delta"],
                "boot95": list(s["boot95"]),
                "support": support,
            }
        )
        if (rep + 1) % 10 == 0:
            print(f"[B] {rep + 1}/{N_REPS_B} K={k} cpu={cpu_used():.1f}s", flush=True)
    n_done = len(reps)
    flag = "INFLATION FLAG" if k >= K_FLAG else "NO GROSS INFLATION DETECTED"
    out["B"] = {
        "code": git_head(),
        "seed_synth": SEED_SYNTH,
        "seed_bootstrap": SEED_BOOT,
        "replicates_planned": N_REPS_B,
        "replicates_done": n_done,
        "K": k,
        "rule": f"INFLATION FLAG if K >= {K_FLAG} of {N_REPS_B}, else NO GROSS INFLATION DETECTED",
        "outcome": flag if n_done == N_REPS_B else f"INCOMPLETE ({n_done}/{N_REPS_B})",
        "not_calibration": True,
        "replicates": reps,
        "cpu_seconds_so_far": round(cpu_used(), 2),
        **{kk: v for kk, v in out.get("B", {}).items() if kk in ("stopped",)},
    }
    _save(out)
    print(f"[B] K={k}/{n_done} outcome={out['B']['outcome']}", flush=True)


def _save(out: dict) -> None:
    out["cpu_seconds_total"] = round(cpu_used(), 2)
    out["cpu_hours_total"] = round(cpu_used() / 3600.0, 4)
    out["budget_cpu_hours"] = 0.3
    (EXP / "pilot_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    which = ORIG_ARGV[1] if len(ORIG_ARGV) > 1 and ORIG_ARGV[1] in ("A", "B", "all") else "all"
    out: dict = {}
    if (EXP / "pilot_results.json").exists():
        out = json.loads((EXP / "pilot_results.json").read_text(encoding="utf-8"))
    t0 = time.time()
    if which in ("A", "all"):
        run_block_A(out, t0)
    if which in ("B", "all") and cpu_used() < BUDGET_CPU_S:
        run_block_B(out)
    _save(out)
    print("cpu hours used:", round(cpu_used() / 3600.0, 4), "of 0.3 budget", flush=True)


if __name__ == "__main__":
    main()
