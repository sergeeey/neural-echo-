# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. Not frozen. Nothing below is fixed until this section is reviewed, the data download is approved, and the status is set to FROZEN in manifest.yaml.

## Dataset

- Name and version: Functional Ultrasound Imaging (fUSI) data from head-fixed, freely running mice (DOI 10.5522/04/31376338), version as downloaded.
- Source, licence, retrieval date: UCL RDR; CC BY-NC 4.0; not yet retrieved.
- Per-file SHA-256 checksums: to be recorded at download time (manifest.yaml `dataset.files`).

## Split strategy

- Unit of splitting: session (and subject). Held-out sessions are never used for fitting or model selection.
- Generalisation unit: mouse. The claim about generalisation uses leave-one-mouse-out. Session-held-out results support only within-mouse stability.
- Paired design: both models are fitted and scored on the identical sessions and time points. Sessions lacking whisking or eye channels are excluded from both.
- Train / validation / holdout: to be set once the session list is read. Holdout used once.

## Leakage controls

- Session leakage: no session appears in both training and test.
- Subject leakage: the interval is resampled by mouse. Leave-one-mouse-out is the primary generalisation check, not an optional add-on.
- Motion-independent control (required; needs no motion file): the same model on the fUSI signal from a reference region outside the brain or from a large vessel. If that reference predicts wheel activity about as well as the brain signal, H0 (motion artefact) is not excluded.
- Motion regressor: used only if the files contain one. Its absence is recorded in the decision, not assumed away.
- Lag windows: set from the haemodynamic delay in the data before freezing. Not set in this draft.
- Temporal permutation: circular shift of the wheel label within each session.

## Baselines

- Nuisance-only: whisking and eye regressors (plus motion if available, see Leakage controls), same model class.
- Chance: majority class per session.
- Shuffled-label control: wheel labels permuted within session.

## Metrics

- Primary: held-out log loss difference (nuisance-only minus full), with a mouse-cluster bootstrap 95% interval. Positive means the fUSI model helps.
- Detectability: n = 5 mice; baseline or sigma UNKNOWN until data; alpha 0.05 two-sided; power 0.8; MDE UNKNOWN; MCID NOT SET (owner decision).
- Secondary: balanced accuracy, Brier score. Reported, not used to decide the claim.

## Model and run parameters

- Model class: to be fixed before data is read. Candidate: regularised logistic regression on time-lagged features. Hyperparameters fixed in advance, not tuned on held-out data.
- Random seeds: to be recorded.
- Software environment: uv.lock of this repository (hash recorded in manifest.yaml).
- Success and falsification criteria: as in claim.md.

## Amendments

None.
