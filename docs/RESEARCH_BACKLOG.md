# RESEARCH BACKLOG

Ordered by scientific value per cost, as of 2026-10-27. Items marked **APPROVAL** need an explicit yes from the owner before work starts.

| # | Task | Why | Blocked by | Status |
|---|---|---|---|---|
| 1 | Owner decision on licence scope: the dataset is CC BY-NC 4.0 | Non-commercial only. The mission lists possible monetisation, which this licence excludes. | Owner | OPEN |
| 2 | Download one subject archive (sub-ALD002, 5.27 GB) | DONE 2026-10-26 under the owner's instruction. MD5 matches figshare. Stored in git-ignored `data/raw/landemard2026/`. | — | DONE |
| 3 | Inspect files of sub-ALD002: physio channels, sessions, timing, motion signal | DONE for structure: 17 runs with wheel, whisking, eye; no motion file; whisking derived from wheel velocity. No motion-independent reference found. | — | DONE (structure); reference OPEN |
| 4 | NE-EXP-001 as exploratory behaviour-to-fUS prediction audit (claim.md statement 1 only) | Current scientific question. Statements 2–4 are not testable with this design. | Owner decision on compute and on the restricted question | PLANNED, BLOCKED (see decision.md) |
| 5 | Calibration precision for NE-EXP-001 null (500+ replicates, 1000 permutations) | Current 40-replicate results have ±2.5% precision. Profiled: about 150 ms per permutation; caching can speed this up. | **APPROVAL** for compute | OPEN |
| 6 | Minimal discriminating set (no confounder / hidden / measured arousal) | Separates implementation error from non-identifiability | Run in NE-EXP-001 scripts (`run_nex001_discriminate.py`) | RUNNING or DONE: see `discriminate_results.json` |
| 7 | NE-EXP-002: temporal specificity and latent-confounding stress test (synthetic) | Tests whether the failure is identifiability (requested 2026-10-27) | Item 6 result | PLANNED (`experiments/20261027-ne-exp-002-temporal-latent-confounding`) |
| 8 | Conditional (eye-residual) block permutation as an alternative null | The independent wheel permutation destroys wheel–eye dependence (median max |ccf| in window ≈ 0.09, up to 0.25) | Implementation | OPEN |
| 9 | Verify the official fUSI-BIDS VolumeTiming convention | ConfUSIus source only; official text not checked | Network access to the official spec | OPEN |
| 10 | Read the full text of the Landemard article (PRIMARY_SOURCE_READ) | Needed before any claim from the paper | Access to the full text | OPEN |
| 11 | Literature search for fUS decoding baselines (arXiv, INSPIRE) | Needed for a baseline choice | None | OPEN |
| 12 | Decide compute: local CPU only, or a paid service | Mission §18 requires approval for paid compute | Owner | OPEN |
| 13 | **Open owner question:** the mission (§15) names NE-EXP-002 the Reflexio synthetic fusion test, and the 2026-10-27 request names NE-EXP-002 the latent-confounding stress test. Choose one; the other moves to NE-EXP-003. | Avoids two experiments with the same ID | Owner | OPEN |
| 14 | Reflexio integration contract on synthetic data only | Mission §15. No real personal memory. | Item 13 and owner confirmation | OPEN |

Constraints for every item: no human experiments, no remote changes without approval, no paid resources without approval, no claims beyond the verified data.
