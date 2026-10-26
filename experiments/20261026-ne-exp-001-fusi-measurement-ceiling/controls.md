# Controls

- **Negative controls:** wheel velocity permuted in 10 s blocks (pipeline check); chance baseline (run mean).
- **Session-mismatched control (required):** fUS features from another run, paired with the target run's wheel velocity. Same feature count as the real model. The gain must vanish.
- **Reference-region control (required, not yet possible):** the same model on a signal from outside the brain or from a large vessel. No such signal is verified in the archive. Until one is verified, this control is NOT AVAILABLE, and H0 is not excluded.
- **Wheel-free nuisance:** eye movement and pupil size. Both are computed from eye camera data, not from wheel velocity.
- **Whisking sensitivity:** whisking is reported as a sensitivity analysis only. Its definition includes wheel velocity, so it is not an independent control.
- **Target-derivative check:** no regressor may be computed from the fUS target. Checked by code review before freezing.
- **Known confounds:** wheel movement moves the body, eye and whiskers. The eye-and-pupil nuisance set does not remove all of it. Motion control is the open problem.
- **Positive control:** none available in this dataset. Stated as a limitation.
