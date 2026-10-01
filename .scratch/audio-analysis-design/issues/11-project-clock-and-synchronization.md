# Choose the project clock and synchronization contract

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 03, 10

## Question

How are original stream/sample times mapped to one canonical project timeline without losing precision, offset direction, drift, or gaps?

Choose a precision/round-trip policy for seconds, integer ticks, sample positions, or rational times, with explicit conversions and interval endpoint semantics. Define project zero, manual positive/negative offsets, embedded PTS/time-base/start handling, nonzero source starts, unequal durations, interrupted source spans, and provenance of user adjustments.

Decide the initial synchronization promise: constant offsets, optional waveform alignment with accept/reject feedback, drift measurement/correction, and piecewise mapping if warranted. Handle no-common-audio, repeated/ambiguous patterns, uncertain matches, and gain/compression differences. Keep measurement uncertainty distinct from model confidence. A global "synchronized" flag is insufficient for partially aligned sources.

Specify how changing alignment updates project-time views and invalidates only genuinely time-dependent results. Identify representative timing experiments required to validate the proposed contract; final editor timecode conversion belongs at export.
