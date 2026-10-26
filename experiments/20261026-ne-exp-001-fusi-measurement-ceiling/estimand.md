# Estimand

- **Population:** head-fixed awake mice in the Landemard fUSI dataset (5 subjects), sessions as listed in the subject tables. Inclusion and exclusion: to be fixed before data is read.
- **Intervention / condition contrast:** wheel-active versus wheel-rest periods, as defined by the wheel physiology channel.
- **Comparator / baseline:** a model using whisking, eye and motion-nuisance regressors only.
- **Endpoint:** log loss of predicting wheel-active versus rest from fUSI power-Doppler, held-out by session (primary). Balanced accuracy is secondary.
- **Summary measure:** difference in held-out log loss between the full model and the nuisance-only baseline, with a confidence interval.
- **Intercurrent events and handling:** sessions without wheel or whisking channels are excluded and counted, not imputed.

**Natural language statement (write before results):**
> We estimate the held-out log-loss difference between a fUSI-plus-nuisance model and a nuisance-only model for predicting wheel activity in awake head-fixed mice, using session-held-out splits.

**What this result does NOT mean:**
1. It does NOT show that fUSI decodes thoughts or intentions.
2. It does NOT generalise to humans or to other fUSI setups.
3. It does NOT show a causal role of blood volume in locomotion.
