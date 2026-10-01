# Choose acoustic detector candidates and evidence gates

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 05, 10

## Question

Which laughter and yelling/shouting candidates deserve representative evaluation, and what contract and evidence gate should govern each detector's supported, experimental, or deferred status?

Agree the vocalization taxonomy, temporal event versus clip-label behavior, required input context, inference cadence, preprocessing, raw score retention, threshold calibration, provenance, false-positive examples, and performance/license limits. A weakly supervised tag score must not masquerade as a calibrated event probability.

Keep laughter and shouting independently optional and distinguish no event from detector disabled, failed, or unevaluated. Define the metric/annotation evidence required to promote each candidate, including Indonesian/game-audio/Discord conditions.

This selects an evaluation shortlist and interface policy, not an unmeasured accuracy winner. Actual product tiers remain provisional until the resulting experiments and final readiness decision inspect the evidence.
