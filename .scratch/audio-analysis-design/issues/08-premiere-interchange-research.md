# Establish Premiere marker and timestamp interchange options

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: local-developer
Claimed by: charting-remaining-research
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none
Research branch: research/audio-analysis-premiere
Research worktree: ../research/premiere
Research asset: [Premiere interchange evidence](../research/premiere/research.md)

## Question

Which supported, realistically usable interchange paths can move selected project-time points or windows into Adobe Premiere Pro markers, and what can be round-tripped back?

Use Adobe documentation, relevant interchange specifications, and authoritative API/source references. Distinguish built-in marker CSV export from actual CSV import; distinguish caption import from marker import; inspect XML/XMP/extension or scripting paths where relevant, with version and setup constraints. Do not assume an undocumented format works.

Explain sequence versus clip markers, point versus duration markers, marker IDs/labels/notes, project zero versus sequence start timecode, rational frame rates, drop-frame display, variable-frame-rate media, rounding, and audio-subframe limitations. Propose the smallest manual workflow and validation fixture that can establish actual compatibility later, without implementing a Premiere plugin or assuming 30 fps.

## Answer

Resolved 2026-09-27. The coordinator verified and recorded the delegated agent's saved [Premiere marker and timestamp interchange evidence](../research/premiere/research.md) after its tool session reported usage-limit failures.

Official UXP APIs since Premiere 25.6 expose sequence/clip marker creation and enumeration; stable native marker GUID access is documented only from 26.3. This supports a possible local adapter, not built-in JSON/CSV import. Legacy FCP XML is a sequence-interchange candidate requiring a fixture, and importing an auxiliary sequence does not itself insert markers into an existing one. Caption import creates captions. No native arbitrary marker-CSV importer was established.

The report distinguishes source/sequence ownership, canonical elapsed time, sequence start display, rational rates, drop-frame labels and quantization. It proposes manual-entry, XML-transfer and UXP validation paths with clear setup costs. Exact CSV round-trip fields, subframe preservation, and the user's installed-version behavior remain untested. The human still chooses the optional marker scope and mechanism; no Premiere compatibility or successful import is claimed.
