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
