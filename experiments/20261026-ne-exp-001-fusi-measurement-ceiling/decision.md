# Decision

Not yet. Status PLANNED. No evaluation has been run. The structure audit read only file headers, sidecars and summary statistics of the physio channels; no fUS result has been looked at.

- **Outcome:** none
- **Classification:** EXPLORATORY. Reason: with 5 mice, the exact sign test cannot reach two-sided p below 0.0625, so no statistically independent validation at alpha 0.05 is achievable. Power 0.8 is not calculated for this design and is not claimed.
- **MCID:** not set. It cannot be justified now: no effect-size anchor exists (the article full text has not been read), and no downstream decision threshold has been defined. It must not be chosen after the final holdout.
- **Blocking items before freezing:**
  1. Reference-region definition (a motion-independent signal). Not verified in the archive. Needs image-based mask and owner decision.
  2. Time alignment check (wheel to fUS clock). Not verified against an event.
  3. Lag basis and ridge penalty: fixed by nested CV on development runs only.
  4. Whether to use binary wheel-state at all. Currently exploratory.
- **Non-blocking:** sensitivity to whisking; other mice (replication).
- **Scientific review verdict:** pending re-review after these changes.
- **What would change our model of the problem?** A gain that survives the reference-region control would make wheel-linked fUS signal a candidate for locomotion-linked measurement. A gain that disappears under the reference control would show the signal is motion, which narrows Track B.
