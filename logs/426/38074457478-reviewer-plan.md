# reviewer (plan) for #426

Run: https://github.com/dokima-dev/dokima/actions/runs/38074457478

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #426: Every Dokima run records the GitHub API budget left before and after it
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [427], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/426
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #427
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #368, story 1</summary>
> 
> **Part of:** #368 Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> **User story:** The owner can see what each Dokima run cost in GitHub's hourly API budget, GraphQL and REST, so the heaviest workflows are known.
> 
> **Context:** Each run reaches GitHub through gh in several places: dokima/agent.py (about 60 calls), dokima/card.py, dokima/board.py (its own graphql() and rest() helpers at lines 30 to 41), dokima/plan.py (two GraphQL queries at lines 169 and 186), dokima/planner.py, dokima/body.py and dokima/audit.py, plus about 90 gh calls straight from the workflow files in .github/workflows/. `gh issue view`, `gh pr view` and `gh pr list` use GraphQL under the hood. GitHub's `GET /rate_limit` reports both budgets (resources.graphql and resources.core) and does not itself count against either. The budget is shared by every workflow running at once, so 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_budget.py tests/test_budget_record.py tests/test_budget_workflows.py; head -30 .github/workflows/planner.yml .github/workflows/worker.yml
```

> <persisted-output>
> Output too large (29.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/eb903684-00d2-409d-86e9-c4f5ddd02818/tool-results/bl2bz5gkz.txt
> 
> Preview (first 2KB):
> commit a0550b816016785bd6b036f11a2e7d8e5091b65d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:06:27 2026 +0000
> 
>     planner for #426 (run 38073945676)
> 
>  tests/test_budget.py           | 161 +++++++++++++++++++++++++++++++
>  tests/test_budget_record.py    | 121 ++++++++++++++++++++++++
>  tests/test_budget_workflows.py | 209 +++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 491 insertions(+)
> """Tests for #426: every run records the GitHub API budget left before and after it.
> 
> These run `python3 -m dokima.budget before|after KEY FILE` the way a workflow step runs it, against a fake `gh` put
> first on PATH. The fake answers `gh api rate_limit` with GitHub's own shape (resources.graphql and resources.core),
> or refuses the way gh does (GitHub's reason on stderr, exit 1), and logs every call it gets so a test can see the
> command spent nothing but the free rate-limit read. Each reading goes to the step's log (stdout) and, as one JSON
> line, to FILE, the small file the workflow keeps with the run.
> """
> import datetime
> import json
> import os
> import re
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> 
> FAKE_GH = """#!{python}
> import json, os, sys
> with open(os.en

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_budget.py | sed -n 40,200p
```

> bin_dir.mkdir(exist_ok=True)
>     gh = bin_dir / "gh"
>     gh.write_text(FAKE_GH.format(python=sys.executable))
>     gh.chmod(0o755)
>     log = tmp_path / "gh-calls.jsonl"
>     file = tmp_path / "budget.jsonl"
>     env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}", "PYTHONPATH": ROOT,
>            "FAKE_GH_LOG": str(log), "FAKE_GH_ANSWER": answer, "FAKE_GH_FAIL": fail, "GH_TOKEN": "fake-token",
>            "GITHUB_WORKFLOW": "card", "GITHUB_RUN_ID": "4242", "GITHUB_REPOSITORY": "acme/widgets"}
>     env.pop("PYTHONSAFEPATH", None)
>     if not fail:
>         env.pop("FAKE_GH_FAIL")
>     r = subprocess.run([sys.executable, "-m", "dokima.budget", moment, key, str(file)], cwd=str(tmp_path), env=env,
>                        capture_output=True, text=True, timeout=30)
>     entries = [json.loads(l) for l in file.read_text().splitlines() if l.strip()] if file.exists() else []
>     calls = [json.loads(l) for l in log.read_text().splitlines() if l.strip()] if log.exists() else []
>     return r.returncode, r.stdout + r.stderr, entries, calls
> 
> 
> def number(n):
>     """A number as the log may write it: 4321 or 4,321."""
>     s = str(n)
>     return rf"{s[:-3]},?{s[-3:]}" if len(s) > 3 else s
> 
> 
> def test_a_reading_before_the_run_goes_to_the_log_and_the_file(tmp_path, record_property):
>     """A run's budget before it starts shows in its log and its kept file.
> 
>     Proves 426.2.
> 
>     Runs the budget command for `before` with the Dokima app's key against a fake GitHub that has 4,321 G

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_budget_record.py
```

> """Tests for #426: an agent run's record shows the API budget before and after it.
> 
> agent.yml reads the Dokima app's budget into OUT/budget.jsonl (one JSON line per reading, written by
> `python3 -m dokima.budget`) before the run and again once the agent has finished, before the record is written.
> These run the workflow's own record commands (`python3 -m dokima.agent record` and `not-started`) on such a file and
> check the JSON record holds the four numbers and the footnote under the card shows them.
> """
> import json
> import os
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> REPO = "acme/widgets"
> 
> 
> def reading(moment, graphql=None, rest=None, error=None):
>     """One line of the budget file, as `python3 -m dokima.budget` writes it."""
>     e = {"workflow": "agent", "run": "42", "time": "2026-10-10T18:00:00Z", "key": "app", "moment": moment}
>     if error:
>         e["error"] = error
>     else:
>         e.update(graphql=graphql, rest=rest)
>     return json.dumps(e)
> 
> 
> def make_out(tmp_path, lines):
>     """A hand-back folder holding a passed plan and the budget readings; returns (out, logs)."""
>     out, logs = tmp_path / "out", tmp_path / "logs"
>     out.mkdir()
>     logs.mkdir()
>     (out / "plan.json").write_text(json.dumps({"kind": "user_story", "summary": "A plan.", "user_story": "A story.",
>                                                "acceptance_criteria": [], "non_functional": [], "scope": [],
>                                         

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_budget_workflows.py
```

> """Tests for #426: every workflow calling GitHub's API reads the budget before and after.
> 
> These read the workflow files with the repo's own YAML reader (tests/test_start.py's load_yaml, no YAML library).
> A job calls GitHub's API when any of its steps is given GH_TOKEN. Each such job must run
> `python3 -m dokima.budget before KEY FILE` before its first call and `python3 -m dokima.budget after KEY FILE` after
> its last, even when a step failed, and keep FILE with the run as an artifact. KEY is `app` when the job holds the
> Dokima app's key and `github-token` when it only holds the repo's own GITHUB_TOKEN, which has a budget of its own.
> The command itself, and what it writes, is proven in tests/test_budget.py.
> """
> import os
> import re
> import shlex
> import sys
> 
> import pytest
> 
> HERE = os.path.dirname(os.path.abspath(__file__))
> ROOT = os.path.abspath(os.path.join(HERE, ".."))
> sys.path.insert(0, HERE)
> import test_start as ts  # noqa: E402
> 
> WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
> NAMED = ["agent.yml", "assign.yml", "audit.yml", "autopilot.yml", "board.yml", "card.yml", "commands.yml",
>          "done-whens.yml", "planner.yml", "worker.yml", "uptodate.yml"]
> BUDGET = re.compile(r"python3\s+(?:-m\s+dokima\.budget|\S*dokima/budget\.py)\s+(.*)")
> APP_TOKEN = re.compile(r"^\$\{\{\s*steps\.([\w-]+)\.outputs\.token\s*\}\}$")
> 
> 
> def load(name):
>     """One workflow file, read."""
>     return ts.load_yaml(open(os.path.join(WORKFLOWS, name)).read())
> 
> 
> def token(step):
>     """The GH_TOKEN a

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_budget.py tests/test_budget_record.py tests/test_budget_workflows.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|426\.[0-9]:" | head -60
```

> >       assert code == 0, f"426.2: the budget command failed (exit {code}):\n{log[-800:]}"
> E       AssertionError: 426.2: the budget command failed (exit 1):
> >       assert code == 0, f"426.2: the budget command failed after the run (exit {code}):\n{log[-800:]}"
> E       AssertionError: 426.2: the budget command failed after the run (exit 1):
> >       assert code == 0, f"426.3: a budget GitHub would not give must not fail the run, but the command exited {code}:\n{log}"
> E       AssertionError: 426.3: a budget GitHub would not give must not fail the run, but the command exited 1:
> >       assert code == 0, f"426.3: an unreadable answer must not fail the run, but the command exited {code}:\n{log}"
> E       AssertionError: 426.3: an unreadable answer must not fail the run, but the command exited 1:
> >       assert code == 0, f"426.4: the budget command failed (exit {code}):\n{log[-800:]}"
> E       AssertionError: 426.4: the budget command failed (exit 1):
> >       assert got == want, f"426.1: the JSON record should hold budget.before and budget.after with both numbers; got {b}"
> E       AssertionError: 426.1: the JSON record should hold budget.before and budget.after with both numbers; got {}
>             f"426.1: the not-started record should hold the budget before and after; it holds {b}"
> E       AssertionError: 426.1: the not-started record should hold the budget before and after; it holds {}
>             f"426.3: the JSON record should keep GitHub's reason for the budget before; it hol

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -l "GH_TOKEN" .github/workflows/*.yml; grep -n "GH_TOKEN\|GITHUB_TOKEN\|github.token" .github/workflows/{full-suite,reviews,wiki}.yml; grep -n "^name:" .github/workflows/*.yml | head -20; grep -n "def footnote\|def cmd_not_started\|not-started\|def not_started" dokima/agent.py | head
```

> .github/workflows/assign.yml
> .github/workflows/autopilot.yml
> .github/workflows/audit.yml
> .github/workflows/agent.yml
> .github/workflows/board.yml
> .github/workflows/commands.yml
> .github/workflows/card.yml
> .github/workflows/planner.yml
> .github/workflows/done-whens.yml
> .github/workflows/worker.yml
> .github/workflows/uptodate.yml
> .github/workflows/wiki.yml:16:          TOKEN: ${{ github.token }}
> .github/workflows/assign.yml:1:name: assign
> .github/workflows/audit.yml:1:name: audit
> .github/workflows/autopilot.yml:1:name: autopilot
> .github/workflows/card.yml:1:name: card
> .github/workflows/commands.yml:1:name: commands
> .github/workflows/agent.yml:1:name: agent
> .github/workflows/planner.yml:1:name: planner
> .github/workflows/reviews.yml:1:name: reviews
> .github/workflows/done-whens.yml:1:name: done-whens
> .github/workflows/board.yml:1:name: board
> .github/workflows/worker.yml:1:name: worker
> .github/workflows/uptodate.yml:1:name: uptodate
> .github/workflows/wiki.yml:1:name: wiki
> .github/workflows/full-suite.yml:1:name: full suite
> 418:def not_started(role, stage, why, meta):
> 421:    return {"role": "not-started", "attempt": role or "command", "stage": stage or None, **meta, "handback": {},
> 639:    if role == "not-started":
> 795:def footnote(rec):
> 1814:    if role == "not-started":
> 1989:    agent not-started ROLE STAGE OUT WHY_FILE  (the same, for a run or command that failed before its agent started) |
> 2037:    if argv[1] == "not-started":
> 2122:        d, items = ({}, []) if rec.get("role") in 

**Agent:** Still grading the plan for #426: the new tests all fail today for the right reason. Now checking the not-started record's footnote and the planner's raised issue.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; d=$(mktemp -d); mkdir $d/out; echo "why" > $d/why; PYTHONPATH=. GITHUB_SERVER_URL=https://github.com GITHUB_REPOSITORY=a/b GITHUB_RUN_ID=1 python3 -m dokima.agent not-started worker "" $d/out $d/why; tail -2 $d/out/comment.md; sed -n 1,25p .github/workflows/planner.yml
```

> <sub>No agent ran · [run](https://github.com/a/b/actions/runs/1)</sub>
> name: planner
> run-name: "planner for #${{ github.event.issue.number }}${{ github.event.label.name != 'plan' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> # Adding the `plan` label to an issue starts the planner: a fresh GitHub machine
> # reads the repo and the issue, and the planner hands back a plan with its tests,
> # its questions for the owner listed inside it. Only a code owner's label counts. The planner
> # holds no GitHub key: code checks what it handed back, and only then writes the
> # plan into the issue and pushes the tests to work/issue-N.
> on:
>   issues:
>     types: [labeled]
> concurrency:
>   group: plan-${{ github.event.issue.number }}-${{ github.event.label.name }}
>   cancel-in-progress: true
> permissions:
>   contents: read
>   issues: read
> jobs:
>   plan:
>     environment: keys
>     if: github.event.label.name == 'plan'
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           fetch-depth: 0

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three criteria and one non-functional requirement, matching story 1 of #368, with ten tests across three new test files.",
          "It raised one issue outside this one: planner.yml and worker.yml still start the old label-driven agents."],
  "decided": ["A new command, python3 -m dokima.budget before|after KEY FILE, reads the budget with the one free call gh api rate_limit and writes one JSON line per reading; the key is app or github-token.",
              "An agent's footnote shows GraphQL and REST as before → after, and its JSON record holds them under budget.before and budget.after, read from $OUT/budget.jsonl."],
  "open": ["Calls agent.yml makes after the record is written show only in the job's log and file, not in the record."]},
 "verdict": "approve",
 "summary": "The plan covers every ask of story 1 of #368, and all ten new tests fail today because the budget reading does not exist yet.",
 "raises": [],
 "answers": [{"raise": "P1", "answer": "done", "why": "Confirmed: .github/workflows/planner.yml lines 8-20 still start the planner on the plan label (on: issues labeled, if: github.event.label.name == 'plan'), while AGENTS.md's Commands section starts agents with /plan and /work only. It is a real problem outside this issue and worth its own issue."}],
 "asks": [
  {"ask": "Every agent run's record shows the GraphQL and REST budget left before and after the run in its footnote. Its JSON record holds the four numbers.", "source": "https://github.com/dokima-dev/dokima/issues/426", "criterion": "426.1"},
  {"ask": "Every other Dokima workflow run that calls GitHub's API writes both budgets left before and after it to its log and a small file kept with the run.", "source": "https://github.com/dokima-dev/dokima/issues/426", "criterion": "426.2"},
  {"ask": "Each entry names the workflow, the run's time and whose key's budget it is, so story 2 c
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#426](https://github.com/dokima-dev/dokima/issues/426) (every run records the GitHub API budget left before and after it). The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Every ask is covered.** Each of the issue's four asks from story 1 of [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking the API budget per run) maps to a criterion, 426.1 to 426.4. None is missing or narrowed.
- **The tests fail today for the right reason.** I ran all 10 new tests and they all fail:
  - The `dokima.budget` command doesn't exist yet, so those tests exit 1.
  - The agent's JSON record has no `budget` field yet.
  - None of the 11 named workflows reads the budget yet.

  None fails on a crash or a bad path.
- **The tests break on deviation.** They cover a reading GitHub gives, one it refuses with its reason, and an answer that isn't a budget at all. They also check:
  - Only `gh api rate_limit` is called, so measuring spends no budget.
  - The key label is right for each job.
  - The reading after a run happens even when a step failed.
  - The file is uploaded with the run, and no artifact name repeats within one run.
  - In `agent.yml`, a reading falls between the agent finishing and the record being written.
- **The planner's raise P1 is confirmed.** `.github/workflows/planner.yml` (and, per the planner, `worker.yml`) still start the old label-driven agents on the `plan` and `work` labels. AGENTS.md no longer describes that path, so it's worth its own issue.

I raised no blockers. One limit is in the plan's Out of scope list: in `agent.yml`, the calls made after the record is written (posting it, the board, starting the next stage) appear only in the job's log and file, not in the record.
