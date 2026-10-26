# Controls

- **Negative controls:** shuffled wheel labels within session; circular label shift; chance baseline.
- **Motion-independent control (addresses H0, required):** the same model on a reference-region fUSI signal (outside the brain or a large vessel). Positive only if the brain signal beats the reference.
- **Session-mismatched control (required):** fUSI features from a different session of the same mouse, paired with the target session's wheel labels. Same feature count as the real model.
- **Leakage checks:** session-disjoint splits; motion control if a motion signal exists (else NOT AVAILABLE); subject-level report.
- **Simple baseline result:** pending (nuisance-only model).
- **Sensitivity analyses:** motion correction on and off; two lag windows.
- **Known confounds:** whisking, eye and wheel movement may co-vary with blood volume. The nuisance model tests whether the wheel signal adds anything beyond whisking and eye. Wheel is the target here, so it is not a regressor.
- **Positive control:** none available in this dataset. Stated as a limitation.
