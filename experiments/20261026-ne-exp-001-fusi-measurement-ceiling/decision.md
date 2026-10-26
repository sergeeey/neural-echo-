# Decision

Not yet. Status PLANNED. No evaluation has been run. Audits used sidecars, the scans table, angiography and NIfTI headers, summary statistics, and the whole-slice signal of the 16 development runs. The holdout was not read.

**Classification:** EXPLORATORY. Reason: no independent motion-free reference is verified, and a replication across the 5 animals cannot reach alpha 0.05 (exact sign test minimum 0.0625). Power 0.8 is not claimed.

**MCID:** not set; cannot be justified now (no effect-size anchor; article full text not read; no decision threshold). Not to be chosen after results.

## Freeze readiness table

| # | Blocker | How checked | Confirmed source(s) | Actual status | Remaining risk |
|---|---|---|---|---|---|
| 1 | Motion-independent reference or motion signal | Archive listing; angiography header and sidecar | No motion or reference file in the archive. Angiography is static, 60×125×36, no time axis, voxels differ from fUS | **OPEN.** Blocks any neural reading; claim stays predictive | Body motion and locomotion-linked blood flow not separated |
| 2 | Motion-derived metrics | Whisking sidecar | Whisking is "estimated from motion SVD and wheel velocity" | Sensitivity only, explicitly circular with wheel | Cannot serve as a control |
| 3 | `VolumeTiming` convention | ConfUSIus source: "onset time of each volume"; default reference start | Third-party code; official fUSI-BIDS text not verified | **Partly verified** (onset reference). Official text OPEN | Lag-0 interpretation |
| 4 | Physio–fUS clock alignment | BIDS physio text fetched | Zero of `StartTime` not defined in the fetched text | **OPEN.** Declared as an assumption with shift sensitivity (±1, ±2 s) | Lag timing uncertain by up to 2 s |
| 5 | VolumeTiming vs NIfTI volumes | Per-run comparison, development runs (holdout also checked for its own match) | 8 of 16 development runs: one extra onset. ref02: 11308 vs 11307; ref27: 11319 vs 11318. ref22 and ref06_run-2 match | **Declared** mapping (first t onsets) with alternative as sensitivity. Official convention still OPEN | One-frame misalignment if wrong |
| 6 | Autocorrelation and blocks | Integrated tau on 16 development runs | Median 49 frames (≈15 s), max 76 (≈23 s). ACF at lag 20: 0.33–0.54 | **Done:** 120 s blocks, 60 s buffers | Estimates from one mouse; buffer definition now stated for folds and permutations |
| 7 | Holdout identity and scoring | scans.tsv; protocol text | `ref10_run-2` by rule; fixed one-shot scoring, 1000 permutations, seed 20261026 | **Done in text** | Null on one held-out run is weak |
| 8 | Data access | Archive listing; ConfUSIus tree; Landemard DOI / DataCite / figshare | Only sub-ALD002 downloaded (5.27 GB, checksums match) | **Done.** No further download | Other subjects not examined |
| 9 | Primary metric and sign | Protocol text | Gaussian log loss; Δ = L_nuisance − L_full; positive = wheel helps; variance from training residuals | **Done in text** | Gaussian assumption not checked |
| 10 | MCID | No literature full text; no decision threshold | None | **Not set** | Null results uninformative |
| 11 | Statistical power at n=5 | Exact sign test | Minimum two-sided p = 0.0625 (replication only) | **Confirmed**, applied to replication, not to the 1-mouse primary analysis | Power 0.8 not claimed |
| 12 | Target-derivative leakage | Protocol text | No regressor from target; no registration motion | **Done in text.** Code check still to be written before freezing | Implementation risk |
| 13 | Freeze status | manifest.yaml; protocol heading | Heading present; status PLANNED; git_commit, lock hash and seeds empty | **Not frozen** | Must not be read as frozen |
| 14 | Edge frames | ref22 onset 0.056 s; wheel starts 0 s | First 20 frames dropped in all runs | **Done in text** | Shorter effective runs |
| 15 | Clutter filter support | ClutterFilterWindowDuration 0.6 s vs frame 0.3 s | Frame window may understate temporal support | **Noted.** Affects interpretation of lag 0 | Temporal smearing |
| 16 | Positive control (synthetic wheel-coupled signal in development data) | Not yet run | — | **OPEN.** Cheap; needed to show the null can detect a planted effect | Null may be unable to detect anything |

## Verdict

**BLOCKED.** Open: items 1, 3 (official text), 4 (declared, not verified), 5 (declared, convention unverified), 10 (owner decision), 13 (not frozen), 16 (positive control, not yet run).

The text rules (7, 9, 12, 14) are now fixed. Items 4 and 5 can become declared assumptions with sensitivity analyses; that would make READY_AS_EXPLORATORY reachable for a predictive claim, provided item 16 is run first.

## Parameters that affect the final test (all fixed in protocol.md before holdout is read)

Holdout identity; development set; date grouping and 7-of-9 criterion; per-run preparation (linear mean target, detrend, edge-frame drop, 99% coverage); VolumeTiming mapping rule; clock-shift assumption (0 primary); lag grid 0–6 s, wheel only; ridge alpha 1.0; training-only standardisation; residual variance per model; permutation count 1000, seed 20261026; block 120 s; buffer 60 s.

## What would change our model of the problem

A gain above the block-permutation null, stable across dates, would suggest wheel velocity carries predictive information for this whole-slice signal, pending clock alignment. It would not show a neural origin until a motion-independent reference is verified.
