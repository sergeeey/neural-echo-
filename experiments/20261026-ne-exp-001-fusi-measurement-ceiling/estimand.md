# Estimand

Classification: **EXPLORATORY**. Status PLANNED. Protocol.md is authoritative for all numbers.

## Direction of prediction (fixed)

- **Target (Y):** whole-slice power-Doppler per frame (fUS).
- **Predictor (X):** signed wheel velocity at lags 0 to 6 s, plus wheel-free nuisance (eye movement, pupil size).
- The study is therefore a **behaviour-to-fUS prediction audit**: how well wheel-linked behaviour predicts the fUS signal beyond eye and pupil. It is **not** decoding of wheel activity, and it makes no neural claim.

## Primary estimand

- **Population:** sub-ALD002, the 8 count-matched development runs over 6 calendar dates (holdout excluded). Other mice are a separate, unrun replication.
- **Summary measure:** Δ = L_nuisance − L_full, held-out mean negative Gaussian log predictive density. Positive = the wheel-including model predicts better.
- **Intercurrent events:** runs with count mismatch are excluded (exclusion, not truncation); interval gaps are masked (6 s after each gap); edge frames without physio are trimmed; interior physio gaps exclude a run.

## Independence audit (three levels, kept separate)

| Level | Unit | What it supports | What it does NOT support |
|---|---|---|---|
| Held-out run | one acquisition | Within-date stability of the prediction | Independence of runs: runs in one date share session conditions |
| Held-out acquisition day | calendar date (6 primary dates) | Stability across sessions in one animal | Between-animal generalisation |
| Held-out mouse | animal | Between-animal generalisation (needs ≥2 animals, not present here) | Nothing in the primary analysis: only one mouse is analysed |

- The criterion **Δ > 0 on at least 5 of 6 dates** is a within-animal consistency criterion. It is **not** an independent population confirmation: all dates come from one mouse, and 6 dates are not 6 animals.
- Any sentence claiming generalisation beyond sub-ALD002 is out of scope for this experiment.

## Statistical scope

- Exact two-sided sign test over 5 animals has minimum p = 0.0625: alpha 0.05 is not attainable for a between-animal claim with this design. Power 0.8 is not claimed.
- MDE: UNKNOWN. MCID: not set (no basis; not chosen after results).

## Natural language statement (write before results)

> We estimate the held-out log-loss difference, nuisance-only minus wheel-including, for whole-slice power-Doppler in the eight count-matched sub-ALD002 runs, leave-one-calendar-date-out over six dates, against a block-permutation null of wheel velocity.

## What this result does NOT mean

1. It does NOT show that fUSI decodes thoughts, intentions or any internal state.
2. It does NOT show a neural origin for the signal: body motion and locomotion-linked blood flow are not excluded.
3. It does NOT generalise beyond one mouse, and does NOT generalise to humans.
4. It does NOT establish a causal role of blood volume in locomotion.
5. The 5-of-6-dates consistency criterion is NOT an independent population confirmation.
