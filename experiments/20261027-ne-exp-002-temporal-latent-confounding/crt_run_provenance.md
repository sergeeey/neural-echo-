# Run provenance: CRT v1/v2 pilots and diagnostics (NE-EXP-002, synthetic only)

No fUS outcome is used in any file below. The holdout run was excluded by name and never read.
Status values: COMPLETE, PARTIAL (not used for any verdict), CHECK (diagnostic, no outcome).

| Artifact | Code version | Seed | Config | Status |
|---|---|---|---|---|
| `crt_pilot_v1_n30.json` | 04267d6 (flags: standardise False, edge_frames 20) | 20261027 | 30 reps x 99 draws, 6 scenarios | COMPLETE |
| `crt_pilot_v2_n30.json` | 04267d6 (flags: standardise True, edge_frames 40) | 20261027 | 30 reps x 99 draws, 6 scenarios | COMPLETE |
| `crt_comparison.md` | summariser `scripts/summarise_crt_pilot.py` (uncommitted when run) | n/a | reads the two JSON files above | COMPLETE |
| `crt_pilot_v1_full100.json` | pre-edge working tree on HEAD 6d430f4 (launched 09:11); file's `code_version` field reads 04267d6 (HEAD at write time) | 20261027 | 100 reps x 99 draws, six scenarios | COMPLETE (supplementary; see `crt_v1_full100_summary.md`) |
| `crt_pilot_v1_n100_PARTIAL.txt` | same run, stdout snapshot at 10:21 | 20261027 | 4 of 6 scenarios | SUPERSEDED by the complete JSON |
| `crt_pilot_v1_n1` reproduction | 04267d6 with flags | 20261027 | 1 rep x 19 draws | CHECK: max difference 0.0 against the saved smoke file |
| `crt_pairing_check.txt` | `scripts/check_crt_pairing.py` | 20261027 | 1 rep per scenario | CHECK: v1 and v2 synthetic series identical, RNG state identical |
| `crt_diagnostics.json` | HEAD 6d430f4 at run time (the JSON's `code_version`); script as committed in 04267d6 | n/a | development runs, leave-one-run-out profile | CHECK |
| `crt_wheel_raw_audit.txt` | `scripts/audit_crt_wheel_raw.py` (untracked at run time) | n/a | raw physio, development runs, read-only | CHECK: exact-zero 80–94%, no NaN |
| `crt_wheel_investigation.txt` | `scripts/investigate_crt_wheel.py` (uncommitted when run) | n/a | development runs | CHECK |
| `crt_surrogate_fidelity.txt` | `scripts/check_crt_surrogates.py` (uncommitted when run) | 7 | development runs, 19 draws | CHECK |
| `crt_two_component_fidelity.txt` | `scripts/check_crt_two_component.py` (uncommitted when run) | 11 | development runs, 19 draws | CHECK |
| `prediction_comparison_calibration.txt` | `scripts/check_prediction_comparison.py` (uncommitted when run) | 31 | 20 reps per synthetic scenario | CHECK; not a calibrated test |

## Notes on provenance

- The v1-30 and v2-30 runs share one seed and one random stream; `crt_pairing_check.txt` confirms
  that the synthetic series and the final RNG state are identical. The paired comparison is valid.
- The 100-rep v1 run was launched before the edge and standardisation flags existed in the file it
  loaded. It completed all six scenarios (`crt_pilot_v1_full100.json`); the earlier 4-of-6 stdout
  snapshot is superseded. The per-replicate p values were not stored in that run, so it cannot be
  paired with the 30-rep runs.
- Seven scripts in `scripts/` were untracked when their outputs were produced and are NOT in any commit yet (`git status` at the time of this record): `summarise_crt_pilot.py`, `investigate_crt_wheel.py`, `check_crt_surrogates.py`, `check_crt_two_component.py`, `check_prediction_comparison.py`, `check_crt_pairing.py`, `audit_crt_wheel_raw.py`. The v1-30 and v2-30 JSON files were produced by the committed code (04267d6). The 100-rep JSON was produced by an uncommitted pre-v2 tree on 6d430f4 (see the table below). (Earlier wording of this line listed four scripts and claimed a commit that did not exist.)
- Commit identifiers in this table refer to the local commit 04267d6 (not pushed).

## Provenance fields per run group (split: reported vs executed)

Commit timing (from `git log` and the reflog, local time +0500): 6d430f4 at 09:01:39; 04267d6 at 09:39:23.
The launch time of the 30-replicate pilots (09:39:54) is taken from the session transcript and the process
list; it is **unverified from the repository**, because the JSON mtimes record only completion. The evidence
that the executed code equals commit 04267d6 is that the crt.py and runner blobs are identical to their
04267d6 versions today (`git rev-parse`), not the launch timing.

| Run group | reported_git_head (in JSON) | execution_git_head | execution_worktree | source_hash | reconstruction_status |
|---|---|---|---|---|---|
| `crt_pilot_v1_n30.json` (v1 config, 30 reps) | 04267d6 | 04267d6 | tracked source files unchanged (crt.py and runner blobs equal to 04267d6 today); docs and results files modified since, not executed code; untracked analysis scripts not imported by the pilot | crt.py blob `25453e8143961eb4fd8edd66c89276bc3ca96017`; runner blob `66690e1c215bf61603cc8bac3a4a81307b2b66b5` (both at 04267d6) | REPRODUCED from the commit (executed code is the committed code) |
| `crt_pilot_v2_n30.json` (v2, 30 reps) | 04267d6 | 04267d6 | as above | as above | REPRODUCED from the commit |
| `crt_pilot_v1_full100.json` (v1, 100 reps) | 04267d6 (HEAD at write time, 10:52) | 6d430f4 | UNCOMMITTED_PRE_V2: crt.py without the edge_frames argument; runner without VERSION flags (launched 09:11) | UNKNOWN (no snapshot of the loaded file was saved) | PARTIALLY_REPRODUCED: v1 flags match the smoke file on 1 rep x 19 draws (max difference 0.0); the 100-rep run itself is not reproduced |
| `crt_diagnostics.json` | 6d430f4 (its `code_version` field) | 6d430f4 at write time, script as committed in 04267d6 | not recorded separately | UNKNOWN for the JSON; script blob as committed | CHECK |

Neither the 04267d6 value in `crt_pilot_v1_full100.json` nor the 6d430f4 value in the diagnostics JSON
describes the code that produced the numbers without the qualifications above.
