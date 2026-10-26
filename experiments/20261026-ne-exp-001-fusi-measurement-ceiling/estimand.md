# Estimand

Classification: **EXPLORATORY**. Status PLANNED. Consistent with protocol.md (the protocol is authoritative for numbers).

## Primary estimand (predictive, not causal)

- **Population:** sub-ALD002, the 16 development runs (holdout excluded). The 5-mouse count comes from participants.tsv (read); other mice are a separate, unrun replication step.
- **Target Y:** whole-slice power-Doppler per frame, detrended and standardised on training runs only.
- **Predictor of interest:** signed wheel velocity, lags 0 to 6 s, resampled to each run's VolumeTiming windows (mapping rule open, see decision.md).
- **Nuisance:** eye movement and pupil size, same lags.
- **Summary measure (sign fixed):** Δ = L_nuisance − L_full, where L is the held-out mean negative Gaussian log predictive density. **Positive means the wheel-including model predicts better.** Compared with a block-permutation null (120 s blocks, 60 s buffers).
- **Intercurrent events:** runs failing the 99% coverage rule are excluded from both models before evaluation.

## Secondary (exploratory only)

- R² gain (same models): reported, not decisive.
- Speed (absolute wheel velocity) sensitivity.
- Binary wheel-state decoding: needs a threshold and bout length, neither set. Not part of the claim.

## Not used

- The authors' precomputed products (`Compact_data_regions_*.npz`).
- Whisking as a wheel-free regressor (its definition uses wheel velocity).
- The angiography volume as a motion input (static; cannot give per-frame motion).

## Natural language statement (write before results)

> We estimate the held-out log-loss difference, nuisance-only minus wheel-including, for whole-slice power-Doppler in sub-ALD002 development runs, leave-one-calendar-date-out, compared with a block-permutation null.

## What this result does NOT mean

1. It does NOT show that fUSI decodes thoughts, intentions or any internal state.
2. It does NOT show neurovascular coupling: body motion and locomotion-linked blood flow are not excluded.
3. It does NOT generalise beyond one mouse, and does NOT generalise to humans.
4. It does NOT show a causal role of blood volume in locomotion.
