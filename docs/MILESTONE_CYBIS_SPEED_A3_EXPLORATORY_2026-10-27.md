# A-3 stage E result: EXPLORATORY (not independent)

Spec: `docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md`, amendment A-3 (commit `25ddeb6`). Runner: `scripts/run_cybis_speed_baseline_a3.py` (commit `af4e0a8`, identical code for this run). Output: `docs/results/cybis_speed_baseline_A3_exploratory.json`.

**Label: EXPLORATORY.** The three original sessions were used for both the diagnostic and its interpretation. Nothing here is independent confirmation. Stage F is the only independent test, and it has not been run.

## Run history (transparency)

The first exploratory run was interrupted after its first fold by a session break. The second run used the same committed code and the same seed (20261029) and completed. The fold-1 line of the first run is identical to the second run's fold 1. No setting was changed between the two.

## Results (leave-one-session-out, n = 1195 per fold)

| Held-out session | M1 r² | M0 r² | C1 z | M1 − M0 block CI | C5 r² | C6 r² | C5 matches M1 | C6 matches M1 |
|---|---|---|---|---|---|---|---|---|
| ses-20210407 | 0.0206 | −0.0064 | 2.50 | [0.0104, 0.0454] | −0.0061 | −0.0071 | no | no |
| ses-20210412 | 0.0141 | −0.0037 | 2.58 | [0.0093, 0.0278] | −0.0024 | −0.0036 | no | no |
| ses-20210421 | −0.0278 | −0.0005 | −0.29 | [−0.0714, −0.0028] | −0.0179 | −0.0063 | yes | yes |

Decision rule (unchanged): M1 > M0 in every fold, C1 z > 2 in every fold, and no control matching M1.

- Folds 1 and 2: M1 > M0 and z > 2. The M1 − M0 interval excludes zero in both.
- Fold 3: M1 < M0 and z < 2. Both controls match M1 in this fold (within 0.01), so in this fold M1 is no better than a control.
- Verdict: **NOT SUPPORTED** (the rule fails in fold 3 on two conditions).

## What this does and does not show

- Two of three folds show small, statistically separated out-of-session r² (0.014 to 0.021) above the mean predictor. That is a weak, non-zero effect in this subset. It is the reason stage F exists.
- It is NOT evidence of a robust effect: the effect is about 0.02 of variance, and the third fold reverses it.
- Fold 3's failure is what the controls predict if the signal is not specific. A motion-type control matching M1 means fold 3 cannot distinguish M1 from it.
- No change to the spec is made after this result. Stage F uses the spec as frozen.

## Next

Stage F: one run on ses-20210430 and ses-20210505, after both files are complete and checksummed. Hyperparameters are chosen from the three original sessions only, by the frozen A-3 procedure.
