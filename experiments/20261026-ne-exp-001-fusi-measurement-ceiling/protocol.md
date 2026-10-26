# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. **Not frozen.** Nothing below is fixed until the blocking items in decision.md are resolved, a scientific review returns READY, and manifest.yaml is set to FROZEN. Any change after freezing needs a dated amendment.

## Dataset (verified 2026-10-26)

- Source: UCL RDR deposit, DOI 10.5522/04/31376338, version 3, licence CC BY-NC 4.0.
- Archive used: `sub-ALD002.zip` (5,269,296,348 bytes). MD5 matches the figshare record (40ac3dd90ad155354390c4968cf973f4). SHA-256 56c445de19f3beca47f29e4d4a5db57e6411e1eaff2f6cccd80078da33cf48cd.
- Local path: `data/raw/landemard2026/` (git-ignored, not committed).
- Structure verified: 17 fUS runs, each with wheel, whisking and eye physio files. Wheel 1000 Hz (3410 s). Whisking and eye 60.024 Hz (3417 s, start -12.74 s). fUS frame 0.3 s, VolumeTiming starting 6.948 s, one slice 60 x 125 px, 11307 frames (reference run).
- Not verified: the archive contains no motion signal and no reference region (structure only; no image-based mask has been made).
- The scans table gives date only (no time of day). Session identity: date + experiment_id.

## Split strategy

- Final holdout: the last fUS run of sub-ALD002. It is not inspected in any analysis before freezing, and is excluded from all threshold, lag and model choices.
- Development runs: the other 16 runs, used for choices made before freezing.
- Evaluation: leave-one-run-out across the 16 development runs, plus within-run blocked splits (5 contiguous blocks, 10 s buffer each side).
- Generalisation to other mice: a pre-declared replication step, not part of the primary result.

## Time alignment

- Common clock: fUS VolumeTiming. Wheel (start 0 s) and whisking/eye (start -12.74 s) are resampled onto the fUS frame times by window averaging. The alignment has not been checked against an event; this is an open risk.

## Leakage controls

- Session leakage: no session in both training and evaluation.
- No derivative of the target in any model. The target is the fUS slice signal; no regressor is computed from it.
- No authors' precomputed products (PSTH, p-value, bout files) are used.
- Whisking is excluded from the wheel-free nuisance set, because its definition uses wheel velocity.

## Baselines

- Nuisance-only: eye movement and pupil size, with the same lag basis.
- Chance: predicting the run mean.
- Shuffled control: wheel velocity permuted in blocks of 10 s, to test the whole pipeline.

## Metrics

- Primary: held-out R² gain (eye + pupil + wheel minus eye + pupil), pooled across runs, with an interval from resampling runs.
- Secondary: per-run gain sign count.

## Model and run parameters

- Model class: ridge regression on lagged features. Lag basis 0 to 6 s, fixed here. Penalty chosen only inside the development runs by nested CV. Final penalty fixed before the holdout.
- Random seeds: fixed and recorded.
- Software environment: uv.lock of this repository.

## Detectability (estimand-ops rule)

- n: 1 mouse for the primary analysis; 5 mice for the replication step. 16 development runs as repeated measures, not independent units.
- baseline or sigma: UNKNOWN until development runs are summarised.
- alpha, power: see decision.md. The exact sign test over 5 mice cannot reach two-sided p below 0.0625, so alpha 0.05 is not attainable at mouse level. Power 0.8 is not claimed.
- MDE: UNKNOWN.
- MCID: not set and not justifiable now (see decision.md).

## Amendments

None.
