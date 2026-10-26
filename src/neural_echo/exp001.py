"""NE-EXP-001 analysis primitives: lagged design, Gram-based ridge, Gaussian log loss.

Used on development and synthetic data only; the final holdout stays unused until the protocol is
frozen. Numbers follow experiments/20261026-ne-exp-001-fusi-measurement-ceiling/protocol.md.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

FRAME_S = 0.3
N_LAGS = 21  # lags 0..20 frames, i.e. 0 to 6 s at 0.3 s per frame
ALPHA = 1.0  # ridge penalty, fixed by the protocol
BLOCK_FRAMES = 400  # 120 s permutation block at 0.3 s per frame


def lagged_matrix(x: np.ndarray, n_lags: int = N_LAGS) -> np.ndarray:
    """Return rows t = n_lags-1 .. T-1 with columns x[t], x[t-1], ..., x[t-n_lags+1].

    Frames before the first full lag window are dropped (the protocol's edge-frame rule).
    Row i corresponds to frame i + n_lags - 1 of the input.
    """
    x = np.asarray(x, dtype=float)
    T = len(x)
    cols = [x[n_lags - 1 - k : T - k] for k in range(n_lags)]
    return np.column_stack(cols)


def aligned_target(y: np.ndarray, n_lags: int = N_LAGS) -> np.ndarray:
    """Target rows matching lagged_matrix: frames n_lags-1 .. T-1."""
    return np.asarray(y, dtype=float)[n_lags - 1 :]


@dataclass(frozen=True)
class Stats:
    """Sufficient statistics of a block of rows, so training sets combine without refitting."""

    n: int
    sx: np.ndarray
    sy: float
    xtx: np.ndarray
    xty: np.ndarray
    yty: float


def run_stats(X: np.ndarray, y: np.ndarray) -> Stats:
    return Stats(
        n=X.shape[0],
        sx=X.sum(axis=0),
        sy=float(y.sum()),
        xtx=X.T @ X,
        xty=X.T @ y,
        yty=float(y @ y),
    )


def combine(parts: list[Stats]) -> Stats:
    # WHY: np.sum over stacked arrays keeps the array type; the builtin sum starts from 0.
    return Stats(
        n=int(np.sum([p.n for p in parts])),
        sx=np.sum([p.sx for p in parts], axis=0),
        sy=float(np.sum([p.sy for p in parts])),
        xtx=np.sum([p.xtx for p in parts], axis=0),
        xty=np.sum([p.xty for p in parts], axis=0),
        yty=float(np.sum([p.yty for p in parts])),
    )


def subset(s: Stats, idx: np.ndarray) -> Stats:
    return Stats(
        n=s.n,
        sx=s.sx[idx],
        sy=s.sy,
        xtx=s.xtx[np.ix_(idx, idx)],
        xty=s.xty[idx],
        yty=s.yty,
    )


@dataclass(frozen=True)
class RidgeModel:
    beta: np.ndarray
    intercept: float
    sigma2: float  # residual variance on the training rows

    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.beta + self.intercept


def fit_ridge(tr: Stats, alpha: float = ALPHA) -> RidgeModel:
    """Ridge on standardised features, fitted only from training statistics.

    Minimises sum (y - yhat)^2 + alpha * ||b||^2 on standardised features with centred target.
    """
    n = tr.n
    mu = tr.sx / n
    ybar = tr.sy / n
    cov_xx = tr.xtx / n - np.outer(mu, mu)
    cov_xy = tr.xty / n - mu * ybar
    sd = np.sqrt(np.clip(np.diag(cov_xx), 1e-12, None))
    R = cov_xx / np.outer(sd, sd)
    r = cov_xy / sd
    b = np.linalg.solve(n * R + alpha * np.eye(len(mu)), n * r)
    beta = b / sd
    intercept = ybar - float(mu @ beta)
    var_y = tr.yty / n - ybar * ybar
    sigma2 = float(var_y - 2 * b @ r + b @ R @ b)
    return RidgeModel(beta=beta, intercept=intercept, sigma2=max(sigma2, 1e-12))


def gaussian_loss(y: np.ndarray, yhat: np.ndarray, sigma2: float) -> float:
    """Mean negative log predictive density under a Gaussian with variance sigma2."""
    resid = y - yhat
    return float(np.mean(0.5 * np.log(2 * np.pi * sigma2) + resid * resid / (2 * sigma2)))


@dataclass(frozen=True)
class RunDesign:
    """One run, already lagged: columns [nuisance (eye, pupil) | wheel], plus target and group."""

    X_nuis: np.ndarray
    X_wheel: np.ndarray
    y: np.ndarray
    group: str


def _stats_for(run: RunDesign) -> Stats:
    return run_stats(np.hstack([run.X_nuis, run.X_wheel]), run.y)


def leave_one_group_out_delta(runs: list[RunDesign], alpha: float = ALPHA) -> dict:
    """Primary procedure. Returns pooled Δ and per-group Δ.

    Δ = L_nuisance - L_full, positive when the wheel-including model predicts better.
    Each held-out group is a whole calendar date. Training statistics never see the held-out group.
    """
    k_nuis = runs[0].X_nuis.shape[1]
    full_stats = [_stats_for(r) for r in runs]
    groups = sorted({r.group for r in runs})
    per_group: dict[str, float] = {}
    total_sum = 0.0
    total_n = 0
    for g in groups:
        train_idx = [i for i, r in enumerate(runs) if r.group != g]
        test_idx = [i for i, r in enumerate(runs) if r.group == g]
        tr_full = combine([full_stats[i] for i in train_idx])
        tr_nuis = subset(tr_full, np.arange(k_nuis))
        m_full = fit_ridge(tr_full, alpha)
        m_nuis = fit_ridge(tr_nuis, alpha)
        g_sum = 0.0
        g_n = 0
        for i in test_idx:
            r = runs[i]
            Xf = np.hstack([r.X_nuis, r.X_wheel])
            lf = gaussian_loss(r.y, m_full.predict(Xf), m_full.sigma2)
            ln = gaussian_loss(r.y, m_nuis.predict(r.X_nuis), m_nuis.sigma2)
            g_sum += (ln - lf) * len(r.y)
            g_n += len(r.y)
        per_group[g] = g_sum / g_n
        total_sum += g_sum
        total_n += g_n
    return {
        "delta_pooled": total_sum / total_n,
        "delta_by_group": per_group,
        "n_groups_positive": sum(1 for v in per_group.values() if v > 0),
        "n_groups": len(per_group),
    }


def block_permute(
    series: np.ndarray, rng: np.random.Generator, block: int = BLOCK_FRAMES
) -> np.ndarray:
    """Permute whole blocks of a frame series, keeping within-block order.

    Blocks have lengths in [block, 2*block): the remainder is merged into the last block, so
    every sample is permuted and none is left in place.
    """
    n_blocks = max(len(series) // block, 1)
    edges = np.linspace(0, len(series), n_blocks + 1).astype(int)
    chunks = [series[edges[i] : edges[i + 1]] for i in range(n_blocks)]
    order = rng.permutation(n_blocks)
    return np.concatenate([chunks[i] for i in order])


def window_mean(
    signal: np.ndarray, fs: float, start: float, onsets: np.ndarray, width: float = FRAME_S
) -> np.ndarray:
    """Mean of samples inside [onset, onset + width) per onset; NaN where none falls inside."""
    signal = np.asarray(signal, dtype=float)
    csum = np.concatenate([[0.0], np.cumsum(signal)])
    lo = np.ceil((onsets - start) * fs).astype(int)
    hi = np.ceil((onsets + width - start) * fs).astype(int)
    lo = np.clip(lo, 0, len(signal))
    hi = np.clip(hi, 0, len(signal))
    count = hi - lo
    out = np.full(len(onsets), np.nan)
    ok = count > 0
    out[ok] = (csum[hi[ok]] - csum[lo[ok]]) / count[ok]
    return out
