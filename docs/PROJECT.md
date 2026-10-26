# PROJECT

## Purpose

Determine which information about internal human states is recoverable from measurable neural signals, under explicit controls, and make the boundary between signal-supported content and model-introduced content visible.

## Central research question

What information about internal human states is recoverable from measurable neural signals, and how can we distinguish signal-supported reconstruction from information introduced by a model prior?

This is a research question, not an established result.

## Derived questions

- At which representational level (category, attribute, relation, visual embedding, pixels) does information survive the measurement? (see `QUESTION_ZERO.md` Q0.1–Q0.2)
- How much apparent performance comes from the signal, the model prior, confounds, and user adaptation? (Q0.3–Q0.5)
- Is reconstruction the right objective, or is reliable communication of latent intent more achievable? (Q0.8)

## Scope

- Offline analysis of existing, lawfully obtained, de-identified datasets.
- Classical baselines before deep models.
- Negative controls and leakage tests as first-class work.

## Non-goals

- Building a product or interface.
- Claiming thought reading or mind reading.
- Running experiments on humans.
- Large-scale model training before a baseline and controls exist.

## Terminology

See `docs/GLOSSARY.md`. In particular: decoding, reconstruction, and classification are different claims and must not be substituted for one another.

## Scientific boundaries

- A decoder's success does not by itself establish that the signal carries the target representation (representation validity).
- A reconstruction's visual quality does not establish fidelity to the signal.
- Results are bounded by the dataset, the measurement modality, and the controls actually run.
