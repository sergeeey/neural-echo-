# HYPOTHESIS REGISTRY

Every entry is a claim to be tested, not a result. Status vocabulary: `HYPOTHESIS`, `UNKNOWN`,
`NOT_TESTABLE_WITH_CURRENT_DATA`, and later `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`,
`INVALIDATED` (only through an experiment folder with a frozen protocol).

| ID | Claim (falsifiable) | Status | H2 (alternative) | H0 (artifact) | Next step |
|---|---|---|---|---|---|
| H-001 | In sub-ALD002 of the Landemard fUSI deposit, whole-slice power-Doppler carries information about wheel velocity beyond eye and pupil signals (whisking excluded: its definition uses wheel velocity). | HYPOTHESIS, EXPLORATORY. Experiment: `experiments/20261026-ne-exp-001-fusi-measurement-ceiling` (PLANNED, not frozen) | The signal is explained by eye and pupil alone. | Motion artefact from wheel-driven body movement. No motion-independent reference signal is verified yet. | NE-EXP-001: structure verified; freeze blocked (see decision.md). |
| H-002 | Imagined speech or visual imagery is decodable from fUSI in this dataset. | NOT_TESTABLE_WITH_CURRENT_DATA (not listed in the dataset README; file contents not checked) | — | — | Do not claim it without a dataset that lists such labels. |
| H-003 | Adding personal context to neural features improves prediction of an independently defined state, beyond context alone. | UNKNOWN | Context alone explains the gain. | The gain comes from leakage or task structure. | No data yet. Synthetic test first (NE-EXP-002, Phase 4). |

Rules:
- A hypothesis enters this table before its experiment is run.
- A status changes only with a frozen protocol and a `decision.md` in its experiment folder.
- Each row cites the experiment folder once one exists.
