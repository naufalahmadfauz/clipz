# Secure representative recordings and a runtime inventory

Type: task
Labels: wayfinder:task
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: none

## Question

What locally accessible recordings and hardware/runtime facts can support honest design experiments?

Work with the user to identify a compact representative corpus: the current MP4 plus microphone layout; Indonesian/English code-switching; slang; quiet and excited speech; actual laughter/shouting; game explosions/music or compressed Discord that might cause false detections; overlap; and a long session. Seek multistream/multichannel and known-offset/drift/interruption cases where available, and record missing coverage rather than manufacturing it.

The agent inventories accessible hardware and installed runtimes itself. Ask the human only for unavailable recordings, access, and judgments such as reference transcriptions or event labels. Record paths or stable corpus references, source timing/durations, hardware memory/storage facts, and permitted uses. Keep source recordings and private transcript content outside published research assets unless the user explicitly chooses otherwise.

Resolve when the agreed minimum corpus and inventory are available and gaps are explicit. No downloading model weights, installation, or lengthy benchmark is implied by this prerequisite task.
