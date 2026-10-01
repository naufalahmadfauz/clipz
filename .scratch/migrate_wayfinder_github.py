"""One-off, resumable migration using gh; never stages, commits, or pushes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from graphlib import TopologicalSorter


ROOT = Path(__file__).resolve().parent.parent
EFFORT = ROOT / ".scratch/audio-analysis-design"
STATE_PATH = EFFORT / "github-migration.json"
REPO = "naufalahmadfauz/clipz"
BASE = f"repos/{REPO}"
WEB = f"https://github.com/{REPO}"
BRANCH = "docs/wayfinder-audio-analysis"
ASSETS = Path("docs/wayfinder/audio-analysis")
ASSET_NAMES = {
    "media": "media-timing-decoding-and-synchronization.md",
    "transcription": "transcription-capabilities.md",
    "acoustics": "acoustic-detector-candidates.md",
    "loudness": "loudness-spikes-and-reactions.md",
    "chatgpt": "manual-chatgpt-upload-constraints.md",
    "premiere": "premiere-marker-interchange.md",
    "runtime": "windows-colab-runtime-distribution.md",
}
GH = r"C:\Program Files\GitHub CLI\gh.exe"
MARKER = "clipz-wayfinder:audio-analysis-design"
LAST_WRITE = 0.0
LABELS = {
    "wayfinder:map": ("5319e7", "Shared map of product and architecture decisions"),
    "wayfinder:research": ("0075ca", "Primary-source investigation supporting a decision"),
    "wayfinder:prototype": ("a2eeef", "Human-reviewed disposable design experiment"),
    "wayfinder:grilling": ("d876e3", "Decision resolved through a live human interview"),
    "wayfinder:task": ("fbca04", "Prerequisite work that unblocks a decision"),
    "needs-triage": ("ededed", "Maintainer needs to evaluate the issue"),
    "needs-info": ("d876e3", "Waiting for requested information"),
    "ready-for-agent": ("0e8a16", "Fully specified work an agent can execute"),
    "ready-for-human": ("fbca04", "Work requiring a human"),
    "wontfix": ("ffffff", "Work that will not be actioned"),
}


def api(endpoint, method="GET", data=None, paginate=False):
    global LAST_WRITE
    if method != "GET":
        time.sleep(max(0.0, 1.25 - (time.monotonic() - LAST_WRITE)))
    command = [GH, "api", endpoint, "--method", method,
               "-H", "Accept: application/vnd.github+json",
               "-H", "X-GitHub-Api-Version: 2026-03-10"]
    if data is not None:
        command += ["--input", "-"]
    if paginate:
        command += ["--paginate", "--slurp"]
    result = subprocess.run(command, input=None if data is None else json.dumps(data),
                            capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    if method != "GET":
        LAST_WRITE = time.monotonic()
    if result.returncode:
        raise RuntimeError(f"{method} {endpoint}: {result.stderr.strip()}")
    value = json.loads(result.stdout) if result.stdout.strip() else None
    return [item for page in value for item in page] if paginate else value


def read(path):
    return path.read_text(encoding="utf-8")


def source_map_text():
    archive = EFFORT / "map-local-archive.md"
    return read(archive if archive.exists() else EFFORT / "map.md")


def section(text, heading):
    match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)",
                      text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save(state):
    # Generated checkpoint, separate from all authored source documents.
    temporary = STATE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def load():
    state = json.loads(read(STATE_PATH)) if STATE_PATH.exists() else {
        "repository": REPO, "branch": BRANCH, "issues": {}, "source_hashes": {}}
    assert state["repository"] == REPO and state["branch"] == BRANCH
    tickets = {}
    for path in sorted((EFFORT / "issues").glob("[0-9][0-9]-*.md")):
        text = read(path)
        key = path.name[:2]
        fields = dict(re.findall(r"^([A-Za-z ]+): (.+)$", text, re.MULTILINE))
        title = re.search(r"^# (.+)$", text, re.MULTILINE).group(1)
        blockers = [] if fields["Blocked by"] == "none" else fields["Blocked by"].split(", ")
        assert fields["Status"] in {"open", "resolved"}
        assert fields["Labels"] == "wayfinder:" + fields["Type"]
        assert section(text, "Question")
        assert bool(section(text, "Answer")) == (fields["Status"] == "resolved")
        assert (fields["Status"] == "resolved") == (fields["Type"] == "research")
        tickets[key] = {"path": path, "text": text, "title": title, "fields": fields,
                        "blockers": blockers}
        old_hash = state["source_hashes"].get(key)
        if old_hash and old_hash != digest(text):
            raise RuntimeError(f"Source changed during migration: {title}")
        state["source_hashes"][key] = digest(text)
    assert len(tickets) == 26 and len({t["title"] for t in tickets.values()}) == 26
    graph = {key: ticket["blockers"] for key, ticket in tickets.items()}
    assert all(blocker in graph for blockers in graph.values() for blocker in blockers)
    order = list(TopologicalSorter(graph).static_order())
    ancestors = {}
    for key in order:
        ancestors[key] = set(graph[key]).union(*(ancestors[x] for x in graph[key]))
    assert ancestors["25"] == set(graph) - {"25"}
    return state, tickets


def token(key):
    return f"<!-- {MARKER}:{key} -->"


def all_issues():
    return [issue for issue in api(f"{BASE}/issues?state=all&per_page=100", paginate=True)
            if "pull_request" not in issue]


def info(issue):
    return {field: issue[field] for field in ("number", "id", "title", "html_url")}


def asset_map():
    paths = {
        (EFFORT / "brief.md").resolve(): ASSETS / "accepted-brief.md",
        (ROOT / "CONTEXT.md").resolve(): Path("CONTEXT.md"),
        (EFFORT / "tracker.md").resolve(): Path("docs/agents/issue-tracker.md"),
    }
    for source in sorted((EFFORT / "research").glob("*/research.md")):
        paths[source.resolve()] = ASSETS / ASSET_NAMES[source.parent.name]
    assert len(paths) == 10, "Expected brief, glossary, tracker and seven reports"
    return paths


def rewrite(text, source, state, tickets, destination=None, revision=None, draft=False):
    issue_links = {(ticket["path"].resolve()): state["issues"][key]["html_url"]
                   for key, ticket in tickets.items() if key in state["issues"]}
    issue_links[(EFFORT / "map.md").resolve()] = state["map"]["html_url"]
    assets = asset_map()

    def target(value):
        if value.startswith(("http://", "https://", "mailto:", "#")):
            return value
        path_part, sep, fragment = value.partition("#")
        resolved = (source.parent / path_part).resolve()
        if resolved in issue_links:
            url = issue_links[resolved]
        elif resolved in assets:
            dest = assets[resolved]
            if destination is not None:
                url = os.path.relpath(ROOT / dest, (ROOT / destination).parent).replace("\\", "/")
            elif draft:
                url = state["map"]["html_url"]
            else:
                url = f"{WEB}/blob/{revision or BRANCH}/{dest.as_posix()}"
        else:
            raise RuntimeError(f"Unmapped link in {source.name}: {value}")
        return url + ("#" + fragment if sep else "")

    text = re.sub(r"(\[[^\]\n]+\]\()([^\s)]+)(\))",
                  lambda m: m[1] + target(m[2]) + m[3], text)
    return re.sub(r"^(\[[^\]\n]+\]:\s*)(\S+)\s*$",
                  lambda m: m[1] + target(m[2]), text, flags=re.MULTILINE)


def child_body(key, ticket, state, tickets, revision=None, draft=False):
    question = rewrite(section(ticket["text"], "Question"), ticket["path"], state,
                       tickets, revision=revision, draft=draft)
    mode = "Human in the loop" if ticket["fields"]["Mode"] == "HITL" else "Agent-driven research"
    title = state["map"]["title"]
    result = f"{token(key)}\n\nPart of [{title}]({state['map']['html_url']}).\n\n**Mode:** {mode}.\n\n## Question\n\n{question}\n"
    if draft:
        result += "\n_Migration in progress: evidence links and native dependencies are being published._\n"
    elif ticket["fields"]["Type"] == "research":
        result += "\n## Research asset\n\n" + rewrite(ticket["fields"]["Research asset"],
                    ticket["path"], state, tickets, revision=revision) + "\n"
    return result


def create(state, tickets):
    repository = api(BASE)
    assert repository["has_issues"] and repository["permissions"]["push"]
    existing_labels = {item["name"] for item in api(f"{BASE}/labels?per_page=100", paginate=True)}
    for name, (color, description) in LABELS.items():
        if name not in existing_labels:
            api(f"{BASE}/labels", "POST", {"name": name, "color": color, "description": description})
            print(f"Created label {name}", flush=True)
    existing = all_issues()

    def ensure(key, title, body, label):
        matches = [issue for issue in existing if token(key) in (issue["body"] or "")]
        if len(matches) > 1:
            raise RuntimeError(f"Duplicate migration identity: {title}")
        if matches:
            assert matches[0]["title"] == title
            return matches[0]
        if any(issue["title"] == title for issue in existing):
            raise RuntimeError(f"Existing title requires manual reconciliation: {title}")
        issue = api(f"{BASE}/issues", "POST", {"title": title, "body": body, "labels": [label]})
        existing.append(issue)
        print(f"Created {title}: {issue['html_url']}", flush=True)
        return issue

    source_map = source_map_text()
    title = re.search(r"^# (.+)$", source_map, re.MULTILINE).group(1)
    body = f"{token('map')}\n\n## Destination\n\n{section(source_map, 'Destination')}\n\n## Notes\n\nMigration from the existing local map is in progress. The child issues, evidence assets, resolutions and native dependencies will be linked before verification.\n\n## Decisions so far\n\n## Not yet specified\n\n{section(source_map, 'Not yet specified')}\n\n## Out of scope\n\n{section(source_map, 'Out of scope')}\n"
    remote_map = ensure("map", title, body, "wayfinder:map")
    state["map"] = info(remote_map)
    state["map"].setdefault("body_hash", digest(remote_map["body"]))
    save(state)
    for key, ticket in tickets.items():
        body = child_body(key, ticket, state, tickets, draft=True)
        remote = ensure(key, ticket["title"], body, ticket["fields"]["Labels"])
        old = state["issues"].get(key, {})
        state["issues"][key] = info(remote) | {"body_hash": old.get("body_hash", digest(remote["body"]))}
        save(state)
    print(f"Created/reconciled {len(tickets)} children; map: {state['map']['html_url']}")


def assets(state, tickets):
    assert set(state["issues"]) == set(tickets)
    exports = []
    for source, destination in asset_map().items():
        if destination == Path("CONTEXT.md") or destination == Path("docs/agents/issue-tracker.md"):
            continue
        rendered = rewrite(read(source), source, state, tickets, destination=destination)
        exports.append((destination, rendered))
    index = ["# Audio-first gaming analysis design", "",
             f"Canonical map: [{state['map']['title']}]({state['map']['html_url']}).", "",
             "GitHub Issues holds the live decisions, their dependencies and resolutions. These files preserve the accepted brief and cited research evidence.", "",
             "- [Accepted product brief](brief.md)", "- [Domain glossary](../../../CONTEXT.md)",
             "- [GitHub tracker conventions](../../agents/issue-tracker.md)", "",
             "## Research evidence", ""]
    for key, ticket in tickets.items():
        if ticket["fields"]["Type"] == "research":
            slug = ticket["fields"]["Research branch"].removeprefix("research/audio-analysis-")
            index.append(f"- [{ticket['title']}](research/{slug}.md) — [resolution ticket]({state['issues'][key]['html_url']}).")
    index += ["", "## Provenance", "",
              "The source research was preserved from isolated local `research/audio-analysis-*` worktrees. This documentation branch publishes those reports with links rewritten to GitHub issues and the accompanying assets. Research findings are documented capabilities and hypotheses, not measured application performance.", "",
              "Continue with `/wayfinder` and the canonical map URL. The destination remains an evidence-backed design ready for `/to-spec`.", ""]
    exports.append((ASSETS / "README.md", "\n".join(index)))
    # This command prints a patch for apply_patch; it never edits authored documents.
    print("*** Begin Patch")
    for destination, content in exports:
        if (ROOT / destination).exists():
            raise RuntimeError(f"Refusing to overwrite an existing asset: {destination}")
        print(f"*** Add File: {destination.as_posix()}")
        for line in content.splitlines():
            print("+" + line)
    print("*** End Patch")


def guarded_body(remote_info, body, state):
    remote = api(f"{BASE}/issues/{remote_info['number']}")
    if remote["body"] == body:
        remote_info["body_hash"] = digest(body)
        save(state)
        return
    if digest(remote["body"]) != remote_info["body_hash"]:
        raise RuntimeError(f"Concurrent body edit detected: {remote['title']}")
    api(f"{BASE}/issues/{remote['number']}", "PATCH", {"body": body})
    remote_info["body_hash"] = digest(body)
    save(state)


def check_assets():
    files = [ROOT / "AGENTS.md", ROOT / "CONTEXT.md", *sorted((ROOT / "docs").rglob("*.md"))]
    count = 0
    for path in files:
        text = read(path)
        links = re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", text)
        links += re.findall(r"^\[[^\]\n]+\]:\s*(\S+)\s*$", text, re.MULTILINE)
        for link in links:
            if not link.startswith(("http://", "https://", "mailto:", "#")):
                assert (path.parent / link.split("#", 1)[0]).resolve().exists(), f"Broken link in {path}: {link}"
                count += 1
        assert "C:\\Users\\" not in text and "](.scratch/" not in text
    assert all((ROOT / target).is_file() for target in asset_map().values())
    print(f"Verified {len(files)} published/setup documents, {count} local links, and all seven report targets.")


def publish(state, tickets, revision):
    assert re.fullmatch(r"[0-9a-f]{40}", revision)
    tree = api(f"{BASE}/git/trees/{revision}?recursive=1")
    published = {item["path"] for item in tree["tree"] if item["type"] == "blob"}
    assert all(path.as_posix() in published for path in asset_map().values())
    if state.get("asset_commit") and state["asset_commit"] != revision:
        raise RuntimeError("An asset commit was already selected; inspect before changing it")
    state["asset_commit"] = revision
    save(state)
    map_number = state["map"]["number"]
    children = api(f"{BASE}/issues/{map_number}/sub_issues?per_page=100", paginate=True)
    actual = {child["id"] for child in children}
    expected = {issue["id"] for issue in state["issues"].values()}
    assert actual <= expected, "Map acquired an unexpected child; inspect concurrent work"
    for key, ticket in tickets.items():
        remote = state["issues"][key]
        if remote["id"] not in actual:
            api(f"{BASE}/issues/{map_number}/sub_issues", "POST", {"sub_issue_id": remote["id"]})
        guarded_body(remote, child_body(key, ticket, state, tickets, revision=revision), state)
        print(f"Linked child and evidence: {ticket['title']}", flush=True)
    for key, ticket in tickets.items():
        number = state["issues"][key]["number"]
        blockers = api(f"{BASE}/issues/{number}/dependencies/blocked_by?per_page=100", paginate=True)
        actual = {issue["id"] for issue in blockers}
        expected = {state["issues"][other]["id"] for other in ticket["blockers"]}
        assert actual <= expected, f"Unexpected dependency on {ticket['title']}"
        for other in ticket["blockers"]:
            blocker = state["issues"][other]
            if blocker["id"] not in actual:
                api(f"{BASE}/issues/{number}/dependencies/blocked_by", "POST", {"issue_id": blocker["id"]})
        print(f"Wired dependencies: {ticket['title']}", flush=True)
    login = api("user")["login"]
    for key, ticket in tickets.items():
        if ticket["fields"]["Status"] != "resolved":
            continue
        remote = state["issues"][key]
        comment_marker = token("resolution-" + key)
        answer = section(ticket["text"], "Answer")
        notes = section(ticket["text"], "Comments")
        body = comment_marker + "\n\n## Resolution\n\n" + rewrite(answer, ticket["path"], state, tickets, revision=revision)
        if notes:
            body += "\n\n## Preserved migration/research notes\n\n" + rewrite(notes, ticket["path"], state, tickets, revision=revision)
        body += "\n\n_Migrated from the existing resolved local decision; publication does not represent a new experiment._\n"
        comments = api(f"{BASE}/issues/{remote['number']}/comments?per_page=100", paginate=True)
        matching = [c for c in comments if comment_marker in c["body"]]
        assert len(matching) <= 1
        if not matching:
            api(f"{BASE}/issues/{remote['number']}/comments", "POST", {"body": body})
        else:
            assert matching[0]["body"] == body, "Existing resolution differs; inspect before editing"
        latest = api(f"{BASE}/issues/{remote['number']}")
        if latest["state"] != "closed":
            api(f"{BASE}/issues/{remote['number']}", "PATCH",
                {"state": "closed", "state_reason": "completed", "assignees": [login]})
        print(f"Preserved research resolution: {ticket['title']}", flush=True)
    source_map = source_map_text()
    body = source_map[source_map.index("## Destination"):]
    body = re.sub(r"^- Use the \[local tracker conventions\].*$",
                  "- GitHub Issues is the canonical tracker. Discover open work from this map's native sub-issues and blocking relationships; take the first open, unblocked, unassigned child in sub-issue order. Claim before working and refer to issues by linked title.", body, flags=re.MULTILINE)
    body = re.sub(r"^- Research assets live.*$",
                  f"- [Published planning and research assets]({WEB}/blob/{revision}/{ASSETS.as_posix()}/index.md) preserve the accepted brief and all seven reports. Resolution links are pinned to the published evidence commit; local worktrees remain historical sources.", body, flags=re.MULTILINE)
    body = rewrite(body, EFFORT / "map.md", state, tickets, revision=revision)
    guarded_body(state["map"], token("map") + "\n\n" + body, state)
    state["published"] = True
    save(state)
    print("Published canonical map: " + state["map"]["html_url"])


def verify(state, tickets):
    assert state.get("published"), "Publication phase has not finished"
    parent = api(f"{BASE}/issues/{state['map']['number']}")
    assert parent["state"] == "open" and "wayfinder:map" in {x["name"] for x in parent["labels"]}
    assert digest(parent["body"]) == state["map"]["body_hash"]
    children = api(f"{BASE}/issues/{parent['number']}/sub_issues?per_page=100", paginate=True)
    assert [child["id"] for child in children] == [state["issues"][key]["id"] for key in tickets]
    frontier = []
    edge_count = 0
    closed = 0
    for key, ticket in tickets.items():
        remote = api(f"{BASE}/issues/{state['issues'][key]['number']}")
        assert remote["title"] == ticket["title"]
        assert ticket["fields"]["Labels"] in {x["name"] for x in remote["labels"]}
        assert digest(remote["body"]) == state["issues"][key]["body_hash"]
        assert api(f"{BASE}/issues/{remote['number']}/parent")["id"] == parent["id"]
        dependencies = api(f"{BASE}/issues/{remote['number']}/dependencies/blocked_by?per_page=100", paginate=True)
        assert {x["id"] for x in dependencies} == {state["issues"][x]["id"] for x in ticket["blockers"]}
        edge_count += len(dependencies)
        expected_state = "closed" if ticket["fields"]["Status"] == "resolved" else "open"
        assert remote["state"] == expected_state
        if expected_state == "closed":
            assert remote["state_reason"] == "completed"
            comments = api(f"{BASE}/issues/{remote['number']}/comments?per_page=100", paginate=True)
            assert sum(token("resolution-" + key) in c["body"] for c in comments) == 1
            closed += 1
        else:
            assert not remote["assignees"], "An open decision acquired a claim; inspect concurrent work"
            if all(d["state"] == "closed" for d in dependencies):
                frontier.append({"title": remote["title"], "url": remote["html_url"]})
    assert closed == 7 and len(frontier) == 3
    assert frontier[0]["title"] == tickets["01"]["title"]
    assert ".scratch/" not in parent["body"] and "C:\\Users" not in parent["body"]
    state["verification"] = {"children": len(children), "closed_research": closed,
                             "open": len(children) - closed, "dependencies": edge_count,
                             "frontier": frontier}
    save(state)
    print(json.dumps({"map": parent["html_url"], **state["verification"]}, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["create", "assets", "check-assets", "publish", "verify"])
    parser.add_argument("--revision")
    args = parser.parse_args()
    state, tickets = load()
    if args.phase == "create":
        create(state, tickets)
    elif args.phase == "assets":
        assets(state, tickets)
    elif args.phase == "check-assets":
        check_assets()
    elif args.phase == "publish":
        publish(state, tickets, args.revision)
    else:
        verify(state, tickets)
