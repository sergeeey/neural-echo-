# v1 pilot at 100 replicates (supplementary; not the pre-registered v2 gate)

Source: `crt_pilot_v1_full100.json`. Seed 20261027, 99 draws per replicate, alpha 0.05, six scenarios complete.
Code: the process loaded the pre-edge working tree on HEAD 6d430f4 at 09:11. The file's `code_version`
field reads 04267d6 because it was taken from HEAD when the run wrote its output (10:52). The loaded
code is therefore not identical to commit 04267d6. Its v1 setting is reproduced by flags only on 1 rep
(max difference 0.0 against the saved smoke file). This file has no per-replicate p values, so it
cannot be paired with the 30-rep runs; the comparison below is by aggregates only.

| Scenario | Independent k/100 (Wilson 95) | Conditional k/100 (Wilson 95) | v1 30-rep conditional k/30 |
|---|---|---|---|
| zero_effect | 4 (0.016, 0.098) | 6 (0.028, 0.125) | 2 |
| ar_null_strong | 5 (0.022, 0.112) | 5 (0.022, 0.112) | 0 |
| hidden_arousal | 100 (0.963, 1.0) | 100 (0.963, 1.0) | 30 |
| measured_arousal | 16 (0.101, 0.244) | 4 (0.016, 0.098) | 0 (independent 3) |
| lead_misalignment | 100 (0.963, 1.0) | 100 (0.963, 1.0) | 30 |
| known_added_info | 100 (0.963, 1.0) | 100 (0.963, 1.0) | 30 |

Reading (descriptive; no new criterion is applied):
- The independent comparator rejects 16% of replicates under `measured_arousal`, where the wheel carries no
  information beyond the measured nuisance. The conditional test stays at 4%. This is the pattern expected
  when the independent null ignores Z, and it is the reason the conditional null is the primary procedure.
- Null scenarios stay below 7% in the conditional arm at 100 replicates; this does not change the
  pre-registered verdict, which is decided by the diagnostics that failed.
- The 30-rep values are consistent with these rates at their precision; a paired comparison is not possible.

Verdict impact: none. The REVISE verdict rests on the pre-registered diagnostics (quarter variance ratio and
block variance ratio), which do not depend on this run.
