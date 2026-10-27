# Controls

Fixed in this file. Amendment A-1 (in `protocol.md`) records the change from the first draft, made before any result was obtained under this contract. After any result is seen, a change needs a new amendment entry; no criterion is changed silently.

## C0. Shared data and fold structure

- Development runs only (eight count-matched runs, six calendar dates). The holdout is excluded by name and is never read.
- Leave-one-calendar-date-out folds. Every fitted object (ridge models, wheel-on-Z mean mu(Z), residual scale profile, Markov transition probabilities, amplitude residual pool) uses training dates only.
- Test-wheel statistics are used only in the oracle diagnostic (C6), which cannot change any admissibility or verdict.

## C1. Transferability criteria for a wheel null (candidate A)

A surrogate may be used on real data only if its structure transfers across sessions. The check uses **training dates only** and does not require the surrogate to match any held-out statistic exactly.

Nested out-of-sample procedure, for each held-out date d and each training date j in D \ {d}:
1. Fit the generator on D \ {d, j}: neither the held-out date d nor the scored date j is used for fitting. Date j is therefore scored out of sample.
2. Generate draws for date j's Z and compute the statistic T on each draw. Let m_j be the median over draws.
3. Let O_j be the observed value of T on date j's wheel (a training date, so this is not test data for d). Let s_T be the between-session standard deviation of {O_j : j in D \ {d}}.
4. Criterion for T: |O_j − m_j| ≤ 2 s_T for every training date j in D \ {d}.

Cost: 30 generator fits in total (six held-out dates × five scored dates), each on four dates. Limitation: s_T is estimated from five values, and the four-date fits are weaker than the full training set. Both are stated; neither is a calibrated threshold.

Statistics:

| Id | Statistic T | Criterion |
|---|---|---|
| S1 | active fraction (non-zero frames) | step 4 |
| S3 | number of active episodes | step 4 |
| S4 | mean active-episode length (frames) | step 4 |
| S5 | residual variance on active frames (scaled) | step 4 |
| S6 | corr(abs residual, norm of Z) | step 4 |

S2 (exact-zero fraction) is removed: it is the complement of S1. The S2 id is not reused.

A candidate-A null is admissible for held-out date d only if S1, S3, S4, S5 and S6 all pass. Within-date variability is absorbed by the draws; between-session variability by s_T. s_T uses five training dates and each generator fit uses four; this is a stated limitation, and the tolerance is 2 s_T, not a calibrated threshold.

Reason for the rule: NE-EXP-002 surrogates (fitted on training dates) differed from observed wheels by −48% to +56% relative in active fraction, by up to about 2 times in episode count and length, and gave corr(|residual|, ||Z||) near zero where the observed correlation ranged from −0.16 to +0.35 per run. Step 4 asks whether the surrogate's level lies within two between-session SDs, which allows cross-session variation without demanding exact agreement.

## C2. Candidate A — two-component conditional generator

- Activity state: two-state Markov chain (exact zero vs non-zero). Transition probabilities estimated on training dates only. Option (b) of the first draft (fitting on the held-out wheel) is withdrawn: it uses held-out wheel statistics, which this contract excludes outside the oracle.
- Chain start: the stationary distribution of the training-date chain. The held-out run contributes nothing to the generator, not even its first frame.
- Amplitude: on active draws, mu(Z) + scale × r, where r is drawn in blocks (400 frames) from the pooled standardised residuals of active frames of **training dates**. Inactive draws are exactly zero.
- Null scenarios (outcome has no wheel relation):
  - zero_effect: AR(1) noise, no effect. Rejection rate of the declared test reported with its Wilson 95% interval. Calibration is judged by C3-B (flag rule), not by this interval.
  - measured_arousal: arousal correlated with the wheel and included in Z. Descriptive only: no equivalence margin is justified, so no numeric pass/fail is set. Both zero_effect and measured_arousal are reported side by side.
- Positive control: known_added_info (wheel effect R² = 0.05). Power ≥ 0.8 at 60 replicates is required for a negative conclusion to be informative.
- Confound control (expected detection, not a pass for the claim): hidden_arousal.
- Admissibility: C1 must pass for every held-out date before any real-signal run. A failure on any date blocks candidate A.

## C3. Candidate B — out-of-sample comparison of fixed models

- Statistic: per-date Δ_d and pooled Δ. No wheel surrogate and no permutation.
- Layer 1 decision rule (fixed): supported only if pooled Δ > 0 AND the date-level bootstrap lower bound (2000 resamples over six dates) > 0.

### C3-B. Inflation flag for the decision rule (zero-effect synthetic outcome)

- Replicates: 60 independent zero-effect replicates, fixed seeds.
- K = number of replicates in which the Layer 1 decision rule declares support.
- **INFLATION FLAG** if K ≥ 8 (rate ≥ 0.133).
- **NO GROSS INFLATION DETECTED** if K ≤ 7.

This second outcome is **not** a demonstration of calibration. Exact binomial values (`binomial_flag_table.txt`, from `scripts/binomial_flag_table.py`):
- a rule of true size 0.031 is flagged with probability 0.0005 (passes 'no gross inflation' 0.9995 of the time);
- a rule of true size 0.05 is flagged with probability 0.0098;
- a rule of true size 0.10 is flagged with probability 0.2484 and passes 'no gross inflation' 0.7516 of the time;
- a rule of true size 0.15 is flagged with probability 0.6953.

So the flag detects gross inflation only from roughly 0.10 upward, and a rule of size 0.10 is more often reported as 'NO GROSS INFLATION DETECTED' than flagged. The contract therefore never writes 'calibrated' for candidate B; the strongest permitted statement is 'NO GROSS INFLATION DETECTED at 60 replicates'.

- Positive control: known_added_info; power ≥ 0.8.
- Confound controls: hidden_arousal (expected detection) and measured_arousal (descriptive).
- Structure diagnostics: candidate B generates no wheel surrogate, so C1 does not apply to it. Its structural check is the stratified descriptive comparison in `method_comparison.md`.

## C4. Stop and escalation rules

- C1 failure on any held-out date → candidate A BLOCKED; no real fUS outcome is used.
- C3-B INFLATION FLAG → candidate B's rule is not used for inference; a revised rule requires a new amendment and a new calibration run.
- C3-B NO GROSS INFLATION DETECTED → permitted only for the descriptive reporting in C3; it does not allow an inferential claim.
- Positive control below power 0.8 → no negative conclusion from that design.
- Any compute beyond C5 → stop and request owner approval.

## C5. Computational budget (synthetic only; no paid compute)

- Replicates: 60 per scenario, four scenarios per candidate (zero_effect, measured_arousal, hidden_arousal, known_added_info).
- Draws: 99 per replicate for candidate A; none for candidate B.
- Budget: about 1 CPU-hour in total for both candidates (estimate, extrapolated from NE-EXP-002: 30 replicates × 99 draws × six scenarios took roughly 40 minutes under contention; not measured).
- A local diagnostic pilot of about 0.3 CPU-hour is permitted only after the contract is READY, and is not required. The budget is not increased without owner approval.
- Real fUS outcome runs: not covered by this budget; separate owner approval and a frozen protocol.

## C6. Oracle diagnostic (separate; cannot change any verdict)

- Purpose: compare the held-out date d's own wheel statistics (S1, S3, S4, S5, S6) with the surrogate draws fitted on the other dates, as a descriptive check of the procedure's behaviour on real structure.
- Output: reported per held-out date with the z-value (O_d − m_d)/s_T. It is recorded beside the verdict.
- Consequence: an oracle discrepancy beyond 2 s_T is a finding to be reported, and it triggers a protocol-amendment review before any real run. It does not by itself change the admissibility decision computed in C1.
