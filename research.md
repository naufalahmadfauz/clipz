# Loudness, spikes and cross-track reaction evidence

**Retrieved:** 2026-09-27. **Question:** [Establish useful loudness, spike, and reaction evidence](../../issues/06-loudness-and-reactions-research.md). Standards inspected: **ITU-R BS.1770-5 (November 2023)**, **EBU R 128 v5 (November 2023)** and **EBU Tech 3341 v4 (November 2023)**. These establish measurement semantics, not gaming-event quality. No recordings, meters or runtime experiments were executed.

## 1. Verified measurement distinctions

| Measurement | Meaning and time support | Appropriate evidence / limitation |
|---|---|---|
| Windowed RMS | Square root of mean squared PCM amplitude; window and hop are application parameters. Define `20 log10(RMS / full_scale)` explicitly. | Cheap energy envelope; sensitive to gain, DC and frequency content. Not perceptual loudness or vocal effort. |
| Sample peak | Maximum absolute sample in the stated interval; normalized amplitude 1 corresponds to 0 dBFS. | Transients/headroom; a large isolated click can dominate. Sample peaks can miss intersample maxima. |
| True peak | Estimate of maximum reconstructed continuous waveform, reported in dBTP. | Overload/headroom evidence; requires oversampling/interpolation and has implementation tolerances. |
| Momentary loudness, M | EBU-mode K-weighted, channel-weighted energy over a **400 ms rectangular sliding window**, **ungated**. | Local loudness changes, with unavoidable window smearing. |
| Short-term loudness, S | Same underlying measurement over **3 seconds**, **ungated**. | Slower context; can obscure brief interjections. |
| Integrated loudness, I | Gated programme/selected-interval energy aggregation. | Session/interval summary, not a local burst detector. |

Sources: BS.1770-5 Annexes 1–2; Tech 3341 §§2.1–2.6; implementation API/source below. [BS1770] [EBU-meter] [lib-api] [FF-astats]

For RMS, a full-scale-peak sine has RMS approximately 0.707 and thus **−3.01 dBFS under the stated amplitude-reference convention**. Some metering conventions offset RMS values, so an unnamed “dB” field is ambiguous. Digital zero mathematically yields negative infinity; preserve a silence/undefined state alongside any finite display floor. Near-rail sample counts or flat tops can flag suspected clipping, but cannot prove clipping history after lossy coding, resampling or earlier gain changes. [BS1770, Annex 2] [lib-api] [FF-astats]

**Integrated gating is specific:** evaluate 400 ms blocks with **75% overlap** (100 ms advance); exclude blocks at/below **−70 LKFS/LUFS**, calculate the absolute-gated energy loudness, derive a second threshold **10 LU below it**, then aggregate blocks above both thresholds. Incomplete final gating blocks are discarded. Average **linear energies**, not dB values or per-chunk integrated LUFS. LUFS and LKFS are equivalent naming conventions here. EBU's −23 LUFS normalization target concerns broadcast delivery; it is not this project's reaction threshold or a reason to normalize source evidence. [BS1770, Annex 1] [EBU-meter, §2.3] [R128]

EBU mode prohibits additional attack/release smoothing of its M/S signals beyond the specified windows. Any detector smoothing should be a **separately named derived feature**. In particular, changing an integrated meter's block size to 400 ms does not turn repeated calls into a conformant momentary meter. [EBU-meter, §2.2] [pyloudnorm]

## 2. Channels, sample rates and bounded computation

**Verified:** BS.1770 applies a shelf plus high-pass K-weighting filter per channel, computes channel energies, and sums them with channel-position weights. In the basic layout L/R/C weights are 1, surrounds 1.41, and LFE is excluded. Its published filter coefficients are for **48 kHz**; other rates require equivalent responses, not unchanged coefficients. Multichannel LUFS is not the LUFS of an arbitrary mono downmix. Identical dual-mono channels contribute twice the energy of one mono channel, approximately 3.01 LU more under this summation. [BS1770, Annexes 1 and 3]

**Design implication:** measure each selected AudioTrack with explicit channel/layout and gain provenance; optionally retain per-channel peaks/energy to reveal imbalance or cancellation. Keep native/full-band analysis conceptually separate from 16 kHz mono ASR input: resampling/downmixing changes evidence. Independently recorded people are not automatically a surround programme. Missing recording spans are unknown coverage, not digital silence; discontinuities need declared filter/window reset behavior.

Primitives inspected:

- **Rolling RMS/peak and SciPy filtering:** sums of squares plus a bounded ring buffer support windowed RMS; block maxima or a rolling-max structure support peaks. `scipy.signal.sosfilt` accepts initial delay state and returns final state, enabling K-filter continuity across chunks. This is a primitive, not a certified loudness implementation. Inspected SciPy documentation identifies **1.18.0**; its license is BSD-3-Clause. [SciPy] [SciPy-license]
- **libebur128 1.2.6, MIT:** incremental `add_frames_*`, explicit channel maps, M/S/I, sample/true peaks; inputs are interleaved frames with the actual sample rate. `MODE_HISTOGRAM` offers bounded accumulated statistics; ordinary integrated history can grow, and `set_max_history` restricts the measured history. A restricted history is not whole-session I. Its true-peak algorithm is version-dependent. Windows binary/binding packaging still needs verification. [lib-api] [lib-license]
- **FFmpeg n8.0 reference source:** `ebur128` uses fixed-size energy histograms and 400 ms/3 s integrators, exposes metadata, and defaults meter-video generation off. `astats` supplies RMS, peaks and other diagnostics; its reset count refers to incoming audio frames, not a fixed time interval. These filter source files are LGPL-2.1-or-later; distribution rights depend on the complete FFmpeg build. [FF-ebur] [FF-astats]
- **pyloudnorm, MIT:** useful for bounded reference clips, but inspected `integrated_loudness` copies the supplied array, filters it and allocates per-block arrays. Its up-to-five-channel order excludes LFE. Calling it on a four-hour waveform is not a bounded streaming solution; it documents BS.1770-4 rather than automatically claiming all BS.1770-5 capabilities. [pyloudnorm] [py-license]

**Proposed:** persist compact block energies when exact later re-gating is required, or explicitly identify histogram approximation. Save filter state, partial windows, sample position and baseline/event state for restart equivalence. Work boundaries must not reset every window or fabricate padded silence.

## 3. Relative spikes and silence transitions: unvalidated heuristics

No standard reviewed defines a “gaming reaction.” A plausible comparison is short-window RMS against M loudness, each with a slower **per-track robust baseline**. Candidate baselines include rolling median/quantiles and median absolute deviation over a bounded history. Preserve both absolute level and relative excess; a large relative jump from a tiny noise floor can remain inaudible. Bound the dispersion denominator when a quiet baseline has zero variance. Window lengths, history, eligibility floor and thresholds remain human/measurement decisions.

Compare an all-valid-audio baseline with an active-audio baseline. The former can be dominated by long silence; the latter requires a gate and can exclude quiet speech. Mark warm-up/insufficient history. Freezing or slowing baseline updates during candidate bursts may prevent a long reaction from immediately becoming “normal,” but can over-trigger sustained music. Gain steps/AGC and limiter changes can cause false spikes or hide actual shouting; record/reset regimes when known and test change detection rather than claiming gain invariance.

A candidate event state machine can use a higher entry threshold, lower exit threshold, minimum hold/attack, release duration and a declared merge gap. Retain raw onset/offset support separately from any context padding. “Silence-to-energy” should require prior low-energy duration and a subsequent absolute-plus-relative rise. Silence here means signal level below a rule, **not speech VAD**; game effects, breathing and keyboard noise can satisfy it. Neither energy nor speech activity establishes shouting or humor.

## 4. Coincidence is not independent corroboration

**Inference:** coincident peaks on microphone and game/Discord AudioTracks may be the same loudspeaker bleed, duplicated mix, echo or soundboard. First use known routing/track lineage to identify dependent observations. Waveform similarity/cross-correlation can suggest shared content or delay; correlation alone cannot prove different people reacted, and compression/echo can conceal duplication. Retain the observations with a shared-audio/unknown-independence flag rather than deleting evidence or multiplying scores.

Join events only on the project timeline after synchronization. A proposed coincidence allowance must include both tracks' synchronization uncertainty, detector-window support and permitted human response lag. Narrow tolerances create false non-coincidence; wide tolerances join unrelated events. Count independent recording/evidence groups conservatively, not channels or assumed speakers. Pairwise independence, participant count and causal reaction remain unresolved evidence, especially for mixed Discord audio.

## 5. Validation still required

Use EBU/ITU specified meter test cases to check gating, channel weights, peaks and chunk equivalence; then separately annotate useful bursts/transitions and genuine multi-person reactions on representative recordings. Include game-only bursts, duplicated/lagged mixes, AGC changes, sustained loud passages, quiet speech, gaps and uncertain sync. Compare false events/hour, missed annotated events, timing error and runtime/storage with human-agreed thresholds. No tests or measurements were run. These contrasts refine the existing signal-semantics, dataflow, synchronization and validation decisions; they require no new policy ticket.

## Primary sources

[BS1770]: https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf
[EBU-meter]: https://tech.ebu.ch/docs/tech/tech3341.pdf
[R128]: https://tech.ebu.ch/docs/r/r128.pdf
[lib-api]: https://github.com/jiixyj/libebur128/blob/v1.2.6/ebur128/ebur128.h
[lib-license]: https://github.com/jiixyj/libebur128/blob/v1.2.6/COPYING
[SciPy]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt.html
[SciPy-license]: https://github.com/scipy/scipy/blob/v1.18.0/LICENSE.txt
[FF-ebur]: https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavfilter/f_ebur128.c
[FF-astats]: https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavfilter/af_astats.c
[pyloudnorm]: https://github.com/csteinmetz1/pyloudnorm/blob/master/pyloudnorm/meter.py
[py-license]: https://github.com/csteinmetz1/pyloudnorm/blob/master/LICENSE
