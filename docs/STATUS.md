# STATUS

Last meaningful update: 2026-10-26

## Current phase

Phase 0 — repository and reproducibility foundation (in progress). Phase 1 has not started.

## Validated facts

- FACT: Phase 0 gates pass locally and on a fresh clone of the committed state: `uv sync --locked --dev`, Ruff lint and format, Pyright, pytest, `scripts/verify_repo.py` (exit 0). The test count is not recorded here; run `uv run pytest` for the current number.
- FACT: CI workflow exists (`.github/workflows/ci.yml`) but has NOT been observed running on GitHub.
- No scientific facts are established by this repository yet.

## Active hypotheses

None registered. Questions in `docs/QUESTION_ZERO.md` are open questions, not hypotheses. A question becomes a hypothesis only when an experiment folder states H1/H2/H0 in its `alternative_hypotheses.md`.

## Active experiment

None.

## Blockers

- No dataset selected or verified (Phase 1).
- Remote `origin` (`sergeeey/neural-echo-`) has not been pushed by this work; push requires explicit approval.

## Next 3 actions

1. Observe the CI run for the Phase 0 branch once the human approves a push.
2. Ask the human whether to push the branch.
3. After push approval and CI green, ask whether to start Phase 1 (literature and dataset audit).
