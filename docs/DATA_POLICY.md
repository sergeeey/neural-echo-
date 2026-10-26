# DATA POLICY — neural and human data

1. Never commit identifiable human data. Treat any neural recording from a person as potentially identifying.
2. `data/raw/`, `data/interim/`, `data/processed/` are ignored by Git. Only manifests, URLs, checksums, licences and retrieval instructions go into Git.
3. Every dataset record states: source, licence, retrieval date, version, and SHA-256 checksum of the files used.
4. Preserve provenance: do not overwrite raw files; derive processed files by code that is committed.
5. Do not imply consent beyond the dataset licence and its terms of use.
6. No experiments on humans are part of this repository unless separately reviewed and appropriately authorized (ethics approval and consent documentation recorded in an ADR before any such work).
7. Do not place credentials or access tokens for data portals in the repository.

## Checksums

Checksum computation and verification are not implemented yet. `scripts/validate_experiment.py` checks structure only and says so. Checksum tooling is added when the first dataset is adopted (Phase 1).
