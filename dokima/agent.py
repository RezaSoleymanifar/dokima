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


HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}


def records_dir(number):
    """Where an issue's records live: one JSON file per agent run, in order, on the issue's branch."""
    return os.path.join(".dokima", str(number))


def records(number):
    """Every record of the issue, oldest first, as (path, data)."""
    d = records_dir(number)
    paths = sorted(glob.glob(os.path.join(d, "*.json"))) if os.path.isdir(d) else []
    return [(p, json.load(open(p))) for p in paths]


def latest(number, role, passed=True):
    """The newest record of a role whose hand-back passed its check, or None."""
    for path, r in reversed(records(number)):
        if r.get("role") == role and (r.get("check", {}).get("passed") or not passed):
            return r
    return None


def record(number, role, stage, out, check_text, passed, meta):
    """Write this run's record: its hand-back, the code check's verdict and where it came from. Returns the path.

    The record is written by code after the agent has stopped, so the agent never writes or edits a record."""
    d = records_dir(number)
    os.makedirs(d, exist_ok=True)
    seq = len(glob.glob(os.path.join(d, "*.json"))) + 1
    path = os.path.join(d, f"{seq:02d}-{role}{'-' + stage if stage else ''}.json")
    hb = os.path.join(out, HANDBACK[role])
    try:
        handback = json.load(open(hb))
    except (OSError, json.JSONDecodeError) as e:
        handback = {"missing": f"{HANDBACK[role]}: {e}"}
    dropped = os.path.join(out, "dropped.txt")
    rec = {"role": role, "stage": stage or None, **meta, "handback": handback,
           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()]}}
    if os.path.exists(dropped):
        rec["dropped_by_fence"] = [l for l in open(dropped).read().splitlines() if l.strip()]
    with open(path, "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    return path


def models_used(log_dir):
    """Every model named in the run's session logs, so the record proves which model did the work."""
    seen = set()
    for f in glob.glob(os.path.join(log_dir, "**", "*.jsonl"), recursive=True):
        for line in open(f):
            try:
                m = (json.loads(line).get("message") or {}).get("model")
            except json.JSONDecodeError:
                continue
            if m:
                seen.add(m)
    return sorted(seen)


def approved(number):
    """True when the newest passed plan has a plan review after it, and the newest such review approves it."""
    recs = records(number)
    plans = [i for i, (_, r) in enumerate(recs) if r.get("role") == "planner" and r.get("check", {}).get("passed")]
    if not plans:
        return False
    reviews = [r for _, r in recs[plans[-1] + 1:] if r.get("role") == "reviewer" and r.get("stage") == "plan"
               and r.get("check", {}).get("passed")]
    return bool(reviews) and reviews[-1]["handback"].get("verdict") == "approve"


def pack(repo, number, role, stage, dest):
    """Build the starting pack: the issue with every comment, every earlier record, and the latest passed plan.

    The pull request review also gets the worker's session log from its run, to look for gaming."""
    os.makedirs(os.path.join(dest, "in"), exist_ok=True)
    open(os.path.join(dest, "issue.md"), "w").write(issue_text(repo, number))
    for path, _ in records(number):
        shutil.copy(path, os.path.join(dest, "in", os.path.basename(path)))
    plan = latest(number, "planner")
    if role == "worker" and not approved(number):
        return False
    if plan:
        json.dump(plan["handback"], open(os.path.join(dest, "plan.json"), "w"), indent=1)
    if stage == "pr":
        work = latest(number, "worker", passed=False)
        if work and work.get("run_id"):
            gh("run", "download", str(work["run_id"]), "-R", repo, "-n", f"worker-{number}", "-D", os.path.join(dest, "worker-run"))
    return bool(plan)


def problems_questions(qs):
    """Everything wrong with the planner's questions for the owner: a list of plain questions, each asking something ('?')."""
    if not isinstance(qs, list):
        return ["questions must be a list of plain questions"]
    return [f"question {i} must be a plain question with a '?'" for i, q in enumerate(qs, 1)
            if not isinstance(q, str) or "?" not in q]


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


NEEDS = {
    "planner": ["issue.md"],
    "reviewer-plan": ["issue.md", "plan.json"],
    "worker": ["issue.md", "plan.json"],
    "reviewer-pr": ["issue.md", "plan.json", "diff.patch", "tests.txt", "tests.xml", "worker-run"],
}


def problems_pack(role, stage, dest):
    """Everything missing or broken in an agent's starting pack, checked by code before the agent starts."""
    key = f"{role}-{stage}" if role == "reviewer" else role
    if key not in NEEDS:
        return [f"unknown role {key}"]
    bad = []
    for name in NEEDS[key]:
        path = os.path.join(dest, name)
        if not os.path.exists(path):
            bad.append(f"{name} is missing")
        elif os.path.isdir(path) and not glob.glob(os.path.join(path, "**", "*.jsonl"), recursive=True):
            bad.append(f"{name} holds no session log")
        elif os.path.isfile(path) and name != "diff.patch" and not open(path).read().strip():
            bad.append(f"{name} is empty")
    issue = os.path.join(dest, "issue.md")
    if os.path.exists(issue) and "## Comments" not in open(issue).read():
        bad.append("issue.md has no comments section")
    for name in ("plan.json",):
        path = os.path.join(dest, name)
        if os.path.isfile(path):
            try:
                if not isinstance(json.load(open(path)), dict):
                    bad.append(f"{name} is not a JSON object")
            except json.JSONDecodeError:
                bad.append(f"{name} is not valid JSON")
    for path in sorted(glob.glob(os.path.join(dest, "in", "*.json"))):
        try:
            r = json.load(open(path))
            if not {"role", "handback", "check"} <= set(r):
                bad.append(f"record {os.path.basename(path)} lacks role, handback or check")
        except json.JSONDecodeError:
            bad.append(f"record {os.path.basename(path)} is not valid JSON")
    if key == "reviewer-pr" and os.path.isfile(os.path.join(dest, "diff.patch")) and not open(os.path.join(dest, "diff.patch")).read().strip():
        bad.append("diff.patch is empty: there is no work to review")
    return bad


def main(argv):
    """agent pack N ROLE STAGE DIR | agent check-pack ROLE STAGE DIR | agent check review|work FILE | agent record N ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR"""
    if argv[1] == "pack":
        has_plan = pack(os.environ["GITHUB_REPOSITORY"], argv[2], argv[3], argv[4], argv[5])
        return 0 if has_plan or argv[3] == "planner" else 3
    if argv[1] == "check":
        return check(argv[2], argv[3])
    if argv[1] == "check-pack":
        bad = problems_pack(argv[2], argv[3], argv[4])
        for b in bad:
            print(b)
        return 1 if bad else 0
    if argv[1] == "record":
        number, role, stage, out, check_file, passed, log_dir = argv[2:9]
        meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "commit_before": os.environ.get("BASE"),
                "started_by": os.environ.get("GITHUB_ACTOR"), "models": models_used(log_dir),
                "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"}
        text = open(check_file).read() if os.path.exists(check_file) else ""
        print(record(number, role, stage, out, text, passed == "true", meta))
        return 0
    print(main.__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
