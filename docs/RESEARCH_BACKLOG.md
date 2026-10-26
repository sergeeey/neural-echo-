# RESEARCH BACKLOG

Ordered by scientific value per cost, as of 2026-10-26. Items marked **APPROVAL** need an explicit yes from the owner before work starts.

| # | Task | Why | Blocked by | Status |
|---|---|---|---|---|
| 1 | Owner decision on licence scope: the dataset is CC BY-NC 4.0 | Non-commercial only. The mission lists possible monetisation, which this licence excludes. | Owner | OPEN |
| 2 | **APPROVAL** Download one subject archive (about 5 to 11 GB) to test NE-EXP-001 | The README lists physiology channels, but the archive contents (and whether they include labels and motion signals) are not verified. | Owner approval, disk space | OPEN |
| 3 | Inspect files of the downloaded subject: physio channels, sessions, trial structure, any motion signal | Required before any claim about label quality (mission §7.2) | Item 2 | OPEN |
| 4 | Freeze protocol NE-EXP-001 and run it | Measurement ceiling and confound audit (mission §14) | Items 2 and 3 | PLANNED (see `experiments/20261026-ne-exp-001-fusi-measurement-ceiling`) |
| 5 | Read the full text of the Landemard article (PRIMARY_SOURCE_READ) | Needed before any claim from the paper | Access to the full text | OPEN |
| 6 | Reflexio integration contract on synthetic data only (NE-EXP-002) | Mission §15. No real personal memory. | Owner confirmation of the Reflexio contract | OPEN |
| 7 | Literature search for fUS decoding baselines (arXiv, INSPIRE) | Needed for the baseline choice in NE-EXP-001 | None | OPEN |
| 8 | Decide compute: local CPU only, or a paid service | Mission §18 requires approval for paid compute | Owner | OPEN |

Constraints for every item: no human experiments, no remote changes without approval, no paid resources without approval, no claims beyond the verified data.
