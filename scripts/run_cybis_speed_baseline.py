"""Own speed-decoding baseline on raw fUS.

Protocol: docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md.

Data: sub-rat1703, sessions ses-20210407, ses-20210412, ses-20210421 (Cybis Pereira et al.,
Zenodo 15476373, CC BY 4.0), fetched into git-ignored data/raw/cybis_pereira_2026/.

Runtime: numpy only. The NIfTI reader below handles NIfTI-1 uncompressed-after-gzip data.
Outputs: docs/results/cybis_speed_baseline.json (small, committed).
"""

from __future__ import annotations

import gzip
import json
import struct
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "cybis_pereira_2026"
ANIMAL = "sub-rat1703"
SESSIONS = ["ses-20210407", "ses-20210412", "ses-20210421"]
SEED = 20261027
LAGS = 5  # frames (0..5), covers about 3 s at 0.6 s per volume
ALPHAS = [1.0, 10.0, 100.0, 1000.0]
KS = [10, 20, 50]
N_BOOT = 1000
N_SHIFT = 500
SHIFT_MIN = 20  # frames
BLOCK = 20  # frames
OUT = REPO / "docs" / "results" / "cybis_speed_baseline.json"

# NIfTI-1 datatype codes we accept
_DTYPES = {2: np.uint8, 4: np.int16, 8: np.int32, 16: np.float32, 64: np.float64, 512: np.uint16}


def read_nifti(path: Path) -> tuple[np.ndarray, tuple[float, ...]]:
    """Read a NIfTI-1 (.nii or .nii.gz) volume. Returns (array in x,y,z,t order, pixdim)."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as fh:
        hdr = fh.read(348)
        if struct.unpack("<i", hdr[:4])[0] != 348:
            raise ValueError(f"{path.name}: not a little-endian NIfTI-1 header")
        dims = struct.unpack("<8h", hdr[40:56])
        dtype_code = struct.unpack("<h", hdr[70:72])[0]
        pixdim = struct.unpack("<8f", hdr[76:108])
        vox_offset = int(struct.unpack("<f", hdr[108:112])[0])
        slope, inter = struct.unpack("<ff", hdr[112:120])
        if dtype_code not in _DTYPES:
            raise ValueError(f"{path.name}: unsupported datatype {dtype_code}")
        shape = tuple(int(d) for d in dims[1 : dims[0] + 1])
        fh.read(vox_offset - 348)
        count = int(np.prod(shape))
        data = np.frombuffer(
            fh.read(count * np.dtype(_DTYPES[dtype_code]).itemsize), dtype=_DTYPES[dtype_code]
        )
    arr = data.reshape(shape, order="F").astype(np.float64)
    if slope not in (0.0, 1.0) or inter != 0.0:
        arr = arr * (slope if slope != 0.0 else 1.0) + inter
    return arr, pixdim


def load_speed(motion_tsv: Path, fus_times: np.ndarray) -> np.ndarray:
    """Running speed (cm/s) from DLC body position, median-filtered over 0.2 s, at fUS times.

    UNKNOWN: whether DLC time zero equals the first fUS volume time. Assumed here and tested in C4.
    """
    rows = motion_tsv.read_text(encoding="utf-8").strip().splitlines()
    header = rows[0].split("\t")
    ix, iy = header.index("body_x"), header.index("body_y")
    vals = np.array([[float(r.split("\t")[ix]), float(r.split("\t")[iy])] for r in rows[1:]])
    fs = 50.0
    t = np.arange(vals.shape[0]) / fs
    win = int(round(0.2 * fs)) | 1
    pad = win // 2
    xs = np.pad(vals, ((pad, pad), (0, 0)), mode="edge")
    med = np.stack(
        [
            np.median(np.lib.stride_tricks.sliding_window_view(xs[:, c], win), axis=1)
            for c in range(2)
        ],
        axis=1,
    )
    step = np.sqrt(np.sum(np.diff(med, axis=0) ** 2, axis=1)) * fs  # cm/s
    speed = np.concatenate([[0.0], step])
    return np.interp(fus_times, t, speed)


def ridge_fit(X: np.ndarray, y: np.ndarray, alpha: float) -> tuple[np.ndarray, float]:
    mu = X.mean(axis=0)
    ym = y.mean()
    Xc = X - mu
    beta = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ (y - ym))
    return beta, float(ym - mu @ beta)


def ridge_predict(X: np.ndarray, beta: np.ndarray, b0: float) -> np.ndarray:
    return X @ beta + b0


def r2(pred: np.ndarray, act: np.ndarray) -> float:
    ss_res = float(np.sum((act - pred) ** 2))
    ss_tot = float(np.sum((act - act.mean()) ** 2))
    return 1.0 - ss_res / ss_tot


def lagged(pcs: np.ndarray, lags: int) -> np.ndarray:
    """PCs at lags 0..lags within one session. Edge rows are dropped by the caller."""
    T = pcs.shape[0]
    cols = [pcs[lags - k : T - k] for k in range(lags + 1)]
    return np.concatenate(cols, axis=1)


def pca_basis(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    mu = X.mean(axis=0)
    _, _, vt = np.linalg.svd(X - mu, full_matrices=False)
    return mu, vt[:k].T


def build(sess_data: dict, train: list[str], test: list[str], k: int) -> tuple:
    """PCA on training sessions only; lagged PC features per session; targets aligned."""
    Xtr_raw = np.concatenate([sess_data[s]["X"] for s in train], axis=0)
    mu, basis = pca_basis(Xtr_raw, k)

    def feats(s: str) -> tuple[np.ndarray, np.ndarray]:
        pcs = (sess_data[s]["X"] - mu) @ basis
        F = lagged(pcs, LAGS)
        y = sess_data[s]["y"][LAGS:]
        return F, y

    tr = [feats(s) for s in train]
    te = [feats(s) for s in test]
    return (
        np.concatenate([f for f, _ in tr]),
        np.concatenate([y for _, y in tr]),
        te,
    )


def select_hyper(sess_data: dict, train: list[str]) -> tuple[float, int, dict]:
    """Inner leave-one-session-out within the training sessions. Test sessions never seen."""
    grid = {}
    for k in KS:
        for a in ALPHAS:
            scores = []
            for held in train:
                inner_tr = [s for s in train if s != held]
                Ftr, ytr, [(Fte, yte)] = build(sess_data, inner_tr, [held], k)
                beta, b0 = ridge_fit(Ftr, ytr, a)
                scores.append(r2(ridge_predict(Fte, beta, b0), yte))
            grid[f"k={k},alpha={a}"] = round(float(np.mean(scores)), 4)
    best = max(grid, key=lambda name: grid[name])
    k_best = int(best.split(",")[0].split("=")[1])
    a_best = float(best.split(",")[1].split("=")[1])
    return a_best, k_best, grid


def circular_block_diff(
    pred1: np.ndarray, pred0: np.ndarray, act: np.ndarray, rng
) -> tuple[float, float]:
    n = act.size
    nb = int(np.ceil(n / BLOCK))
    diffs = np.empty(N_BOOT)
    for i in range(N_BOOT):
        st = rng.integers(0, n, size=nb)
        idx = ((st[:, None] + np.arange(BLOCK)[None, :]).ravel())[:n] % n
        diffs[i] = r2(pred1[idx], act[idx]) - r2(pred0[idx], act[idx])
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    return round(float(lo), 4), round(float(hi), 4)


def main() -> None:
    rng = np.random.default_rng(SEED)
    sess_data: dict[str, dict] = {}
    for s in SESSIONS:
        fus_dir = RAW / "rawdata" / ANIMAL / s / "fus"
        nii = fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.nii.gz"
        js = json.loads(
            (fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.json").read_text(encoding="utf-8")
        )
        vt = np.array(js["VolumeTiming"], dtype=float)
        vol, pixdim = read_nifti(nii)
        # WHY: a mismatch means the stamps and frames do not describe the same volumes
        if vol.shape[-1] != vt.size:
            raise SystemExit(f"{s}: {vol.shape[-1]} frames but {vt.size} VolumeTiming stamps")
        sess_data[s] = {"vol": vol, "vt": vt, "pixdim": pixdim}

    # Voxel selection (protocol amendment A-1): finite values and non-zero temporal variance,
    # per session. The authors' decode-speed "mask-brain" weights file is NOT used (it holds
    # their fitted decoder weights, not a mask).
    for s in SESSIONS:
        vol = sess_data[s]["vol"]
        T = vol.shape[-1]
        flat = vol.reshape(-1, T)
        ok = np.isfinite(flat).all(axis=1) & (flat.std(axis=1) > 0)
        X = flat[ok].T  # T x V
        mu_s = X.mean(axis=0)
        sd_s = X.std(axis=0)
        Xz = (X - mu_s) / sd_s  # per-session z-score (protocol: stated confound)
        y = load_speed(
            RAW
            / "rawdata"
            / ANIMAL
            / s
            / "motion"
            / f"{ANIMAL}_{s}_task-openfield_tracksys-DLC_motion.tsv",
            sess_data[s]["vt"],
        )
        sess_data[s]["X"] = Xz
        sess_data[s]["y"] = y
        sess_data[s]["global"] = X.mean(axis=1)

    results = {"animal": ANIMAL, "sessions": SESSIONS, "lags": LAGS, "folds": []}
    for s in SESSIONS:
        train = [t for t in SESSIONS if t != s]
        a_best, k_best, grid = select_hyper(sess_data, train)
        Ftr, ytr, [(Fte, yte)] = build(sess_data, train, [s], k_best)
        beta, b0 = ridge_fit(Ftr, ytr, a_best)
        p1 = ridge_predict(Fte, beta, b0)
        p0 = np.full_like(yte, ytr.mean())
        r2_m1, r2_m0 = r2(p1, yte), r2(p0, yte)

        # C1: circular shift of the prediction within the held-out session
        n = yte.size
        null = np.array(
            [
                r2(np.roll(p1, int(rng.integers(SHIFT_MIN, n - SHIFT_MIN))), yte)
                for _ in range(N_SHIFT)
            ]
        )
        sd = float(null.std(ddof=1))
        c1 = {
            "null_mean": round(float(null.mean()), 4),
            "null_sd": round(sd, 4),
            "z": round((r2_m1 - float(null.mean())) / sd, 2) if sd > 0 else None,
            "shift_p": round(float((np.sum(null >= r2_m1) + 1) / (N_SHIFT + 1)), 4),
        }
        # C2: paired M1 - M0 with within-session circular-block bootstrap (NOT cross-session)
        lo, hi = circular_block_diff(p1, p0, yte, rng)

        # C5: single regressor, global mean fUS signal with the same lags
        g_tr = [lagged(sess_data[t]["global"][:, None], LAGS) for t in train]
        g_y = [sess_data[t]["y"][LAGS:] for t in train]
        Gtr = np.concatenate(g_tr)
        Gte = lagged(sess_data[s]["global"][:, None], LAGS)
        gb, g0 = ridge_fit(Gtr, np.concatenate(g_y), a_best)
        r2_global = r2(ridge_predict(Gte, gb, g0), yte)

        results["folds"].append(
            {
                "test_session": s,
                "train_sessions": train,
                "selected": {"alpha": a_best, "k": k_best},
                "inner_grid_mean_r2": grid,
                "n_test": int(n),
                "r2_M1_ridge": round(r2_m1, 4),
                "r2_M0_mean": round(r2_m0, 4),
                "C1_shift": c1,
                "C2_paired_diff_M1_minus_M0_block_CI": [lo, hi],
                "C5_global_signal_r2": round(r2_global, 4),
            }
        )
        print(json.dumps(results["folds"][-1]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", OUT.name)  # name only: the console codepage cannot print the full path


if __name__ == "__main__":
    main()
