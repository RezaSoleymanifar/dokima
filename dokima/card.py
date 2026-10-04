#!/usr/bin/env python3
"""Build and post the Dokima card on a pull request.

The card is the PR's front page: its stage, the links that matter, and each
done-when of the linked issue with GitHub's own verdict from that done-when's
check. It computes no verdicts itself: ✅ appears only when GitHub recorded the
done-when's check as passed on the PR's latest commit.

It runs from the default branch (a workflow_run trigger), never from the PR's
own code, so the work being judged cannot change how it is reported. No AI
writes the card.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dokima import plan  # noqa: E402

MARKER = "<!-- dokima-card -->"
CHECKBOX = re.compile(r"^(\s*)[-*] \[( |x|X)\] (.+)$")
VERIFIED = re.compile(r"^\s+Verified by:\s*(.+)$", re.I)
DONE_PREFIX = re.compile(r"^Done when:\s*", re.I)
NOT_CHECKED = re.compile(r"^\*\*Not checked:\*\*\s*(.+)$", re.I)
WORKER_ACTIVE = {"queued", "in_progress", "requested", "pending", "waiting"}
FULL_SUITE = "all tests"


def parse_issue(body):
    """Goals, each with its done-whens (numbered from 1 across the issue) and how each is verified."""
    goals, n = [], 0
    for line in (body or "").splitlines():
        box = CHECKBOX.match(line)
        if box:
            indent, _, text = box.groups()
            if not indent:
                goals.append({"text": text.strip(), "done_whens": []})
            elif goals:
                n += 1
                goals[-1]["done_whens"].append({"n": n, "text": DONE_PREFIX.sub("", text.strip()), "verified_by": None})
            continue
        verified = VERIFIED.match(line)
        if verified and goals and goals[-1]["done_whens"]:
            goals[-1]["done_whens"][-1]["verified_by"] = verified.group(1).strip()
    return goals


def not_checked(body):
    for line in (body or "").splitlines():
        m = NOT_CHECKED.match(line.strip())
        if m:
            return m.group(1).strip()
    return None


def verdict(check):
    """GitHub's verdict for one check run (already filtered to the PR's latest commit)."""
    if check is None:
        return "⚠️", "no check yet"
    if check["status"] != "completed":
        return "⏳", f"[running]({check['html_url']})"
    if check["conclusion"] == "success":
        return "✅", f"[proof]({check['html_url']})"
    return "❌", f"[proof]({check['html_url']})"


def done_when_line(text, check):
    """One done-when: the verdict word is the link to GitHub's proof."""
    if check is None:
        return f"⚠️ Done when: {text} · no check yet"
    url = check["html_url"]
    if check["status"] != "completed":
        return f"⏳ [Checking]({url}): {text}"
    if check["conclusion"] == "success":
        return f"✅ [Done]({url}): {text}"
    return f"❌ [Failing]({url}): {text}"


def checks_by_key(check_runs):
    """Index done-when checks by their key ('29.1') from names like '29.1 · ...'."""
    found = {}
    for run in check_runs:
        key = run["name"].split(" · ")[0]
        if re.fullmatch(r"\d+\.\d+", key):
            found[key] = run
    return found


def stage(worker, done_when_checks, full_suite):
    """The task's current stage, in plain words."""
    if worker and worker["status"] == "waiting":
        return "Waiting for your approval"
    if worker and worker["status"] in WORKER_ACTIVE:
        return "Building"
    runs = list(done_when_checks) + ([full_suite] if full_suite else [])
    if not runs:
        return "No checks yet"
    if any(r["status"] != "completed" for r in runs):
        return "Checking"
    if all(r["conclusion"] == "success" for r in runs):
        return "Approve the result to merge"
    return "Checks failing"


def live_run(worker, check_runs):
    """Whatever is running now: the worker first, then any running check; None when nothing runs."""
    if worker and worker["status"] in WORKER_ACTIVE - {"waiting"}:
        return worker["html_url"]
    for run in check_runs:
        if run["status"] != "completed":
            return run["html_url"]
    return None


def links_row(repo, pr, issue, worker, check_runs):
    links = []
    if worker and worker["status"] == "waiting":
        links.append(f"[Approve the plan]({worker['html_url']})")
    live = live_run(worker, check_runs)
    if live:
        links.append(f"[live run]({live})")
    if issue:
        links.append(f"[issue #{issue['number']}]({issue['url']})")
    links.append(f"[files changed](https://github.com/{repo}/pull/{pr}/files)")
    return " · ".join(links)


def render(repo, pr, issue, check_runs, worker):
    goals = parse_issue(issue["body"]) if issue else []
    by_key = checks_by_key(check_runs)
    full_suite = next((r for r in check_runs if r["name"] == FULL_SUITE), None)
    done_when_checks = [by_key[k] for k in by_key]
    lines = [MARKER, f"### PR #{pr} · {stage(worker, done_when_checks, full_suite)}",
             links_row(repo, pr, issue, worker, check_runs), ""]
    if not issue:
        lines += ["⚠️ No linked issue. Add `Closes #N` to the description.", ""]
    elif not goals:
        lines += [f"⚠️ Issue #{issue['number']} has no goals and done-whens yet.", ""]
    for goal in goals:
        lines += [f"**{goal['text']}**", ""]
        for dw in goal["done_whens"]:
            check = by_key.get(f"{issue['number']}.{dw['n']}")
            lines.append(f"- {done_when_line(dw['text'], check)}")
            lines.append(f"  **Verified by:** {dw['verified_by'] or '⚠️ not stated'}")
        lines.append("")
    icon, proof = verdict(full_suite)
    lines.append(f"**Full suite:** {icon} {proof}")
    gap = not_checked(issue["body"]) if issue else None
    if gap:
        lines.append(f"**Not checked:** {gap}")
    later = issue.get("edited_after") if issue else None
    if later:
        edits = ", ".join(f"{e['at'][:16].replace('T', ' ')} UTC by {e['by']}" for e in later)
        lines.append(f"**Edited after approval (ignored):** {edits}")
    lines += ["", "<sub>Built by the card workflow from GitHub's records. No AI writes this card.</sub>"]
    return "\n".join(lines)


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def find_pr(repo):
    """The PR this event is about: from the triggering run, or from the worker's issue number."""
    pr = os.environ.get("PR_NUMBER")
    if pr:
        return pr
    title = re.match(r"(?:worker for #|build for work/issue-)(\d+)$", os.environ.get("RUN_TITLE", ""))
    owner = repo.split("/")[0]
    if title:
        prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:work/issue-{title.group(1)}&state=open"))
    else:
        prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
    return str(prs[0]["number"]) if prs else None


def pipeline_state(repo, pr, branch, open_run, build_run, approved, commits):
    """What the worker pipeline is doing for this PR, as {"status", "html_url"}, or None.

    A worker PR with only its start commit and no approval yet is waiting for an
    approver; its Approve link goes to the PR's review page.
    """
    if not plan.WORK_BRANCH.fullmatch(branch):
        return None
    for run in (build_run, open_run):
        if run and run["status"] in WORKER_ACTIVE:
            return run
    if not approved and commits == 1:
        return {"status": "waiting", "html_url": f"https://github.com/{repo}/pull/{pr}/files"}
    return build_run or open_run


def latest_run(repo, workflow, title):
    runs = json.loads(gh("api", f"repos/{repo}/actions/workflows/{workflow}/runs?per_page=30"))["workflow_runs"]
    run = next((r for r in runs if r["display_title"] == title), None)
    return {"status": run["status"], "html_url": run["html_url"]} if run else None


def main():
    repo = os.environ["REPO"]
    pr = find_pr(repo)
    if not pr:
        print("No open pull request for this event; nothing to post.")
        return
    info = json.loads(gh("api", f"repos/{repo}/pulls/{pr}"))
    head = info["head"]
    issue = plan.approved_issue(repo, pr)
    check_runs = json.loads(gh("api", f"repos/{repo}/commits/{head['sha']}/check-runs?per_page=100"))["check_runs"]
    m = plan.WORK_BRANCH.fullmatch(head["ref"])
    worker = None
    if m:
        worker = pipeline_state(repo, pr, head["ref"],
                                latest_run(repo, "worker.yml", f"worker for #{m.group(1)}"),
                                latest_run(repo, "build.yml", f"build for {head['ref']}"),
                                bool(issue and issue["approved_at"]), info["commits"])

    body = render(repo, pr, issue, check_runs, worker)
    with open("card.md", "w") as f:
        f.write(body)
    existing = gh("api", f"repos/{repo}/issues/{pr}/comments", "--paginate",
                  "--jq", f'.[] | select(.body | contains("{MARKER}")) | .id').split()
    if existing:
        gh("api", "-X", "PATCH", f"repos/{repo}/issues/comments/{existing[0]}", "-F", "body=@card.md")
        print(f"Updated card on PR #{pr}")
    else:
        gh("api", f"repos/{repo}/issues/{pr}/comments", "-F", "body=@card.md")
        print(f"Posted card on PR #{pr}")


if __name__ == "__main__":
    main()
