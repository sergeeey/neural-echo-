# Decision

Not yet. Status PLANNED. No evaluation has been run. The structure audit read only sidecars, scans table, sampling rates, VolumeTiming arrays and header-level NIfTI dimensions. No fUS result has been analysed, and no holdout content has been read.

- **Outcome:** none
- **Classification:** EXPLORATORY. With 5 mice, the exact sign test cannot reach two-sided p below 0.0625, so no statistically independent validation at alpha 0.05 is achievable at mouse level. Power 0.8 is not claimed.
- **MCID:** not set. It cannot be justified now: no effect-size anchor exists (article full text not read), and no downstream decision threshold has been defined. Must not be chosen after the holdout.
- **Scientific re-review (2nd round):** BLOCKED. Items B1 to B6 are fixed in the text (per-run resampling, named holdout, session-mismatch test removed, null-based outcomes, fixed ridge alpha, leakage controls). B7 blocks any neural reading.
- **Blocking before freezing (still open):**
  1. Motion-independent reference or motion estimate: needs a decision (angiography-based estimate or validated reference). Without it the claim stays predictive only.
  2. VolumeTiming onset-or-centre convention: UNKNOWN; affects lag 0 interpretation (lag profile is descriptive).
  3. Autocorrelation length of the target: UNVERIFIED; must be measured on development runs before freezing, to confirm the 10 s buffer.
  4. MCID: owner decision, if any practical threshold is wanted. Currently not set.
- **Non-blocking:** whisking sensitivity; replication in other mice; acq-ref code meaning (UNVERIFIED).
- **What would change our model of the problem?** A gain above the block-permutation null that survives the leave-one-day-out split would show that wheel velocity carries predictive information for this signal. It would still not show it is neural, until a motion-independent reference is verified.
