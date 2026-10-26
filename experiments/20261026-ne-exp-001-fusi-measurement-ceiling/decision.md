# Decision

Not yet. Status PLANNED. No evaluation of the real signal has been run. Audits used sidecars, the scans table, angiography and NIfTI headers, summary statistics, and the whole-slice signal of the 16 development runs. The holdout was not read. Synthetic controls use development-run wheel, eye and pupil series with simulated fUS and known truth.

**Classification:** EXPLORATORY. A between-animal claim cannot reach alpha 0.05 with 5 animals (exact sign-test minimum 0.0625). Power 0.8 is not claimed.

**MCID:** not set, cannot be justified now. Not to be chosen after results.

## Verdict

**BLOCKED.** The synthetic controls show that the wheel-specific claim is not identifiable with this design.

## Synthetic controls (scripts/run_nex001_controls.py, 40 replicates × 50 permutations, seed 20261026, 8 primary runs, 6 dates)

Detection is the full rule: margin above the null 95th percentile AND Δ > 0 on at least 5 of 6 dates. Margin-only rates are reported to show what the date rule adds. Monte Carlo SE is for the full-rule rate and is large (about ±0.025 to ±0.075 at 40 replicates). Full results: `controls_results.json`.

| Scenario | Truth | Full rule | Margin only | Reading |
|---|---|---|---|---|
| zero_effect | no effect | 0.025 | 0.05 | Calibrated within precision |
| ar_null_strong (φ=0.99) | no effect | 0.025 | 0.10 | Full rule holds; margin alone does not |
| eye_driven | measured eye drives signal | 0.05 | 0.10 | Nuisance adequate within precision |
| known_effect | wheel effect, R² = 0.05 | 1.00 | 1.00 | Power, optimistic: kernel matches the model's lag form |
| delayed_outside (6 s) | wheel effect delayed beyond the lag window | **0.65** | 1.00 | **Window is not a timing restriction**: the kernel tail still gives gains |
| lead_misalignment (2.1 s) | wheel advanced relative to fUS | **0.80** | 1.00 | **Direction is not identifiable**: a non-causal lead is still detected |
| hidden_confound | unmeasured arousal correlated with the wheel (r ≈ 0.5) | **0.93** | 1.00 | **Wheel gains from a confound it cannot see** |

## What the controls mean

1. The null is acceptable under the full rule at this precision (40 replicates). It is not shown to the precision a freeze requires; 500+ replicates and 1000 permutations are needed (compute not available here).
2. Timing direction is not testable with this design. Delayed and advanced effects are still detected, so the lag window and the "wheel leads" assumption cannot be verified from the data.
3. A wheel-only gain can be produced by an unmeasured arousal variable. The predictive gain therefore cannot be attributed to the wheel, let alone to neural activity.
4. The realistic failures (VolumeTiming mapping, clock shift) act on timing, which points (2) shows the design cannot resolve.

## Timing integrity (see timing_integrity.md)

- 8 of 17 runs have VolumeTiming one element longer than NIfTI volumes. Mechanism not established; excluded from the primary analysis (exclusion, not truncation).
- Actual frame period 0.30013 s, not 0.3 s; recorded onsets are used.
- Interval gaps masked (6 s after each gap, rows with masked windows removed).

## Blocking items

1. **Identifiability:** wheel-specific or timing-specific claims are not identifiable (controls 2 and 3). A freeze can only target a question this design can answer. Owner decision required: restrict the claim to "behavioural covariates predict whole-slice fUS in this animal" (no wheel-specific or timing claim), or change the question.
2. **Calibration precision:** 500+ replicates and 1000 permutations (compute decision by the owner).
3. Motion-independent reference: none verified; any neural reading is blocked.
4. Official VolumeTiming convention (fUSI-BIDS text not verified); physio clock alignment is an assumption.
5. Manifest: git commit, seeds and lock hash empty; status must stay PLANNED until a freeze commit exists.
6. MCID: owner decision if a practical threshold is wanted.

## Options if the question cannot be identified

Per the owner's instruction, if the real timestamps cannot be recovered and the wheel-specific question is not identifiable, the honest route is a dataset or task that does not depend on unproven synchronisation, or a reformulated, purely descriptive question about this animal.

## What would change our model of the problem

A gain above a calibrated null would show that behavioural covariates carry predictive information for this whole-slice signal. It would not show that the wheel is responsible (hidden-confound control), that timing is correct (direction control), or that the signal is neural.
