# Decision

Status: **RUNNING** (synthetic stress test). No real-signal result is produced or used. Holdout not read.

## Minimal discriminating set (run 2026-10-27)

Source: `experiments/20261026-ne-exp-001-fusi-measurement-ceiling/discriminate_results.json`. 40 replicates × 50 block permutations, seed 20261027, no wheel effect in truth, full rule (margin AND ≥ 5 of 6 dates), Wilson 95% intervals on the rate.

| Condition | Detections | Rate | Wilson 95% |
|---|---|---|---|
| 1. no confounder, no effect (implementation null) | 1/40 | 0.025 | [0.004, 0.129] |
| 2. hidden arousal (r = 0.5 with wheel), not in design | 39/40 | 0.975 | [0.871, 0.996] |
| 3. same arousal, added to nuisance | 1/40 | 0.025 | [0.004, 0.129] |

## Decision rule (fixed before reading) and reading

Rule: if 1 is nominal, 2 is detected, and 3 is nominal, the failure is non-identifiability. If 3 remains detected, the implementation is suspect.

Outcome: **the rule is met.** The procedure responds to a hidden confound and returns to the nominal level when that confound is measured.

Limits of this reading:
- Condition 3 is correct by construction: the measured regressor is the generating confounder. It shows the implementation handles a correctly specified nuisance; it does not show the absence of a separate wheel effect in real data.
- Condition 1 is nominal only within the precision of 40 replicates (interval up to 0.129).
- The earlier wheel-specific failure is therefore an identifiability limit of the observational design, not a demonstrated bug.

## Null validity (`experiments/20261026-ne-exp-001-fusi-measurement-ceiling/null_conditional_check.json`)

Zero-effect truth, 10 replicates × 50 permutations, same seed family:

| Null | Mean threshold (q95) | Margin false positives |
|---|---|---|
| Independent wheel block permutation | 0.000304 | 1/10 |
| Eye-conditional block permutation | 0.000368 (≈ +21%) | 0/10 |

Reading: the independent null gives a lower threshold by about 21%. This is the expected direction if the independent null destroys the wheel–eye dependence that contributes to Δ variance. At 10 replicates the false-positive counts are not a comparison (differences of 0.1 are noise). The threshold difference is the informative quantity, and it is material for borderline results. The eye-conditional null is the more conservative choice; it must be checked with adequate replicates before NE-EXP-001 is frozen, which needs owner approval for compute.

- Conditional null: permutes wheel residuals after in-run OLS on the wheel-free nuisance lags (eye and pupil, 0–6 s), then adds the fit back. Preserves the eye-explained part of the wheel.
- Temporal structure: 120 s blocks (≈5 × τ_max) preserve within-block autocorrelation. Stated, not formally proven.
- Leakage: the residualisation uses only each run's wheel, eye and pupil; the fUS target is never used. It is built transductively over all primary runs rather than per fold. This choice is declared, and a fold-wise version is required before any freeze.
- Power: 10 replicates detect differences in false-positive rate of the order of 0.2, not 0.02. The comparison is a consistency check only.

## What would change this decision

- A conditional null that differs materially from the independent null would change which null the protocol should use before freezing NE-EXP-001.
- Measured-confounder condition 3 remaining detected would reopen the implementation.

## Compute

No scaling beyond these runs. Profiling (NE-EXP-001 notes): ≈150 ms per permutation; caching would help. Any larger run needs owner approval.
