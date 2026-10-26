# Decision

Not yet. Status PLANNED. No evaluation of the real signal has been run. Audits read sidecars, the scans table, angiography and NIfTI headers, summary statistics, and the whole-slice signal of the 16 development runs. The holdout was not read. Synthetic controls use development-run wheel, eye and pupil series with simulated fUS.

**Classification:** EXPLORATORY. A between-animal claim cannot reach alpha 0.05 with 5 animals (exact sign-test minimum 0.0625). Power 0.8 is not claimed.

**MCID:** not set, cannot be justified now. Not to be chosen after results.

## Verdict

**BLOCKED.** Three new findings from the synthetic controls and the timing audit block freezing.

## Synthetic controls (scripts/run_nex001_controls.py, 60 replicates × 50 permutations, seed 20261026)

Eight count-matched runs, six dates, procedure as in protocol.md. Monte Carlo SE given. Results saved in `controls_results.json`.

| Scenario | Truth | Detection rate | MC SE | Reading |
|---|---|---|---|---|
| zero_effect | no effect | 0.05 | ±0.028 | Calibrated |
| ar_null_strong (φ=0.99) | no effect | **0.13** | ±0.044 | **Inflated false positives** under strong memory |
| known_effect | wheel effect, R²≈0.05 | 0.92 | ±0.036 | Power, optimistic: kernel shape matches the model's lags |
| misaligned_effect (2.1 s) | delayed effect | 0.95 | ±0.028 | **Scenario too weak**: the shifted kernel still fits inside the 0–6 s window, so no power loss is tested |
| correlated_nuisance | eye-driven signal, no wheel effect | **0.12** | ±0.041 | **Inflated false positives** when the nuisance is correlated with the predictor path |

Reading:
- The null is calibrated for the zero-effect case only.
- Under strong autocorrelation and under an eye-driven signal, the procedure gives false positives above 5%. With 60 replicates the intervals are wide (±0.04), so the excess is a warning, not a precise size. It is nonetheless above nominal in both cases and must be fixed or accepted explicitly before freezing.
- The misalignment control did not stress the temporal model. A stronger shift (beyond the lag window) is required before any claim about timing tolerance.
- Known-effect power is an upper bound: the simulated kernel shares the model's form.

## Timing integrity (see timing_integrity.md)

- 8 of 17 runs have VolumeTiming one element longer than NIfTI volumes (+1 each). Mechanism not established; those runs are excluded from the primary analysis (exclusion, not truncation).
- Actual frame period is 0.30013 s (per-run slope), not the nominal 0.3 s. A nominal grid drifts about 3.5 s over a run; the protocol uses recorded onsets.
- Interval gaps are masked (6 s after each gap); 5 runs have gaps, one of 3.9 s.
- Physio StartTime zero is undefined in the fetched BIDS text: clock alignment remains an assumption.

## Blocking items (current)

1. **Null calibration under strong autocorrelation and correlated nuisance** (controls above). Requires a revised null (e.g. longer or model-based blocks) tested on synthetic data before freezing; the revision must be declared as a change made before any holdout evaluation.
2. **Misalignment control too weak.** Redesign with a shift that moves the effect outside the 0–6 s window, to measure power loss.
3. Motion-independent reference: no verified signal; claim stays predictive.
4. Official VolumeTiming convention (fUSI-BIDS text not verified); clock alignment assumed.
5. Manifest: git commit, lock hash and seeds empty; status must stay PLANNED until a freeze commit exists.
6. MCID: owner decision if a practical threshold is wanted.

## Options if the timing cannot be verified

Per the owner's instruction: if real timestamps cannot be recovered, switch to a dataset or task that does not require unproven synchronisation. For this archive, a predictive analysis on the 8 matched runs with declared assumptions is the only remaining route, and it stays EXPLORATORY.

## What would change our model of the problem

A gain above a calibrated null, stable across dates, would suggest wheel velocity carries predictive information for this whole-slice signal, pending clock alignment and motion control. It would not show a neural origin.
