# Local Wayfinder tracker conventions

> Historical conventions retained for migration provenance. Live work follows [GitHub tracker instructions](../../docs/agents/issue-tracker.md).

This effort uses the installed [local-Markdown tracker](../../.agents/skills/setup-matt-pocock-skills/issue-tracker-local.md), with the Wayfinder map body and labels made explicit below.

## Identity and state

- `map.md` is the canonical map, labelled `wayfinder:map`.
- Each `issues/NN-title.md` is a child issue. Its number is its dependency identity; its H1 title is its human-facing name. Link the title in narration.
- `Type:` is `research`, `prototype`, `grilling`, or `task`; `Labels:` carries the corresponding `wayfinder:<type>` label.
- `Mode:` is `AFK` or `HITL`. `Status:` starts at `open`, becomes `claimed` before work, and becomes `resolved` when the answer is appended under `## Answer`.
- `Assignee: unassigned` denotes an unclaimed issue. A claim sets `Assignee: local-developer`, `Claimed by: <session or research-agent name>`, and `Status: claimed` together before work. Here `local-developer` means the human driving this local map; the session field distinguishes concurrent agents working for that human.
- `Parent:` links to the named map. Physical containment under `issues/` also establishes parentage.
- This tracker has no native dependency relationships. `Blocked by: none` or a comma-separated list of numeric issue identities is the fallback convention. Add issues first and wire edges in a second pass.

## Frontier

Read the map once, then scan issue headers. An issue is takeable when it is `open`, has `Assignee: unassigned`, and every issue in `Blocked by:` is `resolved`. Choose the lowest number unless the user names a particular takeable ticket. Do not open every resolved answer without a reason.

Claim the chosen issue before investigation. Save the claim, then re-read it to detect a concurrent edit; this filesystem convention is not an atomic multi-user tracker. Research agents own only their assigned report and ticket. The coordinating session serializes changes to `map.md`.

## Resolution

Append the resolution under `## Answer`, preserve the original question, set `Status: resolved`, and append one linked gist to the map's Decisions so far. Assets belong in linked files, not pasted into the map. Optional discussion appends under `## Comments`.

Create newly sharp questions as tickets, then add blockers. Remove graduated fog from the map. Before a validation-plan ticket resolves, wire its newly specified experiments into the decisions that accept their results and the final handoff gate so the latter cannot become takeable prematurely. A provisional policy can close to define an experiment; when the experiment depends on that policy, create a validation/follow-up decision rather than adding a backward edge to its prerequisite. Preserve an acyclic dependency graph.

If a ticket is ruled outside the destination, close it using `Status: resolved` with `Resolution: out-of-scope`; append the reason under `## Answer`, link it from Out of scope, and do not add it to Decisions so far. Review dependents because an out-of-scope closure is not supporting evidence.

## Research assets

Each research ticket names its `research/audio-analysis-*` branch, isolated worktree path under `research/`, and `research.md` report. Reports are working-tree assets, not commits. Their relative links work in this local checkout; preserve these directories until the reports are deliberately archived or committed. A branch reference alone does not retain an uncommitted report.

## Concurrency and continuation

Re-read the current issue/map immediately before editing. Do not overwrite another session's claim or answer. Resolve at most one non-research ticket per session, and never resolve a HITL ticket without the live human exchange. Initial charting may resolve research tickets only.
