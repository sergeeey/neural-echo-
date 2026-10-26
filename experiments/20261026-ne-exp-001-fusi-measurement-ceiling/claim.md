# Claim

- **Claim (one sentence, falsifiable):** Held-out prediction of wheel activity from fUSI power-Doppler is better than from whisking and eye regressors alone, with a 95% session-cluster interval for the log-loss difference that excludes zero.
- **Evidence label:** HYPOTHESIS (H-001 in docs/HYPOTHESES.md).
- **Prediction if the claim is true:** the pooled held-out log-loss difference (nuisance-only minus full) is positive, with its 95% interval above zero.
- **Falsification criterion:** the pooled interval includes zero or is negative.
- **Success criterion:** as above. The margin is zero by definition; no practical-significance margin is set yet, so no effect size is claimed. Fixed before data is read.
- **Motion nuisance:** a motion regressor is included only if the data files provide one. The dataset README does not list one. Until checked, this claim uses whisking and eye only.
- **Language to avoid:** "decodes", "reads", "thought", "intention", "image".
