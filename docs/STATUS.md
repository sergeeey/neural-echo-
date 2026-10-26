# STATUS

Last meaningful update: 2026-10-26 (mission received; first experiment drafted; not pushed)

This file is the cross-session source of truth. Update it in the same commit as any change that alters project state (see AGENTS.md § Session start and state updates). Commit identifiers are deliberately not recorded here: read them from `git log`.

## Current phase

Phase 0 — repository and reproducibility foundation: **complete** (gates green locally, on a fresh clone, and on GitHub CI at the last pushed head).

Phase 1 — scientific knowledge foundation: **started, limited**. Mission and brief received (`docs/MISSION.md`). First dataset candidate checked by metadata only. Full text and data not yet examined.

## Mission and brief

- The brief is `docs/MISSION.md` (identical copy of the root `ТЗ.txt`, which remains untracked on purpose; `docs/MISSION.md` is the tracked reference).
- The mission defines 9 research tracks (A–I), 10 research questions (Q0.1–Q0.10), and the autonomy limits in its §18. Read it before choosing work.

## Repository state

- Branch `phase0/foundation`, pushed to `origin` before this session's work. Changes made in this session are **not pushed**.
- `origin` has no other branches; `main` does not exist yet.
- CI on GitHub: last observed run for the pushed head was successful (observed in an earlier session; re-check with `gh run list` before relying on it).

## Validated facts (FACT means checked against a primary or registry source)

- FACT: Landemard et al. article is registered as Nature, DOI 10.1038/s41586-026-10350-9, issued 2026-04-15, licence CC BY 4.0 (Crossref). Full text **not** read.
- FACT: The dataset (DOI 10.5522/04/31376338, UCL RDR) is licensed **CC BY-NC 4.0**, has 37 files, about 41.34 GB, 5 mice, BIDS format (DataCite, figshare API, README read).
- FACT: The dataset README (read) describes awake head-fixed mice, BIDS format, and physiology channels "when available" (whisking, eye, wheel). It does not list speech, imagery or stimulus-category labels, and does not list a motion signal.
- NOT VERIFIED: whether the archives contain labels, a motion signal, or the physio files described. Needs the download (blocker 2).
- FACT: The analysis code repository has **no declared licence** (GitHub API).
- No scientific result is established by this repository.

## Active hypotheses

- H-001 (HYPOTHESIS): fUSI signal carries wheel-activity information beyond whisking, eye and motion regressors. See `docs/HYPOTHESES.md`.
- H-002: NOT_TESTABLE_WITH_CURRENT_DATA (not listed in the dataset README; file contents not checked).
- H-003: UNKNOWN (no data).

## Active experiment

- `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`: **PLANNED**, not frozen, not run. Independent scientific review (local commit 9398036): **BLOCKED**. Open freeze blockers, all still unresolved after the local fixes: (1) wheel-active threshold and minimum bout length, needs the data; (2) lag windows, needs the data; (3) model class; (4) MCID, owner decision; (5) baseline value for MDE, needs the data; (6) reference-region definition, needs the data. Fixed locally: mouse-level resampling, sign convention, paired design, motion-independent and session-mismatched controls, detectability line.

## Blockers (need the owner)

1. **Licence scope.** The dataset is non-commercial only. The mission lists possible monetisation. Decide whether this research stays non-commercial.
2. **Approval to download** one subject archive (about 5 to 11 GB) to test NE-EXP-001. The archives may hold the physio channels; this is not verified.
3. **Compute.** Local CPU only, or a paid service (paid compute needs approval per mission §18).
4. **Scientific reviewer.** A named human reviewer for any claim leaving the repository.
5. **Full text access** for the Landemard article (needed before any claim from it).
6. **Tooling limit.** The Firecrawl account is out of credits, so web scraping falls back to curl. Restore credits if page-level extraction is needed.

## Next 3 actions

1. Get owner answers to blockers 1 and 2. Without them, NE-EXP-001 stays at the protocol-draft stage.
2. Literature search for fUS decoding baselines (arXiv, INSPIRE), recorded in `literature/sources.yaml` with honest verification status.
3. Once data is approved and downloaded: record checksums, inspect labels, then review and freeze the protocol before any run.
