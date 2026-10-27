"""Protocol amendment A-2 rerun of the speed baseline.

Protocol: docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md (amendment A-2).

Reuses the frozen functions of scripts/run_cybis_speed_baseline.py. The first result
(docs/results/cybis_speed_baseline.json, commit 0228f5d) is not overwritten; this writes
docs/results/cybis_speed_baseline_A2.json.

A-2 changes, all declared before this run:
- alpha grid 1e0..1e7 (log-spaced);
- sync lag in [-3, +3] volumes chosen from the TRAINING sessions of each fold (and of each inner
  fold), then speed is aligned as y_aligned[t] = speed[t - lag];
- C5 uses the z-scored global mean (the first run used the raw mean; recorded as a deviation);
- C6 motion-proxy control: frame-to-frame change magnitude of the z-scored global signal, lags 0..5,
  ridge with alpha chosen on training sessions only.
Decision rule unchanged.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "cybis_pereira_2026"
ANIMAL = "sub-rat1703"
SESSIONS = ["ses-20210407", "ses-20210412", "ses-20210421"]
SEED = 20261028  # new seed for A-2; declared with the amendment
LAGS = 5
ALPHAS_A2 = [10.0**e for e in range(0, 8)]
KS = [10, 20, 50]
MAX_SYNC_LAG = 3
N_BOOT = 1000
N_SHIFT = 500
SHIFT_MIN = 20
BLOCK = 20
OUT = REPO / "docs" / "results" / "cybis_speed_baseline_A2.json"


def _load_frozen():
    path = REPO / "scripts" / "run_cybis_speed_baseline.py"
    spec = importlib.util.spec_from_file_location("frozen_baseline", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = _load_frozen()


def xcorr(a: np.ndarray, b: np.ndarray, max_lag: int) -> dict[int, float]:
    """r(lag) = corr(a[t], b[t + lag])."""
    out = {}
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = a[: a.size - lag], b[lag:]
        else:
            x, y = a[-lag:], b[: b.size + lag]
        out[lag] = float(np.corrcoef(x, y)[0, 1])
    return out


def best_lag(sd: dict, train: list[str]) -> int:
    """Lag maximising |mean r| over TRAINING sessions only."""
    curves = [xcorr(sd[s]["speed"], sd[s]["gz"], MAX_SYNC_LAG) for s in train]
    mean = {lag: float(np.mean([c[lag] for c in curves])) for lag in curves[0]}
    return max(mean, key=lambda lag: abs(mean[lag]))


def aligned(y: np.ndarray, lag: int) -> np.ndarray:
    """y_aligned[t] = y[t - lag], with edges clipped."""
    idx = np.clip(np.arange(y.size) - lag, 0, y.size - 1)
    return y[idx]


def with_target(sd: dict, names: list[str], lag: int) -> dict:
    out = {}
    for s in names:
        out[s] = {"X": sd[s]["X"], "y": aligned(sd[s]["speed"], lag), "global": sd[s]["gz"]}
    return out


def select(sd: dict, train: list[str]) -> tuple[float, int]:
    """Inner leave-one-session-out over TRAINING sessions; lag re-chosen inside each inner fold."""
    grid = {}
    for k in KS:
        for a in ALPHAS_A2:
            scores = []
            for held in train:
                inner_tr = [s for s in train if s != held]
                lag = best_lag(sd, inner_tr)
                shifted = with_target(sd, train, lag)
                Ftr, ytr, [(Fte, yte)] = F.build(shifted, inner_tr, [held], k)
                beta, b0 = F.ridge_fit(Ftr, ytr, a)
                scores.append(F.r2(F.ridge_predict(Fte, beta, b0), yte))
            grid[(k, a)] = float(np.mean(scores))
    k_best, a_best = max(grid, key=lambda key: grid[key])
    return a_best, k_best


def circular_block_diff(p1, p0, act, rng) -> tuple[float, float]:
    n = act.size
    nb = int(np.ceil(n / BLOCK))
    d = np.empty(N_BOOT)
    for i in range(N_BOOT):
        st = rng.integers(0, n, size=nb)
        idx = ((st[:, None] + np.arange(BLOCK)[None, :]).ravel())[:n] % n
        d[i] = F.r2(p1[idx], act[idx]) - F.r2(p0[idx], act[idx])
    lo, hi = np.quantile(d, [0.025, 0.975])
    return round(float(lo), 4), round(float(hi), 4)


def load_sessions() -> dict:
    sd: dict = {}
    for s in SESSIONS:
        fus_dir = RAW / "rawdata" / ANIMAL / s / "fus"
        js = json.loads(
            (fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.json").read_text(encoding="utf-8")
        )
        vt = np.array(js["VolumeTiming"], dtype=float)
        vol, _ = F.read_nifti(fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.nii.gz")
        T = vol.shape[-1]
        if T != vt.size:
            raise SystemExit(f"{s}: {T} frames but {vt.size} stamps")
        flat = vol.reshape(-1, T)
        ok = np.isfinite(flat).all(axis=1) & (flat.std(axis=1) > 0)
        X = flat[ok].T
        Xz = (X - X.mean(axis=0)) / X.std(axis=0)
        gz = Xz.mean(axis=1)
        speed = F.load_speed(
            RAW
            / "rawdata"
            / ANIMAL
            / s
            / "motion"
            / f"{ANIMAL}_{s}_task-openfield_tracksys-DLC_motion.tsv",
            vt,
        )
        sd[s] = {"X": Xz, "speed": speed, "gz": gz, "n_voxels": int(ok.sum()), "T": int(T)}
    return sd


def main() -> None:
    rng = np.random.default_rng(SEED)
    sd = load_sessions()
    results = {"amendment": "A-2", "seed": SEED, "alphas": ALPHAS_A2, "ks": KS, "folds": []}
    for s in SESSIONS:
        train = [t for t in SESSIONS if t != s]
        a_best, k_best = select(sd, train)
        lag = best_lag(sd, train)  # chosen from training sessions only
        shifted = with_target(sd, SESSIONS, lag)

        Ftr, ytr, [(Fte, yte)] = F.build(shifted, train, [s], k_best)
        beta, b0 = F.ridge_fit(Ftr, ytr, a_best)
        p1 = F.ridge_predict(Fte, beta, b0)
        p0 = np.full_like(yte, ytr.mean())
        r2_m1, r2_m0 = F.r2(p1, yte), F.r2(p0, yte)

        n = yte.size
        null = np.array(
            [
                F.r2(np.roll(p1, int(rng.integers(SHIFT_MIN, n - SHIFT_MIN))), yte)
                for _ in range(N_SHIFT)
            ]
        )
        sd_null = float(null.std(ddof=1))
        c1 = {
            "null_mean": round(float(null.mean()), 4),
            "z": round((r2_m1 - float(null.mean())) / sd_null, 2) if sd_null > 0 else None,
            "shift_p": round(float((np.sum(null >= r2_m1) + 1) / (N_SHIFT + 1)), 4),
        }
        lo, hi = circular_block_diff(p1, p0, yte, rng)

        # C5: z-scored global mean with the same lags (A-2 definition)
        g_tr = np.concatenate([F.lagged(sd[t]["gz"][:, None], LAGS) for t in train])
        g_y = np.concatenate([shifted[t]["y"][LAGS:] for t in train])
        g_b, g_0 = F.ridge_fit(g_tr, g_y, a_best)
        r2_c5 = F.r2(F.ridge_predict(F.lagged(sd[s]["gz"][:, None], LAGS), g_b, g_0), yte)

        # C6: motion proxy = frame-to-frame change magnitude of the global signal
        m_tr = np.concatenate([_motion_feat(sd, t) for t in train])
        m_te = _motion_feat(sd, s)
        c6_alpha = max(ALPHAS_A2, key=lambda a: _inner_m(sd, train, a))
        mb, m0 = F.ridge_fit(m_tr, g_y, c6_alpha)
        r2_c6 = F.r2(F.ridge_predict(m_te, mb, m0), yte)

        fold = {
            "test_session": s,
            "train_sessions": train,
            "sync_lag_volumes_train": lag,
            "selected": {"alpha": a_best, "k": k_best},
            "n_test": int(n),
            "r2_M1_ridge": round(r2_m1, 4),
            "r2_M0_mean": round(r2_m0, 4),
            "C1_shift": c1,
            "C2_M1_minus_M0_block_CI_within_session": [lo, hi],
            "C5_global_zscore_r2": round(r2_c5, 4),
            "C6_motion_proxy_r2": round(r2_c6, 4),
            "C6_alpha": c6_alpha,
        }
        results["folds"].append(fold)
        print(json.dumps(fold), flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", OUT.name)


def _motion_feat(sd: dict, name: str) -> np.ndarray:
    """C6 predictor: lagged frame-to-frame change magnitude of the z-scored global signal."""
    g = sd[name]["gz"]
    return F.lagged(np.abs(np.diff(g, prepend=g[0]))[:, None], LAGS)


def _inner_m(sd: dict, train: list[str], alpha: float) -> float:
    """Inner leave-one-session-out r² of the C6 model at one alpha; lag re-chosen per inner fold."""
    scores = []
    for held in train:
        inner_tr = [t for t in train if t != held]
        lag_i = best_lag(sd, inner_tr)
        Mtr = np.concatenate([_motion_feat(sd, t) for t in inner_tr])
        ytr = np.concatenate([aligned(sd[t]["speed"], lag_i)[LAGS:] for t in inner_tr])
        Mte = _motion_feat(sd, held)
        yte = aligned(sd[held]["speed"], lag_i)[LAGS:]
        b, b0 = F.ridge_fit(Mtr, ytr, alpha)
        scores.append(F.r2(F.ridge_predict(Mte, b, b0), yte))
    return float(np.mean(scores))


if __name__ == "__main__":
    main()
