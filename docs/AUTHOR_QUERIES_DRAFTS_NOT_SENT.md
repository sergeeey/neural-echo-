# Author query drafts — NOT SENT

Status: prepared for the owner. Nothing here has been sent. Sending is an outward-facing action and needs explicit owner approval for each recipient. No automated process may send these.

The owner asked for the two requests to be combined if the addressee matches. It does not match, so they stay separate:

- Draft 1 goes to the UCL research data repository (Landemard et al. record, DOI 10.5522/04/31376338.v2).
- Draft 2 goes to the authors of the Cybis Pereira et al. record (Zenodo 15476373).

## Draft 1 — VolumeTiming and wheel encoder (Landemard / sub-ALD002)

Recipient: the research data repository contact of the UCL record. The address shown on the mirror page is `researchdatarepository` at `ucl.ac.uk`, obfuscated there. **Owner must confirm the address on the live record before sending.** No named corresponding author is listed.

Subject: Timing of VolumeTiming and the wheel_velocity channel (sub-ALD002, fUSI-BIDS)

Body:

Dear research data repository team,

We are analysing sub-ALD002 in the functional ultrasound dataset above and need to understand its timing. We have only read the archive metadata. We have not used any fUS signal values for this question.

Observations from the files:
- VolumeTiming in each fUSI run has the same length as the NIfTI frame count. Onset intervals have a median of 0.300 s and a per-run mean of 0.300121 to 0.300177 s, with a standard deviation of 3 to 4 ms.
- The sidecar gives FrameAcquisitionDuration of 0.3 s. We found no frame period field.
- The first VolumeTiming onset lies between 0.1 s and 7.3 s, not zero.
- A few intervals are 0.45 to 0.5 s, which is not a whole number of frames. One run has a gap of 3.9 s.
- The NIfTI header field pixdim[4] is 0.1.

Questions:
1. What is the frame period: 0.3 s, or a value measured per run? If measured, how?
2. How is VolumeTiming defined: onset relative to the start or the end of the frame? What is the zero reference? Why does the first onset lie between 0.1 and 7.3 s?
3. Intervals are 0.300 s almost always, with about 12 to 20 per run between 0.35 and 0.45 s, always later and never earlier, and some between 0.45 and 0.5 s. The summed delay is 1 to 1.7 s per run. Are these acquisition events, timing delays recorded in the stamps, or processing artefacts? Are the stamps acquisition times? Is there a documented rule for dropped or delayed frames?
4. Which clock produced VolumeTiming, and what is the reference for the physio recording (StartTime 0.0 s)? Is there a documented offset between the physio and fUS clocks?
5. What does NIfTI pixdim[4] = 0.1 represent?
6. Is wheel_velocity documented beyond "from rotary encoder"? Please give encoder counts per revolution, wheel circumference, the derivation, and any minimum-speed threshold. The exact zeros (80 to 94 percent of samples) — are these real stillness or a threshold?

We do not need personal data. A pointer to acquisition or export documentation, or to the code that writes VolumeTiming, would help.

Thank you.

[Owner to review and sign before sending.]

## Draft 2 — GLM t-statistic maps and lag kernels (Cybis Pereira et al., Zenodo 15476373)

Recipient: the corresponding author of the Cell Reports article (DOI 10.1016/j.celrep.2025.116791), or the first author listed on the Zenodo record (Felipe Cybis Pereira, ORCID 0009-0009-6124-0466). The Zenodo README says the slowwave derivative is requested through the corresponding author. **Owner must confirm the corresponding author and address from the published article before sending.** The journal full text returned HTTP 403 to automated retrieval, so the address is not verified here.

Subject: Request for GLM t-statistic maps for speed decoding (Zenodo 15476373, sub-rat1703)

Body:

Dear Dr Cybis Pereira,

We are reproducing the speed-decoding analysis from "A vascular code for speed in the spatial navigation system" using the Zenodo dataset (CC BY 4.0). Your decode-speed outputs reproduce your quoted maxima on our side. We are now trying a closer replication of the GLM-based lagged convolution you describe, and the archive does not contain the t-statistic maps that the convolution uses. For sub-rat1703, session ses-20210407, the glm-speed derivative holds only the design matrix and the events table.

Requests:
1. The GLM t-statistic maps (voxel-wise, per session or pooled) used to build the time-reversed lagged kernels for decode-speed, for sub-rat1703.
2. The lag range and time step of those kernels (you give -2 to 10 s and dt = 80 ms in the preprint; the exact kernel grid would help).
3. The processing code or a pointer to it for the lagged convolution and the PCA-ridge pipeline, if it is public.
4. If you cannot share the maps, whether the GLM design (the dm.tsv file) plus the events file is sufficient to regenerate them.

We will report results with the source attributed, and will not redistribute the maps. Thank you for your time.

[Owner to review and sign before sending.]
