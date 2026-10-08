"""While an agent works, its live card shows how many minutes it has worked and the step it is on (#187).

The owner asked that no key ever sit on the agent's machine. So the work is split across two machines of the same
run. On the agent's machine, beside the agent and with no key, `agent steps LOG_DIR STOP_FILE` writes one line
`dokima-step: <step>` to the job's log every DOKIMA_PROGRESS_EVERY seconds (60 when unset) until STOP_FILE exists.
A second job of agent.yml, on its own machine, holds the only key: `agent follow ROLE STAGE WHERE` reads the run's
jobs and the agent job's log from GitHub and edits the run's live card on issue or PR WHERE in place, until the agent
step ends.

The commands these tests run:
- `agent step LOG_DIR` prints the step of the newest tool call in the session logs under LOG_DIR.
- `agent progress ROLE STAGE STARTED STEP` prints the live card: STARTED is when the agent started, as GitHub writes
  a time (2026-10-08T05:40:34Z); STEP is a step name, or empty when the step is not known.
- `agent steps` and `agent follow` as above. Every SCRUB_* value in the environment is a secret.

`agent follow` talks to the fake GitHub below. It reads the run's jobs from `repos/o/r/actions/runs/42/jobs` (or
`.../runs/42/attempts/1/jobs`): the agent's job is named `run` and its agent step `The agent (Claude Code)`; the
step's `started_at` is when the agent started. It reads the agent job's log from `repos/o/r/actions/jobs/ID/logs`,
which GitHub may refuse with 404 while the job runs. It finds the run's card among the comments on
`repos/o/r/issues/WHERE/comments`: Dokima's bot's live card whose run link ends in /actions/runs/42. The fake does not
apply --jq or -q; the command reads the JSON itself.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import pytest

import test_start as ts
from test_start import STORY_PLANNED, Run

from dokima import agent

ROOT = ts.ROOT
EVERY = 0.5
PHASE = 3
STEP = re.compile(r"working for (\d+) min(?: · ([^\n<*]+))?")
STEP_LINE = re.compile(r"dokima-step: ([^\n]+)")
ICON = re.compile(r'/dokima/icons/([A-Za-z0-9_-]+)\.svg')
AGENT_STEP = "The agent (Claude Code)"

SLOW_CLAUDE = r'''#!/usr/bin/env python3
"""A slower stand-in for Claude Code: reads the issue, writes a test, checks its output, a few seconds each.

Like the fake in test_start.py it keeps what GitHub showed when it started and its own environment, then writes its
session log one tool call at a time, each with the time it was made, and hands back the review the test chose. When
it ends it notes how many calls GitHub had seen by then (calls-at-agent-end)."""
import datetime, json, os, shutil, time
d = os.environ["FAKE_GH_DIR"]
store = os.path.join(d, "comments.json")
json.dump(json.load(open(store)) if os.path.exists(store) else [], open(os.path.join(d, "at-agent-start.json"), "w"))
json.dump(dict(os.environ), open(os.path.join(d, "agent-env.json"), "w"))
open(os.path.join(d, "agent-started-at"), "w").write(str(time.time()))
open(os.environ["FAKE_CLAUDE_MARK"], "w").write("started")
logs = os.path.join(os.environ["HOME"], ".claude", "projects", "p")
os.makedirs(logs, exist_ok=True)
log = os.path.join(logs, "s.jsonl")
def entry(content):
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    open(log, "a").write(json.dumps({"timestamp": t, "message": {"model": os.environ["MODEL"], "role": "assistant",
                                                                  "content": content}}) + "\n")
def tool(name, i):
    entry([{"type": "tool_use", "id": "t", "name": name, "input": i}])
    time.sleep(PHASE)
tool("Read", {"file_path": os.path.join(os.environ["PACK"], "issue.md")})
tool("Write", {"file_path": os.path.join(os.getcwd(), "tests", "test_x.py"), "content": "def test_a(): pass\n"})
tool("Bash", {"command": "python3 -m dokima.agent check review " + os.environ["OUT"] + "/review.json plan.json 57"})
shutil.copy(os.environ["FAKE_REVIEW"], os.path.join(os.environ["OUT"], "review.json"))
entry("Done.")
open(os.path.join(d, "calls-at-agent-end"), "w").write(str(sum(1 for _ in open(os.path.join(d, "calls-meta.jsonl")))))
print(json.dumps({"num_turns": 3, "duration_ms": 9000, "usage": {}}))
'''.replace("PHASE", str(PHASE))

FOLLOW_GH = r'''#!/usr/bin/env python3
"""A stand-in for the GitHub CLI for `agent follow`: the run's jobs, the agent job's log and the issue's comments.

state.json says what GitHub shows now: jobs (the run's jobs, each with its steps), log (the agent job's log as text,
or null when GitHub refuses it with 404, as it does while a job runs), down (every call fails with HTTP 502),
refuse_edits (every edit of a comment fails) and record (once set, the card has become this record, as the run's
own job would make it). Comments live in comments.json with every version of their body. Like gh, a call with -f/-F
fields and no -X is a POST. Every call is kept in calls.jsonl with the key it was made with."""
import json, os, re, sys
d = os.environ["FAKE_GH_DIR"]
a = sys.argv[1:]
open(os.path.join(d, "calls.jsonl"), "a").write(json.dumps({"args": a, "token": os.environ.get("GH_TOKEN", "")}) + "\n")
state = json.load(open(os.path.join(d, "state.json")))
def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)
if state.get("down"):
    fail("HTTP 502: Server Error (https://api.github.com/)")
if a[:1] != ["api"]:
    fail("this fake GitHub only answers gh api, not gh " + " ".join(a[:2]))
if "-q" in a or "--jq" in a:
    fail("this fake GitHub does not filter with --jq or -q; read the JSON")
fields = any(x in ("-f", "-F", "--field", "--raw-field", "--input") for x in a)
method = next((a[i + 1].upper() for i, x in enumerate(a[:-1]) if x in ("-X", "--method")), "POST" if fields else "GET")
path = next((x.lstrip("/").split("?")[0] for x in a[1:] if re.match(r"/?(repos|installation)/", x)), "")
STORE = os.path.join(d, "comments.json")
cs = json.load(open(STORE))
def save():
    json.dump(cs, open(STORE + ".tmp", "w"), indent=1)
    os.replace(STORE + ".tmp", STORE)
if state.get("record"):
    for c in cs:
        if c["id"] == 5001 and c["versions"][-1] != state["record"]:
            c["versions"].append(state["record"])
            save()
def shown(c):
    return {"id": c["id"], "body": c["versions"][-1], "user": {"login": c["author"]},
            "html_url": f"https://github.com/o/r/issues/{c['number']}#issuecomment-{c['id']}"}
def body():
    if "--input" in a:
        p = a[a.index("--input") + 1]
        return json.load(sys.stdin if p == "-" else open(p)).get("body")
    for i, x in enumerate(a[:-1]):
        if x in ("-f", "-F", "--field", "--raw-field") and a[i + 1].startswith("body="):
            v = a[i + 1][5:]
            if x in ("-F", "--field") and v.startswith("@"):
                return sys.stdin.read() if v == "@-" else open(v[1:]).read()
            return v
    return None
m = re.fullmatch(r"repos/o/r/actions/runs/42(?:/attempts/1)?/jobs", path)
if m and method == "GET":
    print(json.dumps({"total_count": len(state["jobs"]), "jobs": state["jobs"]}))
    sys.exit(0)
m = re.fullmatch(r"repos/o/r/actions/jobs/(\d+)/logs", path)
if m and method == "GET":
    if state.get("log") is None or int(m.group(1)) != 7001:
        fail(f"HTTP 404: Not Found (https://api.github.com/{path})")
    sys.stdout.write(state["log"])
    sys.exit(0)
m = re.fullmatch(r"repos/o/r/issues/(\d+)/comments", path)
if m:
    if method != "GET":
        cs.append({"id": 6000 + len(cs), "number": int(m.group(1)), "author": "dokima-runtime", "versions": [body()]})
        save()
        print(json.dumps(shown(cs[-1])))
    else:
        print(json.dumps([shown(c) for c in cs if c["number"] == int(m.group(1))]))
    sys.exit(0)
m = re.fullmatch(r"repos/o/r/issues/comments/(\d+)", path)
if m:
    c = next((c for c in cs if c["id"] == int(m.group(1))), None)
    if c is None:
        fail(f"HTTP 404: Not Found (https://api.github.com/{path})")
    if method in ("PATCH", "POST"):
        if state.get("refuse_edits"):
            fail(f"HTTP 502: Server Error (https://api.github.com/{path})")
        c["versions"].append(body())
        save()
    print(json.dumps(shown(c)))
    sys.exit(0)
fail(f"HTTP 404: Not Found (https://api.github.com/{path})")
'''


# ---------- helpers ----------

def env_for(tmp, **extra):
    """An environment for Dokima's commands: its code from this repo, a fake gh on PATH, the pack and hand-back folders."""
    bin_dir, gh_dir = os.path.join(tmp, "bin"), os.path.join(tmp, "gh")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(gh_dir, exist_ok=True)
    open(os.path.join(bin_dir, "gh"), "w").write(FOLLOW_GH.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
    os.chmod(os.path.join(bin_dir, "gh"), 0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("SCRUB_", "DOKIMA_PROGRESS", "GH_", "GITHUB_"))}
    env.update({"PATH": bin_dir + os.pathsep + os.environ["PATH"], "PYTHONPATH": ROOT, "FAKE_GH_DIR": gh_dir,
                "GH_TOKEN": "fake-token", "GITHUB_REPOSITORY": "o/r", "GITHUB_RUN_ID": "42", "GITHUB_RUN_ATTEMPT": "1",
                "GITHUB_SERVER_URL": "https://github.com",
                # Outside pytest's own temp folder, whose name holds the word pytest, as the real /tmp/pack does not.
                "PACK": tempfile.mkdtemp(prefix="pack-"), "OUT": tempfile.mkdtemp(prefix="dokima-out-")})
    env.update(extra)
    set_state(env)
    json.dump([], open(os.path.join(gh_dir, "comments.json"), "w"))
    return env


def iso(seconds_ago=0):
    """A time seconds_ago in the past, the way GitHub writes it."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - seconds_ago))


def stamp(seconds_ago=0):
    """A session-log timestamp seconds_ago in the past."""
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() - seconds_ago))


def cmd(env, *args, timeout=30):
    """Run one `python3 -m dokima.agent` command and return what it did."""
    return subprocess.run([sys.executable, "-m", "dokima.agent", *args], cwd=ROOT, env=env, capture_output=True,
                          text=True, timeout=timeout)


def progress(env, started_iso, step):
    """The card `agent progress` prints for a planner whose agent started at started_iso and is on step."""
    return cmd(env, "progress", "planner", "", started_iso, step)


def step_name(env, log_dir):
    """The step `agent step` prints for the session logs under log_dir, stripped."""
    p = cmd(env, "step", log_dir)
    return p, p.stdout.strip()


def write_log(path, entries):
    """A session log at path: one JSON line per entry, each (timestamp, message)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        for t, m in entries:
            f.write(json.dumps({"timestamp": t, "message": m}) + "\n")


def tool_call(name, i):
    """An assistant message that makes one tool call."""
    return {"role": "assistant", "model": "claude-opus-5-5", "content": [{"type": "tool_use", "id": "x", "name": name, "input": i}]}


def card_shows(card, crit):
    """The minutes and step a card shows, as (minutes, step or None); fails the test, naming crit, when it shows neither."""
    m = STEP.search(card or "")
    assert m, f"{crit}: the card does not say 'working for N min':\n{(card or '')[:800]}"
    return int(m.group(1)), (m.group(2).strip().rstrip(".").strip() if m.group(2) else None)


def set_state(env, **state):
    """What the fake GitHub shows from now on (see FOLLOW_GH); written whole, so the fake never reads half of it."""
    p = os.path.join(env["FAKE_GH_DIR"], "state.json")
    s = {"jobs": [], "log": None}
    s.update(state)
    json.dump(s, open(p + ".tmp", "w"))
    os.replace(p + ".tmp", p)


def jobs(agent_status, started_iso=None, job_status="in_progress"):
    """The run's jobs as GitHub lists them: the agent's job `run` with its agent step, and the job that follows it."""
    before = {"name": "Build the starting pack", "status": "completed", "conclusion": "success",
              "started_at": iso(900), "completed_at": iso(890)}
    step = {"name": AGENT_STEP, "status": agent_status, "conclusion": None if agent_status != "completed" else "success",
            "started_at": started_iso, "completed_at": iso(0) if agent_status == "completed" else None}
    return [{"id": 7001, "name": "run", "status": job_status, "started_at": iso(950), "steps": [before, step]},
            {"id": 7002, "name": "progress", "status": "in_progress", "started_at": iso(950), "steps": []}]


def job_log(*steps):
    """The agent job's log as GitHub serves it: every line stamped, the reporter's step lines among others."""
    lines = [f"{iso(60)}.0000000Z ##[group]Run {AGENT_STEP}"]
    lines += [f"{iso(50 - i)}.0000000Z dokima-step: {s}" for i, s in enumerate(steps)]
    return "\n".join(lines) + "\n"


def seed_cards(env, where=57):
    """The run's live card (comment 5001), another run's live card (5002) and an owner's comment on issue or PR where."""
    other = "<!-- dokima-live -->\nworking\n\n<sub>[run](https://github.com/o/r/actions/runs/41)</sub>\n"
    mine = "<!-- dokima-live -->\nworking\n\n<sub>[run](https://github.com/o/r/actions/runs/42)</sub>\n"
    cs = [{"id": 5000, "number": where, "author": "owner-person", "versions": ["/plan see https://github.com/o/r/actions/runs/42"]},
          {"id": 5001, "number": where, "author": agent.BOT, "versions": [mine]},
          {"id": 5002, "number": where, "author": agent.BOT, "versions": [other]}]
    json.dump(cs, open(os.path.join(env["FAKE_GH_DIR"], "comments.json"), "w"))


def comments(env):
    """Every comment on the fake GitHub, by id, with every version of its body."""
    return {c["id"]: c for c in json.load(open(os.path.join(env["FAKE_GH_DIR"], "comments.json")))}


def edits(env):
    """Every version written to the run's card after the first."""
    return comments(env)[5001]["versions"][1:]


def follow(env, where="57"):
    """Start `agent follow` for a planner's run, in the background."""
    return subprocess.Popen([sys.executable, "-m", "dokima.agent", "follow", "planner", "", where], cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def ends(p, crit, within, why):
    """Wait for a background command to end with 0 within `within` seconds; fails the test, naming crit, otherwise."""
    try:
        out, err = p.communicate(timeout=within)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        pytest.fail(f"{crit}: the command was still running {within} s after {why}:\n{out[-600:]}{err[-600:]}")
    assert p.returncode == 0, f"{crit}: the command ended with exit code {p.returncode} after {why}:\n{out[-600:]}{err[-800:]}"
    return out, err


def is_live(v):
    """True when a card version is a live card that does not read as a record."""
    c = {"author": {"login": agent.BOT}, "body": v}
    return v.startswith(agent.LIVE) and agent.records([c]) == [] and not agent.is_record(c)


# ---------- the card: minutes and step ----------

def test_the_card_counts_whole_minutes_since_the_agent_started(record_property, tmp_path):
    """The card says 'working for N min', N being the whole minutes since the agent started.

    Prints the card for agents that started 0 s, 55 s, 65 s, 12 min 34 s and 62 min 5 s ago: it must say 0, 0, 1, 12
    and 62 minutes, and still be a live card with the running icon that never reads as a record. A card that counts
    from anything else, rounds up or shows a fixed number fails."""
    record_property("proves", "187.1")
    env = env_for(str(tmp_path))
    for ago, want in ((0, 0), (55, 0), (65, 1), (754, 12), (3725, 62)):
        p = progress(env, iso(ago), "writing tests")
        assert p.returncode == 0 and p.stdout.strip(), \
            f"187.1: `agent progress` printed no card for an agent that started {ago} s ago (exit {p.returncode}):\n{p.stdout[-400:]}{p.stderr[-800:]}"
        got, step = card_shows(p.stdout, "187.1")
        assert got == want, f"187.1: an agent that started {ago} s ago shows 'working for {got} min', expected {want} min"
        assert step == "writing tests", f"187.1: the card shows the step {step!r}, expected 'writing tests'"
        assert is_live(p.stdout) and "running" in ICON.findall(p.stdout), \
            f"187.1: the card is not a live card with the running icon, or reads as a record:\n{p.stdout[:600]}"
    p = progress(env, iso(125), "")
    assert p.returncode == 0, f"187.1: `agent progress` failed with no step known (exit {p.returncode}):\n{p.stderr[-800:]}"
    got, step = card_shows(p.stdout, "187.1")
    assert (got, step) == (2, None), f"187.1: with no step known the card shows {got} min and step {step!r}, expected 2 min alone"


CASES = [
    ("Read", {"file_path": "{PACK}/issue.md"}, "reading the issue"),
    ("Grep", {"pattern": "blocker", "path": "{PACK}/in"}, "reading the issue"),
    ("Bash", {"command": "cat {PACK}/open_blockers.json"}, "reading the issue"),
    ("Read", {"file_path": "/home/runner/work/r/r/dokima/agent.py"}, "reading the code"),
    ("Glob", {"pattern": "**/*.py", "path": "/home/runner/work/r/r"}, "reading the code"),
    ("Write", {"file_path": "/home/runner/work/r/r/tests/test_new.py", "content": "x"}, "writing tests"),
    ("Edit", {"file_path": "/home/runner/work/r/r/tests/test_old.py", "old_string": "a", "new_string": "b"}, "writing tests"),
    ("Edit", {"file_path": "/home/runner/work/r/r/dokima/agent.py", "old_string": "a", "new_string": "b"}, "writing code"),
    ("Write", {"file_path": "{OUT}/plan.json", "content": "{}"}, "writing its hand-back"),
    ("Bash", {"command": "python3 -m pytest -q tests/test_x.py"}, "running tests"),
    ("Bash", {"command": "python3 -m dokima.planner check 187 {OUT} && python3 -m dokima.agent check-round planner {OUT}/plan.json {PACK}"},
     "checking its output"),
    ("Bash", {"command": "python3 -m dokima.agent check work {OUT}/work.json {PACK}/plan.json 187"}, "checking its output"),
    ("Bash", {"command": "git log --oneline -5"}, "running a command"),
    ("Task", {"description": "Explore", "prompt": "find it"}, "working with sub-agents"),
    ("Agent", {"description": "Explore", "prompt": "find it"}, "working with sub-agents"),
    ("TodoWrite", {"todos": []}, "working"),
]


def test_the_step_is_named_by_code_from_the_newest_tool_call(record_property, tmp_path):
    """The agent's step is named by code from the newest tool call in its session log, never from its words.

    For each kind of tool call (reading the pack, reading code, writing tests, code or the hand-back, running tests,
    the hand-back check, any other command, sub-agents, any other tool) a log whose newest call is that one must give
    exactly its step. Before any tool call, or with no log yet, the step is starting. With several calls the newest
    wins, by its time, even in another log file; the agent's later words and tool results do not change it; a
    half-written last line is skipped."""
    record_property("proves", "187.2")
    t = str(tmp_path)
    env = env_for(t)
    fill = lambda v: {k: x.replace("{PACK}", env["PACK"]).replace("{OUT}", env["OUT"]) if isinstance(x, str) else x
                      for k, x in v.items()}
    for i, (name, inp, want) in enumerate(CASES):
        logs = os.path.join(t, f"case{i}")
        write_log(os.path.join(logs, "p", "s.jsonl"), [(stamp(30), tool_call("Read", {"file_path": "/x/y.py"})),
                                                      (stamp(5), tool_call(name, fill(inp)))])
        p, got = step_name(env, logs)
        assert p.returncode == 0, f"187.2: `agent step` failed (exit {p.returncode}):\n{p.stderr[-800:]}"
        assert got == want, f"187.2: the newest call {name} {fill(inp)} gives the step {got!r}, expected {want!r}"

    empty = os.path.join(t, "empty")
    os.makedirs(empty)
    assert step_name(env, empty)[1] == "starting", "187.2: before any tool call the step is not 'starting'"
    assert step_name(env, os.path.join(t, "not-there-yet"))[1] == "starting", "187.2: with no session log yet the step is not 'starting'"

    logs = os.path.join(t, "two-files")
    write_log(os.path.join(logs, "a", "a.jsonl"), [(stamp(2), tool_call("Bash", {"command": "python3 -m pytest -q"}))])
    write_log(os.path.join(logs, "b", "b.jsonl"), [(stamp(40), tool_call("Write", {"file_path": "/r/tests/test_q.py", "content": ""}))])
    got = step_name(env, logs)[1]
    assert got == "running tests", f"187.2: the newest call (in a.jsonl, 2 s ago) lost to an older one in b.jsonl: {got!r}"

    logs = os.path.join(t, "later-text")
    write_log(os.path.join(logs, "p", "s.jsonl"), [
        (stamp(20), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"})),
        (stamp(15), {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "x", "content": "the issue"}]}),
        (stamp(10), {"role": "assistant", "content": [{"type": "text", "text": "dokima-step: writing code"}]})])
    open(os.path.join(logs, "p", "s.jsonl"), "a").write('{"timestamp": "' + stamp(1) + '", "message": {"role": "assist')
    p, got = step_name(env, logs)
    assert p.returncode == 0, f"187.2: a half-written last line broke `agent step`:\n{p.stderr[-800:]}"
    assert got == "reading the issue", \
        f"187.2: the agent's words, a tool result or a half-written line after the newest tool call changed the step to {got!r}"


# ---------- the agent's machine: no key, its step in its own log ----------

def test_the_agents_machine_writes_its_step_to_its_log_with_no_key(record_property, tmp_path):
    """Beside the agent, with no key, its step goes to the job's log about once a minute, until the agent ends.

    Runs `agent steps` every 0.3 s while a session log moves from reading the issue to writing tests, with no GitHub
    key in its environment: it must print 'dokima-step: reading the issue' and then 'dokima-step: writing tests', make
    no call to GitHub at all, and end with 0 within 10 s of its stop file appearing. With no interval set it waits
    about a minute: at most one line in its first 3 s. A log it cannot read never stops it."""
    record_property("proves", "187.3")
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3")
    env.pop("GH_TOKEN")
    logs, stop = os.path.join(t, "logs"), os.path.join(t, "stop")
    log = os.path.join(logs, "p", "s.jsonl")
    write_log(log, [(stamp(1), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"}))])
    p = subprocess.Popen([sys.executable, "-m", "dokima.agent", "steps", logs, stop], cwd=ROOT, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.5)
    write_log(log, [(stamp(0), tool_call("Write", {"file_path": "/r/tests/test_q.py", "content": ""}))])
    open(log, "a").write("not json at all\n")
    time.sleep(1.5)
    assert p.poll() is None, f"187.3: `agent steps` stopped (exit {p.returncode}) before its stop file appeared"
    open(stop, "w").write("stop")
    out, _ = ends(p, "187.3", 10, "its stop file appeared")
    said = STEP_LINE.findall(out)
    seen = [s.strip() for i, s in enumerate(said) if s.strip() != "starting" and (i == 0 or s != said[i - 1])]
    assert seen == ["reading the issue", "writing tests"], f"187.3: the job's log did not follow the agent's steps; it got {said}"
    calls = os.path.join(env["FAKE_GH_DIR"], "calls.jsonl")
    assert not os.path.exists(calls), f"187.3: the agent's machine called GitHub: {open(calls).read()[:600]}"

    env = env_for(os.path.join(t, "default"))
    stop = os.path.join(t, "stop2")
    p = subprocess.Popen([sys.executable, "-m", "dokima.agent", "steps", logs, stop], cwd=ROOT, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(3)
    open(stop, "w").write("stop")
    out, _ = ends(p, "187.3", 70, "its stop file appeared")
    assert len(STEP_LINE.findall(out)) <= 1, f"187.3: with no interval set it wrote {len(STEP_LINE.findall(out))} lines in 3 s, not about one a minute"


def test_agent_yml_follows_the_agent_from_a_second_job_and_keeps_every_key_off_the_agents_machine(record_property):
    """The card is updated from a second job of agent.yml on its own machine; the agent's job gains no key.

    Reads the workflow. Exactly one job runs `agent follow`, and it is not the agent's job `run` and does not wait for
    it (no needs), so both run at once. The agent's step runs `agent steps` beside the agent and is given no key but
    Claude's own. The agent's job runs no `agent follow`, and makes no new app key: its keys are still the card's two
    one-call keys and the result's, as before."""
    record_property("proves", "187.3")
    jobs_ = ts.workflow("agent.yml")["jobs"]
    followers = [n for n, j in jobs_.items() if any("dokima.agent follow" in str(s.get("run", "")) for s in j.get("steps") or [])]
    assert len(followers) == 1 and followers[0] != "run", \
        f"187.3: expected one job other than the agent's to run `agent follow`, found {followers}"
    assert not jobs_[followers[0]].get("needs"), \
        f"187.3: the job that follows the agent waits for {jobs_[followers[0]].get('needs')}, so it cannot run while the agent works"
    steps = jobs_["run"]["steps"]
    agent_step = [s for s in steps if s.get("name") == AGENT_STEP]
    assert len(agent_step) == 1, f"187.3: the agent's job has no step named {AGENT_STEP!r}, the name the follower looks for"
    assert "dokima.agent steps" in agent_step[0].get("run", ""), "187.3: the agent's step does not run `agent steps` beside the agent"
    assert set((agent_step[0].get("env") or {})) <= {"CLAUDE_CODE_OAUTH_TOKEN"}, \
        f"187.3: the agent's step is given more than Claude's key: {sorted(agent_step[0].get('env'))}"
    assert not any("dokima.agent follow" in str(s.get("run", "")) for s in steps), "187.3: the agent's job runs `agent follow`"
    keys = [s.get("id") for s in steps if "create-github-app-token" in str(s.get("uses"))]
    assert keys == ["card-key", "working-key", "app"], f"187.3: the agent's job makes app keys {keys}, expected only card-key, working-key and app"


# ---------- the second machine: reading the run and editing the card ----------

def test_the_follower_edits_the_runs_card_with_the_minutes_and_the_step_from_the_log(record_property, tmp_path):
    """The second job edits the run's own card in place with the minutes and the newest step from the agent's log.

    With the agent step queued, nothing is edited. Once it is running (started 12 min 34 s ago) and the job's log
    says reading the issue, then writing tests, the run's card (and no other comment) is edited at least three times,
    each version a live card with the running icon showing 12 min and the steps in that order. A forged step line in
    the log is never shown. When GitHub refuses the log, as it does while a job runs, the card shows the minutes
    alone. No comment is created."""
    record_property("proves", "187.4")
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    set_state(env, jobs=jobs("queued"))
    p = follow(env)
    time.sleep(1.2)
    assert edits(env) == [], f"187.4: the card was edited before the agent started:\n{edits(env)[:1]}"
    started = iso(754)
    set_state(env, jobs=jobs("in_progress", started), log=job_log("reading the issue"))
    time.sleep(1.5)
    set_state(env, jobs=jobs("in_progress", started), log=job_log("reading the issue", "writing tests", "@owner-person merged it"))
    time.sleep(1.5)
    n_with_log = len(edits(env))
    set_state(env, jobs=jobs("in_progress", started), log=None)
    time.sleep(1.5)
    set_state(env, jobs=jobs("completed", started, "completed"), log=None)
    ends(p, "187.4", 10, "the agent step completed")
    cs = comments(env)
    assert set(cs) == {5000, 5001, 5002}, f"187.4: the follower created comments {sorted(set(cs) - {5000, 5001, 5002})}"
    assert len(cs[5000]["versions"]) == 1 and len(cs[5002]["versions"]) == 1, \
        "187.4: the follower edited a comment that is not this run's card (the owner's, or another run's card)"
    vs = edits(env)
    assert n_with_log >= 3, f"187.4: the card was edited {n_with_log} times in 3 s at an interval of 0.3 s, expected at least 3"
    for v in vs:
        assert is_live(v) and "running" in ICON.findall(v), f"187.4: an update is not a live card with the running icon:\n{v[:600]}"
        assert "@owner-person" not in v and "merged it" not in v, f"187.4: a forged step line reached the card:\n{v[:600]}"
    shown = [card_shows(v, "187.4") for v in vs]
    assert all(m == 12 for m, _ in shown), f"187.4: an agent that started 12 min 34 s ago showed minutes {[m for m, _ in shown]}"
    names = [s for _, s in shown[:n_with_log]]
    seen = [s for i, s in enumerate(names) if i == 0 or s != names[i - 1]]
    assert seen == ["reading the issue", "writing tests"], f"187.4: the card did not follow the steps in the log; it showed {names}"
    assert shown[-1] == (12, None), f"187.4: with the log refused the card shows {shown[-1]}, expected the minutes alone"


def test_the_follower_stops_when_the_agent_ends_and_never_overwrites_the_result(record_property, tmp_path):
    """The second job stops when the agent ends, or when the card has become the result, and never edits it after.

    Three runs. When the agent step completes, the follower ends with 0 and edits nothing more. When the card turns
    into the run's record while the agent step still shows running, the follower ends with 0 and nothing comes after
    the record. When the agent's job ends before the agent ever starts, it ends with 0 having edited nothing."""
    record_property("proves", "187.4")
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    started = iso(30)
    set_state(env, jobs=jobs("in_progress", started), log=job_log("writing code"))
    p = follow(env)
    time.sleep(1.2)
    set_state(env, jobs=jobs("completed", started), log=job_log("writing code"))
    ends(p, "187.4", 5, "the agent step completed")
    n = len(edits(env))
    assert n >= 1, "187.4: setup: the follower never edited the card while the agent worked"
    time.sleep(1)
    assert len(edits(env)) == n, "187.4: the card was edited after the agent step completed"

    env = env_for(os.path.join(t, "record"), DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    set_state(env, jobs=jobs("in_progress", started), log=job_log("writing code"))
    p = follow(env)
    time.sleep(1.2)
    rec = agent.render(ts.review_record(ts.APPROVE))
    set_state(env, jobs=jobs("in_progress", started), log=job_log("writing code"), record=rec)
    ends(p, "187.4", 5, "the card became the run's record")
    vs = comments(env)[5001]["versions"]
    assert vs[-1] == rec, f"187.4: an update came after the run's record and overwrote it:\n{vs[-1][:600]}"

    env = env_for(os.path.join(t, "never"), DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    set_state(env, jobs=jobs("skipped", None, "completed"))
    p = follow(env)
    ends(p, "187.4", 5, "the agent's job ended before the agent started")
    assert edits(env) == [], "187.4: the card was edited although the agent never started"


def test_the_follower_waits_about_a_minute_between_updates(record_property, tmp_path):
    """With no interval set, the card is updated about once a minute, not more often.

    The agent is running and its log is readable. In the first 3 s the follower must still be running and may edit
    the card once, never more."""
    record_property("proves", "187.4")
    t = str(tmp_path)
    env = env_for(t)
    seed_cards(env)
    set_state(env, jobs=jobs("in_progress", iso(5)), log=job_log("reading the code"))
    p = follow(env)
    time.sleep(3)
    alive = p.poll() is None
    p.kill()
    out, err = p.communicate()
    assert alive, f"187.4: the follower ended (exit {p.returncode}) while the agent was still working:\n{out[-400:]}{err[-600:]}"
    assert len(edits(env)) <= 1, f"187.4: with no interval set the card was edited {len(edits(env))} times in 3 s"


# ---------- non-functional ----------

def test_nothing_the_progress_shows_escapes_scrub(record_property, tmp_path):
    """No secret reaches the card or the job's log: everything shown passes through scrub() first.

    A secret equal to the text 'reading the issue' must be replaced by '[secret removed]' on the printed card, on the
    line `agent steps` writes to the job's log, and on the card `agent follow` writes to GitHub. That proves the whole
    text is scrubbed, not only the parts read from the logs."""
    record_property("proves", "187.5")
    t = str(tmp_path)
    env = env_for(t, SCRUB_PHRASE="reading the issue", DOKIMA_PROGRESS_EVERY="0.3")
    p = progress(env, iso(3), "reading the issue")
    assert p.returncode == 0 and STEP.search(p.stdout), f"187.5: setup: `agent progress` printed no card:\n{p.stdout[:600]}{p.stderr[-600:]}"
    assert "reading the issue" not in p.stdout and "[secret removed]" in p.stdout, \
        f"187.5: the printed card is not passed through scrub(): a secret equal to its step still shows:\n{p.stdout[:800]}"

    logs, stop = os.path.join(t, "logs"), os.path.join(t, "stop")
    write_log(os.path.join(logs, "p", "s.jsonl"), [(stamp(3), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"}))])
    s = subprocess.Popen([sys.executable, "-m", "dokima.agent", "steps", logs, stop], cwd=ROOT, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.2)
    open(stop, "w").write("stop")
    out, _ = ends(s, "187.5", 10, "its stop file appeared")
    assert STEP_LINE.search(out), f"187.5: setup: `agent steps` wrote no step line:\n{out[:600]}"
    assert "reading the issue" not in out and "[secret removed]" in out, \
        f"187.5: the step line written to the job's log is not passed through scrub():\n{out[:600]}"

    env = env_for(os.path.join(t, "follow"), SCRUB_PHRASE="reading the issue", DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    set_state(env, jobs=jobs("in_progress", iso(3)), log=job_log("reading the issue"))
    p = follow(env)
    time.sleep(1.2)
    set_state(env, jobs=jobs("completed", iso(3)), log=job_log("reading the issue"))
    ends(p, "187.5", 5, "the agent step completed")
    new = edits(env)
    assert new and all("reading the issue" not in v and "[secret removed]" in v for v in new), \
        f"187.5: a card the follower wrote to GitHub was not passed through scrub() first:\n{(new or [''])[-1][:600]}"


def test_the_follower_keeps_going_when_github_fails_and_never_fails(record_property, tmp_path):
    """A failed update never stops the follower or fails anything: it tries again next time and ends with 0.

    First every call to GitHub fails (HTTP 502): the follower must keep trying (at least three calls in 2 s at 0.3 s)
    and still be running. Then GitHub refuses only the edits: it must still be running. Then the agent ends and it
    must end with 0. In the workflow, the step that runs it, or its job, continues on error, so it never fails the run."""
    record_property("proves", "187.6")
    job = next((j for j in ts.workflow("agent.yml")["jobs"].values()
                if any("dokima.agent follow" in str(s.get("run", "")) for s in j.get("steps") or [])), None)
    assert job, "187.6: no job of agent.yml runs `agent follow`"
    start = next(s for s in job["steps"] if "dokima.agent follow" in str(s.get("run", "")))
    assert "true" in (str(start.get("continue-on-error", "")).lower(), str(job.get("continue-on-error", "")).lower()), \
        "187.6: a failure of `agent follow` could fail the run: neither its step nor its job continues on error"
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3")
    seed_cards(env)
    set_state(env, jobs=jobs("in_progress", iso(30)), log=job_log("writing code"), down=True)
    p = follow(env)
    time.sleep(2)
    calls = os.path.join(env["FAKE_GH_DIR"], "calls.jsonl")
    tried = sum(1 for _ in open(calls)) if os.path.exists(calls) else 0
    assert p.poll() is None, f"187.6: the follower stopped (exit {p.returncode}) when GitHub failed:\n{p.stderr.read()[-800:]}"
    assert tried >= 3, f"187.6: the follower called GitHub {tried} times in 2 s while it failed; it must keep trying"
    set_state(env, jobs=jobs("in_progress", iso(30)), log=job_log("writing code"), refuse_edits=True)
    time.sleep(1.2)
    assert p.poll() is None, f"187.6: the follower stopped (exit {p.returncode}) when GitHub refused an edit"
    set_state(env, jobs=jobs("completed", iso(30)), log=job_log("writing code"))
    ends(p, "187.6", 5, "the agent step completed")


class SlowRun:
    """One run of the agent's job with the slower fake Claude Code and step lines every half second."""

    def __init__(self, tmp):
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(ts, "FAKE_CLAUDE", SLOW_CLAUDE)
            base = ts.Machine.base_env
            mp.setattr(ts.Machine, "base_env", lambda self, e: {**base(self, e), "DOKIMA_PROGRESS_EVERY": str(EVERY)})
            self.run = Run(tmp, "reviewer", "plan", STORY_PLANNED, try_branch=True)
        gh = os.path.join(self.run.tmp, "gh")
        self.meta = [json.loads(l) for l in open(os.path.join(gh, "calls-meta.jsonl"))]
        p = os.path.join(gh, "calls-at-agent-end")
        self.end = int(open(p).read()) if os.path.exists(p) else None
        p = os.path.join(gh, "agent-env.json")
        self.agent_env = json.load(open(p)) if os.path.exists(p) else None
        self.agent_log = next((l for l in self.run.log if l.startswith(f"## run: {AGENT_STEP} (")), "")


@pytest.fixture(scope="module")
def slow(tmp_path_factory):
    """The agent's job run once with an agent that reads the issue, writes a test and checks its output."""
    return SlowRun(tmp_path_factory.mktemp("progress"))


def test_the_agents_job_writes_its_steps_to_its_log_holds_no_key_and_still_posts_its_result(record_property, slow):
    """In a real run of the agent's job, its log follows the agent step by step, no key is used, and the result lands.

    A plan review whose agent reads the issue, writes a test and checks its output, three seconds each, with step
    lines every half second. The agent step's log must show those three steps in order and end with exit 0; the
    agent's environment holds no bot key; no call to GitHub is made with the bot's key while the agent works; and the
    run posts exactly one passed record of the review."""
    record_property("proves", "187.6")
    s = slow
    assert s.run.agent_started() and s.end is not None, \
        f"187.6: the agent did not run to its end; the run stopped at '{s.run.failed_step}':\n{s.run.tail()}"
    assert s.agent_log.split("\n", 1)[0].endswith("(exit 0)"), f"187.6: the agent step did not end cleanly:\n{s.agent_log[-1500:]}"
    said = [x.strip() for x in STEP_LINE.findall(s.agent_log)]
    seen = [x for i, x in enumerate(said) if x != "starting" and (i == 0 or x != said[i - 1])]
    assert seen == ["reading the issue", "writing tests", "checking its output"], \
        f"187.6: the agent's job log did not follow its steps in order; it showed {said}"
    leaked = sorted(k for k, v in (s.agent_env or {}).items() if "fake-token" in v and k != "GIT_CONFIG_VALUE_0")
    assert s.agent_env is not None and not leaked, f"187.6: the agent's environment holds the bot's key in {leaked}"
    during = [m["args"] for i, m in enumerate(s.meta) if m["agent_started"] and i < s.end and m["token"] == "fake-token"]
    assert during == [], f"187.6: the bot's key was used on the agent's machine while the agent worked: {during[:3]}"
    recs = [r for c in s.run.comments() if c["author"] == agent.BOT
            for r in agent.records([{"author": {"login": agent.BOT}, "body": c["versions"][-1]}])]
    assert [(r["role"], r["check"]["passed"]) for r in recs] == [("reviewer", True)], \
        f"187.6: the result was not posted as exactly one passed record: {recs}\n{s.run.tail()}"


def test_the_followers_key_can_only_write_comments_and_read_the_run_and_is_revoked(record_property):
    """The key that updates the card can only write issue comments and read the run, and is revoked when the job ends.

    Reads the workflow: the step that runs `agent follow` takes its GitHub key from an app key step in its own job
    that asks for issues: write and actions: read and nothing else, and does not skip the revoke GitHub's key action
    does when the job ends."""
    record_property("proves", "187.7")
    jobs_ = ts.workflow("agent.yml")["jobs"]
    name = next((n for n, j in jobs_.items() if any("dokima.agent follow" in str(s.get("run", "")) for s in j.get("steps") or [])), None)
    assert name, "187.7: no job runs `agent follow`"
    job = jobs_[name]
    steps = job["steps"]
    start = next(s for s in steps if "dokima.agent follow" in str(s.get("run", "")))
    token = str((start.get("env") or {}).get("GH_TOKEN", ""))
    m = re.fullmatch(r"\$\{\{\s*steps\.([\w-]+)\.outputs\.token\s*\}\}", token.strip())
    assert m, f"187.7: the step that runs `agent follow` does not take its key from an app key step: GH_TOKEN={token!r}"
    key = next((s for s in steps if s.get("id") == m.group(1)), None)
    assert key is not None and "create-github-app-token" in str(key.get("uses")), f"187.7: no app key step {m.group(1)!r} in the job"
    w = key.get("with") or {}
    perms = {k: v for k, v in w.items() if k.startswith("permission-")}
    assert perms == {"permission-issues": "write", "permission-actions": "read"}, \
        f"187.7: the update key asks for {perms or 'every permission the app has'}, expected only issues: write and actions: read"
    assert str(w.get("skip-token-revoke", "false")).lower() != "true", "187.7: the update key is not revoked when its job ends"
