# Issue tracker: GitHub

Issues, specs, and Wayfinder maps live in GitHub Issues for `naufalahmadfauz/clipz`. Use the `gh` CLI. Local `.scratch/` files are working material or migration archives, not a second live tracker.

## Operations

- Create: `gh issue create --repo naufalahmadfauz/clipz --title "..." --body-file <path>`.
- Read: `gh issue view <number> --repo naufalahmadfauz/clipz --comments`; also fetch labels, state, and assignees when routing work.
- List: `gh issue list --repo naufalahmadfauz/clipz --state all --json number,title,state,labels,assignees,url` with suitable filters.
- Comment: `gh issue comment <number> --repo naufalahmadfauz/clipz --body-file <path>`.
- Label: `gh issue edit <number> --repo naufalahmadfauz/clipz --add-label <label>`.
- Close: `gh issue close <number> --repo naufalahmadfauz/clipz --reason completed` after recording the answer.
- Use `gh api --input <json-file>` for structured requests. Repository issue numbers and numeric database IDs are different values.

## Pull requests as a triage surface

PRs as a request surface: no.

## Wayfinding operations

- Map: one issue labelled `wayfinder:map`; its body contains Destination, Notes, Decisions so far, Not yet specified, and Out of scope. It is an index of resolved decisions, not a list of open work.
- Child: a native sub-issue labelled `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`. Create all issues before wiring relationships. Refer to each issue by its linked title.
- Parent relationship: POST `repos/naufalahmadfauz/clipz/issues/<map-number>/sub_issues` with the child's numeric database `issue_id`. Preserve the map's sub-issue order.
- Blocking: POST `repos/naufalahmadfauz/clipz/issues/<child-number>/dependencies/blocked_by` with the blocker's numeric database `issue_id`. Read that ID from the issue API, not its number or GraphQL node ID.
- Frontier: paginate the map's native sub-issues; retain open, unassigned children whose blockers are all closed. Choose the first in map order. Query dependency endpoints when needed to verify state.
- Claim: assign the selected issue to the driving developer before work, usually with `gh issue edit <number> --add-assignee @me`. Re-read to detect competing claims.
- Resolve: post the answer as a comment, close the child, then append one linked gist to Decisions so far. Link research/prototype assets rather than pasting them into the map.
- New work: create newly precise questions, then wire dependencies and remove graduated fog. Experiments block the decision that accepts their results and the final readiness gate; keep the graph acyclic.
- Out of scope: close with reason `not planned`, explain why, and link it under Out of scope rather than Decisions so far.
- Only if native relationships are demonstrably unavailable, record named parent/blocker links in bodies and document the fallback on the map. Authentication or permission failure does not justify silently creating local tickets.

## Planning assets and continuation

The audio-analysis brief and cited research reports are published under `docs/wayfinder/audio-analysis/` on `docs/wayfinder-audio-analysis`. The asset index points to the canonical GitHub map. Prefer commit-pinned links for evidence cited in resolutions.

Read the map once, zoom into related tickets as needed, and resolve at most one non-research decision per session. HITL decisions require the human's live answers. Research findings do not substitute for measured corpus/runtime evidence.
