"""The PR card is redrawn after merge and shows the true Definition of Done (#315).

These tests run what GitHub runs. An event (a check finishing, an agent's record, the owner's Approve, a merge, a push
to main) is evaluated against the workflows' own files, .github/workflows/card.yml and agent.yml, with the expression
evaluator of test_start.py: the trigger must list the event, the job's and the step's `if:` must hold, and the step's
`${{ }}` env and arguments are filled in. The card code that step runs (`dokima/card.py`, or `-m dokima.card`, with
the step's arguments) then runs here, in this process, as `card.main()` against a fake GitHub, and the tests read what
it wrote on the issue and the pull request.

The fake GitHub is in this file (FakeGitHub). It stands in for `gh` in dokima.card, dokima.agent, dokima.plan and
dokima.body, and answers what the card reads today:
    gh issue view N --json ...                      the issue with its comments (agent records among them)
    gh issue edit N --body-file - (input=...)       writes the issue body
    gh pr list --head BRANCH --state S --json ...   PRs by head branch; state open, closed, merged or all
    gh pr view N --json comments,reviews            the PR's comments (records) and reviews
    gh api graphql (pullRequest closingIssuesReferences)   the issue a PR closes
    gh api repos/o/r/pulls?head=..&state=..         PRs (REST), by head and state (open, closed, all)
    gh api repos/o/r/pulls/N  [.../comments, .../reviews]
    gh api repos/o/r/commits/SHA/check-runs  and  .../commits/SHA/pulls
    gh api repos/o/r/contents/.github/CODEOWNERS    "* @boss"; any other file is missing
    gh api repos/o/r/actions/workflows/.../runs     no runs
    gh api repos/o/r/issues/N  [.../events]
    gh api -X PATCH repos/o/r/pulls/N -F body=@file (or -f body=...)   writes the PR body
    gh api -X PATCH repos/o/r/issues/N ... body                          writes the issue body
Any other call fails the way GitHub refuses an unknown path, and is listed in the failure message.

The repo is o/r, owned by `boss` through CODEOWNERS. Issue #40 was built in PR #5 (branch try/issue-40); its plan and
plan review are records on the issue, its worker record and code review record are on the PR. PR #4 (issue #39) is
an older merged PR whose merge commit is main's head, so a run that maps main's head to a PR finds #4.
"""
import copy
import json
import os
import re
import shlex
import subprocess
import sys

import pytest

import test_start as ts

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, body, card, plan  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = "o/r"
OWNER = "boss"
HEAD = "a" * 40          # PR #5's newest commit
MAIN = "m" * 40          # main's head: the merge commit of the older PR #4
STATES = {"passed", "failed", "running", "not started"}
CARD_CODE = re.compile(r"dokima[/.]card(?:\.py)?\b")


def rec(role, stage=None, n=1, **handback):
    """One agent record, as dokima.agent.records reads it from a bot comment."""
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}"}


def plan_for(number):
    """A one-criterion plan for issue `number`."""
    src = f"https://github.com/o/r/issues/{number}"
    return {"kind": "user_story", "summary": "Owners see one card.", "user_story": "Owners see one card.",
            "acceptance_criteria": [{"text": "First thing works.", "source": src}], "non_functional": [],
            "scope": ["x.py"], "out_of_scope": [], "tests": {f"{number}.1": ["tests/test_a.py::test_one"]},
            "test_changes": {}, "links": {"blocked_by": [], "blocks": [], "relates_to": []}}


REVIEW_RUN = "https://github.com/o/r/actions/runs/14"


def bot(r, at):
    """A record as the bot's comment, written at `at`."""
    return {"author": {"login": agent.BOT}, "body": f"{agent.MARK}\n```json\n{json.dumps(r)}\n```", "createdAt": at}


def check(name, n, status="completed", conclusion="success"):
    """One GitHub check run on a PR's newest commit."""
    return {"name": name, "status": status, "conclusion": conclusion,
            "html_url": f"https://github.com/o/r/actions/runs/9/job/{n}"}


class FakeGitHub:
    """GitHub for repo o/r in memory: issues, PRs, records, checks and reviews.

    Every write is logged in `writes`, every refused call in `unknown`."""

    def __init__(self):
        self.issues, self.prs, self.writes, self.unknown = {}, {}, [], []

    def add_issue(self, n, comments=()):
        """Add issue n with the owner's ask and these comments."""
        self.issues[n] = {"number": n, "title": f"Issue {n}", "body": "My ask.", "comments": list(comments)}

    def add_pr(self, n, issue, state="open", merged_by=None, head=HEAD, comments=(), reviews=(), check_runs=(),
               merge_sha=None, body_text=None):
        """Add PR n built for `issue`, with its records, reviews and checks."""
        merged = state == "merged"
        self.prs[n] = {"number": n, "issue": issue, "state": "closed" if merged else state, "merged": merged,
                       "merged_at": "2026-10-09T04:44:09Z" if merged else None,
                       "merged_by": {"login": merged_by, "type": "User"} if merged_by else None,
                       "merge_commit_sha": merge_sha, "head": {"ref": f"try/issue-{issue}", "sha": head},
                       "base": {"ref": "main"}, "body": body_text if body_text is not None else f"Closes #{issue}",
                       "html_url": f"https://github.com/o/r/pull/{n}", "title": f"PR {n}",
                       "comments": list(comments), "reviews": list(reviews), "check_runs": list(check_runs)}

    def rest_pr(self, p):
        """A PR as GitHub's REST API shows it."""
        return {k: v for k, v in p.items() if k not in ("issue", "comments", "reviews", "check_runs")}

    def cli_pr(self, p):
        """A PR as `gh pr list --json` shows it."""
        return {"number": p["number"], "headRefName": p["head"]["ref"], "title": p["title"], "body": p["body"],
                "state": "MERGED" if p["merged"] else p["state"].upper(), "mergedAt": p["merged_at"],
                "url": p["html_url"]}

    def by_state(self, state):
        """The PRs in a state: open (the default), closed, merged or all."""
        state = state or "open"
        return [p for p in self.prs.values() if state == "all" or (state == "merged" and p["merged"])
                or (state == p["state"])]

    def fail(self, args):
        """Refuse a call the way GitHub refuses an unknown path, and note it."""
        self.unknown.append(args)
        raise subprocess.CalledProcessError(1, ["gh", *args], output="", stderr="gh: Not Found (HTTP 404)")

    def __call__(self, *args, **kw):
        """Answer one `gh` call."""
        args = [str(a) for a in args]

        def flag(name):
            """The value after a flag, or None."""
            return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None
        if args[:2] == ["issue", "view"]:
            i = self.issues.get(int(args[2]))
            return json.dumps(i) if i else self.fail(args)
        if args[:2] == ["issue", "edit"] and flag("--body-file") == "-":
            n = int(args[2])
            self.issues[n]["body"] = kw.get("input")
            self.writes.append(("issue", n))
            return ""
        if args[:2] == ["pr", "list"]:
            found = [self.cli_pr(p) for p in self.by_state(flag("--state"))
                     if flag("--head") in (None, p["head"]["ref"])]
            q = flag("-q") or flag("--jq")
            if q == ".[0].number":
                return f"{found[0]['number']}\n" if found else "\n"
            return json.dumps(found)
        if args[:2] == ["pr", "view"]:
            p = self.prs.get(int(args[2]))
            if not p:
                return self.fail(args)
            return json.dumps({"comments": p["comments"], "body": p["body"], "headRefName": p["head"]["ref"],
                               "reviews": [{"author": r["user"], "body": r.get("body", ""), "state": r["state"],
                                            "submittedAt": r["submitted_at"]} for r in p["reviews"]]})
        if args[:1] == ["api"]:
            return self.api(args, flag)
        return self.fail(args)

    def api(self, args, flag):
        """Answer one `gh api` call: GraphQL, a read or a PATCH of a body."""
        rest = [a for a in args[1:] if not a.startswith("-")]
        if "graphql" in args:
            query = " ".join(args)
            m = re.search(r"\bp=(\d+)", query)
            if "pullRequest(" in query and m and int(m.group(1)) in self.prs:
                n = self.prs[int(m.group(1))]["issue"]
                return json.dumps({"data": {"repository": {"pullRequest": {
                    "closingIssuesReferences": {"nodes": [{"number": n}]}}}}})
            return self.fail(args)
        path = next((a for a in rest if a.startswith("repos/")), "")
        method = flag("-X") or ("POST" if any(a in args for a in ("-f", "-F", "--input")) else "GET")
        if method == "PATCH":
            text = None
            for i, a in enumerate(args):
                if a in ("-f", "-F", "--field", "--raw-field") and args[i + 1].startswith("body="):
                    v = args[i + 1][len("body="):]
                    text = open(v[1:]).read() if v.startswith("@") else v
            m = re.fullmatch(r"repos/o/r/(pulls|issues)/(\d+)", path)
            if not m or text is None:
                return self.fail(args)
            n = int(m.group(2))
            if m.group(1) == "pulls" and n in self.prs:
                self.prs[n]["body"] = text
                self.writes.append(("pr", n))
            elif m.group(1) == "issues" and n in self.issues:
                self.issues[n]["body"] = text
                self.writes.append(("issue", n))
            else:
                return self.fail(args)
            return "{}"
        if method != "GET":
            return self.fail(args)
        bare, _, query = path.partition("?")
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        m = re.fullmatch(r"repos/o/r/pulls/(\d+)(/comments|/reviews)?", bare)
        if m and int(m.group(1)) in self.prs:
            p = self.prs[int(m.group(1))]
            return json.dumps([] if m.group(2) == "/comments" else p["reviews"] if m.group(2) else self.rest_pr(p))
        if bare == "repos/o/r/pulls":
            head = params.get("head", "").split(":")[-1]
            return json.dumps([self.rest_pr(p) for p in self.by_state(params.get("state"))
                               if not head or p["head"]["ref"] == head])
        m = re.fullmatch(r"repos/o/r/commits/(\w+)/(check-runs|pulls)", bare)
        if m:
            sha = m.group(1)
            if m.group(2) == "pulls":
                return json.dumps([self.rest_pr(p) for p in self.prs.values()
                                   if sha in (p["head"]["sha"], p["merge_commit_sha"])])
            runs = next((p["check_runs"] for p in self.prs.values() if p["head"]["sha"] == sha), [])
            return json.dumps({"total_count": len(runs), "check_runs": runs})
        if bare == "repos/o/r/contents/.github/CODEOWNERS":
            return f"* @{OWNER}\n"
        if bare.startswith("repos/o/r/contents/"):
            raise subprocess.CalledProcessError(1, ["gh", *args], output="", stderr="gh: Not Found (HTTP 404)")
        if re.fullmatch(r"repos/o/r/actions/workflows/[\w.-]+/runs", bare):
            return json.dumps({"total_count": 0, "workflow_runs": []})
        m = re.fullmatch(r"repos/o/r/issues/(\d+)(/events)?", bare)
        if m and int(m.group(1)) in self.issues:
            i = self.issues[int(m.group(1))]
            return json.dumps([] if m.group(2) else {"number": i["number"], "title": i["title"], "body": i["body"],
                                                      "state": "open"})
        return self.fail(args)


def history(number, pr_number, verdict="approve"):
    """The records of an issue built in a PR, on both pages.

    The plan and its review are on the issue; the worker and the code review are on the PR."""
    on_issue = [bot(rec("planner", n=11, **plan_for(number)), "2026-10-09T04:00:00Z"),
                bot(rec("reviewer", "plan", n=12, verdict="approve", blockers=[]), "2026-10-09T04:05:00Z"),
                {"author": {"login": OWNER}, "body": "/work", "createdAt": "2026-10-09T04:06:00Z"}]
    on_pr = [bot(rec("worker", n=13), "2026-10-09T04:20:00Z"),
             bot(rec("reviewer", "pr", n=14, verdict=verdict, blockers=[]), "2026-10-09T04:32:00Z")]
    return on_issue, on_pr


def green(number, head_n=1):
    """Passing criterion and all tests checks for issue `number`."""
    return [check(f"{number}.1 · First thing works", head_n), check("all tests", head_n + 1)]


def github_with(state="open", merged_by=None, reviews=()):
    """A fake GitHub: issue #40 built in PR #5, and older merged PR #4.

    PR #5 is in `state`; PR #4, of issue #39, merged into main's head."""
    g = FakeGitHub()
    on_issue, on_pr = history(40, 5)
    g.add_issue(40, on_issue)
    g.add_pr(5, 40, state=state, merged_by=merged_by, comments=on_pr, reviews=reviews, check_runs=green(40))
    old_issue, old_pr = history(39, 4)
    g.add_issue(39, old_issue)
    g.add_pr(4, 39, state="merged", merged_by=OWNER, head="b" * 40, merge_sha=MAIN, comments=old_pr,
             check_runs=green(39, 5))
    return g


def use(monkeypatch, tmp_path, g):
    """Route every `gh` call of the card code to the fake GitHub."""
    for mod in (card, agent, plan, body):
        monkeypatch.setattr(mod, "gh", g)

    def fetch_issue(repo, n):
        i = g.issues[int(n)]
        return {"number": int(n), "title": i["title"], "url": f"https://github.com/o/r/issues/{n}",
                "approved_at": None, "changes": [], "plan": plan.parse(i["body"]), "current_body": i["body"],
                "body": i["body"]}
    monkeypatch.setattr(plan, "fetch_issue", fetch_issue)
    monkeypatch.chdir(tmp_path)


# Reading and evaluating the workflows

class SafeList(list):
    """A list as GitHub expressions read it: past its end is null.

    Objects inside it read with dots."""

    def __getitem__(self, i):
        """Item i, or null past the end."""
        try:
            v = list.__getitem__(self, i)
        except (IndexError, TypeError):
            return ts.NIL
        return ts.Ctx(v) if isinstance(v, dict) else v


def safe(v):
    """An event payload whose lists read as GitHub's do in expressions."""
    if isinstance(v, dict):
        return {k: safe(x) for k, x in v.items()}
    if isinstance(v, list):
        return SafeList(safe(x) for x in v)
    return v


class AnySteps(ts.Ctx):
    """The steps context: every earlier step (an app token step, say) gave a token."""

    def __getattr__(self, k):
        """Any step, with a token in its outputs."""
        return ts.Ctx(outputs=ts.Ctx(token="fake-token", **{"app-slug": "dokima-runtime"}), outcome="success",
                      conclusion="success")


def context(event_name, event, run_id="1", inputs=None):
    """The expression contexts GitHub gives a run for this event."""
    github = {"event_name": event_name, "event": safe(event), "repository": REPO, "repository_owner": "o",
              "run_id": run_id, "actor": OWNER, "ref": "refs/heads/main", "sha": MAIN}
    return {"github": ts.Ctx(github), "inputs": ts.Ctx(inputs or {}), "vars": ts.Ctx(DOKIMA_APP_ID="1"),
            "secrets": ts.Ctx(DOKIMA_APP_KEY="k", CLAUDE_CODE_OAUTH_TOKEN="c"), "steps": AnySteps(),
            "needs": ts.Ctx(), "job": ts.Ctx(status="success")}


def listed(on, event_name):
    """The event's block in a workflow's `on:`, or None when it does not listen."""
    if isinstance(on, str):
        return {} if on == event_name else None
    if isinstance(on, list):
        return {} if event_name in on else None
    if not isinstance(on, dict) or event_name not in on:
        return None
    return on[event_name] if isinstance(on[event_name], dict) else {}


def as_list(v):
    """A value as a list: one value in a list, nothing as []."""
    return v if isinstance(v, list) else [v] if v else []


def fires(wf, event_name, event):
    """True when GitHub starts this workflow for the event."""
    block = listed(wf.get("on"), event_name)
    if block is None:
        return False
    types = as_list(block.get("types"))
    if types and event.get("action") not in types:
        return False
    if event_name == "workflow_run":
        return event["workflow_run"]["name"] in as_list(block.get("workflows"))
    if event_name == "push":
        import fnmatch
        branches = as_list(block.get("branches"))
        if branches and not any(fnmatch.fnmatch(event["ref"].split("/", 2)[-1], b) for b in branches):
            return False
        paths = as_list(block.get("paths"))
        return not paths or any(fnmatch.fnmatch(f, p) or fnmatch.fnmatch(f, p.replace("**", "*"))
                                for f in event["changed"] for p in paths)
    return True


def card_steps(wf, ctx):
    """Every step that runs the card code and would run for one event.

    Returns (step, filled env, filled run text) for each."""
    out = []
    status = {"failed": False}
    wf_env = {k: ts.fill(v, ctx, status) for k, v in (wf.get("env") or {}).items()}
    for job in (wf.get("jobs") or {}).values():
        if not ts.evaluate(ts.condition(job.get("if")), ctx, status):
            continue
        job_env = {**wf_env, **{k: ts.fill(v, {**ctx, "env": ts.Ctx(wf_env)}, status)
                               for k, v in (job.get("env") or {}).items()}}
        sctx = {**ctx, "env": ts.Ctx(job_env)}
        for step in job.get("steps") or []:
            if "run" not in step or not CARD_CODE.search(step["run"]):
                continue
            if not ts.evaluate(ts.condition(step.get("if")), sctx, status):
                continue
            env = {**job_env, **{k: ts.fill(v, sctx, status) for k, v in (step.get("env") or {}).items()}}
            out.append((step, env, ts.fill(step["run"], sctx, status)))
    return out


def card_args(run_text):
    """The arguments a step gives the card code, from its `python3` line."""
    for line in run_text.splitlines():
        if not CARD_CODE.search(line):
            continue
        words = shlex.split(line, comments=True)
        for i, w in enumerate(words):
            if w.endswith("card.py"):
                return words[i + 1:]
            if w == "dokima.card" and i and words[i - 1] == "-m":
                return words[i + 1:]
    return None


CARD_ENV = ("REPO", "ISSUE_NUMBER", "PR_NUMBER", "HEAD_SHA", "RUN_TITLE", "GITHUB_REPOSITORY", "GITHUB_EVENT_NAME",
            "EVENT", "EVENT_NAME")


def run_card(monkeypatch, args, env):
    """Run `card.main()` here, with the step's arguments and environment."""
    for k in CARD_ENV:
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        if isinstance(v, str):
            monkeypatch.setenv(k, v)
    monkeypatch.setattr(sys, "argv", ["card.py", *args])
    card.main()


def card_yml():
    """card.yml, read."""
    return ts.workflow("card.yml")


def redraw_by_card_yml(monkeypatch, g, event_name, event, run_id="1"):
    """Run card.yml for one event and return the writes it made on the fake GitHub.

    Returns [] when GitHub would not start it, or no step that runs the card code would run."""
    wf = card_yml()
    if not fires(wf, event_name, event):
        return []
    steps = card_steps(wf, context(event_name, event, run_id))
    for step, env, text in steps:
        args = card_args(text)
        assert args is not None, f"test setup: cannot read how this card.yml step runs the card code: {text}"
        run_card(monkeypatch, args, {**env, "GITHUB_EVENT_NAME": event_name})
    return list(g.writes)


def workflow_run(name, pr=5, event="pull_request_target", head=HEAD, title=""):
    """A workflow_run event: workflow `name` completed for PR `pr` (None: for main)."""
    return {"action": "completed", "sender": {"login": "o", "type": "User"},
            "workflow": {"name": name},
            "workflow_run": {"name": name, "event": event, "head_sha": head, "conclusion": "success",
                             "head_branch": f"try/issue-40" if pr else "main", "display_title": title,
                             "pull_requests": [{"number": pr, "head": {"sha": head}}] if pr else []}}


def pr_event(action, number=5, merged=True, merged_by=OWNER):
    """A pull_request_target event on PR `number`."""
    return {"action": action, "number": number, "sender": {"login": merged_by, "type": "User"},
            "pull_request": {"number": number, "merged": merged, "state": "closed",
                             "merged_by": {"login": merged_by} if merged else None,
                             "head": {"ref": "try/issue-40", "sha": HEAD}, "base": {"ref": "main"}}}


def issue_edit(number, sender_type):
    """An issues event: issue `number` edited by a user or a bot."""
    return {"action": "edited", "issue": {"number": number}, "sender": {"login": "x", "type": sender_type}}


# What the card shows

def block(text):
    assert plan.CARD_START in (text or "") and plan.CARD_END in text, f"no card between its markers in: {text!r}"
    return text[text.index(plan.CARD_START):text.index(plan.CARD_END) + len(plan.CARD_END)]


def done_row(text):
    """The three Definition of Done verdicts, each with its link.

    Returns [(state, link or None)] for All tests, Code review and Owner approval."""
    line = next((l for l in block(text).splitlines() if "Definition of Done" in l), None)
    assert line, f"the card has no Definition of Done line:\n{text}"
    out = []
    for m in re.finditer(r'(?:<a href="([^"]+)">)?<img [^>]*alt="([^"]*)"[^>]*>(</a>)?', line):
        if m.group(2) in STATES:
            out.append((m.group(2), m.group(1) if m.group(3) else None))
    assert len(out) == 3, f"the Definition of Done line does not hold three verdicts: {line}"
    return out


def status_words(text):
    """The words of the card's status line."""
    lines = [l for l in block(text).splitlines()[1:] if l.strip() and not l.startswith("<!--")]
    return re.sub(r"<[^>]+>|\*", "", next(l for l in lines if "**" in l and "User story" not in l)).strip()


def both_cards(g, crit, case, issue=40, pr=5):
    """The card on the issue and the PR, checked redrawn on both and equal."""
    assert ("issue", issue) in g.writes, f"{crit}: {case}: the card was not redrawn on issue #{issue} (writes: {g.writes}," \
                                         f" calls GitHub refused: {g.unknown})"
    assert ("pr", pr) in g.writes, f"{crit}: {case}: the card was not redrawn on PR #{pr} (writes: {g.writes}," \
                                   f" calls GitHub refused: {g.unknown})"
    a, b = block(g.issues[issue]["body"]), block(g.prs[pr]["body"])
    assert a == b, f"{crit}: {case}: the issue card and the PR card differ:\n{a}\n---\n{b}"
    return a


# The agent workflow's redraw after a record

AGENT_ISSUE = "40"


def agent_card_steps(tmp_path):
    """Run agent.yml's card steps after the record is posted, with `python3` and `gh` faked.

    Each step runs with bash. Returns [(step name, [{argv, env} of each python3 call])]; fails when the step that
    posts the record is gone."""
    wf = ts.workflow("agent.yml")
    job = wf["jobs"]["run"]
    steps = job["steps"]
    at = [i for i, s in enumerate(steps) if str(s.get("name", "")).startswith("Post the record")]
    assert at, "test setup: agent.yml has no step that posts the run's record"
    ctx = context("workflow_dispatch", {}, inputs={"role": "reviewer", "stage": "pr", "issue": AGENT_ISSUE})
    status = {"failed": False}
    job_env = {k: ts.fill(v, {**ctx, "env": ts.Ctx()}, status) for k, v in (job.get("env") or {}).items()}
    sctx = {**ctx, "env": ts.Ctx(job_env)}
    shims = tmp_path / "shims"
    shims.mkdir(exist_ok=True)
    log = tmp_path / "python3-calls.jsonl"
    (shims / "python3").write_text(f"#!{sys.executable}\nimport json, os, sys\n"
                                   f"open({str(log)!r}, 'a').write(json.dumps({{'argv': sys.argv[1:], "
                                   f"'env': dict(os.environ)}}) + '\\n')\n")
    (shims / "gh").write_text("#!/bin/sh\nexit 0\n")
    for f in ("python3", "gh"):
        os.chmod(shims / f, 0o755)
    out = []
    for step in steps[at[0] + 1:]:
        if "run" not in step or not CARD_CODE.search(step["run"]):
            continue
        if not ts.evaluate(ts.condition(step.get("if")), sctx, status):
            continue
        env = {**os.environ, **job_env, "PATH": f"{shims}:{os.environ['PATH']}", "GITHUB_REPOSITORY": REPO,
               "GITHUB_ENV": str(tmp_path / "genv"), "GITHUB_OUTPUT": str(tmp_path / "gout")}
        env.update({k: ts.fill(v, sctx, status) for k, v in (step.get("env") or {}).items()})
        for k in CARD_ENV:
            if k not in job_env and k not in (step.get("env") or {}) and k != "GITHUB_REPOSITORY":
                env.pop(k, None)
        if log.exists():
            log.unlink()
        script = tmp_path / "step.sh"
        script.write_text(ts.fill(step["run"], sctx, status))
        subprocess.run(["bash", "-e", str(script)], cwd=str(tmp_path), env=env, capture_output=True, text=True,
                       timeout=60)
        calls = [json.loads(l) for l in log.read_text().splitlines()] if log.exists() else []
        out.append((step.get("name"), calls))
    return out


def card_call(calls):
    """The `python3` call that runs the card code, and where that code comes from.

    Returns (main or branch, its arguments, its environment), or Nones when no call ran it."""
    for c in calls:
        argv, env = c["argv"], c["env"]
        if argv[:2] == ["-m", "dokima.card"]:
            return ("main" if "/tmp/runtime" in env.get("PYTHONPATH", "") else "branch"), argv[2:], env
        if argv and argv[0].endswith("dokima/card.py"):
            return ("main" if argv[0].startswith("/tmp/runtime/") else "branch"), argv[1:], env
    return None, None, None


def agent_redraw(monkeypatch, tmp_path, g):
    """Run agent.yml's redraw after a code review's record, then the card code it starts.

    Returns why it failed, or None."""
    found = agent_card_steps(tmp_path)
    if not found:
        return "agent.yml runs no card redraw after it posts the run's record"
    for name, calls in found:
        where, args, env = card_call(calls)
        if where is None:
            continue
        if where != "main":
            return f"agent.yml's step '{name}' runs the branch's own copy of the card code, not main's"
        run_card(monkeypatch, args, {k: env[k] for k in CARD_ENV if k in env})
        return None
    return f"agent.yml's steps {[n for n, _ in found]} never ran the card code"


# 315.1: the card is redrawn whenever anything it shows changes

def test_the_card_is_redrawn_on_both_pages_whenever_something_it_shows_changes(record_property, monkeypatch, tmp_path):
    """Both cards are redrawn after a check, a record, an approval and a merge.

    Runs each event through the real workflow files and the card code they start, against a fake GitHub: the all
    tests and criteria checks finishing on PR #5, the code review's record being posted by agent.yml, the owner's
    Approve (its commands run), and the merge of PR #5. Each must redraw the card on issue #40 and on PR #5. A
    command typed in an issue comment and the bot's own edit of the issue must redraw nothing, and never the older
    PR #4 that main's head points to. Proves 315.1."""
    record_property("proves", "315.1")
    wrong = []
    approve = [{"user": {"login": OWNER}, "state": "APPROVED", "submitted_at": "2026-10-09T04:40:00Z",
                "html_url": "https://github.com/o/r/pull/5#pullrequestreview-1", "body": ""}]
    cases = [("the all tests check finished", "workflow_run", workflow_run("full suite"), "open", None, ()),
             ("the criteria checks finished", "workflow_run", workflow_run("done-whens"), "open", None, ()),
             ("the owner approved the PR", "workflow_run",
              workflow_run("commands", event="pull_request_review"), "open", None, approve),
             ("the PR merged", "pull_request_target", pr_event("closed"), "merged", OWNER, ())]
    for i, (case, name, event, state, merged_by, reviews) in enumerate(cases):
        g = github_with(state, merged_by, reviews)
        use(monkeypatch, tmp_path, g)
        try:
            redraw_by_card_yml(monkeypatch, g, name, event, run_id=str(100 + i))
            both_cards(g, "315.1", case)
            if reviews:
                assert done_row(g.prs[5]["body"])[2][0] == "passed", \
                    "315.1: the card redrawn after the owner's Approve does not show Owner approval passed"
        except AssertionError as e:
            wrong.append(str(e).split("\n")[0].removeprefix("315.1: "))
        except (subprocess.CalledProcessError, KeyError, TypeError, ValueError) as e:
            wrong.append(f"{case}: the card code crashed: {e!r}")
    g = github_with()
    use(monkeypatch, tmp_path, g)
    try:
        why = agent_redraw(monkeypatch, tmp_path, g)
        assert why is None, f"315.1: the code review's record was posted: {why}"
        both_cards(g, "315.1", "the code review's record was posted")
    except AssertionError as e:
        wrong.append(str(e).split("\n")[0].removeprefix("315.1: "))
    except (subprocess.CalledProcessError, KeyError, TypeError, ValueError) as e:
        wrong.append(f"the code review's record was posted: the card code crashed: {e!r}")
    for case, name, event in (("a command typed in an issue comment", "workflow_run",
                               workflow_run("commands", pr=None, event="issue_comment", head=MAIN, title="/plan")),
                              ("the bot's own edit of the issue", "issues", issue_edit(40, "Bot"))):
        g = github_with()
        use(monkeypatch, tmp_path, g)
        try:
            writes = redraw_by_card_yml(monkeypatch, g, name, event)
        except (subprocess.CalledProcessError, KeyError, TypeError, ValueError) as e:
            writes = [f"crashed: {e}"]
        if writes:
            wrong.append(f"{case} redrew cards, though nothing on them changed: {writes}")
    assert not wrong, "315.1: " + "\n315.1: ".join(wrong)


# 315.2: after merge, both cards show the true Definition of Done

def test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed(record_property, monkeypatch,
                                                                                      tmp_path):
    """After the owner merges, both cards say Merged with every Definition of Done item passed.

    Merges PR #5 (code owner `boss`, no Approve review) through card.yml's own trigger, with green checks on its
    newest commit and the code review's approving record posted on the PR, not the issue. Both cards must say
    Merged; All tests must link its check; Code review must be passed and link the review's run; Owner approval
    must be passed and link the PR. The same merge by someone who is not a code owner must not show Owner approval
    passed. Proves 315.2."""
    record_property("proves", "315.2")
    g = github_with("merged", OWNER)
    use(monkeypatch, tmp_path, g)
    redraw_by_card_yml(monkeypatch, g, "pull_request_target", pr_event("closed"))
    text = both_cards(g, "315.2", "the owner merged PR #5")
    assert "Merged" in status_words(text), f"315.2: the merged PR's card does not say Merged: {status_words(text)}"
    tests_, review, approval = done_row(text)
    assert tests_ == ("passed", "https://github.com/o/r/actions/runs/9/job/2"), \
        f"315.2: All tests shows {tests_}, not passed with a link to its check"
    assert review == ("passed", REVIEW_RUN), \
        f"315.2: Code review shows {review}, not passed with a link to the review's run on the PR"
    assert approval == ("passed", "https://github.com/o/r/pull/5"), \
        f"315.2: the owner's merge shows Owner approval {approval}, not passed with a link to the PR"
    g = github_with("merged", "someone")
    use(monkeypatch, tmp_path, g)
    redraw_by_card_yml(monkeypatch, g, "pull_request_target", pr_event("closed", merged_by="someone"))
    text = both_cards(g, "315.2", "someone else merged PR #5")
    assert done_row(text)[2][0] != "passed", "315.2: a merge by someone who is not a code owner shows Owner approval passed"


# 315.3: only the criterion's sentence links to its run

def drawn(texts, nfr=(), checks=True):
    """The card for issue #40 with these criteria and non-functional requirements.

    Each has its own check when `checks` is true."""
    p = dict(plan_for(40), acceptance_criteria=[{"text": t, "source": "https://github.com/o/r/issues/40"} for t in texts],
             non_functional=[{"text": t, "why": "w", "principle": "p"} for t in nfr])
    recs = [rec("planner", n=11, **p), rec("reviewer", "plan", n=12, verdict="approve")]
    runs = [check(f"40.{k} · x", k) for k in range(1, len(texts) + len(nfr) + 1)] if checks else []
    found = {"recs": recs, "pr": None, "check_runs": runs, "reviews": [], "owners": {OWNER}, "tests": {},
             "worker": None, "children": []}
    return card.render(REPO, {"number": 40, "url": "https://github.com/o/r/issues/40"}, found)


def bullet(text, label, words):
    """The part of a criterion's bullet after its label, links written as HTML."""
    for line in block(text).splitlines():
        if line.startswith("- ") and f"**{label}:**" in line and words in re.sub(r"<[^>]+>", "", line):
            return line.split(f"**{label}:**", 1)[1].strip()
    raise AssertionError(f"no {label} bullet holds “{words}”:\n{text}")


AUDIT = ("The audit command, `python3 -m dokima.audit OWNER/REPO`, reads the repo's live settings and compares them "
         "with the manifest. It reads the labels, the board and main's branch rule.")


@pytest.mark.parametrize("text, sentence, rest", [
    ("First thing works. It also says why, in more words.", "First thing works.", "It also says why, in more words."),
    (AUDIT, AUDIT.split(" It reads")[0], "It reads the labels, the board and main's branch rule."),
    ("Does it work? Yes, always.", "Does it work?", "Yes, always."),
], ids=["two-sentences", "dots-inside-code", "question"])
def test_only_the_criterion_sentence_links_to_its_run(record_property, text, sentence, rest):
    """Only the criterion's first sentence links to its run; the explanation stays plain.

    Draws a card whose criterion has an explanation after its sentence and checks the bullet is the sentence inside
    the link to its check, then the explanation outside any link. A dot inside a command (dokima.audit) does not end
    the sentence, and a question mark does. Proves 315.3."""
    record_property("proves", "315.3")
    part = bullet(drawn([text]), "Acceptance criterion", sentence)
    url = "https://github.com/o/r/actions/runs/9/job/1"
    want = f'<a href="{url}">{card.escape(sentence)}</a>' + (f" {card.escape(rest)}" if rest else "")
    assert part == want, f"315.3: the criterion reads\n  {part}\nnot\n  {want}"


def test_the_sentence_link_holds_for_non_functional_requirements_and_no_check_means_no_link(record_property):
    """A non-functional requirement links only its sentence; with no check, nothing links.

    Draws a card with one non-functional requirement that has an explanation, and checks only its sentence is
    linked; a criterion of one sentence is linked whole. Then draws the same card with no checks and checks every
    word is there with no link at all. Proves 315.3."""
    record_property("proves", "315.3")
    one = bullet(drawn(["One sentence only."]), "Acceptance criterion", "One sentence only.")
    assert one == '<a href="https://github.com/o/r/actions/runs/9/job/1">One sentence only.</a>', \
        f"315.3: a one-sentence criterion reads {one}"
    text = drawn(["First thing works. Then more."], nfr=["Nothing leaks. Not even logs."])
    part = bullet(text, "Non-functional requirement", "Nothing leaks.")
    assert part == '<a href="https://github.com/o/r/actions/runs/9/job/2">Nothing leaks.</a> Not even logs.', \
        f"315.3: the non-functional requirement reads {part}"
    bare = drawn(["First thing works. Then more."], checks=False)
    part = bullet(bare, "Acceptance criterion", "First thing works.")
    assert part == "First thing works. Then more.", f"315.3: a criterion with no check reads {part}"


# 315.4: every merged PR whose card is stale is redrawn once

STALE = f"{plan.CARD_START}\n**Review**\n\nAll tests running\n{plan.CARD_END}"


def backfill_github(monkeypatch, tmp_path):
    """A fake GitHub with four PRs, two merged, for the redraw of merged cards.

    Merged PR #5 (issue #40) has a stale card, merged PR #6 (issue #41) a card that matches a fresh drawing; open
    PR #7 (issue #42) and closed, unmerged PR #8 (issue #43) both have stale cards."""
    g = FakeGitHub()
    for n, pr, state in ((40, 5, "merged"), (41, 6, "merged"), (42, 7, "open"), (43, 8, "closed")):
        on_issue, on_pr = history(n, pr)
        g.add_issue(n, on_issue)
        g.issues[n]["body"] = body.redraw("My ask.", STALE)
        g.add_pr(n=pr, issue=n, state=state, merged_by=OWNER if state == "merged" else None, head=str(pr) * 40,
                 comments=on_pr, check_runs=green(n, 10 * pr), body_text=f"{STALE}\n\nCloses #{n}")
    use(monkeypatch, tmp_path, g)
    card.draw(REPO, 41, 6)
    g.writes.clear()
    return g


def backfill_by_push(monkeypatch, g):
    """The push to main that lands this change (it changes dokima/card.py), through card.yml."""
    event = {"ref": "refs/heads/main", "after": MAIN, "changed": ["dokima/card.py", "tests/test_card_redraw.py"],
             "head_commit": {"id": MAIN}, "sender": {"login": OWNER, "type": "User"}}
    return redraw_by_card_yml(monkeypatch, g, "push", {**event, "action": None})


def test_when_this_lands_every_merged_pr_with_a_stale_card_is_redrawn_once(record_property, monkeypatch, tmp_path):
    """When this lands on main, each merged PR with a stale card is redrawn once.

    Pushes the change to main through card.yml, with two merged PRs (one stale, one already right), an open one
    and a closed unmerged one, both stale. Only the stale merged PR #5 and its issue #40 must be written, once each,
    with the card a fresh drawing gives; a second run writes nothing. Proves 315.4."""
    record_property("proves", "315.4")
    g = backfill_github(monkeypatch, tmp_path)
    expected = copy.deepcopy(g)
    use(monkeypatch, tmp_path, expected)
    card.draw(REPO, 40, 5)
    use(monkeypatch, tmp_path, g)
    writes = backfill_by_push(monkeypatch, g)
    assert writes, ("315.4: the push to main that changes how cards are drawn redrew no merged PR's card "
                    f"(calls GitHub refused: {g.unknown})")
    assert sorted(writes) == [("issue", 40), ("pr", 5)], \
        f"315.4: the redraw wrote {sorted(writes)}, not just stale merged PR #5 and its issue #40, once each"
    assert block(g.prs[5]["body"]) == block(expected.prs[5]["body"]), "315.4: PR #5's card is not a fresh drawing"
    assert block(g.issues[40]["body"]) == block(expected.issues[40]["body"]), "315.4: issue #40's card is not a fresh drawing"
    assert g.prs[5]["body"].endswith("Closes #40"), "315.4: PR #5 lost its line closing the issue"
    g.writes.clear()
    again = backfill_by_push(monkeypatch, g)
    assert again == [], f"315.4: running the redraw a second time wrote {again}; a card already right is left alone"


# 315.5: main's copy draws every card, and no waiting redraw is dropped

def test_only_mains_copy_of_the_card_code_ever_draws_a_card(record_property, tmp_path):
    """Only main's copy of the card code draws a card, never a pull request's own.

    card.yml must not listen to events that run a pull request's copy of the workflow (pull_request,
    pull_request_review, pull_request_review_comment) and must never check out a pull request's code; agent.yml's
    redraw after a record must run the runtime copied from main, not the branch it has checked out. Proves 315.5."""
    record_property("proves", "315.5")
    wf = card_yml()
    on = wf.get("on")
    for ev in ("pull_request", "pull_request_review", "pull_request_review_comment"):
        assert listed(on, ev) is None, f"315.5: card.yml listens to {ev}, which runs the pull request's own copy"
    for job in (wf.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            if "checkout" in str(step.get("uses")):
                assert not (step.get("with") or {}).get("ref"), \
                    f"315.5: card.yml checks out {step['with']['ref']}, so a pull request's code could draw its card"
    found = agent_card_steps(tmp_path)
    assert found, "315.5: agent.yml runs no card redraw after it posts the run's record"
    wheres = [card_call(calls)[0] for _, calls in found]
    assert "main" in wheres and "branch" not in wheres, \
        f"315.5: agent.yml's redraw runs the card code from {wheres}, not only from main's copy in /tmp/runtime"


def groups(events):
    """The card job's concurrency group for each event, and whether it cancels a running run."""
    wf = card_yml()
    job = next(iter(wf["jobs"].values()))
    levels = [c for c in (wf.get("concurrency"), job.get("concurrency")) if c]
    levels = [{"group": c} if isinstance(c, str) else c for c in levels]
    out = {}
    for i, (name, (event_name, event)) in enumerate(events.items()):
        ctx = context(event_name, event, run_id=str(500 + i))
        status = {"failed": False}
        group = ts.fill(levels[-1].get("group") or "", ctx, status).strip() if levels else ""
        cancels = any(ts.fill(c.get("cancel-in-progress") or "false", ctx, status).strip().lower() == "true"
                      for c in levels)
        out[name] = (group, cancels)
    return out


def test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run(record_property):
    """A waiting redraw is never dropped for another PR's redraw or an idle run.

    GitHub keeps one waiting run per concurrency group and cancels it when a newer one arrives. card.yml's group
    is read for redraws of PR #5 (two checks), PR #6 (merge), PR #7 (approval), issue #41 and issue #40 (an owner's
    edit of each), and for two runs that draw nothing: the bot's own edit of issue #40 (each card write makes one)
    and a command typed in an issue comment. The two redraws of PR #5 must share a group, each other issue and pull
    request must have its own, no run that draws nothing may sit in a redraw's group (not even the group of the
    issue it edits), and no run may cancel one already running. Proves 315.5."""
    record_property("proves", "315.5")
    events = {"all tests on PR #5": ("workflow_run", workflow_run("full suite")),
              "criteria checks on PR #5": ("workflow_run", workflow_run("done-whens")),
              "merge of PR #6": ("pull_request_target", dict(pr_event("closed", 6),
                                                             pull_request=dict(pr_event("closed", 6)["pull_request"],
                                                                               head={"ref": "try/issue-41",
                                                                                     "sha": "6" * 40}))),
              "approval of PR #7": ("workflow_run", workflow_run("commands", pr=7, event="pull_request_review",
                                                                 head="7" * 40)),
              "owner's edit of issue #41": ("issues", issue_edit(41, "User")),
              "owner's edit of issue #40": ("issues", issue_edit(40, "User")),
              "bot's edit of issue #40": ("issues", issue_edit(40, "Bot")),
              "command in an issue comment": ("workflow_run", workflow_run("commands", pr=None, event="issue_comment",
                                                                         head=MAIN, title="/plan"))}
    g = groups(events)
    for name, (group, cancels) in g.items():
        assert group, f"315.5: {name} waits in no concurrency group"
        assert not cancels, f"315.5: {name} cancels a card run already drawing"
    assert g["all tests on PR #5"][0] == g["criteria checks on PR #5"][0], \
        f"315.5: two redraws of PR #5 wait in different groups ({g['all tests on PR #5'][0]!r}, " \
        f"{g['criteria checks on PR #5'][0]!r}), so they can draw at once and an older one can land last"
    redraws = ["all tests on PR #5", "merge of PR #6", "approval of PR #7", "owner's edit of issue #41",
               "owner's edit of issue #40"]
    seen = {}
    for name in redraws:
        assert g[name][0] not in seen, \
            f"315.5: {name} and {seen.get(g[name][0])} share the group {g[name][0]!r}, so one drops the other's redraw"
        seen[g[name][0]] = name
    for name in ("bot's edit of issue #40", "command in an issue comment"):
        assert g[name][0] != g["owner's edit of issue #40"][0], \
            f"315.5: the {name} waits in the group {g[name][0]!r} of a redraw of issue #40, so it cancels that redraw"
        groups_of_redraws = {g[r][0]: r for r in redraws + ["criteria checks on PR #5"]}
        assert g[name][0] not in groups_of_redraws, \
            f"315.5: {name} draws nothing but waits in the group {g[name][0]!r} of the redraw of " \
            f"{groups_of_redraws.get(g[name][0])}, so it cancels that redraw"
