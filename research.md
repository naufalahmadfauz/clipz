# Media timing, decoding, and synchronization evidence

Retrieved **2026-09-27** for [Establish media timing, decoding, and synchronization capabilities](../../issues/03-media-timing-and-decoding-research.md). Research only; no media experiments or performance measurements were performed.

**Bottom line:** FFmpeg and PyAV support incremental, selected-audio decoding and sharing decoded samples. Preserving recording-session timing requires an explicit relationship between source timestamps, decoded samples, and project time. A raw PCM pipe or faster-whisper's file-loading helper does not retain that relationship. Waveform matching can supply alignment evidence when sufficiently distinctive audio is shared; it cannot establish synchronization without corresponding observations.

## Evidence and version boundaries

**Verified** below means documented behavior or inspected upstream source, not a successful local test. **Inference** means a consequence of those facts or stated mathematics. **Proposal** identifies an option or experiment for the human's later decisions.

Context7 was resolved and queried for FFmpeg, PyAV, and faster-whisper. Its older PyAV documentation was cross-checked against current **PyAV 18.1.0** documentation and tagged source. FFmpeg references use the living manuals and **n9.0.2** source; relevant decoder/probing behavior was also checked in **n8.0**. Faster-whisper source is **v1.2.1**. The release APIs identify PyAV 18.1.0 and faster-whisper 1.2.1 as latest releases at retrieval. These are research reference versions, not a proposed dependency lock.[V]

Immediate decode consequence: PyAV 18.1.0's README documents bundled FFmpeg libraries in wheels and FFmpeg **8.x** source-build support. An external `ffmpeg`/`ffprobe` executable and PyAV may therefore use different engines/builds; record both versions and available codecs. Broader distribution decisions belong to the parallel ticket.[P0][F1]

## 1. Discovery: streams are not channels

**Verified:** `ffprobe -show_format -show_streams -of json INPUT` exposes container/stream information; `-select_streams a` restricts stream-related output. Record available stream indices/IDs, codecs, sample formats/rates, channel counts/layouts, time bases, starts, durations, tags, and dispositions. Missing fields remain unknown. `-show_packets` exposes packet evidence; `-show_frames` examines decoded frames. `-read_intervals` seeks approximately, so it is unsuitable as an exact sample-boundary oracle.[F2][F6]

`-map 0:a:1` selects the **second audio stream** in input zero; `-map 0:1` selects absolute stream index one. Neither selects a channel. Without mapping, FFmpeg ordinarily chooses one audio stream, preferring the greatest channel count. `-ac 1` requests mono conversion rather than extracting a particular microphone. `channelsplit` extracts channels; `pan` supports explicit channel indices/names and mixing gains.[F1][F8]

PyAV exposes stream metadata and frame layouts. Planar arrays have separate channel rows; packed arrays interleave channel samples. `AudioFrame.samples` is samples **per channel**, and `to_ndarray()` currently stacks plane views into a new array: do not assume zero-copy sharing.[P3]

**Inference:** logical AudioTracks can reference selected streams/channels or a declared mix. Neither channel labels nor stream titles establish speaker identity. Unknown layouts need explicit handling: FFmpeg tries to guess layouts by default (`-guess_layout_max 0` disables guessing). Downmixing can combine unrelated voices, alter energy, and cancel opposite-polarity signals; retaining the selection/mixing recipe matters for acoustic evidence.[F1][F4][F8]

## 2. Actual audio-only paths and boundedness

| Interface | Verified processing behavior | Timing/memory consequence |
| --- | --- | --- |
| FFmpeg subprocess | Selected stream → audio decoder → filters/conversion → PCM encoder/muxer → binary stdout. `-map 0:a:0 -vn -sn -dn -c:a pcm_f32le -f f32le pipe:1` illustrates output selection.[F1][F10] | Raw PCM contains one stream and **no timestamps or metadata**. Incremental reads are possible, but require known rate/layout/format plus a separate timing relationship.[F3] |
| PyAV in-process | `demux(*selected_streams)` yields packets; `packet.decode()` returns frames. `decode(audio=0)` is a frame iterator for the first audio stream. Final dummy packets flush delayed decoder output.[P1] | Frames retain PTS/time-base/sample information. Bounded consumption is possible; accumulating frames, arrays, or work queues defeats it.[P1][P3] |
| faster-whisper file helper | Decodes `audio=0`, clears frame PTS before FIFO grouping, resamples to s16 mono (or stereo), appends everything to `BytesIO`, then returns float32 audio; invalid-data errors are skipped.[W] | **Whole-input materialization**, lost source timing, and additional buffers. Stereo splitting follows stereo conversion; it is not arbitrary embedded-stream/channel selection.[W] |

**Important qualification:** selected-audio processing avoids a full video decode/render pipeline, but does not promise zero video bytes read or zero video decoding during discovery. PyAV opens with `avformat_find_stream_info`; FFmpeg's probing code can decode audio/video frames to discover parameters. PyAV's later demux loop reads packets and filters selected streams; setting unused streams' `discard` can reduce subsequent work, but happens after opening.[P1][P3][F6]

**Inference:** one source traversal can feed a separate decoder for each selected encoded audio stream. Channels of one decoded stream can share that decode and then branch into different rates/mixes. Separate sources still require separate demux/decode contexts. Reopening the same source independently for every analyzer repeats work. Probe scans, synchronization searches, recovery seeks, and later reanalysis may add passes; “one pass” must name the stage and unit.[F1][P1][F8]

Supplying an appropriately sampled NumPy waveform bypasses faster-whisper's media loader. It does **not** make inference streaming: ordinary `transcribe()` computes features before returning its segment generator; its batched path also prepares feature collections eagerly. `chunk_length` or output iteration is not an input-memory bound. Explicitly bounded waveform calls are an option, with context/overlap/timestamp reconciliation still requiring validation.[W]

## 3. Source time, starts, priming, and interruptions

**Verified:** PyAV stream `start_time`/`duration` use `stream.time_base`; frame PTS uses the frame's own time base. Container start/duration use FFmpeg's `AV_TIME_BASE` units. These clocks must not be interchanged. Retain packet PTS/DTS/durations for provenance, but use decoded frame PTS/sample counts for usable PCM after trimming. DTS concerns decoding; PTS concerns presentation. Timestamp values may be absent.[P1][P3][F6][F7]

**Derived relationship:** for a decoded frame whose first-sample PTS is `p`, time base is `u/v`, sample rate is `r`, and sample index is `j`,

`source_time(j) = p × u/v + j/r`.

Keeping signed integer PTS, rational time bases, and integer sample counts preserves the available precision without choosing the project's canonical clock. `start_time` is not an extra offset to add to an already absolute PTS. Independently zeroing each embedded stream would erase their relative starts unless the removed origins were retained.[P3][F6]

| Mechanism | Verified behavior and resulting constraint |
| --- | --- |
| CLI timestamp rewriting | `-copyts` retains input timestamps including starts, but muxer processing can still change them. `-start_at_zero` deliberately shifts them; `avoid_negative_ts` can shift output. None can make raw PCM carry PTS.[F1][F3] |
| MOV/MP4 edit lists | By default the demuxer modifies its stream index to reflect edit-list timing. “Source PTS” from the decoder is consequently demuxer-interpreted presentation timing, not necessarily unmodified on-disk media time.[F3] |
| Priming/padding | `AV_PKT_DATA_SKIP_SAMPLES` expresses start/end sample removal. FFmpeg's decoder normally applies skip/padding information and adjusts frame PTS/sample counts; manual-skip mode differs. Negative packet PTS can precede usable audio. Do not blindly trim again or apply a universal AAC/MP3 delay.[F7] |
| CLI discontinuity correction | For discontinuous formats such as MPEG-TS/HLS, `-dts_delta_threshold` defaults to 10 seconds and can remove timestamp jumps; `-copyts` normally disables that correction, except wrapping. Other formats have different timestamp-error handling.[F1] |
| Timestamp synchronization | `-isync` uses input start-time differences and expects a shared clock source. It is not waveform matching for independent recorders.[F1] |

**Inference/proposed evidence model:** distinguish recorded silence, absent samples with a PTS gap, decoder corruption/dropout, timestamp reset/overlap, and a recorder pause that concatenates samples without leaving timing evidence. Comparing consecutive decoded frame starts against `previous_start + samples/rate` exposes candidate discontinuities; a tolerance must account for timestamp quantization. No universal threshold is established here.[P3][F6][F7]

An uninterrupted sample counter reconstructs local elapsed audio time, not missing wall-clock time. FFmpeg can infer timestamps when the format lacks them; those do not prove a recording-session origin. If a recorder deletes an interval and preserves neither its duration nor an independent reference, that duration is unknowable from the remaining samples alone. Gap filling, rejecting damaged spans, or retaining discontinuous spans are policy choices. Invented silence must not be mislabeled as observed silence.[F6]

## 4. Resampling and chunk/seek boundaries

**Verified:** libswresample can buffer samples because filters need future input; it exposes delay and actual output counts and requires end flushing. PyAV's resampler returns a **list**, potentially empty, and accepts `None` to flush. Its conversion path follows the first frame's format/layout/rate and rejects later mismatches. Current `options` passes resampler settings through an explicit `aresample` filter.[F5][P2]

Two significant source-level details:

- PyAV FIFO validates PTS against `pts_per_sample × samples_written`, beginning at **zero**, rather than accepting any nonzero starting origin. Its reads construct sample-counter PTS. An external origin/span mapping or deliberate rebasing is necessary; setting PTS to `None` merely bypasses the check.[P2]
- PyAV 18.1.0's resampler passthrough test checks format/layout/rate and `frame_size`, **not `options`**. Same-format/rate/layout conversion with default frame size can bypass requested compensation options. This needs a targeted test before relying on same-rate `async` settings.[P2]

FFmpeg's `async` defaults to zero; enabling it can stretch/squeeze, fill, or trim samples to match supplied timestamps. `first_pts` can pad/trim a stream's beginning. These operations alter the sample-to-time relationship; they do not independently discover clock drift between recordings.[F4]

**Inference/proposal:** retain continuous decoder/resampler state across ordinary processing blocks; use emitted frame timing and actual sample counts, not separately rounded per-block rate ratios. Flush at the end of a continuous span and handle genuine discontinuities explicitly. Analyzer windows can be cut from continuous PCM without restarting media decoding. Changing nominal rate from 48 kHz to 16 kHz alone does not fix independent recorder clock error.[F4][F5][P2]

Seeking is a different operation. PyAV seeks approximately in stream ticks (or container units without a stream) and flushes codec buffers; it does not reset separately held resamplers/FIFOs. FFmpeg input `-ss` seeks earlier and, during accurate transcoding, decodes/discards preroll; `-seek_timestamp` changes interpretation for nonzero starts. MP4 seeking may return a different packet sequence from linear demux. Sample-exact chunks therefore require verified preroll, decode-forward, sample trimming, filter-state treatment, and exclusive endpoints—not merely issuing repeated seeks.[P1][F1][F3]

## 5. PCM sharing and storage arithmetic

**Arithmetic, not a benchmark:** payload bytes = `seconds × samples/second × channels × bytes/sample`. For four hours, seconds = **14,400**; GB = 10^9 bytes, GiB = 2^30 bytes. Sample widths follow the documented PCM formats.[F3][P2]

| PCM representation | Bytes | GB | GiB |
| --- | ---: | ---: | ---: |
| 16 kHz mono s16 | 460,800,000 | 0.4608 | 0.4292 |
| 16 kHz mono float32 | 921,600,000 | 0.9216 | 0.8583 |
| 48 kHz stereo s16 | 2,764,800,000 | 2.7648 | 2.5749 |
| 48 kHz stereo float32 | 5,529,600,000 | 5.5296 | 5.1498 |
| 48 kHz six-channel float32 | 16,588,800,000 | 16.5888 | 15.4495 |

These exclude headers, model features, copies, queues, and caches. One minute of 48 kHz stereo float32 is 23,040,000 bytes, approximately 21.97 MiB. Multiply by independent representations and simultaneously retained blocks. A four-hour stereo float32 WAV exceeds classic RIFF's 32-bit size fields; FFmpeg supports RF64/Wave64, with RF64 defaulting to `never`. Chunking or another large-file representation is another option.[F9]

**Design comparisons, not selections:**

| Representation strategy | Opportunity | Cost/limit to measure |
| --- | --- | --- |
| Independent analyzer PCM | Easy independent lifetimes | Repeated decoding/resampling and duplicated storage |
| Shared native-rate/channel PCM | Reuse across acoustic/speech transforms | Larger footprint; downstream conversions and array copies remain |
| Shared 16 kHz mono PCM | Smaller artifact; common speech-model input | Discards channel separation and higher-frequency information from higher-rate sources; cannot reconstruct original-channel evidence |
| Streaming fan-out | Small live sample working set | Slow consumers require bounded queues/backpressure; revisits need replay or storage |
| Materialized/chunked or memory-mapped PCM | Random access and reuse/resume opportunities | Disk I/O, lifecycle and timing sidecar; mapping a file does not prevent eager analyzer allocations |

These consequences follow from conversion semantics and inspected consumers; comparative RAM, disk throughput, decode cost, and cross-process sharing efficiency remain unmeasured.[F4][P3][W]

## 6. Alignment: offset, drift, and missing evidence

**Verified mathematical basis:** cross-correlation sums products at candidate lags; a lag peak can identify a shifted copy, including noisy examples. Direct and FFT implementations exist. The operation returns correlations, not a calibrated probability of synchronization.[S]

**Proposed estimator, unvalidated on this corpus:** compare selected common-audio channels at a common nominal rate; remove DC, normalize window energy, reject silent/short-overlap windows, constrain plausible lags, then refine coarse matches. Use separated early/middle/late windows, peak ambiguity, and held-out anchors. Gain normalization helps multiplicative gain mathematically; compression, clipping, mixing, polarity reversal, and propagation/network delay require empirical checks. Matching a delayed Discord copy can align that copy while leaving another acoustic path offset.[S]

**Derived mappings:** let `s` be local source time and `t` project time.

- Constant offset: `t = s + b`.
- Constant clock-rate difference: `t = a·s + b`. One anchor cannot identify both parameters; two distinct exact anchors determine them, while additional anchors reveal residual error.
- Interruptions/rate changes: separate valid spans with `t = a_k·s + b_k`; do not interpolate through missing material as though it existed.

For illustration only, `|a−1| = 100×10^-6` produces **1.44 seconds** of divergence over 14,400 seconds. This is arithmetic, not a measured recorder characteristic. Offset-only versus affine versus piecewise fitting should be compared using unused anchors; unrestricted warping can conceal bad correspondences.

**Identifiability limit:** unrelated microphone speech and game/Discord-only audio may contain no common waveform. Repeated music can produce several plausible peaks; silence has no distinctive lag. A numerical maximum still exists in many unrelated inputs and is insufficient evidence. “People reacted together” is not sample-level correspondence. Manual anchors, trustworthy shared-clock metadata, or an intentionally recorded common cue can provide independent evidence; otherwise alignment remains unknown. Nominally equal sample rates and file creation times alone establish neither offset nor drift.[S][F1][P1]

## 7. Unknowns and narrowly framed follow-up experiments

No representative recordings, installed decode-build inventory, agreed synchronization tolerances, or resource budgets were supplied to this research. No result establishes corpus compatibility, four-hour bounded memory, matching accuracy, or seek equivalence. Proposed experiments for the existing clock/dataflow/validation decisions:

1. **Timing preservation:** a small known-marker fixture matrix covering multiple embedded streams/channels, nonzero/negative starts, AAC/MP3 priming, PTS gaps, reset/overlap, and collapsed pauses. Compare decoded sample positions and PTS between pinned CLI and PyAV builds; report every inserted/dropped/unknown interval.
2. **Boundary equivalence:** compare continuous decode/resampling with processing-block splits and separately seeked chunks at 44.1/48→16 kHz. Measure sample counts, marker error, seam differences and flush tails. Include nonzero-origin FIFO and same-rate resampler-option passthrough cases.
3. **Alignment identifiability:** use common-audio pairs with known synthetic offset/rate changes and one interruption, plus repeated-pattern and no-common-audio negatives. Report held-out anchor error and false acceptance; agree acceptance thresholds with the human.
4. **Four-hour dataflow:** compare incremental CLI/PyAV consumption, shared PCM, and faster-whisper's file/explicit-window entry points. Measure peak memory, scratch bytes, passes, elapsed decode time, backpressure, and cancellation/restart behavior under identical analyzer work.

**Newly sharpened decision question:** does “audio-only” permit bounded video decoding during stream discovery, or must opening/probing guarantee zero video frames decoded? Current PyAV's open path does not establish the latter. A strict guarantee would need a separate probing-policy experiment across supported containers.[P1][F6]

## Primary sources

- [V] [PyAV release API](https://api.github.com/repos/PyAV-Org/PyAV/releases/latest); [faster-whisper release API](https://api.github.com/repos/SYSTRAN/faster-whisper/releases/latest). Mutable endpoints; versions observed above.
- [F1] [FFmpeg manual](https://ffmpeg.org/ffmpeg.html), stream selection, audio options, seeking, `copyts`, discontinuity handling, and `isync`.
- [F2] [ffprobe manual](https://ffmpeg.org/ffprobe.html), stream/packet/frame reporting and interval semantics.
- [F3] [FFmpeg formats manual](https://ffmpeg.org/ffmpeg-formats.html), MOV demuxer/edit lists and raw PCM muxers; [n9.0.2 PCM muxer source](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavformat/pcmenc.c).
- [F4] [FFmpeg resampler manual](https://ffmpeg.org/ffmpeg-resampler.html), rematrixing, `async`, `first_pts`.
- [F5] [libswresample API](https://ffmpeg.org/doxygen/trunk/group__lswr.html), buffering, flushing, delay, output counts, timestamp compensation.
- [F6] FFmpeg [n9.0.2 avformat.h](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavformat/avformat.h), [n9.0.2 demux.c](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavformat/demux.c), [n8.0 demux.c](https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavformat/demux.c): time units, inferred timing, `avformat_find_stream_info`/`try_decode_frame`.
- [F7] FFmpeg [n9.0.2 packet.h](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavcodec/packet.h), [n9.0.2 decode.c](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavcodec/decode.c), [n8.0 decode.c](https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavcodec/decode.c): skip-sample metadata and `discard_samples`.
- [F8] FFmpeg n9.0.2 [channelsplit](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavfilter/af_channelsplit.c) and [pan](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavfilter/af_pan.c) implementations.
- [F9] [FFmpeg n9.0.2 WAV/Wave64 muxer](https://github.com/FFmpeg/FFmpeg/blob/n9.0.2/libavformat/wavenc.c), `wav_write_trailer`, RF64 defaults and 64-bit sizes.
- [F10] [FFmpeg pipe protocol](https://ffmpeg.org/ffmpeg-protocols.html#pipe), binary descriptor output and seekability.
- [P0] [PyAV 18.1.0 README](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/README.md), bundled libraries and FFmpeg compatibility.
- [P1] [Current PyAV container API](https://pyav.basswood.io/docs/stable/api/container.html); [18.1.0 input container source](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/container/input.py).
- [P2] [Current PyAV audio API](https://pyav.basswood.io/docs/stable/api/audio.html); 18.1.0 [resampler](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/audio/resampler.py) and [FIFO](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/audio/fifo.py) implementations.
- [P3] PyAV 18.1.0 [stream](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/stream.py), [frame](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/frame.py), and [audio frame](https://github.com/PyAV-Org/PyAV/blob/v18.1.0/av/audio/frame.py) implementations.
- [W] faster-whisper 1.2.1 [audio.py](https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/audio.py) and [transcribe.py](https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/transcribe.py).
- [S] [SciPy 1.18.0 correlation documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html), mathematical definition and noisy-signal examples; no dependency choice implied.
