# Milestone 20/100: final report (2026-10-27)

Scope: the Neural Echo goal contract for the Cybis Pereira et al. fUS record (Zenodo 15476373, CC BY 4.0), the Landemard ALD002 record, and the repository state. Local commits only; nothing pushed, merged or sent; the sealed holdout was not opened; no paid compute.

Earlier checkpoint: `docs/MILESTONE_20_OF_100.md` (commit `3e6fb40`). This report supersedes it.

## Verdict: CONDITIONAL

The checkpoint is reached as a documented, pre-registered result. It is not a neural decoding claim. The pre-registered rule is met on two unused sessions, but the evidence does not yet establish a neural predictive effect (see "Why not GO").

- **GO** would need a mean-corrected comparator, a working motion control, and a second animal, none of which exist.
- **BLOCKED** would be right if the rule were not met; it is met, but only under a weak comparator.

## Definition of Done

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | A-2 classified with its limits | DONE | A-2 is NOT SUPPORTED, and is invalid as a test of the expected lag and of the controls (sync search ±3 volumes, narrower than the 0–5 volume expected range; C5/C6 collapse to M0). See below. |
| 2 | A-3 implemented and checked, or rejected with reason | DONE | A-3 committed as spec (`25ddeb6`) and runner (`af4e0a8`) before any A-3 computation. Checked by exploratory stage E (`fff788a`) and a single final stage F run. |
| 3 | Independent analysis on new sessions, or explicit impossibility | DONE, with a limit | Stage F on ses-20210430 and ses-20210505 (unused sessions of the same animal). Independent of tuning; not independent of the animal. |
| 4 | Scientific review; reproducible results and code | DONE, with a limit | Fallback verifier `skeptic` on each stage (the reviewer agent is closed by its iteration cap). Findings applied to the write-ups. Code and outputs committed. |
| 5 | One final report with GO / CONDITIONAL / BLOCKED and evidence | DONE | This document. |

## What was done, in order

1. **Repository state.** STATUS corrected (frame-period claim marked unconfirmed; Next-3 renumbered). `7c79a4f`.
2. **Landemard ALD002 timing.** BLOCKED. `VolumeTiming` semantics are not established by any retrieved source (`docs/MILESTONE_QUALIFICATION_2026-10-27.md`).
3. **Dataset selection.** Cybis Pereira et al. (CC BY 4.0, Zenodo primary source) chosen as the candidate, because it provides raw fUS, behaviour (DLC) and authors' decoder outputs.
4. **Authors' outputs.** 104 files fetched with SHA-256 manifest. Their test r² reproduces the quoted intra-animal maximum (0.602 vs 0.6); inter-animal 0.354 vs 0.36. `b4403b1`.
5. **Own baseline, A-1 (first result).** Protocol committed before fitting (`7893a24`), with amendment A-1 (the "mask-brain" file is the authors' decoder weights; excluded). Result NOT SUPPORTED: out-of-session r² 0.012, 0.001, −0.037. `0228f5d`.
6. **A-2 rerun.** Widened alpha grid, training-only sync lag in ±3 volumes, motion-proxy control. Result NOT SUPPORTED: r² 0.017, 0.004, −0.031. Review found the sync range too narrow and C5/C6 degenerate. `a92c79d`.
7. **A-3 spec (`25ddeb6`) and runner (`af4e0a8`)**, committed before any A-3 computation.
8. **A-3 stage E (exploratory, `fff788a`).** On the three original sessions: folds 1–2 pass; fold 3 fails with both controls matching M1. Labelled exploratory; not independent.
9. **A-3 stage F (final, one run).** On the two unused sessions: rule met (PASS by the script's string), with the caveats below.

## Classification of earlier results

- **A-1 (first own baseline):** NOT SUPPORTED on the pre-registered rule. Its alpha grid was poorly scaled (effectively unregularised), so it does not test regularised linear prediction. Recorded in `null_results/20261027-speed-baseline-sub-rat1703.md`.
- **A-2:** NOT SUPPORTED under its rule, but not a valid test of the expected haemodynamic lag (sync range too narrow) and its motion controls collapse to the mean predictor. Not evidence of absence.
- **A-3 stage E:** exploratory; NOT SUPPORTED on the original sessions (fold 3 fails, controls match M1 there).
- **A-3 stage F:** the pre-registered rule is met. Its evidential weight is limited, for the reasons below.

## Stage F: what it does and does not show

- Both test sessions have M1 r² above M0 and a within-session interval above zero. ses-20210505 has z = 2.71, only just above 2.
- Both M1 r² values are negative. The r² is measured against each test session's own mean, so the sign shows only that M1 is worse than an unobtainable oracle constant.
- The entire M0 deficit equals the training-versus-test mean offset (an algebraic identity from the JSON). After correcting for it, M1 retains about 0.03–0.04 of variance. That comparator was not pre-registered.
- The motion controls C5 and C6 select alpha at the grid edge and sit at M0. They cannot discriminate, so motion is not excluded.
- Across five held-out sessions of this animal, M1 beats M0 in four.

## Why not GO

1. The pre-registered comparator (M0) confounds predictive skill with the session-level offset.
2. The motion controls are inert, so a motion explanation cannot be excluded.
3. One animal.
4. The stop rule forbids further tuning on the same sessions, so these limits cannot be resolved here.

## Blockers and what would unblock them

- **Comparator.** A mean-corrected comparator must be written as a new amendment before a test. It needs new sessions to be valid.
- **Motion control.** Needs a grid scaled to its features and a voxelwise proxy. A new amendment and a new test.
- **Second animal.** Other animals in the same dataset (sub-rat2306, sub-rat2403, sub-rat73, sub-rat75, sub-rat83, sub-rat84) are available. Each needs the frozen spec with the new comparator, pre-registered.
- **GLM lag kernels** (authors' t-statistic maps) remain absent; closer replication stays blocked.
- **Landemard ALD002 timing** remains BLOCKED (author query drafted, not sent).

## Recommended next step (for the owner to decide)

Pre-register amendment A-4 with (a) a mean-corrected comparator and its threshold, (b) a DVARS-style motion control on a grid scaled to its features, and (c) one further animal from this dataset, with the same frozen spec. Test once. Do not re-tune on sub-rat1703.

## Reviews and reproducibility

- Each stage has a `skeptic` fallback review; findings are recorded in the corresponding milestone notes. The reviewer agent remains closed by its iteration cap.
- Code: `scripts/run_cybis_speed_baseline.py` (A-1 frozen functions), `scripts/run_cybis_speed_baseline_a2.py` (A-2), `scripts/run_cybis_speed_baseline_a3.py` (A-3), `scripts/check_cybis_speed_sync.py` (sync check).
- Data: git-ignored `data/raw/cybis_pereira_2026/`, with SHA-256 manifests (`MANIFEST.sha256.tsv`, `MANIFEST_rawdata.sha256.tsv`).
- Tests: `scripts/verify_repo.py` passes (43 tests) at each commit that touched code.

## Owner decisions still open

1. Approve A-4 as outlined above, or choose another independent dataset or direction.
2. Approve sending the two drafted author queries, one per addressee, after each recipient is verified (`docs/AUTHOR_QUERIES_DRAFTS_NOT_SENT.md`).
