# RESEARCH METHOD — falsification-first

A beautiful reconstruction is not evidence by itself.

Before any result is seen, every experiment records the following in its folder (`experiments/_template/`):

| Element | Where |
|---|---|
| Research question | `question.md` |
| Estimand (population, intervention/condition, comparator, endpoint, summary measure) | `estimand.md` |
| Claim, with its evidence label | `claim.md` |
| Predictions under H1 (target), H2 (alternative), H0 (artifact/noise) | `alternative_hypotheses.md` |
| Dataset, version, checksum | `manifest.yaml` |
| Split strategy and leakage controls (subject, session, stimulus, temporal) | `protocol.md`, `controls.md` |
| Baselines (including a simple linear baseline and shuffled-label control) | `controls.md` |
| Metrics | `protocol.md` |
| Success criterion and falsification criterion | `protocol.md` |
| Frozen parameters and random seeds | `protocol.md` (under `FROZEN PROTOCOL`), `manifest.yaml` |
| Provenance (code commit, environment lock hash) | `manifest.yaml` |

## Procedure

1. Write the question and estimand.
2. Write the alternatives (H1, H2, H0) and what each predicts.
3. Write the protocol and controls. Commit it.
4. Set `status: FROZEN` in `manifest.yaml`. Only then run.
5. Record the outcome as `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, or `INVALIDATED`.
6. In `decision.md`, state what would change our model of the problem.

## Outcome rules

- A result that supports H1 but is equally predicted by H0 or H2 is `INCONCLUSIVE`, not `SUPPORTED`.
- A failed falsification criterion yields `NOT_SUPPORTED`, and the result goes to `null_results/INDEX.md`.
- If a leakage check fails, the affected result is `INVALIDATED`, not patched.

## Amendments

A frozen protocol may change only through an amendment section with date, reason, and whether the change was made before or after seeing outcome data. Post-outcome changes void a confirmatory claim.
