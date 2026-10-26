# Claim

- **Claim (one sentence, falsifiable):** Held-out prediction of wheel activity from fUSI power-Doppler is better than from whisking and eye regressors alone, with a 95% session-cluster interval for the log-loss difference that excludes zero.
- **Evidence label:** HYPOTHESIS (H-001 in docs/HYPOTHESES.md).
- **Prediction if the claim is true:** the pooled held-out log-loss difference (nuisance-only minus full) is positive, with its 95% interval above zero.
- **Falsification criterion:** the pooled interval includes zero or is negative.
- **Success criterion:** as above. The margin is zero by definition; no practical-significance margin is set yet, so no effect size is claimed. Fixed before data is read.
- **Motion nuisance:** a motion regressor is included only if the data files provide one. The dataset README does not list one. Until checked, this claim uses whisking and eye only.
- **Scope limit (from review):** a positive result supports the claim only together with the motion-independent reference-region control in controls.md. Without it, a gain may be a motion artefact, and the result is reported as "predicts wheel activity beyond whisking and eye; motion not excluded", not as a neural result.
- **Detectability line (estimand-ops rule):** n = 5 mice (independent units); baseline or sigma: UNKNOWN until data are read; alpha 0.05 two-sided; power 0.8; MDE: UNKNOWN until baseline is known; MCID: NOT SET (owner decision). A null result is reported only with its MDE, and while MCID is unset a null result is uninformative.
- **Language to avoid:** "decodes", "reads", "thought", "intention", "image".
