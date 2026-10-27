# Protocol: own speed-decoding baseline on raw fUS (Cybis Pereira et al., Zenodo 15476373)

Status: written before any fit on the raw data. Changes after the first fit require a dated amendment at the end of this file.

## L0 classification

**Predictive.** The question is whether fUS blood-volume signals predict running speed out of session. It is not causal, not a mechanism claim, and not a claim about thought or internal states. (`docs/PROJECT.md`, `AGENTS.md` scientific rules.)

## Estimand

- Population: one animal, sub-rat1703, three recording sessions (ses-20210407, ses-20210412, ses-20210421). Sessions are the unit of generalisation. Other animals are not in the estimand.
- Endpoint: instantaneous running speed (cm/s) at each fUS volume time, computed from DLC body position.
- Summary measure: out-of-session coefficient of determination r² on each held-out session.
- Comparator: a constant mean predictor fitted on the training sessions, and a circular-shift null of the prediction (see Controls).
- MCID: not defined. Stated as undefined; no practical threshold is claimed.
- Intercurrent events: none modelled. Frames with missing motion are excluded, not imputed.

Sentence: we estimate out-of-session r² of running speed from the fUS blood-volume time series of one animal, comparing a ridge model against a mean predictor, with each session held out in turn.

What this does NOT mean:
1. Does not show the signal is blood-volume coupling to neurons; it may be motion artefact (see Confounds).
2. Does not generalise to other animals or other probes.
3. Does not establish temporal precedence or any lag structure beyond the one tested.

## Data (fixed)

- fUS: `rawdata/sub-rat1703/ses-<s>/fus/*_pwd.nii.gz` (power Doppler NIfTI). Voxel selection: finite values and non-zero temporal variance within the session, computed from that session's data only. No external mask.
- The file `derivatives/decode-speed/sub-rat1703/*mask-brain*_weights.nii` is NOT a brain mask. It holds values from -4 to 7 with about half the voxels non-zero, consistent with the authors' trained decoder weights. It is not used anywhere in this analysis, because the authors fitted it on all sessions including the test session.
- Frame times: `VolumeTiming` in the `_pwd.json` sidecar (regular, 0.6006 s steps in the first session checked).
- Motion: `rawdata/.../motion/*_tracksys-DLC_motion.tsv` (50 Hz, body_x, body_y in cm; likelihood columns present but not used for filtering in the baseline; see Controls).
- Checksums: `data/raw/cybis_pereira_2026/MANIFEST_rawdata.sha256.tsv` (git-ignored) with SHA-256 per file.

## Preprocessing (fixed before fitting)

1. Speed: body position median-filtered over 0.2 s, speed = |Δposition| / Δt at 50 Hz, then linearly interpolated to fUS volume times.
2. Voxels: non-zero, finite voxels inside the brain mask. Within each session, each voxel is z-scored over that session's frames. (Z-scoring per session uses only that session, so the held-out session is not used for the training statistics. This is an accepted, stated choice; it makes the held-out session's own mean and variance enter the features of that session. See Confounds.)
3. Features: PCA fitted on training sessions only, keeping k components; lags of the PCs at 0 to L frames (L = 5, covering 3 s).
4. Target: speed at time t, from fUS frame t.

## Split (no leakage by construction)

- Outer: leave-one-session-out over the three sessions. Each session is the test set once; the other two are training.
- Inner (hyperparameters only): within the training sessions, leave-one-session-out again. The test session is never seen by tuning.
- Hyperparameters: ridge alpha over {1, 10, 100, 1000}; k over {10, 20, 50}; L fixed at 5.
- Selection criterion: mean inner r². Chosen once per outer fold. Not revised after the outer result is seen.

## Models

- M0 (mean): predicts the training mean speed.
- M1 (ridge): PCA(k) + lags + ridge, as above. This is the baseline.
- M2 (PCA + ridge) equals M1 by definition here; no separate model is added unless M1 fails the controls.

## Controls (pre-specified)

- C1 circular-shift null: the prediction of M1 is circularly shifted in time within the held-out session by shifts of at least 20 frames (about 12 s). Report null mean, sd, z. The M1 r² is compared with this null. Reminder: a shifted null of r² is centred below zero, so it tests alignment, not chance; it is reported with z, not as the sole test.
- C2 mean-predictor comparison: M1 minus M0 on each held-out session, paired, with a circular-block bootstrap over frames (block 20 frames). This is within-session uncertainty and is labelled as such. It is NOT an independent check across sessions.
- C3 session-level comparison: with three sessions, the per-session M1 − M0 differences are reported individually. Three is too few to estimate a between-session variance; no between-session interval is claimed.
- C4 sync check (training data only): the lag of maximum cross-correlation between speed and the mean fUS signal over the training sessions is reported. A lag far from the expected hemodynamic range (0 to 3 s) is a red flag, not a fitted parameter.
- C5 motion-confound probe: r² of predicting speed from the mean fUS signal alone (a single regressor) on held-out sessions. If this matches M1, the signal is not multivariate.

## Confounds (named, not solved here)

- Body motion produces Doppler artefacts; speed is the main driver of motion. A high r² can be motion, not haemodynamics. This baseline does not separate them. (UNKNOWN: whether the clutter filter removes it.)
- Per-session z-scoring uses held-out-session statistics within that session's own features (stated in Preprocessing).
- The authors' own decode outputs (`decode-speed`) used a different pipeline and are not used as inputs here.

## Comparison with published values

The preprint (bioRxiv 10.1101/2025.07.15.663536) quotes maxima: intra-animal r² up to 0.6; inter-animal up to 0.36. This baseline is a different pipeline (own preprocessing, own split). Any agreement or disagreement is reported as a comparison, not as reproduction. The published Cell Reports text was not accessible (HTTP 403), so its method details are UNKNOWN beyond the preprint.

## Decision rules (fixed)

- The baseline counts as showing out-of-session predictive value only if: M1 mean out-of-session r² > M0 on all three held-out sessions, AND C1 z > 2 on all three, AND C5 does not match M1.
- If C5 matches M1, the result is reported as "fUS-global signal predicts speed", with the motion confound open.
- Otherwise: NOT SUPPORTED on this subset.

## Amendments

- **A-2 (2026-10-27, after the first result `0228f5d`, before any rerun; approved by the owner with conditions).** The first result is retained unchanged in `docs/results/cybis_speed_baseline.json`. A-2 defines a new, separate procedure; it does not overwrite the first.
  1. **Alpha grid widened and log-spaced:** alpha in {1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7}. Reason: the first grid left every inner r² nearly unchanged across its range (see `0228f5d` review), so it did not test regularisation.
  2. **Sync identified from training data only:** for each outer fold, the lag L* in [−3, +3] volumes maximising the absolute cross-correlation between speed and the mean z-scored fUS signal over the training sessions is chosen. Speed is then shifted by L* for the held-out session. The test session is not used to choose L*. Reason: the first sync check found no identifiable lag; this rule uses only training data.
  3. **Motion-proxy control C6 (new):** predictor = the fUS frame-to-frame change magnitude of the mean z-scored signal, with lags 0 to 5, fitted by ridge on training sessions. If C6 matches M1 on held-out sessions, M1 is read as a motion proxy. Reason: the Doppler artefact confound was not separated.
  4. **Decision rule unchanged** from the original protocol, applied to A-2 results. An A-2 pass does not turn the A-1 result into a pass.
  5. **Still not done:** no holdout, no push, no merge, no email, no paid compute. The three sessions are the same.
  6. **A-2 record, written AFTER the A-2 run for transparency (not pre-registered):** the C5 definition (z-scored global mean), the seed 20261028 and the C6 alpha procedure were implemented in `scripts/run_cybis_speed_baseline_a2.py` and are recorded here only after the run. The independent review found two problems that A-2 does not solve: (a) the sync search of ±3 volumes is narrower than the 0 to 3 s (0 to 5 volume) haemodynamic range that this protocol itself expects, so the chosen lags may be an artefact of the range; (b) the alpha grid was sized for PCs, so C5 and C6 collapse to the mean predictor. A-2 is therefore not a valid test of the expected lag, and a further amendment (A-3) is needed before any test of it. A-3 is NOT made here; it requires owner approval, declared before its run. (Superseded by A-3 below, which the owner approved.)

- **A-3 (2026-10-27, written before any A-3 run; owner-approved).** This amendment corrects the design faults that A-2 exposed. It is the only specification used for any A-3 run. Its status is set out in the three steps below.
  1. **Lag range.** The sync lag L is searched over {0, 1, 2, 3, 4, 5} volumes (0 to about 3 s at 0.6 s per volume), because fUS is expected to lag speed. The search is restricted to these non-negative lags, with the sign declared before any run. The lag is chosen from the training sessions only, by maximum mean correlation across them. The aligned target is y_aligned[t] = speed[t − L].
  2. **Feature scaling and grid.** Each PC, each lagged global-signal feature and each motion feature is standardised by its training-session mean and standard deviation. Ridge alpha is searched over {1e-1, 1e0, 1e1, 1e2, 1e3, 1e4} on the standardised features. If the selected value is at an edge of this grid, the edge is reported, not extended.
  3. **Controls redefined.**
     - C5: the global mean of the z-scored voxels, lags 0 to 5, standardised, ridge with alpha from the same grid chosen on training sessions.
     - C6: a voxelwise DVARS-style motion proxy, namely the root-mean-square over voxels of the frame-to-frame difference of the z-scored voxel series, lags 0 to 5, standardised, ridge with alpha chosen on training sessions.
     - A control "matches" M1 in a held-out session if its r² is at least M1 r² − 0.01. This criterion is fixed here.
  4. **Decision rule.** Unchanged from the original protocol, applied to A-3 results.
  5. **Two-stage use of data, fixed in advance.**
     - Stage E (exploratory, one run only): A-3 on the original three sessions, with leave-one-session-out and the inner selection as above. The output is labelled EXPLORATORY. No setting is changed after this run.
     - Stage F (final, one run only): the two sessions not used before, ses-20210430 and ses-20210505 of sub-rat1703. Hyperparameters are selected from the original three sessions only, using the A-3 procedure, and then the model is evaluated once on each new session. The test sessions play no part in any choice.
  6. **Scope statement.** Stage E is exploratory and is not independent confirmation. Only Stage F is an independent test, and only if its code and hyperparameters were fixed before it was run.
  7. **Unchanged:** the three sessions of stage E, the z-scoring per session, the seeds (new seed 20261029 for A-3), and the no-holdout, no-push, no-email, no-paid-compute restrictions.

- **A-1 (2026-10-27, before any fit on raw data).** Correction of the Data section. The `mask-brain` weights volume was first described as a voxel mask; inspection showed it is the authors' decoder weights (values -4 to 7, 7678 of 14336 voxels non-zero). It is excluded. Voxel selection is replaced by finite values and non-zero temporal variance computed per session. No outcome, no split, no control, no decision rule is changed. The change is recorded here, not silently applied.
