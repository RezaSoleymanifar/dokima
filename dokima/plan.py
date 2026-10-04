#!/usr/bin/env python3
"""The plan: what it says, who approved it, and what changed since.

An issue's plan is approved when an approver adds the `work` label. Approvers
are the code owners in CODEOWNERS (the owners of `*`), or the repository owner
when there is no such file. The plan is frozen at the moment the label was
added: the worker, the checks and the card all read the issue as it stood then,
taken from GitHub's own edit history. Edits made while the label is on are not
used; the card lists what changed. To use them, remove `work` and add it again.

The plan is read from the card (the issue's text once the card has been written
into it) or from the older checkbox format. Only words count: the card's icons
and links change as checks run, but they are never part of the plan.
"""
import difflib
import json
import os
import re
import subprocess
import sys

LABEL = "work"
WORK_BRANCH = re.compile(r"work/issue-(\d+)")
CARD_START = "<!-- dokima-card -->"
CARD_END = "<!-- /dokima-card -->"

# Older checkbox format: "- [ ] Goal: ..." then indented "- [ ] Done when: ..." and "Verified by: ...".
CHECKBOX = re.compile(r"^(\s*)[-*] \[( |x|X)\] (.+)$")
VERIFIED = re.compile(r"^\s+Verified by:\s*(.+)$", re.I)
CRITERION_PREFIX = re.compile(r"^(?:Done when|Criteria|Criterion):\s*", re.I)
GOAL_PREFIX = re.compile(r"^Goal:\s*", re.I)
NOT_CHECKED = re.compile(r"^\*\*Not checked:\*\*\s*(.+)$", re.I)
# Card format, written by the card workflow.
CARD_GOAL = re.compile(r"^\*\*Goal: (.+)\*\*$")
CARD_CRITERION = re.compile(r'^(?:&emsp;)?<img [^>]*alt="(?:passed|failed|running|none)"[^>]*> (?:\[(.*)\]\(https?://[^)\s]*\)|(.*?))<br>$')
CARD_VERIFIED = re.compile(r"^(?:&emsp;)?<sub>Verified by: (.*)</sub>$")
# Current card layout: criteria sit inside an indented block, as their circle, then
# the word "Criteria" (a link once checked), then their words.
BLOCK_CRITERION = re.compile(r'^<img [^>]*alt="(?:passed|failed|running|none)"[^>]*> (?:\[Criteria\]\(https?://[^)\s]*\)|Criteria): (.*?)(?:<br>)?$')
BLOCK_VERIFIED = re.compile(r"^\*?Verified by: (.*?)\*?$")


def parse(body):
    """The plan's words: goals with their criteria (numbered from 1 across the issue), Not checked, and notes.

    Notes are any other lines outside the card, kept as they were written.
    """
    goals, n, gap, notes, in_card = [], 0, None, [], False
    for line in (body or "").splitlines():
        stripped = line.strip()
        if stripped == CARD_START:
            in_card = True
            continue
        if stripped == CARD_END:
            in_card = False
            continue
        goal = CARD_GOAL.match(stripped)
        crit = (BLOCK_CRITERION.match(stripped) if in_card else None) or CARD_CRITERION.match(stripped)
        ver = (BLOCK_VERIFIED.match(stripped) if in_card else None) or CARD_VERIFIED.match(stripped)
        box = CHECKBOX.match(line)
        checked = NOT_CHECKED.match(stripped)
        if goal or (box and not box.group(1)):
            goals.append({"text": GOAL_PREFIX.sub("", (goal.group(1) if goal else box.group(3)).strip()), "criteria": []})
        elif (crit or box) and goals:
            n += 1
            text = next(g for g in crit.groups() if g is not None) if crit else box.group(3)
            goals[-1]["criteria"].append({"n": n, "text": CRITERION_PREFIX.sub("", text.strip()), "verified_by": None})
        elif (ver or VERIFIED.match(line)) and goals and goals[-1]["criteria"]:
            goals[-1]["criteria"][-1]["verified_by"] = (ver or VERIFIED.match(line)).group(1).strip()
        elif checked:
            gap = checked.group(1).strip()
        elif not in_card:
            notes.append(line)
    while notes and not notes[0].strip():
        notes.pop(0)
    while notes and not notes[-1].strip():
        notes.pop()
    return {"goals": goals, "not_checked": gap, "notes": "\n".join(notes)}


def lines(plan):
    """The plan as plain lines of words, for comparing two versions."""
    out = []
    for goal in plan["goals"]:
        out.append(f"Goal: {goal['text']}")
        for c in goal["criteria"]:
            out.append(c["text"])
            out.append(f"Verified by: {c['verified_by'] or ''}")
    if plan["not_checked"]:
        out.append(f"Not checked: {plan['not_checked']}")
    return out


def changes(approved, current):
    """What changed in the plan's words since it was approved, as ("Changed", old, new), ("Added", new) or ("Removed", old)."""
    a, b = lines(approved), lines(current)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "replace":
            olds, news = a[i1:i2], b[j1:j2]
            for k in range(max(len(olds), len(news))):
                if k < len(olds) and k < len(news):
                    out.append(("Changed", olds[k], news[k]))
                elif k < len(news):
                    out.append(("Added", news[k]))
                else:
                    out.append(("Removed", olds[k]))
        elif op == "insert":
            out += [("Added", x) for x in b[j1:j2]]
        elif op == "delete":
            out += [("Removed", x) for x in a[i1:i2]]
    return out


def approvers(codeowners, repo_owner):
    """The people whose approval counts: the owners of `*` in CODEOWNERS, else the repository owner."""
    for line in (codeowners or "").splitlines():
        parts = line.split("#")[0].split()
        if parts and parts[0] == "*" and len(parts) > 1:
            return {name.lstrip("@") for name in parts[1:]}
    return {repo_owner}


def repo_approvers(repo_owner, root="."):
    path = os.path.join(root, ".github", "CODEOWNERS")
    return approvers(open(path).read() if os.path.exists(path) else "", repo_owner)


def approved_at(events, approver_names):
    """When an approver last added the `work` label, if it is still on; else None. Nobody else's label counts."""
    added = [e["created_at"] for e in events if e.get("event") == "labeled"
             and (e.get("label") or {}).get("name") == LABEL and (e.get("actor") or {}).get("login") in approver_names]
    removed = [e["created_at"] for e in events if e.get("event") == "unlabeled"
               and (e.get("label") or {}).get("name") == LABEL]
    if not added or (removed and max(removed) >= max(added)):
        return None
    return max(added)


def approved_version(body, edits, at):
    """The issue text as it stood at time `at`. `edits` come from GitHub's edit history, each the full text."""
    if not at or not edits:
        return body
    before = [e for e in edits if e["editedAt"] <= at]
    return max(before, key=lambda e: e["editedAt"])["diff"] if before else body


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def fetch_issue(repo, number):
    """The issue with its plan as approved (or as it is, when not approved) and what changed since."""
    owner, name = repo.split("/")
    query = ("query($o:String!,$n:String!,$i:Int!){repository(owner:$o,name:$n){issue(number:$i)"
             "{number title body url userContentEdits(first:100){nodes{editedAt diff}}}}}")
    data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}", "-F", f"i={number}"))
    issue = data["data"]["repository"]["issue"]
    edits = [e for e in issue.pop("userContentEdits")["nodes"] if e.get("diff") is not None]
    events = json.loads(gh("api", f"repos/{repo}/issues/{number}/events?per_page=100", "--paginate"))
    at = approved_at(events, repo_approvers(owner))
    current = parse(issue["body"])
    approved = parse(approved_version(issue["body"], edits, at)) if at else current
    issue.update(approved_at=at, plan=approved, current_body=issue["body"],
                 changes=changes(approved, current) if at else [])
    return issue


def pr_issue_number(repo, pr):
    """The issue a PR closes, or None."""
    owner, name = repo.split("/")
    query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
             "{closingIssuesReferences(first:1){nodes{number}}}}}")
    data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}", "-F", f"p={pr}"))
    nodes = data["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]
    return nodes[0]["number"] if nodes else None


def as_text(number, title, plan):
    """The approved plan as plain text, for the worker to read."""
    out = [f"Issue #{number}: {title}", ""]
    for goal in plan["goals"]:
        out.append(f"- Goal: {goal['text']}")
        for c in goal["criteria"]:
            out.append(f"  - Criterion {number}.{c['n']}: {c['text']}")
            out.append(f"    Verified by: {c['verified_by'] or 'not stated'}")
    if plan["not_checked"]:
        out += ["", f"Not checked: {plan['not_checked']}"]
    if plan["notes"]:
        out += ["", plan["notes"]]
    return "\n".join(out)


def main(argv):
    if argv[1] == "approvers":
        # Comma-separated approvers.
        print(",".join(sorted(repo_approvers(os.environ["GITHUB_REPOSITORY_OWNER"]))))
    elif argv[1] == "issue":
        # The issue's plan as approved, for the worker to read.
        issue = fetch_issue(os.environ["GITHUB_REPOSITORY"], argv[2])
        print(as_text(issue["number"], issue["title"], issue["plan"]))


if __name__ == "__main__":
    main(sys.argv)
