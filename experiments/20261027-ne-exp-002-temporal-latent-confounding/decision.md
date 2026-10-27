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

## CRT v2 validation gate (2026-10-27): verdict REVISE

Pre-registered criteria applied as written (see `crt_comparison.md`, `crt_run_provenance.md`):
- Null inflation: none flagged (largest v2 conditional null rejection 3/30). Passed.
- Power on known_added_info: 30/30 for both configurations. Passed, but saturated, so not informative about power below the effect size used. The summariser also checks that v2 is not lower than v1-config by more than 0.10 on paired replicates (per the plan; not in the shortened criteria list above).
- Diagnostics: quarter variance ratio after standardisation median 2.50 (criterion 1.5) and block variance ratio median about 6.3 x 10^4 (criterion 3). **Failed.**

Verdict: **REVISE.** Negative result recorded in `null_results/20261027-ne-exp-002-crt-v2-distribution.md`.

Status of the gate: **closed as REVISE**. The CRT v2 procedure is not validated, and this record is not reopened by later synthetic results.
- The v1 run at 100 replicates (`crt_pilot_v1_full100.json`, summary in `crt_v1_full100_summary.md`) completed and is reported as supplementary. Its numbers (for example measured_arousal 16/100 independent against 4/100 conditional) show that the choice of null changes the rejection rate under a measured confound. They do not validate the conditional procedure, because its surrogates fail the distributional checks above on the development data.
- Provenance is split per run group in `crt_run_provenance.md`. The 30-replicate runs executed the committed code (04267d6; blob hashes match today, launch timing is from the transcript and unverified in the repository); the 100-replicate run did not.
- Consolidated table: `crt_consolidated_results.md` (generated by `scripts/consolidate_crt_results.py`).

Findings (synthetic only; origin of exact zeros UNKNOWN):
- Conditional surrogates do not reproduce the activity state (active fraction 0.96 to 1.00 against 0.09 to 0.24 observed), episode structure (1 to 11 per run against 113 to 410 observed; two-component draws 149 to 248), or the dependence of residual magnitude on physiology (median 0.003 to 0.013 against 0.120; per run the observed correlation ranges from -0.16 to +0.35).
- The exact-zero origin is UNKNOWN (`crt_wheel_raw_audit.txt`: 1000 Hz, no NaN, exact zeros in 80 to 94 percent of samples). The causal chain from zero mass to the failed diagnostics is consistent with the data, not established; alternatives (a)–(e) are listed in `null_results/20261027-ne-exp-002-crt-v2-distribution.md`.
- Independent block permutation keeps episodes but loses the physiology dependence.
- A two-component generator matches the cross-run median active fraction (0.139 against 0.120) but not the episode count (median 219 against 172; per run 149 to 248 against 113 to 410) or the physiology dependence (0.013 against 0.120); per-run active fraction errors range from -48% to +56%. Its state-wise variance agreement holds by construction and is not evidence for the generator. Not validated.
- A date-level prediction comparison has a zero-effect false-positive rate of 4/20 at nominal 0.05 and does not separate a hidden confounder from a real effect. Not a calibrated test.

What would change this decision: a new procedure, pre-registered as a new contract version, that reproduces the activity state, episodes and physiology dependence in surrogates, and an independent check before any real-signal use. No criterion of CRT v2 is changed.

## Compute

No scaling beyond these runs. Profiling (NE-EXP-001 notes): ≈150 ms per permutation; caching would help. Any larger run needs owner approval.
