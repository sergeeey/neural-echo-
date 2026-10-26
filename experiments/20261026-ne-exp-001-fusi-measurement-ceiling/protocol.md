# Protocol

## FROZEN PROTOCOL

> Status: PLANNED. Not frozen. Nothing below is fixed until this section is reviewed, the data download is approved, and the status is set to FROZEN in manifest.yaml.

## Dataset

- Name and version: Functional Ultrasound Imaging (fUSI) data from head-fixed, freely running mice (DOI 10.5522/04/31376338), version as downloaded.
- Source, licence, retrieval date: UCL RDR; CC BY-NC 4.0; not yet retrieved.
- Per-file SHA-256 checksums: to be recorded at download time (manifest.yaml `dataset.files`).

## Split strategy

- Unit of splitting: session (and subject). Held-out sessions are never used for fitting or model selection.
- Train / validation / holdout: to be set once the session list is read. Holdout used once.

## Leakage controls

- Session leakage: no session appears in both training and test.
- Subject leakage: reported separately; a leave-one-subject-out run is added if at least 3 subjects qualify.
- Motion control: only if a motion regressor or motion-correction output is found in the files. Otherwise this control is marked NOT AVAILABLE in the decision, not assumed.
- Temporal permutation: circular shift of the wheel label within each session.

## Baselines

- Nuisance-only: whisking and eye regressors (plus motion if available, see Leakage controls), same model class.
- Chance: majority class per session.
- Shuffled-label control: wheel labels permuted within session.

## Metrics

- Primary: held-out log loss difference (nuisance-only minus full), with a session-cluster bootstrap 95% interval. Positive means the fUSI model helps.
- Secondary: balanced accuracy, Brier score. Reported, not used to decide the claim.

## Model and run parameters

- Model class: to be fixed before data is read. Candidate: regularised logistic regression on time-lagged features. Hyperparameters fixed in advance, not tuned on held-out data.
- Random seeds: to be recorded.
- Software environment: uv.lock of this repository (hash recorded in manifest.yaml).
- Success and falsification criteria: as in claim.md.

## Amendments

None.
