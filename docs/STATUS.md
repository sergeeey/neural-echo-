# STATUS

Last meaningful update: 2026-10-26 (freeze-readiness audit; local commits only; not pushed)

This file is the cross-session source of truth. Update it in the same commit as any change that alters project state (see AGENTS.md § Session start and state updates). Commit identifiers are read from `git log`, not recorded here.

## Current phase

- Phase 0 (repository foundation): **complete**. Gates green locally, on a fresh clone, and on GitHub CI at the last pushed head.
- Phase 1 (scientific knowledge foundation): **in progress**. First dataset (Landemard fUSI, CC BY-NC 4.0) audited at structure level for one mouse.

## Repository state

- Branch `phase0/foundation`. Origin has the state up to `8caa73c`. Later local commits are not pushed.
- No merge, no push, no paid action since the owner's last instruction.

## Data (verified, sub-ALD002 only)

- Archive `data/raw/landemard2026/sub-ALD002.zip` (git-ignored); MD5 matches figshare; SHA-256 in the experiment manifest.
- 17 fUS runs over 9 calendar dates; each run has wheel (1000 Hz), whisking and eye (30 or 60 Hz, per run), and a fUS NIfTI.
- Whisking is documented as estimated from motion SVD **and wheel velocity**. Excluded from the wheel-free set.
- No motion-independent reference or motion signal in the archive. Angiography is static (no time axis).
- The compact `.npz` files contain the authors' precomputed analyses; not used as inputs.

## Active experiment

- `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`: **PLANNED**, not frozen, not run. Classified **EXPLORATORY**. Verdict of the latest independent review: **BLOCKED**.
- Holdout: `ref10_run-2` (rule in protocol.md). Not read.

## Blockers

1. Motion control: no motion-independent reference verified. Owner decision needed (e.g. angiography-based mask after registration, or an externally validated reference). Without it the claim stays predictive only.
2. Official `VolumeTiming` convention (fUSI-BIDS text not verified; ConfUSIus source indicates onset). Mapping rule declared; sensitivity required.
3. Physio–fUS clock alignment: BIDS text does not define the zero of `StartTime`. Declared as assumption with shift sensitivity.
4. VolumeTiming longer than NIfTI volume count in 8 of 16 development runs. Mapping declared; alternative as sensitivity.
5. Positive control (planted wheel-coupled signal in development data) not yet run.
6. MCID: not set; cannot be justified now. Owner decision if a practical threshold is wanted.
7. Manifest: git commit, lock hash and seeds still empty; status must stay PLANNED until a freeze commit exists.

## Next 3 actions

1. Run the positive control on development data (synthetic signal injected into development runs only) to test whether the null can detect a planted effect.
2. Implement the code path for the protocol (target, lags, ridge, leave-one-date-out, block permutation) and a target-derivative test, all before any holdout access.
3. Request a fresh independent review after items 1–2; the protocol may reach READY_AS_EXPLORATORY only with items 2–4 declared as assumptions and item 5 run.
