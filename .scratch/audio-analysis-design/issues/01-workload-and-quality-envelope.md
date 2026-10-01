# Agree the workload, resource, and quality envelope

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none

## Question

What concrete operating envelope and quality trade-offs should the first release be designed for, within the accepted Windows CLI and single-session scope?

Agree typical and upper-bound session duration, simultaneously analyzed speech tracks, source layouts, acceptable processing latency, RAM/VRAM and scratch-disk budgets, and cold versus cached expectations. Use the measured runtime inventory when available rather than assuming every RTX 4060 configuration is identical.

Define which errors matter most: missing versus extra acoustic candidates, Indonesian/code-switched recognition errors, timestamp/synchronization errors, interrupted-job recovery, and compact-export omissions. Distinguish hard acceptance gates, target ranges, and unknowns to measure. The four-hour use case needs concrete criteria, not an invented throughput promise.

This resolves product priorities and resource/quality bounds, not a model or concurrency implementation. Link the later benchmark protocol to these agreed bounds.
