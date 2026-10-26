# Controls

- **Negative controls:** shuffled wheel labels within session; circular label shift; chance baseline.
- **Leakage checks:** session-disjoint splits; motion control if a motion signal exists (else NOT AVAILABLE); subject-level report.
- **Simple baseline result:** pending (nuisance-only model).
- **Sensitivity analyses:** motion correction on and off; two lag windows.
- **Known confounds:** whisking, eye and wheel movement may co-vary with blood volume. The nuisance model tests whether the wheel signal adds anything beyond whisking and eye. Wheel is the target here, so it is not a regressor.
- **Positive control:** none available in this dataset. Stated as a limitation.
