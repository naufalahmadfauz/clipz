# Set the audio-only discovery and probing boundary

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 03

## Question

Must audio-only processing guarantee zero video frames decoded even while opening and probing a source, or is a strictly bounded metadata-discovery exception acceptable?

[Media timing and decoding evidence](../research/media/research.md) found that PyAV opens through FFmpeg stream discovery, which can decode video frames to determine stream parameters. Selecting audio output or filtering later demux packets does not itself prove zero video decoding during opening.

Preserve the user's requirement until the human explicitly decides otherwise. Compare strict audio-only discovery strategies against a bounded probing exception, including supported containers, incomplete metadata, fallback behavior, resource limits, observability, and the implications for FFmpeg/PyAV selection. Neither option authorizes video feature analysis, rendering, or transcoding.

Record the enforceable guarantee and any narrowly scoped probing experiment needed to establish it on representative containers. This decision constrains the audio dataflow and performance protocol; source-level plausibility alone does not verify the guarantee.
