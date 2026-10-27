# A-3 stage F: final test on unused sessions (sub-rat1703)

Spec: `docs/PROTOCOL_CYBIS_SPEED_BASELINE_2026-10-27.md`, amendment A-3 (`25ddeb6`). Runner: `scripts/run_cybis_speed_baseline_a3.py` (`af4e0a8`), run once in `final` mode. Output: `docs/results/cybis_speed_baseline_A3_final.json`.

Hyperparameters, sync lag and standardisation were chosen from the three original sessions only. The two test sessions played no part in any choice. The spec was not changed after the run.

## Result

| Session | M1 r² | M0 r² | C1 z | M1 − M0 block CI (within session) | C5 r² | C6 r² | Controls match M1 |
|---|---|---|---|---|---|---|---|
| ses-20210430 | −0.0162 | −0.0539 | 4.55 | [+0.0029, +0.0629] | −0.0550 | −0.0542 | no |
| ses-20210505 | −0.0138 | −0.0452 | 2.71 | [+0.0059, +0.0554] | −0.0456 | −0.0453 | no |

The script's verdict string is "PASS (decision rule met)". That string applies the rule as written. It is not a claim of neural predictive value, for the reasons below.

## Reviewer findings (fallback verifier `skeptic`, checked against the code and JSON)

1. **The r² denominator is the test session's own mean.** A negative M1 r² means "worse than predicting that session's own mean". That predictor cannot be deployed, so the sign of an absolute r² is not evidence of skill.
2. **The M0 deficit is exactly the training-versus-test mean offset.** For a constant predictor, r²_M0 = −Δ²/var_test. From the JSON, |Δ|/sd_test = 0.232 (ses-20210430) and 0.213 (ses-20210505), so the whole M0 deficit is the offset. Raw mean speeds were not printed in this run; this step is algebraic from the JSON, and the means remain to be read from the data (NEEDS-REAL-DATA).
3. **Per-session z-scoring removes each test session's level.** Speed is not used in it, so there is no target leakage. But the features of each test session are centred on that session, so the model cannot correct the offset either. The protocol permits this (Preprocessing item 2; Confounds).
4. **Correcting for the offset leaves an advantage of about 0.03–0.04 of variance.** Corrected M1 r² is 0.0377 (ses-20210430) and 0.0314 (ses-20210505). The M1 − M0 gap is unchanged, and it lies inside the within-session intervals above. This corrected comparator is NOT in the pre-registered rule, which compares against M0 only.
5. **The motion controls are inert, so C5 and C6 cannot rule out motion.** Both select alpha = 1e4, the grid edge, and their scores equal M0. A control that cannot separate itself from a constant cannot show that M1 is not a motion proxy. "The controls do not match M1" is therefore not evidence against the motion confound.
6. **The rule text says "all three" sessions**; stage F has two. A-3 did not amend that wording. The verdict is correct for the two sessions as run, but the wording should be corrected in a future amendment.

## What the data support

- Out-of-session prediction in absolute terms: **not supported**. r² is negative in both sessions.
- Within-session covariance after removing the offset: about 3–4% of variance in two sessions, with lower interval bounds of 0.003 and 0.006. ses-20210505 has z = 2.71, only just above 2.
- Across all five sessions of this animal, M1 beats M0 in four (stage E fold 3, ses-20210421, fails). The test sessions are later in time than the training sessions, so the offset may be drift.
- All of this is one animal. The two test sessions are independent of the tuning sessions, but not of the animal.

## What the data do NOT support

- A neural claim. The motion confound is not separated, because the controls are inert.
- A claim that the effect is specific to neural signal, or to speed decoding, rather than to slow drift or motion.
- Any inference about other animals.

## Verdict: CONDITIONAL (for the checkpoint, not for a neural claim)

The pre-registered rule is met on two unused sessions. That is the only independent test in this series. It does not yet establish a neural predictive effect, for three reasons above: the comparator does not correct for the level offset; the motion controls cannot discriminate; and the evidence is one animal.

Conditions for a further claim (each needs a new, pre-registered amendment and new sessions, not a re-run on these):
1. A mean-corrected comparator, named in advance, with its threshold.
2. A motion control that is not at the grid edge, with a grid scaled to its features.
3. At least one further animal from the same dataset, analysed with the frozen spec.

The stop rule applies: no further tuning on these sessions.
