# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. **Not frozen.** A heading is not a freeze. Freezing requires: every blocking item in decision.md resolved or explicitly declared as an assumption with its sensitivity analysis, an independent review returning READY or READY_AS_EXPLORATORY, and manifest.yaml set to FROZEN with the git commit. Any change afterwards needs a dated amendment.

## Dataset (verified 2026-10-26)

- Source: UCL RDR deposit, DOI 10.5522/04/31376338, version 3, licence CC BY-NC 4.0.
- Archive: `sub-ALD002.zip` (5,269,296,348 bytes). MD5 matches figshare (40ac3dd90ad155354390c4968cf973f4). SHA-256 56c445de19f3beca47f29e4d4a5db57e6411e1eaff2f6cccd80078da33cf48cd. Local path `data/raw/landemard2026/` (git-ignored).
- 17 fUS runs over 9 calendar dates; each run has wheel, whisking and eye files and a fUS NIfTI. Per run (verified from sidecars): wheel 1000 Hz, start 0 s; whisking and eye 60.024, 60.06 or 30.012 Hz, start −11.7 to −24.7 s; fUS frame duration 0.3 s; VolumeTiming length 8339 to 11344; ClutterFilterWindowDuration 0.6 s.
- The angiography volume is static (no time axis) and is not used as an input.

## Holdout and development

- **Final holdout: `sub-ALD002_task-awake_acq-ref10_run-2`.** Rule: latest acquisition date in scans.tsv (2023-03-30); that date also contains ref06_run-2, so the tie is broken by the larger experiment_id (3). The holdout is not read before freezing.
- **Development: the other 16 runs.**
- Grouping: calendar date is the unit of leave-one-out (9 dates); runs within a date are not independent days. The development part of the 2023-03-30 date (ref06_run-2) is a development run.
- **Final holdout test (fixed procedure):** fit once on all 16 development runs with the frozen settings; score the holdout once; compute Δ on the holdout and compare it with the holdout-specific null (block permutation of the holdout's wheel, 1000 permutations, seed 20261026). No re-fitting, threshold change, or lag choice after seeing the holdout.

## Per-run preparation (applied identically to all 17 runs)

- Target: whole-slice mean of the power-Doppler values per frame (linear mean, no log transform), then a linear detrend fitted to that run's own signal. This is unsupervised and uses no wheel or model information.
- Frame times: onset from VolumeTiming (start reference, see decision.md). The frame window is [onset, onset + 0.3 s]. Lags are measured in frames.
- **VolumeTiming mapping (declared assumption):** the first t onsets are matched to the t NIfTI volumes, where t is the NIfTI time dimension. Where VolumeTiming is longer (8 of 16 development runs), the extra final onset is discarded. The alternative mapping (drop first onset) is a pre-declared sensitivity analysis, reported and not used to choose.
- **Clock alignment (declared assumption):** wheel and eye/pupil zero are both taken as the physio StartTime reference, unverified. Sensitivity: shifts of −2 s, −1 s, +1 s, +2 s applied to the wheel only, reported. The primary analysis uses shift 0.
- **Edge frames:** the first 20 frames of each run (6 s, the lag window) are dropped from all fits and scores, because their lags reach before the recording start. This is applied to every run.
- Coverage rule: wheel and eye/pupil must cover at least 99% of the retained windows. Runs failing it are excluded from both models before evaluation (applied before any evaluation).

## Models

- Predictor of interest: **signed wheel velocity at lags 0 to 6 s only** (wheel leads the fUS signal). Lags of the fUS signal are not used. Lag grid: 0 to 6 s in steps of one frame (0.3 s).
- Wheel-free nuisance: eye movement and pupil size (pupil normalised by the **session** median, per sidecar), same lag grid.
- Ridge regression on standardised features. **alpha = 1.0, fixed.** Standardisation is fitted on the training runs only.
- Predictive distribution: Gaussian with mean from the model; **variance is the residual variance on the training runs of that model**, separately for nuisance-only and wheel-including models.

## Primary metric

- L = mean over held-out frames of −log N(y | ŷ, σ²).
- **Δ = L_nuisance − L_full. Positive = the wheel-including model predicts better.** This sign is used everywhere.
- Primary evaluation: leave-one-calendar-date-out over the 9 dates, restricted to development runs; Δ is pooled over the held-out dates.
- Consistency criterion (pre-declared): Δ > 0 on at least 7 of the 9 held-out dates.

## Null distribution

- Block permutation of signed wheel velocity within each run, in 120 s blocks, 1000 permutations, seed 20261026, applied to the development runs.
- Buffers: a 60 s exclusion on each side of any held-out block, both in permutation tests and at the boundaries of leave-one-date-out folds (training frames within 60 s of a held-out fold are removed).
- The observed Δ is compared with the 95th percentile of the permuted Δ.

## Descriptive and sensitivity analyses (not tests)

- R² gain (same models); speed (absolute velocity) instead of signed velocity; alternative VolumeTiming mapping; clock-shift sensitivity; centre-of-window sensitivity (onset + 0.15 s).
- Lag profile at lag 0 versus lags 1 to 3 s: descriptive only; lag-0 interpretation depends on the open timing convention.

## Leakage controls

- No regressor derived from the fUS target. No registration motion regressor. No authors' precomputed products (`Compact_data_regions_*.npz`).
- Whisking excluded from the wheel-free set (its sidecar says it is estimated from motion SVD **and wheel velocity**).

## Detectability (estimand-ops rule)

- Independent units in the primary analysis: 1 mouse. Calendar dates are not independent units of a mouse.
- The 5-mouse bound (exact two-sided sign test minimum 0.0625) applies only to a future replication across the 5 animals listed in participants.tsv. It does not apply to the 1-mouse primary analysis; the EXPLORATORY label rests on the replication bound and on the absence of an independent reference.
- Power 0.8 is not claimed. MDE: UNKNOWN until development results are summarised. MCID: not set.

## Amendments

None.
