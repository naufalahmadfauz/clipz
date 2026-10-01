# Define the persistent evidence model and extensible JSON contract

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 10, 11, 12, 13, 14, 15

## Question

What durable analysis model and versioned export contract represent complete evidence without forcing future detectors or clients to rewrite old projects?

Define Project/Source/AudioTrack references; transcript segments and words; stable observation IDs; overlap and chronological ordering; event points/intervals; measurement units; synchronization mappings; identity/attribution; score semantics; model/configuration provenance; processing coverage; and disabled/failed/partial analysis states. Choose exact serialized timing and interval conventions from the clock contract.

Decide extension namespaces, unknown detector/event handling, schema versions and migration/backward-read guarantees, reproducibility metadata, and deduplicated context references. Separate the durable working store/artifacts from a portable full-analysis snapshot when useful; one giant mutable JSON file is not assumed to be the processing database.

Agree examples and validation rules sufficient to hand off a schema design, including re-alignment and future detector additions. Do not implement the final schema or persistence engine during this map.
