# GLOSSARY

- **Neural signal** — a measured physiological quantity (for example EEG voltage, fMRI BOLD, fUS blood volume) recorded from a person or animal. Its content is an empirical question.
- **Stimulus** — an externally presented input whose identity is controlled by the experimenter.
- **Internal representation** — a state inside the brain or a model that carries information about a stimulus, percept, memory, or intention. Its existence and level are hypotheses to be tested.
- **Reconstruction** — producing an output (image, text, vector) intended to approximate a target. Reconstruction quality does not by itself show that the signal carried the target.
- **Decoding** — predicting a target variable from signal. Accuracy measures predictive success, not mechanism.
- **Model prior** — information in a model's parameters or training data that is present in the output regardless of the input. A generative model can add content not contained in the signal.
- **Uncertainty** — quantified doubt about an estimate, reported with its method (for example interval, posterior, ensemble spread). An unqualified number is not uncertainty.
- **Leakage** — any path by which information about the test target reaches training or model selection (for example same subject across splits, same session, duplicated stimuli, temporal autocorrelation, artifacts correlated with labels).
- **Baseline** — a simple, pre-specified comparator (for example majority class, linear model, shuffled labels) that a complex method must beat.
- **Holdout** — data withheld from all training and model selection and used once, for the frozen protocol.
- **Out-of-distribution (OOD)** — inputs whose distribution differs from training data in a way that matters for the claim (new subject, session, stimulus set, or device).
- **Evidence-supported attribute** — a property of the output that is predicted from the signal above baseline and controls, with its control residual stated. Attributes that appear only through the model prior are not evidence-supported.
