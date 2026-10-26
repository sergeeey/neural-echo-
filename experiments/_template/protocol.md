# Protocol

## FROZEN PROTOCOL

> Everything in this file is fixed when `status` in `manifest.yaml` becomes `FROZEN`, before any run. Fill every section below first, then freeze. Changes after freezing require a dated entry under "Amendments".

## Dataset

- Name and version:
- Source, licence, retrieval date:
- Per-file SHA-256 checksums (see `manifest.yaml` `dataset.files`):

## Split strategy

- Unit of splitting (subject / session / trial / stimulus):
- Train / validation / holdout definition:
- Holdout used once: yes / no

## Leakage controls

- Subject leakage check:
- Session leakage check:
- Stimulus leakage check:
- Temporal permutation control:

## Baselines

- Simple linear baseline:
- Majority-class / chance baseline:
- Shuffled-label control:

## Metrics

- Primary metric and its uncertainty method:
- Secondary metrics:

## Model and run parameters

- Model and hyperparameters:
- Random seeds:
- Software environment (lock file hash):
- Success criterion (copied from claim.md):
- Falsification criterion (copied from claim.md):

## Amendments

None.
