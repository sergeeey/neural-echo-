# Negative result: CRT v2 conditional wheel null fails its distributional diagnostics (NE-EXP-002)

Status: **REVISE** under the pre-registered criteria. No null inflation flag. Synthetic only.
Code: local commit 04267d6 (not pushed); diagnostics JSON produced at 6d430f4 before that commit.
Provenance: `experiments/20261027-ne-exp-002-temporal-latent-confounding/crt_run_provenance.md`.

## What failed

1. **Quarter variance ratio after standardisation:** median 2.50 across 8 development runs (criterion 1.5). Seven of eight runs exceed 1.5. Standardisation worsened three runs (03-20: 3.14 to 5.17; 03-23: 6.28 to 7.55; 03-30: 1.47 to 2.53).
2. **Block variance ratio (max/min across 400-frame blocks):** median about 6.3 x 10^4 (criterion 3); all eight runs exceed 3. Blocks with no nonzero wheel frame have residual variance 5e-6 to 4.9e-5 in the cases shown in section C; the highest-variance blocks reach 0.8 to 8.3. Whole-run variance on active frames is 0.006 to 0.071 (`crt_wheel_investigation.txt`, section B).
3. **Activity structure of conditional draws:** active fraction 0.96 to 1.00 in the draws against 0.09 to 0.24 observed; 1 to 11 episodes against 113 to 410 observed per run (the two-component draws give 149 to 248). The conditional draw never reaches the exact zero the recording contains.
4. **Dependence on physiology:** median corr(|residual|, ||Z||) is 0.120 observed and 0.003 to 0.013 in the surrogates. Per run, the observed correlation ranges from -0.16 to +0.35 and the surrogate stays near zero in six of eight runs.

## What passed

- No pilot null inflation: the largest conditional rejection on a null scenario is 3/30 (zero_effect, v2). In the 30-replicate runs the independent comparator also stays nominal; at 100 replicates it does not under measured_arousal (16/100, see the supplementary run).
- v1-config and v2 use identical synthetic series and RNG stream (`crt_pairing_check.txt`).
- The v1 flags reproduce the saved smoke statistics (maximum difference 0.0, 1 rep x 19 draws).

## Origin of the exact zeros: UNKNOWN

`crt_wheel_raw_audit.txt` (read-only, development runs): the raw `wheel_velocity` channel is sampled at 1000 Hz, has no NaN, and is exactly zero in 80 to 94 percent of samples. Per run, the median zero-run length is 20 to 178 samples at 1000 Hz (that is, 20 to 178 ms; these are raw samples, not 0.3 s frames) and the longest is 55 to 310 s (18 development runs in the audit; the diagnostics use 8). The sidecar documents no fill code, but that absence is not verified beyond the sidecar. It gives no encoder resolution or velocity derivation, so physical rest and encoder quantisation (no tick in the sample interval) cannot be separated. The origin is recorded as UNKNOWN. Checks made: this subject archive (sub-ALD002.zip) contains no README or encoder description; dataset-level files were not examined (only `scans.tsv` and the wheel sidecar with one line, "Wheel velocity from rotary encoder", cm/s). A web search located the dataset record (DOI 10.5522/04/31376338.v2) and the analysis repository agneslandemard/fusi_analyses; the publicly listed behaviour scripts do not show how wheel velocity is derived, and the modules that might contain that processing were not reachable. No external confirmation of the encoder resolution was found.

## Interpretation (consistent with, not established)

The data are consistent with a misspecified conditional null for this variable: a continuous Gaussian residual permuted within blocks does not reproduce the exact-zero component or the state-dependent variance. Quarter standardisation does not address this. The causal chain is not established. Alternatives that the present data do not exclude:

- (a) Bursty rest bouts lasting minutes, which a two-state chain with the fitted transition rates would rarely produce as all-zero blocks, yet four of eight runs contain one, and two more have only 0.5% and 1.2% nonzero frames in some block.
- (b) Heavy-tailed spikes: maximum step is 23 to 89 times the mean step in every run.
- (c) Misfit of the linear mu(Z) on the wheel.
- (d) Block means drifting more than expected: block-mean dispersion up to 8.9 times expectation and lag-1 correlation up to 0.68.
- (e) The thresholds 1.5 and 3 were not calibrated against a stationary zero-inflated simulation.

No intervention (for example, quarter ratio on active frames only) has been run.

## Alternatives assessed (neither validated)

- **Two-component conditional generator** (Markov activity state plus amplitude from permuted active residuals). Median across runs: active fraction 0.139 against 0.120 observed; episode count 219 against 172 (per run 149 to 248 against 113 to 410); corr(|residual|, ||Z||) 0.013 against 0.120. Per run, the active fraction error ranges from -48% to +56% (for example 0.242 observed against 0.125 surrogate; 0.091 against 0.141). Episode length is 4.1 to 12.2 observed against 6.6 to 8.0 surrogate. The state-wise residual variance agreement holds by construction (stationary residual is -mu/scale; active residuals are resampled from the observed ones), so it is not evidence for the generator. Not validated.
- **Date-level prediction comparison.** Synthetic calibration at 20 replicates: zero-effect false-positive rate 4/20 against a nominal 0.05 (Wilson 95% about 0.08 to 0.42; this interval excludes the exact sign-test size of 0.031, so the rate is above nominal). It does not separate a hidden confounder (10/20) from a real effect (13/20); mean pooled deltas 0.013 and 0.026 overlap at this replicate count. Not a calibrated test.

## What this does NOT mean

- It does not show that the wheel carries no information about fUS. The real-signal test was not run; NE-EXP-001 stays PLANNED / BLOCKED.
- It does not show the zeros are artefacts. Their origin is UNKNOWN.
- Lower rejection rates on synthetic null scenarios (for example 4/100 and 6/100 under zero_effect, or 4/100 under measured_arousal) do not validate the conditional procedure. Its surrogates fail the distributional checks on the real development wheel, so its synthetic behaviour need not transfer to real data.
- The approximate permutation procedure is not an exact conditional randomisation test.
- The supplementary 100-rep v1 run completed (`crt_pilot_v1_full100.json`). Under `measured_arousal` the independent comparator rejects 16/100 and the conditional test 4/100; the verdict rests on the diagnostics, not on this run.

## Kill analysis

Killed: the claim that the approximate conditional block permutation of the wheel residual gives a valid null for this recording (scope: this procedure, this data, synthetic outcomes).
Not killed: the predictive question on real data; the independent-permutation comparator as a diagnostic; the pre-registered criteria themselves.

## Revival condition

A new procedure that preserves the activity state, episode structure and physiology dependence in surrogates, pre-registered as a new contract version, and checked independently before any real-signal use.
