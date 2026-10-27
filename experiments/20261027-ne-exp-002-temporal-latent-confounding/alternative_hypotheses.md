# Alternative hypotheses

| ID | Hypothesis | Prediction | Refuting prediction |
|---|---|---|---|
| H1 | The procedure is correctly implemented and fails only because of non-identifiability | No-confounder null is nominal; measured confounder restores null; hidden confounder is detected | Measured confounder does not restore null |
| H2 | Implementation error inflates detections in all conditions | Null is inflated even without confounder | No-confounder null is nominal |
| H0 | Sampling noise only | Detection rates are compatible with nominal null in all conditions | Hidden confounder is detected above the nominal null |

**Discriminating test:** the three-condition set in `scripts/run_nex001_discriminate.py` (no confounder; hidden confounder; measured confounder).
