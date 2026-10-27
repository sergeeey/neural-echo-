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

- `experiments/20261027-ne-exp-004-wheel-added-information-contract`: **PLANNED**, not frozen, no result. Separates predictive value (Layer 1, estimable with caveats), conditional independence (Layer 2, NOT established) and causal interpretation (Layer 3, NOT estimable). Compares candidate A (two-component conditional generator) and candidate B (out-of-sample fixed-model comparison). Both **BLOCKED** for inference: A because its surrogates have not passed the structure criteria on the development runs, B because its decision rule is uncalibrated, and its C3-B check at 60 replicates was run by the pilot (K = 1 of 60; NO GROSS INFLATION DETECTED, not calibration). C3-B outcomes are INFLATION FLAG (K ≥ 8 of 60) or NO GROSS INFLATION DETECTED, and the second is not calibration. Amendment A-1 applied before any result. Descriptive per-date Δ with a date-level CI is the simpler framing. ID chosen because NE-EXP-003 is reserved by the mission and by an open owner question. Author query drafted in `author_query_draft.md`, **NOT sent**.
- CRT v2 (NE-EXP-002) is closed as a completed negative methodological result, verdict REVISE; artifacts retained, criteria unchanged.
- NE-EXP-004 diagnostic pilot (2026-10-27, CPU 0.10 of 0.3 h, synthetic and development-wheel only): candidate A **BLOCKED** (C1 admissible on 2 of 6 held-out dates; dominant failure is episode count, plus rest-length and amplitude mismatch). Candidate B: **NO GROSS INFLATION DETECTED** (K = 1 of 60; not calibration). Negative result: `null_results/20261027-ne-exp-004-candidates-ab-pilot.md`. Scientific verdict for the independent review: A BLOCKED, B descriptive-only.
- NE-EXP-004 Phase B: frozen 2026-10-27 at `1dbf79e` with C-V2 NOT PASSED. **Amendment A-1 accepted by the owner on 2026-10-27** (primary: 8 runs over 6 dates; sensitivity without `ref04` and `ref11`, which covers 5 dates). Acceptance record in `phase_b_protocol.md`; frozen text unchanged. C-V2 remains NOT PASSED. H8 (delays vs wheel activity, wheel and stamps only, circular-shift reference): NOT DETECTED, p = 0.65, weak power; conditional on UNKNOWN clock alignment. Phase B not run.

## Blockers

1. Owner decision: restrict NE-EXP-001 to predictive association only (recommended by the current evidence), or change the question.
2. Owner decision on compute for calibration precision (500+ replicates, 1000 permutations). Profiled: about 150 ms per permutation; caching the nuisance lags and Gram blocks can reduce this. No large run without approval.
3. Owner question: the mission (§15) names NE-EXP-002 the Reflexio synthetic fusion test; the 2026-10-27 request names NE-EXP-002 the latent-confounding test. One must move to NE-EXP-003.
4. Motion-independent reference, VolumeTiming convention (official fUSI-BIDS text unverified), physio clock alignment, MCID, manifest commit and seeds: open.

## Next 3 actions

1. Owner decision on proposed amendment A-1 (revised) to `phase_b_protocol.md`: it withdraws the lattice exclusion and recommends the six-date primary set with a pre-specified sensitivity analysis. Independent review verdict: READY (a verdict on reasoning and wording, not acceptance; recorded in `timing_evidence_ledger.md` §6a). The owner must still record acceptance as a dated entry. No real-signal run is authorised.
2. Owner decision: send the timing query to the UCL repository contact (`author_query_draft_timing.md`, NOT sent; confirm the address on the live record first).
3. Timing evidence (`timing_evidence_ledger.md`, `timing_stalls.json`): onset intervals sit on an exact 0.300 s tick with one-sided delays (12–20 per run of 0.35–0.45 s; summed delay 1.0–1.7 s per run, equal to the endpoint excess). The frozen C-V2 period test is not a test of a true period. Whether the stamps are acquisition times, the VolumeTiming convention, the physio–fUS clock offset and the encoder derivation remain UNKNOWN.
2. Owner decision: whether to send the technical query on the wheel encoder to the dataset authors (`author_query_draft.md`, NOT sent; recipient to be verified from the dataset record). The origin of the exact zeros stays UNKNOWN until an answer or a specification is available.
3. Independent review of NE-EXP-004 (protocol, controls, method comparison) before any freeze. Resolve the NE-EXP-002 vs NE-EXP-003 numbering (`docs/RESEARCH_BACKLOG.md` item 13).
