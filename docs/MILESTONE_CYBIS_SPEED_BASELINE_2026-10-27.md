# Milestone result: own speed-decoding baseline on raw fUS (sub-rat1703, three sessions)

Protocol: `docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md` (committed `7893a24`, amendment A-1 before any fit). Results: `docs/results/cybis_speed_baseline.json`, `docs/results/cybis_speed_sync.json`. Scripts: `scripts/run_cybis_speed_baseline.py`, `scripts/check_cybis_speed_sync.py`.

## Verdict: NOT SUPPORTED on this subset

The protocol's decision rule requires all three of: M1 mean out-of-session r² above M0 in every held-out session; C1 z > 2 in every session; the C5 global-signal control not matching M1. The first two fail. The protocol's rule is applied as written.

## Results (leave-one-session-out, n = 1195 volumes per test session)

| Held-out session | M1 ridge r² | M0 mean r² | M1 − M0 (within-session block CI) | C1 shift z | C5 global-signal r² | Selected (alpha, k) |
|---|---|---|---|---|---|---|
| ses-20210407 | 0.0122 | −0.0064 | [−0.011, +0.046] | 2.32 | −0.0065 | (1000, 20) |
| ses-20210412 | 0.0010 | −0.0035 | [−0.037, +0.033] | 1.95 | −0.0296 | (1000, 10) |
| ses-20210421 | −0.0368 | −0.0006 | [−0.093, −0.004] | −0.33 | −0.0007 | (1000, 10) |

Reading:
- Out-of-session r² is close to zero in every fold. The best fold is 0.012.
- The within-session block intervals include zero in two folds, and are negative in the third.
- The third fold (ses-20210421) is worse than the mean predictor.

## Caveats that limit the reading

1. **Selection at the grid edge.** The pre-registered alpha grid tops out at 1000, and that value was selected in all three folds. The optimum may lie beyond it. Extending the grid is a protocol change and needs a dated amendment; it has not been made. The result therefore says "no signal at alpha ≤ 1000", not "no signal".
2. **Sync is not established.** The descriptive check (`docs/results/cybis_speed_sync.json`) gives best lags of 1, 1 and −7 volumes (0.6 s, 0.6 s, −4.2 s), with |r| only 0.06–0.13. Lag −7 lies outside the expected 0–3 s haemodynamic range. The DLC time zero is assumed to match the first fUS volume, and that assumption is not confirmed (UNKNOWN).
3. **The pipeline differs from the authors'.** This baseline uses per-session z-scored voxels, PCA, and lags of PCs. It does not use the authors' GLM-based lagged convolution, band-pass filter, white-matter regression, or voxel selection. It also defines speed independently from DLC body position, not from the authors' GLM speed regressor. Because of these differences, **this is a test of this simple baseline, not of the published claim.** It does not refute the paper.
4. **Motion confound not addressed.** Body motion produces Doppler artefact. A positive result would have needed the C5 control to separate it. The result is negative, so this confound did not need to be resolved here.
5. **One animal.** All three sessions are from sub-rat1703. No between-animal inference is made.

## Comparison with the published values (not a reproduction)

The preprint quotes intra-animal r² up to 0.6 and inter-animal up to 0.36, computed on the authors' own outputs (`data/raw/cybis_pereira_2026/decode-speed`). Those outputs reproduce the quoted maxima (see `docs/MILESTONE_CYBIS_PEREIRA_DECODE_2026-10-27.md`). This baseline's r² near zero is not comparable with those numbers, because the pipeline, split and speed definition differ. No agreement or disagreement with the published claim is claimed.

## What this milestone does not establish

- It does not establish that fUS signals predict speed in this animal, or in any animal, under the authors' pipeline.
- It does not establish a reproducible baseline in the sense of the protocol's Step 4; the alignment question is open.
- It does not change the C-V2 result (NOT PASSED).
- It is not a causal or mechanistic result.

## Next steps (not run)

1. Extend the alpha grid with a dated amendment, and re-run; the optimum may lie beyond 1000.
2. Resolve the sync question: DLC time zero against the fUS volume times, using the acquisition times in `scans.tsv` (acq_time 10:03:47 for fUS, session clock not yet aligned to the DLC file).
3. Implement the authors' lagged GLM convolution, to test whether the pipeline difference explains the gap.
4. If the gap persists, document the authors' pipeline dependency; do not claim the published result is wrong.
