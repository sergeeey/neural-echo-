# CLAUDE.md

@AGENTS.md

## Claude Code specifics

- Canonical project state is `docs/STATUS.md`, not any memory file under `.claude/`.
- Before editing protocols under `experiments/`, confirm the experiment's status in `manifest.yaml`; frozen protocols change only through a dated amendment.
- Run `uv run python scripts/verify_repo.py` before reporting work as done.
