# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. **Not frozen.** A heading is not a freeze. Freezing requires: every blocking item in decision.md resolved or declared with its sensitivity analysis, an independent review returning READY or READY_AS_EXPLORATORY, and manifest.yaml set to FROZEN with the git commit. Any change afterwards needs a dated amendment.

## Dataset (verified 2026-10-26)

- Source: UCL RDR deposit, DOI 10.5522/04/31376338, version 3, licence CC BY-NC 4.0.
- Archive: `sub-ALD002.zip` (5,269,296,348 bytes), MD5 40ac3dd90ad155354390c4968cf973f4 (matches figshare), SHA-256 56c445de19f3beca47f29e4d4a5db57e6411e1eaff2f6cccd80078da33cf48cd. Local path `data/raw/landemard2026/` (git-ignored).
- 17 fUS runs over 9 calendar dates. Per-run timing and integrity are in `timing_integrity.md`.
- Verified: VolumeTiming slope is 0.30013 s per frame, not 0.3 s. A nominal grid is therefore not used.

## Holdout and development (declared before any evaluation)

- **Final holdout: `sub-ALD002_task-awake_acq-ref10_run-2`.** Rule: latest acquisition date in scans.tsv (2023-03-30); that date also holds ref06_run-2; tie broken by the larger experiment_id (3). The holdout is not read before freezing. Its timing is matched (11310 volumes = 11310 onsets) and it is eligible.
- **Development runs eligible for the primary analysis: the 8 runs with matching counts and no unmasked interior gap**, i.e. ref04, ref06_run-1, ref06_run-2, ref08, ref11, ref18, ref20_run-2, ref22. The 8 runs with a count mismatch (ref02, ref10_run-1, ref12, ref14, ref20_run-1, ref23, ref24, ref27) are excluded from the primary analysis (exclusion, not truncation) and form a sensitivity analysis under a declared mapping.
- Dates in the primary development set: 2023-03-15, 03-20, 03-21, 03-23, 03-28, 03-30 (ref06_run-2 is on the holdout date). That is **6 development dates**. The earlier criterion (7 of 9 dates) cannot be met by construction and is **replaced by 5 of 6 dates** (declared here, before any holdout evaluation, as a direct consequence of the timing exclusion).

## Per-run preparation

- Target: whole-slice mean of power-Doppler per frame (linear mean), then a linear detrend fitted to that run's own signal (unsupervised; no wheel or model information).
- Frame times: VolumeTiming onsets as recorded. Frame window [onset, onset + 0.3 s].
- **Edge trimming:** frames with missing physio at the start or end of a run are dropped (0 to 4 frames per run). An interior physio gap excludes the run. Verified: no interior gap in the 8 primary runs' physio.
- **Interval gaps:** intervals above 0.45 s are masked. Samples within 6 s after each gap are not used as lagged predictors or targets. (ref04 has a 3.9 s gap; ref11 has seven gaps up to 0.93 s.)
- Clock alignment (declared assumption): wheel and eye/pupil zero both at their StartTime reference. Shift sensitivity: −2, −1, +1, +2 s applied to the wheel. The primary analysis uses shift 0.
- Edge-frame rule: the first 20 frames (6 s lag window) are dropped from all fits and scores.

## Models

- Predictor of interest: signed wheel velocity at lags 0 to 6 s (frame offsets), wheel leads the fUS signal.
- Wheel-free nuisance: eye movement and pupil size, same lags. Pupil normalised by session median (per sidecar).
- Ridge on standardised features. **alpha = 1.0, fixed.** Standardisation from training runs only.
- Predictive distribution: Gaussian, mean from the model, variance = residual variance on training rows, separately per model.

## Primary metric and sign

- L = mean over held-out frames of −log N(y | ŷ, σ²).
- **Δ = L_nuisance − L_full. Positive = the wheel-including model predicts better.**
- Primary evaluation: leave-one-calendar-date-out over the 6 primary development dates.
- Consistency criterion: **Δ > 0 on at least 5 of the 6 primary development dates** (replaces 7 of 9; see above).

## Null distribution

- Block permutation of signed wheel velocity within each run, in 120 s blocks, 1000 permutations on the holdout procedure, seed 20261026.
- Buffers: a 60 s exclusion on each side of any held-out block in within-run blocked evaluation; at leave-one-date-out fold boundaries, training frames within 60 s of a held-out run are removed.
- Observed Δ is compared with the 95th percentile of permuted Δ.

## Final holdout procedure (one shot)

- Fit once on the 8 primary development runs with frozen settings; score the holdout once (eligible, matched); compute Δ and the null from the same fitted settings; no re-fitting, threshold change or lag choice after seeing it.

## Sensitivity analyses (declared, reported, not used for selection)

- The 8 excluded mismatched runs under mapping "first t onsets" and under mapping "drop first onset".
- Clock shifts −2, −1, +1, +2 s applied to the wheel.
- Speed (absolute velocity) instead of signed velocity; centre-of-window sensitivity (onset + 0.15 s); R² gain in place of Δ.

## Synthetic controls (see decision.md)

The synthetic positive and negative controls (`scripts/run_nex001_controls.py`, results in `controls_results.json`) run the same procedure on simulated fUS signals with known truth, built from real development wheel, eye and pupil series. They test calibration of the null and power, but not the real signal.

## Leakage controls

- No regressor derived from the fUS target; no registration-based motion regressor; no authors' precomputed products (`Compact_data_regions_*.npz`).
- Whisking excluded from the wheel-free set (its sidecar says it is estimated from motion SVD and wheel velocity).

## Estimand direction (fixed)

- Target: fUS. Predictor: wheel velocity. The study is a **neurovascular prediction / coupling audit**, not decoding of wheel activity. Wheel activity is not the target.

## Detectability (estimand-ops rule)

- Independent units in the primary analysis: 1 mouse. Dates are not independent units of a mouse.
- A replication across the 5 animals (participants.tsv) would have an exact sign-test minimum of 0.0625, so alpha 0.05 is not attainable at mouse level. Power 0.8 is not claimed.
- MDE: UNKNOWN. MCID: not set.

## Amendments

None. The change of the date criterion (7 of 9 → 5 of 6) and the exclusion of mismatched runs are made before any holdout evaluation and are declared here as a consequence of the timing audit.
