# Negative result: NE-EXP-004 diagnostic pilot, candidates A and B

Status: negative result for the candidate procedures as specified in the contract (abe5dec). Synthetic and development-wheel structure only. No real fUS outcome used. Holdout not read. Synthetic results do not validate any method.

Code: `abe5dec` (scripts `run_nex004_pilot.py`, `summarise_nex004_pilot.py`, untracked at run time). Seeds 20261027 (block A and block B synthetic series) and 20261028 (block B bootstrap). Process CPU time 0.10 of 0.3 CPU-hours. Bootstrap seed 20261028 (block B). The "uncommitted entries at run time: 1" value recorded in `pilot_results.json` comes from a counting bug in `git_head()` (fixed in the script after the run; it does not describe the code that ran). No data or result was changed by the fix. Full results: `experiments/20261027-ne-exp-004-wheel-added-information-contract/pilot_results.json`, summary `pilot_summary.md`, log `pilot_log.txt`.

## Candidate A — training-only two-component generator (contract C1)

- Admissible for held-out dates 2023-03-21 and 2023-03-28 only. Not admissible for 2023-03-15, 2023-03-20, 2023-03-23, 2023-03-30. The contract requires every held-out date, so **A fails C1**.
- The only failing C1 criterion is S3, the number of active episodes. Date 2023-03-30 has 412 observed episodes against 152 to 204 predicted by the five out-of-sample fits. Margins over the limit 2·s_T: fold 03-15 260 against 228.1; fold 03-20 226.0 against 225.3 (0.3% over); fold 03-23 221 against 218.5 (1.2% over); fold 03-30 (date 03-15) 102.5 against 76.6. The two admissible folds pass narrowly (fold 03-28: 224 against 225.1; fold 03-21: 208 against 214.4), so the 2-of-6 split sits close to the limit. The contract still requires every date. The exact-zero transition rate p01 varies between dates by a factor of about four (0.011 to 0.043), which the generator does not carry across sessions.
- Rest and movement diagnostics (per scored date, out-of-sample; these are diagnostics, not C1 criteria): the surrogate rest episodes are longer than observed (median 26 to 46 frames against 11 to 28). The surrogate active-amplitude medians lie in 0.015 to 0.115 against observed 0.000 to 0.289. The observed exit rate p10 (0.082 to 0.245) is not reproduced: the surrogate reproduces its own fitted rate (0.113 to 0.166), not the observed one.
- Oracle C6 (test-date statistics; descriptive only): the held-out z-values are mostly within ±2, with S4 = +2.32 for 2023-03-20 and S3 = +5.85 for 2023-03-30. Oracle values cannot change admissibility and are not used for the verdict.

## Candidate B — out-of-sample comparison (contract C3-B)

- 60 independent zero-effect replicates. K = 1 replicate declared support (pooled Δ > 0 and date-level bootstrap lower bound > 0). Wilson 95% interval for the rate: [0.003, 0.089].
- Outcome under the fixed rule (K ≥ 8 flags): **NO GROSS INFLATION DETECTED**. This is not a demonstration of calibration. A rule of true size 0.05 would be flagged with probability 0.0098, and a rule of size 0.10 with probability 0.25 (`binomial_flag_table.txt`), so the test has low power to detect moderate inflation.

## Verdict (engineering versus scientific validity kept separate)

- A: **BLOCKED** scientifically. The generator does not transfer across sessions, so it cannot serve as a wheel null for the predictive claim.
- B: **NO GROSS INFLATION DETECTED** at 60 replicates. Scientifically the rule is still uncalibrated; the result licenses only descriptive reporting after freeze and owner approval.
- Engineering: the pilot ran to completion within the CPU budget and all outputs are saved. This is engineering readiness only and does not make either method valid.

## What this does not mean

- It does not show that the wheel carries no predictive information about fUS. The question is open at Layer 1.
- It does not show that the exact zero frames are artefacts. Their origin remains UNKNOWN.
- It does not establish conditional independence or any causal or mechanistic claim.

## Simplest next discriminating test

Layer 1, descriptive, on the development runs once the protocol is frozen and the owner has approved the real-signal run: per-date Δ_d and pooled Δ with a date-level bootstrap interval, plus the stratified split by wheel-rest versus wheel-active frames. It needs no generator, and its sign pattern across dates would show whether any gain is driven by one date, as the S3 failure suggests. It is not run here.

## Kill analysis

Killed: the approximate training-fitted two-component generator as a wheel null for this recording (scope: this generator, this development data, these criteria).
Not killed: the predictive question at Layer 1; the descriptive stratified comparison; the C1 criteria themselves.
