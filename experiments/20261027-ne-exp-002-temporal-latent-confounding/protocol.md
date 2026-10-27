# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. Not frozen. Synthetic stress test; no real-signal analysis.

## Inputs

- Real behavioural series (wheel velocity, eye movement, pupil size) from the 8 primary development runs of NE-EXP-001 (holdout excluded by name).
- fUS signal simulated: AR(1) noise (phi = 0.96, unit variance) plus a known effect.

## Conditions

1. No confounder, no effect (implementation null).
2. Hidden arousal correlated with wheel (r = 0.5), not in the design, no direct effect.
3. Same arousal, included as a measured nuisance regressor.
4. Hidden arousal with r ∈ {0.25, 0.5} (strength sweep) — to be run after 1–3 pass.
5. Lag offset sweep of a true wheel effect: 0, +6 s, −2.1 s (timing specificity), reported descriptively.

## Procedure under test

Identical to NE-EXP-001 protocol.md: 6 s gap masking, leave-one-date-out, block-permutation null of the wheel (blocks of 400–799 frames), full rule (margin AND ≥ 5 of 6 dates).

## Null-validity check (planned)

The independent wheel permutation destroys wheel–eye dependence (median max |ccf| inside the lag window ≈ 0.09, up to 0.25 in one run). A conditional null that permutes wheel residuals given eye is planned as a comparison, to measure how much the independent null matters.

## Compute

- Per permutation ≈ 150 ms on this machine (profile: lag build 55 ms, Gram fits 96 ms, permutation 0.5 ms). Nuisance lags and Gram blocks can be cached; the wheel block alone changes per permutation. Scaling beyond the current runs needs owner approval.

## Amendments

None.
