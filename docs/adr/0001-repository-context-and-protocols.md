# ADR 0001 — Repository context, agent portability, frozen protocols and negative results

Status: accepted (2026-10-26)

## Context

The project will be worked on across sessions, tools (Claude Code, Codex, others) and machines. Chat history is not durable. Multiple memory files drift and contradict each other. Scientific work is vulnerable to post-hoc changes of hypotheses, metrics, and splits.

## Decision

1. **One canonical repository-level context.** State lives in `docs/STATUS.md` and the `docs/` set. No tool-specific memory is a source of truth.
2. **`AGENTS.md` is the vendor-neutral operating manual.** It holds durable rules only.
3. **`CLAUDE.md` is minimal** and imports `AGENTS.md` (`@AGENTS.md`). It adds only Claude-specific lines.
4. **Experiments use frozen protocols.** A protocol is committed and marked `FROZEN` before the run; changes require a dated amendment.
5. **Negative results are preserved** in `null_results/INDEX.md` and are never deleted to improve the record.

## Consequences

- Agents must read `docs/STATUS.md` before acting and update it after meaningful changes.
- Some overhead per experiment (template, manifest). Accepted in exchange for an audit trail.
- Tool-specific features (for example Claude memory) are optional conveniences, never required for correctness.
- Reversal: a superseding ADR, not an edit to this file.
