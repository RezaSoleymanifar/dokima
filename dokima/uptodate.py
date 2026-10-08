"""Bring every open PR that fell behind main up to date with GitHub's own Update branch, after each merge to main.

    python3 -m dokima.uptodate     # reads GITHUB_REPOSITORY, GITHUB_REF_NAME and GITHUB_SHA

Rules live in run() and clash(); the GitHub calls go through rest(method, path, **fields), shaped like dokima.board.api.
A clash on a Dokima PR (try/issue-N in this repo) leaves a record on issue N and starts its planner; a clash on any
other PR mentions the code owners on it and starts nothing.
"""
import json
import os
import re
import subprocess
import sys

from dokima import agent, plan
from dokima.board import api

PER_PAGE = 100


def open_prs(repo, base, rest):
    """Every open PR into base, drafts included."""
    out, page = [], 1
    while True:
        batch = rest("GET", f"repos/{repo}/pulls?state=open&base={base}&per_page={PER_PAGE}&page={page}")
        out += [p for p in batch if p.get("base", {}).get("ref") == base]
        if len(batch) < PER_PAGE:
            return out
        page += 1


def reason(e):
    """GitHub's own reason for refusing a call: its JSON message, else gh's one-line error."""
    try:
        message = json.loads(e.output or "").get("message")
    except (ValueError, AttributeError):
        message = None
    return message or (e.stderr or "").strip() or str(e)


def run(repo, base, sha, rest=api, on_clash=None):
    """Update every open PR into base whose branch is behind it; a refused PR gets one comment saying why.

    on_clash(pr, sha) is called for each PR GitHub refuses with a merge conflict. Returns (updated, refused) numbers."""
    updated, refused = [], []
    for pr in open_prs(repo, base, rest):
        n, head = pr["number"], pr["head"]["sha"]
        if not rest("GET", f"repos/{repo}/compare/{base}...{head}").get("behind_by"):
            continue
        try:
            rest("PUT", f"repos/{repo}/pulls/{n}/update-branch", expected_head_sha=head)
        except subprocess.CalledProcessError as e:
            why = reason(e)
            refused.append(n)
            rest("POST", f"repos/{repo}/issues/{n}/comments",
                 body=f"This pull request could not be updated with `{base}` ({sha[:7]}). GitHub said: {why}")
            if on_clash and "merge conflict" in why.lower():
                on_clash(pr, sha)
            continue
        updated.append(n)
    return updated, refused


def trial_merge(base, sha, pr):
    """The paths that clash when the PR's head merges with `sha`, from a trial merge in this checkout that leaves its
    files untouched; what it needs is fetched from the `origin` remote."""
    n = pr["number"]
    subprocess.run(["git", "fetch", "-q", "origin", f"+refs/heads/{base}:refs/remotes/origin/{base}",
                    f"+refs/pull/{n}/head:refs/dokima/pr-{n}"], check=True, capture_output=True, text=True)
    main = sha if subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], capture_output=True).returncode == 0 \
        else f"origin/{base}"
    p = subprocess.run(["git", "merge-tree", "--write-tree", "--name-only", "--no-messages", f"refs/dokima/pr-{n}", main],
                       capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise subprocess.CalledProcessError(p.returncode, p.args, p.stdout, p.stderr)
    return sorted(set(p.stdout.splitlines()[1:])) if p.returncode == 1 else []


def merged_pr(repo, sha, rest):
    """The PR whose merge put `sha` on main, or None when it came with no PR."""
    pulls = rest("GET", f"repos/{repo}/commits/{sha}/pulls")
    return next((p["number"] for p in pulls or [] if p.get("merged_at")), None)


def history(repo, number, rest):
    """The issue's comments, oldest first, shaped as the river reads them: the bot's REST login is its plain name."""
    out, page = [], 1
    while True:
        batch = rest("GET", f"repos/{repo}/issues/{number}/comments?per_page={PER_PAGE}&page={page}")
        for c in batch:
            login = (c.get("user") or {}).get("login")
            out.append({"author": {"login": agent.BOT if login == f"{agent.BOT}[bot]" else login},
                        "body": c.get("body") or "", "createdAt": c.get("created_at")})
        if len(batch) < PER_PAGE:
            return out
        page += 1


def planner_waiting(items):
    """True when the newest clash record has had no planner run answer it yet: its planner is queued or running."""
    recs = agent.records(items)
    at = max((i for i, r in enumerate(recs) if r.get("role") == "updater"), default=None)
    return at is not None and not any("planner" in (r.get("role"), r.get("attempt")) for r in recs[at + 1:])


def dokima_issue(repo, pr):
    """Issue N when the PR is Dokima's own, from branch try/issue-N of this same repo; otherwise None."""
    head = pr.get("head") or {}
    m = re.fullmatch(r"try/issue-(\d+)", head.get("ref") or "")
    return int(m.group(1)) if m and ((head.get("repo") or {}).get("full_name") == repo) else None


def clash(repo, base, sha, pr, rest=api, files=None, owners=None):
    """Handle one PR that clashes with base after merge `sha`. A Dokima PR leaves one record on its issue naming the
    merge, its PR and every clashed file, then starts the planner, unless a clash record is still waiting for it. Any
    other PR gets one comment saying the same and mentioning the code owners; no agent starts."""
    n = pr["number"]
    try:
        clashed, why = sorted((files or (lambda p, s: trial_merge(base, s, p)))(pr, sha)), None
    except subprocess.CalledProcessError as e:
        clashed, why = [], f"Code could not list the clashed files: {(e.stderr or str(e)).strip()}"
    by = merged_pr(repo, sha, rest)
    issue = dokima_issue(repo, pr)
    if issue is None:
        who = sorted(owners if owners is not None else plan.repo_approvers(repo.split("/")[0]))
        lines = [f"This pull request clashes with `{base}` since {sha[:7]}" + (f" (#{by})" if by else "") + " merged, in:", ""]
        lines += [f"- `{f}`" for f in clashed] or [f"- {why}"]
        lines += ["", f"**Next:** {' '.join('@' + o for o in who)} Dokima didn't build this pull request, so it starts "
                      "nothing: resolve the clash on its branch."]
        rest("POST", f"repos/{repo}/issues/{n}/comments", body="\n".join(lines) + "\n")
        return
    waiting = planner_waiting(history(repo, issue, rest))
    server, run_id = os.environ.get("GITHUB_SERVER_URL", "https://github.com"), os.environ.get("GITHUB_RUN_ID")
    rec = {"role": "updater", "stage": None, **({"run": f"{server}/{repo}/actions/runs/{run_id}"} if run_id else {}),
           "handback": {"base": base, "merge": sha, "merged_pr": by, "pr": n, "files": clashed, **({"why": why} if why else {})},
           "check": {"passed": True, "problems": []}}
    step = ("start", "planner", "")
    nxt = "**Next:** The planner started by an earlier clash re-plans against the newest main." if waiting \
        else agent.next_line(step, ())
    rest("POST", f"repos/{repo}/issues/{issue}/comments", body=agent.render(rec) + "\n" + nxt + "\n")
    if not waiting:
        rest("POST", f"repos/{repo}/dispatches", event_type="dokima-next", **{
            "client_payload[role]": "planner", "client_payload[stage]": "plan", "client_payload[issue]": str(issue)})


def main():
    repo, base, sha = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_REF_NAME"], os.environ["GITHUB_SHA"]
    failed = []

    def on_clash(pr, at):
        try:
            clash(repo, base, at, pr)
        except subprocess.CalledProcessError as e:
            failed.append(pr["number"])
            print(f"::error::uptodate: the clash on #{pr['number']} could not be handled: {reason(e)}")

    updated, refused = run(repo, base, sha, on_clash=on_clash)
    for n in updated:
        print(f"uptodate: updated #{n}")
    for n in refused:
        print(f"::warning::uptodate: #{n} could not be updated")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
