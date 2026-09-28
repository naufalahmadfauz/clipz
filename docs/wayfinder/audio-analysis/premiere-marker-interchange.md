# Premiere markers and timestamp interchange

**Retrieved:** 2026-09-27. **Question:** [Establish Premiere marker and timestamp interchange options](https://github.com/naufalahmadfauz/clipz/issues/10). Adobe's current UXP references, first-party samples/help, and Apple's archived **Final Cut Pro 7 XML Interchange Format** establish capabilities below. Context7 discovery was checked against Adobe references. No Premiere instance, importer, plugin, XML fixture or round-trip was executed; compatibility with the user's installed release remains unverified.

## 1. Interchange routes and their actual boundaries

### Direct manual markers: smallest setup burden

Adobe documents moving the playhead, adding a marker with **M**, and editing properties through the marker dialog/panel. Source Monitor markers accompany the source clip into a sequence. A short, correctly formatted list of selected times/names/notes can therefore support manual entry. The operator must deliberately choose sequence versus clip ownership; the currently selected track item and focused panel matter. This is viable for a small selection, but its practical effort/error rate is unmeasured. [Add] [Properties] [Overview]

### CSV reports and captions do not establish marker import

Keep the built-in marker CSV **export** workflow conceptually one-way: a report leaving Premiere is not an accepted marker-import schema. **Evidence gap:** the current help pages retrieved did not specify that export's exact columns, ID preservation or encoding, and no native marker CSV importer was established. Adobe's supported-format table lists CSV/PBL/TXT/TAB specifically as **batch lists**, not marker files. An extension advertising CSV import needs its own schema/version/anchor verification. Do not label an arbitrary application CSV “Premiere-compatible” merely because Premiere accepts another kind of CSV. [Formats]

SRT import is expressly documented: importing and dragging an SRT into a sequence creates a **caption track**. That supplies visible timed text, not sequence/clip markers or a marker round-trip. XML also has multiple meanings: caption Timed Text XML and FCP project XML are separate entries in Adobe's format table. [Captions] [Formats]

### FCP XML: sequence interchange, not insertion into an existing sequence

Adobe documents FCP XML project import/export, warns about translation losses, and says modern **`.fcpxml` cannot be directly imported** without conversion in the documented FCP X workflow. Its current export command is **File > Export > Final Cut Pro XML**, with an FCP Translation Results log. Apple's legacy **`xmeml` version 5** specification describes sequence/clip markers with name, comment, in/out and optional color. That is the relevant legacy interchange vocabulary, not a license to generate arbitrary `.fcpxml`. [ImportXML] [ExportXML] [AppleXML]

**Proposed:** a generated auxiliary sequence containing markers is a plausible file-based route to test. Importing that sequence does not merge markers into an already-open sequence. Adobe documents “Copy Paste Includes Sequence Markers,” preserving color, notes, duration and type **when copying/pasting timeline items**. A carrier-item transfer might bridge an auxiliary sequence, but placement, selection span, extra media/items and destination behavior require validation. A marker-only empty sequence importing successfully is also unproven. Apple's `updatebehavior` is a Final Cut feature, not evidence Premiere will patch an existing sequence. [Copy] [AppleXML]

### UXP: explicit existing-sequence marker operations

**Verified, since Premiere 25.6:** `Markers.getMarkers(owner)` accepts a **Sequence or ClipProjectItem**. The resulting collection exposes `createAddMarkerAction(name, markerType, startTime, duration, comments)`, enumeration, move and remove actions. Adobe's sample adds zero-duration comment markers through `Project.executeTransaction` inside `lockedAccess`. Thus an installed local UXP adapter can, in principle, read a selection file and add markers to an explicitly selected existing sequence. The API is not itself a built-in JSON/CSV importer. [Markers] [Project] [Sample]

Marker methods expose start, duration, name, comments, type and color; setters return actions. **Native `Marker.guid` is documented only from 26.3**, although the other marker methods date to 25.6. The creation API does not accept a caller-supplied GUID. A proposed stable application selection ID in name/comments plus project/sequence identity is therefore useful even with GUID access; test preservation and duplicate-import behavior rather than assuming GUIDs survive XML or copy/paste. [Marker]

Development setup currently requires **Premiere 25.6+, UXP Developer Tool 2.2+, developer mode and restart**, plus a manifest targeting the host. Sample manifests/READMEs retain earlier beta minimums and now include newer beta typings; these do not override each API's release annotation. Adobe's CEP sample README says UXP superseded CEP in 25.6, recommends UXP for new development, and describes a planned one-calendar-year coexistence period. Existing ExtendScript/CEP integrations remain a version-specific alternative, not a dependable indefinite support promise or standalone Python API. [Setup] [Samples] [CEP]

### XMP: source metadata, not a generic sequence patch

Adobe distinguishes file metadata embedded in media (or sidecars) from clip metadata inside a Premiere project. XMP is a legitimate metadata mechanism, but this investigation did not establish that writing an arbitrary XMP marker sidecar imports sequence markers with stable IDs into an existing sequence. Source-file association, metadata preferences and supported fields require a dedicated fixture if this route is considered. [Metadata]

## 2. Time and ownership contract

**Verified:** `TickTime` accepts seconds, tick strings or frame count plus `FrameRate`. Its `ticks` property is a string; `alignToFrame` floors to a frame boundary while `alignToNearestFrame` chooses the nearest. `FrameRate` exposes ticks-per-frame, and `Sequence` exposes timebase, zero point and audio/video display format. The API offers precise representations; that alone does not prove which subframe values the marker UI or interchange preserves. [Ticks] [Rate] [Sequence]

**Proposed mapping:** define an explicit project-time anchor placed at an explicit sequence-relative position. Compute sequence-relative elapsed time from that mapping, then quantize using the **actual rational target rate**—for example 30000/1001, not rounded 29.97 or an assumed 30. Sequence start timecode is a display origin, not the source's synchronization offset. Read/check both independently, and test whether each API/import field is relative or display-origin-adjusted before adding an offset.

For frame rate `p/q`, the unrounded frame position is `elapsed_seconds × p/q`. Compare nearest-frame points against outward-rounded windows (floor start, ceil exclusive end). These are policy candidates, not chosen semantics. Record original canonical times and quantization error. At nearest rounding the mathematical error bound is half a frame, excluding all synchronization/detector uncertainty. Adobe's UI clip In/Out convention includes the displayed endpoint frames; translating a half-open analysis window by copying its end into that UI can add a frame. [TimeEntry]

Drop-frame is **frame-number labeling**, not dropping media frames or changing elapsed duration. Store the rational rate and DF/NDF display flag separately. Apple's XML timecode `frame` is an actual frame count accounting for skipped labels; marker in/out values are interpreted in the applicable rate. Its archived catalog does not establish modern Premiere support for every rate/DF combination or every point-marker encoding. Derive the accepted XML point/duration syntax from an actual Premiere export. [AppleXML]

A clip marker is source-anchored; reuse, trimming, movement or retiming of that clip can expose the same marker at different sequence positions. A sequence marker is anchored to that sequence. The Markers panel may display sequence timecode for a selected track item and source timecode in the Source Monitor, so appearance alone does not identify ownership. Variable-frame-rate source averages must not become the sequence clock: map elapsed source/project time to the target sequence, and separately verify that Premiere's source playback remains aligned. Arbitrary edited/retimed-sequence mapping is beyond this session-timeline design. [Overview]

## 3. Small validation workflow—all unrun

First record the user's exact Premiere build, target rate/timebase, DF setting, sequence start timecode and project-zero placement. Start with a short selection list and manually add a point and range marker to establish the intended ownership/display. Save a fixture copy and inspect an actual CSV/XML export; API enumeration is another round-trip candidate.

Then test only the mechanism chosen in the Wayfinder decision "Choose the Premiere marker round-trip contract": XML auxiliary-sequence transfer or a minimal UXP import/enumeration fixture if batch placement justifies setup. Include project zero, one frame, half-frame boundaries, a one-frame window, a point near four hours, overlapping windows, nonzero start timecode, 30000/1001 DF minute/ten-minute transitions, a reused trimmed clip, and Unicode/commas/newlines in notes. Test repeated import, manual marker edits, undo, save/reopen, and application-ID preservation.

Compare stored starts/durations and displayed frame labels against independent rational calculations; confirm source/sequence ownership and unchanged intended placement after reopening. A successful XML parse or API call is insufficient. CSV serialization, XML field preservation, subframe retention and actual installed-version behavior remain explicit unanswered facts; there is no material blocker to the external capability comparison. These validation details belong to the existing marker/clock/validation decisions, not a new human decision ticket.

## Primary sources

[Add]: https://helpx.adobe.com/premiere/desktop/organize-media/apply-labeling/add-a-marker-to-a-clip.html
[Properties]: https://helpx.adobe.com/premiere/desktop/organize-media/apply-labeling/view-marker-comments.html
[Overview]: https://helpx.adobe.com/premiere-pro/using/markers.html
[Formats]: https://helpx.adobe.com/premiere-pro/using/supported-file-formats.html
[Captions]: https://helpx.adobe.com/premiere/desktop/add-text-images/insert-captions/import-caption-file-from-third-party-service.html
[ImportXML]: https://helpx.adobe.com/premiere-pro/using/importing-xml-project-files-final.html
[ExportXML]: https://helpx.adobe.com/premiere-pro/using/exporting-projects-applications.html
[AppleXML]: https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/FinalCutPro_XML/Elements/Elements.html
[Copy]: https://helpx.adobe.com/premiere/desktop/organize-media/apply-labeling/copy-and-paste-sequence-markers.html
[Markers]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/markers/
[Marker]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/marker/
[Project]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/project/
[Sample]: https://github.com/AdobeDocs/uxp-premiere-pro-samples/blob/main/sample-panels/premiere-api/src/markers.ts
[Setup]: https://developer.adobe.com/premiere-pro/uxp/plugins/
[Samples]: https://github.com/AdobeDocs/uxp-premiere-pro-samples/blob/main/README.md
[CEP]: https://github.com/Adobe-CEP/Samples/blob/master/PProPanel/ReadMe.md
[Metadata]: https://helpx.adobe.com/premiere-pro/using/metadata.html
[Ticks]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/ticktime/
[Rate]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/framerate/
[Sequence]: https://developer.adobe.com/premiere-pro/uxp/ppro_reference/classes/sequence/
[TimeEntry]: https://helpx.adobe.com/premiere-pro/using/timecode.html
