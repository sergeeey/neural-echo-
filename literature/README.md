# Literature provenance

`sources.yaml` holds only entries whose metadata has been checked against a primary source. It is empty on purpose: no citation may be written from memory.

## Fields

- `id` — stable slug
- `title`, `authors`, `year`
- `doi`, `url` — as checked
- `source_type` — paper | preprint | dataset | book | report | code
- `accessed_at` — date the source was checked (YYYY-MM-DD)
- `verification_status` — one of:
  - `UNVERIFIED` — listed, not checked
  - `METADATA_VERIFIED` — title, authors, year, DOI confirmed against the publisher or a database record
  - `PRIMARY_SOURCE_READ` — the full text was read
  - `REPRODUCED` — a reported result was reproduced in this repository, linked to an experiment
- `supports` / `contradicts` — claim IDs from `docs/`
- `notes`

## Rules

- Reading a PDF does not make a paper `REPRODUCED`.
- Do not fill metadata from model memory. Use a database or the publisher page.
