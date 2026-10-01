# Decide whether mixed-track diarization belongs in the first release

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 04, 10

## Question

Does identifying individual voices within a mixed Discord track add enough value to justify a first-release diarization path, or should that track remain explicitly mixed/unknown?

Distinguish known track attribution, anonymous diarization clusters, named people, overlapping speech, and source separation. Consider the user's real source layout and whether uncertain cluster identity would mislead downstream ChatGPT analysis. Independent known-speaker tracks must not acquire a mandatory diarization dependency.

If diarization is deferred, settle the extension and uncertainty boundary. If it is wanted, graduate focused model/license/runtime research and corpus validation before selecting a dependency or claiming support; wire those tickets into affected architecture and readiness decisions.
