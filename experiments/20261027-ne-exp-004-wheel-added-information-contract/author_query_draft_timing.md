# DRAFT — NOT SENT

Status: prepared for the owner. Not sent. Sending is an outward-facing action and needs explicit owner approval. Do not send from any automated process.

Recipient: the research data repository contact of the UCL record for "Functional Ultrasound Imaging (fUSI) data from head-fixed, freely running mice" (DOI 10.5522/04/31376338.v2). The address is `researchdatarepository` at `ucl.ac.uk` as shown on the mirror page; the owner must confirm it on the live record before sending. No named corresponding author is listed. The authors listed are Agnès Landemard, Michael Krumin (listed as "Krumins" on one mirror), Samuel Le Meur-Diebolt and Matteo Carandini; they may be copied only if the repository confirms a contact route.

Subject: Timing and sampling of VolumeTiming and the wheel_velocity channel (sub-ALD002 fUSI-BIDS)

Body (draft):

Dear research data repository team,

We are analysing sub-ALD002 in the functional ultrasound dataset above and need to understand its timing. We have only read the archive metadata; we have not used any fUS signal values for this question.

Observations from the files:
- VolumeTiming in each fUSI run has the same length as the NIfTI frame count, but the onset intervals have a median of 0.300 s and a per-run mean of 0.300121 to 0.300177 s, with a standard deviation of 3 to 4 ms.
- The sidecar gives FrameAcquisitionDuration of 0.3 s. We could not find a frame period field.
- The first VolumeTiming onset is between 0.1 s and 7.3 s, not zero.
- A few intervals are 0.45 to 0.5 s, which is not a whole number of frames, and one run has a gap of 3.9 s.
- The NIfTI header field pixdim[4] is 0.1.

Questions:
1. What is the frame period: 0.3 s, or a value measured per run? If measured, how was it obtained?
2. How is VolumeTiming defined: onset relative to the start or the end of the frame, what is the zero reference, and why does the first onset lie between 0.1 and 7.3 s?
3. The onset intervals are 0.300 s in almost every case, with about 12 to 20 intervals per run between 0.35 and 0.45 s, one-sided (later, never earlier), and a few between 0.45 and 0.5 s. The summed delay is 1 to 1.7 s per run. Are these delays acquisition events, software timing delays recorded in the stamps, or processing artefacts? Are the stamps acquisition times? Is there a documented rule for dropped or delayed frames, and is any delay expected to correlate with the animal's movement?
4. Which clock produced VolumeTiming, and what is the reference for the physio recording (StartTime 0.0 s)? Is there a documented offset between the physio and fUS clocks?
5. What does NIfTI pixdim[4] = 0.1 represent?
6. Is the wheel_velocity channel documented beyond "from rotary encoder" (encoder counts per revolution, wheel circumference, derivation, minimum speed or thresholds)?

We do not need any personal data. A pointer to the relevant acquisition or export documentation, or to the code that writes VolumeTiming, would help.

Thank you.

Owner to review and sign before sending.
