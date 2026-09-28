# Independent-track transcription: capability evidence

**Researched:** 2026-09-27. **Assigned decision:** [Establish faster-whisper accuracy and throughput controls](https://github.com/naufalahmadfauz/clipz/issues/6). **Scope:** research for the [accepted brief](accepted-brief.md), not a selected transcription policy.

## Evidence and version boundary

GitHub's latest-release endpoints returned **faster-whisper 1.2.1** (2025-10-31) and **CTranslate2 4.8.2** (2026-08-31). Those tags anchor implementation claims below. Faster-whisper permits `ctranslate2>=4.0,<5`; this permits 4.8.2 but does not establish a tested combination on this project's machines. Context7 was used for API discovery, then checked against primary release source. Model cards and vendor pages are observations as of the research date, not pinned model artifacts. [FW-release], [CT-release], [FW-deps]

**Verified** below means documented or visible in source, not executed locally. **Inference** means a consequence for this design. **Missing evidence / proposed experiments** are explicitly unrun. No dependencies, models, or recordings were installed/downloaded, and no local accuracy, speed, or memory measurements were made.

## 1. Standard and batched inference are different policies

Both public `transcribe` methods accept **one** path, binary file-like object, or NumPy waveform, returning `(segments, info)`. Their similar signatures do not imply equivalent decoding. This comparison is verified in `transcribe.py` at 1.2.1. [FW-source]

| Aspect | `WhisperModel.transcribe` | `BatchedInferencePipeline.transcribe` |
|---|---|---|
| Work unit | Sequential windows; advances using decoded timing and, optionally, word alignment | Independently decoded chunks of one supplied waveform; `batch_size=8` default |
| Default VAD | Off; enabling it uses `VadOptions()` | On; default options set 160 ms minimum silence and maximum speech duration to `chunk_length` |
| Context | `condition_on_previous_text=True`; previous output can prompt subsequent windows | Previous-output conditioning forced off; initial prompt reused for each chunk |
| Temperature / failure heuristics | Temperature fallback, compression/log-probability checks, no-speech skipping | First temperature only; compression/log-probability/no-speech thresholds unused |
| Other compatibility arguments | Applies relevant standard decoding options | `prefix`, `prompt_reset_on_temperature`, `max_initial_timestamp`, `hallucination_silence_threshold` unused; `best_of` is stored but not forwarded as hypotheses |
| Timestamp default | `without_timestamps=False` | `without_timestamps=True`; without word alignment, output can describe whole chunks rather than fine decoded boundaries |
| Word timing | Optional cross-attention/DTW alignment | Also available, despite the timestamp-token default |
| Explicit clips | Comma-separated string or flat start/end seconds; bypasses VAD | List of `{"start": seconds, "end": seconds}`; bypasses VAD and automatic chunk merging |

Beam size, patience, length/repetition penalties and token suppression are applied in batching. Batched explicit clips over 30 seconds generate a warning and features are trimmed to the encoder window; they are not automatically fully transcribed. With VAD off and no explicit clips, batching rejects inputs at least `chunk_length` long. These are material limits on “drop-in replacement.” [FW-source], [FW-audio]

**Native batching versus orchestration.** Faster-whisper's public pipeline does not accept a list of files/tracks. CTranslate2 **does** natively accept batched Mel features, per-example prompts, and asynchronous `Whisper.generate`; its feature shape is `[batch_size, n_mels, frames]`. Thus cross-track model batching is technically available at the lower level, while decoding, compatible-feature packing, track IDs, per-track context, language handling, VAD maps, alignment and result routing require application orchestration. Concurrent independent `transcribe` calls are another mechanism, not automatic cross-file batching. Concatenating recordings would create one artificial input and require additional boundary handling. [FW-source], [CT-api]

## 2. Input consumption and bounded-memory implications

**Verified:** file input is eagerly decoded before `transcribe` returns. `decode_audio` uses PyAV, selects `audio=0`, resamples/downmixes to mono by default, buffers decoded samples, and produces normalized float32. It explicitly clears frame PTS while grouping frames. Public transcription exposes no embedded-stream/channel selector; the decoder's separate `split_stereo` helper is not invoked by transcription. These APIs therefore cannot themselves preserve the project's embedded-stream timing contract. [FW-audio], [FW-source]

An ndarray bypasses decoding and resampling: the caller must supply the selected logical AudioTrack as a one-dimensional, appropriately normalized waveform at the extractor's expected rate (normally **16 kHz**). An arbitrary stereo/48-kHz/integer array is not automatically corrected. Standard transcription eagerly extracts the whole supplied waveform's features; batching eagerly runs VAD/chunk collection, extracts all chunk features and stacks them before returning. Language detection can also execute then. The iterator defers segment generation, **not** all preprocessing or GPU activity. [FW-source], [FW-features]

**Arithmetic, not a measurement:** four hours × 16,000 samples/second × four bytes is **921,600,000 bytes (~0.92 GB)** for just one float32 mono waveform. Decoder copies, VAD buffers, STFT intermediates, Mel features and model memory add to that. `batch_size` bounds a model call, not this total host allocation. Memory mapping alone does not eliminate eager feature allocations. **Inference:** bounded long-session memory requires bounded inputs or a deliberate lower-level feature pipeline, with corresponding context/timing tests. [FW-audio], [FW-source], [FW-features]

## 3. VAD, timestamps and confidence semantics

Faster-whisper 1.2.1 bundles **Silero VAD v6**, run with ONNX Runtime's CPU provider. Standard `VadOptions` defaults include threshold 0.5, minimum silence 2,000 ms, speech padding 400 ms, minimum speech duration zero and no finite maximum duration. Batched defaults override silence/max-duration as above; a supplied dictionary and a `VadOptions` instance take different construction paths, so capture effective settings. VAD returns sample-index speech intervals after thresholds/padding, not a transcript, person identity, or calibrated project-specific probability. [FW-release], [FW-vad], [FW-source]

When internal VAD removes gaps, `restore_speech_timestamps` maps segment/word endpoints back to the **original supplied waveform**. Word endpoints use the same retained chunk, selected by the word's midpoint; segment endpoints are then derived from its first/last word. Without words, start/end have separate boundary lookup. Restoration rounds to two decimal places. Explicit batched clips instead carry original offsets and skip this restoration. Do not restore twice. `seek` is an internal feature-position field and is not restored alongside endpoints. [FW-source], [FW-vad]

Whisper timestamp tokens have **20 ms granularity**, not a 20 ms accuracy guarantee. Word timestamps use cross-attention alignment and dynamic time warping, with punctuation merging and duration/boundary heuristics; they are estimates attached to recognized text, not independently verified phonetic boundaries. Word alignment can modify segment bounds. VAD concatenation can join separated speech, so discontinuity-adjacent words and segments bridging silence need explicit validation. [FW-source], [FW-tokenizer]

**Inference for the project timeline:** retain the input chunk's source/sample origin, apply the source-to-project synchronization mapping after local restoration, and preserve overlaps between independently transcribed tracks. This also permits timing-map edits without confusing them with changes to recognition. The library does not establish source PTS, clock drift, or interrupted-recording mappings. [FW-audio], [FW-source]

Keep these outputs semantically distinct:

- `avg_logprob`: generated-sequence score converted to average token log probability.
- `Word.probability`: mean aligned text-token probability for that word.
- `no_speech_prob`: Whisper's no-speech-token probability, **not** Silero's VAD score.
- `compression_ratio`: text repetition heuristic, not probability.
- `language_probability`: language-token score when detected; **hard-coded to 1 when language is supplied**.

These definitions are verified; calibration for Indonesian gaming speech is missing. In particular, neither a word score nor `language_probability=1` proves recognition correctness. Store names, provenance and raw values rather than relabeling them “confidence that this happened.” `duration_after_vad` reports retained duration, not independently verified speech coverage. [FW-source], [CT-api]

## 4. Indonesian, code-switching, context and model candidates

Multilingual tokenizers support Indonesian (`id`) and English (`en`). `task="transcribe"` requests original-language recognition; `translate` requests English translation. Compare fixed `language="id"`, initial automatic detection, and `multilingual=True`, which re-detects per window/chunk. The latter is not word-level language identification or a guarantee of within-sentence code-switch accuracy. Initial automatic detection defaults to one window; additional detection windows/thresholds are configurable. [FW-tokenizer], [FW-source]

Prompts/hotwords are text conditioning, not a forced vocabulary or guarantee of spelling. Standard previous-output conditioning may help continuity but can propagate errors; batching does not carry that history. There is a finite 448-token context/generation budget, and prompt components are truncated. Standard accepts text or token IDs for `initial_prompt`; the batched implementation directly tokenizes it, so its annotated token-ID alternative should not be assumed functional. **Inference:** separate calls need explicit context policy, and one track's recognized text should not silently become another track's history. [FW-source]

Changing external chunk boundaries changes audio context, language detection, prompts, VAD boundaries and even feature normalization: the extractor clips relative to the maximum log-Mel value of the supplied waveform. Therefore chunking is not merely a scheduling optimization. Increasing `chunk_length` does not enlarge Whisper's 30-second encoder receptive field; faster-whisper pads/trims inference features to 3,000 frames. Overlap, ownership of boundary words, deduplication and restart equivalence remain experiments. [FW-features], [FW-audio], [FW-source], [Turbo-card]

| Candidate family, not ranking | Verified suitability boundary | License / provenance |
|---|---|---|
| Multilingual `small`, `medium` | Smaller comparison points, including for CPU; Indonesian supported, adequacy unknown | Original OpenAI weights MIT; inspect the chosen conversion revision |
| `large-v2`, `large-v3` | Multilingual quality comparators; do not assume v3 wins this corpus | Original weights MIT; inspected Systran large-v3 conversion also declares MIT and FP16 storage |
| `large-v3-turbo` / `turbo` | Multilingual; prunes v3 decoder from 32 layers to four; not trained for translation; recognition trade-off unknown | Original and inspected converted card declare MIT; 1.2.1 alias targets `mobiuslabsgmbh/faster-whisper-large-v3-turbo` |
| `.en`, Distil-Whisper `distil-large-v3` / `v3.5` | English models; their English evaluations do not support an Indonesian choice | Distil cards declare MIT; API availability is not target-language validation |

Sources: upstream model documentation, cards and actual alias registry. The mutable Turbo conversion card now shows a `dropbox-dash` example despite the release alias: resolve and record the actual repository/revision, not just `"turbo"`. [Whisper-readme], [Large-card], [Turbo-card], [Turbo-conversion], [Distil-v3], [Distil-v35], [FW-models]

OpenAI documents hallucination, repetition and uneven performance across languages/dialects. No reviewed primary source establishes accuracy for this user's slang, profanity, gaming terms, Discord compression or overlapping voices. Faster-whisper's default suppressed tokens concern symbols/non-speech annotations, not an explicit profanity blacklist; that does not establish faithful profanity recognition. [Whisper-card], [FW-tokenizer]

**Diarization boundary:** returned `Segment`/`Word` records contain no speaker identity. Track attribution belongs to the caller. A mixed Discord AudioTrack remains mixed/unknown unless a separately justified process supplies speaker evidence; independent tracks acquire no mandatory diarization dependency. Transcribed laughter-like text likewise is not acoustic laughter detection. [FW-source], [Whisper-card]

## 5. Runtime, compute types and memory constraints

### Current CUDA/cuDNN evidence corrects stale guidance

The 1.2.1 README says CUDA 12/cuBLAS and cuDNN 9; CTranslate2's tagged installation page still says cuDNN 8. Neither sentence alone accurately describes current build intent. CTranslate2 4.5 moved to cuDNN 9; **4.6.3 added native CUDA convolution, making cuDNN optional**. Both **4.8.2 Windows and Linux x86-64 wheel scripts build with CUDA 12.8 and `WITH_CUDNN=OFF`**. CMake selects native CUDA convolution in that case. [FW-readme], [CT-install], [CT-changelog], [CT-windows], [CT-linux], [CT-cmake]

Important qualification: the Windows script still copies `cudnn64_9.dll` into the package, and package initialization preloads packaged DLLs. Optional convolution backend does not mean “no cuDNN DLL is packaged or loaded.” **Missing evidence:** exact wheel imports, DLL resolution, CUDA inference and word alignment on the user's Windows installation and a fresh T4 runtime. The release source establishes build configuration, not a completed deployment smoke test. CUDA driver/library compatibility must be checked for the pinned artifact; NVIDIA documents restrictions on minor-version compatibility. [CT-windows], [CT-init], [NVIDIA-compat]

Upstream specifies Python >=3.9, Windows x86-64/Linux wheels, and the Visual C++ runtime on Windows. CPU execution is available without a CUDA device; its usable model/profile remains unmeasured. [FW-readme], [CT-install]

| Target | Hardware/documented compute candidates | Qualification |
|---|---|---|
| RTX 4060 | Compute capability 8.9; FP32, FP16, INT8 mixed FP32/FP16; BF16 variants supported by CT2's capability table | NVIDIA desktop specification is 8 GB VRAM; actual free memory/environment unmeasured |
| T4 | Capability 7.5; FP32, FP16, `int8_float16` / `int8_float32` | No native BF16 profile; nominal 16 GB is not usable-free-memory evidence |
| CPU | FP32 and INT8/`int8_float32`; Intel/MKL also has INT16 support | Prebuilt CPU fallback table converts FP16/BF16 to FP32; CPU and thread budget unknown |

Sources: NVIDIA hardware specifications and CTranslate2 quantization tables. BF16 availability does not make it fastest or highest quality. `int8` leaves nonquantized operations in a floating type; it does not make all allocations eight-bit. `default` depends on stored precision and `auto` on runtime capabilities. Proposed diagnostics are `ctranslate2.get_supported_compute_types("cuda", 0)` / `("cpu")` and the loaded model's `compute_type`; none was executed here. [NVIDIA-cc], [NVIDIA-4060], [NVIDIA-T4], [CT-quant], [CT-types], [CT-api]

`num_workers` maps to CT2 `inter_threads`; CPU threads map to `intra_threads`. Concurrent workers on one device share weights but add active execution/cache memory, and upstream explicitly says extra CUDA streams may not improve throughput. Queue controls do not bound faster-whisper's eager preprocessing. A batched pipeline also owns mutable `last_speech_timestamp`, reset on normal iterator exhaustion; custom standard `chunk_length` mutates extractor state. **Inference:** concurrent reuse/cancellation needs lifecycle tests, not an assumption of reentrancy. [FW-source], [FW-features], [CT-parallel], [CT-api]

No reviewed API promises automatic OOM-to-CPU recovery. Model size, precision, beam width, batch size, alignment and simultaneous workloads need a measured memory envelope. Colab neither guarantees a T4 allocation nor stable session resources. Published faster-whisper benchmark figures concern different hardware/settings/corpora, including 1.1.0 on a 3070 Ti; they do not predict this project's speed or memory. [FW-source], [FW-readme], [Colab]

Faster-whisper, CTranslate2 and Silero declare MIT; that does not license every bundled runtime dependency. Preserve model conversion provenance and notices: faster-whisper's model-download allowlist does not include license files. Binary redistribution belongs with the runtime/distribution decision. [FW-license], [CT-license], [Silero-license], [FW-models]

## 6. Missing evidence and proposed contrasts — all unrun

No material external-research blocker remains. Runtime/corpus evidence remains a prerequisite for choosing profiles and claiming support. These contrasts inform the Wayfinder decisions on transcription policy, bounded decoding and scheduling, cache/resume boundaries, distribution, and validation; they do not resolve them:

1. **Recognition:** human-annotated Indonesian/code-switch clips spanning clean microphone, mixed Discord, gaming noise, short interjections, slang/profanity, overlap and silence/music negatives. Compare agreed multilingual model candidates using explicit normalization rules, WER/CER, term recall, hallucinated insertions and deletions. Set acceptance thresholds with the human.
2. **Inference semantics:** standard versus batched, including batched size one; separate default-policy comparison from controlled VAD/clips/settings comparisons. Contrast fixed `id`, initial detection and per-window detection, prompts off/on, standard history off/on, and beam widths. Check whether faster output simply omitted speech.
3. **Timing/coverage:** word timing off/on; VAD off/default/tuned; leading/trailing silence, brief words, speech near removed gaps and known external chunk offsets. Measure annotated endpoint error and omissions; verify local restoration before project drift/offset mapping. Explicit clips must stay within supported windows.
4. **Chunk/restart behavior:** bounded chunks with candidate overlap/context versus continuous reference; quantify lost/duplicated boundary words. Compare uninterrupted completion with resumed chunks, and cancel a reused batched iterator before transcribing another track to test state isolation against a fresh pipeline.
5. **Performance/runtime:** CPU, actual 4060 and available T4; FP16 versus INT8 GPU and FP32 versus INT8 CPU; batch-size/worker contrasts within observed memory limits. Record cold/warm decode, VAD, feature, language-detection, ASR and alignment times, total wall time, audio-track hours, peak RSS/VRAM, cancellation and four-hour scaling. Consume the iterator fully. Record runtime/library versions, effective options, model revision and available hardware.

**New decision question:** none required beyond the existing map's policy, dataflow, cache, distribution and validation questions. The newly specific cancellation/state-isolation and VAD-discontinuity probes should be incorporated into their experiments rather than duplicate policy tickets.

## Primary sources

Inline source links use **FW** for faster-whisper release source, **CT** for CTranslate2 release source, and publisher/model names for first-party model cards and hardware/service documentation. Library links are version-tagged; mutable cards/vendor pages were accessed on 2026-09-27.

[FW-release]: https://github.com/SYSTRAN/faster-whisper/releases/tag/v1.2.1
[CT-release]: https://github.com/OpenNMT/CTranslate2/releases/tag/v4.8.2
[FW-deps]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/requirements.txt
[FW-source]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/transcribe.py
[FW-audio]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/audio.py
[FW-features]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/feature_extractor.py
[FW-vad]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/vad.py
[FW-tokenizer]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/tokenizer.py
[FW-models]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/faster_whisper/utils.py
[FW-readme]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/README.md
[CT-api]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/python/cpp/whisper.cc
[CT-install]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/docs/installation.md
[CT-changelog]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/CHANGELOG.md
[CT-windows]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/python/tools/prepare_build_environment_windows.sh
[CT-linux]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/python/tools/prepare_build_environment_linux.sh
[CT-cmake]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/CMakeLists.txt
[CT-init]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/python/ctranslate2/__init__.py
[CT-quant]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/docs/quantization.md
[CT-types]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/python/cpp/module.cc
[CT-parallel]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/docs/parallel.md
[Whisper-readme]: https://github.com/openai/whisper/blob/main/README.md
[Whisper-card]: https://github.com/openai/whisper/blob/main/model-card.md
[Large-card]: https://huggingface.co/Systran/faster-whisper-large-v3/blob/main/README.md
[Turbo-card]: https://huggingface.co/openai/whisper-large-v3-turbo/blob/main/README.md
[Turbo-conversion]: https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo/blob/main/README.md
[Distil-v3]: https://huggingface.co/distil-whisper/distil-large-v3/blob/main/README.md
[Distil-v35]: https://huggingface.co/distil-whisper/distil-large-v3.5/blob/main/README.md
[NVIDIA-cc]: https://developer.nvidia.com/cuda-gpus
[NVIDIA-4060]: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4060-4060ti/
[NVIDIA-T4]: https://www.nvidia.com/en-us/data-center/tesla-t4/
[NVIDIA-compat]: https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html
[Colab]: https://research.google.com/colaboratory/faq.html
[FW-license]: https://github.com/SYSTRAN/faster-whisper/blob/v1.2.1/LICENSE
[CT-license]: https://github.com/OpenNMT/CTranslate2/blob/v4.8.2/LICENSE
[Silero-license]: https://github.com/snakers4/silero-vad/blob/master/LICENSE
