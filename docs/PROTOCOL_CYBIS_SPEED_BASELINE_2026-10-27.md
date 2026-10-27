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

- fUS: `rawdata/sub-rat1703/ses-<s>/fus/*_pwd.nii.gz` (power Doppler NIfTI). Brain mask: the `mask-brain` weights volume shipped in `derivatives/decode-speed/sub-rat1703/`, used only as a voxel mask.
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

None yet.
