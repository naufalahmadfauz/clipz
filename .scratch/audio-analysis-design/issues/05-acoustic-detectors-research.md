# Establish credible acoustic laughter and shouting options

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-remaining-research
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-acoustics
Research worktree: ../research/acoustics
Research asset: [Acoustic detector evidence](../research/acoustics/research.md)

## Question

Which available acoustic models can plausibly detect laughter and yelling/shouting in Indonesian gaming recordings, and what evidence would distinguish supported, experimental, or unsuitable candidates?

Inspect a small credible shortlist using primary model cards, taxonomy files, source, papers, and separate code/weight licenses. Verify actual laughter/shout/scream classes, clip versus frame outputs, input sample rates/channels/context, temporal resolution, offline inference feasibility, CPU/GPU dependencies and memory implications, score semantics, and release/maintenance facts.

Consider speech-independent acoustic evidence, game-audio/music false positives, vocalizations versus excited speech, Discord compression, overlapping people, and domain/language shift. Do not equate a label in AudioSet or high model score with reliable event localization or calibrated probability. Recommend comparisons and reference annotation needs; leave product inclusion and thresholds to HITL decisions and measurements.

## Answer

[Acoustic detector evidence](../research/acoustics/research.md), retrieved 2026-09-27, establishes YAMNet and PANNs DecisionLevelMax as plausible laughter/shout/scream comparators, plus a conditional specialized laughter candidate. It verifies actual taxonomies, input/context and score timing, Windows runtime constraints, and separate code/weight evidence. PANNs' nominal 10 ms output is interpolated from a coarser grid; its deposited weights are CC BY 4.0 despite MIT code. Exact YAMNet and specialized-checkpoint weight-license coverage remains a documented pre-distribution check. Corpus accuracy, calibration, timing/runtime tests, thresholds and product tiers remain unrun or human decisions; the research does not claim support.
