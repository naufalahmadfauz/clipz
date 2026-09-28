# Acoustic laughter and shouting: candidate evidence

**Retrieved:** 2026-09-27. **Question:** [Establish credible acoustic laughter and shouting options](https://github.com/naufalahmadfauz/clipz/issues/7). This is a comparison shortlist, not a supported-model or product-tier decision. “Verified” means documented/source-inspected, not locally executed. No models or audio were downloaded, and no performance, calibration, or corpus experiments were run.

## 1. Small viable shortlist

### YAMNet: lightweight broad-event baseline

**Verified:** Google's `google/yamnet/1` accepts one-dimensional float32 **mono, 16 kHz**, nominally [-1, 1]. It produces independent scores shaped `[patches, 521]`, 1,024-dimensional embeddings, and a log-Mel spectrogram. Patches are **0.96 seconds**, advancing **0.48 seconds**; STFT windows are 25 ms with 10 ms hops. The source explains that the first complete patch actually needs **975 ms of waveform** because of STFT framing. The README's example averages scores over the entire file; that average is a clip summary, not event localization. Preserve patch scores and their actual support intervals instead. [Y-card] [Y-code]

Its taxonomy explicitly contains **Shout (6), Bellow (7), Whoop (8), Yell (9), Children shouting (10), Screaming (11), Laughter (13), Baby laughter (14), Giggle (15), Snicker (16), Belly laugh (17), and Chuckle, chortle (18)**. Store class MID as well as index: indices differ from PANNs. Parent/child labels overlap; summing their scores is not an event probability. YAMNet drops AudioSet's “Battle cry” and “Funny music,” among other classes. [Y-labels] [Y-code]

The MobileNet-v1 model has approximately **3.7 million weights**, according to upstream. That is a useful relative-complexity fact, not measured RAM or throughput. Its card explicitly says scores are **not calibrated across classes** and warns of domain mismatch. [Y-card] [Y-code]

**Runtime implications:** native Windows TensorFlow remains a CPU route; TensorFlow **2.10 was the last native-Windows GPU release**. Newer official GPU support uses WSL2/Linux. Current YAMNet source additionally warns that its Keras construction needs **Keras 2 / `tf-keras`, not Keras 3**. An existing SavedModel and reconstruction from HDF5 are distinct deployment paths requiring separate smoke tests. CPU YAMNet could coexist with CUDA transcription, but its cost and concurrency benefit are unmeasured. [TF-install] [Y-code]

### PANNs: temporal broad-event comparator

**Verified:** compare **`Cnn14_DecisionLevelMax_mAP=0.385.pth`**, not ordinary Cnn14 alone. Ordinary Cnn14 returns clipwise scores and an embedding; DecisionLevelMax exposes both clipwise and temporal scores. The standard wrapper uses **mono waveform batches at 32 kHz**, a **1,024-sample/32 ms** Hann STFT and **320-sample/10 ms** hop, 64 Mel bins, and 527 classes. Its input array is not automatically resampled by the inference method. [P-wrapper] [P-models]

The actual taxonomy includes **Shout (8), Bellow (9), Whoop (10), Yell (11), Battle cry (12), Children shouting (13), Screaming (14), Laughter (16)** and the same five laughter subclasses at 17–21. These are acoustic labels, not “the person is excited” or “this is funny.” [P-labels]

**Important timing qualification:** five time-pooling stages reduce the model grid by **32**. Temporal sigmoid outputs are interpolated back to the spectrogram grid and padded; therefore nominal **10 ms returned samples are derived from a roughly 320 ms latent stride**, with still wider convolutional context. They are not independent 10 ms observations or a boundary-accuracy guarantee. Clipwise max pooling also means a high clip score does not specify duration. Training uses weak clip labels. Published AudioSet tagging mAP is not laughter/shouting localization performance. [P-models] [P-readme]

The pretrained-model deposit is **Zenodo version v3, DOI 10.5281/zenodo.3987831**; it lists the DecisionLevelMax checkpoint as **327.4 MB**, which is download size, not runtime memory. PyTorch offers Windows CPU/CUDA distributions; CNN activations and batch length add substantial unmeasured memory. The original training repo describes Python 3.7, and the convenience wrapper shells out to `wget` for missing weights/labels. Thus current Windows installation, checkpoint loading, and offline startup need adaptation/verification rather than blind reuse of the example. [P-weights] [P-readme] [P-wrapper] [P-config] [Torch]

### Gillick et al.: conditional specialized laughter comparator

The **2021 “Robust Laughter Detection in Noisy Environments”** implementation is justified as a third, laughter-only comparator: its paper directly investigates noise/domain degradation and supplies temporally annotated AudioSet laughter. It does **not** supply shouting/screaming classes. Checkpoints were trained on Switchboard; the repository's documented tested stack is old (Python 3.6.1, PyTorch 1.3.1, librosa 0.8.1). [L-paper] [L-readme]

Source uses **8 kHz mono**, **44 Mel-feature frames per classification window**, sliding one feature frame with a **186-sample hop = 23.25 ms**. This is approximately one second of feature context, not a 23 ms laughter boundary detector. Feature extraction adds STFT context. A sigmoid supplies one laughter score, then low-pass filtering and duration/threshold segmentation produce intervals. The CLI derives output FPS as `number_of_predictions / file_duration`, rather than preserving each window's exact sample anchor; this mapping and tail coverage require audit before timestamp use. It eagerly loads audio/features, and its top-level multiworker CLI needs Windows-spawn testing. [L-source] [L-loader] [L-config] [L-models]

## 2. Code and weight rights are separate evidence

| Candidate | Code | Weight evidence / remaining check |
|---|---|---|
| YAMNet | TensorFlow Models `/research` is Apache-2.0. | The retrieved first-party model card identifies `google/yamnet/1` but does not state a weight license. Kaggle's page did not expose license metadata to this fetch. **Exact artifact licensing remains unverified**; do not infer it from the source or documentation license. |
| PANNs | Training code and wrapper each contain MIT license files. | The **pretrained-weight deposit explicitly declares CC BY 4.0**. Preserve attribution, license link, checkpoint identity, and any modification/conversion notice; do not relabel weights MIT. |
| Specialized laughter | Repository declares MIT. | Checkpoints are supplied in the same repository, but no independently explicit weight-license statement was established. Record repository provenance and clarify checkpoint coverage before redistribution; Switchboard training provenance is not a redistribution license for recordings. |

Sources: [Y-license] [Y-card] [Y-listing] [P-license] [P-wrapper-license] [P-weights] [L-license] [L-readme]. These are procurement checks for the existing detector/distribution decisions, not legal guarantees. Mutable source branches were inspected on the retrieval date; only the named model handle/deposit and 2021 paper establish version boundaries here. Pin commit and weight hashes during evaluation.

## 3. Design implications and unrun evidence gates

**Proposed, unvalidated:** test YAMNet and PANNs for both target families, adding the specialized comparator only if its modernization/license/timing work is worthwhile. Use bounded overlapping audio blocks, retain only owned output windows, and record input resampling, patch support, padding, class IDs, model revision, raw scores and threshold/postprocessing versions. Whole-session averaging can erase rare laughter; score smoothing can merge distinct reactions. Model outputs should remain separate from loudness evidence and transcript text.

**Unanswered:** none of the inspected primary sources establishes reliable Indonesian/code-switch gaming performance. Laughter is not lexical transcription, but phonetics, laugh-speech blends, microphone distance, Discord compression/noise suppression, overlap and gain processing can still shift its acoustics. Game-character screams, canned laughter, music vocals, soundboards and excited ordinary speech are crucial hard negatives—or acoustically real events with **unknown human/source attribution**. A mixed track cannot establish which person reacted.

**Unrun validation:** annotate laughter, laugh-speech, shout/yell, scream and uncertain intervals independently, including quiet chuckles and game-only negatives. Include random quiet/ordinary regions, not only detector hits. Compare event precision/recall, false events per hour, missed durations and onset/offset error under an agreed matching tolerance; report track/domain slices and annotator disagreement. Split threshold tuning from evaluation. Measure CPU/4060 wall time, peak RAM/VRAM and chunk-boundary equivalence with transcription concurrency. Human-selected error budgets and these results must determine supported, experimental or deferred status; no tier or threshold is settled here.

## Primary sources

[Y-card]: https://github.com/tensorflow/tfhub.dev/blob/master/assets/docs/google/models/yamnet/1.md
[Y-code]: https://github.com/tensorflow/models/blob/master/research/audioset/yamnet/README.md
[Y-labels]: https://github.com/tensorflow/models/blob/master/research/audioset/yamnet/yamnet_class_map.csv
[Y-license]: https://github.com/tensorflow/models/blob/master/LICENSE
[Y-listing]: https://www.kaggle.com/models/google/yamnet/tensorFlow2/yamnet/1
[TF-install]: https://www.tensorflow.org/install/pip
[P-readme]: https://github.com/qiuqiangkong/audioset_tagging_cnn/blob/master/README.md
[P-wrapper]: https://github.com/qiuqiangkong/panns_inference/blob/master/panns_inference/inference.py
[P-models]: https://github.com/qiuqiangkong/panns_inference/blob/master/panns_inference/models.py
[P-config]: https://github.com/qiuqiangkong/panns_inference/blob/master/panns_inference/config.py
[P-labels]: https://github.com/qiuqiangkong/audioset_tagging_cnn/blob/master/metadata/class_labels_indices.csv
[P-weights]: https://zenodo.org/records/3987831
[P-license]: https://github.com/qiuqiangkong/audioset_tagging_cnn/blob/master/LICENSE.MIT
[P-wrapper-license]: https://github.com/qiuqiangkong/panns_inference/blob/master/LICENSE.MIT
[Torch]: https://pytorch.org/get-started/locally/
[L-paper]: https://www.isca-archive.org/interspeech_2021/gillick21_interspeech.html
[L-readme]: https://github.com/jrgillick/laughter-detection/blob/master/README.md
[L-source]: https://github.com/jrgillick/laughter-detection/blob/master/segment_laughter.py
[L-loader]: https://github.com/jrgillick/laughter-detection/blob/master/utils/data_loaders.py
[L-config]: https://github.com/jrgillick/laughter-detection/blob/master/configs.py
[L-models]: https://github.com/jrgillick/laughter-detection/blob/master/models.py
[L-license]: https://github.com/jrgillick/laughter-detection/blob/master/LICENSE
