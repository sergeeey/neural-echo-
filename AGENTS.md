# AGENTS.md — operating manual for coding and research agents

This file is vendor-neutral. Claude Code reads it through `CLAUDE.md`; other agents read it directly.
The repository is the project memory. Do not create parallel memory systems (`.claude/memory`, `.cursor/rules`, personal notes) as sources of truth.

## Project

Neural Echo is an experimental research project on what information about internal human states is recoverable from measurable neural signals. It is not a product and not a thought-reading system. See `docs/PROJECT.md`.

## Canonical context (read in this order in a fresh session)

1. `docs/STATUS.md` — current phase, validated facts, active experiment, next actions.
2. `docs/PROJECT.md` — scope, questions, non-goals.
3. `docs/QUESTION_ZERO.md` — foundational questions that gate experiments.
4. `docs/RESEARCH_METHOD.md` — how every experiment must be specified before results.
5. `docs/DATA_POLICY.md` — rules for human/neural data.
6. `ROADMAP.md` — phases. Current phase is in `docs/STATUS.md`.
7. `docs/adr/` — architecture decisions. Do not contradict an accepted ADR without a new ADR.

## Scientific rules (non-negotiable)

- Label every claim: `FACT` (cited or reproduced), `INFERENCE`, `HYPOTHESIS`, `UNKNOWN`. Never promote a label silently.
- Do not describe decoding, classification, or reconstruction as "thought reading".
- Do not fabricate publications, DOIs, datasets, benchmarks, metrics, or results. If unsure, write `UNKNOWN`.
- Negative results are first-class outputs. Record them in `null_results/INDEX.md`.
- Do not change a hypothesis, metric, split, or success criterion after seeing results. Changes require a new experiment or an explicit, dated amendment in the protocol.
- A reconstruction is not evidence by itself. Separate signal-supported information, model-prior information, and unresolved information.
- No experiments on humans in this repository unless separately reviewed and authorized (see `docs/DATA_POLICY.md`).

## Coding standards

- Python 3.12, `src/` layout, package `neural_echo`.
- Runtime dependencies minimal. Dev tools in the `dev` dependency group.
- Type-annotate public functions. Keep Pyright clean.
- Ruff for lint and format. Do not add lint suppressions without a reason comment.
- Notebooks may explore, but important logic lives in `src/`. Notebook output is never the source of truth.
- Minimal diffs. Do not refactor unrelated code.

## Commands

```bash
uv sync --locked --dev          # install from lockfile
uv run ruff check .             # lint
uv run ruff format --check .    # format check
uv run pyright                  # types
uv run pytest -q                # tests
uv run python scripts/verify_repo.py        # repository validator (runs the above subset + structure checks)
uv run python scripts/validate_experiment.py experiments/<id>   # structural check of one experiment
```

## Experiment workflow

1. Copy `experiments/_template/` to `experiments/<YYYYMMDD>-<slug>/`.
2. Fill `question.md`, `estimand.md`, `claim.md`, `alternative_hypotheses.md` (H1 target, H2 alternative, H0 artifact), `controls.md`.
3. Fill `protocol.md` completely, then set `status: FROZEN` in `manifest.yaml` and commit before running anything.
4. Run. Record outputs and the git commit in `manifest.yaml`.
5. Write `decision.md`, including "What would change our model of the problem?".
6. Update `null_results/INDEX.md` for non-supported outcomes and `docs/STATUS.md`.

Status vocabulary: `PLANNED`, `FROZEN`, `RUNNING`, `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, `INVALIDATED`. Never use `SUCCESS` for a confirmed hypothesis.

## Files that must be updated after meaningful work

- `docs/STATUS.md` — always, after any change that alters project state.
- `null_results/INDEX.md` — when an experiment yields a negative or inconclusive result.
- `pearl_registry/INDEX.md` — when an unexpected observation is worth later investigation (a pearl is not a finding).
- `docs/adr/` — when an architectural decision is made. Trivial choices do not need an ADR.
- `literature/sources.yaml` — only with verified metadata (see `literature/README.md`).

## Prohibited shortcuts

- Marking a paper `REPRODUCED` because its PDF was read.
- Committing raw or identifiable human data, or any file under `data/raw/`.
- Committing secrets, tokens, or credentials.
- Editing a frozen protocol without an amendment entry.
- Declaring CI green without running it or observing a passing run.
- Hiding failing tests, lint, or type errors.

## Definition of "next task"

Read `docs/STATUS.md` → "Next 3 actions". If empty or ambiguous, stop and ask the human.
