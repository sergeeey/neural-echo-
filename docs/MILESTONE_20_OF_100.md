# Milestone 20/100: checkpoint report (2026-10-27)

Scope: the Neural Echo goal contract, stage by stage. Local commits only; nothing pushed or merged. The sealed holdout was not opened. No paid compute was used.

## Starting point

Repository at Phase 0 foundation; Landemard / ALD002 fUS record under audit; NE-EXP-002 (CRT v2) closed as REVISE; NE-EXP-004 frozen in Phase B with C-V2 NOT PASSED. The progress estimate of about 12/100 is the owner's, not verified here.

## Definition of Done: status

| Criterion | Status | Evidence |
|---|---|---|
| Consistent repository state | MET | `scripts/verify_repo.py` passes (ruff, format, pyright, 43 pytest); STATUS corrected in `7c79a4f` |
| Temporal qualification with PASS / CONDITIONAL / BLOCKED | MET for Landemard ALD002: BLOCKED. For sub-rat1703, stamps regular at 0.6006 s (session 1), not fully verified | `docs/MILESTONE_QUALIFICATION_2026-10-27.md`; `timing_evidence_ledger.md` |
| At least one scientifically justified real-neural candidate, with source and licence | MET: Cybis Pereira et al., Zenodo 15476373, CC BY 4.0 | `docs/MILESTONE_QUALIFICATION_2026-10-27.md` |
| Reproducible baseline, or strictly documented blocker | PARTIAL: own baseline run and documented (NOT SUPPORTED); closer replication of the authors' method BLOCKED (lag kernels absent from archive) | `docs/MILESTONE_CYBIS_SPEED_BASELINE_2026-10-27.md`; `null_results/20261027-speed-baseline-sub-rat1703.md` |
| Independent review | PARTIAL: baseline reviewed by `skeptic` (fallback; reviewer cap closed); earlier decode-output review had four P1 items, addressed in `b4403b1` | Milestone note, section "Independent review" |
| Tests | MET: 43 pass | `verify_repo.py` |
| Final report with GO / NO-GO | This document | Below |

## What was done

1. Repository state: STATUS corrected (0.30013 s frame period marked unconfirmed; Next-3 numbering); committed `7c79a4f`.
2. Landemard ALD002 timing: BLOCKED, because `VolumeTiming` semantics are not established from any retrieved source.
3. Alternative datasets: ConfUSIus listing reviewed; Cybis Pereira 2026 found with CC BY 4.0 (Zenodo primary source).
4. Authors' outputs for speed decoding: 104 files fetched with SHA-256 manifest. Their test r² reproduces the quoted intra-animal maximum (0.602 vs 0.6); inter-animal 0.354 vs 0.36 (not exact). Duplicated inter dummy rows excluded. Commit `b4403b1`.
5. Own baseline on raw fUS (three sessions of sub-rat1703): protocol committed before fitting (`7893a24`) with amendment A-1 (the "mask-brain" file is the authors' decoder weights and was excluded). Result: NOT SUPPORTED. Out-of-session r² 0.012, 0.001, −0.037. Commit `0228f5d`.
6. Sync check (protocol C4): no identifiable lag (best |r| 0.06–0.13, lags 1, 1, −7 volumes); sync is not established.
7. Independent review of the baseline: `skeptic` fallback. Found two overstatements in the milestone note (grid scaling; sync lag), corrected. Found deviations C4 and C5, recorded.
8. Negative result recorded in `null_results/` and its index.

## What is established (VERIFIED)

- The licence, source and checksums for the Cybis Pereira decoding outputs and the three fUS sessions.
- The authors' decoder test outputs reproduce their quoted intra-animal maximum (r² 0.602 against 0.6).
- Our own simple linear baseline does not predict running speed out of session on sub-rat1703 under the pre-registered rule (NOT SUPPORTED).

## What is not established

- Whether fUS predicts running speed under the authors' pipeline on the raw data: the closer replication is blocked (see below).
- Synchronisation between DLC motion and fUS volumes: UNKNOWN.
- Whether the signal is haemodynamic or motion artefact: not separated.
- Inter-animal prediction: the inter-animal outputs cover three animals and reproduce 0.354 against a quoted 0.36, which is not exact.
- The published (Cell Reports) version: not accessible (HTTP 403).
- Any causal or mechanistic claim: none made.

## Blockers

1. **Closer replication of the authors' method is blocked.** The authors convolve voxels with time-reversed lagged t-statistics from their GLM. For sub-rat1703 session 20210407, the archive holds only the GLM design matrix and events table; no t-statistic maps are present. Whether the authors' GLM code is public is UNKNOWN.
2. **Landemard ALD002 timing is BLOCKED.** `VolumeTiming` semantics need the authors' answer or a fUSI-BIDS definition. The author query has not been sent (needs owner approval).
3. **Alpha grid for the own baseline is poorly scaled.** A wider pre-registered grid needs a dated amendment.
4. **Motion confound and DLC–fUS alignment** need a dedicated control before any positive claim.

## GO / NO-GO

- **NO-GO** for claiming that fUS predicts running speed in sub-rat1703, or in any animal, from this evidence.
- **NO-GO** for claiming that the published result is reproduced or refuted.
- **GO** for one further step on the same candidate, only with: (a) a dated amendment widening the alpha grid, (b) a DLC–fUS sync check that identifies a lag, and (c) the motion control. This step needs owner approval because it would add compute and a protocol amendment.

The Milestone 20/100 is NOT reached as a positive scientific result. The checkpoint is reached as a documented outcome: a verified candidate, a verified data subset, and a negative result with its blockers evidenced.

## Decisions for the owner

1. Approve the dated amendment that widens the alpha grid, and the sync and motion controls, for a rerun on the same three sessions.
2. Approve sending the timing query to the UCL repository contact (`author_query_draft_timing.md`, not sent).
3. Decide whether to request the authors' GLM t-statistic maps, the step that would unblock closer replication.
