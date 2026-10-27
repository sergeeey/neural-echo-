# CRT pilot comparison: v1 configuration vs v2 (NE-EXP-002, synthetic only)

v1-config code_version: `04267d6` flags {'standardise': False, 'edge_frames': 20}  
v2 code_version: `04267d6` flags {'standardise': True, 'edge_frames': 40}  
reps per scenario: 30, draws per replicate: 99, alpha 0.05, same seed 20261027 (paired synthetic series)

## Rejection rates (conditional test, and the independent comparator)

| scenario | kind | v1-config k/n | v1 Wilson95 | v2 k/n | v2 Wilson95 | paired b (v1 only) | paired c (v2 only) |
|---|---|---|---|---|---|---|---|
| zero_effect | independent | 1/30 | [0.006, 0.167] | 1/30 | [0.006, 0.167] | 0 | 0 |
| zero_effect | conditional | 2/30 | [0.018, 0.213] | 3/30 | [0.035, 0.256] | 0 | 1 |
| ar_null_strong | independent | 1/30 | [0.006, 0.167] | 1/30 | [0.006, 0.167] | 0 | 0 |
| ar_null_strong | conditional | 0/30 | [0.000, 0.114] | 1/30 | [0.006, 0.167] | 0 | 1 |
| hidden_arousal | independent | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |
| hidden_arousal | conditional | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |
| measured_arousal | independent | 3/30 | [0.035, 0.256] | 2/30 | [0.018, 0.213] | 1 | 0 |
| measured_arousal | conditional | 0/30 | [0.000, 0.114] | 0/30 | [0.000, 0.114] | 0 | 0 |
| lead_misalignment | independent | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |
| lead_misalignment | conditional | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |
| known_added_info | independent | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |
| known_added_info | conditional | 30/30 | [0.886, 1.000] | 30/30 | [0.886, 1.000] | 0 | 0 |

Paired differences in rejection rate (v2 minus v1-config) equal (c - b) / n.

## Mean p-value and mean 95% null quantile

| scenario | kind | v1 mean p | v2 mean p | v1 mean q95 null | v2 mean q95 null |
|---|---|---|---|---|---|
| zero_effect | independent | 0.560 | 0.558 | 0.000154 | 0.000161 |
| zero_effect | conditional | 0.553 | 0.539 | 0.000172 | 0.000169 |
| ar_null_strong | independent | 0.596 | 0.597 | 0.000437 | 0.000437 |
| ar_null_strong | conditional | 0.612 | 0.603 | 0.000474 | 0.000473 |
| hidden_arousal | independent | 0.010 | 0.010 | -0.009711 | -0.009752 |
| hidden_arousal | conditional | 0.010 | 0.010 | -0.010130 | -0.010898 |
| measured_arousal | independent | 0.385 | 0.390 | 0.000133 | 0.000137 |
| measured_arousal | conditional | 0.588 | 0.587 | 0.000177 | 0.000185 |
| lead_misalignment | independent | 0.010 | 0.010 | -0.013214 | -0.013225 |
| lead_misalignment | conditional | 0.010 | 0.010 | -0.014324 | -0.015367 |
| known_added_info | independent | 0.010 | 0.010 | -0.015714 | -0.015789 |
| known_added_info | conditional | 0.010 | 0.010 | -0.016347 | -0.017788 |

## Pre-registered decision

- Null inflation flags: none
- Power (known_added_info): v1 1.0, v2 1.0, retained: True
- Diagnostics failing: ['quarter variance ratio after standardisation median 2.502 > 1.5', 'block variance ratio (max/min across blocks) median 62857.702 > 3']

**Verdict: REVISE.** no null flag, but diagnostics fail: quarter variance ratio after standardisation median 2.502 > 1.5; block variance ratio (max/min across blocks) median 62857.702 > 3.

Caveats: n = 30 replicates per scenario; Wilson intervals are wide; the diagnostics use a pooled OLS mu (diagnostic only); the conditional test is approximate, not an exact CRT.
