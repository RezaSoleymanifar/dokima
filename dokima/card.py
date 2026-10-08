#!/usr/bin/env python3
"""Build the Dokima card and write it at the top of both the issue and its PR.

The card shows the plan's goals and criteria, each with GitHub's own verdict
from that criterion's check. It computes no verdicts itself: a pass appears only
when GitHub recorded the criterion's check as passed on the PR's latest commit.

It runs from the default branch, never from a PR's own code, so the work being
judged cannot change how it is reported. No AI writes the card. On the issue,
the card is the issue's text: its words are the plan, and only the icons and
links change as checks run.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dokima import body, plan  # noqa: E402

WORKER_ACTIVE = {"queued", "in_progress", "requested", "pending", "waiting"}
FULL_SUITE = "all tests"
INDENT = "&emsp;"  # used for the list of edits at the bottom of the card
CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #\d+", re.I)


def icon(repo, name):
    """One of GitHub's own circle icons (Octicons, MIT), served from this repo, centered on its line."""
    url = f"https://raw.githubusercontent.com/{repo}/main/dokima/icons/{name}.svg"
    return f'<img src="{url}" width="16" height="16" align="absmiddle" alt="{name}">'


def state(check):
    """GitHub's verdict for one check run (already filtered to the PR's latest commit)."""
    if check is None:
        return "none"
    if check["status"] != "completed":
        return "running"
    return "passed" if check["conclusion"] == "success" else "failed"


def criterion_line(repo, text, check):
    """One criterion: its circle, then the words "Acceptance criteria" (the link to GitHub's proof once a check exists), then its words."""
    st = state(check)
    word = "Acceptance criteria" if st == "none" else f"[Acceptance criteria]({check['html_url']})"
    return f"{icon(repo, st)} {word}: {text}"


def full_suite_line(repo, check):
    st = state(check)
    if st == "none":
        return f"{icon(repo, st)} Full suite · no check yet"
    return f"{icon(repo, st)} [Full suite]({check['html_url']})"


def checks_by_key(check_runs):
    """Index criterion checks by their key ('67.1') from names like '67.1 · ...'."""
    found = {}
    for run in check_runs:
        key = run["name"].split(" · ")[0]
        if re.fullmatch(r"\d+\.\d+", key):
            found[key] = run
    return found


def stage(approved, worker, pr, criterion_checks, full_suite):
    """Where the work is, in plain words."""
    if pr and pr.get("merged"):
        return "Merged"
    if worker and worker["status"] in WORKER_ACTIVE:
        return "Building"
    if not pr:
        if worker and worker.get("conclusion") == "failure":
            return "The worker stopped"
        return "Building" if approved else "Plan: add `work` to start"
    runs = list(criterion_checks) + ([full_suite] if full_suite else [])
    if not runs:
        return "No checks yet"
    if any(r["status"] != "completed" for r in runs):
        return "Checking"
    if all(r["conclusion"] == "success" for r in runs):
        return "Approve the result to merge"
    return "Checks failing"


def links_row(repo, issue, pr, worker, check_runs, page):
    """The links that matter, minus a link to the page the card is on ("issue" or "pr")."""
    links = []
    if worker:
        links.append(f"[latest run]({worker['html_url']})")
    if page != "issue":
        links.append(f"[issue #{issue['number']}]({issue['url']})")
    if pr and page != "pr":
        links.append(f"[PR #{pr['number']}](https://github.com/{repo}/pull/{pr['number']})")
    if pr:
        links.append(f"[files changed](https://github.com/{repo}/pull/{pr['number']}/files)")
    return " · ".join(links)


def change_line(change):
    if change[0] == "Changed":
        return f"{INDENT}Changed: “{change[1]}” → “{change[2]}”<br>"
    return f"{INDENT}{change[0]}: “{change[1]}”<br>"


def render(repo, issue, words, pr, check_runs, worker, page="issue"):
    """The card for `issue` on `page` ("issue" or "pr"), showing the plan `words` (the approved plan, or the current one)."""
    by_key = checks_by_key(check_runs)
    full_suite = next((r for r in check_runs if r["name"] == FULL_SUITE), None)
    title = stage(issue["approved_at"], worker, pr, list(by_key.values()), full_suite)
    lines = [plan.CARD_START, f"### {title}", links_row(repo, issue, pr, worker, check_runs, page), ""]
    if not words["goals"]:
        lines += ["This issue has no objective and acceptance criteria yet.", ""]
    for goal in words["goals"]:
        # The criteria sit in one indented block (a description list), so every line, wrapped ones too, keeps the indent.
        lines += [f"**Objective: {goal['text']}**", "", "<dl><dd>", ""]
        for c in goal["criteria"]:
            lines.append(criterion_line(repo, c["text"], by_key.get(f"{issue['number']}.{c['n']}")))
            lines.append(f"*Verified by: {c['verified_by'] or 'not stated'}*")
            lines.append("")
        lines += ["</dd></dl>", ""]
    lines += [full_suite_line(repo, full_suite), ""]
    if words["not_checked"]:
        lines += [f"**Not checked:** {words['not_checked']}", ""]
    if issue["changes"]:
        lines.append("**Edited after approval, not in use yet.** Re-add `work` to use it:<br>")
        lines += [change_line(c) for c in issue["changes"]]
        lines.append("")
    lines.append(plan.CARD_END)
    return "\n".join(lines)


def issue_body(card, notes):
    """The issue's text: the card, then any notes, kept as written."""
    return card + ("\n\n" + notes if notes else "")


def pr_body(card, body):
    """The PR's description: the card, then the line linking the issue, and nothing else."""
    found = CLOSES.search(body or "")
    return card + ("\n\n" + found.group(0) if found else "")


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def find_work(repo):
    """The issue and open PR this event is about, as (issue number, PR number or None)."""
    owner = repo.split("/")[0]

    def open_pr(n):
        prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:work/issue-{n}&state=all"))
        return prs[0]["number"] if prs else None

    if os.environ.get("ISSUE_NUMBER"):
        n = int(os.environ["ISSUE_NUMBER"])
        return n, open_pr(n)
    title = re.match(r"worker for #(\d+)$", os.environ.get("RUN_TITLE", ""))
    if title:
        n = int(title.group(1))
        return n, open_pr(n)
    pr = os.environ.get("PR_NUMBER")
    if not pr:
        prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
        pr = prs[0]["number"] if prs else None
    if not pr:
        return None, None
    return plan.pr_issue_number(repo, pr), int(pr)


def latest_worker_run(repo, number):
    runs = json.loads(gh("api", f"repos/{repo}/actions/workflows/worker.yml/runs?per_page=50"))["workflow_runs"]
    run = next((r for r in runs if r["display_title"] == f"worker for #{number}"), None)
    return {"status": run["status"], "conclusion": run["conclusion"], "html_url": run["html_url"]} if run else None


def main():
    repo = os.environ["REPO"]
    number, pr_number = find_work(repo)
    if not number:
        print("No issue for this event; nothing to write.")
        return
    issue = plan.fetch_issue(repo, number)
    worker = latest_worker_run(repo, number)
    pr, check_runs = None, []
    if pr_number:
        pr = json.loads(gh("api", f"repos/{repo}/pulls/{pr_number}"))
        check_runs = json.loads(gh("api", f"repos/{repo}/commits/{pr['head']['sha']}/check-runs?per_page=100"))["check_runs"]
    # The issue keeps its current words, so rewriting it never erases an edit; the PR shows the approved plan.
    # Only the part above the marker is code's; the owner's ask below it is saved as it is, or the save is refused.
    text = issue["current_body"] or ""
    current = plan.parse(text.split(body.MARKER, 1)[0])
    notes = current["notes"] if body.MARKER in text else ""
    if body.save(repo, number, text, issue_body(render(repo, issue, current, pr, check_runs, worker), notes)):
        print(f"Card written into issue #{number}")
    if pr and pr["state"] == "open":
        with open("pr.md", "w") as f:
            f.write(pr_body(render(repo, issue, issue["plan"], pr, check_runs, worker, page="pr"), pr.get("body")))
        gh("api", "-X", "PATCH", f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md")
        print(f"Card written into PR #{pr_number}")


if __name__ == "__main__":
    main()
