# HYPOTHESIS REGISTRY

Every entry is a claim to be tested, not a result. Status vocabulary: `HYPOTHESIS`, `UNKNOWN`,
`NOT_TESTABLE_WITH_CURRENT_DATA`, and later `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`,
`INVALIDATED` (only through an experiment folder with a frozen protocol).

Updated 2026-10-27. H-001 was split into four statements (experiments/.../claim.md); each keeps its own status.

| ID | Statement (falsifiable) | Status | Alternative | Artifact / confound | Next step |
|---|---|---|---|---|---|
| H-001a | Predictive association: adding wheel velocity (lags 0–6 s) to eye and pupil improves held-out prediction of whole-slice fUS in sub-ALD002, above a block-permutation null, consistent across dates. | HYPOTHESIS, EXPLORATORY. NE-EXP-001 (PLANNED, not frozen, BLOCKED) | Eye and pupil explain the signal alone. | Wheel-correlated motion; hidden arousal (synthetic: detected at 93%). | NE-EXP-001 controls and decision.md. |
| H-001b | Temporal specificity: the wheel leads the fUS signal in the assumed lag window. | NOT_TESTABLE_WITH_CURRENT_DATA. Delayed (6 s) and advanced (2.1 s) synthetic effects are detected (65%, 80%). | Any direction within the window. | VolumeTiming convention unverified; clock alignment assumed. | None with this design. Needs a verified clock and an independent timing reference. |
| H-001c | Wheel-specific contribution: the gain in H-001a is due to wheel velocity itself. | NOT_TESTABLE_WITH_CURRENT_DATA. | Unmeasured arousal correlated with the wheel. | Hidden confound: detected at 93% (synthetic). | NE-EXP-002 (latent-confounding stress test) to confirm the failure is identifiability. |
| H-001d | Neural or physiological mechanism of the fUS signal. | NOT_TESTABLE_WITH_CURRENT_DATA. | Motion, locomotion-linked blood flow, arousal. | No motion-independent reference verified. | None. Requires an independent motion or neural reference. |
| H-002 | Imagined speech or visual imagery is decodable from fUSI in this dataset. | NOT_TESTABLE_WITH_CURRENT_DATA (not listed in the dataset README; file contents not checked) | — | — | Do not claim it without a dataset that lists such labels. |
| H-003 | Adding personal context to neural features improves prediction of an independently defined state, beyond context alone. | UNKNOWN | Context alone explains the gain. | Leakage or task structure. | No data. Deferred; numbering of the Reflexio synthetic test is an open owner question (see RESEARCH_BACKLOG.md). |

Negative results recorded: `null_results/20261026-ne-exp-001-temporal-wheel-specificity.md` (design-level, NOT_SUPPORTED for H-001b and H-001c).
Meta-level pearl: `pearl_registry/NE-PEARL-001.md` (predictive success vs identifiability).

Rules:
- A hypothesis enters this table before its experiment is run.
- A status changes only with a frozen protocol and a `decision.md` in its experiment folder.
- Each row cites the experiment folder once one exists.
