#!/usr/bin/env python3
"""Build and post the Dokima card on a pull request.

The card shows the linked issue's goals, each done-when, how it is verified,
and, once verified, one proof link. It runs from the default branch (a
workflow_run trigger), never from the pull request's own code, so the work being
judged cannot change how it is reported. It uses only GitHub's records. No model
writes the card.

A done-when shows ✅ only when GitHub recorded its verification passing, in a run
on the pull request's latest commit. The card builds the proof link itself from
that record; there is no slot for anyone to supply one. Anything else is ⚠️ or ❌.

Verification tests declare which done-when they prove with
record_property("proves", "<issue>.<n>"), where n counts the issue's done-whens
from 1, top to bottom.
"""
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET

MARKER = "<!-- dokima-card -->"
CHECKBOX = re.compile(r"^(\s*)[-*] \[( |x|X)\] (.+)$")
VERIFIED = re.compile(r"^\s+Verified by:\s*(.+)$", re.I)
DONE_PREFIX = re.compile(r"^Done when:\s*", re.I)


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


def parse_junit(xml_text):
    """One result per test case: file, name, status, and which done-whens it proves."""
    results = []
    for tc in ET.fromstring(xml_text).iter("testcase"):
        status = "passed"
        for child in tc:
            if child.tag in ("failure", "error"):
                status = "failed"
            elif child.tag == "skipped":
                status = "skipped"
        proves = [p.get("value") for p in tc.iter("property") if p.get("name") == "proves"]
        results.append({"file": tc.get("file"), "name": tc.get("name"), "status": status, "proves": proves})
    return results


def node_id(result):
    return f"{result['file']}::{result['name']}"


def verdict(issue_number, n, results, run, current_sha, proof_link):
    """Status of one done-when: ('✅', link) only for a recorded pass on the latest commit, else ⚠️ or ❌."""
    if not run or not run.get("url"):
        return "⚠️", "no proof: no recorded run"
    if run.get("sha") != current_sha:
        return "⚠️", "no proof: the run is for an older commit"
    tests = [r for r in results if f"{issue_number}.{n}" in r["proves"]]
    if not tests:
        return "⚠️", "no proof: no test verifies this yet"
    failed = [t for t in tests if t["status"] != "passed"]
    if failed:
        return "❌", f"[proof]({proof_link(failed[0])})"
    return "✅", f"[proof]({proof_link(tests[0])})"


def render(pr, issue, goals, results, run, current_sha, proof_link):
    title = f"### PR #{pr}"
    if run and run.get("url"):
        title += f" · [live run]({run['url']})"
    lines = [MARKER, title, ""]
    if not issue:
        lines.append("⚠️ No linked issue. Add `Closes #N` to the description to show its goals here.")
    elif not goals:
        lines.append(f"⚠️ Issue #{issue['number']} has no goals and done-whens yet.")
    for goal in goals:
        lines.append(f"**{goal['text']}**")
        lines.append("")
        for dw in goal["done_whens"]:
            icon, proof = verdict(issue["number"], dw["n"], results, run, current_sha, proof_link)
            lines.append(f"- {icon} **Done when:** {dw['text']} · {proof}")
            lines.append(f"  **Verified by:** {dw['verified_by'] or '⚠️ not stated'}")
        lines.append("")
    lines.append("<sub>Built by the card workflow from GitHub's records. No AI writes this card.</sub>")
    return "\n".join(lines)


def step_line_links(job, log_text, results):
    """Map each test to a link at the line in its run's log where pytest reported it."""
    step = next((s for s in job.get("steps", []) if "pytest" in (s.get("name") or "")), None)
    lines = [re.sub(r"^\S+Z ", "", line) for line in log_text.splitlines()]
    start = next((i for i, line in enumerate(lines) if line.startswith("##[group]Run pytest")), None)
    links = {}
    for r in results:
        url = job["html_url"]
        if step and start is not None:
            target = f"{r['status'].upper()} {node_id(r)}"
            hit = next((i for i in range(start, len(lines)) if lines[i].startswith(target)), None)
            url += f"#step:{step['number']}:{hit - start + 1}" if hit is not None else f"#step:{step['number']}"
        links[node_id(r)] = url
    return links


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main():
    repo = os.environ["REPO"]
    run_id = os.environ["RUN_ID"]
    run = {"url": os.environ.get("RUN_URL"), "sha": os.environ["HEAD_SHA"]}
    pr = os.environ.get("PR_NUMBER") or ""
    if not pr:
        prs = json.loads(gh("api", f"repos/{repo}/commits/{run['sha']}/pulls"))
        if not prs:
            print(f"No pull request for {run['sha']}; nothing to post.")
            return
        pr = str(prs[0]["number"])
    current_sha = gh("api", f"repos/{repo}/pulls/{pr}", "--jq", ".head.sha").strip()

    owner, name = repo.split("/")
    query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
             "{closingIssuesReferences(first:1){nodes{number title body}}}}}")
    data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}", "-F", f"p={pr}"))
    nodes = data["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]
    issue = nodes[0] if nodes else None

    path = os.environ.get("RESULTS", "results/results.xml")
    results = parse_junit(open(path).read()) if os.path.exists(path) else []
    links = {}
    if results:
        jobs = json.loads(gh("api", f"repos/{repo}/actions/runs/{run_id}/jobs"))["jobs"]
        job = next((j for j in jobs if j["name"] == "tests"), None)
        if job:
            run["url"] = job["html_url"]
            links = step_line_links(job, gh("api", f"repos/{repo}/actions/jobs/{job['id']}/logs"), results)

    body = render(pr, issue, parse_issue(issue["body"]) if issue else [], results, run, current_sha,
                  lambda r: links.get(node_id(r), run["url"]))
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
