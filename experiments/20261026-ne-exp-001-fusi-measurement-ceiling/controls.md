# Controls

- **Block-permuted wheel control (required):** wheel velocity permuted in 10 s blocks within each run, repeated many times. Defines the null distribution for the primary gain.
- **Chance baseline:** predicting the training mean.
- **Wheel-free nuisance:** eye movement and pupil size only. Whisking is excluded because its sidecar defines it from wheel velocity.
- **Motion-independent reference (required for any neural reading, currently NOT AVAILABLE):** no verified signal is free of brain blood flow and body motion. A large-vessel signal is **not** a motion-free reference, because it carries real blood-flow changes. A registration-based motion regressor would be computed from the target images and is forbidden in this protocol. Options (each needs a decision before freezing): a motion estimate from the independent angiography scan, or a reference region validated against an external criterion.
- **Session-specificity check:** not used as an H0 test. A session-mismatched wheel pairing removes motion artefact and real coupling alike, so it cannot separate them.
- **Target-derivative check:** no regressor may be computed from the fUS target. Checked by code review before freezing.
- **Positive control:** none available in this dataset. Stated as a limitation.
