import numpy as np

from neural_echo.exp001 import (
    N_LAGS,
    RunDesign,
    aligned_target,
    block_permute,
    combine,
    fit_ridge,
    gaussian_loss,
    lagged_matrix,
    leave_one_group_out_delta,
    run_stats,
    window_mean,
)


def test_lagged_matrix_columns_are_lags_in_order() -> None:
    x = np.arange(30, dtype=float)
    X = lagged_matrix(x, n_lags=4)
    # Row 0 corresponds to frame 3: columns x[3], x[2], x[1], x[0].
    assert np.array_equal(X[0], [3.0, 2.0, 1.0, 0.0])
    assert X.shape == (27, 4)
    assert np.array_equal(aligned_target(x, n_lags=4)[:2], [3.0, 4.0])


def test_gram_ridge_matches_direct_standardised_ridge() -> None:
    rng = np.random.default_rng(0)
    X = rng.normal(size=(500, 5)) * np.array([1.0, 3.0, 0.5, 2.0, 1.0]) + 4.0
    y = X @ np.array([0.5, -0.2, 0.0, 1.0, 0.3]) + rng.normal(size=500)
    model = fit_ridge(run_stats(X, y), alpha=1.0)

    # Direct reference: standardise on the same data, ridge with centred target.
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    Z = (X - mu) / sd
    yc = y - y.mean()
    b = np.linalg.solve(Z.T @ Z + 1.0 * np.eye(5), Z.T @ yc)
    beta_ref = b / sd
    assert np.allclose(model.beta, beta_ref, atol=1e-8)
    assert np.isclose(model.intercept, y.mean() - mu @ beta_ref, atol=1e-8)


def test_training_statistics_combine_exactly() -> None:
    rng = np.random.default_rng(1)
    X1, y1 = rng.normal(size=(100, 3)), rng.normal(size=100)
    X2, y2 = rng.normal(size=(80, 3)), rng.normal(size=80)
    together = run_stats(np.vstack([X1, X2]), np.concatenate([y1, y2]))
    parts = combine([run_stats(X1, y1), run_stats(X2, y2)])
    assert np.allclose(together.xtx, parts.xtx)
    assert np.allclose(together.xty, parts.xty)
    assert together.n == parts.n


def test_gaussian_loss_is_minimal_at_true_variance() -> None:
    rng = np.random.default_rng(2)
    y = rng.normal(0, 2.0, size=20000)
    losses = {s2: gaussian_loss(y, np.zeros_like(y), s2) for s2 in (1.0, 4.0, 9.0)}
    assert losses[4.0] < losses[1.0] and losses[4.0] < losses[9.0]


def test_block_permutation_keeps_values_and_block_order_inside_blocks() -> None:
    rng = np.random.default_rng(3)
    s = np.arange(1000, dtype=float)
    p = block_permute(s, rng, block=100)
    assert sorted(p) == sorted(s)
    for i in range(10):
        chunk = p[i * 100 : (i + 1) * 100]
        assert np.all(np.diff(chunk) == 1)  # inner order preserved within each block


def test_window_mean_uses_onset_windows() -> None:
    fs = 10.0
    signal = np.arange(100, dtype=float)  # sample i has time i / 10 s
    onsets = np.array([0.0, 1.0])
    out = window_mean(signal, fs, start=0.0, onsets=onsets, width=0.3)
    assert np.allclose(out, [1.0, 11.0])  # samples 0,1,2 -> mean 1; samples 10,11,12 -> mean 11


def test_strong_injected_effect_is_detected_and_zero_effect_is_not() -> None:
    rng = np.random.default_rng(4)

    def make_runs(effect: float) -> list[RunDesign]:
        runs = []
        for i in range(4):
            T = 1500
            eye = rng.normal(size=T)
            wheel = rng.normal(size=T)
            y = rng.normal(size=T)
            # Smooth the effect so it survives the lag design.
            wheel_eff = np.convolve(wheel, np.ones(3) / 3, mode="same")
            y = y + effect * wheel_eff
            runs.append(
                RunDesign(
                    X_nuis=lagged_matrix(eye, N_LAGS),
                    X_wheel=lagged_matrix(wheel, N_LAGS),
                    y=aligned_target(y, N_LAGS),
                    group=f"d{i}",
                )
            )
        return runs

    strong = leave_one_group_out_delta(make_runs(1.0))
    assert strong["delta_pooled"] > 0.05
    null_runs = make_runs(0.0)
    null = leave_one_group_out_delta(null_runs)
    assert abs(null["delta_pooled"]) < 0.01
