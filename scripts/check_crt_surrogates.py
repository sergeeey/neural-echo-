"""Do conditional and independent wheel draws keep the structure of the observed wheel?

No fUS outcome is used. For each held-out development run, compare observed aligned wheel with
draws: active fraction, number and mean length of active episodes (nonzero runs), residual
variance given activity (conditional draws only), and corr(|resid|, ||Z||).
"""

import importlib.util
from pathlib import Path

import numpy as np

from neural_echo.crt import build_plans, draw_wheel
from neural_echo.exp001 import N_LAGS, aligned_target

spec = importlib.util.spec_from_file_location(
    "controls", Path("E:/РАБОИЕ ПРОЕКТЫ👌/A-9  Neural Echo/scripts/run_nex001_controls.py")
)
assert spec is not None and spec.loader is not None
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
dev, _ = C.read_primary_runs()
from neural_echo.crt import RawRun  # noqa: E402

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


def episodes(x: np.ndarray) -> tuple[int, float]:
    act = (x != 0).astype(int)
    d = np.diff(np.concatenate([[0], act, [0]]))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    lens = ends - starts
    return len(lens), float(lens.mean()) if len(lens) else 0.0


def stats(w: np.ndarray, mu: np.ndarray | None, scale: np.ndarray | None, Z: np.ndarray) -> dict:
    n_ep, mean_len = episodes(w)
    out = {"active_frac": float(np.mean(w != 0)), "episodes": n_ep, "mean_episode_len": mean_len}
    if mu is not None and scale is not None:
        res = (w - mu) / scale
        act = w != 0
        if act.any() and (~act).any():
            out["resid_var_active"] = float(res[act].var())
            out["resid_var_stationary"] = float(res[~act].var())
        out["corr_abs_resid_Zmag"] = float(
            np.corrcoef(np.abs(res), np.linalg.norm(Z, axis=1))[0, 1]
        )
    return out


plans = build_plans(runs, conditional=True, standardise=True, edge_frames=40)
rng = np.random.default_rng(7)
for plan in plans:
    for pr, r in zip(plan.test, [x for x in runs if x.group == plan.date], strict=True):
        Z = pr.X_nuis  # kept rows only
        obs_seg = aligned_target(r.wheel)[pr.keep]
        obs = stats(
            obs_seg,
            pr.mu[pr.keep] if pr.mu is not None else None,
            pr.scale[pr.keep] if pr.scale is not None else None,
            Z,
        )
        cond = []
        ind = []
        for _ in range(19):
            d = draw_wheel(pr, True, rng)[N_LAGS - 1 :][pr.keep]
            assert pr.mu is not None and pr.scale is not None
            cond.append(stats(d, pr.mu[pr.keep], pr.scale[pr.keep], Z))
            di = draw_wheel(pr, False, rng)[N_LAGS - 1 :][pr.keep]
            ind.append(stats(di, None, None, Z))

        def med(rows: list[dict], key: str) -> float:
            vals = [x[key] for x in rows if key in x and np.isfinite(x[key])]
            return float(np.median(vals)) if vals else float("nan")

        print(
            f"{plan.date} obs active={obs['active_frac']:.3f} ep={obs['episodes']} "
            f"len={obs['mean_episode_len']:.1f} | cond active={med(cond, 'active_frac'):.3f} "
            f"ep={med(cond, 'episodes'):.0f} len={med(cond, 'mean_episode_len'):.1f} "
            f"varA={med(cond, 'resid_var_active'):.4f} "
            f"varS={med(cond, 'resid_var_stationary'):.6f} "
            f"corr={med(cond, 'corr_abs_resid_Zmag'):.3f} | "
            f"ind active={med(ind, 'active_frac'):.3f} "
            f"ep={med(ind, 'episodes'):.0f} len={med(ind, 'mean_episode_len'):.1f}"
        )
        print(
            f"   obs varA={obs.get('resid_var_active', float('nan')):.4f} "
            f"varS={obs.get('resid_var_stationary', float('nan')):.6f} "
            f"corr={obs.get('corr_abs_resid_Zmag', float('nan')):.3f}"
        )
