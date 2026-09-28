# Accepted brief: audio-first gaming analysis

This is the charting baseline accepted by the user, recorded on 2026-09-27, not a resolved implementation specification. Architecture proposals below remain hypotheses until their decision tickets resolve.

## Product and workflow

Design an open-source, local analysis application inspired by AegEdits but with a much narrower purpose: produce evidence from long gaming recordings, not edited media. The user manually uploads analysis data to ChatGPT Chat for semantic/funny-moment interpretation and performs editing in Adobe Premiere Pro. Avoid API costs intentionally; no ChatGPT/OpenAI API integration.

The destination is a technical/product design sufficiently resolved for `/to-spec`, with no fundamental architecture questions outstanding and representative validation of architecture-critical assumptions.

## Recordings and tracks

- Current input: one MP4 containing video plus game/Discord audio, and a separate microphone recording.
- Required design space: multiple embedded audio streams, multichannel audio, arbitrary external WAV/MP3/M4A/FLAC recordings, and combinations of these.
- Represent selected audio as logical AudioTracks regardless of origin. Users can name/classify them, for example Nau, Friend A, Discord, Game, or Unknown. Distinguish a speaker identity from a mixed track or a source channel.
- Each project is one recording session on a continuous project timeline. Sources can start late, end early, or contain gaps. Investigate clock drift and interrupted recordings within that model.
- Preserve embedded-stream source timing. Support explicit/manual offsets at minimum; investigate waveform synchronization when recordings share enough audio.
- Choose a high-precision canonical project-time representation. Do not hardcode a frame rate; generate editor-specific timecodes only using the actual target frame rate and sequence timing.

## Transcription

- Prefer faster-whisper, with NVIDIA CUDA acceleration and CPU fallback.
- Independently transcribe relevant speech tracks; retain segment timestamps and preferably word timestamps.
- Handle Indonesian and mixed Indonesian/English gaming terminology, slang, and profanity.
- Investigate model choice, compute types, batching, VAD, decoding/chunking effects, and memory/throughput trade-offs.
- Merge observations chronologically without discarding overlapping speech or confusing track identity with speaker certainty.
- Separate speaker tracks do not need diarization. Whether mixed Discord audio needs diarization remains open.

## Acoustic evidence

- Required first-release baseline: transcription plus useful loudness and relative-volume-spike evidence.
- Investigate RMS and/or LUFS, relative rather than only absolute loudness, silence followed by energy bursts, and simultaneous reactions across tracks.
- Evaluate real acoustic laughter and yelling/shouting detection rather than interpreting Whisper's text as acoustic proof.
- Decide supported, experimental, or deferred status from evidence. Record detector provenance, confidence/strength semantics, and timestamped evidence. Do not treat arbitrary model scores as calibrated probabilities.
- Preserve raw evidence and analysis limitations; do not make irreversible decisions about humor.

## Engine and performance

- Several-hour recordings, including a representative four-hour case, motivate bounded memory and efficient media handling.
- Investigate minimizing decode passes, PCM sharing/materialization/streaming, concurrent CPU analysis and GPU inference, batching, restartability, cache invalidation, and incremental recomputation.
- Avoid unnecessary intermediate MP3 encodes, video decoding, and all video rendering/transcoding.
- The hypothesis is: discovery -> logical tracks -> synchronization -> decode/audio pipeline -> analyzers -> unified evidence timeline -> persistent/cacheable model -> exports. Challenge this if the evidence warrants it.
- Python is preferred for the ML/audio ecosystem; a language switch needs a material measured benefit.

## Data and exports

- Full machine-readable analysis, conceptually `project.analysis.json`: project and source metadata, track definitions, synchronization/offsets, transcripts and word/segment timing, identity/provenance, acoustic events, scores, and context references.
- Extensible, versioned schema that accommodates new event detectors without breaking old projects.
- Investigate a compact LLM-oriented export, with candidate/event-rich regions and nearby transcript context, alongside complete evidence. A four-hour recording should not become needlessly repetitive or enormous.
- Investigate readable merged transcripts, SRT/VTT, CSV, and Premiere-compatible marker interchange, including selected timestamps returned from a manual ChatGPT interaction.
- Semantic humor analysis stays with the human's ChatGPT workflow. Acoustic candidate generation must remain transparent and reversible.

## Targets and audience

- First release: Windows CLI, headless reusable core, user's RTX 4060 and CPU fallback.
- Future GUI boundary and concrete Colab/T4 compatibility contract plus validation plan are part of the design. GUI and notebook implementations are later.
- Initial users are the author and technical early adopters. Reproducible Python/CUDA setup is acceptable; investigate licenses, binary dependencies, and future redistribution obstacles.

## Evidence before handoff

The user permits narrow disposable experiments that resolve decisions, not application implementation. Obtain suitable representative recordings and runtime information as an explicit prerequisite. Validate architecture-critical assumptions before `/to-spec`; define the broader quality/performance acceptance suite for implementation.

Exact resource budgets, acceptable recognition/detection errors, synchronization tolerances, and benchmark thresholds have not yet been agreed. Research may propose options but cannot decide the human's preferences or claim measurements that were not made.
