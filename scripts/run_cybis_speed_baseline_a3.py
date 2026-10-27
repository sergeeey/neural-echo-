"""Protocol amendment A-3 speed baseline: exploratory (stage E) and final (stage F) runs.

Spec: docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md, amendment A-3 (committed 25ddeb6 before
this file was written). Frozen functions are imported from scripts/run_cybis_speed_baseline.py.

Usage:
  python scripts/run_cybis_speed_baseline_a3.py exploratory   # stage E: 3 original sessions, LOSO
  python scripts/run_cybis_speed_baseline_a3.py final         # stage F: fit 3 originals, test 2 new

Outputs: docs/results/cybis_speed_baseline_A3_exploratory.json or
         docs/results/cybis_speed_baseline_A3_final.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "cybis_pereira_2026"
ANIMAL = "sub-rat1703"
ORIGINAL = ["ses-20210407", "ses-20210412", "ses-20210421"]
NEW = ["ses-20210430", "ses-20210505"]
SEED = 20261029
LAGS = 5
SYNC_LAGS = [0, 1, 2, 3, 4, 5]
KS = [10, 20, 50]
ALPHAS = [1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]
N_BOOT = 1000
N_SHIFT = 500
SHIFT_MIN = 20
BLOCK = 20
MATCH_TOL = 0.01


def _load_frozen():
    path = REPO / "scripts" / "run_cybis_speed_baseline.py"
    spec = importlib.util.spec_from_file_location("frozen_baseline", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = _load_frozen()


def load_session(name: str) -> dict:
    fus_dir = RAW / "rawdata" / ANIMAL / name / "fus"
    js = json.loads(
        (fus_dir / f"{ANIMAL}_{name}_task-openfield_pwd.json").read_text(encoding="utf-8")
    )
    vt = np.array(js["VolumeTiming"], dtype=float)
    vol, _ = F.read_nifti(fus_dir / f"{ANIMAL}_{name}_task-openfield_pwd.nii.gz")
    T = vol.shape[-1]
    if T != vt.size:
        raise SystemExit(f"{name}: {T} frames but {vt.size} stamps")
    flat = vol.reshape(-1, T)
    ok = np.isfinite(flat).all(axis=1) & (flat.std(axis=1) > 0)
    X = flat[ok].T
    Xz = (X - X.mean(axis=0)) / X.std(axis=0)
    speed = F.load_speed(
        RAW
        / "rawdata"
        / ANIMAL
        / name
        / "motion"
        / f"{ANIMAL}_{name}_task-openfield_tracksys-DLC_motion.tsv",
        vt,
    )
    dvars = np.sqrt(np.mean(np.diff(Xz, axis=0) ** 2, axis=1))
    dvars = np.concatenate([[dvars[0]], dvars])  # C6: voxelwise DVARS-style proxy
    return {
        "Xz": Xz.astype(np.float32),
        "speed": speed,
        "gz": Xz.mean(axis=1),
        "dvars": dvars,
        "T": int(T),
        "n_voxels": int(ok.sum()),
    }


def pca_state(sd: dict, train: list[str], kmax: int) -> dict:
    """PCA on training sessions only; PC scores standardised by training mean and sd."""
    X = np.concatenate([sd[s]["Xz"] for s in train]).astype(np.float64)
    mu = X.mean(axis=0)
    _, _, vt = np.linalg.svd(X - mu, full_matrices=False)
    basis = vt[:kmax].T
    scores = {s: (sd[s]["Xz"].astype(np.float64) - mu) @ basis for s in train}
    allscore = np.concatenate([scores[s] for s in train])
    pc_mu, pc_sd = allscore.mean(axis=0), allscore.std(axis=0)
    gz_all = np.concatenate([sd[s]["gz"] for s in train])
    dv_all = np.concatenate([sd[s]["dvars"] for s in train])
    return {
        "mu": mu,
        "basis": basis,
        "pc_mu": pc_mu,
        "pc_sd": pc_sd,
        "gz_mu": gz_all.mean(),
        "gz_sd": gz_all.std(),
        "dv_mu": dv_all.mean(),
        "dv_sd": dv_all.std(),
    }


def feats(sd: dict, st: dict, name: str, model: str, k: int) -> np.ndarray:
    if model == "M1":
        pcs = (sd[name]["Xz"].astype(np.float64) - st["mu"]) @ st["basis"][:, :k]
        pcs = (pcs - st["pc_mu"][:k]) / st["pc_sd"][:k]
        return F.lagged(pcs, LAGS)
    if model == "C5":
        g = (sd[name]["gz"] - st["gz_mu"]) / st["gz_sd"]
        return F.lagged(g[:, None], LAGS)
    if model == "C6":
        d = (sd[name]["dvars"] - st["dv_mu"]) / st["dv_sd"]
        return F.lagged(d[:, None], LAGS)
    raise ValueError(model)


def best_lag(sd: dict, train: list[str]) -> int:
    """Sync lag over {0..5} maximising the mean (signed) correlation across TRAINING sessions.

    Convention: y_aligned[t] = speed[t - lag] is correlated with the mean fUS signal at t.
    """
    means = {}
    for lag in SYNC_LAGS:
        rs = []
        for s in train:
            sp, g = sd[s]["speed"], sd[s]["gz"]
            a = sp[: sp.size - lag] if lag else sp
            b = g[lag:] if lag else g
            rs.append(float(np.corrcoef(a, b)[0, 1]))
        means[lag] = float(np.mean(rs))
    return max(means, key=lambda lag: means[lag])


def aligned(y: np.ndarray, lag: int) -> np.ndarray:
    idx = np.clip(np.arange(y.size) - lag, 0, y.size - 1)
    return y[idx]


def build(sd: dict, st: dict, names: list[str], lag: int, model: str, k: int):
    X = np.concatenate([feats(sd, st, s, model, k) for s in names])
    y = np.concatenate([aligned(sd[s]["speed"], lag)[LAGS:] for s in names])
    return X, y


def select(sd: dict, train: list[str], model: str) -> tuple[float, int, dict]:
    """Inner leave-one-session-out over training sessions; lag re-chosen inside each inner fold."""
    grid = {}
    kset = KS if model == "M1" else [KS[0]]
    for k in kset:
        for a in ALPHAS:
            scores = []
            for held in train:
                inner_tr = [s for s in train if s != held]
                lag_i = best_lag(sd, inner_tr)
                st = pca_state(sd, inner_tr, max(kset))
                Xtr, ytr = build(sd, st, inner_tr, lag_i, model, k)
                Xte, yte = build(sd, st, [held], lag_i, model, k)
                beta, b0 = F.ridge_fit(Xtr, ytr, a)
                scores.append(F.r2(F.ridge_predict(Xte, beta, b0), yte))
            grid[f"k={k},alpha={a}"] = round(float(np.mean(scores)), 5)
    best = max(grid, key=lambda name: grid[name])
    k_best = int(best.split(",")[0].split("=")[1])
    a_best = float(best.split(",")[1].split("=")[1])
    return a_best, k_best, grid


def block_ci(p1: np.ndarray, p0: np.ndarray, act: np.ndarray, rng) -> tuple[float, float]:
    n = act.size
    nb = int(np.ceil(n / BLOCK))
    d = np.empty(N_BOOT)
    for i in range(N_BOOT):
        st_ = rng.integers(0, n, size=nb)
        idx = ((st_[:, None] + np.arange(BLOCK)[None, :]).ravel())[:n] % n
        d[i] = F.r2(p1[idx], act[idx]) - F.r2(p0[idx], act[idx])
    lo, hi = np.quantile(d, [0.025, 0.975])
    return round(float(lo), 4), round(float(hi), 4)


def evaluate(sd: dict, train: list[str], test: list[str], rng) -> dict:
    """Fit on train with selected hyperparameters; evaluate on each test session."""
    a1, k1, grid1 = select(sd, train, "M1")
    a5, _, grid5 = select(sd, train, "C5")
    a6, _, grid6 = select(sd, train, "C6")
    lag = best_lag(sd, train)
    st = pca_state(sd, train, max(KS))
    Xtr, ytr = build(sd, st, train, lag, "M1", k1)
    beta, b0 = F.ridge_fit(Xtr, ytr, a1)
    X5, y5 = build(sd, st, train, lag, "C5", KS[0])
    b5, c50 = F.ridge_fit(X5, y5, a5)
    X6, y6 = build(sd, st, train, lag, "C6", KS[0])
    b6, c60 = F.ridge_fit(X6, y6, a6)
    out = {
        "train_sessions": train,
        "sync_lag_volumes": lag,
        "selected": {"M1": [a1, k1], "C5_alpha": a5, "C6_alpha": a6},
        "inner_grid_M1": grid1,
        "inner_grid_C5": grid5,
        "inner_grid_C6": grid6,
        "tests": [],
    }
    for s in test:
        Xte, yte = build(sd, st, [s], lag, "M1", k1)
        p1 = F.ridge_predict(Xte, beta, b0)
        p0 = np.full_like(yte, ytr.mean())
        r2_1, r2_0 = F.r2(p1, yte), F.r2(p0, yte)
        n = yte.size
        null = np.array(
            [
                F.r2(np.roll(p1, int(rng.integers(SHIFT_MIN, n - SHIFT_MIN))), yte)
                for _ in range(N_SHIFT)
            ]
        )
        sdn = float(null.std(ddof=1))
        z = round((r2_1 - float(null.mean())) / sdn, 2) if sdn > 0 else None
        X5t, y5t = build(sd, st, [s], lag, "C5", KS[0])
        X6t, y6t = build(sd, st, [s], lag, "C6", KS[0])
        r2_c5 = F.r2(F.ridge_predict(X5t, b5, c50), y5t)
        r2_c6 = F.r2(F.ridge_predict(X6t, b6, c60), y6t)
        lo, hi = block_ci(p1, p0, yte, rng)
        out["tests"].append(
            {
                "test_session": s,
                "n_test": int(n),
                "r2_M1": round(r2_1, 4),
                "r2_M0": round(r2_0, 4),
                "C1_z": z,
                "C1_shift_p": round(float((np.sum(null >= r2_1) + 1) / (N_SHIFT + 1)), 4),
                "C2_M1_minus_M0_block_CI": [lo, hi],
                "C5_r2": round(r2_c5, 4),
                "C6_r2": round(r2_c6, 4),
                "C5_matches_M1": bool(r2_c5 >= r2_1 - MATCH_TOL),
                "C6_matches_M1": bool(r2_c6 >= r2_1 - MATCH_TOL),
                "M1_beats_M0": bool(r2_1 > r2_0),
                "C1_above_2": bool(z is not None and z > 2),
            }
        )
    return out


def verdict(tests: list[dict]) -> str:
    if not tests:
        return "NO TEST"
    beat = all(t["M1_beats_M0"] for t in tests)
    z2 = all(t["C1_above_2"] for t in tests)
    controls = any(t["C5_matches_M1"] or t["C6_matches_M1"] for t in tests)
    if beat and z2 and not controls:
        return "PASS (decision rule met)"
    if beat and z2 and controls:
        return "CONFOUNDED (controls match M1)"
    return "NOT SUPPORTED"


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in {"exploratory", "final"}:
        raise SystemExit("usage: run_cybis_speed_baseline_a3.py exploratory|final")
    rng = np.random.default_rng(SEED)
    if mode == "exploratory":
        sd = {s: load_session(s) for s in ORIGINAL}
        folds = []
        for held in ORIGINAL:
            train = [s for s in ORIGINAL if s != held]
            res = evaluate(sd, train, [held], rng)
            folds.append(res)
            print(json.dumps(res["tests"][0]), flush=True)
        tests = [f["tests"][0] for f in folds]
        result = {
            "stage": "E",
            "label": "EXPLORATORY (not independent)",
            "seed": SEED,
            "folds": folds,
            "verdict_all_folds": verdict(tests),
        }
        out = REPO / "docs" / "results" / "cybis_speed_baseline_A3_exploratory.json"
    else:
        sd = {s: load_session(s) for s in ORIGINAL + NEW}
        res = evaluate(sd, ORIGINAL, NEW, rng)
        result = {
            "stage": "F",
            "label": "FINAL independent test on unused sessions",
            "seed": SEED,
            "fit_sessions": ORIGINAL,
            "test": res,
            "verdict": verdict(res["tests"]),
        }
        out = REPO / "docs" / "results" / "cybis_speed_baseline_A3_final.json"
        print(json.dumps(res["tests"]), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", out.name)


if __name__ == "__main__":
    main()
