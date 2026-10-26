# Estimand

Classification: **EXPLORATORY**. Status PLANNED.

## Primary estimand (predictive, not causal)

- **Population:** sub-ALD002, 16 development runs (holdout run excluded; see protocol.md). Other mice: a separate replication step, not part of the primary estimand. The 5-mouse count comes from participants.tsv (read).
- **Target Y:** whole-slice power-Doppler per frame, detrended within training runs only.
- **Predictor of interest:** signed wheel velocity, lags 0 to 6 s, resampled to each run's VolumeTiming windows.
- **Nuisance:** eye movement and pupil size, same lag basis, same resampling.
- **Summary measure (sign fixed):** held-out R² of (eye + pupil + wheel) minus held-out R² of (eye + pupil), pooled over runs, compared with the block-permutation null. Positive means wheel velocity adds predictive information.
- **Intercurrent events:** runs failing the 99% coverage rule are excluded from both models, before evaluation.

## Secondary (exploratory only)

- Speed (absolute wheel velocity) as a sensitivity analysis.
- Binary wheel-state decoding: needs a threshold and minimum bout length, neither set. Not part of the claim.

## Not used

- The authors' precomputed products (`Compact_data_regions_*.npz`). Analysing them would analyse the authors' analysis.
- Whisking as a wheel-free regressor (its definition uses wheel velocity).

## Natural language statement (write before results)

> We estimate the pooled held-out R² gain from adding wheel velocity to eye and pupil signals when predicting whole-slice power-Doppler in sub-ALD002 development runs, compared with a block-permutation null.

## What this result does NOT mean

1. It does NOT show that fUSI decodes thoughts, intentions or any internal state.
2. It does NOT show neurovascular coupling: body motion and locomotion-related blood flow are not excluded.
3. It does NOT generalise beyond one mouse, and does NOT generalise to humans.
4. It does NOT show a causal role of blood volume in locomotion.
