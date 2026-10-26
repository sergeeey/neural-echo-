# STATUS

Last meaningful update: 2026-10-26 (data qualification; local commits only; not pushed)

This file is the cross-session source of truth. Update it in the same commit as any change that alters project state (see AGENTS.md § Session start and state updates). Commit identifiers are deliberately not recorded here: read them from `git log`.

## Current phase

Phase 0 — repository and reproducibility foundation: **complete** (gates green locally, on a fresh clone, and on GitHub CI at the last pushed head).

Phase 1 — scientific knowledge foundation: **in progress**. Mission received (`docs/MISSION.md`). First dataset (Landemard fUSI, CC BY-NC 4.0) qualified at structure level for one mouse.

## Mission and brief

- The brief is `docs/MISSION.md`. The root `ТЗ.txt` is the owner's original and is git-ignored.
- Read the mission before choosing work.

## Repository state

- Branch `phase0/foundation`. Origin has the state up to `8caa73c`. Later local commits are not pushed. Read `git log` for the exact state.
- No merge, no push, no paid action since the owner's last instruction.

## Data (verified, sub-ALD002 only)

- Archive: `data/raw/landemard2026/sub-ALD002.zip` (git-ignored). Size 5,269,296,348 bytes. MD5 matches figshare. SHA-256 recorded in the experiment manifest.
- 17 fUS runs. Each run has wheel velocity (1000 Hz), whisking and eye movement with pupil size (60.024 Hz), and a power-Doppler NIfTI.
- Wheel velocity is a rotary-encoder signal (cm/s). Whisking is documented as estimated from motion SVD **and wheel velocity**, so it is not independent of wheel.
- No motion-independent reference region is identified in the archive. This is open.
- The compact `.npz` files contain the authors' precomputed analyses (PSTHs, p-values, bouts). They are not used as raw inputs.
- Scans table gives date only (no time of day).

## Validated facts (FACT means checked against a primary or registry source)

- FACT: Landemard et al. article is registered as Nature, DOI 10.1038/s41586-026-10350-9, issued 2026-04-15, licence CC BY 4.0 (Crossref). Full text **not** read.
- FACT: The dataset (DOI 10.5522/04/31376338) is CC BY-NC 4.0 (DataCite, figshare).
- FACT: The analysis code repository has no declared licence (GitHub API).
- No scientific result is established by this repository.

## Active hypotheses

- H-001 (HYPOTHESIS, EXPLORATORY): wheel velocity carries information about fUS beyond eye and pupil in sub-ALD002. Freeze blocked. See `docs/HYPOTHESES.md`.
- H-002: NOT_TESTABLE_WITH_CURRENT_DATA.
- H-003: UNKNOWN.

## Active experiment

- `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`: **PLANNED**, not frozen, not run. Classified **EXPLORATORY**: with 5 mice the exact sign test cannot reach two-sided p below 0.0625, so alpha 0.05 is not attainable at mouse level.

## Blockers before freezing

1. Reference-region definition: a motion-independent signal. Not verified; needs an image-based mask and an owner decision.
2. Time-alignment check (wheel to fUS clock). Not verified against any event.
3. MCID: not set and not justifiable now. Owner decision if a practical threshold is required.
4. Scientific re-review of the revised protocol (not yet requested).

## Next 3 actions

1. Verify a motion-independent reference signal from the fUS image (outside-brain pixels or large vessel), without looking at the final holdout.
2. Verify wheel-to-fUS alignment with an available reference (e.g. VolumeTiming against physio start times).
3. Request scientific re-review once blockers 1 and 2 are answered or explicitly declared open.
