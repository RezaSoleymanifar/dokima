"""A run that starts an agent either starts it or says why on the issue, and a split gets its plan review (#176).

These tests run the agent workflow's own steps, read from .github/workflows/agent.yml, the way GitHub runs them: each
step's `if:` is evaluated, its `${{ }}` expressions filled in, and its script run with bash in a clone of a temp git
repo whose origin is a local bare repo. Nothing leaves the machine: a fake `gh` answers from a fake issue and records
every comment, dispatch and issue it is asked to create; a fake `claude` hands back a review; `pip` and `npm` do
nothing; pushes to github.com are redirected to the local origin. Steps that only `uses:` an action are skipped (the
app token step gives a fake token). Paths under /tmp and /home/runner are moved into the test's temp folder. Values a
step writes to GITHUB_ENV or GITHUB_OUTPUT are read as single KEY=value lines.

The fake issue is #57 in repo o/r, owned by `owner-person` through CODEOWNERS; Dokima's code is copied from this repo.
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OWNER = "owner-person"
N = "57"
SPLIT = {"kind": "feature", "feature": "Stuck issues get unstuck.", "stories": [
    {"title": "First", "user_story": "u1", "acceptance_criteria": [{"text": "a", "source": "https://github.com/o/r/issues/57"}],
     "non_functional": [], "depends_on": []},
    {"title": "Second", "user_story": "u2", "acceptance_criteria": [{"text": "b", "source": "https://github.com/o/r/issues/57"}],
     "non_functional": [], "depends_on": [0]}]}
STORY = {"kind": "user_story", "user_story": "u", "acceptance_criteria": [{"text": "a", "source": "https://github.com/o/r/issues/57"}],
         "non_functional": [], "scope": ["x.py"], "out_of_scope": [], "tests": {"57.1": ["tests/test_x.py::test_a"]}}
APPROVE = {"previous_step": {"did": ["Proposed a split into two stories."], "decided": [], "open": []},
           "stage": "plan", "round": 1, "verdict": "approve", "summary": "The split keeps every promise once.",
           "blockers": [], "notes": [], "outside_plan": [], "resolved": []}

FAKE_GH = r'''#!/usr/bin/env python3
"""A stand-in for the GitHub CLI: answers from the fake issue and records every call."""
import json, os, shutil, sys
d = os.environ["FAKE_GH_DIR"]
a = sys.argv[1:]
open(os.path.join(d, "calls.jsonl"), "a").write(json.dumps(a) + "\n")
def flag(name):
    return a[a.index(name) + 1] if name in a else None
if a[:2] == ["issue", "view"]:
    issue = json.load(open(os.path.join(d, "issue.json")))
    print(issue["title"] if flag("-q") == ".title" else json.dumps(issue))
elif a[:2] in (["issue", "comment"], ["pr", "comment"]):
    body = open(flag("--body-file")).read() if flag("--body-file") else flag("--body")
    open(os.path.join(d, "posted.jsonl"), "a").write(json.dumps({"where": a[:3], "body": body}) + "\n")
elif a[:2] == ["issue", "create"]:
    print("https://github.com/o/r/issues/900")
elif a[:2] == ["pr", "list"]:
    print("" if (flag("-q") or flag("--jq")) else "[]")
elif a[:1] == ["api"] and any(x.startswith("users/") for x in a):
    print("1")
elif a[:1] == ["api"] and "--paginate" in a:
    print("[]")
elif a[:1] == ["api"]:
    print("{}")
'''

FAKE_CLAUDE = r'''#!/usr/bin/env python3
"""A stand-in for Claude Code: hands back the review the test chose and leaves a session log naming its model."""
import json, os, shutil
open(os.environ["FAKE_CLAUDE_MARK"], "w").write("started")
shutil.copy(os.environ["FAKE_REVIEW"], os.path.join(os.environ["OUT"], "review.json"))
logs = os.path.join(os.environ["HOME"], ".claude", "projects", "p")
os.makedirs(logs, exist_ok=True)
open(os.path.join(logs, "s.jsonl"), "w").write(json.dumps({"message": {"model": os.environ["MODEL"], "role": "assistant", "content": "Done."}}) + "\n")
print(json.dumps({"num_turns": 1, "duration_ms": 1000, "usage": {}}))
'''


class Nil:
    """A missing value in a GitHub expression: falsy, equal to '' and null, printed as ''."""
    def __getattr__(self, k):
        return NIL

    def __bool__(self):
        return False

    def __eq__(self, o):
        return o in ("", None) or isinstance(o, Nil)

    __hash__ = None

    def __str__(self):
        return ""


NIL = Nil()


class Ctx(dict):
    """A GitHub expression context: dotted access, a missing key is Nil."""
    def __getattr__(self, k):
        v = self.get(k, NIL)
        return Ctx(v) if isinstance(v, dict) and not isinstance(v, Ctx) else v


def evaluate(expr, ctx, status):
    """Evaluate one GitHub expression against the contexts and the job's status so far."""
    parts = re.split(r"('[^']*')", expr)
    for i in range(0, len(parts), 2):
        p = parts[i].replace("&&", " and ").replace("||", " or ").replace("!=", "\0")
        p = re.sub(r"!", " not ", p).replace("\0", "!=")
        p = re.sub(r"\.([A-Za-z_]\w*(?:-\w+)+)", lambda m: f"[{m.group(1)!r}]", p)
        p = re.sub(r"\bnull\b", "NIL", re.sub(r"\btrue\b", "True", re.sub(r"\bfalse\b", "False", p)))
        parts[i] = p
    names = {**ctx, "NIL": NIL, "always": lambda: True, "success": lambda: not status["failed"],
             "failure": lambda: status["failed"], "cancelled": lambda: False,
             "startsWith": lambda s, p: str(s).lower().startswith(str(p).lower()),
             "contains": lambda s, p: str(p).lower() in str(s).lower(),
             "format": lambda f, *xs: re.sub(r"\{(\d+)\}", lambda m: str(xs[int(m.group(1))]), f)}
    return eval("".join(parts), {"__builtins__": {}}, names)


def fill(text, ctx, status):
    """Fill every ${{ }} in a string."""
    def one(m):
        v = evaluate(m.group(1), ctx, status)
        return "" if v is None or isinstance(v, Nil) else ("true" if v is True else "false" if v is False else str(v))
    return re.sub(r"\$\{\{(.*?)\}\}", one, text)


def unquote(v):
    """A YAML scalar as written, without its quotes."""
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'" else v


def parse(text):
    """The run job's env and its steps, read without a YAML library: [{name, id, if, uses, env, run}]."""
    lines = text.split("\n  run:\n", 1)[1].split("\n")
    job_env, steps, i = {}, [], 0
    while i < len(lines):
        line = lines[i]
        if line == "    env:":
            i += 1
            while lines[i].startswith("      ") and not lines[i].startswith("       "):
                if not lines[i].strip().startswith("#"):
                    k, v = lines[i].strip().split(":", 1)
                    job_env[k] = unquote(v)
                i += 1
            continue
        if line.startswith("      - "):
            step, i = {"env": {}}, i
            lines[i] = "        " + line[8:]
            while i < len(lines) and (lines[i].startswith("        ") or not lines[i].strip()):
                l = lines[i]
                if l.startswith("        ") and not l.startswith("         ") and not l.strip().startswith("#"):
                    k, v = l.strip().split(":", 1)
                    v = v.strip()
                    if k == "run" and v == "|":
                        body, i = [], i + 1
                        while i < len(lines) and (lines[i].startswith("          ") or not lines[i].strip()):
                            body.append(lines[i][10:])
                            i += 1
                        step["run"] = "\n".join(body).rstrip() + "\n"
                        continue
                    if k in ("env", "with"):
                        i += 1
                        while i < len(lines) and lines[i].startswith("          "):
                            if k == "env" and not lines[i].startswith("           "):
                                ek, ev = lines[i].strip().split(":", 1)
                                step["env"][ek] = unquote(ev)
                            i += 1
                        continue
                    step[k] = unquote(v)
                i += 1
            steps.append(step)
            continue
        i += 1
    return job_env, steps


def sh(cwd, *args):
    """Run git or another command quietly; fail loudly with its output."""
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=git_env(os.environ))
    assert p.returncode == 0, f"test setup failed: {' '.join(args)}\n{p.stdout}{p.stderr}"
    return p.stdout.strip()


def git_env(base):
    """An environment where git has an identity."""
    return {**base, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}


def record_comment(rec, t):
    """A comment the bot posted carrying a record, as GitHub returns it."""
    return {"author": {"login": agent.BOT}, "body": agent.render(rec), "createdAt": t}


def owner_comment(body, t):
    """A comment the owner wrote."""
    return {"author": {"login": OWNER}, "body": body, "createdAt": t}


def planner_record(handback):
    """A passed planner record, the way the workflow writes one."""
    return {"role": "planner", "stage": None, "run_id": "1", "run": "https://github.com/o/r/actions/runs/1",
            "models": ["claude-opus-5-5"], "handback": handback, "check": {"passed": True, "problems": []}}


def review_record(handback):
    """A passed plan review record, the way the workflow writes one."""
    return {"role": "reviewer", "stage": "plan", "run_id": "2", "run": "https://github.com/o/r/actions/runs/2",
            "models": ["claude-opus-5-5"], "handback": handback, "check": {"passed": True, "problems": []}}


class Run:
    """One run of the agent workflow's job, on a temp repo with fake GitHub, Claude, pip and npm."""

    def __init__(self, tmp, role, stage, comments, try_branch=False, actor=OWNER):
        self.tmp = str(tmp)
        t = self.tmp
        os.makedirs(f"{t}/bin")
        os.makedirs(f"{t}/gh")
        os.makedirs(f"{t}/home")
        os.makedirs(f"{t}/runner-temp")
        for name, body in (("gh", FAKE_GH), ("claude", FAKE_CLAUDE), ("pip", "#!/bin/sh\nexit 0\n"), ("npm", "#!/bin/sh\nexit 0\n")):
            open(f"{t}/bin/{name}", "w").write(body.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
            os.chmod(f"{t}/bin/{name}", 0o755)
        json.dump({"number": int(N), "title": "Stuck issue", "body": "Fix it.", "comments": comments}, open(f"{t}/gh/issue.json", "w"))
        json.dump(APPROVE, open(f"{t}/review.json", "w"))
        # The repo: Dokima's code from this checkout, owned by owner-person, pushed to a local origin.
        src = f"{t}/src"
        shutil.copytree(os.path.join(ROOT, "dokima"), f"{src}/dokima", ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(f"{src}/.github")
        open(f"{src}/.github/CODEOWNERS", "w").write(f"* @{OWNER}\n")
        sh(t, "git", "init", "-q", "--bare", "-b", "main", f"{t}/origin.git")
        sh(src, "git", "init", "-q", "-b", "main")
        sh(src, "git", "add", "-A")
        sh(src, "git", "commit", "-qm", "main")
        sh(src, "git", "remote", "add", "origin", f"{t}/origin.git")
        sh(src, "git", "push", "-q", "origin", "main")
        self.main_sha = sh(src, "git", "rev-parse", "HEAD")
        self.try_sha = None
        if try_branch:
            sh(src, "git", "checkout", "-q", "-b", f"try/issue-{N}")
            os.makedirs(f"{src}/tests")
            open(f"{src}/tests/test_x.py", "w").write('def test_a():\n    """A."""\n')
            sh(src, "git", "add", "-A")
            sh(src, "git", "commit", "-qm", "tests")
            sh(src, "git", "push", "-q", "origin", f"try/issue-{N}")
            self.try_sha = sh(src, "git", "rev-parse", "HEAD")
        sh(t, "git", "clone", "-q", f"{t}/origin.git", f"{t}/ws")
        self.ws = f"{t}/ws"
        text = open(os.path.join(ROOT, ".github", "workflows", "agent.yml")).read()
        text = text.replace("/tmp/", f"{t}/").replace("/home/runner/", f"{t}/home/")
        self.job_env, self.steps = parse(text)
        self.role, self.stage, self.actor = role, stage, actor
        self.ran, self.failed_step, self.log = [], None, []
        self.run()

    def run(self):
        """Run every step in order the way GitHub does, keeping the job's status, env and step outputs."""
        t = self.tmp
        status = {"failed": False}
        steps_ctx, added = {}, {}
        ctx = {"inputs": Ctx(role=self.role, stage=self.stage, issue=N),
               "github": Ctx(event_name="workflow_dispatch", actor=self.actor, event=Ctx(), run_id="42", run_attempt="1",
                             server_url="https://github.com", repository="o/r", token="fake-github-token"),
               "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
               "vars": Ctx(DOKIMA_APP_ID="1"), "steps": Ctx()}
        job_env = {k: fill(v, {**ctx, "env": Ctx()}, status) for k, v in self.job_env.items()}
        base = git_env({"PATH": f"{t}/bin:" + os.environ["PATH"], "HOME": f"{t}/home", "FAKE_GH_DIR": f"{t}/gh",
                        "FAKE_REVIEW": f"{t}/review.json", "FAKE_CLAUDE_MARK": f"{t}/claude-started",
                        "GITHUB_REPOSITORY": "o/r", "GITHUB_REPOSITORY_OWNER": "o", "GITHUB_RUN_ID": "42",
                        "GITHUB_SERVER_URL": "https://github.com", "GITHUB_ACTOR": self.actor, "GITHUB_EVENT_NAME": "workflow_dispatch",
                        "GITHUB_STEP_SUMMARY": f"{t}/summary.md", "RUNNER_TEMP": f"{t}/runner-temp",
                        "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": f"url.file://{t}/origin.git.insteadOf",
                        "GIT_CONFIG_VALUE_0": "https://x-access-token:fake-token@github.com/o/r.git"})
        for step in self.steps:
            ctx["steps"] = Ctx(steps_ctx)
            ctx["env"] = Ctx({**job_env, **added})
            cond = step.get("if", "success()")
            if not re.search(r"\b(always|failure|success|cancelled)\(\)", cond):
                cond = f"success() && ({cond})"
            if not evaluate(cond, ctx, status):
                continue
            name = step.get("name") or step.get("uses") or step.get("id")
            self.ran.append(name)
            outputs = {}
            if "run" in step:
                env = {**base, **job_env, **added}
                env.update({k: fill(v, ctx, status) for k, v in step["env"].items()})
                env["GITHUB_ENV"], env["GITHUB_OUTPUT"] = f"{t}/step-env", f"{t}/step-output"
                for f in (env["GITHUB_ENV"], env["GITHUB_OUTPUT"]):
                    open(f, "w").close()
                open(f"{t}/step.sh", "w").write(fill(step["run"], ctx, status))
                p = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", f"{t}/step.sh"], cwd=self.ws,
                                   env=env, capture_output=True, text=True, timeout=120)
                self.log.append(f"## {name} (exit {p.returncode})\n{p.stdout[-1500:]}{p.stderr[-1500:]}")
                for l in open(env["GITHUB_ENV"]).read().splitlines():
                    if "=" in l:
                        k, v = l.split("=", 1)
                        added[k] = v
                for l in open(env["GITHUB_OUTPUT"]).read().splitlines():
                    if "=" in l:
                        k, v = l.split("=", 1)
                        outputs[k] = v
                if p.returncode != 0:
                    status["failed"] = True
                    self.failed_step = self.failed_step or name
            elif step.get("id") == "app":
                outputs = {"token": "fake-token", "app-slug": "dokima-runtime"}
            if step.get("id"):
                steps_ctx[step["id"]] = {"outputs": outputs, "outcome": "failure" if status["failed"] else "success"}
        self.env = {**job_env, **added}
        self.failed = status["failed"]

    def calls(self):
        """Every call made to the fake gh, as argument lists."""
        path = f"{self.tmp}/gh/calls.jsonl"
        return [json.loads(l) for l in open(path)] if os.path.exists(path) else []

    def posted(self):
        """Every comment posted, as {where, body}."""
        path = f"{self.tmp}/gh/posted.jsonl"
        return [json.loads(l) for l in open(path)] if os.path.exists(path) else []

    def dispatches(self):
        """Every signal sent to start another stage."""
        return [c for c in self.calls() if c[:1] == ["api"] and any("dispatches" in x for x in c)]

    def created_issues(self):
        """Every issue the run asked GitHub to create."""
        return [c for c in self.calls() if c[:2] == ["issue", "create"]]

    def agent_started(self):
        """True when the fake Claude Code was started."""
        return os.path.exists(f"{self.tmp}/claude-started")

    def board(self):
        """Where the run put the card, as written for the board step ('Plan needs'), or '' when it wrote nothing."""
        out = self.env.get("OUT", "")
        path = os.path.join(out, "board.txt")
        return open(path).read().strip() if out and os.path.exists(path) else ""

    def tail(self):
        """The failed step's output, then the last steps' output, for a failure message."""
        first = [l for l in self.log if self.failed_step and l.startswith(f"## {self.failed_step} (")][:1]
        return "\n".join(first + self.log[-3:])[-3000:]


SPLIT_PROPOSED = [owner_comment("/plan", "2026-10-07T10:00:00Z"),
                  record_comment(planner_record(SPLIT), "2026-10-07T10:10:00Z")]


def test_the_plan_reviewer_starts_on_a_split_with_no_try_branch(record_property, tmp_path):
    """The plan reviewer starts on an issue whose planner proposed a split, though the issue has no try branch.

    Runs the agent workflow for the reviewer at the plan stage on issue #57, whose newest record is a split and which
    has no try/issue-57 branch. The run must get through every step before the agent, start the agent, check its
    review and post its record on the issue, and it must start from main. Two neighbours keep their old behaviour: with
    a try branch the plan reviewer still starts on that branch, and the pull request reviewer, which has no work to
    look at without a branch, still does not start."""
    record_property("proves", "176.1")
    r = Run(tmp_path / "split", "reviewer", "plan", SPLIT_PROPOSED)
    assert r.agent_started(), (f"176.1: the plan reviewer never started on a split with no try/issue-57 branch; "
                               f"it stopped at '{r.failed_step}':\n{r.tail()}")
    assert not r.failed, f"176.1: the plan review of a split failed at '{r.failed_step}':\n{r.tail()}"
    assert r.env.get("BASE") == r.main_sha, "176.1: with no try branch the plan reviewer did not start from main"
    recs = agent.records([{"author": {"login": agent.BOT}, "body": p["body"]} for p in r.posted()])
    assert [(x["role"], x["stage"], x["check"]["passed"]) for x in recs] == [("reviewer", "plan", True)], \
        f"176.1: the plan review of the split did not post exactly one passed review record: {recs}"

    r = Run(tmp_path / "branch", "reviewer", "plan", SPLIT_PROPOSED, try_branch=True)
    assert r.agent_started() and r.env.get("BASE") == r.try_sha, \
        f"176.1: with a try branch the plan reviewer no longer starts on it:\n{r.tail()}"

    r = Run(tmp_path / "pr", "reviewer", "pr", SPLIT_PROPOSED)
    assert not r.agent_started(), "176.1: the pull request reviewer started with no try branch and so no work to review"


def test_a_reviewed_split_stops_for_the_owner_and_files_nothing_before_work(record_property, tmp_path, monkeypatch, capsys):
    """A split goes planner, reviewer, then stops and mentions the owner; its child issues are filed only after `/work`.

    Runs the plan review of a proposed split with no try branch, the reviewer approving. Its posted card must end with
    a Next line mentioning the owner, the card must carry the Needs you pill, no next stage may start and no issue may
    be filed. Then, as commands.yml decides what `/work` does: before the review the issue is not an approved split
    (so `/work` files nothing), and after the approving review it is one, which is what makes `/work` file the stories."""
    record_property("proves", "176.2")
    r = Run(tmp_path / "split", "reviewer", "plan", SPLIT_PROPOSED)
    assert r.agent_started(), f"176.2: the reviewer never reviewed the proposed split; it stopped at '{r.failed_step}':\n{r.tail()}"
    bodies = [p["body"] for p in r.posted()]
    assert len(bodies) == 1, f"176.2: the plan review posted {len(bodies)} comments, expected its one record"
    assert f"**Next:** @{OWNER}" in bodies[0], f"176.2: the approved split did not stop and mention the owner:\n{bodies[0][-600:]}"
    assert r.dispatches() == [], f"176.2: the approved split started another stage on its own: {r.dispatches()}"
    assert r.created_issues() == [], "176.2: child issues were filed before the owner's /work"
    assert r.board().endswith("needs"), f"176.2: the card does not show Needs you after the split was approved: {r.board()!r}"

    def kind_after(comments):
        issue = {"number": int(N), "title": "t", "body": "b", "comments": comments}
        monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
        monkeypatch.setattr(agent, "gh", lambda *a: json.dumps(issue) if a[:2] == ("issue", "view") else "[]")
        agent.main(["agent", "kind", N])
        return capsys.readouterr().out.strip()
    assert kind_after(SPLIT_PROPOSED) == "", "176.2: /work would file the stories of a split no reviewer has approved"
    approved = SPLIT_PROPOSED + [record_comment(review_record(APPROVE), "2026-10-07T10:20:00Z")]
    assert kind_after(approved) == "feature", "176.2: /work would not file the stories of the approved split"


def assert_says_why_and_stops(r, reason, crit="176.3"):
    """The run posted exactly one record on the issue naming the reason, mentioned the owner, and started nothing."""
    assert not r.agent_started(), f"{crit}: the agent started though its start should have failed"
    posts = r.posted()
    assert len(posts) == 1, f"{crit}: a start failure at '{r.failed_step}' posted {len(posts)} comments, expected one:\n{r.tail()}"
    assert posts[0]["where"][:2] == ["issue", "comment"] and N in posts[0]["where"], \
        f"{crit}: the start failure was not posted on issue #{N}: {posts[0]['where']}"
    body = posts[0]["body"]
    recs = agent.records([{"author": {"login": agent.BOT}, "body": body}])
    assert len(recs) == 1, f"{crit}: the start failure comment is not a record the bot can read back:\n{body[:600]}"
    assert recs[0]["check"]["passed"] is False, f"{crit}: the start failure's record says it passed"
    assert reason.lower() in body.lower(), f"{crit}: the comment does not say why ({reason!r}):\n{body[:800]}"
    assert "hand-back rejected" not in body, f"{crit}: the comment blames a hand-back, but the agent never started:\n{body[:600]}"
    assert f"**Next:** @{OWNER}" in body, f"{crit}: the start failure does not stop and mention the owner:\n{body[-600:]}"
    assert r.board().endswith("needs"), f"{crit}: the card does not show Needs you after the start failure: {r.board()!r}"
    assert r.dispatches() == [], f"{crit}: a start failure started another stage: {r.dispatches()}"


def test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner(record_property, tmp_path):
    """A run that fails before its agent starts posts a record on the issue saying why and mentions the owner.

    Three failures before the agent, each run through the whole workflow: a run started by someone who is not a code
    owner fails at the code-owner gate, a worker on an issue with no try branch fails at the starting branch, and a
    worker on an issue whose plan nobody approved fails building its pack. Each must post one record on the issue that
    names its own reason (not a code owner, try/issue-57, no passed plan), ends with a Next line mentioning the owner,
    puts Needs you on the card and starts no other stage."""
    record_property("proves", "176.3")
    story = [owner_comment("/plan", "2026-10-07T10:00:00Z"), record_comment(planner_record(STORY), "2026-10-07T10:10:00Z")]
    approved = story + [record_comment(review_record(APPROVE), "2026-10-07T10:20:00Z"), owner_comment("/work", "2026-10-07T10:30:00Z")]
    r = Run(tmp_path / "gate", "worker", "", approved, try_branch=True, actor="stranger")
    assert r.failed_step, "176.3: setup: the run started by someone who is not a code owner did not fail"
    assert_says_why_and_stops(r, "not a code owner")
    r = Run(tmp_path / "branch", "worker", "", approved)
    assert r.failed_step, "176.3: setup: the worker with no try branch did not fail"
    assert_says_why_and_stops(r, f"try/issue-{N}")
    r = Run(tmp_path / "pack", "worker", "", story, try_branch=True)
    assert r.failed_step, "176.3: setup: the worker with no approved plan did not fail"
    assert_says_why_and_stops(r, "no passed plan")


def test_a_start_failure_still_fails_the_run(record_property, tmp_path):
    """A run that fails before its agent starts still ends as a failed run on GitHub, after saying why.

    Runs the worker on an issue with no try branch: the comment saying why is posted, and the run itself ends failed,
    so a start failure is never shown as a success."""
    record_property("proves", "176.4")
    story = [owner_comment("/plan", "2026-10-07T10:00:00Z"), record_comment(planner_record(STORY), "2026-10-07T10:10:00Z")]
    r = Run(tmp_path / "branch", "worker", "", story)
    assert len(r.posted()) == 1, f"176.4: the start failure posted {len(r.posted())} comments, expected one:\n{r.tail()}"
    assert r.failed, "176.4: the run that failed before its agent started ended as a success"
