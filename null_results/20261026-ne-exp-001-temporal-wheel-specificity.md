# Null result: temporal direction and wheel-specific mechanism are not identifiable with the NE-EXP-001 design

- **Experiment:** NE-EXP-001 (`experiments/20261026-ne-exp-001-fusi-measurement-ceiling`)
- **Date:** 2026-10-27
- **Verdict:** NOT_SUPPORTED for the wheel-specific and temporal-direction claims. Design-level null: the design cannot discriminate the competing explanations.
- **Evidence type:** synthetic controls with known truth (`controls_results.json`, `synthetic_controls_preliminary.md`). No result on the real signal is used.
- **Code version:** commit 3e751fe. Seed 20261026. 40 replicates × 50 permutations. Status EXPLORATORY.

## What was tested

Whether a predictive gain of wheel velocity over eye and pupil in whole-slice fUS (sub-ALD002, 8 primary runs, 6 dates) can be attributed to (a) wheel-specific contribution, or (b) a temporal direction in which the wheel leads the signal.

## Result (full rule, Wilson 95% in brackets)

| Scenario | Rate |
|---|---|
| Wheel effect delayed 6 s (beyond lag window) | 0.65 [0.50, 0.78] |
| Wheel effect advanced 2.1 s | 0.80 [0.65, 0.90] |
| Unmeasured arousal correlated with wheel, no wheel effect | see `synthetic_controls_preliminary.md` (0.93 point estimate, interval in that file) |

Null scenarios: zero effect 0.025, strong autocorrelation 0.025, eye-driven 0.05 (intervals in the preliminary file).

## What this kills

- The claim that the predictive gain identifies a wheel-specific contribution, under this design.
- The claim that the lag structure (wheel leads fUS, lags 0 to 6 s) is verified by the data.

## What this does NOT kill

- The predictive association of behavioural covariates with the whole-slice fUS signal in this animal. The design still detects it (known-effect scenario and the real-data margin, untested on real signal until the protocol is frozen).
- Any other mechanism in which the wheel contributes.

## Why the design cannot separate them

A latent variable correlated with the wheel (hidden arousal) produces the same predictive gain as a wheel effect. A wheel effect delayed beyond the window and a wheel effect advanced by 2 s are both detected. Prediction success is therefore compatible with several causal structures that the observational design does not distinguish. This is an identifiability limit, not a sampling limit.

## Relaxation map (what could revive a narrower claim)

1. Interventional or independent measurement of arousal (not present in the archive).
2. An external motion or timing reference (not verified in the archive).
3. A design in which the direction of time is fixed by the experiment itself (not available in this dataset).

## Status

Recorded. Not reopened unless one of the relaxation conditions is met by new data.
