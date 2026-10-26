# Data

No datasets are committed to this repository.

## Layout

- `data/raw/` — downloaded originals. Ignored by Git.
- `data/interim/` — intermediate files. Ignored by Git.
- `data/processed/` — derived files. Ignored by Git.

Only the following go into Git: manifests, URLs, licences, checksums, retrieval instructions.

## Provenance and checksums

Each adopted dataset gets an entry in its experiment `manifest.yaml`: name, version, source, licence, retrieval date, SHA-256 of each file used. Checksum computation and verification code is **not implemented yet**; it is added in Phase 1 when the first dataset is adopted.

## Adoption note

DVC is not adopted. Revisit when a dataset or artifact exists that is impractical to store in Git. Until then, do not add it.
