# Choose readable transcript and tabular export semantics

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 12, 13, 17

## Question

Which readable merged/per-track transcripts, SRT/VTT, and CSV views should be supported, and what can each represent faithfully?

Decide chronological ordering, speaker versus track labels, simultaneous dialogue, segment/word timing, point/interval event representation, Unicode Indonesian text, escaping, and local/project time references. Resolve whether subtitles are per track, merged, or both and explicitly represent format limitations rather than flattening overlapping evidence in the canonical data.

Define the minimal first-release exports, their relationship to the full JSON evidence, and representative fixtures for Unicode, overlap, long duration, gaps, and nonzero offsets. Caption export is optional evidence interchange, not a burned-in-caption or automatic editing feature.
