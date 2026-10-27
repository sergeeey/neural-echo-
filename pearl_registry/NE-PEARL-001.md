# NE-PEARL-001: predictive success does not identify the mechanism

- **Observation:** In the NE-EXP-001 synthetic controls, a predictive gain above a calibrated-looking null is produced equally by a wheel effect, by a delayed wheel effect, by a wheel effect advanced in time, and by an unmeasured arousal correlated with the wheel. Predictive success therefore does not discriminate among causal structures.
- **Originating experiment:** NE-EXP-001 synthetic controls (`controls_results.json`), 2026-10-27.
- **Status:** OPEN (candidate, not a discovery).
- **Scope of novelty:** not claimed. The distinction between prediction and explanation is established in the literature. Verified: Shmueli, G. (2010), "To Explain or to Predict?", *Statistical Science* 25(3), DOI 10.1214/10-sts330 (Crossref record checked 2026-10-27). The confounding and identifiability point is standard; a textbook reference was not verified and is not cited here.
- **Project-local value:** a registered reminder that behavioural-covariate prediction of fUS must not be reported as a wheel-specific or temporal result.

## Alternative explanations

1. Implementation error in the controls (ruled out in part: zero-effect null is near nominal, and a confound-strength sweep is planned in NE-EXP-002 to test this).
2. Shared structure of wheel and fUS through motion (not separable with current data).
3. Genuine wheel-linked haemodynamics (not separable from 2 and 4 with current data).
4. Hidden arousal (synthetic result shows it is sufficient to produce the gain).

## Falsification test

Show that a predictive gain disappears under a control that removes the hidden confound while keeping the wheel effect (requires an arousal measurement not in the archive), or that the gain depends on the true timing (requires a verified clock; see decision.md).

## Next check

When any new dataset with an independent arousal measure and a verified clock is adopted, or at the next revision of NE-EXP-001.
