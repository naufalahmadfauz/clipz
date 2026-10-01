# Manual ChatGPT Chat uploads: capacity and coverage evidence

**Retrieved:** 2026-09-27. **Question:** [Establish manual ChatGPT upload and context constraints](../../issues/07-manual-chatgpt-export-research.md). Sources are official **ChatGPT Chat** help articles, not API limits. These are mutable service descriptions, not versioned compatibility promises. No account was inspected, no file was uploaded, and no model or data-analysis test was run.

## 1. Verified upload limits are several different limits

The current File Uploads FAQ documents the following. Recheck at the eventual manual trial: plan, workspace controls, model and remaining allowance can affect access. [Uploads]

| Constraint | Documented value / scope |
|---|---|
| General file-size ceiling | **512 MB per file** uploaded to a ChatGPT conversation or GPT. |
| Text/document ceiling | **2 million tokens per file**; does not apply to spreadsheets. This is an ingestion ceiling, not model context. |
| CSV/spreadsheets | Approximately **50 MB**, depending on row size; the general 512 MB ceiling is not the practical spreadsheet budget. |
| Images | **20 MB per image**; irrelevant to a text-first analysis package. |
| Upload rate | Up to **80 files per three hours**; Free users **three uploads/day**. Limits may be lowered during peak hours; failed attempts can count. |
| Shared storage | **25 GB per end user; 100 GB per organization**, across chats, Projects and GPT knowledge. These are storage quotas, not context. |
| Project file count | Free **5**; Go/Plus **25**; Edu/Pro/Business/Enterprise **40**. Projects documentation says only **10 at a time**. |

The FAQ currently also says up to ten files per GPT over that GPT's lifetime. That is a GPT-specific statement, **not** a guaranteed ten-file conversation limit. Data-analysis documentation expressly says conversation attachment limits vary with upload type, model, plan, settings and remaining allowance. The storage UI can show Library storage; a remaining rolling-upload counter is not currently provided. [Uploads] [Projects] [Analysis]

**Types:** the general supported-types article lists CSV/TSV, Excel, DOCX, PPTX, PDF and TXT. The more specific data-analysis article also names **JSON, XML, YAML, TXT and Markdown**, with capability qualifications. Thus structured JSON and readable Markdown/TXT have first-party support evidence. A distinct guarantee for `.jsonl` was not established. A fallback TXT/CSV representation may be useful, but changing an extension does not enlarge context or guarantee a particular processing route. [Types] [Analysis]

## 2. Successful ingestion does not mean exhaustive semantic review

**Verified:** ChatGPT can run Python in a stateful notebook environment for some analysis tasks. The docs recommend one record per row with descriptive column names and reviewing generated code, outputs and assumptions. They explicitly warn that a file may upload successfully yet be too large, complex or poorly structured for complete analysis; inspecting specific sections or splitting files is recommended. [Analysis]

OpenAI's Enterprise-specific optimization guide distinguishes text extraction/retrieval from code analysis. In that guide, TXT/MD/JSON commonly enter text retrieval; spreadsheets use Code Interpreter, and a user can explicitly request Code Interpreter for JSON. Text may be partly inserted into model context and partly searched from a private index. It documents a **128k model window and up to 110k document tokens inserted**, with the start of a single overlarge document inserted first, and a allocation procedure for multiple documents. It expressly says those details are under active development. [Enterprise-files]

**Scope/conflict qualification:** that Enterprise article still discusses GPT-series/o-series routing, while the current general ChatGPT model article describes **GPT-5.6 and GPT-6 Pro** and does not establish one universal numeric context window. The Enterprise guide is evidence that retrieval and partial context insertion exist; its numbers and search-count examples should **not** become a permanent rule for all current ChatGPT plans/models. This investigation did not establish the user's effective context allowance, routing, conversation-history consumption or truncation behavior. API context specifications cannot fill that gap. [Enterprise-files] [Chat-models]

**Design inference:** Python successfully parsing every JSON record can establish structural coverage—counts, IDs, valid intervals—but the model may see only previews, aggregates or selected outputs. It does not establish that each line received semantic attention. Likewise, even content fully inserted into context has no documented guarantee of exhaustive humor discovery. A claim such as “read everything” in an answer is not a coverage audit. Ask for record-referenced outputs and bounded review passes; keep human interpretation and completeness claims separate.

## 3. Proposed export roles, pending the existing policy decision

**Full analysis package:** retain complete transcripts/timing, observations, source/AudioTrack identities, processing coverage and detector provenance locally. This is the authoritative evidence snapshot, not automatically the first ChatGPT attachment. Continuous measurement arrays and word objects can dominate size without adding useful immediate reading context.

**Compact review export:** a short manifest and chronological evidence regions, with cross-track dialogue context, stable transcript/event IDs, canonical project times, and raw score/measurement definitions. Merge overlapping context intervals before rendering their text; an event can reference an already-present transcript span. Deduplicate **identical records/IDs**, not similar utterances: repeated lines may be a running joke, echo, different speakers or an ASR artifact. Preserve overlapping speech and uncertain attribution.

**Complete chronological pages:** provide access to all recognized speech independently of acoustic triggers. A deadpan remark, callback, insult or quiet conversation can have no loudness/laughter event. An event-rich view alone introduces salience and rare-event bias; balanced sampling only audits the bias and does not restore omitted material. Page coverage should reflect available evidence, including ASR gaps, rather than imply unrecognized speech was reviewed. These implications fit [Choose candidate regions and compact LLM evidence exports](../../issues/19-candidates-and-compact-export.md).

**Chunked workflow:** choose bounded project-time pages with enough surrounding dialogue to understand boundaries. Give each page an owned interval plus separately identified repeated context, and stable global IDs. An index should list page count, filenames/content hashes, project/analysis revision, tracks, record counts, covered and omitted intervals, omission reasons and export policy. Keep “exported,” “uploaded,” “structurally checked” and “semantically reviewed” as different states. A new chat needs its manifest/instructions supplied again; project memory is useful organization, not a substitute for explicit revision/coverage tracking. [Projects]

Returned selections should cite project/export revision, source observation IDs, proposed canonical start/end times and the interpretation. Resolve IDs locally against the saved package and reject unknown/out-of-range references. Keep ChatGPT's rationale distinct from acoustic facts. Never use regenerated prose timestamps as the sole link to Premiere.

## 4. Synthetic size arithmetic—not an upload experiment

Assume **four hours = 240 minutes**, two speech AudioTracks, each active 50% of the time at 150 words per active minute:

`240 × 2 × 0.5 × 150 = 36,000 recognized words`.

Assuming five **UTF-8 bytes per word including spacing**, raw text is about **180,000 bytes**. This is an illustrative mostly-ASCII assumption, not measured Indonesian/code-switch tokenization. At eight words per segment there are 4,500 segments; assuming 90 bytes of IDs/timing/structure per segment adds 405,000 bytes, giving roughly **0.585 MB** before the manifest/events. Repeating 100 bytes of structure for every word instead adds **3.6 MB**. At an assumed 1.6 tokens per lexical word, text alone is approximately **57,600 tokens**; JSON syntax, times, IDs, prompts and chat history are additional and must not be ignored.

For contrast, exporting two tracks' continuous scalar measurements at **10 Hz** gives `14,400 × 2 × 10 = 288,000 rows`. At an assumed 100 bytes/row, that is **28.8 MB**. A crude **four bytes/token** assumption would imply **7.2 million tokens** if serialized as text—over the documented text limit despite modest bytes. Actual tokenizer behavior could differ materially. CSV's spreadsheet exception might permit ingestion under its approximate byte ceiling but does not make all those rows semantically visible. [Uploads]

These calculations justify configurable budgets and event/summary references, not a fixed chosen page size. Measure actual serialized bytes and record counts, identify the tokenizer if estimating tokens, and reserve context for task instructions, answers and history. Neither a four-hour duration nor the number of sources predicts export size by itself.

## 5. Unanswered facts and proposed validation

The external question is answerable; account-specific behavior and review quality remain unverified. Before treating the export policy as validated, run a human-authorized trial on the actual plan/model using a representative four-hour package plus small fixtures containing known early/middle/late records, overlaps, duplicated context and quiet semantic-only material. Request structural counts through code and independently compare selected IDs/coverage. Test page boundaries and returned-window reconciliation separately from subjective interpretation. Record model/plan/date and omissions; do not call a successful upload or accurate count an exhaustive-attention result. No new decision ticket is needed beyond the existing schema, compact-export and validation questions.

## Primary sources

[Uploads]: https://help.openai.com/en/articles/8555545-file-uploads-faq
[Analysis]: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
[Types]: https://help.openai.com/en/articles/8983675-what-types-of-files-are-supported
[Projects]: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
[Enterprise-files]: https://help.openai.com/en/articles/10029836-optimizing-file-uploads-in-chatgpt-enterprise
[Chat-models]: https://help.openai.com/en/articles/11909943-gpt-5-in-chatgpt
