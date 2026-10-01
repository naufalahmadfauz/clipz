# Choose the Premiere marker round-trip contract

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 08, 11, 17, 19

## Question

What is the smallest verified manual workflow for turning selected project-time points/windows into useful Premiere markers, and is import back into this tool worthwhile initially?

Choose the interchange mechanism based on established Premiere capabilities and the user's actual workflow. Specify sequence versus clip anchoring, target frame-rate rational, sequence start timecode, drop-frame display, rounding, duration markers, labels/notes/IDs, duplicate import behavior, and any required manual or extension step.

Define the accepted selected-window data returned or manually copied from ChatGPT without relying on an API. Decide what validation catches malformed, out-of-range, overlapping, or wrong-origin timestamps. Marker interoperability may be optional or deferred if the necessary workflow is disproportionate, but the decision and future boundary must be explicit.

Require a real Premiere import/display check using a small known-timing fixture before claiming compatibility. Keep canonical analysis timestamps independent of editor frame assumptions.
