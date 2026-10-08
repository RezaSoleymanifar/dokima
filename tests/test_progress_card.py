"""While an agent works, its live card shows how many minutes it has worked and the step it is on (#187).

Two kinds of test. The first run Dokima's own commands the way the workflow runs them: `agent progress ROLE STAGE
STARTED LOG_DIR` prints the card for a session log, and `agent watch CARD_ID ROLE STAGE STARTED LOG_DIR STOP_FILE`
edits the run's card in place every DOKIMA_PROGRESS_EVERY seconds (60 when unset) until STOP_FILE exists. STARTED is
when the agent started, in seconds since 1970; PACK and OUT name the agent's pack and hand-back folders; every SCRUB_*
value is a secret. GitHub is the fake `gh` from test_start.py.

The second run the whole agent workflow (.github/workflows/agent.yml) on the fake machine from test_start.py, with a
slower fake Claude Code that works through three steps, a few seconds each, writing its session log as it goes, and
with DOKIMA_PROGRESS_EVERY set to half a second so the card is updated several times while it works.
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
from test_start import N, STORY_PLANNED, Run

from dokima import agent

ROOT = ts.ROOT
EVERY = 0.5
PHASE = 3
STEP = re.compile(r"working for (\d+) min · ([^\n<*]+)")
STEPS = ["starting", "reading the issue", "reading the code", "writing tests", "writing code", "writing its hand-back",
         "running tests", "checking its output", "running a command", "working with sub-agents", "working"]
ICON = re.compile(r'/dokima/icons/([A-Za-z0-9_-]+)\.svg')

SLOW_CLAUDE = r'''#!/usr/bin/env python3
"""A slower stand-in for Claude Code: reads the issue, writes a test, checks its output, a few seconds each.

Like the fake in test_start.py it keeps what GitHub showed when it started and its own environment, then writes its
session log one tool call at a time, each with the time it was made, and hands back the review the test chose. When
it ends it notes how many calls GitHub had seen by then (calls-at-agent-end), so a test can tell which calls the run
made while the agent worked."""
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


# ---------- helpers ----------

def env_for(tmp, **extra):
    """An environment for Dokima's commands: its code from this repo, a fake gh on PATH, the pack and hand-back folders."""
    bin_dir, gh_dir = os.path.join(tmp, "bin"), os.path.join(tmp, "gh")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(gh_dir, exist_ok=True)
    open(os.path.join(bin_dir, "gh"), "w").write(ts.FAKE_GH.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
    os.chmod(os.path.join(bin_dir, "gh"), 0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("SCRUB_", "DOKIMA_PROGRESS"))}
    env.update({"PATH": bin_dir + os.pathsep + os.environ["PATH"], "PYTHONPATH": ROOT, "FAKE_GH_DIR": gh_dir,
                "GH_TOKEN": "fake-token", "GITHUB_REPOSITORY": "o/r", "GITHUB_RUN_ID": "42",
                "GITHUB_SERVER_URL": "https://github.com",
                # Outside pytest's own temp folder, whose name holds the word pytest, as the real /tmp/pack does not.
                "PACK": tempfile.mkdtemp(prefix="pack-"), "OUT": tempfile.mkdtemp(prefix="dokima-out-")})
    env.update(extra)
    return env


def progress(env, started, log_dir, role="planner", stage=""):
    """The card `agent progress` prints; fails the test when the command is missing or fails."""
    p = subprocess.run([sys.executable, "-m", "dokima.agent", "progress", role, stage, str(int(started)), log_dir],
                       cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    return p


def write_log(path, entries):
    """A session log at path: one JSON line per entry, each (timestamp, message)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        for t, m in entries:
            f.write(json.dumps({"timestamp": t, "message": m}) + "\n")


def tool_call(name, i):
    """An assistant message that makes one tool call."""
    return {"role": "assistant", "model": "claude-opus-5-5", "content": [{"type": "tool_use", "id": "x", "name": name, "input": i}]}


def stamp(seconds_ago=0):
    """A session-log timestamp seconds_ago in the past."""
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() - seconds_ago))


def step_of(card, crit):
    """The minutes and step a card shows, as (minutes, step); fails the test, naming crit, when it shows neither."""
    m = STEP.search(card or "")
    assert m, f"{crit}: the card does not say 'working for N min · <step>':\n{(card or '')[:800]}"
    return int(m.group(1)), m.group(2).strip().rstrip(".").strip()


def seed_card(env, body="<!-- dokima-live -->\nworking\n"):
    """A fake GitHub holding the run's card on issue #57, as comment 5001."""
    json.dump([{"id": 5001, "kind": "issue", "number": int(N), "created": "2026-10-08T00:00:00Z",
                "versions": [body], "author": "dokima-runtime"}], open(os.path.join(env["FAKE_GH_DIR"], "comments.json"), "w"))


def versions(env):
    """Every version of the card, oldest first, and whether any other comment was written."""
    cs = json.load(open(os.path.join(env["FAKE_GH_DIR"], "comments.json")))
    return [c for c in cs if c["id"] == 5001][0]["versions"], len(cs)


def watch(env, log_dir, stop, started=None):
    """Start `agent watch` for card 5001 in the background."""
    return subprocess.Popen([sys.executable, "-m", "dokima.agent", "watch", "5001", "planner", "", str(int(started or time.time())),
                             log_dir, stop], cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def stop_watch(p, stop, crit):
    """Create the stop file and wait for the watch to end; fails the test, naming crit, when it does not end with 0."""
    open(stop, "w").write("stop")
    try:
        out, err = p.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        p.kill()
        pytest.fail(f"{crit}: `agent watch` was still running 10 s after its stop file appeared")
    assert p.returncode == 0, f"{crit}: `agent watch` ended with exit code {p.returncode}:\n{out[-800:]}{err[-800:]}"


# ---------- the commands ----------

def test_the_card_counts_whole_minutes_since_the_agent_started(record_property, tmp_path):
    """The card says 'working for N min', N being the whole minutes since the agent started.

    Prints the card for agents that started 0 s, 59 s, 61 s, 12 min 34 s and 62 min 5 s ago: it must say 0, 0, 1, 12
    and 62 minutes. A card that counts from anything else, rounds up or shows a fixed number fails."""
    record_property("proves", "187.1")
    env = env_for(str(tmp_path))
    logs = str(tmp_path / "logs")
    os.makedirs(logs)
    for ago, want in ((0, 0), (59, 0), (61, 1), (754, 12), (3725, 62)):
        p = progress(env, time.time() - ago, logs)
        assert p.returncode == 0 and p.stdout.strip(), \
            f"187.1: `agent progress` printed no card for an agent that started {ago} s ago (exit {p.returncode}):\n{p.stdout[-400:]}{p.stderr[-800:]}"
        got, _ = step_of(p.stdout, "187.1")
        assert got == want, f"187.1: an agent that started {ago} s ago shows 'working for {got} min', expected {want} min"


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


def test_the_card_names_the_step_of_the_newest_tool_call(record_property, tmp_path):
    """The card names the agent's step, mapped by code from the newest tool call in its session log.

    For each kind of tool call (reading the pack, reading code, writing tests, code or the hand-back, running tests,
    the hand-back check, any other command, sub-agents, any other tool) a log whose newest call is that one must give
    exactly its step. Before any tool call the card says starting. With several calls the newest wins, by its time,
    even when it sits in another log file; later text and tool results do not change it; a half-written last line is
    skipped."""
    record_property("proves", "187.2")
    t = str(tmp_path)
    env = env_for(t)
    fill = lambda v: {k: x.replace("{PACK}", env["PACK"]).replace("{OUT}", env["OUT"]) if isinstance(x, str) else x
                      for k, x in v.items()}
    for i, (name, inp, want) in enumerate(CASES):
        logs = os.path.join(t, f"case{i}")
        write_log(os.path.join(logs, "p", "s.jsonl"), [(stamp(30), tool_call("Read", {"file_path": "/x/y.py"})),
                                                      (stamp(5), tool_call(name, fill(inp)))])
        p = progress(env, time.time(), logs)
        assert p.returncode == 0, f"187.2: `agent progress` failed (exit {p.returncode}):\n{p.stderr[-800:]}"
        _, got = step_of(p.stdout, "187.2")
        assert got == want, f"187.2: the newest call {name} {fill(inp)} shows the step {got!r}, expected {want!r}"

    empty = os.path.join(t, "empty")
    os.makedirs(empty)
    _, got = step_of(progress(env, time.time(), empty).stdout, "187.2")
    assert got == "starting", f"187.2: before any tool call the card shows {got!r}, expected 'starting'"
    _, got = step_of(progress(env, time.time(), os.path.join(t, "not-there-yet")).stdout, "187.2")
    assert got == "starting", f"187.2: with no session log yet the card shows {got!r}, expected 'starting'"

    logs = os.path.join(t, "two-files")
    write_log(os.path.join(logs, "a", "a.jsonl"), [(stamp(2), tool_call("Bash", {"command": "python3 -m pytest -q"}))])
    write_log(os.path.join(logs, "b", "b.jsonl"), [(stamp(40), tool_call("Write", {"file_path": "/r/tests/test_q.py", "content": ""}))])
    _, got = step_of(progress(env, time.time(), logs).stdout, "187.2")
    assert got == "running tests", f"187.2: the newest call (in a.jsonl, 2 s ago) lost to an older one in b.jsonl: shows {got!r}"

    logs = os.path.join(t, "later-text")
    write_log(os.path.join(logs, "p", "s.jsonl"), [
        (stamp(20), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"})),
        (stamp(15), {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "x", "content": "the issue"}]}),
        (stamp(10), {"role": "assistant", "content": [{"type": "text", "text": "Now I will think."}]})])
    open(os.path.join(logs, "p", "s.jsonl"), "a").write('{"timestamp": "' + stamp(1) + '", "message": {"role": "assist')
    p = progress(env, time.time(), logs)
    assert p.returncode == 0, f"187.2: a half-written last line broke `agent progress`:\n{p.stderr[-800:]}"
    _, got = step_of(p.stdout, "187.2")
    assert got == "reading the issue", \
        f"187.2: text, tool results or a half-written line after the newest tool call changed the step to {got!r}"


def test_the_watch_edits_the_same_card_as_the_agent_goes_until_told_to_stop(record_property, tmp_path):
    """While the agent works, the run's card is edited in place again and again, following the agent's step.

    Runs `agent watch` every 0.3 s on a card on a fake GitHub while a session log moves from reading the issue to
    writing tests. The one card (no new comment) must get at least three new versions, showing reading the issue and
    then writing tests, each still a live card that never reads as a record and showing the running icon. Once the
    stop file appears the watch ends with 0 and edits nothing more. With no interval set it waits about a minute: no
    edit in its first 3 s."""
    record_property("proves", "187.3")
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3")
    seed_card(env)
    logs, stop = os.path.join(t, "logs"), os.path.join(t, "stop")
    log = os.path.join(logs, "p", "s.jsonl")
    write_log(log, [(stamp(1), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"}))])
    p = watch(env, logs, stop)
    time.sleep(1.5)
    write_log(log, [(stamp(0), tool_call("Write", {"file_path": "/r/tests/test_q.py", "content": ""}))])
    time.sleep(1.5)
    stop_watch(p, stop, "187.3")
    vs, count = versions(env)
    assert count == 1, f"187.3: the watch wrote {count - 1} new comments instead of editing the card in place"
    new = vs[1:]
    assert len(new) >= 3, f"187.3: the card was edited {len(new)} times in 3 s at an interval of 0.3 s, expected at least 3"
    steps = [step_of(v, "187.3")[1] for v in new]
    seen = [s for i, s in enumerate(steps) if s != "starting" and (i == 0 or s != steps[i - 1])]
    assert seen == ["reading the issue", "writing tests"], f"187.3: the card did not follow the agent's steps; it showed {steps}"
    for v in new:
        assert v.startswith(agent.LIVE) and agent.records([{"author": {"login": agent.BOT}, "body": v}]) == [] \
            and not agent.is_record({"author": {"login": agent.BOT}, "body": v}), f"187.3: an update reads as a record:\n{v[:600]}"
        assert "running" in ICON.findall(v), f"187.3: an update does not show the running icon:\n{v[:600]}"
    time.sleep(1)
    assert len(versions(env)[0]) == len(vs), "187.3: the watch edited the card after its stop file appeared"

    env = env_for(os.path.join(t, "default"))
    seed_card(env)
    stop = os.path.join(t, "stop2")
    p = watch(env, logs, stop)
    time.sleep(3)
    vs, _ = versions(env)
    stop_watch(p, stop, "187.3")
    assert len(vs) == 1, f"187.3: with no interval set the card was edited {len(vs) - 1} times in 3 s, not about once a minute"


def test_nothing_the_progress_shows_escapes_scrub(record_property, tmp_path):
    """No secret in the session log reaches the card: the whole card passes through scrub() before it is shown.

    A secret in the newest tool call's command and file path never appears on the printed card or on any version the
    watch writes to GitHub. To prove the whole card is scrubbed, not just the log, a secret equal to the text
    'reading the issue' must be replaced by '[secret removed]' on the card, both printed and as written by the watch."""
    record_property("proves", "187.4")
    t = str(tmp_path)
    secret = "ghs_S3cretToken0123456789abcdef"
    env = env_for(t, SCRUB_GITHUB=secret, SCRUB_CLAUDE="sk-ant-oat01-another-secret-value", DOKIMA_PROGRESS_EVERY="0.3")
    logs = os.path.join(t, "logs")
    write_log(os.path.join(logs, "p", "s.jsonl"), [
        (stamp(9), tool_call("Read", {"file_path": f"/r/{secret}/agent.py"})),
        (stamp(3), tool_call("Bash", {"command": f"GH_TOKEN={secret} python3 -m dokima.agent check review {env['OUT']}/review.json x 1"}))])
    p = progress(env, time.time(), logs)
    assert p.returncode == 0, f"187.4: `agent progress` failed (exit {p.returncode}):\n{p.stderr[-800:]}"
    assert step_of(p.stdout, "187.4")[1] == "checking its output", f"187.4: setup: wrong step shown:\n{p.stdout[:600]}"
    assert secret not in p.stdout, f"187.4: a secret from the session log is on the card:\n{p.stdout[:800]}"
    seed_card(env)
    stop = os.path.join(t, "stop")
    w = watch(env, logs, stop)
    time.sleep(1.2)
    stop_watch(w, stop, "187.4")
    vs, _ = versions(env)
    assert len(vs) >= 2, "187.4: setup: the watch never wrote the card"
    assert not any(secret in v for v in vs), "187.4: a secret from the session log was written to the card on GitHub"

    env = env_for(os.path.join(t, "phrase"), SCRUB_PHRASE="reading the issue", DOKIMA_PROGRESS_EVERY="0.3")
    logs = os.path.join(t, "logs2")
    write_log(os.path.join(logs, "p", "s.jsonl"), [(stamp(3), tool_call("Read", {"file_path": env["PACK"] + "/issue.md"}))])
    p = progress(env, time.time(), logs)
    assert p.returncode == 0 and STEP.search(p.stdout), \
        f"187.4: setup: `agent progress` printed no card:\n{p.stdout[:600]}{p.stderr[-600:]}"
    assert "reading the issue" not in p.stdout and "[secret removed]" in p.stdout, \
        f"187.4: the printed card is not passed through scrub(): a secret equal to its step text still shows:\n{p.stdout[:800]}"
    seed_card(env)
    stop = os.path.join(t, "stop2")
    w = watch(env, logs, stop)
    time.sleep(1.2)
    stop_watch(w, stop, "187.4")
    new = versions(env)[0][1:]
    assert new and all("reading the issue" not in v and "[secret removed]" in v for v in new), \
        "187.4: a card the watch wrote to GitHub was not passed through scrub() first"


def test_the_watch_keeps_going_when_github_refuses_an_update(record_property, tmp_path):
    """A failed update never stops the watch or fails anything: it tries again next time and ends cleanly when told.

    Every call to GitHub fails the way GitHub fails (HTTP 502), and the session log does not exist yet. The watch must
    keep trying (at least three attempts in 2 s at an interval of 0.3 s), still be running after 2 s, and end with 0
    once its stop file appears."""
    record_property("proves", "187.5")
    t = str(tmp_path)
    env = env_for(t, DOKIMA_PROGRESS_EVERY="0.3", FAKE_GH_FAIL="api|HTTP 502: Server Error")
    seed_card(env)
    stop = os.path.join(t, "stop")
    p = watch(env, os.path.join(t, "no-logs-yet"), stop)
    time.sleep(2)
    alive = p.poll() is None
    calls = os.path.join(env["FAKE_GH_DIR"], "calls.jsonl")
    tried = sum(1 for _ in open(calls)) if os.path.exists(calls) else 0
    stop_watch(p, stop, "187.5") if alive else None
    assert alive, f"187.5: the watch stopped (exit {p.returncode}) when GitHub refused its updates:\n{p.stderr.read()[-800:] if p.stderr else ''}"
    assert tried >= 3, f"187.5: the watch tried to update the card {tried} times in 2 s; after a refusal it must keep trying"


# ---------- the whole workflow ----------

class SlowRun:
    """One run of the agent workflow with the slower fake Claude Code and updates every half second."""

    def __init__(self, tmp, options=None):
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(ts, "FAKE_CLAUDE", SLOW_CLAUDE)
            base = ts.Machine.base_env
            mp.setattr(ts.Machine, "base_env", lambda self, e: {**base(self, e), "DOKIMA_PROGRESS_EVERY": str(EVERY)})
            self.t0 = time.time()
            self.run = Run(tmp, "reviewer", "plan", STORY_PLANNED, try_branch=True, options=options)
            self.took = time.time() - self.t0
        gh = os.path.join(self.run.tmp, "gh")
        self.comments = self.run.comments()
        time.sleep(4 * EVERY)
        self.comments_later = self.run.comments()
        self.meta = [json.loads(l) for l in open(os.path.join(gh, "calls-meta.jsonl"))]
        p = os.path.join(gh, "calls-at-agent-end")
        self.end = int(open(p).read()) if os.path.exists(p) else None
        p = os.path.join(gh, "agent-env.json")
        self.agent_env = json.load(open(p)) if os.path.exists(p) else None

    def during(self):
        """The calls the run made to GitHub while the agent worked, as indexes into meta."""
        return [i for i, m in enumerate(self.meta) if m["agent_started"] and i < (self.end or 0)]


@pytest.fixture(scope="module")
def slow(tmp_path_factory):
    """The two workflow runs these tests read: one where GitHub takes every edit, one where it refuses every edit."""
    t = tmp_path_factory.mktemp("progress")
    return {"ok": SlowRun(t / "ok"), "no-edit": SlowRun(t / "no-edit", {"fail_edits": True})}


def is_edit(args):
    """True when a gh call edits a comment."""
    method = next((args[i + 1] for i, x in enumerate(args[:-1]) if x in ("-X", "--method")), "").upper()
    return args[:1] == ["api"] and method in ("PATCH", "POST") and any(re.fullmatch(r"/?repos/o/r/issues/comments/\d+", x) for x in args)


def is_revoke(args):
    """True when a gh call revokes the key it was made with."""
    method = next((args[i + 1] for i, x in enumerate(args[:-1]) if x in ("-X", "--method")), "").upper()
    return args[:1] == ["api"] and method == "DELETE" and any(re.fullmatch(r"/?installation/token", x) for x in args)


def test_the_workflow_updates_the_card_while_the_agent_works_and_never_after_its_result(record_property, slow):
    """In a real run of the workflow, the card follows the agent step by step, then becomes the result and stays so.

    A plan review whose agent reads the issue, writes a test and checks its output, three seconds each, with updates
    every half second. The run must leave exactly one comment, its card. Its versions while the agent worked must show
    'working for 0 min' and the steps reading the issue, writing tests and checking its output, in that order. No such
    version may come after the record, the last version is the run's passed record, and two seconds after the run
    ended nothing has edited it."""
    record_property("proves", "187.3")
    s = slow["ok"]
    assert s.run.agent_started() and s.end is not None, \
        f"187.3: setup: the agent did not run to its end; the run stopped at '{s.run.failed_step}':\n{s.run.tail()}"
    assert s.took < 60, f"187.3: setup: the run took {s.took:.0f} s, too long to expect 0 minutes on the card"
    assert len(s.comments) == 1, f"187.3: the run left {len(s.comments)} comments, expected its one card"
    vs = s.comments[0]["versions"]
    progress_at = [i for i, v in enumerate(vs) if STEP.search(v)]
    assert len(progress_at) >= 3, \
        f"187.3: the card was updated {len(progress_at)} times while the agent worked for 9 s with updates every 0.5 s:\n{s.run.tail()}"
    steps = [step_of(vs[i], "187.3") for i in progress_at]
    assert all(m == 0 for m, _ in steps), f"187.3: a 9-second run showed minutes {[m for m, _ in steps]}, expected 0"
    names = [x for _, x in steps]
    seen = [x for i, x in enumerate(names) if x != "starting" and (i == 0 or x != names[i - 1])]
    assert seen == ["reading the issue", "writing tests", "checking its output"], \
        f"187.3: the card did not follow the agent's steps in order; it showed {names}"
    first_record = next((i for i, v in enumerate(vs) if agent.records([{"author": {"login": agent.BOT}, "body": v}])), None)
    assert first_record is not None and first_record == len(vs) - 1 and max(progress_at) < first_record, \
        f"187.3: an update came after the run's result, or the result is not the card's last version (record at {first_record}, updates at {progress_at})"
    recs = agent.records([{"author": {"login": agent.BOT}, "body": vs[-1]}])
    assert [(r["role"], r["check"]["passed"]) for r in recs] == [("reviewer", True)], f"187.3: the card did not end as the run's passed record: {recs}"
    assert s.comments_later == s.comments, "187.3: the card was edited after the run ended, overwriting its result"


def test_the_workflow_still_posts_the_result_when_every_update_fails(record_property, slow):
    """When GitHub refuses every update of the card, the agent still works to its end and its result still lands.

    The same slow plan review, with GitHub refusing every edit of a comment. The run must have tried to update the
    card at least twice while the agent worked, the agent must have run to its end, and Dokima's bot must have posted
    exactly one record: the review's passed record."""
    record_property("proves", "187.5")
    s = slow["no-edit"]
    assert s.run.agent_started() and s.end is not None, \
        f"187.5: the agent did not run to its end when updates failed; the run stopped at '{s.run.failed_step}':\n{s.run.tail()}"
    tried = [i for i in s.during() if is_edit(s.meta[i]["args"])]
    assert len(tried) >= 2, f"187.5: the run tried to update the card {len(tried)} times while the agent worked, expected at least 2"
    recs = [r for c in s.comments if c["author"] == agent.BOT
            for r in agent.records([{"author": {"login": agent.BOT}, "body": c["versions"][-1]}])]
    assert [(r["role"], r["check"]["passed"]) for r in recs] == [("reviewer", True)], \
        f"187.5: the result was not posted as exactly one passed record when updates failed: {recs}\n{s.run.tail()}"


def test_the_updates_key_can_only_write_comments_is_not_the_agents_and_dies_with_the_agent(record_property, slow):
    """The key that updates the card can only write issue comments, never reaches the agent, and is revoked when it ends.

    Reads the workflow: the step that starts `agent watch` takes its GitHub key from an app key step that asks for
    issues: write and no other permission. Runs the slow plan review: the agent's own environment holds no bot key,
    and after the agent ended the key is revoked (DELETE installation/token) after the last update and before the run's
    result is written, which is the only edit after it."""
    record_property("proves", "187.6")
    job = ts.workflow("agent.yml")["jobs"]["run"]
    steps = job["steps"]
    starts = [st for st in steps if "dokima.agent watch" in str(st.get("run", ""))]
    assert len(starts) == 1, f"187.6: expected one workflow step that starts `agent watch`, found {len(starts)}"
    token = str((starts[0].get("env") or {}).get("GH_TOKEN", ""))
    m = re.fullmatch(r"\$\{\{\s*steps\.([\w-]+)\.outputs\.token\s*\}\}", token.strip())
    assert m, f"187.6: the step that starts the watch does not take its key from an app key step: GH_TOKEN={token!r}"
    key = next((st for st in steps if st.get("id") == m.group(1)), None)
    assert key is not None and "create-github-app-token" in str(key.get("uses")), f"187.6: no app key step {m.group(1)!r}"
    perms = {k: v for k, v in (key.get("with") or {}).items() if k.startswith("permission-")}
    assert perms == {"permission-issues": "write"}, f"187.6: the update key asks for {perms or 'every permission the app has'}, expected only issues: write"

    s = slow["ok"]
    leaked = sorted(k for k, v in (s.agent_env or {}).items() if "fake-token" in v and k != "GIT_CONFIG_VALUE_0")
    assert s.agent_env is not None and not leaked, f"187.6: the agent's environment holds the bot's key in {leaked}"
    after = [i for i, m in enumerate(s.meta) if m["agent_started"] and s.end is not None and i >= s.end]
    revokes = [i for i in after if is_revoke(s.meta[i]["args"])]
    assert revokes, "187.6: the update key was never revoked after the agent ended"
    edits_during = [i for i in s.during() if is_edit(s.meta[i]["args"])]
    assert edits_during, "187.6: setup: the card was never updated while the agent worked"
    edits_after = [i for i in after if is_edit(s.meta[i]["args"]) and i > revokes[0]]
    assert len(edits_after) == 1 and edits_after[-1] == max(i for i, m in enumerate(s.meta) if is_edit(m["args"])), \
        f"187.6: after the update key was revoked there were {len(edits_after)} edits; expected only the run's result"
