# Estimand

- **Population:** simulated fUS signals with known truth, built on the real behavioural series of the 8 primary development runs of sub-ALD002. No real fUS values are used.
- **Quantity:** detection rate of the full rule (margin above a block-permutation null AND date consistency) as a function of (a) the presence and strength of a latent confounder, (b) its measurement status, and (c) the lag offset between the true effect and the model window.
- **Summary:** detection rate with Wilson 95% interval, per condition.
- **Interpretation rule:** detection under a latent confounder is evidence that the procedure cannot separate prediction from that confounder. It is not evidence about any real animal.

## What this does NOT mean

1. It does NOT show that any real behavioural covariate is confounded.
2. It does NOT estimate any effect size for the real signal.
3. It does NOT establish a temporal direction or a mechanism.
