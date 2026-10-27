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

1. **The alpha grid is poorly scaled, so the result is weaker than a grid-edge statement suggests.** Alpha 1000 was selected in all three folds, but the inner r² for k = 10 moves only about 0.005 between alpha 1 and alpha 1000 (fold 1: −0.0903 to −0.0854). The PCs of 14336 z-scored voxels carry large variance, so every alpha in the grid is effectively unregularised. Every inner score is negative, so the selection picks the least bad option. The honest reading is: no positive out-of-session prediction was found with effectively unregularised linear fits on these PCs. The grid needs a much wider range (for example up to 1e7). Extending it is a protocol change and needs a dated amendment; it has not been made. This scaling point is INFERRED from the inner scores and has not been tested by running a wider grid.
2. **Sync is not established, and no lag estimate is given.** The descriptive check (`docs/results/cybis_speed_sync.json`) gives a best |r| of 0.06–0.13 at lags 1, 1 and −7 volumes. In session 1 the lag-6 correlation (|r| ≈ 0.10) is about as large as the best lag (0.115), so no lag is identified: these peaks are at the level expected from autocorrelated series. The DLC time zero is assumed to match the first fUS volume, and that assumption is UNKNOWN.
3. **The pipeline differs from the authors'.** This baseline uses per-session z-scored voxels, PCA, and lags of PCs. It does not use the authors' GLM-based lagged convolution, band-pass filter, white-matter regression, or voxel selection. It also defines speed independently from DLC body position, not from the authors' GLM speed regressor. Because of these differences, **this is a test of this simple baseline, not of the published claim.** It does not refute the paper.
4. **Motion confound not addressed.** Body motion produces Doppler artefact. A positive result would have needed the C5 control to separate it. The result is negative, so this confound did not need to be resolved here.
5. **One animal.** All three sessions are from sub-rat1703. No between-animal inference is made.

## Independent review (fallback verifier)

The reviewer agent was closed by its iteration cap (four non-LGTM verdicts; see the gate message). The documented fallback (`doubt-driven-development.md`, Independent Review Fallback Policy) was used: the `skeptic` agent, with fresh context. Its findings, checked against the files:

- **Train/test separation: passes.** PCA, ridge centring, the mean predictor and the inner selection use training sessions only. Per-session z-scoring uses the held-out session's own statistics on features only. The protocol allows this.
- **Lag alignment: passes by trace** (feature row i is time i+5; `y[LAGS:]` matches). A unit test with a synthetic `arange` input is still to be added.
- **Metrics and nulls: pass.** r², the circular-block bootstrap and the shift range are correct.
- **Recomputed numbers match the JSON.** The z values and M1 − M0 values match the stored outputs to rounding.
- **Deviation C4:** the protocol says "training data only" for the sync check; the script ran on all three sessions. It is descriptive and nothing is fitted on it. Recorded here, not fixed.
- **Deviation C5:** the baseline script uses the raw mean over voxels as the global signal, while the sync script uses the mean of z-scored voxels. The raw mean is scale-dependent, so C5 values (−0.03 to −0.0007) are uninformative. C5 does not affect the verdict, which already fails on conditions 1 and 2. Recorded here; a z-scored rerun is not done.
- **Speed sampling:** speed is a point sample of the differenced 50 Hz position, not averaged over each 0.6 s volume. This is a choice the protocol does not specify; it adds jitter and lowers the achievable r². Recorded as a limitation.
- **Overstatements corrected above** (grid scaling and sync lag). The review found them; they are fixed in this note.

## Replication of the authors' method: blocked

The authors' decoder (per the preprint) convolves voxels with time-reversed lagged t-statistics from their GLM. For sub-rat1703, session 20210407, the GLM derivative folder holds only the design matrix (`_dm.tsv`) and the events table (`_events.tsv`). No t-statistic maps are in the archive for this session. Whether the authors' GLM code is public is UNKNOWN (not checked), and the derivative README did not load (HTTP 504). So a closer replication cannot be built from the archive: the lag kernels are missing. This blocker is documented, not worked around.

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
