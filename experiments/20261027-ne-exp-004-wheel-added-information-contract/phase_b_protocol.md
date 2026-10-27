# Phase B protocol: descriptive predictive audit (NE-EXP-004)

Status: **FROZEN for Phase B on 2026-10-27**, with C-V2 NOT PASSED at freeze (see the freeze record at the end). Any change needs a dated amendment. No real-signal run is authorised by this document; that needs separate owner approval (section 11). The final fUS holdout is not read and is not named here.

## 1. Question and direction

On the eight count-matched development runs of sub-ALD002 (six calendar dates), does adding lagged wheel velocity (lags 0 to 6 s, 21 lags at 0.3 s frames) to a wheel-free model (eye and pupil, lags 0 to 6 s) reduce held-out prediction error for the whole-slice fUS signal?

Direction: fUS at frame t is predicted from lagged predictors at frames t−0 to t−20 (as in NE-EXP-001/002). The lags are nominal 0 to 6 s relative to the aligned target; the alignment is uncertain by at least about 0.5 s in some runs, and the physio–fUS clock offset and the onset-versus-end convention are unquantified (section 8), so the lag window is not a verified temporal window. The sign convention is Δ = L_nuisance − L_full, so **positive Δ means the wheel-augmented model predicts better**.

## 2. Metric, unit and uncertainty

- Loss: per-frame Gaussian predictive negative log-density, with variance taken from the training residuals of each model (as in `neural_echo.exp001.gaussian_loss`).
- Primary: pooled Δ over all scored frames of all held-out dates.
- Secondary: per-date Δ_d (mean over the frames of that date); number of dates with Δ_d > 0 (sign count, descriptive; see below).
- Grouping unit: **calendar date**. Runs within a date stay together. The effective sample for uncertainty is six dates from one animal.
- Per-date Δ_d: the frame-weighted mean of the per-frame loss difference over the scored frames of that date. The pooled Δ is the frame-weighted mean over all dates (weights are the scored-frame counts), as in `scripts/check_prediction_comparison.py`.
- Uncertainty: date-level bootstrap. Dates are resampled with replacement, 2000 random draws, seed 20261028, and the pooled Δ is recomputed for each draw. There are 6^6 = 46,656 possible resamples, so the percentile interval is coarse and can be narrow with six dates; it is reported with that caveat.
- Sign count: the number of dates with Δ_d > 0. The exact binomial sign test assumes independence of dates, and consecutive recording days may not be independent; it is therefore a descriptive count, not an independent test.
- Frame-level intervals are not reported because frames are autocorrelated.

## 3. Split scheme

Leave-one-calendar-date-out over the six dates. Each held-out date is scored once. All fitted objects use training dates only.

## 4. Training-only rule (binding)

Every quantity below is computed from training dates for each fold, and never from the held-out date:
- ridge regression (alpha 1.0) and any standardisation (means and scales from training rows);
- the lag structure (21 lags) and the wheel-free / full model definitions;
- the edge rule (rows with frame index below 40 are not scored) and the gap mask (20 frames are masked after each onset gap above 0.45 s, and every row whose 21-lag window touches a masked frame is dropped, which removes up to about 40 rows per gap), both structural and fixed in advance;
- the predictive variance (from training residuals).

No parameter is tuned on held-out scores. The timing checks in section 8 inform whether the run may be interpreted; they do not change any model setting.

## 5. Stratified description (descriptive only)

Held-out frames are split by the observed wheel value at the scored frame:
- **zero-wheel frames**: wheel value exactly 0;
- **non-zero-wheel frames**: wheel value not 0.

The threshold is fixed at exactly 0 and is not fitted. A zero-wheel frame still carries non-zero wheel lags 1 to 20 when earlier frames moved, so it is not a no-input control. A third reported sub-stratum, **zero-window frames** (all 21 lag values of the wheel are exactly 0), is the closest available no-wheel-input description; its frame count is reported, and it may be small. The labels say what the frames are, not what the animal was doing: the origin of the exact zeros is UNKNOWN (see `null_results/20261027-ne-exp-002-crt-v2-distribution.md`), so "rest" is not used as a label. Δ is reported pooled and per date for each stratum, with frame counts. The stratum uses the held-out run's own wheel, which is a predictor of the model, so this is a conditioning on a predictor for description only; it is not a null, not a test of conditional independence, and not evidence about cause.

## 6. Pre-specified sensitivity (descriptive; no selection)

Reported alongside the primary result, with no choice among them:
- edge rule 20 frames instead of 40 (the NE-EXP-001 setting);
- without the gap mask.

## 7. Reference not included

A wheel-shuffled reference (block permutation within each held-out date) is **not part of this protocol**. Its cost (about 3.5 s per replicate, 99 draws per date) would exceed the audit budget in section 10, so it would need its own budget and owner approval.

## 8. Pre-run checks and interpretation limits

From `phase_b_timing_checks.md` (structural, read-only):
- **C-V1 PASSED**: VolumeTiming length equals the frame count for all eight eligible runs.
- **C-V2 NOT PASSED** (tolerance 0.1 s, fixed before the corrected statistic was computed): the endpoint discrepancy between the onset span (gap excess removed) and the span expected from the quoted period 0.30013 s ranges from −0.106 s to +0.526 s over the eight runs. Two runs exceed the tolerance clearly (+0.53 s with seven gaps; +0.18 s with a 3.9 s gap) and one is marginally outside (−0.106 s). The endpoint discrepancy is at least about 0.5 s in some runs. The physio–fUS clock offset and the onset-versus-end convention (up to one frame, 0.3 s) are unquantified. All three must be stated with every result.
- **Correction record**: an earlier version of this check used the median onset interval and reported a drift of −1.08 to −1.47 s. That statistic is withdrawn: the median is not the mean period, and onsets are quantised to 1 ms. It is kept here for provenance only.
- Until C-V2 is resolved, lag-specific or temporal interpretations are not permitted. The lag-window-averaged Δ may be reported as a predictive association in this animal, with the alignment uncertainty stated; it is not described as robust to an unknown clock offset.
- **C-V3 PASSED**: physio covers all onsets for all eight runs.
- Open and not checked: the VolumeTiming convention (onset relative to frame start or end) and the physio–fUS clock alignment. Both are recorded as UNKNOWN.


## 9. Non-interpretations (required in every result)

1. Positive Δ does not show that the wheel carries information beyond arousal or any other unmeasured variable.
2. Δ does not show causal influence of the wheel on the fUS signal, and does not decode any mental or behavioural state.
3. The result is for one animal. Date-level intervals describe stability within this animal across six dates, not transferability to other animals or to a population.
4. A null or negative Δ does not show absence of a wheel-related signal; the design may be insensitive.
5. The zero-wheel versus non-zero-wheel split describes where the predictor value differs; it does not establish rest or movement.
6. Alignment uncertainty: the physio–fUS clock offset and the VolumeTiming convention are unresolved, and the endpoint discrepancy is at least about 0.5 s in some runs. Results are not robust to an unknown clock offset, and lag-specific readings are not permitted.
7. The target is the whole-slice fUS signal (not a region or a voxel), so no regional or anatomical claim follows.

## 10. Compute and budget

Six held-out folds, each with two ridge models and a 2000-resample bootstrap. Estimated well under 0.05 CPU-hours (the pilot used 0.10 CPU-hours for 60 synthetic replicates plus block A). Cap: 0.05 CPU-hours for the audit. Any increase needs owner approval.

## 11. Decision categories (for the independent review)

- **PROCEED**: the protocol is complete and internally consistent; checks are readable; limits are stated. Freezing is then allowed. Running still needs owner approval.
- **REVISE**: fixable defects in the protocol or its checks.
- **BLOCKED**: a methodological premise fails and cannot be fixed by wording.

Engineering readiness of the code and scientific validity of the protocol are reviewed separately.

## 12. Provenance of the pilot `fb75649` (stated for the record)

Commit `fb75649` is the commit that recorded the pilot results and the null record. The pilot itself was executed on the working tree on top of `abe5dec`, with its runner script untracked at run time. The committed runner (461 lines) is not byte-identical to the script that was executed (464 lines). Two items were recorded after the run: the bootstrap seed 20261028 (added to the protocol and manifest) and a counting bug in `git_head()` (fixed afterwards). Neither changed a result. This protocol is not a pre-registration of the pilot.

## Freeze record

- Frozen: 2026-10-27, Phase B only (NE-EXP-004). The manifest status stays PLANNED; the contract's candidate A and B status is unchanged.
- Condition at freeze: **C-V2 NOT PASSED** (endpoint discrepancy −0.106 to +0.526 s, tolerance 0.1 s). Temporal and lag-specific interpretation is not permitted until a dated amendment resolves C-V2.
- Independent review: protocol review returned PROCEED with three wording edits (applied in this freeze).
- Not authorised by the freeze: any real fUS run, any use of the holdout, any push or merge.
- The freezing commit is the one whose message begins "NE-EXP-004 Phase B: freeze".

## Amendments

None.
