# Establish useful loudness, spike, and reaction evidence

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-remaining-research
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-loudness
Research worktree: ../research/loudness
Research asset: [Loudness and reaction evidence](../research/loudness/research.md)

## Question

Which low-cost signal measurements and baseline methods are defensible for useful loudness, relative spikes, silence-to-energy transitions, and simultaneous reactions across gaming audio tracks?

Compare windowed RMS/dBFS, peak/clipping, and momentary/short-term/integrated LUFS using standards and library docs. Identify sample-rate/channel handling, gating, bounded-memory incremental computation, adaptive robust baselines, silence floors, hysteresis, attack/release, event merging, and gain/AGC changes. Distinguish silence detection from speech VAD and energy from shouting or humor.

Explain cross-track coincidence limitations when the same game/Discord mix bleeds into several recordings, and how sync uncertainty limits coincidence precision. Identify plausible implementation primitives and their licenses, but do not choose thresholds or claim event quality without representative measurements.

## Answer

[Loudness and reaction evidence](../research/loudness/research.md), retrieved 2026-09-27, distinguishes RMS/peaks from the 400 ms ungated momentary, 3 s ungated short-term, and two-stage-gated integrated measurements in current ITU/EBU standards. Incremental primitives are available, but integrated history, channel layouts, filter continuity and histogram approximation require explicit contracts. Robust baselines, hysteresis and silence-to-energy rules are proposed heuristics, not validated reaction detectors. Coincident events can be duplicate game/Discord audio; independent reactions require provenance and synchronization-aware validation. Thresholds, event quality and implementation choice remain with the existing human decisions and unrun experiments.
