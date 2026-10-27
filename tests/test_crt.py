import numpy as np

from neural_echo.crt import (
    EDGE_FRAMES,
    RawRun,
    build_plans,
    draw_wheel,
    keep_rows,
    loss_delta,
    null_draws,
    observed_delta,
    p_value,
    pooled_delta,
)
from neural_echo.exp001 import (
    N_LAGS,
    aligned_target,
    block_permute,
    combine,
    fit_ridge,
    gaussian_loss,
    lagged_matrix,
    run_stats,
    subset,
)


def _runs(seed: int, n_dates: int = 3, T: int = 4000) -> list[RawRun]:
    rng = np.random.default_rng(seed)
    runs = []
    for d in range(n_dates):
        eye = rng.normal(size=T)
        pupil = rng.normal(size=T)
        wheel = rng.normal(size=T)
        y = 0.5 * wheel + rng.normal(size=T)
        invalid = np.zeros(T, dtype=int)
        invalid[300:306] = 1  # one masked post-gap segment
        runs.append(RawRun(eye, pupil, wheel, y, invalid, group=f"d{d}"))
    return runs


def _naive_rows(r: RawRun, wheel: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Design rows built from raw series with the v2 edge rule (independent of the cached path)."""
    conv = np.convolve(r.invalid, np.ones(N_LAGS, dtype=int), mode="valid") == 0
    conv[: EDGE_FRAMES - (N_LAGS - 1)] = False
    Xn = np.hstack([lagged_matrix(r.eye), lagged_matrix(r.pupil)])[conv]
    Xw = lagged_matrix(wheel)[conv]
    y = aligned_target(r.y)[conv]
    return Xn, Xw, y


def _naive_delta(runs: list[RawRun], test_wheels: dict[int, np.ndarray]) -> float:
    """Refit every fold from raw series, then score the test runs with the replaced wheels."""
    total, n = 0.0, 0
    for d in sorted({r.group for r in runs}):
        stats, k_nuis = [], 0
        for r in runs:
            if r.group == d:
                continue
            Xn, Xw, y = _naive_rows(r, r.wheel)
            k_nuis = Xn.shape[1]
            stats.append(run_stats(np.hstack([Xn, Xw]), y))
        tr = combine(stats)
        m_full = fit_ridge(tr)
        m_nuis = fit_ridge(subset(tr, np.arange(k_nuis)))
        for i, r in enumerate(runs):
            if r.group != d:
                continue
            Xn, Xw, y = _naive_rows(r, test_wheels[i])
            lf = gaussian_loss(y, m_full.predict(np.hstack([Xn, Xw])), m_full.sigma2)
            ln = gaussian_loss(y, m_nuis.predict(Xn), m_nuis.sigma2)
            total += (ln - lf) * len(y)
            n += len(y)
    return total / n


def test_observed_matches_pooled_with_real_wheel() -> None:
    runs = _runs(0)
    plans = build_plans(runs)
    real = [r.wheel for plan in plans for r in [x for x in runs if x.group == plan.date]]
    assert np.isclose(observed_delta(plans, runs), pooled_delta(plans, real), rtol=0, atol=1e-12)


def test_cached_path_equals_naive_recompute_for_a_draw() -> None:
    """Optimised scoring equals a full naive recompute for the same draws (v1 residuals)."""
    runs = _runs(1)
    plans = build_plans(runs, standardise=False)
    rng = np.random.default_rng(7)
    flat = [pr for plan in plans for pr in plan.test]
    wheels = [draw_wheel(pr, True, rng) for pr in flat]
    fast = pooled_delta(plans, wheels)
    test_runs = [r for plan in plans for r in runs if r.group == plan.date]
    naive = _naive_delta(runs, {i: w for i, w in enumerate(wheels)})
    assert len(test_runs) == len(wheels)
    assert np.isclose(fast, naive, rtol=0, atol=1e-9), (fast, naive)


def test_edge_rows_before_frame_40_are_not_scored() -> None:
    runs = _runs(5)
    keep = keep_rows(runs[0])
    assert not keep[: EDGE_FRAMES - (N_LAGS - 1)].any()
    assert keep[EDGE_FRAMES - (N_LAGS - 1) + 10]


def test_conditional_mean_uses_training_dates_only() -> None:
    runs = _runs(2)
    base = build_plans(runs)
    d_last = sorted({r.group for r in runs})[-1]
    changed = [
        RawRun(
            r.eye, r.pupil, r.wheel, r.y + 100.0 if r.group == d_last else r.y, r.invalid, r.group
        )
        for r in runs
    ]
    alt = build_plans(changed)
    b = {p.date: p.mu_coef for p in base}
    a = {p.date: p.mu_coef for p in alt}
    bd, ad = b[d_last], a[d_last]
    assert bd is not None and ad is not None
    assert np.allclose(bd, ad), "mu for the altered date used its own outcome"


def test_scale_profile_does_not_use_the_test_run() -> None:
    """The residual scale of a test run must be unchanged when that run's wheel is altered."""
    runs = _runs(6)
    base = build_plans(runs)
    d_last = sorted({r.group for r in runs})[-1]
    altered = [
        RawRun(
            r.eye,
            r.pupil,
            r.wheel * 5.0 if r.group == d_last else r.wheel,
            r.y,
            r.invalid,
            r.group,
        )
        for r in runs
    ]
    alt = build_plans(altered)
    s_base = [pr.scale for p in base if p.date == d_last for pr in p.test][0]
    s_alt = [pr.scale for p in alt if p.date == d_last for pr in p.test][0]
    assert s_base is not None and s_alt is not None
    assert np.allclose(s_base, s_alt), "scale profile used the test run"


def test_conditional_draw_is_standardised_residual_permutation() -> None:
    """(draw - mu) / scale permutes the standardised residuals (block scheme property)."""
    runs = _runs(3)
    plans = build_plans(runs)
    rng = np.random.default_rng(11)
    pr = plans[0].test[0]
    draw = draw_wheel(pr, True, rng)[N_LAGS - 1 :]
    assert pr.mu is not None and pr.scale is not None and pr.resid is not None
    standardised = (draw - pr.mu) / pr.scale
    assert np.allclose(np.sort(standardised), np.sort(pr.resid))


def test_head_wheel_is_kept_in_draws() -> None:
    runs = _runs(8)
    plans = build_plans(runs)
    rng = np.random.default_rng(3)
    pr = plans[0].test[0]
    draw = draw_wheel(pr, True, rng)
    assert np.array_equal(draw[: N_LAGS - 1], pr.head_wheel)


def test_p_value_bounds_and_direction() -> None:
    null = np.arange(99, dtype=float)
    assert p_value(1000.0, null) == 1 / 100
    assert p_value(-1.0, null) == 1.0
    assert 0 < p_value(50.0, null) <= 1


def test_strong_real_effect_gives_small_p_and_no_effect_does_not() -> None:
    rng = np.random.default_rng(5)

    def make(effect: float) -> list[RawRun]:
        out = []
        for d in range(4):
            T = 4000
            w = rng.normal(size=T)
            y = effect * np.convolve(w, np.ones(3) / 3, mode="same") + rng.normal(size=T)
            out.append(
                RawRun(
                    rng.normal(size=T),
                    rng.normal(size=T),
                    w,
                    y,
                    np.zeros(T, dtype=int),
                    group=f"d{d}",
                )
            )
        return out

    strong = make(1.0)
    plans = build_plans(strong)
    obs = observed_delta(plans, strong)
    nulls = null_draws(plans, 40, np.random.default_rng(9), conditional=True)
    assert p_value(obs, nulls) <= 0.05

    weak = make(0.0)
    plans0 = build_plans(weak)
    obs0 = observed_delta(plans0, weak)
    nulls0 = null_draws(plans0, 40, np.random.default_rng(9), conditional=True)
    assert p_value(obs0, nulls0) > 0.05


def test_v1_flags_disable_standardisation_and_edge_exclusion() -> None:
    """v1 reproduction by flags: no residual scaling, frame 20 is scored again."""
    runs = _runs(9)
    plans = build_plans(runs, standardise=False, edge_frames=20)
    pr = plans[0].test[0]
    assert pr.scale is None
    assert keep_rows(runs[0], edge_frames=20)[0]
    assert not keep_rows(runs[0])[0]


def test_test_outcome_does_not_change_fold_models_or_null_draws() -> None:
    """Altering the held-out outcome of one date changes no fitted parameter and no null draw."""
    runs = _runs(10)
    d_last = sorted({r.group for r in runs})[-1]
    changed = [
        RawRun(
            r.eye, r.pupil, r.wheel, r.y + 50.0 if r.group == d_last else r.y, r.invalid, r.group
        )
        for r in runs
    ]
    base = build_plans(runs)
    alt = build_plans(changed)
    bp = [p for p in base if p.date == d_last][0]
    ap = [p for p in alt if p.date == d_last][0]
    # Fitted parameters come from training dates only, so they must not move.
    assert np.allclose(bp.m_full.beta, ap.m_full.beta)
    assert np.allclose(bp.m_nuis.beta, ap.m_nuis.beta)
    assert bp.m_full.sigma2 == ap.m_full.sigma2
    assert bp.mu_coef is not None and ap.mu_coef is not None
    assert np.allclose(bp.mu_coef, ap.mu_coef)
    # Null draws of the wheel depend on Z and the wheel only, never on the outcome.
    # (The statistic itself does use y, so the Δ values are not compared.)
    for pb, pa in zip(bp.test, ap.test, strict=True):
        wb = draw_wheel(pb, True, np.random.default_rng(42))
        wa = draw_wheel(pa, True, np.random.default_rng(42))
        assert np.array_equal(wb, wa)


def test_v2_draw_is_mu_plus_scale_times_permuted_residual() -> None:
    """Pins the alignment of mu, scale and resid: the draw is exactly mu + scale * resid[perm]."""
    runs = _runs(11)
    plans = build_plans(runs)
    pr = plans[0].test[0]
    assert pr.mu is not None and pr.scale is not None and pr.resid is not None
    idx = block_permute(np.arange(len(pr.resid)), np.random.default_rng(5)).astype(int)
    draw = draw_wheel(pr, True, np.random.default_rng(5))
    assert np.allclose(draw[N_LAGS - 1 :], pr.mu + pr.scale * pr.resid[idx])


def test_test_wheel_does_not_change_fold_models_mu_or_scale() -> None:
    """Changing the held-out wheel moves no training-fitted object (models, mu, scale)."""
    runs = _runs(12)
    d_last = sorted({r.group for r in runs})[-1]
    changed = [
        RawRun(
            r.eye,
            r.pupil,
            r.wheel * 3.0 if r.group == d_last else r.wheel,
            r.y,
            r.invalid,
            r.group,
        )
        for r in runs
    ]
    bp = [p for p in build_plans(runs) if p.date == d_last][0]
    ap = [p for p in build_plans(changed) if p.date == d_last][0]
    assert np.allclose(bp.m_full.beta, ap.m_full.beta)
    assert np.allclose(bp.m_nuis.beta, ap.m_nuis.beta)
    assert bp.mu_coef is not None and ap.mu_coef is not None
    assert np.allclose(bp.mu_coef, ap.mu_coef)
    assert bp.test[0].scale is not None and ap.test[0].scale is not None
    assert np.allclose(bp.test[0].scale, ap.test[0].scale)


def test_loss_delta_is_finite_and_counts_rows() -> None:
    runs = _runs(4)
    plans = build_plans(runs)
    pr = plans[0].test[0]
    run = [x for x in runs if x.group == plans[0].date][0]
    t, n = loss_delta(pr, run.wheel, plans[0].m_full, plans[0].m_nuis)
    assert n == len(pr.y)
    assert np.isfinite(t)
