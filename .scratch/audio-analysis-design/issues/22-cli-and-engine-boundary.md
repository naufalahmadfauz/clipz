# Define CLI workflows and the reusable engine boundary

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 09, 10, 16, 18, 19, 20, 21

## Question

What user workflow and headless public boundary support discovery, track configuration, synchronization, analysis, restart, and exports from a Windows CLI while remaining reusable by a future GUI and Colab notebook?

Agree command responsibilities and project/config ownership rather than prematurely committing to a command parser library. Cover selecting/naming/classifying streams and channels, setting/previewing offsets, editing analyzer profiles, progress and diagnostics, partial failures, cancellation/resume, export/re-export, and actionable CUDA/CPU capability reporting.

Choose the engine's request/result/progress/cancellation boundary and the small set of persistent user concepts. Keep UI interaction, Windows-specific process concerns, file selection, and notebook conveniences outside reusable analysis policy. Define where interactive confirmation is required and how headless invocations remain reproducible.

Consult `codebase-design`. If the workflow cannot be evaluated verbally, graduate a disposable HITL CLI/storyboard prototype rather than implementing commands.
