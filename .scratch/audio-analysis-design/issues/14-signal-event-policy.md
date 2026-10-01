# Choose loudness, spike, silence, and coincident-reaction semantics

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 06, 10, 11

## Question

Which signal measurements and event definitions constitute the useful, required non-transcription baseline?

Choose proposed RMS/dBFS and/or LUFS measurements, analysis windows, track/channel aggregation, relative baseline adaptation, minimum silence/energy conditions, hysteresis, event merging, and score units. Distinguish retained raw/summary measurements from derived events, including configurable or recalculable thresholds.

Decide whether cross-track coincidence is useful enough for the first release, how alignment uncertainty is handled, and how shared/mirrored audio or bleed avoids being counted as several independent reactions. Preserve game-audio spikes as classified evidence rather than labeling them as people yelling.

Specify failure examples and threshold-calibration experiments. Preserve the distinction between signal strength, detector score, and confidence; do not assign synthetic probabilities to deterministic measurements.
