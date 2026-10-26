# ROADMAP

Phases are ordered by gate, not by date. A phase is complete only when its gate passes. Later phases do not promise success.

## Phase 0 — repository and reproducibility foundation
Gate: fresh clone → documented command → green (lint, types, tests, repository validator). Scientific claims: none.

## Phase 1 — literature and dataset audit
Gate: at least one candidate dataset with source, licence, version and checksum recorded; literature entries carry verification states from `literature/README.md`.

## Phase 2 — reproduce one classical neural decoding baseline
Gate: a pre-registered experiment reproduces a published baseline within a stated tolerance, or records that it does not.

## Phase 3 — leakage and negative-control suite
Gate: shuffled-label, temporal permutation, subject, session, and stimulus leakage checks run on the Phase 2 pipeline, with results recorded even when negative.

## Phase 4 — uncertainty- and evidence-aware decoding
Gate: decoder outputs carry calibrated uncertainty and are reported against the signal-vs-prior decomposition in `docs/GLOSSARY.md`.

## Phase 5 — reconstruction experiments
Gate: reconstructions are labelled by evidence-supported vs model-prior content, with controls. Conditional on Phases 1–4 and on Q0.8.
