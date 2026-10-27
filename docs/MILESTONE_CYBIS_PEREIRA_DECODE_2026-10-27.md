# Milestone evidence: speed decoding, Cybis Pereira et al. (Zenodo 15476373)

Status labels: VERIFIED (reproduced by a script in this repository this session), SOURCE (stated by the cited page), UNKNOWN.

## Dataset qualification

| Item | Status | Evidence |
|---|---|---|
| Licence | VERIFIED: CC BY 4.0 | Zenodo API `license.id` = `cc-by-4.0`; record 10.5281/zenodo.15476373 |
| Source of raw data | VERIFIED | Zenodo `dataset.zip`, 11,653,544,308 bytes, md5 `43ce010b4557bc495829c6ef7edb68a1` (Zenodo metadata) |
| Full archive downloaded | NO | The archive was not downloaded in full (about 5 hours at the observed rate). Only the authors' decoding outputs were fetched, via HTTP Range requests into the archive |
| Decoding outputs fetched | VERIFIED | 104 files (`decode-speed`, `interanimal-decode-speed`; TSV, JSON, NIfTI). `.joblib` deliberately skipped (pickle, not loaded). Manifest: `data/raw/cybis_pereira_2026/MANIFEST.sha256.tsv` (git-ignored), SHA-256 of manifest `59963c0ccb82a77b676f9483a0d73cbb6b7eebf6957ec307cf28d62d172254f8` |
| Per-file integrity | VERIFIED | zipfile CRC-32 checked on every extracted member; SHA-256 recorded per file |
| Published method | SOURCE (preprint v1, bioRxiv 10.1101/2025.07.15.663536) | PCA followed by ridge regression; intra-animal leave-one-session-out; inter-animal decoder trained on one animal, validated on four. Quoted maxima: intra r² up to 0.6, inter r² up to 0.36. Hyperparameters, chance construction and lag window not reported in the text |
| Published version | UNKNOWN | The Cell Reports version (DOI 10.1016/j.celrep.2025.116791) was not accessible; the preprint may differ |
| Raw-data baseline reproduction | NOT RUN | Refitting from raw fUS needs the raw NIfTI and the GLM convolution; not in this milestone. It is the next step, see below |

## Output-level reproduction (`scripts/check_cybis_pereira_decode.py`)

The script takes the authors' own `predicted` and `actual` test columns, computes r² = 1 − SS_res/SS_tot, and compares with the quoted maxima.

| Set | Model | Files | Max r² | Median r² | Quoted max |
|---|---|---|---|---|---|
| intra | regressor | 12 | 0.6023 | 0.3912 | 0.6 |
| intra | dummy | 12 | 0.1060 | 0.0721 | not quoted |
| inter | regressor | 4 | 0.3535 | 0.2745 | 0.36 |
| inter | dummy | 4 (0 independent; see Duplicates) | 0.0895 | 0.0398 | not quoted |

Per-file r² of three files was recomputed by a standalone script that does not import the repository module (`sub-rat1703` regressor 0.3946, `sub-rat75` dummy 0.0884, `sub-rat83` dummy 0.0437). All three match the script to four decimals.

Reading:
- The intra-animal maximum is consistent with the quoted 0.6 at its stated precision (0.602 against 0.6).
- The inter-animal maximum is 0.354 against 0.36. Not exact; the quoted figure may come from a different version or set. Not resolved.
- Regressor against dummy, paired per animal and test length, with a circular-block bootstrap of the r² difference (block = 200 frames, 1000 draws): the 95% interval excludes zero in 11 of 12 intra-animal pairs (the exception is sub-rat73, n = 2780, interval −0.073 to +0.348) and in 4 of 4 inter-animal pairs. Mean intra difference 0.15 to 0.52.
- Power and minimum detectable effect are not computed. Stated design: n = test frames per file (2224 to 6417); alpha = 0.05 two-sided; power and MDE undetermined; MCID not defined.

## Duplicates

Four inter-animal dummy rows have the same animal, n and r² to four decimals as an intra-animal dummy row (sub-rat2306, sub-rat73, sub-rat83 × 2). Their files are byte-different (SHA-256 in the manifest), so the cause is UNKNOWN. They are flagged and excluded from the aggregates. Inter-animal dummy is therefore 0 independent files, and the inter-animal dummy row above is not evidence.

## Negative controls

Permutation of predictions was tried first and rejected: speed series are strongly autocorrelated, so a permuted prediction loses temporal structure and gives an optimistic null. The script uses circular time-shifts of the prediction (1000 draws, shifts ≥ 200 frames), reporting null mean, null sd, z and p.

- The shift null is centred below zero (null means −0.08 to −0.91). A circular shift breaks the alignment and gives negative r², so shift p answers "is the observed r² above a misaligned reference", not "is it above chance". It is reported but is not the main test.
- Regressor files: z between 6.1 and 17.4; shift p = 0.001 in all 12 intra and 4 inter files.
- Dummy files: z between 0.9 and 5.6; shift p = 0.001 in 11 of 12 intra files; the exception (sub-rat83, n = 2224, r² −0.044) has z = 0.91 and p = 0.258.
- The paired difference above is the stronger comparison. The dummy model is not a zero baseline (median r² 0.07), so "regressor beats dummy" does not mean "regressor beats chance".
- Neither control shows that the decoder is free of leakage.

## What this does not establish

- No leakage test on the authors' pipeline: session identity is not stored in the output TSVs, so leave-one-session-out cannot be checked from them. UNKNOWN.
- No refit from raw fUS data. The reproduction is of reported outputs, not of the fitting procedure.
- The inter-animal output files cover three animals (sub-rat2306, sub-rat73, sub-rat83; 4 files). The validation set in the preprint text is four animals; the mismatch is not explained by the files. UNKNOWN.
- No claim about mechanism. Speed decoding from CBV is a predictive association (EstimandOps L0: Predictive). It is not causal.
- Not established: that the preprint v1 numbers match the published version.

## Next step (not run)

1. Obtain the Cell Reports version and check its decoder and metric description against the preprint.
2. Refit the PCA + ridge pipeline from raw fUS for one animal (sub-rat1703), with session-level leave-one-out, using the GLM lag convolution as described. This needs the raw NIfTI from `rawdata/sub-rat1703` (361 MB) and the GLM outputs from `derivatives/glm-speed`. Needs a stated budget.
3. Negative control on the refit: shuffled speed labels within session, and shuffled-session controls.
