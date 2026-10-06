"""Packs and hand-back checks for running one agent by hand on a fresh machine.

`pack` builds the agent's starting pack from GitHub's records: the issue as it stands (body and every comment) and the
JSON hand-backs of earlier runs, downloaded from those runs. `check` is the deterministic check an agent runs on its own
hand-back before it finishes, and that code runs again after it: a malformed hand-back never reaches the next agent.
The plan's own check lives in dokima/planner.py; this module adds review.json and work.json.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

VERDICTS = {"approve", "block", "escalate"}
ANSWERS = {"fixed", "disagree"}


def gh(*args):
    """Run the GitHub CLI and return its output."""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


MARK = "<!-- dokima-record -->"
BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}


def linked_prs(repo, number):
    """Pull requests built for the issue: from its work or try branch."""
    found = []
    for head in (f"work/issue-{number}", f"try/issue-{number}"):
        found += json.loads(gh("pr", "list", "-R", repo, "--head", head, "--state", "all", "--json", "number"))
    return sorted({p["number"] for p in found})


def conversation(repo, number):
    """The issue and its pull requests as one list of comments, oldest first, each saying where it was written."""
    d = json.loads(gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,comments"))
    items = [{**c, "where": f"issue #{number}"} for c in d["comments"]]
    for pr in linked_prs(repo, number):
        p = json.loads(gh("pr", "view", str(pr), "-R", repo, "--json", "comments,reviews"))
        items += [{**c, "where": f"PR #{pr}"} for c in p["comments"]]
        items += [{"author": r["author"], "body": r["body"], "createdAt": r["submittedAt"], "where": f"PR #{pr} review ({r['state'].lower()})"}
                  for r in p["reviews"] if r.get("body")]
        for n in json.loads(gh("api", f"repos/{repo}/pulls/{pr}/comments", "--paginate")):
            items.append({"author": {"login": n["user"]["login"]}, "body": n["body"], "createdAt": n["created_at"],
                          "where": f"PR #{pr} line note on {n['path']}:{n.get('line') or n.get('original_line')}"})
    items.sort(key=lambda c: c["createdAt"])
    return d, items


def issue_text(d, items):
    """The issue as it stands: title, body and every comment with its author and where it was written, oldest first."""
    parts = [f"# Issue #{d['number']}: {d['title']}", "", d["body"] or "", "", "## Comments"]
    for c in items:
        parts += ["", f"### {c['author']['login']} on {c['where']} ({c['createdAt']})", "", c["body"]]
    return "\n".join(parts) + "\n"


def records(items):
    """Every agent record in the conversation, oldest first. Only comments the bot posted count: anyone can paste text."""
    out = []
    for c in items:
        body = c.get("body") or ""
        if (c.get("author") or {}).get("login") != BOT or MARK not in body:
            continue
        m = re.search(r"```json\n(.*?)\n```", body, re.S)
        try:
            out.append(json.loads(m.group(1)) if m else None)
        except json.JSONDecodeError:
            continue
    return [r for r in out if isinstance(r, dict)]


def latest(recs, role, passed=True):
    """The newest record of a role whose hand-back passed its check, or None."""
    for r in reversed(recs):
        if r.get("role") == role and (r.get("check", {}).get("passed") or not passed):
            return r
    return None


def approved(recs):
    """True when the newest passed plan has a plan review after it, and the newest such review approves it."""
    plans = [i for i, r in enumerate(recs) if r.get("role") == "planner" and r.get("check", {}).get("passed")]
    if not plans:
        return False
    reviews = [r for r in recs[plans[-1] + 1:] if r.get("role") == "reviewer" and r.get("stage") == "plan"
               and r.get("check", {}).get("passed")]
    return bool(reviews) and reviews[-1]["handback"].get("verdict") == "approve"


def is_record(c, role=None, stage=None):
    """True when a comment is a record the bot posted, of the given role and stage when given."""
    if (c.get("author") or {}).get("login") != BOT or MARK not in (c.get("body") or ""):
        return False
    r = records([c])
    return bool(r) and (role is None or (r[0].get("role") == role and (r[0].get("stage") or "") == (stage or "")))


def open_blockers(recs, stage):
    """The blockers of the newest review at this stage, unless it approved; these must be answered by id."""
    for r in reversed(recs):
        if r.get("role") == "reviewer" and (r.get("stage") or "") == stage and r.get("check", {}).get("passed"):
            return [] if r["handback"].get("verdict") == "approve" else r["handback"].get("blockers", [])
    return []


def problems_round(role, h, pack_dir):
    """Every open blocker of the newest review must be answered by id; the reviewer must resolve or keep each one."""
    path = os.path.join(pack_dir, "open_blockers.json")
    blockers = {b["id"] for b in (json.load(open(path)) if os.path.exists(path) else [])}
    if role == "reviewer":
        carried = set(h.get("resolved", [])) | {b.get("id") for b in h.get("blockers", [])}
        return [f"earlier blocker {b} is neither resolved nor still listed" for b in sorted(blockers - carried)]
    replied = {r.get("blocker") for r in h.get("replies", []) if isinstance(r, dict)}
    return [f"blocker {b} is not answered" for b in sorted(blockers - replied)]


def build_record(role, stage, out, check_text, passed, meta):
    """This run's record: its hand-back, the code check's verdict and where it came from. Written by code, never the agent."""
    hb = os.path.join(out, HANDBACK[role])
    try:
        handback = json.load(open(hb))
    except (OSError, json.JSONDecodeError) as e:
        handback = {"missing": f"{HANDBACK[role]}: {e}"}
    rec = {"role": role, "stage": stage or None, **meta, "handback": handback,
           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()] if not passed else []}}
    dropped = os.path.join(out, "dropped.txt")
    if os.path.exists(dropped):
        rec["dropped_by_fence"] = [l for l in open(dropped).read().splitlines() if l.strip()]
    return rec


def render(rec):
    """The comment that carries a record: a short readable summary, then the full record as JSON in a fold."""
    role, h = rec["role"], rec["handback"]
    head = {"planner": "Planner", "reviewer": f"Reviewer ({rec.get('stage')})", "worker": "Worker"}[role]
    lines = [MARK, f"**{head}**" + ("" if rec["check"]["passed"] else " · hand-back rejected by code")]
    if not rec["check"]["passed"]:
        lines += [""] + [f"- {p}" for p in rec["check"]["problems"]]
    elif role == "planner" and h.get("kind") == "feature":
        lines += ["", f"Proposes a split: {h.get('feature', '')}", ""]
        lines += [f"{i}. {st.get('title', '')}" for i, st in enumerate(h.get("stories", []), 1)]
    elif role == "planner":
        lines += ["", h.get("user_story") or h.get("question") or ""]
    elif role == "reviewer":
        lines += ["", f"**{h.get('verdict')}**: {h.get('summary', '')}"]
        lines += [f"- **{b.get('id')}** ({b.get('criterion')}): {b.get('problem')}" for b in h.get("blockers", [])]
    else:
        lines += ["", h.get("summary", "")]
    if role == "planner" and h.get("questions"):
        lines += ["", "**Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):"]
        lines += [f"- {q}" for q in h["questions"]]
    prev = h.get("previous_step") if isinstance(h, dict) else None
    if isinstance(prev, dict) and any(prev.get(k) for k in ("did", "decided", "open")):
        lines += ["", "<details><summary>What the previous step did</summary>", ""]
        for k, label in (("did", "Did"), ("decided", "Decided"), ("open", "Still open")):
            lines += [f"- **{label}:** {x}" for x in prev.get(k) or []]
        lines += ["", "</details>"]
    lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
              "", footnote(rec)]
    return "\n".join(lines) + "\n"


def jsonl_files(root):
    """Every session log under root, hidden folders included (Claude keeps its logs under .claude)."""
    return sorted(os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.endswith(".jsonl"))


def scrub(text, secrets):
    """Remove every secret value from text before it is saved anywhere public."""
    for v in sorted((x for x in secrets if len(x) >= 8), key=len, reverse=True):
        text = text.replace(v, "[secret removed]")
    return text


def transcript(log_dir, secrets=()):
    """A readable transcript of the run's session: what the agent said, each tool it used and a cut of each result."""
    out, n = [], 0
    for f in jsonl_files(log_dir):
        for line in open(f):
            try:
                m = json.loads(line).get("message") or {}
            except json.JSONDecodeError:
                continue
            content = m.get("content")
            for b in ([{"type": "text", "text": content}] if isinstance(content, str) else content or []):
                kind = b.get("type")
                if kind == "text" and b.get("text", "").strip() and m.get("role") == "assistant":
                    out.append(f"**Agent:** {b['text'].strip()}")
                elif kind == "tool_use":
                    n += 1
                    i = b.get("input") or {}
                    what = i.get("command") or i.get("file_path") or i.get("pattern") or json.dumps(i)
                    out.append(f"`{n}. {b.get('name')}`\n```\n{str(what)[:2000]}\n```")
                elif kind == "tool_result":
                    r = b.get("content")
                    r = r if isinstance(r, str) else " ".join(x.get("text", "") for x in (r or []) if isinstance(x, dict))
                    out.append("> " + r.strip()[:1500].replace("\n", "\n> "))
    return scrub("\n\n".join(out) + "\n", secrets)


def run_report(path):
    """Claude's own end-of-run report: time, turns, tokens and API-equivalent cost, exactly as Claude gave them."""
    try:
        d = json.load(open(path))
    except (OSError, json.JSONDecodeError):
        return {}
    u = d.get("usage") or {}
    return {"duration_ms": d.get("duration_ms"), "turns": d.get("num_turns"), "cost_usd": d.get("total_cost_usd"),
            "tokens_in": (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0),
            "tokens_out": u.get("output_tokens")}


def footnote(rec):
    """One line under every card: model, time, turns, tokens and cost, and the link to the full conversation."""
    r = rec.get("report") or {}
    pretty = lambda m: (lambda x: f"{x.group(1).title()} {x.group(2)}.{x.group(3)}" if x else m)(re.match(r"claude-([a-z]+)-(\d+)-(\d+)", m))
    parts = [", ".join(pretty(m) for m in rec.get("models") or []) or "model unknown"]
    if r.get("duration_ms"):
        parts.append(f"{round(r['duration_ms'] / 60000, 1)} min")
    if r.get("turns"):
        parts.append(f"{r['turns']} turns")
    if r.get("tokens_in") or r.get("tokens_out"):
        parts.append(f"{r.get('tokens_in', 0):,} tokens in, {r.get('tokens_out') or 0:,} out")
    if r.get("cost_usd") is not None:
        parts.append(f"${r['cost_usd']:.2f} at API prices")
    links = " · ".join(x for x in (f"[conversation]({rec['log']})" if rec.get("log") else "", f"[run]({rec['run']})" if rec.get("run") else "") if x)
    return "<sub>" + " · ".join(parts) + (" · " + links if links else "") + "</sub>"


def models_used(log_dir):
    """Every model named in the run's session logs, so the record proves which model did the work."""
    seen = set()
    for f in jsonl_files(log_dir):
        for line in open(f):
            try:
                m = (json.loads(line).get("message") or {}).get("model")
            except json.JSONDecodeError:
                continue
            if m:
                seen.add(m)
    return sorted(seen)


def pack(repo, number, role, stage, dest):
    """Build the starting pack from GitHub's records: the issue and its PRs' conversation, every agent record so far,
    and the newest passed plan. The pull request review also gets the worker's session log from its run."""
    d, items = conversation(repo, number)
    recs = records(items)
    os.makedirs(os.path.join(dest, "in"), exist_ok=True)
    answers_to = {"planner": "plan", "worker": "pr", "reviewer": stage}[role]
    json.dump(open_blockers(recs, answers_to), open(os.path.join(dest, "open_blockers.json"), "w"), indent=1)
    open(os.path.join(dest, "issue.md"), "w").write(issue_text(d, items))
    for i, r in enumerate(recs, 1):
        name = f"{i:02d}-{r['role']}{'-' + r['stage'] if r.get('stage') else ''}.json"
        json.dump(r, open(os.path.join(dest, "in", name), "w"), indent=1)
    plan = latest(recs, "planner")
    if role == "worker" and not approved(recs):
        return False
    if plan:
        json.dump(plan["handback"], open(os.path.join(dest, "plan.json"), "w"), indent=1)
    if stage == "pr":
        work = latest(recs, "worker", passed=False)
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
    prev = r.get("previous_step")
    if not isinstance(prev, dict) or not any(prev.get(k) for k in ("did", "decided", "open")):
        bad.append("previous_step must sum up what the planner or worker did, decided and left open")
    elif sum(len(prev.get(k) or []) for k in ("did", "decided", "open")) > 5:
        bad.append("previous_step holds at most five lines")
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
        elif os.path.isdir(path) and not jsonl_files(path):
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


COMMANDS = {"/plan": "planner", "/work": "worker", "/review": "reviewer"}


def command_of(body):
    """The stage a comment starts: its first line's first word, when that word is a command; otherwise None."""
    first = (body or "").strip().splitlines()[0].split() if (body or "").strip() else []
    return COMMANDS.get(first[0].lower()) if first else None


def issue_of_pr(head, body):
    """The issue a pull request was built for: from its branch (work/issue-N or try/issue-N), else 'Closes #N'."""
    m = re.match(r"(?:work|try)/issue-(\d+)$", head or "") or re.search(r"(?i)\b(?:closes|fixes|resolves) #(\d+)", body or "")
    return m.group(1) if m else None


def route(body, on_pr, number, head="", pr_body=""):
    """What a code owner's comment starts: {role, stage, issue}, or None when it starts nothing.

    /review on an issue grades the plan; on a pull request it grades the work. A pull request routes to its issue."""
    role = command_of(body)
    if not role:
        return None
    issue = issue_of_pr(head, pr_body) if on_pr else str(number)
    if not issue:
        return None
    stage = ("pr" if on_pr else "plan") if role == "reviewer" else ""
    return {"role": role, "stage": stage, "issue": issue}


def main(argv):
    """agent pack N ROLE STAGE DIR | agent check-pack ROLE STAGE DIR | agent check review|work FILE |
    agent record ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR  (writes OUT/record.json and OUT/comment.md)"""
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
        role, stage, out, check_file, passed, log_dir = argv[2:8]
        meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "commit_before": os.environ.get("BASE"),
                "started_by": os.environ.get("GITHUB_ACTOR"), "models": models_used(log_dir),
                "report": run_report(os.path.join(out, "claude.json")), "log": os.environ.get("LOG_URL"),
                "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"}
        text = open(check_file).read() if os.path.exists(check_file) else ""
        rec = build_record(role, stage, out, text, passed == "true", meta)
        json.dump(rec, open(os.path.join(out, "record.json"), "w"), indent=1)
        open(os.path.join(out, "comment.md"), "w").write(render(rec))
        return 0
    if argv[1] == "check-round":
        try:
            h = json.load(open(argv[3]))
        except (OSError, json.JSONDecodeError) as e:
            print(f"{argv[3]}: {e}")
            return 1
        bad = problems_round(argv[2], h if isinstance(h, dict) else {}, argv[4])
        for b in bad:
            print(b)
        return 1 if bad else 0
    if argv[1] == "transcript":
        secrets = [v for k, v in os.environ.items() if k.startswith("SCRUB_")]
        sys.stdout.write(transcript(argv[2], secrets))
        return 0
    if argv[1] == "route":
        on_pr = os.environ.get("ON_PR") == "true"
        head, pr_body = os.environ.get("HEAD", ""), ""
        if on_pr:
            p = json.loads(gh("pr", "view", os.environ["NUMBER"], "-R", os.environ["GITHUB_REPOSITORY"], "--json", "headRefName,body"))
            head, pr_body = p["headRefName"], p["body"]
        r = route(os.environ.get("BODY", ""), on_pr, os.environ.get("NUMBER", ""), head, pr_body)
        for k, v in (r or {}).items():
            print(f"{k}={v}")
        return 0
    print(main.__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
