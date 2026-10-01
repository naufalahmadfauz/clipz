# Establish faster-whisper accuracy and throughput controls

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-transcription-research
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-transcription
Research worktree: ../research/transcription
Research asset: [Transcription capability evidence](../research/transcription/research.md)

## Question

Which current faster-whisper/CTranslate2 APIs and model/runtime choices are credible candidates for independent-track Indonesian/code-switched transcription on Windows RTX 4060, CPU fallback, and Colab T4?

Verify CUDA/cuDNN and compute-type support; model/language limitations; VAD defaults and timestamp restoration; word and segment timestamps; batched versus ordinary inference semantics; ndarray/file input and eager/lazy decoding; external chunking/context/prompt behavior; and GPU memory/concurrency implications. Clarify whether batching across separate tracks is supported directly or needs orchestration.

Distinguish language support from demonstrated slang/profanity accuracy, upstream benchmark claims from local measurements, and VAD/ASR scores from calibrated confidence. Do not select a winner or promise real-time performance without corpus evidence. Identify experiment contrasts and any model/weight licenses relevant to the shortlist. Establish the diarization boundary without presuming a diarization dependency.

## Answer

Resolved 2026-09-27: [Transcription capability evidence](../research/transcription/research.md), anchored to faster-whisper 1.2.1 and CTranslate2 4.8.2 release source.

Verified capabilities include materially different standard/batched decoding, eager audio/features despite lazy segment generation, VAD/word timestamp restoration, native CT2 feature batching versus application-owned cross-track orchestration, Indonesian/model/license boundaries, hardware compute types, and absence of built-in speaker attribution. Current CT2 wheel build scripts use CUDA 12.8 with the cuDNN backend disabled; the report records conflicting older documentation and the remaining Windows bundled-DLL caveat.

**Evidence boundary:** no corpus, deployment, quality, throughput or memory tests were run. Model/settings choices, calibrated confidence, supported runtime profiles and performance claims remain unresolved. The report proposes recognition, VAD/timing, chunk/context, cancellation-state and CPU/4060/T4 contrasts for [Choose the transcription, language, and inference policy](12-transcription-policy.md), [Choose bounded audio decoding, PCM sharing, and scheduling](16-audio-dataflow-and-scheduling.md), [Choose cache invalidation and resumable job boundaries](18-cache-and-resume-contract.md), [Choose reproducible distribution and Colab compatibility](23-distribution-and-colab-contract.md), and [Set benchmark protocols and architecture-validation gates](24-benchmark-and-validation-protocol.md). No material external-research blocker or additional policy ticket was identified.
