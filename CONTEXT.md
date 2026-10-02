# Audio Analysis

Evidence from a recording session is organized on a common timeline for later human interpretation and editing.

## Language

**Project**:
One recording session represented on one continuous timeline, including recordings that start late, end early, or contain interruptions.
_Avoid_: Editing sequence, montage

**Source**:
The particular content of an input recording file containing audio, optionally alongside video. Moving or copying identical content does not change the Source; changed content belongs to a different Source.
_Avoid_: Track when referring to an input file

**Audio stream**:
An independently selectable audio sequence contained in a Source, comprising one or more Audio channels. A Source can contain several Audio streams, each distinct from the AudioTracks selected from it.
_Avoid_: Track when referring to a Source's embedded stream

**Audio channel**:
One ordered signal within an Audio stream, whose meaning may be a spatial position, a separately recorded input, or unknown. A channel is not inherently a person, and a channel pair is not inherently two separable voices.
_Avoid_: Speaker

**AudioTrack**:
A logical audio feed analyzed as a unit within a Project, independent of its Source, number of channels, or number of people heard. Its editable name describes the feed; neither its name nor its identity establishes who is speaking.
_Avoid_: File, speaker

**Source span**:
A contiguous portion of selected audio from one Source placed as an uninterrupted part of an AudioTrack on the Project timeline, with its own stream/channel selection and known or unknown channel layout. Several Source spans can continue a track across recordings from the same session while preserving gaps and each portion's origin.
_Avoid_: Recording session, edited clip

**Track definition revision**:
A particular version of the selected audio that constitutes an AudioTrack, including its Source spans and stream/channel selections. Revised selections belong to the same track but remain distinguishable from the selections underlying earlier evidence.
_Avoid_: Track rename

**Analysis rendition**:
A derived representation of an AudioTrack's selected audio used for analysis, such as a mono downmix. It retains its relationship to the original selection and transformations rather than becoming another logical AudioTrack.
_Avoid_: New track, new speaker

**Track classification**:
A user's declaration of an AudioTrack's expected content, using any combination of voice, game, music, and other, or leaving the content unknown. Voice includes speech, laughter, and shouting; a classification is distinct from the track's name and from detected evidence.
_Avoid_: Speaker identity, detector result

**Speaker makeup**:
A user's declaration that an AudioTrack across all its Source spans contains one voice, multiple voices, no voice, or an unknown number of voices. Known participants may be named separately; a sole voice may remain unnamed, and knowing who participates in a mixed track does not identify the speaker of each utterance.
_Avoid_: Channel count, diarization result

**Speaker**:
A person whose voice occurs in a Project's recorded audio, with an identity shared across that Project's AudioTracks wherever that person is known to occur. A Speaker's identity is distinct from their editable name and is local to the Project.
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
