# Choose reproducible distribution and Colab compatibility

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 09, 12, 13, 15, 16, 22

## Question

What install, runtime capability, dependency, and model-artifact contract is realistic for technical Windows users and portable to Colab/T4?

Choose supported Python/platform profiles, CPU versus CUDA dependency paths, reproducible environment strategy, FFmpeg/PyAV distribution strategy, model acquisition/cache/offline semantics, version/provenance reporting, and setup diagnostics. Resolve code/model/binary licensing suitability for the selected candidates, separating local use from future redistribution.

Choose the application's open-source license and the notices/artifact-provenance policy. Verify model-weight permissions independently of code licenses, including any unresolved candidate terms identified by acoustic research; a dependency's permissive source license does not decide the application's license or license every bundled artifact.

Specify a T4-compatible runtime profile and validation plan, GPU-unavailable behavior, ephemeral versus persisted storage boundaries, resume/export behavior after runtime loss, and absence of Windows UI assumptions. Do not guarantee a particular Colab allocation or ship a notebook as part of this decision.

Identify smoke-test and representative runtime evidence needed to support the compatibility claim. Defer a nontechnical installer while recording constraints that would make later packaging difficult.
