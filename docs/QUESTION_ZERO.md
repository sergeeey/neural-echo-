# QUESTION ZERO

Foundational questions that gate experimental design. Each is `UNKNOWN` until an experiment or cited evidence answers it. None is a claim.

- **Q0.1** What exactly is the target representation? (category, attribute, relation, visual embedding, pixels, intention)
- **Q0.2** What information is observable in the measurement at each representational level?
- **Q0.3** What information comes from the model prior?
- **Q0.4** What information comes from confounds (eye movement, breathing, heart rate, muscle activity, task timing, stimulus structure)?
- **Q0.5** Does the user adapt to the decoder? (fixed decoder vs adaptive decoder vs feedback vs no-feedback control)
- **Q0.6** Is there a shared representation across subjects, or does each subject need a separate model? Hypotheses: H1 shared latent space; H2 subject-specific geometry; H0 apparent transfer arises from task artifacts.
- **Q0.7** What is the information ceiling of each modality (EEG, fUS, fMRI)?
- **Q0.8** Is reconstruction the right objective, or is reliable communication of a latent intent (choice, category, attention direction) more achievable and useful?

## Reversal condition

If communication accuracy for high-level states is high while reconstruction fidelity is low, the project scope is revisited through an ADR before further reconstruction work.
