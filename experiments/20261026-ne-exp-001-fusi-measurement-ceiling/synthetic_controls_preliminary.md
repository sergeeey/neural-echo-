# Synthetic controls for NE-EXP-001: PRELIMINARY (EXPLORATORY)

Status: **preliminary**. These are simulation results on development-run inputs with known truth.
They are not evidence about the real signal and are not a basis for any freeze.

## Provenance

- Code version: git commit 3e751fe (script `scripts/run_nex001_controls.py`, primitives in `src/neural_echo/exp001.py`).
- Seed: 20261026 (single `numpy.random.default_rng`, scenarios run in fixed order).
- Data: eligible development runs only (count-matched; holdout excluded by name). Primary runs: 8; dates: 6; excluded mismatched runs: 8.
- Consistency rule: >= 5 of 6 dates.
- Mean wheel–eye correlation over primary runs (zero lag): -0.0342.

## Results

Full rule = margin above the block-permutation null 95th percentile AND date consistency. Wilson 95% intervals (binomial) on the full-rule rate. Margin-only shown for comparison.

| Scenario | Role | Count | Rate | Wilson 95% | Margin-only (Wilson 95%) | Permutations |
|---|---|---|---|---|---|---|
| zero_effect | null: no effect (false positives) | 1/40 | 0.025 | [0.004, 0.129] | 0.014 to 0.165 | 50 |
| ar_null_strong | null: strong autocorrelation (false positives) | 1/40 | 0.025 | [0.004, 0.129] | 0.040 to 0.231 | 50 |
| known_effect | power: wheel effect, R² 0.05 in truth (optimistic kernel) | 40/40 | 1.000 | [0.912, 1.000] | 0.912 to 1.000 | 50 |
| delayed_outside | wheel effect delayed 6 s (timing specificity) | 26/40 | 0.650 | [0.495, 0.779] | 0.912 to 1.000 | 50 |
| lead_misalignment | wheel effect advanced 2.1 s (timing direction) | 32/40 | 0.800 | [0.652, 0.895] | 0.912 to 1.000 | 50 |
| eye_driven | null: signal driven by measured eye (nuisance adequacy) | 2/40 | 0.050 | [0.014, 0.165] | 0.040 to 0.231 | 50 |
| hidden_confound | unmeasured arousal correlated with wheel (wheel-specificity) | 37/40 | 0.925 | [0.801, 0.974] | 0.912 to 1.000 | 50 |

## Reading (what this does and does not show)

- The null rows (zero_effect, ar_null_strong, eye_driven) bound the false-positive rate of the full rule at this precision. Each Wilson interval is wide; with 40 replicates, values up to about 0.12 are compatible with the nominal 0.05. The precision is too low to certify calibration.
- The positive and stress rows show what the design detects. They do not show that the detected effect is wheel-specific, temporal, or neural: hidden_confound, delayed_outside and lead_misalignment are all detected at high rates.
- Permutations per replicate are 50, so each null threshold is itself noisy. Nominal size with 50 permutations is about 0.067 by simulation (review note), not 0.05.
- All conclusions are exploratory and carry no multiplicity correction across scenarios.
