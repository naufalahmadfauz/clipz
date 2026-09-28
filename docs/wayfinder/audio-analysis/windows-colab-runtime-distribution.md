# Reproducible Windows and Colab runtime constraints

**Retrieved:** 2026-09-27. **Question:** [Establish reproducible Windows and Colab runtime constraints](https://github.com/naufalahmadfauz/clipz/issues/11). Completed by the coordinating session after repeated delegated-agent usage-limit failures. Facts below come from primary documentation and the linked release-source investigations; proposed policies remain human decisions. No dependencies, model weights, GPU profiles, installation environments or Colab sessions were tested.

## 1. Supported packaging mechanisms, not a selected dependency matrix

**Verified:** pip documents increasingly reproducible installations through exact direct/transitive version pins, artifact hashes, and an optional offline wheelhouse. Wheelhouses containing compiled packages are OS/architecture-specific. Python's standardized `pylock.toml` format can record supported environments, Python constraints, extras and dependency groups; the format does not prove that a chosen tool or every target supports a particular lock. [pip] [pylock]

Two credible technical-user options are:

| Option | Capability established by documentation | Trade-off to decide |
| --- | --- | --- |
| Isolated Python environment plus pinned/hashed requirements per target profile | pip supports pins, hashes and offline installation artifacts. | Straightforward consumption; lock generation, profile updates and exact Python/native prerequisites still need an explicit workflow. |
| A packaged Python project managed with uv | uv maintains a project lock, syncs selected extras/groups and exports requirements or `pylock.toml`. `--locked` rejects stale metadata; `--frozen` skips that check. | Adds a tool dependency; uv-specific source/index configuration is not consumed automatically by other installers. |

uv's exact sync removes unlisted packages, while its ordinary run uses inexact sync. Therefore installing an application profile directly into Colab's prepopulated environment without an isolation policy can alter or retain unrelated packages. Extras are optional dependency sets, not detection of the installed GPU or a replacement for driver setup. Keep detector dependencies optional if their product tier is optional; do not install both TensorFlow and PyTorch merely because they are on a research shortlist. These are design implications, not a chosen package manager. [uv-sync] [uv-deps]

**Python compatibility is an intersection.** PyAV **18.1.0** declares **Python >=3.11**, with classifiers through 3.14. CTranslate2 **4.8.2** documentation says Python >=3.9 and Windows x86-64/Linux wheels. Neither statement establishes a complete compatible environment with the chosen NumPy, ONNX Runtime, detector and model-loading dependencies. Inspect actual wheel availability for the selected interpreter and optional profiles before locking. Choosing the newest local Python by default would not demonstrate compatibility. [av-project] [CT-install]

## 2. NVIDIA support needs runtime-specific checks

The [transcription capability investigation](transcription-capabilities.md) inspected faster-whisper **1.2.1** and CTranslate2 **4.8.2**. Its release-source findings matter because upstream installation prose conflicts: the CT2 installation page still says cuDNN 8, the faster-whisper README says cuDNN 9, while current wheel build scripts use CUDA 12.8 and disable the cuDNN convolution backend. Windows packaging still includes/preloads a cuDNN DLL. Preserve that distinction rather than publishing a universal "install cuDNN version X" instruction. [CT-install] [ASR]

**Verified:** NVIDIA documents driver/runtime minor-version compatibility with limitations for newer features and PTX. The OS driver, installed toolkit, dynamically loaded cuBLAS/cuDNN libraries and Python wheel build are separate layers. A CUDA version reported by `nvidia-smi` does not establish the exact libraries imported by this process; the selected wheel must execute successfully. Windows CT2 also requires the Visual C++ runtime. [NVIDIA] [CT-install]

**Proposed capability contract:** independently report the selected Python/package/build versions, device identity and available memory, CT2 supported compute types, actual loaded compute type, and a small consumed transcription/alignment smoke result. Record failures with their stage: missing library, unsupported compute type, model load, inference or allocation. PyTorch CUDA availability only describes PyTorch's path, not CT2's. CPU fallback should be an explicit recorded execution profile, not a silent substitution that reuses a misleading cache key. The existing ASR investigation supplies RTX 4060/T4/CPU compute candidates, not measured free memory or deployment success. [ASR]

For detectors, current native-Windows TensorFlow GPU support stops at 2.10; contemporary official GPU use is a WSL2/Linux path. YAMNet CPU and PyTorch-based candidates therefore impose different packaging/concurrency costs. A headless Windows-first engine should not accidentally require WSL because one optional comparator used TensorFlow. [TF-install] [Acoustics]

## 3. Decoder and model artifacts have their own identities

The [media investigation](media-timing-decoding-and-synchronization.md) found that PyAV wheels bundle FFmpeg libraries; an external `ffmpeg`/`ffprobe` executable may use a different build and codec set. Capture both identities if both are used. Avoid assuming installation of one supplies the other's executable or guarantees equivalent timestamp behavior. PyAV's wrapper is BSD-3-Clause; linked decoder components retain their own licensing. [Media] [av-license]

**Verified:** Hugging Face Hub download APIs default to the latest `main` revision but accept an explicit full commit revision. Their cache is version-aware; returned cached files must not be edited. `HF_HOME`/`HF_HUB_CACHE` configure location. `HF_HUB_OFFLINE=1` prevents Hub HTTP calls and errors on unavailable cached artifacts; ordinary cached access can still check remote metadata. On Windows, unavailable symlinks can increase storage by duplicating files. [HF-download] [HF-env]

**Proposed:** separate model acquisition from analysis, record model origin/revision/hash/conversion/configuration/license notices, support local artifact paths, and give offline startup a predictable missing-artifact error. Package locks do not pin model weights, taxonomy files or external executables. A selectable cache location and measured peak scratch/model-storage requirement are particularly relevant for multi-hour Windows sessions and transient Colab machines. Acquisition is not cloud inference and does not require any ChatGPT integration.

## 4. Colab portability is an execution contract

**Verified:** Google does not guarantee a particular GPU type, capacity, or availability. VM lifetime/idle/resource limits vary, VMs can be deleted, and notebook sharing does not include installed libraries or runtime files. The FAQ describes free sessions running at most 12 hours depending on conditions, rather than promising 12 uninterrupted hours; paid offerings also have resource constraints. A T4-capable profile cannot guarantee a T4 allocation. [Colab]

Google also recommends reducing mounted-Drive I/O and avoiding many tiny reads, favoring copying data to the VM for processing. Drive operations can fail due to quotas and interruptions. [Colab]

**Proposed contract:** the same headless engine accepts ordinary paths/configuration and emits persistent artifacts independent of notebook UI. Probe actual hardware/runtime at startup; use a documented CPU alternative when CUDA is unavailable. Keep hot PCM/features on local scratch while checkpointing completed evidence/model references and exporting to user-selected durable storage. A notebook wrapper would obtain files and call the engine; it should not contain analysis policy. Persist enough identity and completion state to resume after a fresh environment and changed mount paths. Atomic local writes alone do not prove durable upload to Drive, so successful checkpoint transfer needs its own completion boundary.

Windows-spawn/process behavior, binary pipes, Unicode/space-containing paths, filesystem replacement semantics, and cancellation must be tested on both hosts; portable Python orchestration alone does not demonstrate parity. No OS-bound UI APIs are needed by the requirements. These implications feed the existing scheduling, cache, CLI/core and distribution decisions rather than mandating an implementation now.

## 5. Distribution rights need artifact-level accounting

| Artifact | Established evidence | Remaining product decision/check |
| --- | --- | --- |
| Application source | Open-source intent, no license selected yet. | Choose an application license compatible with selected redistribution and contribution goals. |
| faster-whisper / CT2 / upstream Whisper candidates | Their code/model notices are examined in the ASR report; relevant upstream licenses are MIT. | Retain exact model-conversion provenance and notices; do not generalize to every dependency. |
| PyAV | BSD-3-Clause wrapper license. | Inventory bundled FFmpeg libraries and build flags separately. |
| FFmpeg | Generally LGPL-2.1-or-later; optional GPL components change the resulting FFmpeg build's license. Official guidance discusses source and linking obligations. | Determine the actual distributed build, notices and corresponding source obligations; a subprocess boundary does not erase obligations for binaries shipped with the app. |
| PANNs | MIT code versus explicitly **CC BY 4.0 deposited weights**. | Preserve attribution and artifact identity. |
| YAMNet / specialized laughter checkpoints | Source licenses are documented, exact independent weight-license coverage was not established in the acoustic research. | Verify the selected artifact's terms before distributing it; otherwise choose a different distribution/candidate policy. |
| NVIDIA runtime components | Separate from the MIT/BSD Python wrappers. | Inspect the selected redistributables' current terms and manifests; no blanket redistribution claim is made here. |

Sources: [ASR] [av-license] [FFmpeg-legal] [Acoustics]. This is an inventory of verified rights and remaining checks, not a legal guarantee. User-managed installation, dependency downloads and bundling have different practical artifact responsibilities; none automatically settles compatibility or weight licensing.

## 6. Evidence still needed before support claims

No material external-research blocker prevents choosing among these approaches. The exact package manager, Python version/profile lock and distribution policy remain HITL decisions. Required future smoke/validation contrasts include clean Windows CPU and 4060 environments; a fresh available T4 runtime; model prefetch then disconnected restart; missing/corrupt cache behavior; relinked durable artifacts after runtime loss; optional-detector absence; and decoder/ASR/detector version reporting. Measure startup, download/cache space, inference success and restart behavior separately from corpus accuracy. The application license and exact model-weight permissions should be explicitly settled in the Wayfinder decision "Choose reproducible distribution and Colab compatibility."

## Primary sources and linked investigations

[pip]: https://pip.pypa.io/en/stable/topics/repeatable-installs/
[pylock]: https://packaging.python.org/en/latest/specifications/pylock-toml/
[uv-sync]: https://docs.astral.sh/uv/concepts/projects/sync/
[uv-deps]: https://docs.astral.sh/uv/concepts/projects/dependencies/
[av-project]: https://github.com/PyAV-Org/PyAV/blob/v18.1.0/pyproject.toml
[av-license]: https://github.com/PyAV-Org/PyAV/blob/v18.1.0/LICENSE.txt
[CT-install]: https://opennmt.net/CTranslate2/installation.html
[NVIDIA]: https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html
[TF-install]: https://www.tensorflow.org/install/pip
[HF-download]: https://huggingface.co/docs/huggingface_hub/guides/download
[HF-env]: https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables
[Colab]: https://research.google.com/colaboratory/faq.html
[FFmpeg-legal]: https://ffmpeg.org/legal.html
[ASR]: transcription-capabilities.md
[Media]: media-timing-decoding-and-synchronization.md
[Acoustics]: acoustic-detector-candidates.md
