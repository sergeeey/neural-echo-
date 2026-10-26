# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. **Not frozen.** A heading is not a freeze. Freezing requires: every blocking item in decision.md resolved, an independent scientific review returning READY or READY_AS_EXPLORATORY, and manifest.yaml set to FROZEN with a git commit. Any change afterwards needs a dated amendment.

## Dataset (verified 2026-10-26)

- Source: UCL RDR deposit, DOI 10.5522/04/31376338, version 3, licence CC BY-NC 4.0.
- Archive: `sub-ALD002.zip` (5,269,296,348 bytes). MD5 matches figshare (40ac3dd90ad155354390c4968cf973f4). SHA-256 56c445de19f3beca47f29e4d4a5db57e6411e1eaff2f6cccd80078da33cf48cd. Local path `data/raw/landemard2026/` (git-ignored).
- 17 fUS runs (9 calendar dates), each with wheel, whisking and eye files, and an angiography volume (static, see below).
- Per run, verified from sidecars: wheel 1000 Hz (start 0 s); whisking and eye at 60.024, 60.06 or 30.012 Hz with start between −11.7 and −24.7 s; fUS frame duration 0.3 s; `VolumeTiming` length 8339 to 11344.

## Holdout and development (declared before any evaluation)

- **Final holdout: `sub-ALD002_task-awake_acq-ref10_run-2`.** Rule: the latest acquisition date in scans.tsv (2023-03-30); two runs share that date, and the tie is broken by the larger experiment_id (3). Never read in any analysis before freezing. The autocorrelation audit excluded it by name and asserted the 16 development runs.
- **Development: the other 16 runs.**
- Grouping levels (what each supports):
  - run: a single acquisition; repeated measures within a day (not independent days);
  - calendar date: 9 groups; runs within a date are not independent days;
  - subject: 1 mouse in the primary analysis, so no between-animal generalisation is possible here.
- Primary evaluation: leave-one-calendar-date-out over the 9 dates, restricted to development runs. Secondary: leave-one-run-out, reported with its stated limitation.

## Timing (see decision.md for the open checks)

- Frame time = `VolumeTiming` onset. ConfUSIus (third-party implementation) defines `VolumeTiming` as "onset time of each volume in seconds" and the default reference as `start`. The official fUSI-BIDS text was not verified.
- Frame window = [onset, onset + 0.3 s]. Centre-of-window sensitivity: onset + 0.15 s.
- **Length mismatch:** in 8 of 16 development runs, `VolumeTiming` has one more element than NIfTI volumes. Rule before freezing: the mapping (drop last onset, or other) must be decided on development data and fixed. Until then, frames are matched only by the first t onsets and the mismatch is reported.
- Physio clock: the BIDS physio text fetched does not define the zero of `StartTime`. Alignment between physio and fUS is UNVERIFIED. Lag 0 is not interpreted.
- Resampling: each run to its own windows, using its own physio sampling rate and start. A run is included only if wheel and eye/pupil cover at least 99% of its windows (rule applied before evaluation).

## Autocorrelation and blocks (development data only)

- Whole-slice signal, linearly detrended per run. Integrated autocorrelation time (truncated at first crossing of 0.05):
  - median 49 frames (≈15 s); maximum 76 frames (≈23 s) across the 16 development runs.
  - Autocorrelation at lag 20 frames (6 s) is 0.33 to 0.54.
- **Permutation block length: 120 s** (≈5 × τ_max). **Buffer: 60 s** on each side of any evaluation block (≈2 × τ_max plus the 6 s lag window).
- These values are estimated on development data and are fixed before freezing. They are not tuned on the holdout.

## Models

- Target Y: whole-slice power-Doppler per frame, detrended and standardised **on training runs only**.
- Predictor of interest: signed wheel velocity, lags 0 to 6 s (frame offsets), fixed.
- Wheel-free nuisance: eye movement and pupil size (pupil normalised by the run median, per sidecar), same lags.
- Ridge regression on standardised features. **Penalty alpha = 1.0, fixed.** Sensitivity over 0.1 and 10 is reported and not used for selection.
- Predictive distribution: Gaussian, mean from the model, variance estimated on training runs.

## Primary metric: held-out log loss (consistent sign)

- L = −mean log N(y | ŷ, σ²) over held-out frames.
- Primary difference: Δ = L_nuisance − L_full. **Positive means the fUSI-plus-wheel model predicts better.** This is the sign used everywhere.
- Secondary: R² gain, speed-based sensitivity, number of held-out dates with Δ > 0.
- Null: block-permuted wheel control (120 s blocks, 60 s buffers), repeated many times, giving the null distribution of Δ. The observed Δ is compared with it.

## Descriptive checks (not tests)

- Lag profile (lag 0 versus 1 to 3 s): reported descriptively; not interpreted until timing is verified.
- Angiography-based motion estimate: **not used as an input.** A static angiogram cannot give per-frame motion (see decision.md, motion audit).

## Leakage controls

- No regressor derived from the fUS target. No registration-based motion regressor (it would use the target images).
- No authors' precomputed products (`Compact_data_regions_*.npz`).
- Whisking excluded from the wheel-free set: its sidecar says it is estimated from motion SVD **and wheel velocity**.

## Detectability (estimand-ops rule)

- Independent units for the primary analysis: 1 mouse. Dates are not independent units.
- Exact sign test over 5 mice: minimum two-sided p = 0.0625. Alpha 0.05 is therefore not attainable at mouse level with 5 animals. Power 0.8 is not claimed.
- MDE: UNKNOWN until development results are summarised.
- MCID: **not set.** No basis exists for one (see decision.md).

## Amendments

None.
