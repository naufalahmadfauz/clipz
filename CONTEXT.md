# Audio Analysis

Evidence from a recording session is organized on a common timeline for later human interpretation and editing.

## Language

**Project**:
One recording session represented on one continuous timeline, including recordings that start late, end early, or contain interruptions.
_Avoid_: Editing sequence, montage

**Source**:
An input recording that contains audio, optionally alongside video. A source is distinct from the logical audio tracks selected from it.
_Avoid_: Track when referring to an input file

**AudioTrack**:
A named logical unit of audio in a project, independent of whether its audio originated in an embedded stream or an external recording. Its identity does not by itself establish who is speaking.
_Avoid_: File, speaker

**Speaker**:
A person whose voice occurs in recorded audio. An audio track may contain one speaker, several speakers, or no speech.
_Avoid_: Track

**Project timeline**:
The common elapsed-time reference for a recording session against which evidence from all audio tracks is located.
_Avoid_: Premiere timecode when referring to the shared time reference

**Transcript**:
A record of recognized speech, its timing, and the audio track from which it was recognized.

**Audio event**:
A timestamped observation of an acoustic occurrence, such as a volume spike, laughter, or shouting. An audio event is evidence, not a judgment that a moment is funny.
_Avoid_: Highlight, funny moment

**Analysis package**:
The exported evidence about a project's recordings, tracks, timing, transcripts, and audio events, intended for later interpretation.
_Avoid_: Edited video, highlight reel
