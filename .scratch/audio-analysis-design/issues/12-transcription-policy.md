# Choose the transcription, language, and inference policy

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 04, 10

## Question

Which faster-whisper model/compute profiles and inference policies should be compared and provisionally supported on RTX 4060, CPU fallback, and T4?

Decide per-track speech selection, Indonesian versus automatic language handling, code-switched gaming vocabulary, prompts/hotwords where supported, VAD behavior, segment/word timing requirements, external chunk context/overlap, batching policy, and deterministic configuration provenance. Distinguish safe defaults from expert overrides and define OOM/fallback behavior without silently changing the meaning of cached results.

Require independent attribution for known-speaker tracks and preserved overlaps in the merged conversation. Define uncertain/no-speech output and score semantics. Reference representative quality and speed comparisons before treating a provisional configuration as evidence-backed. Do not take upstream throughput figures as this application's acceptance criteria.
