# Estimand

Classification: **EXPLORATORY** (see decision on statistical feasibility below). Status stays PLANNED.

## Primary estimand (continuous coupling / confound audit)

- **Population:** awake head-fixed mice with the BIDS structure of the Landemard deposit (5 subjects). The primary analysis uses sub-ALD002 only (17 fUS runs, all with wheel, whisking and eye files). Other subjects are a pre-declared replication step, not part of the primary estimand.
- **Target Y:** whole-slice power-Doppler signal per frame (60 x 125 px, 0.3 s frames, VolumeTiming as clock). Detrended within run.
- **Predictor of interest:** wheel velocity (rotary encoder, 1000 Hz, cm/s), resampled to frame times by averaging over each 0.3 s window. Lag basis of 0 to 6 s, fixed in advance.
- **Nuisance set (wheel-free):** eye movement and pupil size (60 Hz), resampled the same way, same lag basis.
- **Sensitivity nuisance:** whisking. The sidecar states that whisking is "estimated from motion SVD and wheel velocity", so it contains wheel information. It is never used in the primary estimand.
- **Summary measure (sign fixed):** held-out R² of (eye + pupil + wheel) minus held-out R² of (eye + pupil). Positive means wheel velocity adds explained variance beyond the wheel-free nuisance set.
- **Intercurrent events:** runs with missing physio are excluded from both models. None is missing in sub-ALD002 (verified by structure audit).

## Secondary (exploratory only)

- **Binary wheel-state decoding:** requires a threshold and minimum bout length. Neither is set. They would be fitted on calibration runs only, never on evaluation runs. Not part of the primary claim.

## Not used

- The authors' precomputed products in `Compact_data_regions_*.npz` (PSTHs, p-values, bouts). Using them would analyse the authors' own analysis, not the raw data.
- Whisking as a wheel-free regressor (see above).

## Natural language statement (write before results)

> We estimate the held-out R² gain from adding wheel velocity to eye and pupil signals when predicting whole-slice power-Doppler in sub-ALD002, using leave-one-run-out and within-run blocked splits.

## What this result does NOT mean

1. It does NOT show that fUSI decodes thoughts, intentions or any internal state.
2. It does NOT generalise beyond one mouse, and does NOT generalise to humans.
3. It does NOT show a causal role of blood volume in locomotion.
4. It does NOT exclude motion artefact from wheel-driven movement (see claim.md, reference-region limitation).
