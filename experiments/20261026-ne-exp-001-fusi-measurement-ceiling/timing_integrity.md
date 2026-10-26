# Timing integrity table (sub-ALD002, 17 fUS runs)

Source of time axis: `VolumeTiming` in each run's fUS sidecar (onset of each volume, start reference per ConfUSIus source; the official fUSI-BIDS text is NOT verified). Nominal `FrameAcquisitionDuration` = 0.3 s. Volume count from the NIfTI header. Headers and sidecars only; no image values were used for this table. The holdout row is metadata only.

Measured on all runs: onset intervals have median 0.300 s, the whole-run linear slope is **0.30013 s per frame** (not 0.3), so a nominal 0.3 s grid drifts about 3.5 s over a run. No onset interval is below 0.15 s. Edge intervals (first and last) are 0.300 s in every run, so the extra onset in mismatched runs is not an edge artefact.

| run | volumes (NIfTI) | onsets (VolumeTiming) | difference | onset range (s) | median dt (s) | interval >0.45 s | status | usability for analysis |
|---|---|---|---|---|---|---|---|---|
| ref02 | 11307 | 11308 | +1 | 6.948–3400.421 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref04 | 11311 | 11311 | 0 | 6.551–3404.813 | 0.300 | 1 (3.907 s) | match; interior gap | gap masking required; flagged |
| ref06_run-1 | 11311 | 11311 | 0 | 6.859–3401.271 | 0.300 | 0 | match | usable under declared rules |
| ref06_run-2 | 11310 | 11310 | 0 | 6.594–3400.907 | 0.300 | 1 (0.452 s) | match; minor gap | usable; gap masked |
| ref08 | 11311 | 11311 | 0 | 7.268–3401.634 | 0.300 | 0 | match | usable under declared rules |
| ref10_run-1 | 11279 | 11280 | +1 | 6.397–3391.467 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref10_run-2 (holdout) | 11310 | 11310 | 0 | 6.728–3400.906 | 0.300 | 0 | match (metadata only) | holdout: not analysed |
| ref11 | 11297 | 11297 | 0 | 6.185–3398.992 | 0.300 | 7 (max 0.926 s) | match; gaps | gap masking required |
| ref12 | 11343 | 11344 | +1 | 6.859–3411.311 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref14 | 11120 | 11121 | +1 | 6.402–3343.943 | 0.300 | 1 (0.472 s) | MISMATCH; minor gap | not verified: excluded from primary |
| ref18 | 11316 | 11316 | 0 | 6.693–3402.558 | 0.300 | 0 | match | usable under declared rules |
| ref20_run-1 | 11330 | 11331 | +1 | 6.321–3407.007 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref20_run-2 | 11308 | 11308 | 0 | 6.024–3399.667 | 0.300 | 1 (0.457 s) | match; minor gap | usable; gap masked |
| ref22 | 8339 | 8339 | 0 | 0.056–2502.485 | 0.300 | 0 | match | usable; starts at 0.056 s |
| ref23 | 11284 | 11285 | +1 | 6.570–3393.274 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref24 | 11312 | 11313 | +1 | 6.517–3401.485 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |
| ref27 | 11318 | 11319 | +1 | 6.975–3403.736 | 0.300 | 0 | MISMATCH | not verified: excluded from primary |

## Summary

- 17 runs; **8 mismatches, all exactly +1** (onsets = volumes + 1). The 9 others match exactly.
- Interval gaps above 0.45 s occur in 5 runs; in 2 of these the gap is large (3.9 s, 0.93 s). Gaps do not explain the count mismatch: ref11 has seven gaps and matches exactly.

## Mechanism tests (what was checked, what it shows)

| candidate | test | result |
|---|---|---|
| Trailing extra onset (VolumeTiming longer at the end) | Last onset interval on the regular grid | Consistent with a regular extra frame, not a boundary artefact (last interval 0.300 s in all runs). Not discriminating alone |
| Leading extra onset (first onset not in data) | First interval and grid residual | First interval 0.300 s in all runs. Not discriminating alone |
| Padded or zeroed volume (volume list padded) | Count of all-zero volumes at each end | 0 zero volumes in every run |
| Cropped first or last volume (volume dropped at export) | Mean image intensity of first and last volume vs interior (z-scores) | Mismatched runs: |z| at both edges is at most 2.24 (ref24 first −2.24; ref20_run-1 last −1.75; the rest below 1.2). A matched run, ref06_run-2, has last z = −5.11, so an edge outlier does not identify the mismatch. The edge signal does not identify the dropped side |
| Start delay (onsets shifted, count changed) | Start time vs physio start | Start times differ per run (6.0–7.3 s), but a delay does not change the count; not a mechanism for +1 |
| Frame-rate change | Slope and interval | Slope 0.30013 in all runs; no run-specific rate change |
| Metadata error in the count | No independent frame count in sidecar | Not testable from this archive |

**Verdict on mechanism: NOT ESTABLISHED.** The data do not show which end carries the extra onset, nor whether the NIfTI or the VolumeTiming list is correct. No correction by truncation is applied, per the rule. The protocol therefore excludes the 8 mismatched runs from the primary analysis (exclusion, not truncation) and reports them as a sensitivity analysis under a declared mapping.

## Clock alignment with physio

Physio StartTime zero is not defined in the BIDS text fetched. Alignment is therefore an assumption with shift sensitivity (protocol.md). This table does not verify it.
