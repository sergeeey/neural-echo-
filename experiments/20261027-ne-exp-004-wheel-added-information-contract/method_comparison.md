# Method comparison (NE-EXP-004, planning stage)

Status of every row: planning only. No result is claimed.

| Aspect | Candidate A: two-component generator, training-fitted | Candidate B: out-of-sample fixed-model comparison |
|---|---|---|
| What it estimates | Pooled Δ, with a surrogate null only if C1 passes. No p-value is claimed by default | Pooled Δ and per-date Δ_d with a date-level CI |
| Layer covered | Layer 1 (predictive). A conditional-null claim (Layer 2) is not made under this contract | Layer 1 only |
| Null used | Wheel surrogate: Markov activity state fitted on training dates; amplitude from pooled training-date active residuals | No surrogate; the zero-effect C3-B check is the only null-based check |
| Assumption about Y ⊥ W | Would need the surrogate to reproduce the wheel's conditional structure; the C1 transferability check is the test of that, and it has not been run | None beyond the fixed model class |
| Structure diagnostics | C1 transferability, training-date nested, criteria S1, S3, S4, S5, S6 (required before any real use) | Not applicable; stratified descriptive check (below) |
| Known failure mode | Activity state, episode structure and physiology dependence not reproduced in NE-EXP-002 surrogates | The decision rule is uncalibrated. A related date-level sign-test rule (a different rule) gave 4/20 false positives under zero effect at 20 replicates. A confound (hidden arousal) is indistinguishable from a real effect |
| Current status | BLOCKED until C1 passes for every held-out date; wheel-zero origin UNKNOWN | BLOCKED for inference; C3-B at 60 replicates not yet run; descriptive use only after freeze and owner approval (P4) |
| What the C3-B / C1 result can and cannot say | C1 pass would permit a real-signal run; it would not validate the method | C3-B NO GROSS INFLATION DETECTED would not establish calibration |
| Compute | About 0.7 CPU-hour synthetic (C5, estimate) | About 0.3 CPU-hour synthetic (C5, estimate) |
| Simplest checkable framing | Not simpler than B | Descriptive per-date Δ and CI, stratified by wheel-active vs wheel-rest frames |

## Stratified descriptive check (candidate-independent, no test)

For each development date, split held-out frames by wheel state (rest: exact zero; active: non-zero) and report the loss difference Δ within each stratum. This shows where any predictive gain sits, without a p-value. It can reveal that a gain comes only from active frames, which would be consistent with H3 in `alternative_hypotheses.md`.

## Recommendation (planning stage, not a verdict)

Keep candidate B as the simpler, checkable framing for Layer 1 only: per-date Δ with a date-level CI and the stratified descriptive check. Candidate A stays BLOCKED until C1 passes on the development runs. Neither candidate may be used for Layer 2 or Layer 3 claims.
