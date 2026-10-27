# Milestone qualification note (2026-10-27)

Scope: stages 2 and 3 of the 20-of-100 mission. Read-only, no downloads, no real-signal run.
Evidence labels: VERIFIED (read by a tool in this session), SOURCE (documented by the cited page), UNKNOWN.

## Stage 2 — timing qualification of the Landemard / ALD002 record

**Verdict: BLOCKED.**

Reason: the semantics of `VolumeTiming` (onset at frame start or end, zero reference, and what the stamps measure) cannot be established from any available source.

| Question | Status | Evidence |
|---|---|---|
| What `VolumeTiming` means | UNKNOWN | BEP 040 page (https://bids.neuroimaging.io/extensions/beps/bep_040.html) does not mention `VolumeTiming`; it only says timing metadata was copied from fMRI-BIDS and that non-stable sampling "could be discussed" (SOURCE, fetched this session) |
| Frame period | UNKNOWN (quoted 0.30013 s not confirmed) | Sidecar `FrameAcquisitionDuration` = 0.3 s, no frame-period field (VERIFIED, `timing_evidence_ledger.md` §1) |
| Onset tick and delays | VERIFIED | Intervals on an exact 0.300 s tick; one-sided delays of 0.35–0.45 s, 12–20 per run (`timing_stalls.json`) |
| Whether stamps are acquisition times or software times | UNKNOWN | Needs authors' confirmation |
| Physio–fUS clock offset | UNKNOWN | No shared clock documented |
| Wheel encoder derivation | UNKNOWN | Not stated in archive or on the dataset record |

What would change the verdict: a written definition of `VolumeTiming` from the authors or from a fUSI-BIDS specification text that defines it; a stated clock source for both streams. Neither is available now. The author query (`author_query_draft_timing.md`) remains NOT SENT.

Consequence: no baseline is run on ALD002 under this mission until the verdict changes.

## Stage 3 — alternative open fUS datasets (search only)

No dataset was downloaded. Licence and signal content were checked against the listing pages only.

| Candidate | Source | Species | Behaviour/physio signals | Licence | Published decoding baseline | Status |
|---|---|---|---|---|---|---|
| `fetch_cybis_pereira_2026` (ConfUSIus) | https://confusius.tools/latest/user-guide/datasets/ | Rat | DeepLabCut videos; linear and angular speed (GLM derivatives). No wheel, pupil, whisking, or physio | Not stated | Not stated; `decode-speed` and `interanimal-decode-speed` derivatives are provided | Strongest lead: a behavioural label is present, but licence and baseline unconfirmed |
| `fetch_nunez_elizalde_2022` (ConfUSIus) | same | Mouse | Not stated | Not stated | Not stated | Lead, low detail |
| `fetch_landemard_2026` (ConfUSIus) | same | Mouse | Locomotion implied, no signal named | Not stated | Not stated | Same record as ALD002; does not resolve the timing question |
| Griggs et al. 2023, NHP saccade/reach fUS | arXiv 2509.18507 (search result, not fetched) | Macaque | Movement direction as label | Not checked | Not checked | Lead only; repository not confirmed |

Licence note: the ConfUSIus page states that licences vary (CC BY 4.0, CC0 1.0, CC BY-NC 4.0 are listed for the collection) but does not give a licence per dataset. A per-dataset check in https://github.com/confusius-tools/confusius-datasets is required before any download.

Source note: the ConfUSIus page fetch returned an automated warning about a command-injection pattern in the response. The content was treated as reference data only; no instruction in it was followed.

## Stage 4 — baseline status

- ALD002: not run. Blocked by Stage 2.
- Cybis Pereira 2026 (candidate): not run. Needs (a) licence confirmed per dataset, (b) download permission from the owner (downloading requires explicit approval), (c) a stated baseline definition. None is in place.

## What this milestone does not establish

- It does not establish that any dataset is usable for decoding.
- It does not establish a reproduced baseline.
- It does not change the C-V2 result, which remains NOT PASSED.
- The estimate of progress toward 20/100 is the owner's; this note adds no new scientific evidence.

## Decisions for the owner

1. Permission to check the per-dataset licence on the ConfUSIus repository (read-only).
2. Permission to download the Cybis Pereira 2026 dataset, if its licence allows, to run a classical speed-decoding baseline.
3. Whether to send the timing query (`author_query_draft_timing.md`), which is the only route that can unblock Stage 2.
