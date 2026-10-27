# Timing evidence ledger (NE-EXP-004 Phase B, C-V2 qualification)

Read-only evidence. No fUS values used. Status: VERIFIED (read from the archive or the page by a tool in this session), FROM SOURCE (documented by the cited source), HYPOTHESIS (not confirmed), UNKNOWN.

## 1. Timing sources per development run

| Item | Source | Value | Status |
|---|---|---|---|
| VolumeTiming length | `sub-ALD002/fusi/<run>_pwd.json` | equals NIfTI frame count for 8 runs | VERIFIED |
| VolumeTiming first onset | same | 0.1–7.3 s (not zero; ref22 starts at 0.1 s, others at 6–7 s) | VERIFIED |
| Onset interval median | same | 0.300 s (1 ms quantisation) | VERIFIED |
| Onset interval mean (non-gap) | same | 0.300121–0.300177 s per run | VERIFIED |
| Onset interval SD (non-gap) | same | 3.2–4.2 ms | VERIFIED |
| FrameAcquisitionDuration | `_pwd.json` | 0.3 s | VERIFIED (sidecar) |
| PowerDopplerIntegrationDuration | `_pwd.json` | 0.3 s | VERIFIED (sidecar) |
| RepetitionTime / frame period field | `_pwd.json` | no such field found | VERIFIED (absent) |
| NIfTI pixdim[4] | `_pwd.nii.gz` header | 0.1 (not a frame period) | VERIFIED; meaning UNKNOWN |
| Quoted frame period 0.30013 s | `docs/STATUS.md` line on frame period | no sidecar field carries it | UNKNOWN provenance |
| Wheel channel | `_recording-wheel_physio.json` | `wheel_velocity`, cm/s, "from rotary encoder", SamplingFrequency 1000 Hz, StartTime 0.0 | VERIFIED |
| Encoder resolution, derivation, time reference | none in archive | not stated | UNKNOWN |
| VolumeTiming convention (onset at frame start or end, zero reference) | fUSI-BIDS specification | not retrieved; generic BIDS tools use different conventions | UNKNOWN |
| Clock relation physio to fUS | none in archive | not stated | UNKNOWN |

## 2. Lattice analysis (`timing_lattice.json`, `scripts/check_timing_lattice.py`)

Per-run period taken as the mean of non-gap intervals (intervals ≤ 0.45 s). A gap is an interval above 0.45 s.

This table tests the period-based model, which sections 3 (H1, H7) supersede. The per-run periods are descriptive only.

| Run | Gaps (s) | Per-run period | Gap residual to nearest integer multiple of period (s) |
|---|---|---|---|
| ref04 | 3.907 | 0.300146 | 0.005 (13 periods) |
| ref06-1 | none | 0.300125 | — |
| ref06-2 | 0.452 | 0.300129 | 0.148 (1.5 periods: not a lattice value) |
| ref08 | none | 0.300121 | — |
| ref11 | 0.453, 0.494, 0.61, 0.926, … | 0.300177 | 0.147 belongs to the 0.453 s gap (1.5 periods); 0.494 s gives 0.106 (1.65 periods); 0.61 ≈ 2 periods; 0.926 ≈ 3.09 periods (residual ≈ 0.026) |
| ref18 | none | 0.300121 | — |
| ref20-2 | 0.457 | 0.300123 | 0.143 (1.5 periods: not a lattice value) |
| ref22 | none | 0.300123 | — |

With a single period of 0.3 s the endpoint span exceeds the lattice prediction by +1.0 to +1.7 s in every run. That excess is the summed delay (section 3, H1 and H7); a lattice that ignores delays cannot explain it, so the period-based reading of this table is retired.
With a single period of 0.30013 s the endpoint residual is (per-run mean − 0.30013) × (number of intervals), i.e. −0.23 to +0.19 s, and it depends on the per-run mean. The global 0.30013 is not a per-run value.

## 3. Explanations tested

| Hypothesis | Test | Result | Status |
|---|---|---|---|
| H1: the 0.3 s tick is the true onset grid, with one-sided delays added | endpoint span against the 0.3 s grid; delay distribution | +1.0 to +1.7 s endpoint excess in all runs is the summed delay (an identity, not evidence by itself); 99.77–99.85% of non-gap intervals sit at 0.300 s; four intervals at 0.299 s across three runs | SUPPORTED (inferred from the delay distribution; `timing_stalls.json`) |
| H2: single global period 0.30013 s | endpoint residual per run | residual tracks each run's own mean period (0.300121–0.300177); a global value is not exact | REJECTED as an exact global period |
| H3: per-run clock-rate difference | per-run means differ by up to 5.6e-5 s/frame | the per-run means reflect the number of delays per run, not the clock rate; the earlier "clock-rate" reading is withdrawn | WITHDRAWN (replaced by H1) |
| H4: long gap is whole missed volumes | gap 3.907 s | 13 periods, residual 0.005 s | SUPPORTED for ref04 |
| H5: short gaps (0.45–0.5 s) are missed volumes | gaps 0.452, 0.457, 0.494 s | not whole multiples of 0.3 s; they sit in the upper tail of the same one-sided delay distribution (0.35–0.45 s in every run) | REJECTED as missed volumes; treated as delays (INFERRED) |
| H7: delays are sporadic and one-sided on an exact 0.3 s tick | non-gap interval histogram (`timing_stalls.json`) | below-median share 0 to 0.0002; 12–20 intervals of 0.35–0.45 s per run; delay budget 1.0–1.7 s per run (an identity against the endpoint span; the evidence is the distribution) | SUPPORTED (inferred; to confirm with the authors) |
| H8: delays co-occur with wheel activity | not yet tested (wheel-only check) | — | UNTESTED |
| H6: the C-V2 failure is caused by an arbitrary offset | not tested; no free offset is fitted | — | NOT ASSESSED; no offset is assigned |

## 4. Alignment consequences

- Physio–fUS clock offset: not measurable from onset spacing; UNKNOWN.
- Onset-versus-end convention: up to one frame (0.3 s) if the convention differs; UNKNOWN.
- Accumulated delay: 1.0 to 1.7 s per run in the stamped onsets (sum of one-sided delays). Whether this is alignment error depends on whether the stamps are acquisition times (UNKNOWN).
- Irregular intervals at 0.45–0.5 s: cause UNKNOWN; they are masked by the current gap rule and do not map to whole frames.

## 5. Open questions for the authors (see `author_query_draft_timing.md`, NOT SENT)

1. The frame period: is it 0.3 s (sidecar acquisition duration), or a measured value per run?
2. VolumeTiming: onset at frame start or end; zero reference; why the first onset is 0.1–7.3 s.
3. Delays of 0.35–0.45 s (12–20 per run, one-sided) and intervals of 0.45–0.5 s and 0.6–0.9 s: acquisition events, software delays recorded in the stamps, missed frames, or processing? Are the stamps acquisition times?
4. The clock source for VolumeTiming and for the physio recording, and the offset between them.
5. Meaning of the NIfTI pixdim[4] value (0.1).

## 6. Sources checked

- Dataset record: UCL Research Data Repository, DOI 10.5522/04/31376338.v2 (the DOI redirect page returned HTTP 403 to automated fetch). The B2FIND mirror `https://b2find.eudat.eu/dataset/20510cf4-8b43-53f8-b274-09d9002735a5` lists the authors (Landemard, Krumin, Le Meur-Diebolt, Carandini), no named corresponding author, and a repository contact address (researchdatarepository at ucl.ac.uk, obfuscated on the page). The record does not describe VolumeTiming, the frame period or the wheel encoder. Status: FROM SOURCE (mirror page), VERIFIED for the listed content only.
- fUSI-BIDS specification: not retrieved in this session (search returned general BIDS examples only). Status: UNKNOWN.
- Analysis repository `agneslandemard/fusi_analyses`: partially visible; no timing or encoder code found in the visible files. Status: UNKNOWN for the unseen modules.

## 7. What this ledger does not establish

- It does not establish that the stamps are acquisition times rather than software times. The one-sided delay pattern is consistent with stamps that record delayed onsets; this is INFERRED and needs the authors' confirmation.
- The frozen C-V2 test (period 0.30013 s) is not a test of a true period. Its NOT PASSED result reflects accumulated delay, not a clock difference.
- It does not establish alignment between physio and fUS.
- It does not make any run temporally valid.
