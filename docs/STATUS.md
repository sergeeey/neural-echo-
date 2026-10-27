# STATUS

Last meaningful update: 2026-10-27 (CRT v2 validation gate: REVISE, negative result recorded, provenance and alternatives assessed; local commits only; not pushed)

This file is the cross-session source of truth. Update it in the same commit as any change that alters project state (see AGENTS.md § Session start and state updates). Commit identifiers are read from `git log`, not recorded here.

## Current phase

- Phase 0 (repository foundation): **complete**. Gates green locally, on a fresh clone, and on GitHub CI at the last pushed head.
- Phase 1 (scientific knowledge foundation): **in progress**. First dataset (Landemard fUSI, CC BY-NC 4.0) audited for one mouse. Scientific question narrowed to predictive association only.

## Repository state

- Branch `phase0/foundation`. Origin has the state up to `8caa73c`. Later local commits are not pushed.
- No merge, no push, no paid action since the owner's last instruction.

## Data (verified, sub-ALD002 only)

- Archive `data/raw/landemard2026/sub-ALD002.zip` (git-ignored); MD5 matches figshare; SHA-256 in the manifests.
- 17 fUS runs over 9 dates. VolumeTiming: 8 runs have one extra onset (mechanism not established, excluded from primary). Frame period 0.30013 s, not 0.3 s.
- Whisking is documented as estimated from motion SVD **and wheel velocity**; excluded from the wheel-free set.
- No motion-independent reference. Angiography is static. Compact `.npz` files are the authors' analyses; not used as inputs.

## Scientific status (what is and is not established)

- **Predictive association (statement 1):** HYPOTHESIS, EXPLORATORY. Not tested on the real signal yet; the protocol is BLOCKED.
- **Temporal specificity (statement 2):** NOT TESTABLE with this design. Delayed (6 s) and advanced (2.1 s) synthetic effects are detected at 65% and 80%.
- **Wheel-specific contribution (statement 3):** NOT TESTABLE with this design. A hidden arousal correlated with the wheel is detected at 93% (synthetic).
- **Mechanism (statement 4):** NOT TESTABLE.
- Negative result recorded: `null_results/20261026-ne-exp-001-temporal-wheel-specificity.md`.
- Meta-level pearl: `pearl_registry/NE-PEARL-001.md` (verified prior art: Shmueli 2010, DOI 10.1214/10-sts330).

## Active experiments

- `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`: **PLANNED**, not frozen, not run on the real signal. Classified EXPLORATORY. Preliminary synthetic controls recorded in `synthetic_controls_preliminary.md` (40 replicates, Wilson intervals). Verdict BLOCKED.
- `experiments/20261027-ne-exp-002-temporal-latent-confounding`: **RUNNING**, synthetic stress test. Minimal set: no confounder 1/40, hidden arousal 39/40, measured arousal 1/40 (decision rule met: non-identifiability, not implementation). Eye-conditional null check: threshold about 21% higher than independent null; needs adequate replicates before freezing NE-EXP-001.
- CRT v2 validation gate (2026-10-27): **REVISE**. No null inflation (largest conditional v2 null rejection 3/30), but the pre-registered diagnostics fail (quarter variance ratio 2.50 against 1.5; block variance ratio about 6.3e4 against 3). The conditional surrogate does not reproduce the activity state, episodes or physiology dependence. Negative result: `null_results/20261027-ne-exp-002-crt-v2-distribution.md`. Two alternatives assessed, neither validated: two-component generator (partial) and date-level prediction comparison (miscalibrated at 20 replicates). Provenance: `experiments/20261027-ne-exp-002-temporal-latent-confounding/crt_run_provenance.md`. A supplementary v1 run at 100 replicates completed (6 of 6 scenarios; `crt_pilot_v1_full100.json`, summary in `crt_v1_full100_summary.md`). Its loaded code is the pre-edge working tree, not exactly commit 04267d6. It does not change the verdict.

## Blockers

1. Owner decision: restrict NE-EXP-001 to predictive association only (recommended by the current evidence), or change the question.
2. Owner decision on compute for calibration precision (500+ replicates, 1000 permutations). Profiled: about 150 ms per permutation; caching the nuisance lags and Gram blocks can reduce this. No large run without approval.
3. Owner question: the mission (§15) names NE-EXP-002 the Reflexio synthetic fusion test; the 2026-10-27 request names NE-EXP-002 the latent-confounding test. One must move to NE-EXP-003.
4. Motion-independent reference, VolumeTiming convention (official fUSI-BIDS text unverified), physio clock alignment, MCID, manifest commit and seeds: open.

## Next 3 actions

1. Owner decision: whether to pre-register a new surrogate contract version for the wheel (activity-state preserving, pre-registered before any run) or to restrict the question to predictive association only. No CRT v2 criterion changes.
2. Establish the origin of the exact wheel zeros: encoder resolution and velocity derivation from the vendor or the dataset authors (currently UNKNOWN). Do not infer physiology from them.
3. Obtain an independent review of the negative result and the alternatives before any freeze of NE-EXP-001 or any real-signal use.
