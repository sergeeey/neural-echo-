# Speed baseline, protocol amendment A-2 rerun (sub-rat1703, three sessions)

Protocol: `docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md`, amendment A-2 (committed `eed5d39`, before this run). Script: `scripts/run_cybis_speed_baseline_a2.py`. Results: `docs/results/cybis_speed_baseline_A2.json`. The first result (`docs/results/cybis_speed_baseline.json`, commit `0228f5d`) is unchanged.

## Verdict: NOT SUPPORTED (decision rule fails, as before)

The rule requires M1 above M0 in every held-out session, and C1 z above 2 in every session. It fails: M1 is above M0 in two of three folds, and C1 z is above 2 in one fold only.

## Results

| Held-out session | Sync lag (train) | Selected (alpha, k) | M1 r² | M0 r² | C1 z | M1 − M0 within-session block CI | C5 (z global) r² | C6 (motion proxy) r² |
|---|---|---|---|---|---|---|---|---|
| ses-20210407 | 0 | (1e4, 20) | 0.0168 | −0.0064 | 2.48 | [−0.0015, +0.0479] | −0.0061 | −0.0064 |
| ses-20210412 | +1 | (1e7, 50) | 0.0040 | −0.0037 | 1.87 | [−0.0003, +0.0143] | −0.0037 | −0.0037 |
| ses-20210421 | +1 | (1e5, 20) | −0.0313 | −0.0005 | 0.58 | [−0.0906, +0.0063] | −0.0007 | −0.0059 |

Compared with the first run (`0228f5d`): fold 1 rose from 0.012 to 0.017; fold 2 from 0.001 to 0.004; fold 3 from −0.037 to −0.031. The changes are small.

## What the widened grid shows

- The selected M1 alpha is at the new top of the grid (1e7) in fold 2; folds 1 and 3 select 1e4 and 1e5. The C6 control selects 1e7 in folds 1 and 2. So the grid edge recurs at the higher value. A wider grid would only move the edge again.
- At strong shrinkage the ridge prediction approaches the training mean. The selected M1 models are therefore close to the mean predictor. This is the reading to keep: the features carry little out-of-session linear signal that the ridge can use at any tested regularisation.
- The motion-proxy control C6 has r² ≈ 0 in every fold. A frame-to-frame change magnitude of the global signal does not predict speed out of session. This is a weak control, not evidence that motion is absent.
- The sync lags chosen from training data are 0, +1 and +1 volumes (0 to 0.6 s). These are small and consistent between folds, but the correlations behind them were small (see the first run). Sync is better constrained but not confirmed.

## Review findings (fallback verifier, `skeptic`, 2026-10-27)

The reviewer agent is closed by its iteration cap; `skeptic` was used as the documented fallback. Findings, checked against the files:

1. **Leakage: passes.** Lag and alpha selection use training sessions only; inner folds re-choose the lag. Per-session z-scoring uses the held-out session's own statistics; the protocol declares this. Limit: with three sessions each inner fold trains on one session, so selection uses less data than the final fit.
2. **Design limit (new, important): the sync search range is too narrow.** The protocol expects a haemodynamic lag of 0 to 3 s (0 to 5 volumes), but A-2 searched only −3 to +3 volumes (±1.8 s). The lags chosen (0, +1, +1) may be an artefact of that range. A-2 therefore cannot rule out the expected lag, and "no signal" is not established under the expected haemodynamic delay. Testing it needs a new amendment with a wider range, declared before the run.
3. **Decision rule: applied as written.** NOT SUPPORTED. No fold's M1 − M0 interval excludes zero.
4. **Numbers: match the JSON.** The write-up table equals `docs/results/cybis_speed_baseline_A2.json`.
5. **Controls C5 and C6 collapse to the mean predictor.** The alpha grid (1e0 to 1e7) was sized for PCs. The C6 features (a frame-to-frame change of the global mean) have small variance, so any alpha at or above 1e2 zeroes them. C6 and C5 therefore equal M0 in several folds. The motion control is uninformative as specified, and this write-up previously described it as if it were a valid null.
6. **"Features carry little signal at any regularisation" is not supported.** The A-2 JSON does not log the inner grid, the shrinkage factors or the sync curves, so this cannot be checked. Alpha is not comparable across scales.
7. **Undocumented deviations.** The C5 definition change, the new seed and the C6 alpha procedure were recorded only in the script, not in the amendment. They are now recorded in the protocol (below).
8. **Sync curves not logged.** The claim that the lags are "small and consistent" is not supported, because the folds are not independent and the curves are not in the output.

What the data do support: under the A-2 procedure, with a ±3-volume sync search and this causal feature window, out-of-session r² is at most about 0.02 across the three sessions. It is not evidence of absence.

## What this does and does not establish

- Establishes: under the A-2 rule the status is NOT SUPPORTED. That is a status under a pre-registered rule, not evidence that the baseline does not predict speed. The review above shows the sync search and the motion control cannot settle that question.
- Does not establish: that the authors' published effect is absent. The authors' pipeline (GLM lag kernels, filtering, voxel selection) is not reproduced; closer replication remains blocked.
- Does not establish: that motion is or is not the source of any signal. C6 is a crude proxy.
- The rule is applied as written; no criterion was changed after seeing these results.

## Next

1. Independent review of this rerun (the reviewer agent is still closed by its cap; the `skeptic` fallback is used and named in the commit).
2. The author queries remain drafts, not sent (`docs/AUTHOR_QUERIES_DRAFTS_NOT_SENT.md`). Sending needs owner approval, per recipient.
