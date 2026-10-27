# Pearl registry

A pearl is an unexpected observation that may deserve later investigation. **A pearl is not an established discovery.**

Each entry states:

- **Observation:**
- **Originating experiment:**
- **Alternative explanations:**
- **Status:** OPEN | INVESTIGATED_NOT_REPRODUCED | ESCALATED_TO_EXPERIMENT
- **Next falsification test:**

| ID | Date | Observation | Origin | Status |
|---|---|---|---|---|
| NE-PEARL-001 | 2026-10-27 | Predictive success does not identify the mechanism (wheel-specific, temporal, hidden confound) | NE-EXP-001 synthetic controls | OPEN ([file](NE-PEARL-001.md)) |
| NE-PEARL-002 | 2026-10-27 | Wheel recording is zero-inflated (exact zeros in 75-91% of frames); a Gaussian residual permutation cannot reproduce activity state, so quarter standardisation fails. Origin of zeros UNKNOWN. Prediction: if zeros are encoder quantisation, non-zero amplitudes have a lower bound near one encoder tick; if physical rest, zero-run timing tracks eye and pupil state. Either check can be run on existing raw data | NE-EXP-002 CRT v2 diagnostics | OPEN (next check: vendor/dataset encoder spec, before any new surrogate contract) |
