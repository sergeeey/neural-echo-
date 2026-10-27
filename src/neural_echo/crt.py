"""Conditional and independent tests of wheel information beyond wheel-free nuisance, NE-EXP-001.

Two null procedures on the same data, with identical fold-wise models:

  independent  the test fold's wheel (aligned segment) is block-permuted without conditioning.
               Baseline comparator. It is not a CRT.
  conditional  the test fold's wheel is redrawn as mu(Z) + block-permuted residuals, where mu is an
               OLS fit of wheel on the wheel-free nuisance lags Z, trained on TRAINING dates only.
               An approximate conditional randomisation test (see limitations).

Hypotheses, per held-out date d (leave-one-calendar-date-out):
  H0 (conditional): given Z (eye and pupil, lags 0..6 s), the wheel adds no predictive information
                    about the whole-slice fUS signal on date d.
  H1: it does.

Fixed by training dates only: the full and nuisance ridge models, and mu(Z). The held-out fUS target
never enters any null. Statistic: pooled held-out Δ = L_nuisance − L_full over all folds.

Limitations (stated):
  * Residual block permutation approximates exchangeability of residuals within blocks; not proven.
    This is an approximate conditional randomisation test, not an exact CRT.
  * The first N_LAGS-1 wheel frames have no conditional mean and are kept as observed. In v2 they
    are never scored (EDGE_FRAMES), so the head matters only for v1, where those rows are scored.
  * mu is linear in Z. Non-linear wheel-on-Z dependence is not modelled.
  * The test-run residual uses the training-fitted mu, so no test-fold outcome enters.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from neural_echo.exp001 import (
    N_LAGS,
    RidgeModel,
    aligned_target,
    block_permute,
    combine,
    fit_ridge,
    gaussian_loss,
    lagged_matrix,
    run_stats,
    subset,
)


@dataclass(frozen=True)
class RawRun:
    """One run at frame level. `extra` is optional measured nuisance (e.g. arousal) added to Z."""

    eye: np.ndarray
    pupil: np.ndarray
    wheel: np.ndarray
    y: np.ndarray
    invalid: np.ndarray  # 1 where a frame lies in a masked post-gap segment
    group: str
    extra: np.ndarray | None = None


EDGE_FRAMES = 40  # v2: rows whose frame index is below this are not scored (boundary audit)
N_QUARTERS = 4


def keep_rows(run: RawRun, edge_frames: int = EDGE_FRAMES) -> np.ndarray:
    """Rows scored by the test. edge_frames=20 reproduces v1 (no extra frames dropped)."""
    keep = np.convolve(run.invalid, np.ones(N_LAGS, dtype=int), mode="valid") == 0
    # Row i corresponds to frame i + N_LAGS - 1; drop frames below edge_frames.
    keep[: max(edge_frames - (N_LAGS - 1), 0)] = False
    return keep


def quarter_profile(resids: list[np.ndarray]) -> np.ndarray:
    """Residual scale per quarter of the aligned sequence, pooled over TRAINING runs only."""
    out = np.empty(N_QUARTERS)
    for k in range(N_QUARTERS):
        vals = []
        for r in resids:
            n = len(r)
            vals.append(r[k * n // N_QUARTERS : (k + 1) * n // N_QUARTERS])
        v = np.concatenate(vals)
        out[k] = np.sqrt(np.mean(v * v))
    return out


def scale_vector(profile: np.ndarray, n: int) -> np.ndarray:
    idx = np.minimum((np.arange(n) * N_QUARTERS) // n, N_QUARTERS - 1)
    return profile[idx]


def nuisance_lags(run: RawRun) -> np.ndarray:
    cols = [lagged_matrix(run.eye), lagged_matrix(run.pupil)]
    if run.extra is not None:
        cols.append(lagged_matrix(run.extra))
    return np.hstack(cols)


@dataclass(frozen=True)
class PreparedRun:
    """Objects that do not depend on the wheel draw, computed once per fold."""

    group: str
    keep: np.ndarray
    X_nuis: np.ndarray  # kept rows only
    y: np.ndarray  # kept rows only
    aligned_wheel: np.ndarray
    head_wheel: np.ndarray
    resid: np.ndarray | None  # (aligned_wheel - mu(Z)) / scale; None without conditional model
    scale: np.ndarray | None
    mu: np.ndarray | None  # mu(Z) on aligned frames


def prepare(
    run: RawRun,
    mu_coef: np.ndarray | None,
    profile: np.ndarray | None = None,
    edge_frames: int = EDGE_FRAMES,
) -> PreparedRun:
    Z = nuisance_lags(run)
    resid = scale = mu = None
    if mu_coef is not None:
        mu = np.column_stack([np.ones(len(Z)), Z]) @ mu_coef
        raw = aligned_target(run.wheel) - mu
        if profile is not None:
            scale = scale_vector(profile, len(raw))
            resid = raw / scale
        else:
            resid = raw
    keep = keep_rows(run, edge_frames)
    return PreparedRun(
        group=run.group,
        keep=keep,
        X_nuis=Z[keep],
        y=aligned_target(run.y)[keep],
        aligned_wheel=aligned_target(run.wheel),
        head_wheel=run.wheel[: N_LAGS - 1].copy(),
        resid=resid,
        scale=scale,
        mu=mu,
    )


def draw_wheel(pr: PreparedRun, conditional: bool, rng: np.random.Generator) -> np.ndarray:
    """Full-length wheel series for one draw; the head (first N_LAGS-1 frames) is kept."""
    if not conditional:
        seg = block_permute(pr.aligned_wheel, rng)
    else:
        assert pr.resid is not None and pr.mu is not None
        scale = pr.scale if pr.scale is not None else 1.0
        seg = pr.mu + scale * block_permute(pr.resid, rng)
    return np.concatenate([pr.head_wheel, seg])


@dataclass(frozen=True)
class FoldPlan:
    date: str
    m_full: RidgeModel
    m_nuis: RidgeModel
    mu_coef: np.ndarray | None
    test: list[PreparedRun]
    mu_rows: list[np.ndarray | None]


def build_plans(
    runs: list[RawRun],
    conditional: bool = True,
    standardise: bool = True,
    edge_frames: int = EDGE_FRAMES,
) -> list[FoldPlan]:
    """Fit fold-wise models on training dates only; prepare test runs.

    standardise=True (v2): residual scale profile from TRAINING residuals only.
    standardise=False (v1): raw residuals are permuted (first pilot).
    """
    dates = sorted({r.group for r in runs})
    plans = []
    for d in dates:
        train = [r for r in runs if r.group != d]
        test = [r for r in runs if r.group == d]
        stats, k_nuis = [], 0
        for r in train:
            keep = keep_rows(r, edge_frames)
            Xn = nuisance_lags(r)[keep]
            Xw = lagged_matrix(r.wheel)[keep]
            k_nuis = Xn.shape[1]
            stats.append(run_stats(np.hstack([Xn, Xw]), aligned_target(r.y)[keep]))
        tr = combine(stats)
        m_full = fit_ridge(tr)
        m_nuis = fit_ridge(subset(tr, np.arange(k_nuis)))
        mu_coef = None
        profile = None
        if conditional:
            Z = np.vstack([nuisance_lags(r)[keep_rows(r, edge_frames)] for r in train])
            w = np.concatenate([aligned_target(r.wheel)[keep_rows(r, edge_frames)] for r in train])
            X = np.column_stack([np.ones(len(Z)), Z])
            mu_coef, *_ = np.linalg.lstsq(X, w, rcond=None)
            if standardise:
                train_resids = []
                for r in train:
                    Zt = nuisance_lags(r)
                    mt = np.column_stack([np.ones(len(Zt)), Zt]) @ mu_coef
                    train_resids.append(aligned_target(r.wheel) - mt)
                profile = quarter_profile(train_resids)
        test_prepared = [prepare(r, mu_coef, profile, edge_frames) for r in test]
        plans.append(
            FoldPlan(
                date=d,
                m_full=m_full,
                m_nuis=m_nuis,
                mu_coef=mu_coef,
                test=test_prepared,
                mu_rows=[pr.mu for pr in test_prepared],
            )
        )
    return plans


def loss_delta(
    pr: PreparedRun, wheel: np.ndarray, m_full: RidgeModel, m_nuis: RidgeModel
) -> tuple[float, int]:
    """Sum over kept frames of (L_nuisance − L_full), and the number of kept frames."""
    Xf = np.hstack([pr.X_nuis, lagged_matrix(wheel)[pr.keep]])
    lf = gaussian_loss(pr.y, m_full.predict(Xf), m_full.sigma2)
    ln = gaussian_loss(pr.y, m_nuis.predict(pr.X_nuis), m_nuis.sigma2)
    n = len(pr.y)
    return (ln - lf) * n, n


def pooled_delta(plans: list[FoldPlan], wheels: list[np.ndarray] | None = None) -> float:
    """Pooled held-out Δ. `wheels` lists a replacement wheel per test run, in plan order."""
    total, n, i = 0.0, 0, 0
    for plan in plans:
        for pr in plan.test:
            wheel = None if wheels is None else wheels[i]
            if wheel is None:
                raise ValueError("replacement wheel required")
            t, m = loss_delta(pr, wheel, plan.m_full, plan.m_nuis)
            total += t
            n += m
            i += 1
    return total / n


def observed_delta(plans: list[FoldPlan], runs: list[RawRun]) -> float:
    total, n = 0.0, 0
    for plan in plans:
        test_runs = [r for r in runs if r.group == plan.date]
        for pr, r in zip(plan.test, test_runs, strict=True):
            t, m = loss_delta(pr, r.wheel, plan.m_full, plan.m_nuis)
            total += t
            n += m
    return total / n


def p_value(observed: float, null_values: np.ndarray) -> float:
    """Monte Carlo p-value with the +1 correction; larger Δ is more evidence for the wheel."""
    return float((1 + np.sum(null_values >= observed)) / (len(null_values) + 1))


def null_draws(
    plans: list[FoldPlan], n_draws: int, rng: np.random.Generator, conditional: bool
) -> np.ndarray:
    """Null distribution of pooled Δ. Every draw replaces the wheel of every test run."""
    flat = [pr for plan in plans for pr in plan.test]
    out = np.empty(n_draws)
    for b in range(n_draws):
        wheels = [draw_wheel(pr, conditional, rng) for pr in flat]
        out[b] = pooled_delta(plans, wheels)
    return out


@dataclass(frozen=True)
class TestResult:
    observed: float
    null: np.ndarray
    p: float


def run_test(
    plans: list[FoldPlan],
    runs: list[RawRun],
    n_draws: int,
    rng: np.random.Generator,
    conditional: bool,
) -> TestResult:
    obs = observed_delta(plans, runs)
    nulls = null_draws(plans, n_draws, rng, conditional)
    return TestResult(observed=obs, null=nulls, p=p_value(obs, nulls))
