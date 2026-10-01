# Set benchmark protocols and architecture-validation gates

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 02, 16, 18, 19, 21, 23, 26

## Question

Which concrete experiments, metrics, and pass/revise criteria are sufficient to validate the proposed architecture before `/to-spec`, and which broader checks become implementation acceptance criteria?

Use the actual corpus and inventory. Specify cold/warm and CPU/4060/T4 comparisons where available, audio hours versus wall time, stage timings and decode passes, CPU/GPU utilization, peak RAM/VRAM, scratch space, cache hits, interruption/restart cost, and four-hour scaling. Distinguish measured hardware from estimated or unavailable targets.

Define recognition metrics with Indonesian/code-switching annotation policy; word/segment timing and drift/gap checks; laughter/shouting precision/recall and temporal tolerance; useful loudness-event cases; shared-audio coincidence false positives; compact-export size/coverage; and actual Premiere marker placement. Separate architecture feasibility gates from detector promotion gates and optional integrations.

Resolve by agreeing the minimum decision-relevant experiment set, comparison configurations, fixtures, budgets, and thresholds. Create each newly specifiable probe/measurement/HITL review as a child ticket and wire it into the affected follow-up decisions and the final readiness gate before closing this ticket. Do not run the whole suite or produce application code as part of this conversation.
