# RESEARCH BACKLOG

Ordered by scientific value per cost, as of 2026-10-26. Items marked **APPROVAL** need an explicit yes from the owner before work starts.

| # | Task | Why | Blocked by | Status |
|---|---|---|---|---|
| 1 | Owner decision on licence scope: the dataset is CC BY-NC 4.0 | Non-commercial only. The mission lists possible monetisation, which this licence excludes. | Owner | OPEN |
| 2 | Download one subject archive (sub-ALD002, 5.27 GB) | DONE 2026-10-26 under the owner's instruction for this step. MD5 matches figshare. Stored in git-ignored `data/raw/landemard2026/`. | — | DONE |
| 3 | Inspect files of sub-ALD002: physio channels, sessions, timing, any motion signal | DONE for structure: 17 runs with wheel, whisking, eye; no motion file; whisking derived from wheel velocity (sidecar). Reference region NOT found. | — | DONE (structure); reference region OPEN |
| 4 | Freeze protocol NE-EXP-001 and run it | Measurement ceiling and confound audit (mission §14) | Items 2 and 3 | PLANNED (see `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`) |
| 5 | Read the full text of the Landemard article (PRIMARY_SOURCE_READ) | Needed before any claim from the paper | Access to the full text | OPEN |
| 6 | Reflexio integration contract on synthetic data only (NE-EXP-002) | Mission §15. No real personal memory. | Owner confirmation of the Reflexio contract | OPEN |
| 7 | Literature search for fUS decoding baselines (arXiv, INSPIRE) | Needed for the baseline choice in NE-EXP-001 | None | OPEN |
| 8 | Decide compute: local CPU only, or a paid service | Mission §18 requires approval for paid compute | Owner | OPEN |

Constraints for every item: no human experiments, no remote changes without approval, no paid resources without approval, no claims beyond the verified data.
