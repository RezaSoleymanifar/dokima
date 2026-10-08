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
import time

from dokima.card import icon

VERDICTS = {"approve", "block", "escalate"}
FIXERS = {"worker", "planner"}
ANSWERS = {"fixed", "disagree"}


def gh(*args):
    """Run the GitHub CLI and return its output."""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


MARK = "<!-- dokima-record -->"
LIVE = "<!-- dokima-live -->"
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


def blockers_for(recs, role):
    """The blockers this role must answer by id. A planner answers the test blockers of a code review that sent the work
    back to it, else the newest plan review's; a worker answers only the code blockers of the newest code review."""
    if role == "worker":
        return [b for b in open_blockers(recs, "pr") if not (isinstance(b, dict) and b.get("fixer") == "planner")]
    for r in reversed(recs):
        if r.get("role") == "reviewer" and r.get("check", {}).get("passed"):
            if (r.get("stage") or "") == "pr" and r["handback"].get("verdict") == "block":
                tests = [b for b in r["handback"].get("blockers", []) if isinstance(b, dict) and b.get("fixer") == "planner"]
                if tests:
                    return tests
            break
    return open_blockers(recs, "plan")


def problems_round(role, h, pack_dir):
    """Every open blocker of the newest review must be answered by id; the reviewer must resolve or keep each one."""
    path = os.path.join(pack_dir, "open_blockers.json")
    blockers = {b.get("id") for b in (json.load(open(path)) if os.path.exists(path) else []) if isinstance(b, dict)}
    bad = []
    if role == "reviewer":
        resolved, listed = h.get("resolved", []), h.get("blockers", [])
        if not isinstance(resolved, list) or not all(isinstance(x, str) for x in resolved):
            bad.append("resolved must be a list of blocker ids")
            resolved = []
        if not isinstance(listed, list) or not all(isinstance(b, dict) for b in listed):
            bad.append("blockers must be a list of objects")
            listed = listed if isinstance(listed, list) else []
        carried = set(resolved) | {b.get("id") for b in listed if isinstance(b, dict)}
        return bad + [f"earlier blocker {b} is neither resolved nor still listed" for b in sorted(blockers - carried)]
    replies = h.get("replies", [])
    if not isinstance(replies, list) or not all(isinstance(r, dict) for r in replies):
        bad.append("replies must be a list of objects")
        replies = replies if isinstance(replies, list) else []
    replied = {r.get("blocker") for r in replies if isinstance(r, dict)}
    return bad + [f"blocker {b} is not answered" for b in sorted(blockers - replied)]


def story_body(parent, i, story, parent_title):
    """A story's issue body, drawn by code from the approved plan, so the child planner starts from exactly what was agreed."""
    lines = ["<!-- dokima-card -->", "<!-- /dokima-card -->", "",
             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
             f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
    if story.get("context"):
        lines += [f"**Context:** {story['context']}", ""]
    lines += ["**Acceptance criteria:**"]
    lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
    if story.get("non_functional"):
        lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', '')})" for n in story["non_functional"]]
    return "\n".join(lines + ["", "</details>"]) + "\n"


def file_split(repo, parent, recs):
    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links.

    Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
    done = latest(recs, "split", passed=True)
    if done:
        return done
    plan = latest(recs, "planner")["handback"]
    info = json.loads(gh("issue", "view", str(parent), "-R", repo, "--json", "title,labels"))
    title = info["title"]
    # Stories of a parent on autopilot are on autopilot too.
    extra = ["--label", AUTOPILOT] if any(l["name"] == AUTOPILOT for l in info.get("labels") or []) else []
    filed = []
    for i, st in enumerate(plan["stories"], 1):
        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
        number = int(url.rstrip("/").split("/")[-1])
        node = json.loads(gh("api", f"repos/{repo}/issues/{number}"))["id"]
        gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues", "-F", f"sub_issue_id={node}")
        filed.append({"story": i, "issue": number, "title": st["title"], "id": node,
                      "blocked_by": [d + 1 for d in st.get("depends_on", [])]})
    by_story = {f["story"]: f for f in filed}
    for f in filed:
        for d in f["blocked_by"]:
            try:
                gh("api", "-X", "POST", f"repos/{repo}/issues/{f['issue']}/dependencies/blocked_by", "-F", f"issue_id={by_story[d]['id']}")
            except subprocess.CalledProcessError:
                f.setdefault("link_failed", []).append(by_story[d]["issue"])
    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}


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


def not_started(role, stage, why, meta):
    """The record of a run or command that failed before its agent started: what it tried to start and why it could not."""
    lines = [l.strip() for l in why.splitlines() if l.strip()] or ["A step before the agent failed; see the run for which."]
    return {"role": "not-started", "attempt": role or "command", "stage": stage or None, **meta, "handback": {},
            "check": {"passed": False, "problems": lines}}


def cancelled(role, stage, started, meta):
    """The record of a run someone cancelled: what it was and whether its agent had started. Nothing it handed back
    is used, and the river starts nothing after it."""
    return {"role": "cancelled", "attempt": role, "stage": stage or None, "agent_started": started, **meta,
            "handback": {}, "check": {"passed": False, "problems": []}}


def live_card(role, stage, state, ahead=None):
    """The run's card while it is still running: queued (or waiting for the run `ahead` of it), getting ready, then
    working since the agent started.

    It carries its own marker and no JSON fold, so it never reads as a record; at the end of the run code edits this
    same comment into the run's record. A hand-off's queued card is put up before its run exists, so it links none."""
    head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker",
            "split": "Filing the split"}.get(role, "Command")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
    if state in ("queued", "handoff"):
        if ahead:
            line = f"{icon(repo, 'queued')} **{head}** · waiting for [this run]({ahead})"
            what = (f"Queued, and waiting for [this run]({ahead}) on the same issue to end; this run starts after it. "
                    "This card says working when the agent starts, then becomes the run's record.")
        else:
            line = f"{icon(repo, 'queued')} **{head}** · queued"
            what = "Queued: the run starts in a moment. This card says working when the agent starts, then becomes the run's record."
        return "\n".join([LIVE, line, "", what] + ([] if state == "handoff" else ["", f"<sub>[run]({run})</sub>"])) + "\n"
    if state == "working":
        line = f"{icon(repo, 'running')} **{head}** · working since {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC"
        what = "The agent is working. This card becomes the run's record when it ends."
    else:
        line = f"{icon(repo, 'queued')} **{head}** · getting ready"
        what = "The machine is getting ready. This card says working when the agent starts, then becomes the run's record."
    return "\n".join([LIVE, line, "", what, "", f"<sub>[run]({run})</sub>"]) + "\n"


GOING = {"queued", "in_progress", "waiting", "requested", "pending"}


def where_card(repo, number, role, stage):
    """Where a run's card and record go: the open pull request for the worker and the code review, else the issue."""
    pr = gh("pr", "list", "-R", repo, "--head", f"try/issue-{number}", "--state", "open", "--json", "number",
            "-q", ".[0].number").strip()
    return pr if pr and (role == "worker" or stage == "pr") else str(number)


def run_ahead(repo, number):
    """The link of another run still going on the issue or its pull request, found from GitHub's records: a live card
    the bot put up there, which links its run, and GitHub's word that the run has not completed. None when there is none."""
    own = os.environ.get("GITHUB_RUN_ID", "")
    places = {str(number), where_card(repo, number, "worker", "")}
    for n in sorted(places):
        for c in json.loads(gh("api", f"repos/{repo}/issues/{n}/comments", "--paginate") or "[]"):
            body = c.get("body") or ""
            if (c.get("user") or {}).get("login") not in (BOT, f"{BOT}[bot]") or LIVE not in body or MARK in body:
                continue
            for rid in dict.fromkeys(re.findall(r"/actions/runs/(\d+)", body)):
                if rid == own:
                    continue
                if gh("api", f"repos/{repo}/actions/runs/{rid}", "--jq", ".status").strip() in GOING:
                    return f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{rid}"
    return None


def queue(role, stage, number, state):
    """Put up a run's queued card where its record will go, saying so when it waits for another run; returns its id."""
    repo = os.environ["GITHUB_REPOSITORY"]
    try:
        ahead = run_ahead(repo, number)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        ahead = None
    body = live_card(role, stage, state, ahead)
    return gh("api", "-X", "POST", f"repos/{repo}/issues/{where_card(repo, number, role, stage)}/comments",
              "-f", f"body={body}", "--jq", ".id").strip()


def render(rec):
    """The comment that carries a record: a short readable summary, then the full record as JSON in a fold."""
    role, h = rec["role"], rec["handback"]
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if role == "not-started":
        a = rec.get("attempt")
        head = {"planner": "Planner", "reviewer": f"Reviewer ({rec.get('stage')})", "worker": "Worker",
                "split": "Filing the split"}.get(a, "Command")
        lines = [MARK, f"{icon(repo, 'failed')} **{head}** · stopped before any agent started", ""] + [f"- {p}" for p in rec["check"]["problems"]]
        lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
                  "", f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
        return "\n".join(lines) + "\n"
    if role == "cancelled":
        a = rec.get("attempt")
        head = {"planner": "Planner", "reviewer": f"Reviewer ({rec.get('stage')})", "worker": "Worker"}.get(a, "Command")
        what = ("The run was cancelled after its agent started; nothing it handed back is used." if rec.get("agent_started")
                else "The run was cancelled before its agent started.")
        lines = [MARK, f"{icon(repo, 'cancelled')} **{head}** · cancelled", "", what]
        lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
                  "", footnote(rec) if rec.get("agent_started") else f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
        return "\n".join(lines) + "\n"
    head = {"planner": "Planner", "reviewer": f"Reviewer ({rec.get('stage')})", "worker": "Worker", "split": "Split filed"}[role]
    lines = [MARK, f"{icon(repo, 'passed' if rec['check']['passed'] else 'failed')} **{head}**"
             + ("" if rec["check"]["passed"] else " · hand-back rejected by code")]
    if not rec["check"]["passed"]:
        lines += [""] + [f"- {p}" for p in rec["check"]["problems"]]
    elif role == "planner" and h.get("kind") == "feature":
        lines += ["", f"Proposes a split: {h.get('feature', '')}", ""]
        lines += [f"{i}. {st.get('title', '')}" for i, st in enumerate(h.get("stories", []), 1)]
    elif role == "planner":
        lines += ["", h.get("user_story") or h.get("question") or ""]
    elif role == "reviewer":
        lines += ["", f"**{h.get('verdict')}**: {h.get('summary', '')}"]
        fixes = lambda b: f", the {b['fixer']} fixes it" if b.get("fixer") in FIXERS else ""
        lines += [f"- **{b.get('id')}** ({b.get('criterion')}{fixes(b)}): {b.get('problem')}" for b in h.get("blockers", [])]
        if h.get("issues_found"):
            lines += ["", "**Issues found outside this one** (proposals until you file them):"]
            lines += [f"{i}. {f.get('title')}: {f.get('why')}" for i, f in enumerate(h["issues_found"], 1)]
    elif role == "split":
        num = {f["story"]: f["issue"] for f in h.get("stories", [])}
        lines += [""] + [f"{f['story']}. #{f['issue']} {f['title']}" + (f" (blocked by {', '.join('#' + str(num[d]) for d in f['blocked_by'])})" if f["blocked_by"] else "")
                         for f in h.get("stories", [])]
        lines += ["", "Each story now goes through the flow on its own: comment `/plan` on it to start."]
    else:
        lines += ["", h.get("summary", "")]
    if role == "planner" and h.get("questions"):
        lines += ["", "**Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):"]
        lines += [f"- {q.get('question', '')} Assumed: {q.get('assumption', '')}" if isinstance(q, dict) else f"- {q}"
                  for q in h["questions"]]
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
    if rec.get("role") == "split":
        return f"<sub>Filed by code, no model · [run]({rec.get('run', '')})</sub>"
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
    answers = blockers_for(recs, role) if role != "reviewer" else open_blockers(recs, stage)
    json.dump(answers, open(os.path.join(dest, "open_blockers.json"), "w"), indent=1)
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


QUESTION_SHAPE = '{"question": "...?", "assumption": "..."}'


def problems_questions(qs):
    """Everything wrong with the planner's questions for the owner: each is exactly a question (with a '?') and the
    reading the plan assumed, nothing else."""
    if not isinstance(qs, list):
        return [f"questions must be a list, each {QUESTION_SHAPE}"]
    bad = []
    for i, q in enumerate(qs, 1):
        if not isinstance(q, dict):
            bad.append(f"question {i} must be a question and its assumption, {QUESTION_SHAPE}")
            continue
        extra = sorted(str(k) for k in q if k not in ("question", "assumption"))
        if extra:
            bad.append(f"question {i} has {', '.join(extra)}: a question is only the question and its assumption, "
                       "never options or a recommendation")
        for field in ("question", "assumption"):
            if not filled(q.get(field)):
                bad.append(f"question {i} has no {field}: it must be non-empty text")
        if filled(q.get("question")) and "?" not in q["question"]:
            bad.append(f"question {i} asks nothing: its question needs a '?'")
    return bad


def problems_review(r):
    """Everything wrong with a review.json, as plain sentences; empty when it is well formed."""
    bad = []
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
    for i, f in enumerate(r.get("issues_found") or [], 1):
        if not isinstance(f, dict) or not all(str(f.get(k, "")).strip() for k in ("title", "why", "evidence")):
            bad.append(f"issue found {i} needs a title, why and evidence")
    if "questions" in r:
        bad.append("the reviewer never asks the owner; escalate on round three instead")
    return bad


def problems_asks(r, ids):
    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
    asks = r.get("asks")
    if not isinstance(asks, list) or not asks:
        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
                "\"source\": \"a link to where they said it\", \"criterion\": \"N.k\" or \"missing\"}"]
    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
    for a in good:
        c = a["criterion"].strip()
        if c != "missing" and c not in ids:
            bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
                       f"({', '.join(ids) or 'none'})")
    gone = [a["ask"] for a in good if a["criterion"].strip() == "missing"]
    if r.get("verdict") == "approve" and gone:
        bad.append("an approve keeps every ask, but these are marked missing: " + "; ".join(f'"{g}"' for g in gone))
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


def filled(v):
    """True for a non-empty string."""
    return isinstance(v, str) and bool(v.strip())


def problems_items(h, field, keys, name=None):
    """Everything wrong with an optional list of objects that each need some non-empty text fields, naming the field."""
    v = h.get(field, [])
    if not isinstance(v, list):
        return [f"{field} must be a list"]
    bad = []
    for i, x in enumerate(v, 1):
        label = f"{field} item {i}" + (f" ({x.get(name)})" if name and isinstance(x, dict) and filled(x.get(name)) else "")
        if not isinstance(x, dict):
            bad.append(f"{label} must be an object with {', '.join(keys)}")
            continue
        missing = [k for k in keys if not filled(x.get(k))]
        if missing:
            bad.append(f"{label} needs {', '.join(missing)}")
    return bad


def problems_shape(kind, h):
    """Everything missing, wrongly typed or wrongly shaped in a hand-back against its prompt's shape, each naming the field."""
    bad = []
    if kind == "review":
        prev = h.get("previous_step")
        if not isinstance(prev, dict):
            bad.append("previous_step must be an object with did, decided and open")
        elif not all(isinstance(prev.get(k, []), list) and all(filled(x) for x in prev.get(k, [])) for k in ("did", "decided", "open")):
            bad.append("previous_step: did, decided and open must each be a list of lines")
        if h.get("verdict") not in VERDICTS:
            bad.append("verdict must be approve, block or escalate")
        if not filled(h.get("summary")):
            bad.append("summary must be one non-empty sentence")
        bad += problems_items(h, "blockers", ("id", "criterion", "problem", "evidence", "fix"), name="id")
        for i, b in enumerate(h.get("blockers") if isinstance(h.get("blockers"), list) else [], 1):
            if isinstance(b, dict) and ("test" not in b or not (b["test"] is None or isinstance(b["test"], str))):
                bad.append(f"blockers item {i}" + (f" ({b.get('id')})" if filled(b.get("id")) else "") + " needs test: a test name, or null")
            if isinstance(b, dict) and b.get("fixer") not in FIXERS:
                bad.append(f"blockers item {i}" + (f" ({b.get('id')})" if filled(b.get("id")) else "") + " needs fixer: worker or planner")
        bad += problems_items(h, "notes", ("text", "evidence"))
        bad += problems_items(h, "outside_plan", ("file", "change"))
        bad += problems_items(h, "issues_found", ("title", "why", "evidence"))
        resolved = h.get("resolved", [])
        if not isinstance(resolved, list) or not all(filled(x) for x in resolved):
            bad.append("resolved must be a list of blocker ids")
        return bad
    if not filled(h.get("summary")):
        bad.append("summary must be two non-empty sentences")
    crit = h.get("criteria")
    if not isinstance(crit, dict) or not crit:
        bad.append("criteria must be an object giving one line per criterion")
    else:
        bad += [f"criteria: the line for {k} must be non-empty text" for k, v in crit.items() if not filled(v)]
    if not filled(h.get("evidence")):
        bad.append("evidence must name the last test command and its result line")
    bad += problems_items(h, "outside_scope", ("file", "why"))
    bad += problems_items(h, "suspect_tests", ("test", "evidence"))
    bad += problems_items(h, "replies", ("blocker", "answer", "why"), name="blocker")
    for i, r in enumerate(h.get("replies") if isinstance(h.get("replies"), list) else [], 1):
        if isinstance(r, dict) and filled(r.get("answer")) and r["answer"] not in ANSWERS:
            bad.append(f"replies item {i}: answer must be fixed or disagree")
    return bad


def plan_criteria(plan, number):
    """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
    count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
    if plan.get("kind") == "feature":
        stories = plan.get("stories") if isinstance(plan.get("stories"), list) else []
        return [f"S{s}.{k}" for s, st in enumerate(stories, 1) if isinstance(st, dict) for k in range(1, count(st) + 1)]
    return [f"{number}.{k}" for k in range(1, count(plan) + 1)]


def problems_plan(kind, h, plan, number):
    """Everything in a hand-back that does not match the approved plan: a work line per criterion, exactly, and every
    blocker on one of the plan's criteria, naming either no test or one of the plan's tests for that criterion."""
    ids = plan_criteria(plan, number)
    bad = []
    if kind == "work":
        crit = h.get("criteria")
        if isinstance(crit, dict):
            bad += [f"criteria has no line for {c}, a criterion of the plan" for c in ids if c not in crit]
            bad += [f"criteria gives a line for {c}, which the plan does not have" for c in crit if c not in ids]
        return bad
    tests = plan.get("tests") if isinstance(plan.get("tests"), dict) else {}
    for b in h.get("blockers") if isinstance(h.get("blockers"), list) else []:
        if not isinstance(b, dict) or not filled(b.get("criterion")):
            continue
        c, t = b["criterion"], b.get("test")
        if c not in ids:
            bad.append(f"blocker {b.get('id')} names {c}, which is not a criterion of the plan ({', '.join(ids) or 'none'})")
        elif filled(t) and t not in (tests.get(c) or []):
            bad.append(f"blocker {b.get('id')} names {t}, which is not one of the plan's tests for {c}")
    return bad


def load(path, name):
    """Read a JSON object from a file; return (object, None) or (None, the reason naming the file)."""
    try:
        data = json.load(open(path))
    except FileNotFoundError:
        return None, f"{name} is missing ({path})"
    except (OSError, json.JSONDecodeError) as e:
        return None, f"{name} is not valid JSON ({path}): {e}"
    if not isinstance(data, dict):
        return None, f"{name} is not a JSON object ({path})"
    return data, None


def check(kind, path, plan_path=None, number=None):
    """Check one hand-back file against its prompt's shape and, when given, the approved plan and the issue's number.
    Print every problem and return 1 if there are any, else 0."""
    data, err = load(path, os.path.basename(path))
    if err:
        print(err)
        return 1
    bad = problems_shape(kind, data) or (problems_review if kind == "review" else problems_work)(data)
    if plan_path is not None:
        plan, err = load(plan_path, "plan.json")
        if err:
            bad.append(f"{err}: the hand-back can't be checked against the plan")
        elif not str(number or "").isdigit():
            bad.append(f"the issue number {number!r} is not a number: the hand-back can't be checked against the plan")
        else:
            bad += problems_plan(kind, data, plan, number)
            if kind == "review" and os.environ.get("STAGE") == "plan":
                bad += problems_asks(data, plan_criteria(plan, number))
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
    plan_path = os.path.join(dest, "plan.json")
    if key == "worker" and os.path.isfile(plan_path):
        try:
            if json.load(open(plan_path)).get("kind") == "feature":
                bad.append("plan.json is a split: /work files its stories as sub-issues, no worker builds it")
        except (json.JSONDecodeError, AttributeError):
            pass
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


def autopilot_of(body):
    """"start" or "stop" when a comment's first line begins `/autopilot start` or `/autopilot stop`; otherwise None."""
    first = (body or "").strip().splitlines()[0].split() if (body or "").strip() else []
    if len(first) >= 2 and first[0].lower() == "/autopilot" and first[1].lower() in ("start", "stop"):
        return first[1].lower()
    return None


def route(body, on_pr, number, head="", pr_body=""):
    """What a code owner's comment starts: {role, stage, issue}, or None when it starts nothing.

    /review on an issue grades the plan; on a pull request it grades the work. A pull request routes to its issue.
    `/autopilot start|stop` starts no stage: it routes to {autopilot, issue}, the issue whose tree it switches."""
    role, switch = command_of(body), autopilot_of(body)
    if not role and not switch:
        return None
    issue = issue_of_pr(head, pr_body) if on_pr else str(number)
    if not issue:
        return None
    if switch:
        return {"autopilot": switch, "issue": issue}
    stage = ("pr" if on_pr else "plan") if role == "reviewer" else ""
    return {"role": role, "stage": stage, "issue": issue}


AUTOPILOT = "autopilot"


def issue_tree(repo, number):
    """The issue and every sub-issue under it, at every level, from GitHub's native sub-issues; parents first."""
    tree, todo = [], [int(number)]
    while todo:
        n = todo.pop(0)
        if n in tree:
            continue
        tree.append(n)
        # GitHub allows at most 100 sub-issues per parent, so one page holds them all.
        todo += [c["number"] for c in json.loads(gh("api", f"repos/{repo}/issues/{n}/sub_issues?per_page=100") or "[]")]
    return tree


def switch_autopilot(repo, number, switch):
    """Put the issue's tree on autopilot ("start") or take it off ("stop"), touching no other label; returns the
    issues switched: those whose `autopilot` label was added or removed."""
    switched = []
    for n in issue_tree(repo, number):
        labels = {l["name"] for l in json.loads(gh("api", f"repos/{repo}/issues/{n}")).get("labels", [])}
        if switch == "start" and AUTOPILOT not in labels:
            # Adding a label GitHub does not have yet creates it.
            gh("api", "-X", "POST", f"repos/{repo}/issues/{n}/labels", "-f", f"labels[]={AUTOPILOT}")
            switched.append(n)
        elif switch == "stop" and AUTOPILOT in labels:
            gh("api", "-X", "DELETE", f"repos/{repo}/issues/{n}/labels/{AUTOPILOT}")
            switched.append(n)
    return switched


def autopilot_comment(number, switch, switched):
    """The one comment `/autopilot start|stop` leaves where it was said: every issue it switched."""
    names = ", ".join(f"#{n}" for n in switched)
    if switch == "start":
        said = f"Autopilot is on for {names}." if switched else f"#{number} and every issue under it were already on autopilot."
    else:
        said = f"Autopilot is off for {names}." if switched else f"No issue in #{number}'s tree was on autopilot."
    return said + " No stage was started.\n"


def next_step(items, rec, owners, rounds=3):
    """The river: what follows the run that just finished. ("start", role, stage) or ("stop", why), decided by code.

    A planner hands to the reviewer unless it has questions for the owner. A worker hands to the reviewer. A blocking
    review sends the work back, until three blocks in a row at that stage since the owner last spoke; then it is the
    owner's call. An approval, a question, an escalation or a hand-back code rejected always stops for the owner. A
    cancelled run starts nothing and mentions no one: whoever cancelled it knows."""
    role, stage, h = rec.get("role"), rec.get("stage") or "", rec.get("handback") or {}
    if role == "cancelled":
        return ("cancelled", "Nothing starts by itself after a cancel. Give the command again to start this stage.")
    if role == "not-started":
        return ("stop", "Nothing ran, see why above. Fix the cause, then give the command again.")
    if not rec.get("check", {}).get("passed"):
        return ("stop", "The hand-back was rejected by code, see the problems above. Fix the cause, then start the stage again.")
    if role == "planner":
        if h.get("questions"):
            return ("stop", "The plan has questions for you. Answer with `/plan` and your words, or say `/review` to go on with its assumptions.")
        return ("start", "reviewer", "plan")
    if role == "worker":
        return ("start", "reviewer", "pr")
    if role != "reviewer":
        return ("stop", "")
    verdict = h.get("verdict")
    if verdict == "approve" and stage == "plan" and test_fix(items, owners):
        return ("start", "worker", "")
    if verdict == "approve":
        return ("stop", "The plan is approved. Say `/work` to build it, or `/plan` with changes." if stage == "plan" else
                "The work is approved. Merge the pull request, or review it with a command to send it back.")
    if verdict == "escalate":
        return ("stop", "The reviewer escalated this to you, see why above.")
    last_owner = max([i for i, c in enumerate(items) if (c.get("author") or {}).get("login") in owners], default=-1)
    later = [r for r in records(items[last_owner + 1:]) if r.get("role") == "reviewer" and (r.get("stage") or "") == stage]
    blocks = sum(1 for r in later if (r.get("handback") or {}).get("verdict") == "block") + 1
    if blocks >= rounds:
        return ("stop", f"{blocks} blocking reviews in a row without agreement. Your call: `/plan`, `/work` or `/review` with your words.")
    to_planner = stage == "plan" or any(isinstance(b, dict) and b.get("fixer") == "planner" for b in h.get("blockers", []))
    return ("start", "planner" if to_planner else "worker", "")


def criteria_texts(plan):
    """A plan's criteria as the owner approves them: every acceptance and non-functional criterion's text, in order."""
    return [[c.get("text") if isinstance(c, dict) else c for c in plan.get(k) or []] for k in ("acceptance_criteria", "non_functional")]


def test_fix(items, owners):
    """True when the newest plan is a re-plan a code review asked for with a test blocker, the owner has not spoken
    since that review, and its criteria are exactly those of the plan the owner approved with `/work`."""
    owner_at = [i for i, c in enumerate(items) if (c.get("author") or {}).get("login") in owners]
    works = [i for i in owner_at if command_of(items[i].get("body")) == "worker"]
    if not works:
        return False
    review = next((i for i in range(len(items) - 1, works[-1], -1) if is_record(items[i], "reviewer", "pr")), None)
    if review is None or any(i > review for i in owner_at):
        return False
    r = records([items[review]])[0]
    h = r.get("handback") or {}
    if not r.get("check", {}).get("passed") or h.get("verdict") != "block" or \
            not any(isinstance(b, dict) and b.get("fixer") == "planner" for b in h.get("blockers", [])):
        return False
    replan = latest(records(items[review + 1:]), "planner")
    agreed = latest(records(items[:works[-1]]), "planner")
    return bool(replan and agreed) and criteria_texts(replan["handback"]) == criteria_texts(agreed["handback"])


STAGE_COLUMN = {("planner", ""): "Plan", ("reviewer", "plan"): "Plan", ("worker", ""): "Work", ("reviewer", "pr"): "Review"}


def board_place(rec, step):
    """Where the card goes after this run: the column of the stage now running, or of this stage when it stops for
    the owner, and the Needs you pill exactly when the river stops for the owner (not after a cancel)."""
    if step[0] == "start":
        return STAGE_COLUMN[(step[1], step[2] if step[1] == "reviewer" else "")], False
    return STAGE_COLUMN.get((rec.get("attempt") or rec.get("role"), rec.get("stage") or ""), "Plan"), step[0] == "stop"


def move_card(repo, number, column, needs_you, spec, q=None):
    """Put the issue and its open pull request in that column, with the Needs you pill, or else the Autopilot pill while
    the issue is on autopilot."""
    from dokima import board
    b = board.Board(spec, repo, q or board.gql)
    on = not needs_you and b.autopilot("issue", int(number))
    targets = [("issue", int(number))]
    pr = gh("pr", "list", "-R", repo, "--head", f"try/issue-{number}", "--state", "open", "--json", "number", "-q", ".[0].number").strip()
    if pr:
        targets.append(("pr", int(pr)))
    for kind, n in targets:
        iid = b.item(kind, n)
        b.set(iid, "Status", column)
        b.set(iid, "Action", board.pill(needs_you, on))
    return targets


def next_line(step, owners):
    """The last line of a card: what happens next, mentioning the owner when it is their turn."""
    if step[0] == "start":
        who = {"planner": "The planner", "worker": "The worker", "reviewer": "The reviewer"}[step[1]]
        return f"**Next:** {who} starts now."
    if step[0] == "cancelled":
        return f"**Next:** {step[1]}"
    mention = " ".join(f"@{o}" for o in owners)
    return f"**Next:** {mention} {step[1]}".strip()


def main(argv):
    """agent pack N ROLE STAGE DIR | agent check-pack ROLE STAGE DIR | agent check review|work FILE PLAN N |
    agent record ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR  (writes OUT/record.json and OUT/comment.md) |
    agent not-started ROLE STAGE OUT WHY_FILE  (the same, for a run or command that failed before its agent started) |
    agent cancelled ROLE STAGE OUT STARTED LOG_DIR  (the same, for a run someone cancelled) |
    agent card ROLE STAGE ready|working  (prints the run's live card, which is not a record) |
    agent queue ROLE STAGE N [queued|handoff]  (puts up a run's queued card where its record will go, prints its id) |
    agent autopilot start|stop N  (switches N's issue tree on or off autopilot, prints the comment naming what switched)"""
    if argv[1] == "pack":
        has_plan = pack(os.environ["GITHUB_REPOSITORY"], argv[2], argv[3], argv[4], argv[5])
        return 0 if has_plan or argv[3] == "planner" else 3
    if argv[1] == "check":
        if len(argv) < 6:
            print("the check needs plan.json and the issue number: agent check review|work FILE PLAN N")
            return 1
        return check(argv[2], argv[3], argv[4], argv[5])
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
    if argv[1] == "not-started":
        role, stage, out, why_file = argv[2:6]
        meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "started_by": os.environ.get("GITHUB_ACTOR"),
                "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"}
        rec = not_started(role, stage, open(why_file).read() if os.path.exists(why_file) else "", meta)
        json.dump(rec, open(os.path.join(out, "record.json"), "w"), indent=1)
        open(os.path.join(out, "comment.md"), "w").write(render(rec))
        return 0
    if argv[1] == "cancelled":
        role, stage, out, started, log_dir = argv[2:7]
        meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "started_by": os.environ.get("GITHUB_ACTOR"),
                "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"}
        if started == "true":
            meta.update({"models": models_used(log_dir), "report": run_report(os.path.join(out, "claude.json")),
                         "log": os.environ.get("LOG_URL")})
        rec = cancelled(role, stage, started == "true", meta)
        json.dump(rec, open(os.path.join(out, "record.json"), "w"), indent=1)
        open(os.path.join(out, "comment.md"), "w").write(render(rec))
        return 0
    if argv[1] == "card":
        sys.stdout.write(live_card(argv[2], argv[3], argv[4]))
        return 0
    if argv[1] == "queue":
        print(queue(argv[2], argv[3], argv[4], argv[5] if len(argv) > 5 else "queued"))
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
    if argv[1] == "split":
        repo, parent = os.environ["GITHUB_REPOSITORY"], argv[2]
        _, items = conversation(repo, parent)
        recs = records(items)
        if not approved(recs) or latest(recs, "planner")["handback"].get("kind") != "feature":
            print("The newest plan is not an approved split.")
            return 1
        rec = file_split(repo, parent, recs)
        rec["run"] = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
        card = os.environ.get("CARD_ID", "")
        if card:
            # The command's queued card becomes the Split filed record, edited in place.
            gh("api", "-X", "PATCH", f"repos/{repo}/issues/comments/{card}", "-f", f"body={render(rec)}", "--silent")
        elif not any(r.get("role") == "split" for r in recs):
            gh("issue", "comment", parent, "-R", repo, "--body", render(rec))
        spec = os.environ.get("DOKIMA_BOARD", "").strip()
        if spec:
            from dokima import board
            b = board.Board(spec, repo, board.gql)
            for f in rec["handback"]["stories"]:
                iid = b.item("issue", f["issue"])
                b.set(iid, "Status", "Backlog")
                b.set(iid, "Action", board.pill(False, b.autopilot("issue", f["issue"])))
            iid = b.item("issue", int(parent))
            b.set(iid, "Status", "Work")
            b.set(iid, "Action", board.pill(False, b.autopilot("issue", int(parent))))
        return 0
    if argv[1] == "kind":
        _, items = conversation(os.environ["GITHUB_REPOSITORY"], argv[2])
        recs = records(items)
        plan = latest(recs, "planner")
        print(plan["handback"].get("kind", "") if plan and approved(recs) else "")
        return 0
    if argv[1] == "next":
        number, out = argv[2], argv[3]
        owners = [o for o in os.environ.get("OWNERS", "").split(",") if o]
        rec = json.load(open(os.path.join(out, "record.json")))
        # A run that never started stops for the owner, and a cancelled one stops, whatever the conversation says,
        # so it is not read.
        items = [] if rec.get("role") in ("not-started", "cancelled") else conversation(os.environ["GITHUB_REPOSITORY"], number)[1]
        step = next_step(items, rec, owners)
        with open(os.path.join(out, "comment.md"), "a") as f:
            f.write("\n" + next_line(step, owners) + "\n")
        column, needs = board_place(json.load(open(os.path.join(out, "record.json"))), step)
        open(os.path.join(out, "board.txt"), "w").write(f"{column} {'needs' if needs else 'none'}\n")
        print(" ".join(step) if step[0] == "start" else "stop")
        return 0
    if argv[1] == "board":
        spec = os.environ.get("DOKIMA_BOARD", "").strip()
        if not spec:
            print("No board set; nothing to move.")
            return 0
        try:
            column, needs = open(os.path.join(argv[3], "board.txt")).read().split()
        except (OSError, ValueError):
            # Deciding what follows failed, so the river stopped: the run's own stage, with Needs you.
            try:
                rec = json.load(open(os.path.join(argv[3], "record.json")))
            except (OSError, json.JSONDecodeError):
                rec = {"role": os.environ.get("ROLE", ""), "stage": os.environ.get("STAGE", "")}
            column, needs = board_place(rec if isinstance(rec, dict) else {}, ("stop",))
            needs = "needs" if needs else "none"
        for kind, n in move_card(os.environ["GITHUB_REPOSITORY"], argv[2], column, needs == "needs", spec):
            print(f"board: {kind} #{n} -> {column}{' · Needs you' if needs == 'needs' else ''}")
        return 0
    if argv[1] == "autopilot":
        switch, number = argv[2], argv[3]
        switched = switch_autopilot(os.environ["GITHUB_REPOSITORY"], number, switch)
        sys.stdout.write(autopilot_comment(number, switch, switched))
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
    try:
        sys.exit(main(sys.argv))
    except subprocess.CalledProcessError as e:
        # GitHub's own error, so the step that failed can say why.
        sys.stderr.write((e.stderr or str(e)).strip() + "\n")
        sys.exit(1)
