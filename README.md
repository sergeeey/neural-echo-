# Neural Echo

**Status: FOUNDATION / NO SCIENTIFIC RESULTS YET**

Neural Echo is an experimental research project on a narrow question:

> What information about internal human states is recoverable from measurable neural signals, and how can we distinguish signal-supported reconstruction from information introduced by a model prior?

## Non-claims

- This project does not read thoughts. Classification, decoding, reconstruction and correlation are not "thought reading".
- No decoding result exists yet. No model has been trained. No dataset has been adopted.
- No literature has been verified or reproduced in this repository yet.
- No experiments on humans are part of this repository unless separately reviewed and authorized.

## Scientific positioning

The project is organized as falsification-first research. Every experiment states its estimand, claim, controls and falsification criterion before results are seen. Negative results are kept and searchable. See `docs/PROJECT.md`, `docs/QUESTION_ZERO.md` and `docs/RESEARCH_METHOD.md`.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Operating manual for coding agents (vendor-neutral). `CLAUDE.md` imports it. |
| `docs/STATUS.md` | Current state. Read first. |
| `docs/PROJECT.md`, `docs/QUESTION_ZERO.md`, `docs/RESEARCH_METHOD.md`, `docs/DATA_POLICY.md`, `docs/GLOSSARY.md` | Canonical scientific context. |
| `docs/adr/` | Architecture decision records. |
| `ROADMAP.md` | Phases, not dates. |
| `experiments/` | Experiment templates and (later) experiments. |
| `null_results/`, `pearl_registry/` | Negative results and unexpected observations. |
| `literature/` | Source schema. Empty until verified entries exist. |
| `data/` | Data policy and ignored local data directories. No data is committed. |
| `src/neural_echo/` | Python package. |
| `scripts/` | `verify_repo.py`, `validate_experiment.py`. |

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 (pinned in `.python-version`).

```bash
uv sync --locked --dev
uv run python scripts/verify_repo.py
```

## Reproducibility philosophy

A result counts only if a fresh clone, one documented command set, and the committed lockfile reproduce it. Notebooks do not hold the only implementation of a result. Dataset identity is recorded by source, licence, retrieval date and checksum.
