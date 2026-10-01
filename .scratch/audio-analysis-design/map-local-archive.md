# Audio-first gaming analysis: a design ready for /to-spec

> Historical local snapshot. The live map is [Audio-first gaming analysis: a design ready for /to-spec](https://github.com/naufalahmadfauz/clipz/issues/2). The conventions and statuses below describe the pre-migration state.

Labels: wayfinder:map
Status: open

## Destination

A sufficiently resolved technical/product design for a local, audio-first gaming-recording analyzer that can be handed to `/to-spec` with no fundamental architecture questions remaining. Architecture-critical assumptions must be supported by representative evidence before handoff.

## Notes

- Planning only. Narrow, disposable experiments may resolve decisions; production implementation follows the map.
- [Accepted product brief](brief.md) records the original requirements and the human's charting answers. [Domain glossary](../../CONTEXT.md) records settled terminology.
- One project is one recording session on a continuous timeline. Investigate clock drift, late starts, unequal durations, gaps, and interrupted recordings within that boundary.
- Windows CLI first, headless Python preferred, RTX 4060 primary and CPU fallback required. Specify Colab/T4 compatibility and validation; GUI and notebook implementations are later work.
- Initial audience: the user and technical early adopters. Require reproducible setup and investigate dependency, model-weight, and redistribution licensing.
- Transcription plus useful loudness/relative-spike analysis are required. Acoustic laughter and yelling are evidence-gated into supported, experimental, or deferred tiers. Scores are not automatically calibrated probabilities.
- The user manually uploads exported data to ChatGPT and edits in Premiere. Preserve evidence; compact exports must make their coverage and omissions inspectable.
- Every working session loads `wayfinder`. Grilling sessions also load `grilling` and `domain-modeling`; architecture/interface decisions consult `codebase-design`. Research agents load `research` and use Context7 plus primary sources for current library/API facts.
- Use the [local tracker conventions](tracker.md). Open work is discovered from child issues; the next ticket is the lowest-numbered open, unclaimed child with all blockers resolved. Claim before working. Refer to issues by title.
- Resolve at most one non-research ticket per working session. HITL questions require the human's answers. Initial charting resolves no HITL tickets.
- Research assets live in isolated local worktrees on `research/audio-analysis-*` branches, linked by their tickets. They remain uncommitted working files until a commit is requested; preserve the worktrees and reports.
- External research establishes capabilities and constraints, not measured project performance. No real recording measurements have been taken at charting time.
- New experiments block the decisions that accept their results and the final readiness gate. A policy may resolve provisionally to define an experiment; if the experiment depends on that policy, create a validation/follow-up decision rather than a backward dependency cycle. Re-read affected files before editing because other sessions may be working concurrently.

## Decisions so far

<!-- One gist and named link per resolved ticket. The resolution itself lives in the ticket. -->

- [Establish media timing, decoding, and synchronization capabilities](issues/03-media-timing-and-decoding-research.md): Incremental audio decoding is feasible; source-time spans, eager ASR loading, drift/gaps, and common-audio alignment need explicit handling and validation.
- [Establish faster-whisper accuracy and throughput controls](issues/04-transcription-capabilities-research.md): Release-source evidence establishes multilingual ASR options; batching changes semantics, preprocessing is eager, and timing/orchestration remain application responsibilities.
- [Establish credible acoustic laughter and shouting options](issues/05-acoustic-detectors-research.md): YAMNet, temporal PANNs, and a specialized laughter comparator offer testable options; score calibration, localization, runtime fit, and weight licenses need separate evidence gates.
- [Establish useful loudness, spike, and reaction evidence](issues/06-loudness-and-reactions-research.md): Incremental RMS/peak and LUFS primitives are available; relative-spike heuristics and cross-track independence require separate validation.
- [Establish manual ChatGPT upload and context constraints](issues/07-manual-chatgpt-export-research.md): Upload capacity is not exhaustive semantic coverage; compact evidence needs stable references, explicit omissions, and access to complete chronological speech.
- [Establish Premiere marker and timestamp interchange options](issues/08-premiere-interchange-research.md): UXP marker APIs and legacy sequence interchange offer testable paths; arbitrary CSV import and real-version/timecode round-trip compatibility are not established.
- [Establish reproducible Windows and Colab runtime constraints](issues/09-runtime-distribution-research.md): Reproducible environment profiles, model identities, runtime-specific GPU checks, artifact licensing and durable Colab checkpoints need explicit contracts.

## Not yet specified

- Concrete experiments and resulting design revisions: which source layouts, model variants, detector thresholds, pipeline alternatives, and recovery boundaries merit comparison will become clear from the operating envelope, corpus, research, and proposed policies. Graduate narrowly scoped experiments once their exact contrasts and success conditions are known.
- Unanticipated timing and provenance cases exposed by real recordings: the known drift/gap problem has a ticket; any new failure modes found in the corpus may require additional decisions.
- Additional model sourcing or adaptation if available acoustic models fail the agreed evidence gates; similarly, any diarization-model investigation depends on deciding that mixed-track identity is worth pursuing.
- Changes to compact-export coverage or human review prompted by representative upload/review trials; the initial export policy has a ticket, but the specific usability failures are not known yet.
- Architecture revisions triggered by measured throughput, memory, scratch-storage, cancellation, or resume behavior. Published upstream benchmarks cannot determine those revisions in advance.

## Out of scope

- Production application implementation and writing the final spec during this map; the destination is the evidence-backed design handed to `/to-spec`.
- Automatic video editing, rendering/transcoding, final MP4 highlights, reframing, vertical conversion, burned-in captions, thumbnails, montages, and TikTok/Reels generation.
- Visual/action analysis and video-decoding passes for evidence generation. The newly exposed metadata-probing constraint needs an explicit decision; no exception to the user's audio-only requirement has been approved.
- OpenAI/ChatGPT API integration, cloud LLM calls, and local semantic humor scoring. Lightweight acoustic candidate generation remains a design question.
- Replacing Premiere Pro, or modeling arbitrary edited sequences with cuts, speed changes, and multiple recording sessions.
- Shipping a desktop GUI, a Colab notebook, or a nontechnical one-click installer in the first release. Their relevant engine, compatibility, and future-distribution boundaries remain in scope.
