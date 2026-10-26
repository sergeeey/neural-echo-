# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. **Not frozen.** Nothing below is fixed until the blocking items in decision.md are resolved, a scientific review returns READY or READY_AS_EXPLORATORY, and manifest.yaml is set to FROZEN. Any change after freezing needs a dated amendment.

## Dataset (verified 2026-10-26)

- Source: UCL RDR deposit, DOI 10.5522/04/31376338, version 3, licence CC BY-NC 4.0.
- Archive used: `sub-ALD002.zip` (5,269,296,348 bytes). MD5 matches figshare (40ac3dd90ad155354390c4968cf973f4). SHA-256 56c445de19f3beca47f29e4d4a5db57e6411e1eaff2f6cccd80078da33cf48cd.
- Local path: `data/raw/landemard2026/` (git-ignored, not committed).
- Verified (17 fUS runs, all with wheel, whisking and eye files, from sidecars and scans table):
  - Wheel: 1000 Hz, start 0 s, signed velocity in cm/s.
  - Whisking and eye: 60.024 or 60.06 Hz in most runs, **30.012 Hz in ref12, ref23, ref27**; start between −11.7 and −24.7 s, differing per run.
  - fUS: frame duration 0.3 s; VolumeTiming per run, from 0.056 s (ref22) to 7.27 s; **8339 frames in ref22, 11121 to 11344 in the others**.
- Not verified: whether VolumeTiming marks frame onset or centre (affects lag 0).
- Not verified: the number of subjects beyond participants.tsv (5 rows, read); whether acq-ref codes denote imaging planes.
- Not verified: any motion signal or reference region in the archive. None is listed.

## Holdout and development split (declared before any evaluation)

- **Final holdout: `sub-ALD002_task-awake_acq-ref10_run-2_pwd.nii.gz`.** Rule: the run with the latest acq_time date in scans.tsv; two runs share 2023-03-30, so the tie is broken by the larger experiment_id (3, ref10_run-2 over ref06_run-2). Not inspected in any analysis before freezing.
- **Development: the other 16 runs.** Used for every choice made before freezing.
- Grouping: runs are grouped by acq_time date. Leave-one-day-out over development runs is the primary evaluation. Leave-one-run-out is secondary.
- Within-run blocked check: 5 contiguous blocks with a 10 s buffer on each side. The 10 s buffer exceeds the 6 s lag window; the autocorrelation length of the target is UNVERIFIED and must be measured on development runs before freezing.

## Resampling

- Each run is resampled to its own VolumeTiming windows, using its own physio sampling rate and start time. A nominal 0.3 s grid is not used.
- A run is included only if the wheel and eye/pupil signals cover at least 99% of its VolumeTiming windows. The rule is applied before evaluation.
- Wheel velocity: signed, as recorded. Speed (absolute value) is a sensitivity analysis.

## Models

- Target Y: whole-slice power-Doppler signal per frame, detrended **within training runs only**.
- Predictor of interest: wheel velocity, lags 0 to 6 s (frame offsets from VolumeTiming), fixed.
- Wheel-free nuisance: eye movement and pupil size, same lag basis. Pupil is normalised by the run median (per sidecar); this is not target leakage.
- Ridge regression on standardised features. **Penalty fixed at alpha = 1.0.** Sensitivity over 0.1 and 10 is reported and is not used to select.
- Standardisation fitted on training runs only.

## Null distribution

- Block-permuted wheel control: wheel velocity permuted in 10 s blocks, within each run, repeated many times. This gives the null distribution of the R² gain.
- The pooled observed gain is compared with this null distribution. A gain above the null is reported as "gain above block-permutation null". It is not called a falsification or a discovery.

## Lag profile (pre-declared descriptive check)

- Gain at lag 0 versus lags 1 to 3 s is reported as a descriptive profile. It is not a test. Lag 0 is interpreted only after the VolumeTiming convention is verified.

## Leakage controls

- No derivative of the target in any model. No regressor is computed from the fUS images.
- No authors' precomputed products (PSTH, p-values, bouts) are used.
- Whisking is excluded from the wheel-free set: its sidecar says it is estimated from motion SVD **and wheel velocity**.
- Motion regressors from image registration are **not** used. They would be computed from the target images, which is forbidden here. An alternative motion estimate from the angiography scan (`angio/sub-ALD002_pwd.nii.gz`, independent of the run images) is an open option, and would need a separate decision before freezing.

## Baselines

- Nuisance-only: eye movement and pupil size, same lag basis, same ridge settings.
- Chance: predicting the training mean.
- Block-permuted wheel: null distribution (above).

## Metrics

- Primary: held-out R² gain (eye + pupil + wheel minus eye + pupil), pooled over runs, compared with the null distribution.
- Secondary: number of runs with positive gain; lag profile; speed-based sensitivity.

## Detectability (estimand-ops rule)

- n: 1 mouse for the primary analysis (16 development runs are repeated measures, not independent units).
- Replication across the other 4 mice of participants.tsv is a pre-declared, separate step.
- The exact sign test over 5 mice cannot reach two-sided p below 0.0625, so alpha 0.05 is not attainable at mouse level. Power 0.8 is not claimed.
- MDE: UNKNOWN until development runs are summarised.
- MCID: not set and not justifiable now (see decision.md).

## Amendments

None.
