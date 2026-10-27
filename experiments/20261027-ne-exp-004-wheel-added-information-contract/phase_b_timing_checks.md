# Phase B structural timing checks (development runs; read-only)

Eligible runs: 8. Excluded for count mismatch: 8 (sub-ALD002_task-awake_acq-ref02, sub-ALD002_task-awake_acq-ref10_run-1, sub-ALD002_task-awake_acq-ref12, sub-ALD002_task-awake_acq-ref14, sub-ALD002_task-awake_acq-ref20_run-1, sub-ALD002_task-awake_acq-ref23, sub-ALD002_task-awake_acq-ref24, sub-ALD002_task-awake_acq-ref27).
The holdout is excluded by name and is not read.

| run | date | VT len | VT first–last (s) | dt median / min / max (s) | endpoint discrepancy, gap excess removed (s) | gaps >0.45 s | physio fs / dur (s) | physio covers | aligned wheel frames |
|---|---|---|---|---|---|---|---|---|---|
| sub-ALD002_task-awake_acq-ref04 | 2023-03-21 | 11311 | 6.6–3404.8 | 0.30000 / 0.29900 / 3.90700 | +0.18 | 1 | 1000.0 / 3415.0 | True | 11307 |
| sub-ALD002_task-awake_acq-ref06_run-1 | 2023-03-28 | 11311 | 6.9–3401.3 | 0.30000 / 0.30000 / 0.39100 | -0.06 | 0 | 1000.0 / 3411.0 | True | 11309 |
| sub-ALD002_task-awake_acq-ref06_run-2 | 2023-03-30 | 11310 | 6.6–3400.9 | 0.30000 / 0.29900 / 0.45200 | -0.01 | 1 | 1000.0 / 3411.0 | True | 11310 |
| sub-ALD002_task-awake_acq-ref08 | 2023-03-21 | 11311 | 7.3–3401.6 | 0.30000 / 0.30000 / 0.38700 | -0.10 | 0 | 1000.0 / 3411.0 | True | 11311 |
| sub-ALD002_task-awake_acq-ref11 | 2023-03-20 | 11297 | 6.2–3399.0 | 0.30000 / 0.30000 / 0.92600 | +0.53 | 7 | 1000.0 / 3410.0 | True | 11294 |
| sub-ALD002_task-awake_acq-ref18 | 2023-03-15 | 11316 | 6.7–3402.6 | 0.30000 / 0.30000 / 0.38700 | -0.11 | 0 | 1000.0 / 3412.0 | True | 11314 |
| sub-ALD002_task-awake_acq-ref20_run-2 | 2023-03-23 | 11308 | 6.0–3399.7 | 0.30000 / 0.30000 / 0.45700 | -0.08 | 1 | 1000.0 / 3409.0 | True | 11304 |
| sub-ALD002_task-awake_acq-ref22 | 2023-03-15 | 8339 | 0.1–2502.5 | 0.30000 / 0.29900 / 0.38900 | -0.05 | 0 | 1000.0 / 2512.0 | True | 8339 |

C-V1 (VolumeTiming length equals frame count): enforced by read_primary_runs; 8 of 8 eligible.
C-V2 (endpoint discrepancy with the quoted period 0.30013 s, gap excess removed, tolerance 0.1 s, fixed before this statistic was computed): NOT PASSED. Range over runs -0.106 s to +0.526 s.
Correction record: an earlier version used the median onset interval and reported
a drift of −1.08 to −1.47 s. The median is not the mean period (onsets are quantised
to 1 ms and gaps skew the mean), so that statistic over-states the drift; withdrawn.
The corrected endpoint discrepancy is at least about 0.5 s in some runs (largest with
long gaps). The physio-fUS clock offset and the onset-versus-end convention are
unquantified; they are not measured by this check.
C-V3 (physio recording covers all onsets): 8 of 8 runs.

Not checked here: the VolumeTiming convention (onset relative to frame start or end) and
the clock alignment between physio and fUS. Both remain open; temporal interpretation is
not permitted until they are resolved.
