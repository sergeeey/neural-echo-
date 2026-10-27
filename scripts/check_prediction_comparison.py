"""Out-of-sample prediction comparison across dates, with no wheel null and no fUS holdout.

Statistic per held-out date d: the mean per-frame held-out loss difference, nuisance minus full
model (positive = the wheel helps), from the same fold-wise models as the CRT. Uncertainty comes
from the six dates themselves: an exact two-sided sign test on the date-level signs and a
bootstrap over dates. This answers a predictive question only; it does not separate wheel
information from a correlated unmeasured variable and does not test temporal specificity.

Synthetic calibration (no permutation): under zero_effect the sign-test false-positive rate
should be near or below its nominal level; hidden_arousal and known_added_info show what the
rule does with an association that is confounded versus a real wheel effect.
"""

from __future__ import annotations

import importlib.util
import sys
from math import comb
from pathlib import Path

import numpy as np

from neural_echo.crt import RawRun, build_plans, loss_delta

REPO = Path(__file__).resolve().parent.parent
sys.argv = ["pilot", "1", "19", "2"]  # import-time argv only
_spec = importlib.util.spec_from_file_location(
    "pilot", REPO / "scripts" / "run_nex001_crt_pilot.py"
)
assert _spec is not None and _spec.loader is not None
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

N_REPS_SYNTH = 20
BOOT = 2000


def sign_test_two_sided(k_pos: int, n: int) -> float:
    """Exact two-sided sign test p-value for k_pos positive out of n (ties excluded upstream)."""
    k = min(k_pos, n - k_pos)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / 2**n
    return min(1.0, 2 * tail)


def date_deltas(
    runs: list[RawRun], wheels: list[np.ndarray] | None = None
) -> tuple[list[str], list[float], list[int]]:
    """Per-date mean loss difference (nuisance minus full), using `wheels` or the observed wheel."""
    plans = build_plans(runs, conditional=True, standardise=True, edge_frames=40)
    dates, deltas, counts = [], [], []
    i = 0
    for plan in plans:
        total, n = 0.0, 0
        test_runs = [r for r in runs if r.group == plan.date]
        for pr, r in zip(plan.test, test_runs, strict=True):
            w = r.wheel if wheels is None else wheels[i]
            i += 1
            t, m = loss_delta(pr, w, plan.m_full, plan.m_nuis)
            total += t
            n += m
        dates.append(plan.date)
        deltas.append(total / n)
        counts.append(n)
    return dates, deltas, counts


def summarise(deltas: list[float], counts: list[int], rng: np.random.Generator) -> dict:
    d = np.array(deltas)
    w = np.array(counts, dtype=float)
    pos = int(np.sum(d > 0))
    neg = int(np.sum(d < 0))
    n_sign = pos + neg
    p = sign_test_two_sided(pos, n_sign) if n_sign else 1.0
    pooled = float(np.sum(d * w) / np.sum(w))
    boot = np.empty(BOOT)
    for b in range(BOOT):
        idx = rng.integers(0, len(d), len(d))
        boot[b] = np.sum(d[idx] * w[idx]) / np.sum(w[idx])
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return {
        "pooled_delta": pooled,
        "boot95": (float(lo), float(hi)),
        "dates_positive": pos,
        "dates_negative": neg,
        "sign_p_two_sided": p,
    }


def main() -> None:
    dev, _ = P.C.read_primary_runs()
    # The real fUS outcome is not used here: NE-EXP-001 is BLOCKED, and this script only checks the
    # inference rule on synthetic outcomes built from the real wheel, eye and pupil.
    rng = np.random.default_rng(31)
    print("synthetic calibration, 20 replicates per scenario (no permutation):")
    for name in ("zero_effect", "hidden_arousal", "known_added_info"):
        hits, pooled_vals = 0, []
        for _ in range(N_REPS_SYNTH):
            synth_runs, _ = P.synth(name, dev, rng)
            _, d, c = date_deltas(synth_runs)
            s = summarise(d, c, rng)
            hits += int(s["sign_p_two_sided"] <= 0.05)
            pooled_vals.append(s["pooled_delta"])
        print(
            f"{name}: sign-test p<=0.05 in {hits}/{N_REPS_SYNTH}; "
            f"mean pooled delta {np.mean(pooled_vals):.5f}"
        )


if __name__ == "__main__":
    main()
