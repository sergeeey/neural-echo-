# Decision

Status: **PLANNED**. No result under this contract. No real fUS outcome used. Holdout not read.

## Prior result this contract builds on (closed)

CRT v2 (NE-EXP-002) is a completed negative methodological result, verdict REVISE under its pre-registered criteria. Its artifacts are retained: `experiments/20261027-ne-exp-002-temporal-latent-confounding/` and `null_results/20261027-ne-exp-002-crt-v2-distribution.md`. Its criteria are not changed here.

## Candidate status (planning stage; the verdict is decided only by the checks below)

| Candidate | Current status | What decides it | Not yet run |
|---|---|---|---|
| A: two-component generator, training-fitted only | **BLOCKED** until C1 passes | C1 (training-date nested transferability) for every held-out date | C1 on the development wheel. It uses no outcome, but it is a diagnostic run and is permitted only after READY (C5). |
| B: out-of-sample fixed-model comparison | **BLOCKED** for inference | C3-B: NO GROSS INFLATION DETECTED or INFLATION FLAG at 60 zero-effect replicates; no calibration claim in either case | C3-B at 60 replicates (about 0.3 CPU-h, pilot after READY). |

Neither status changes until these checks are run and the results are reviewed. Passing C1 or C3-B would still not validate a candidate. C3-B NO GROSS INFLATION DETECTED would still not be calibration.

## Simpler checkable framing (used because both candidates are blocked for inference)

Layer 1 only, descriptive: per-date Δ_d and pooled Δ on the development runs, with a date-level bootstrap interval, plus the stratified check by wheel-rest vs wheel-active frames. It makes no p-value, conditional or causal claim and needs no new generator. This is the framing recommended for the next step.

## Pilot result (2026-10-27; `pilot_results.json`, `pilot_summary.md`, `pilot_log.txt`)

- Candidate A, C1: admissible for 2023-03-21 and 2023-03-28 only; **not admissible** for the other four held-out dates. Contract outcome: **BLOCKED**. The only failing C1 criterion is S3 (episode count); the rest-length and amplitude mismatches are diagnostics, not C1 criteria. The S3 margins are small for three of the four failing folds (0.3% to 1.2% over the limit for two of them) and large for two (fold 03-15: 260 against 228.1; fold 03-30: 102.5 against 76.6), so the verdict rests on the clear failures and on the contract's requirement of every date.
- Candidate B, C3-B: K = 1 of 60 zero-effect replicates. Outcome: **NO GROSS INFLATION DETECTED**. This is not a demonstration of calibration.
- CPU used: 0.10 of 0.3 CPU-hours (process time). No budget increase.
- Negative result recorded in `null_results/20261027-ne-exp-004-candidates-ab-pilot.md`.
- Verdict category for the independent review: A is BLOCKED on scientific grounds, B is descriptive-only, and engineering readiness is separate from validity.

## What this decision does not mean

- It does not show that the wheel carries no predictive information about fUS.
- It does not validate any candidate.
- It does not establish conditional independence, a causal effect or a mechanism.
- It does not claim that measured_arousal and zero_effect differ or agree; the comparison is descriptive.

## Owner actions (not performed by this contract)

1. Approve or refuse the pilot (C5, about 0.3 CPU-h) that runs C1 for candidate A and C3-B for candidate B.
2. Decide whether to send the technical query to the dataset authors (`author_query_draft.md`; NOT sent; recipient not verified).
3. Choose the replicate count or bound for C3-B before freezing, if the owner judges the current 60-replicate rule too strict to be informative (operating characteristics in `binomial_flag_table.txt`).
4. Resolve NE-EXP-002 vs NE-EXP-003 numbering (`docs/RESEARCH_BACKLOG.md` item 13); this contract took NE-EXP-004.
