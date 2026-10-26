# Controls

- **Block-permuted wheel control (required):** signed wheel velocity permuted in **120 s blocks** within each run, with 60 s buffers, repeated many times. Defines the null distribution of Δ. Block length from the development autocorrelation audit (protocol.md).
- **Chance baseline:** predicting the training mean.
- **Wheel-free nuisance:** eye movement and pupil size only. Whisking excluded (its sidecar defines it from wheel velocity).
- **Motion-independent reference (required for any neural reading; currently NOT AVAILABLE):** no verified signal is free of brain blood flow and body motion. A large-vessel signal is not a motion-free reference. A registration motion regressor would use the target images and is forbidden. The static angiogram cannot give per-frame motion; a mask from it needs an unverified registration.
- **Session-specificity check:** not used as an H0 test (it does not separate motion from coupling).
- **Target-derivative check:** no regressor may be computed from the fUS target. Code review before freezing.
- **Positive control:** none available in this dataset.
