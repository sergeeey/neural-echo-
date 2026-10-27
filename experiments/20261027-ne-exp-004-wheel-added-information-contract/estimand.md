# Estimand

The contract separates three layers. Only the first is estimable with a stated procedure, and only with the caveats below.

## Layer 1 — Predictive value (estimable, scoped)

- Population: sub-ALD002 development runs (eight count-matched runs over six calendar dates; holdout excluded by name).
- Intervention: adding wheel velocity, lags 0 to 6 s (21 lags, 0.3 s frames), to the wheel-free model (eye and pupil, lags 0 to 6 s).
- Comparator: the wheel-free model fitted on the same training dates.
- Endpoint: held-out Gaussian predictive loss per frame, whole-slice fUS signal (aligned target), evaluated leave-one-calendar-date-out.
- Summary measure: pooled held-out difference Δ = L_nuisance − L_full (positive = wheel helps). Per-date Δ_d is reported alongside.
- Uncertainty: over the six dates (date-level bootstrap and exact sign counts). Not over frames, which are autocorrelated.
- MCID: not defined. This layer cannot claim a practically important effect until one is fixed before any real-signal run. Open item.

## Layer 2 — Conditional independence (NOT established)

- Target statement: wheel velocity carries no information about fUS beyond eye and pupil, i.e. Y ⊥ W | Z.
- Status: no valid conditional null is currently available. The approximate conditional block permutation (NE-EXP-002) failed its distributional diagnostics on the development wheel.
- Consequence: no p-value or "conditional" claim may be stated under this contract unless a candidate null first passes the structure criteria in `controls.md` on the development runs.

## Layer 3 — Causal interpretation (NOT estimable here)

- Any statement that the wheel causes, drives or is the mechanism of the fUS signal requires an identification argument. None is available: the hidden-arousal control (NE-EXP-002, 39/40 detections) shows that a predictive gain can arise from an unmeasured variable correlated with the wheel.
- Statement 2 (temporal specificity) and statement 4 (mechanism) remain NOT TESTABLE.

## Non-interpretations (required)

1. A positive Δ does not show that the wheel carries information not carried by eye and pupil.
2. A positive Δ does not establish direction in time or the lag window.
3. A null Δ does not show absence of wheel-related signal; the design can be insensitive (see the controls).
