#!/usr/bin/env python3
"""The approved plan: who can start a build, and what the plan said when they did.

An approver starts a build with GitHub's own Approve button on the worker's
pull request. Approvers are the code owners in the repo's CODEOWNERS file (the
owners of `*`), or the repository owner when there is no such file. From that
moment the plan is frozen: the worker, the gate and the card all read the issue
as it was when it was approved, taken from GitHub's own edit history. Later
edits change nothing, and the card lists them as ignored.
"""
import json
import os
import re
import subprocess
import sys

WORK_BRANCH = re.compile(r"work/issue-(\d+)")
# A dismissed review keeps its submit time; new commits dismiss the plan
# approval (dismiss stale reviews is on), so it still marks when the plan was approved.
APPROVAL_STATES = {"APPROVED", "DISMISSED"}


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


def starts_build(state, reviewer, approver_names, branch, commits):
    """True only for an approver's approval on a worker PR that has no work yet (just its start commit)."""
    return (state.lower() == "approved" and reviewer in approver_names
            and bool(WORK_BRANCH.fullmatch(branch)) and commits == 1)


def approved_at(reviews, approver_names):
    """When an approver first approved this PR, or None. Nobody else's approval counts."""
    times = [r["submitted_at"] for r in reviews
             if r["user"]["login"] in approver_names and r["state"] in APPROVAL_STATES and r.get("submitted_at")]
    return min(times) if times else None


def approved_version(body, edits, at):
    """The issue text as it stood at time `at`. `edits` come from GitHub's edit history, each the full text."""
    if not at or not edits:
        return body
    before = [e for e in edits if e["editedAt"] <= at]
    return max(before, key=lambda e: e["editedAt"])["diff"] if before else body


def edits_after(edits, at):
    """Edits made after the approval, oldest first: these are ignored."""
    if not at:
        return []
    later = [e for e in edits if e["editedAt"] > at]
    return [{"at": e["editedAt"], "by": (e.get("editor") or {}).get("login", "someone")}
            for e in sorted(later, key=lambda e: e["editedAt"])]


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def approved_issue(repo, pr):
    """The PR's linked issue, with its body as approved and the list of ignored later edits."""
    owner, name = repo.split("/")
    query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
             "{closingIssuesReferences(first:1){nodes{number title body url"
             " userContentEdits(first:100){nodes{editedAt diff editor{login}}}}}}}}")
    data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}", "-F", f"p={pr}"))
    nodes = data["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]
    if not nodes:
        return None
    issue = nodes[0]
    edits = [e for e in issue.pop("userContentEdits")["nodes"] if e.get("diff") is not None]
    at = approved_at(json.loads(gh("api", f"repos/{repo}/pulls/{pr}/reviews?per_page=100")), repo_approvers(owner))
    issue["body"] = approved_version(issue["body"], edits, at)
    issue["approved_at"] = at
    issue["edited_after"] = edits_after(edits, at)
    return issue


def main(argv):
    if argv[1] == "starts":
        # Used by the build workflow: prints start=true|false for GITHUB_OUTPUT.
        state, reviewer, branch, commits = argv[2:6]
        names = repo_approvers(os.environ["GITHUB_REPOSITORY_OWNER"])
        print("start=" + str(starts_build(state, reviewer, names, branch, int(commits))).lower())
    elif argv[1] == "issue":
        # Writes the issue text as approved, for the worker to read.
        issue = approved_issue(os.environ["GITHUB_REPOSITORY"], argv[2])
        print(f"Issue #{issue['number']}: {issue['title']}\n\n{issue['body']}")


if __name__ == "__main__":
    main(sys.argv)
