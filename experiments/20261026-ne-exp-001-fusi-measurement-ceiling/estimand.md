# Estimand

- **Population:** head-fixed awake mice in the Landemard fUSI dataset (5 subjects), sessions as listed in the subject tables. Inclusion and exclusion: to be fixed before data is read.
- **Intervention / condition contrast:** wheel-active versus wheel-rest periods. BLOCKING, OPEN: the binary label needs a threshold on the wheel signal and a minimum bout length. Neither is set; both must be fixed from the wheel distribution in the data and written into protocol.md before freezing.
- **Comparator / baseline:** a model using whisking and eye regressors only, plus a motion regressor if the files contain one. The full model contains the same regressors plus the fUSI features.
- **Endpoint:** log loss of predicting wheel-active versus rest from fUSI power-Doppler, held-out by session (primary). Balanced accuracy is secondary.
- **Summary measure (sign fixed):** nuisance-only log loss minus full-model log loss, on held-out data. Positive means the fUSI model predicts better. Pooled over sessions, with the interval resampled by mouse (5 units), not by session, because sessions are nested in mice.
- **Intercurrent events and handling:** sessions without wheel or whisking channels are excluded and counted, not imputed.

**Natural language statement (write before results):**
> We estimate the held-out log-loss difference between a fUSI-plus-nuisance model and a nuisance-only model for predicting wheel activity in awake head-fixed mice, using session-held-out splits.

**What this result does NOT mean:**
1. It does NOT show that fUSI decodes thoughts or intentions.
2. It does NOT generalise to humans or to other fUSI setups.
3. It does NOT show a causal role of blood volume in locomotion.
