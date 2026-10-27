# DRAFT — NOT SENT

Status: prepared for the owner. Not sent. Sending requires explicit owner approval, because it is an outward-facing message.

Recipient: to be identified from the dataset record (DOI 10.5522/04/31376338.v2, figshare). The contact address is NOT verified; do not send to any address until it is confirmed on the record.

Subject: Question on the wheel_velocity channel of the sub-ALD002 physio recordings

Body (draft):

Dear dataset authors,

We are analysing the fUSI-BIDS recordings of sub-ALD002 (Landemard et al.) and would be grateful for documentation of the running-wheel channel. The sidecar states "Wheel velocity from rotary encoder" in cm/s, sampled at 1000 Hz. In our raw audit, the velocity is exactly zero in roughly 80 to 94 percent of samples, in runs from milliseconds to several minutes. We cannot tell from the files whether these zeros reflect the animal being stationary, a sensor resolution limit, or a processing step. Could you tell us:

1. The encoder model, counts per revolution, and wheel circumference, so the velocity resolution can be computed.
2. How wheel_velocity is derived from the encoder: differencing of counts, any filtering, thresholding, minimum-speed cut-off, or resampling to 1000 Hz.
3. Whether a zero value means no encoder count in the sample interval, or whether zeros were introduced by any processing step.
4. Whether the processed fUSI-BIDS files contain any unprocessed version of this channel.
5. How the physio StartTime (0.0 s) is referenced to the VolumeTiming onsets of the fUSI runs.

We do not need any personal data. Any pointer to a document or to the relevant analysis code would help.

Thank you.

Owner to review and sign before sending.
