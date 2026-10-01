# Choose cache invalidation and resumable job boundaries

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 09, 16, 17

## Question

What artifact identities, dependency edges, and checkpoint semantics make long analyses safely incremental and restartable?

Decide source fingerprinting and relinking, analyzer/model/weight/config/version signatures, chunk identity, completed versus partial artifacts, atomic completion, corrupt/stale cache behavior, interrupted/OOM recovery, and when outputs may be reused. Evaluate whole-track versus chunk checkpoints against context-sensitive inference and boundary reproducibility.

Walk through renaming a track, changing an offset/drift mapping, changing VAD/model/thresholds, adding one detector, replacing a source, changing only an export, and resuming after a Colab reset. Separate media-local evidence from project-time derived artifacts to avoid gratuitous re-inference.

Choose cache/working-store boundaries, retention/cleanup controls, and concurrency/locking expectations. Name the interruption and recomputation experiments required before accepting the design.
