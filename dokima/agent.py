"""Packs and hand-back checks for running one agent by hand on a fresh machine.

`pack` builds the agent's starting pack from GitHub's records: the issue as it stands (body and every comment) and the
JSON hand-backs of earlier runs, downloaded from those runs. `check` is the deterministic check an agent runs on its own
hand-back before it finishes, and that code runs again after it: a malformed hand-back never reaches the next agent.
The plan's own check lives in dokima/planner.py; this module adds review.json and work.json.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

VERDICTS = {"approve", "block", "escalate"}
ANSWERS = {"fixed", "disagree"}


def gh(*args):
    """Run the GitHub CLI and return its output."""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def issue_text(repo, number):
    """The issue as it stands: title, body and every comment with its author, oldest first."""
    d = json.loads(gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,comments"))
    parts = [f"# Issue #{d['number']}: {d['title']}", "", d["body"] or "", "", "## Comments"]
    for c in d["comments"]:
        parts += ["", f"### {c['author']['login']} ({c['createdAt']})", "", c["body"]]
    return "\n".join(parts) + "\n"


def bring_in(repo, run_ids, dest, logs=False):
    """Download the given runs' artifacts and copy their JSON hand-backs into dest; session logs too only when asked.

    Logs are for the pull request review, which looks for gaming; a plan review never sees the planner's reasoning."""
    os.makedirs(dest, exist_ok=True)
    for rid in [r.strip() for r in run_ids.split(",") if r.strip()]:
        tmp = os.path.join(dest, ".dl", rid)
        gh("run", "download", rid, "-R", repo, "-D", tmp)
        for f in glob.glob(os.path.join(tmp, "**", "*.json"), recursive=True):
            shutil.copy(f, os.path.join(dest, f"run-{rid}-{os.path.basename(f)}"))
        found = glob.glob(os.path.join(tmp, "**", "*.jsonl"), recursive=True) if logs else []
        if found:
            ldir = os.path.join(dest, f"run-{rid}-session-log")
            os.makedirs(ldir, exist_ok=True)
            for f in found:
                shutil.copy(f, ldir)
    shutil.rmtree(os.path.join(dest, ".dl"), ignore_errors=True)


def problems_questions(qs):
    """Everything wrong with the planner's questions for the owner: each is one question ending in '?'.

    Options and a recommendation are optional help, and a recommendation must be one of the options when both are given.
    The owner answers in prose, in their own words."""
    if not isinstance(qs, list):
        return ["questions must be a list"]
    bad = []
    for i, q in enumerate(qs, 1):
        q = q if isinstance(q, dict) else {}
        if not str(q.get("question", "")).strip().endswith("?"):
            bad.append(f"question {i} must be one question ending in '?'")
        opts, rec = q.get("options"), str(q.get("recommendation", "")).strip()
        if opts is not None and not isinstance(opts, list):
            bad.append(f"question {i}'s options must be a list")
        elif opts and rec and rec not in [str(o).strip() for o in opts]:
            bad.append(f"question {i}'s recommendation must be one of its options")
    return bad


def problems_review(r):
    """Everything wrong with a review.json, as plain sentences; empty when it is well formed."""
    bad = []
    if r.get("stage") not in ("plan", "pr"):
        bad.append('stage must be "plan" or "pr"')
    if not isinstance(r.get("round"), int) or r.get("round", 0) < 1:
        bad.append("round must be a whole number from 1")
    if r.get("verdict") not in VERDICTS:
        bad.append("verdict must be approve, block or escalate")
    if not str(r.get("summary", "")).strip():
        bad.append("summary is empty")
    blockers = r.get("blockers", [])
    if not isinstance(blockers, list):
        bad.append("blockers must be a list")
        blockers = []
    ids = [b.get("id") for b in blockers if isinstance(b, dict)]
    if len(ids) != len(set(ids)):
        bad.append("blocker ids repeat")
    for b in blockers:
        for field in ("id", "criterion", "problem", "evidence", "fix"):
            if not str((b or {}).get(field) or "").strip():
                bad.append(f"blocker {(b or {}).get('id', '?')} has no {field}")
    if r.get("verdict") == "approve" and blockers:
        bad.append("an approve has no blockers")
    if r.get("verdict") == "block" and not blockers:
        bad.append("a block needs at least one blocker")
    if len(r.get("notes", [])) > 3:
        bad.append("at most three notes")
    if r.get("stage") == "plan" and r.get("outside_plan"):
        bad.append("outside_plan is for a pull request only")
    if "questions" in r:
        bad.append("the reviewer never asks the owner; escalate on round three instead")
    return bad


def problems_work(w):
    """Everything wrong with a work.json, as plain sentences; empty when it is well formed."""
    bad = []
    if not str(w.get("summary", "")).strip():
        bad.append("summary is empty")
    if not isinstance(w.get("criteria"), dict) or not w["criteria"]:
        bad.append("criteria must give one line per criterion")
    if not str(w.get("evidence", "")).strip():
        bad.append("evidence is empty: name the last test command and its result line")
    for r in w.get("replies", []):
        if r.get("answer") not in ANSWERS or not str(r.get("why", "")).strip() or not r.get("blocker"):
            bad.append(f"reply to {r.get('blocker', '?')} needs a blocker id, fixed or disagree, and why")
    for s in w.get("suspect_tests", []):
        if not s.get("test") or not str(s.get("evidence", "")).strip():
            bad.append("every suspect test needs the test and the evidence")
    if "questions" in w:
        bad.append("the worker never asks the owner; the plan is the contract")
    return bad


def check(kind, path):
    """Check one hand-back file; print every problem and return 1 if there are any, else 0."""
    try:
        data = json.load(open(path))
    except FileNotFoundError:
        print(f"{path} is missing")
        return 1
    except json.JSONDecodeError as e:
        print(f"{path} is not valid JSON: {e}")
        return 1
    bad = (problems_review if kind == "review" else problems_work)(data if isinstance(data, dict) else {})
    for b in bad:
        print(b)
    return 1 if bad else 0


def main(argv):
    """agent pack N DIR [RUN_IDS] | agent check review|work FILE"""
    if argv[1] == "pack":
        repo = os.environ["GITHUB_REPOSITORY"]
        os.makedirs(argv[3], exist_ok=True)
        open(os.path.join(argv[3], "issue.md"), "w").write(issue_text(repo, argv[2]))
        if len(argv) > 4 and argv[4].strip():
            bring_in(repo, argv[4], os.path.join(argv[3], "in"), logs=os.environ.get("STAGE") == "pr")
        return 0
    if argv[1] == "check":
        return check(argv[2], argv[3])
    print(main.__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
