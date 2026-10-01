# Define project, source, track, channel, and speaker identity

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 03

## Question

What domain relationships distinguish a Project, input Source, embedded stream, audio channel, logical AudioTrack, speaker identity, and user track classification?

Walk through the current MP4 plus microphone setup, one file with multiple embedded streams, stereo game audio, dual-mono speakers, multichannel surround, multiple external speakers, and the same voice appearing in several tracks. Decide when a logical track selects a stream, channel subset, or derived mix, how the user confirms intent, and which combinations are initially supported. Never silently treat every channel as a person or every stereo pair as separable speakers.

Agree stable identities, naming versus role/classification, provenance for derived tracks, source replacement/relinking semantics, and how one interrupted recording session refers to multiple source spans. Decide whether users may map several recordings into one logical track or whether that is a later extension. Preserve mixed/unknown identity explicitly.

Update the glossary as terms settle. Leave exact timestamp units, storage schema, and job orchestration to their tickets.
