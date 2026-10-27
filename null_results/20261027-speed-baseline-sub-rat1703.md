# Null result: own speed-decoding baseline on raw fUS (sub-rat1703, three sessions)

Date: 2026-10-27. Protocol: `docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md` (committed `7893a24`, amendment A-1). Milestone: `docs/MILESTONE_CYBIS_SPEED_BASELINE_2026-10-27.md`. Commit: `0228f5d`.

## Outcome

NOT SUPPORTED on this subset. The pre-registered decision rule fails: M1 (ridge on PCs with lags) is not above the mean predictor in every held-out session, and the shift-null z is not above 2 in every session.

Out-of-session r² (M1): 0.0122, 0.0010, −0.0368.

## What was killed

Positive out-of-session prediction of running speed from the fUS voxel time series of sub-rat1703, using per-session z-scoring, PCA and lagged PCs, linear ridge, with leave-one-session-out.

## What was NOT killed

- The predictive association in the authors' own pipeline (their outputs reproduce their quoted maxima; see `docs/MILESTONE_CYBIS_PEREIRA_DECODE_2026-10-27.md`). This baseline uses a different pipeline, so it does not test the published claim.
- Nonlinear or differently regularised decoders: the alpha grid was effectively unregularised (see below), so no regularised linear fit was tested.

## Why the result is weak evidence either way

1. The alpha grid (1, 10, 100, 1000) is poorly scaled for PCs of 14336 z-scored voxels. Inner r² changes by about 0.005 across the grid. A wider grid (up to 1e7) is needed. This is INFERRED from the inner scores and not yet tested.
2. Speed and fUS are not confirmed to be synchronised; the sync check gives no identifiable lag.
3. The motion confound (Doppler artefact from body movement) is not separated.

## Revival condition

A wider, pre-registered alpha grid (dated amendment) and a confirmed DLC–fUS time alignment, rerun on the same three sessions. Or the authors' lag-kernel pipeline, once its t-statistic maps are available (currently not in the archive).
