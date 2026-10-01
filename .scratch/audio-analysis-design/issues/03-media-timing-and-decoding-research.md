# Establish media timing, decoding, and synchronization capabilities

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-media-research
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-media
Research worktree: ../research/media
Research asset: [Media timing and decoding evidence](../research/media/research.md)

## Question

What do current FFmpeg/ffprobe and PyAV capabilities actually allow for discovering embedded streams versus channels, preserving source timing, bounded audio-only decoding, resampling, and aligning independently recorded audio?

Compare CLI pipes and in-process decode, independent versus shared PCM representations, seek/chunk boundary behavior, timestamp/time-base metadata, nonzero/negative starts, priming/delay, discontinuities, and channel selection/downmix risks. Explain where per-stream or per-source decoding can be shared and where claims of a single pass are unrealistic. Quantify PCM storage from stated arithmetic, not a fabricated benchmark.

Investigate waveform correlation, ambiguous/no-common-audio cases, offset versus clock drift, anchor-based/piecewise mappings, and validation needs. Distinguish library facts from proposed architecture and measured evidence. Cite primary documentation/source with versions or retrieval dates; record packaging constraints only where they follow directly from the decoding options.

## Answer

Resolved 2026-09-27. [Media timing, decoding, and synchronization evidence](../research/media/research.md) cites current primary documentation and tagged sources, distinguishes verified behavior from inference, and proposes focused follow-up experiments.

- FFmpeg/PyAV support incremental selected-audio decoding. One source traversal can feed per-stream decoders and shared channel/rate derivatives; independent sources, eager consumers, seeking, and reanalysis prevent an unconditional single-pass promise.
- Stream selection is distinct from channel extraction/downmixing. Source timing needs signed PTS/time bases, sample counts, priming/edit-list handling, and explicit discontinuity/span mappings. Raw PCM omits timestamps; faster-whisper 1.2.1's file loader clears PTS and materializes the waveform.
- Resampling requires retained state, actual output counts, and flushing. PyAV 18.1.0's FIFO expects zero-origin continuous PTS, and its resampler passthrough can bypass options. Seeked chunks require boundary-equivalence validation.
- Four-hour PCM payload arithmetic ranges from 0.9216 GB for 16 kHz mono float32 to 5.5296 GB for 48 kHz stereo float32, excluding copies/features/queues. Materialization, shared PCM, and streaming trade-offs are compared without invented benchmarks.
- Correlation supports candidate offsets only with sufficient common audio. Multiple anchors can distinguish offset, drift, and interrupted spans; silence, repeated patterns, and no-common-audio cases need rejection or independent/manual evidence.

Limits: no recordings or runtime measurements were available; corpus compatibility, resource bounds, synchronization accuracy, and seek/resample equivalence remain experimental questions for the existing clock, dataflow, and validation decisions. Architecture and acceptance thresholds remain human choices.

New decision for the coordinator: does the audio-only requirement permit bounded video decoding during metadata probing, or require zero video frames decoded from opening onward? PyAV's current opening path calls FFmpeg stream discovery, which can decode video to determine parameters. The report proposes a narrowly scoped probing-policy experiment if the stricter guarantee is required.
