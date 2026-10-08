#!/usr/bin/env python3
"""Build the Dokima card and write it at the top of both the issue and its PR.

The card shows the plan's user story and criteria, each with GitHub's own verdict
from that criterion's check. It computes no verdicts itself: a pass appears only
when GitHub recorded the criterion's check as passed on the PR's latest commit.

It runs from the default branch, never from a PR's own code, so the work being
judged cannot change how it is reported. No AI writes the card. It is drawn only
from the agents' records and GitHub's checks and reviews, never from the issue's
text, so the issue and its PR show the same card.
"""
import ast
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dokima import body, plan  # noqa: E402

WORKER_ACTIVE = {"queued", "in_progress", "requested", "pending", "waiting"}
ALL_TESTS = "all tests"
ICON_FILE = {"passed": "passed", "failed": "failed", "running": "running", "not started": "none"}
CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #\d+", re.I)


def icon(repo, name, alt=None):
    """One of GitHub's own circle icons (Octicons, MIT), served from this repo, centered on its line."""
    url = f"https://raw.githubusercontent.com/{repo}/main/dokima/icons/{name}.svg"
    return f'<img src="{url}" width="16" height="16" align="absmiddle" alt="{alt or name}">'


def state(check):
    """GitHub's verdict for one check run (already filtered to the PR's latest commit): passed, failed, running or not started."""
    if check is None:
        return "not started"
    if check["status"] == "completed":
        return "passed" if check["conclusion"] == "success" else "failed"
    return "running" if check["status"] == "in_progress" else "not started"


def circle(repo, st, url=None):
    """The verdict circle for state `st`, linked to its proof when there is one."""
    img = icon(repo, ICON_FILE[st], alt=st)
    return f'<a href="{url}">{img}</a>' if url else img


def escape(text):
    return html.escape(text or "", quote=False)


def checks_by_key(check_runs):
    """Index criterion checks by their key ('67.1') from names like '67.1 · ...'."""
    found = {}
    for run in check_runs:
        key = run["name"].split(" · ")[0]
        if re.fullmatch(r"\d+\.\d+", key):
            found[key] = run
    return found


def stage(approved, worker, pr, criterion_checks, all_tests):
    """Where the work is, in plain words."""
    if pr and pr.get("merged"):
        return "Merged"
    if worker and worker["status"] in WORKER_ACTIVE:
        return "Building"
    if not pr:
        if worker and worker.get("conclusion") == "failure":
            return "The worker stopped"
        return "Building" if approved else "Plan: add `work` to start"
    runs = list(criterion_checks) + ([all_tests] if all_tests else [])
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


def criterion_row(repo, text, check, tests):
    """One criterion as a table row: its circle alone in the first cell, hanging outside its words, linked to its check;
    then its words and, when any of its tests has a docstring, Verified by with each one linking to its test."""
    st = state(check)
    words = escape(text)
    proofs = [f'<a href="{t["url"]}">{escape(t["verified_by"])}</a>' for t in tests if t and t.get("verified_by")]
    if proofs:
        words += "<br>Verified by: " + "; ".join(proofs)
    return f"<tr><td>{circle(repo, st, check and check['html_url'])}</td><td>{words}</td></tr>"


def criteria_table(repo, number, start, criteria, plan_tests, by_key, tests):
    """The table of criteria numbered from `start`, each row with its own check and tests."""
    out = ["<table>"]
    for k, c in enumerate(criteria, start):
        key = f"{number}.{k}"
        out.append(criterion_row(repo, c.get("text"), by_key.get(key), [tests.get(t) for t in plan_tests.get(key, [])]))
    return out + ["</table>"]


def code_review(recs):
    """The newest code review whose record passed its check, since the worker last built; None when there is none."""
    builds = [i for i, r in enumerate(recs) if r.get("role") == "worker"]
    after = recs[builds[-1] + 1:] if builds else recs
    reviews = [r for r in after if r.get("role") == "reviewer" and r.get("stage") == "pr" and r.get("check", {}).get("passed")]
    return reviews[-1] if reviews else None


def owner_review(reviews, owners):
    """The newest Approve or Request changes on the PR by a code owner; None when there is none."""
    found = [r for r in reviews if r.get("state") in ("APPROVED", "CHANGES_REQUESTED")
             and (r.get("user") or {}).get("login") in owners]
    return found[-1] if found else None


def done_row(repo, found, all_tests):
    """The Definition of Done: All tests, the code review and the owner's approval, each with its verdict and proof."""
    review = code_review(found["recs"])
    review_st = "not started" if not review else "passed" if review["handback"].get("verdict") == "approve" else "failed"
    approval = owner_review(found["reviews"], found["owners"])
    approval_st = "not started" if not approval else "passed" if approval["state"] == "APPROVED" else "failed"
    return ("**Definition of Done:** "
            f"{circle(repo, state(all_tests), all_tests and all_tests['html_url'])} All tests · "
            f"{circle(repo, review_st, review and review.get('run'))} Code review · "
            f"{circle(repo, approval_st, approval and approval.get('html_url'))} Owner approval")


def render(repo, issue, found, page="issue"):
    """The card for `issue` on `page` ("issue" or "pr"), drawn only from `found`: the agents' records, the PR, its
    latest commit's checks, its reviews, the code owners, the plan's tests and the latest worker run."""
    from dokima import agent
    recs, pr, check_runs, worker = found["recs"], found["pr"], found["check_runs"], found["worker"]
    by_key = checks_by_key(check_runs)
    all_tests = next((r for r in check_runs if r["name"] == ALL_TESTS), None)
    title = stage(agent.approved(recs), worker, pr, list(by_key.values()), all_tests)
    lines = [plan.CARD_START, f"### {title}", links_row(repo, issue, pr, worker, check_runs, page), ""]
    planned = agent.latest(recs, "planner")
    h = planned["handback"] if planned else None
    if not h:
        lines += ["This issue has no plan yet.", ""]
    else:
        criteria, nfr = h.get("acceptance_criteria") or [], h.get("non_functional") or []
        tests, plan_tests = found["tests"], h.get("tests") or {}
        if h.get("user_story"):
            lines += [f"**User story:** {escape(h['user_story'])}", ""]
        lines += ["**Acceptance criteria**", ""]
        lines += criteria_table(repo, issue["number"], 1, criteria, plan_tests, by_key, tests) + [""]
        if nfr:
            lines += ["<details><summary><b>Non-functional requirements</b></summary>", ""]
            lines += criteria_table(repo, issue["number"], len(criteria) + 1, nfr, plan_tests, by_key, tests)
            lines += ["", "</details>", ""]
        lines += ["**Scope:**", ""] + [f"- {escape(s)}" for s in h.get("scope") or []] + [""]
        lines += ["**Out of scope:**", ""] + [f"- {escape(s)}" for s in h.get("out_of_scope") or []] + [""]
    lines += [done_row(repo, found, all_tests), "", plan.CARD_END]
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
        for branch in (f"try/issue-{n}", f"work/issue-{n}"):
            prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
            if prs:
                return prs[0]["number"]
        return None

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


def test_entry(repo, ref, path, source, name):
    """One test's Verified by (its docstring's first line, or None) and the link to the line it starts on at `ref`."""
    url = f"https://github.com/{repo}/blob/{ref}/{path}"
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"verified_by": None, "url": url}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            doc = (ast.get_docstring(node) or "").strip()
            return {"verified_by": doc.splitlines()[0] if doc else None, "url": f"{url}#L{node.lineno}"}
    return {"verified_by": None, "url": url}


def file_at(repo, path, ref=None):
    """A file's text at `ref` (the default branch when None), or None when GitHub has no such file."""
    target = f"repos/{repo}/contents/{path}" + (f"?ref={ref}" if ref else "")
    try:
        return gh("api", target, "-H", "Accept: application/vnd.github.raw")
    except subprocess.CalledProcessError:
        return None


def gather(repo, number, pr_number):
    """Everything the card is drawn from, fetched from GitHub: never the issue's text."""
    from dokima import agent
    _, items = agent.conversation(repo, number)
    recs = agent.records(items)
    pr, check_runs, reviews = None, [], []
    if pr_number:
        pr = json.loads(gh("api", f"repos/{repo}/pulls/{pr_number}"))
        check_runs = json.loads(gh("api", f"repos/{repo}/commits/{pr['head']['sha']}/check-runs?per_page=100"))["check_runs"]
        reviews = json.loads(gh("api", f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100"))
    # Code owners are read from the default branch, never from the PR's own commit.
    owners = plan.approvers(file_at(repo, ".github/CODEOWNERS") or "", repo.split("/")[0])
    ref = pr["head"]["sha"] if pr else f"try/issue-{number}"
    planned = agent.latest(recs, "planner")
    tests, sources = {}, {}
    for t in sorted({t for ts in ((planned or {}).get("handback", {}).get("tests") or {}).values() for t in ts}):
        path, _, name = t.partition("::")
        if path not in sources:
            sources[path] = file_at(repo, path, ref)
        if sources[path] is not None:
            tests[t] = test_entry(repo, ref, path, sources[path], name)
    return {"recs": recs, "pr": pr, "check_runs": check_runs, "reviews": reviews, "owners": owners,
            "tests": tests, "worker": latest_worker_run(repo, number)}


def main():
    repo = os.environ["REPO"]
    number, pr_number = find_work(repo)
    if not number:
        print("No issue for this event; nothing to write.")
        return
    issue = plan.fetch_issue(repo, number)
    found = gather(repo, number, pr_number)
    pr = found["pr"]
    # Only the part above the marker is code's; the owner's ask below it is saved as it is, or the save is refused.
    if body.save(repo, number, issue["current_body"] or "", render(repo, issue, found)):
        print(f"Card written into issue #{number}")
    if pr and pr["state"] == "open":
        with open("pr.md", "w") as f:
            f.write(pr_body(render(repo, issue, found, page="pr"), pr.get("body")))
        gh("api", "-X", "PATCH", f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md")
        print(f"Card written into PR #{pr_number}")


if __name__ == "__main__":
    main()
