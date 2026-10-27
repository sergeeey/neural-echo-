# Decision

Not yet. Status PLANNED. Synthetic stress test; no real-signal result is produced or used.

- **Outcome:** none yet. The minimal discriminating set (conditions 1–3) is run in NE-EXP-001 scripts; its results are recorded in `experiments/20261026-ne-exp-001-fusi-measurement-ceiling/discriminate_results.json`.
- **Decision rule (fixed before reading):** if condition 1 is nominal, condition 2 is detected, and condition 3 is nominal, the failure is non-identifiability. If condition 3 remains detected, the implementation is suspect and this experiment is INVALIDATED for the implementation.
- **What would change our model of the problem?** A measured-confounder restoration would show that the procedure responds to confounding as predicted, so the earlier wheel-specific failure is an identifiability limit of the design, not a bug.
