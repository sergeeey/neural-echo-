# Decision

Not yet. Status PLANNED. No evaluation has been run. The audits read sidecars, the scans table, angiography and NIfTI headers, and summary statistics. The autocorrelation audit read the whole-slice signal of the 16 development runs only. The holdout was not read.

**Classification:** EXPLORATORY. With 5 mice the exact sign test cannot reach two-sided p below 0.0625, so no alpha-0.05 claim is possible at mouse level. Power 0.8 is not claimed.

**MCID:** not set, and cannot be justified now. No effect-size anchor exists (article full text not read; no downstream decision threshold defined). It must not be chosen after results.

## Freeze readiness table

| # | Blocker | How checked | Confirmed source(s) | Actual status | Remaining risk |
|---|---|---|---|---|---|
| 1 | Motion-independent reference or motion signal | Archive listing; angiography header and sidecar | Listing: no motion or reference file. Angiography: static 3D volume, 60×125×36, voxels 0.0907×0.0488×0.4 mm, no time axis, no plane coordinates; fUS voxels 0.1×0.0483×0.4 mm | **OPEN.** Angiography cannot give per-frame motion. A mask from it would need registration, which is unverified | Body motion and locomotion-linked blood flow are not separated. Claim stays predictive |
| 2 | Motion-derived diagnostics | Whisking sidecar text | Whisking "estimated from motion SVD and wheel velocity" | Usable only as a sensitivity analysis, explicitly dependent on the fUS signal | Circular if used as a control |
| 3 | `VolumeTiming` convention | ConfUSIus source (`validation.py`: "onset time of each volume"; `timing.py`: default reference start) | Third-party implementation, not the official fUSI-BIDS text (not verified) | **Partly verified:** onset reference. Window length 0.3 s from sidecar | Lag-0 interpretation depends on the official text |
| 4 | Physio–fUS clock alignment | BIDS physio spec fetched | The spec text fetched does not define the zero of `StartTime` | **OPEN.** UNVERIFIED | Lags are not clock-aligned until resolved |
| 5 | VolumeTiming vs NIfTI volume count | Per-run comparison, development runs | 8 of 16 development runs have one more onset than volumes (e.g. ref02: 11308 vs 11307) | **OPEN.** Mapping rule must be fixed on development data | One frame offset would misalign every lag |
| 6 | Autocorrelation and block length | Integrated τ on 16 development runs | τ median 49 frames (≈15 s), max 76 (≈23 s); lag-20 ACF 0.33–0.54 | **Done:** blocks 120 s, buffer 60 s (fixed, development only) | Estimates from one mouse |
| 7 | Holdout identity and grouping | scans.tsv | 17 runs, 9 dates, 17 (date, experiment_id) pairs. Holdout `ref10_run-2`, latest date, tie broken by experiment_id | **Done.** Named and asserted | experiment_id meaning UNVERIFIED (may be a plane or block) |
| 8 | Data access and sources | ConfUSIus repository tree; Landemard DOI, DataCite, figshare | Only sub-ALD002 downloaded (5.27 GB, checksums match). No further download | **Done.** No further data needed for this audit | Other subjects not examined |
| 9 | Primary metric and sign | Protocol text | Held-out Gaussian log loss; Δ = L_nuisance − L_full, positive = fUS better | **Done** in protocol; consistent with the owner's request | Gaussian assumption not checked |
| 10 | MCID | Literature not read; no decision threshold | None | **Not set.** Cannot be justified now | Null results uninformative until MCID set |
| 11 | Statistical power at n=5 mice | Exact sign test bound | Minimum two-sided p = 0.0625 | **Confirmed.** Exploratory only | Power 0.8 not claimed |
| 12 | Target-derivative leakage | Protocol text | No regressor from the fUS target; no registration motion regressors | **Done in text.** Code check still needed | Code not yet written |
| 13 | Freeze status | manifest and protocol heading | Heading "FROZEN PROTOCOL" is present, but status PLANNED | **Not frozen.** Heading is not a freeze | Must not be read as frozen |

## Verdict

**BLOCKED.** Blockers 1, 3 (official text), 4 and 5 are open and need data-level checks or an owner decision. Blocker 10 needs an owner decision. Blocker 6 and 7 are resolved.

## Parameters that affect the final test (all fixed before holdout is read)

Holdout identity; development set; date grouping; resampling rule and 99% coverage; VolumeTiming mapping (open, blocker 5); lag set 0 to 6 s; ridge alpha 1.0; standardisation on training only; Gaussian predictive model; block length 120 s; buffer 60 s; null count (to be set); exclusion rules. Undefined until frozen: VolumeTiming mapping, physio alignment rule.

## What would change our model of the problem

A gain in held-out log loss above the block-permutation null, stable across dates, would show wheel velocity carries predictive information for this whole-slice signal. It would still not show a neural origin until a motion-independent reference is verified.
