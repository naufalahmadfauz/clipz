# Choose bounded audio decoding, PCM sharing, and scheduling

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Parent: [Audio-first gaming analysis: a design ready for /to-spec](../map.md)
Blocked by: 01, 03, 04, 11, 12, 13, 14, 15, 26

## Question

What proposed audio dataflow minimizes avoidable work while remaining memory-bounded, restartable, and compatible with the actual analyzers?

Compare streaming pipes, normalized materialized PCM, memory-mapped/chunked artifacts, and a justified hybrid. Distinguish source demux/decode from channel extraction and analyzer-specific resampling. Set ownership of decode, sample-rate/channel contracts, chunk overlap/context, timestamp mapping, backpressure, scratch lifetime, and reuse.

Choose a CPU/GPU concurrency model, GPU ownership/batch scheduling, per-stage work units, thread/process boundaries, cancellation, and failure isolation. Account for the actual faster-whisper consumption API and acoustic model context; do not promise one-pass streaming if an analyzer materializes input or requires revisits.

Describe cold-run and reanalysis flows, CPU-only behavior, and the comparisons that must validate decode overhead, memory, disk, concurrency, and throughput. The target is efficient inference-focused processing, not maximum parallelism at any cost.
