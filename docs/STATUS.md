# STATUS

Last meaningful update: 2026-10-26 (after push of `phase0/foundation`)

This file is the cross-session source of truth. Update it in the same commit as any change that alters project state (see AGENTS.md § Session start and state updates). Commit identifiers are deliberately not recorded here: read them from `git log`.

## Current phase

Phase 0 — repository and reproducibility foundation: **complete** (gates green locally, on a fresh clone, and on GitHub CI at the last pushed head).
Phase 1 — literature and dataset audit: **not started**; waiting for inputs listed under Blockers.

## Repository state

- Branch `phase0/foundation`, pushed to `origin` (`sergeeey/neural-echo-`). `origin` has no other branches; `main` does not exist yet.
- CI on GitHub: last observed run for the pushed head was successful, all steps including the repository verification.

## Validated facts

- FACT: `scripts/verify_repo.py` passed locally and on a fresh clone of the Phase 0 review-fix commit (exit 0). Re-run it for the current state; do not rely on this line.
- FACT: CI on GitHub passed for the last pushed head of `phase0/foundation`.
- No scientific facts are established by this repository yet.

## Active hypotheses

None registered. Questions in `docs/QUESTION_ZERO.md` are open questions, not hypotheses. A question becomes a hypothesis only when an experiment folder states H1/H2/H0 in its `alternative_hypotheses.md`.

## Active experiment

None.

## Blockers (inputs needed from the human before Phase 1)

1. Technical brief: research goal, main question, success and failure criteria, out-of-scope list.
2. Dataset decision: which dataset, who is responsible for its licence and access, and whether it contains identifiable human data (if so, see `docs/DATA_POLICY.md`).
3. Compute decision: where experiments run and the budget.
4. Named human for scientific review of any claim that leaves the repository.

## Next 3 actions

1. Wait for the technical brief (blocker 1). Do not start literature or dataset work without it.
2. Record the brief in `docs/PROJECT.md` and the chosen dataset in `literature/sources.yaml` only after metadata is checked against a primary source.
3. Ask the human whether to merge `phase0/foundation` into `main` (open a PR if they want review).
