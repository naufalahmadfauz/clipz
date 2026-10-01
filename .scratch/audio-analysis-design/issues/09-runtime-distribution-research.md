# Establish reproducible Windows and Colab runtime constraints

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-coordinator-recovery
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-runtime
Research worktree: ../research/runtime
Research asset: [Runtime and distribution evidence](../research/runtime/research.md)

## Question

What packaging and execution constraints should a headless Python audio/ML application respect for reproducible Windows NVIDIA/CPU setup and later Colab T4 use?

Investigate Python/platform wheel compatibility, virtual-environment/lock and optional-extra strategies, native decoder/GPU libraries, driver versus runtime responsibility, model download/cache/offline behavior, and actionable capability detection. Avoid assuming that PyTorch CUDA availability establishes CTranslate2 readiness.

For Colab, establish current GPU availability limitations, runtime reset/session/storage constraints, persistent artifact implications, and host-independent CLI/core boundaries. Separate a T4 compatibility contract from a guarantee that Colab allocates a T4.

Record code, model-weight, and FFmpeg-build distribution obligations separately; identify unresolved licensing checks instead of offering legal guarantees. Compare technical-user distribution paths without designing a one-click GUI installer. Coordinate cross-references to the media/model research rather than declaring a universally valid pinned dependency matrix prematurely.

## Comments

2026-09-27: The research-agent launch repeatedly returned a usage-limit error. The coordinating session reclaimed this still-unfinished investigation after verifying that no runtime report had been saved. Primary-source research continues directly; this is an execution fallback, not a change to the product scope or a claim that the delegated pass completed.

## Answer

Resolved 2026-09-27 by the coordinating session's documented quota-recovery fallback. [Runtime and distribution evidence](../research/runtime/research.md) compares pinned/hashed pip profiles and uv lock/extra workflows, identifies Python/native-wheel constraints, and separates drivers, runtime libraries, models, decoder builds and application caches.

PyAV 18.1.0 requires Python >=3.11; the complete optional-profile wheel intersection still needs selection and smoke testing. Current CT2 wheel-source findings differ from older cuDNN installation prose, so runtime-specific capability checks and a consumed inference test must establish support. Model revisions/offline caches require explicit identities outside package locks. Colab does not guarantee T4 allocation or session lifetime; local scratch and durable checkpoint/export boundaries need separate contracts.

Code, model-weight and FFmpeg/NVIDIA binary terms are distinct; PANNs' deposited weights are CC BY 4.0 despite MIT code, and some candidate weight terms remain to verify. The application license, install/profile choices and selected artifact licensing are assigned to the existing distribution decision. No dependencies were installed and no Windows/Colab runtime, performance or recovery measurements were made.
