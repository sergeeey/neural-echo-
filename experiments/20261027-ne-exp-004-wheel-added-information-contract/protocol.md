# Protocol

## FROZEN PROTOCOL

> NOT FROZEN. Status is PLANNED. This section is fixed only when `status` in `manifest.yaml` becomes FROZEN, before any real-signal run. Changes after freezing need a dated entry under "Amendments".

## Dataset

- Name and version: sub-ALD002 development runs (count-matched; holdout excluded). Synthetic controls use the same behavioural inputs.
- Source, licence, retrieval date: see `manifest.yaml` (`CC BY-NC 4.0`, retrieved 2026-10-26).
- Per-file SHA-256 checksums: `manifest.yaml` `dataset.files`.
- Known data limitations: exact-zero frames in the wheel channel with unknown origin (`null_results/20261027-ne-exp-002-crt-v2-distribution.md`); VolumeTiming convention unverified; physio clock alignment assumed.

## Split strategy

- Unit of splitting: calendar date (leave-one-calendar-date-out, six primary dates).
- Train / validation / holdout definition: training dates fit every model and every wheel-on-Z model; the held-out date is scored once per fold. No separate validation split is used for the decision rule, which is fixed in `controls.md`.
- Holdout used once: no. The final holdout is not read under this contract.

## Leakage controls

- Subject leakage check: one subject only; this is stated as a limitation, not a control.
- Session leakage check: runs of the same date stay in the same fold.
- Stimulus leakage check: not applicable (no stimulus labels used).
- Temporal permutation control: block permutation (blocks of 400 frames, 120 s) for any wheel null; not applicable to candidate B.
- Fold-wise isolation check: the test run's outcome must not change any fitted object or any draw under a fixed seed (test in `tests/test_crt.py`, to be re-implemented for the new scripts).

## Baselines

- Simple linear baseline: the wheel-free ridge model (eye and pupil lags).
- Majority-class / chance baseline: not applicable (continuous outcome); the zero-model (predict the training mean) is reported.
- Shuffled-label control: the zero-effect synthetic outcome (C2, C3 in `controls.md`) plays this role.

## Metrics

- Primary metric and its uncertainty method: pooled held-out Δ (positive = wheel helps); uncertainty by date-level bootstrap (2000 resamples over six dates).
- Secondary metrics: per-date Δ_d; exact sign count of positive dates; structure statistics S1 to S6 per run (candidate A only).

## Model and run parameters

- Model and hyperparameters: ridge regression, alpha 1.0, standardised features, Gaussian predictive variance from the training residuals; lags 0 to 6 s (21 lags, 0.3 s frames); edge rule: rows with frame index below 40 not scored; gap mask: 20 frames after onsets with gaps above 0.45 s.
- Random seeds: 20261027 for all synthetic runs, as in NE-EXP-001/002.
- Software environment (lock file hash): `uv.lock`; hash to be recorded at freeze.
- Success criterion (copied from `claim.md`): see `claim.md`, including prerequisites P1 to P4.
- Falsification criterion (copied from `claim.md`): see `claim.md`.

## Amendments

**A-1 (2026-10-27, before any result under this contract).** Replaces the first-draft criteria in `controls.md`:
- Candidate A: the generator is fitted on training dates only; option (b) (fitting on the held-out wheel) is withdrawn; the amplitude residual pool is drawn from training dates, not from the held-out run.
- S1, S3, S4, S5, S6 are replaced by the transferability rule in `controls.md` C1 (training-date nested out-of-sample check: for each scored training date j, the generator is fitted on the dates other than the held-out date d and j; tolerance 2 × between-session SD). The first-draft fixed tolerances (0.02, 15%, 25%, 0.05) are withdrawn. S2 is removed as redundant with S1.
- Candidate B: the Wilson-bound calibration criterion is replaced by the C3-B flag outcome (INFLATION FLAG if K ≥ 8 of 60; NO GROSS INFLATION DETECTED otherwise). The exact binomial values are in `binomial_flag_table.txt`. The outcome is explicitly not a calibration proof.
- measured_arousal versus zero_effect is descriptive only; no equivalence margin is set.
- Oracle diagnostic (C6) added; it cannot change the verdict.

Reason: the first-draft tolerances could not be met by a training-fitted generator (NE-EXP-002) and, under option (b), passed by construction. The first-draft B criterion had operating characteristics that reject a correctly sized rule (true size 0.031 to 0.05) about 56% to 81% of the time (the first-draft Wilson-bound criterion is not in `binomial_flag_table.txt`; its 19% and 44% pass probabilities come from the same binomial model, computed by hand and checked by the reviewer, 2026-10-27). No result under this contract has been seen.
