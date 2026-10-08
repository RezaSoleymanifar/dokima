# reviewer (plan) for #241

Run: https://github.com/dokima-dev/dokima/actions/runs/37851588001

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (72.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d9b895d2-6631-4afe-aa0a-3aefabb1092a/tool-results/bqmodze3t.txt
> 
> Preview (first 2KB):
> .:
> total 92
> drwxr-xr-x  3 runner runner  4096 Oct  8 22:09 .
> drwxrwxrwt 18 root   root    4096 Oct  8 22:09 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 22:09 in
> -rw-r--r--  1 runner runner 69011 Oct  8 22:09 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 22:09 open_blockers.json
> -rw-r--r--  1 runner runner  4650 Oct  8 22:09 plan.json
> 
> in:
> total 52
> drwxr-xr-x 2 runner runner 4096 Oct  8 22:09 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 22:09 ..
> -rw-r--r-- 1 runner runner 5526 Oct  8 22:09 01-planner.json
> -rw-r--r-- 1 runner runner 5255 Oct  8 22:09 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5121 Oct  8 22:09 03-planner.json
> -rw-r--r-- 1 runner runner 3977 Oct  8 22:09 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2055 Oct  8 22:09 05-worker.json
> -rw-r--r-- 1 runner runner 1979 Oct  8 22:09 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5277 Oct  8 22:09 07-planner.json
> # Issue #241: The planner hands back no concerns or replies, keeps its questions, and holds at most five criteria per story
> 
> <!-- dokima-card -->
> The planner's hand-back drops concerns and replies, keeps its questions, and is capped at five criteria per story.
> 
> **Plan**
> 
> [PR #255](https://github.com/dokima-dev/dokima/pull/255) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; grep -n "^## \|^### \|^\*\*.*\*\* commented\|^---" issue.md | head -80; wc -l issue.md
```

> {
>  "kind": "user_story",
>  "summary": "The planner's hand-back drops concerns and replies, keeps its questions, and is capped at five criteria per story.",
>  "user_story": "The owner sees the planner's plan and its questions, with no concerns or replies to read past, and never a story too big to land in one go.",
>  "acceptance_criteria": [
>   {
>    "text": "A planner hand-back carrying a concerns field, even an empty one, is rejected, saying \"a doubt about the ask goes in as a question\". This holds for a user story and a split, and the reason names concerns. The planner's prompt no longer offers a concerns field or a concern example and says a doubt goes in as a question; AGENTS.md's Planner line says the same instead of \"raises a concern\".",
>    "source": "https://github.com/dokima-dev/dokima/issues/241"
>   },
>   {
>    "text": "A planner hand-back carrying a replies field, even an empty one, is rejected, saying \"replies are no longer part of a plan\". This holds for a user story and a split. The planner's prompt no longer mentions replies.",
>    "source": "https://github.com/dokima-dev/dokima/issues/241"
>   },
>   {
>    "text": "A later-round plan or split with no replies passes both the planner check and its round check while the newest review's blockers are open. The round check is `agent check-round planner`. The reviewer's round check still passes a review that resolves or keeps each open blocker, and rejects one that drops any, naming it.",
>    "source": "https://github.com/dokim

`3. Bash`
```
cd /tmp/pack; sed -n 1,72p issue.md | grep -v "^<td\|^<tr\|^</t" | tail -40; sed -n 390,400p issue.md; sed -n 685,700p issue.md; sed -n 840,860p issue.md; sed -n 1000,1013p issue.md
```

> - The reviewer's prompt and the plan grade are left as they are; reviewer.md still reads the worker's replies.
> - The sample tests/samples/132/plan.json loses its concerns field in this plan's tests, so the real sample still passes the new check; nothing else in it changes.
> - The word caps and docstring rules #246 added to the planner check stay as they are; this plan's tests follow them.
> 
> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37851455881/job/113565088723"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/running.svg" width="16" height="16" align="absmiddle" alt="running"></a> All tests · <a href="https://github.com/dokima-dev/dokima/actions/runs/37832626249"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8; git diff main --stat; cat /tmp/pack/in/07-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]);print(d.keys())"
```

> cc8ced3 Merge branch 'main' into try/issue-241
> 61e0b7e Open PRs are brought up to date after every merge to main (#267)
> 4ff0278 Every field on a card has its own GitHub icon, fixed by code (#248)
> 2cce556 Merge branch 'main' into try/issue-241
> 7961d88 The planner's criteria and docstrings stay short, and a little over the cap never fails a run (#246)
> 50765e4 The owner's ask reads open on the issue they wrote (#249)
> ab2dcaa The all tests check runs main's copy of its workflow, so a pull request can't rewrite its own judge (#263)
> 79e34d6 planner for #244 (run 37827165425) (#266)
>  AGENTS.md                      |   2 +-
>  dokima/agent.py                |   5 +-
>  dokima/planner.py              |  12 +++
>  dokima/roles/planner.md        |  16 ++--
>  tests/samples/132/plan.json    |  16 +---
>  tests/test_agent.py            |   7 +-
>  tests/test_fixer.py            |   5 +-
>  tests/test_plan_shape.py       |   5 +-
>  tests/test_planner_handback.py | 189 +++++++++++++++++++++++++++++++++++++++++
>  9 files changed, 223 insertions(+), 34 deletions(-)
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37849696922",
>  "commit_before": "2cce556c2ad686a926533cc603292d7108b6a951",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 952361,
>   "turns": 21,
>   "cost_usd": 0.9197844000000001,
>   "tokens_in": 1205064,
>   "tokens_out": 9657
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/241/37849696922-planner.md",
>  "run": "https://github.com

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main -- dokima/ AGENTS.md tests/test_agent.py tests/test_fixer.py tests/test_plan_shape.py tests/samples; python3 -m pytest -q 2>&1 | tail -15
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bndp1f7ot). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b895d2-6631-4afe-aa0a-3aefabb1092a/tasks/bndp1f7ot.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Reviewing the plan for #241: running the full test suite in the background while I read the diff and the planner's tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main -- dokima/ AGENTS.md tests/test_agent.py tests/test_fixer.py tests/test_plan_shape.py tests/samples
```

> diff --git a/AGENTS.md b/AGENTS.md
> index 12e534a..f818774 100644
> --- a/AGENTS.md
> +++ b/AGENTS.md
> @@ -39,7 +39,7 @@ GitHub is the office: issues are the tasks, pull requests are the work, comments
>  ## Roles
>  
>  - **Owner:** decides. Approves plans and results, routes proposals. Only a code owner's commands count.
> -- **Planner:** turns a rough issue into a plan: an objective, acceptance criteria, scope, and a test for every criterion written before any code. It judges the ask first and raises a concern only with evidence. It may change or delete an older test when the plan makes it wrong, with a reason the owner sees. It proposes splits; it never writes code.
> +- **Planner:** turns a rough issue into a plan: an objective, acceptance criteria, scope, and a test for every criterion written before any code. It judges the ask first; a doubt about the ask goes in as a question, with evidence. It may change or delete an older test when the plan makes it wrong, with a reason the owner sees. It proposes splits; it never writes code.
>  - **Worker:** builds what the approved plan says, on a fresh machine, within scope, until its tests pass. It never changes the plan's tests.
>  - **Reviewer:** checks the plan, then the result (a real PR review). It blocks only on a promise with no proof or a proof that proves nothing, and ends with a list of proposed issues.
>  - **Code:** everything that must be exact (see the principles).
> diff --git a/dokima/agent.py b/dokima/agent.py
> index 4e27c78..3d50250 1

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_planner_handback.py; git log --oneline main..HEAD | head; git log --format='%h %s' -5 -- tests/test_planner_handback.py
```

> """The planner hands back no concerns or replies, keeps its questions, and holds at most five criteria per story (#241).
> 
> The owner asked (story 3 of #229) that a doubt about the ask go in as a question, not a concern; that the planner stop
> answering blockers with replies, since the reviewer already resolves or keeps each one itself; that questions keep
> reaching the owner; and that a story with more than five criteria be split. Every check here runs the way the planner
> workflow runs it: `planner check` through planner.main inside a temp git repo (the `check` fixture of
> tests/test_plan_check.py), then `python3 -m dokima.agent check-round planner FILE PACK` on a starting pack built in a
> temp folder. The card is drawn with agent.render, the code that writes every record comment.
> """
> import copy
> import json
> import os
> import re
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent  # noqa: E402
> from tests.test_plan_check import FEATURE, ISSUE, STORY, check  # noqa: E402,F401
> from tests.test_run_cards import rec, top  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> QUESTIONS = [{"question": "Should job ids be numbers?", "assumption": "The plan assumes they are strings."},
>              {"question": "Should a failed run move to Needs you?", "assumption": "The plan assumes it does."}]
> BLOCKERS = [{"id": "B1", "criterion": "9.1", "test": None, "problem": "p", "evidence"

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 41303e2 HEAD -- tests/test_planner_handback.py | head -60; git show --stat HEAD | head -30; python3 -c "
import json;d=json.load(open('/tmp/pack/in/07-planner.json'));h=d['handback'];print(json.dumps({k:v for k,v in h.items() if k not in ('acceptance_criteria',)},indent=1)[:2500])"
```

> commit cc8ced391b0d34ebf0903394cd38261a291cca50
> Merge: 2cce556 61e0b7e
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 22:07:31 2026 +0000
> 
>     Merge branch 'main' into try/issue-241
> 
>  .github/workflows/uptodate.yml        |  31 +++
>  dokima/agent.py                       |  50 ++--
>  dokima/card.py                        |  33 ++-
>  dokima/icons/acceptance-criterion.svg |   1 +
>  dokima/icons/autopilot.svg            |   1 +
>  dokima/icons/blocked-by.svg           |   1 +
>  dokima/icons/blocker.svg              |   1 +
>  dokima/icons/blocks.svg               |   1 +
>  dokima/icons/code-review.svg          |   1 +
>  dokima/icons/files-changed.svg        |   1 +
>  dokima/icons/issue-found.svg          |   1 +
>  dokima/icons/merged.svg               |   1 +
>  dokima/icons/needs-you.svg            |   1 +
>  dokima/icons/note.svg                 |   1 +
>  dokima/icons/outside-the-plan.svg     |   1 +
>  dokima/icons/owner-approval.svg       |   1 +
>  dokima/icons/plan-review.svg          |   1 +
>  dokima/icons/planner.svg              |   1 +
>  dokima/icons/question.svg             |   1 +
>  dokima/icons/related.svg              |   1 +
>  dokima/icons/stats.svg                |   1 +
>  dokima/icons/still-open.svg           |   1 +
>  dokima/icons/verified-by.svg          |   1 +
> {
>  "kind": "user_story",
>  "summary": "The planner's hand-back drops concerns and replies, keeps its questions, and is capped at five criteria per story.",
>  "user_story": "Th

`9. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b895d2-6631-4afe-aa0a-3aefabb1092a/tasks/bndp1f7ot.output | tail -15
```

> -    example per rule (user story, feature, bug fix, non-functional, scope, docstring, question, concern).
> +    example per rule (user story, feature, bug fix, non-functional, scope, docstring, question). Concerns are gone
> +    (#241): a doubt about the ask goes in as a question.
>      """
>      record_property("proves", "138.1")
>      for term in ["User story", "Feature", "Acceptance criteria", "Non-functional requirements", "Definition of Done",
> @@ -42,7 +43,7 @@ def test_prompt_teaches_the_terms_voice_and_every_example(record_property):
>                       "A rejected plan never fails silently", "Repos without a board are left alone"]:
>          assert approved in PROMPT, f"138.1: the owner's approved example is missing: {approved!r}"
>      for rule in ["- User story:", "- Feature:", "- Bug fix as a criterion:", "- Non-functional with reason",
> -                 "- Scope:", "- Test docstring:", "- Question:", "- Concern:"]:
> +                 "- Scope:", "- Test docstring:", "- Question:"]:
>          assert rule in PROMPT, f"138.1: no example for {rule!r}"
>      assert "Objective:" not in PROMPT and "Non-goals:" not in PROMPT, "138.1: the prompt still uses Objective or Non-goals"

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_planner_handback.py tests/test_agent.py::test_each_round_answers_every_open_blocker tests/test_fixer.py tests/test_plan_shape.py 2>&1 | tail -30
```

> ..........F....................                                          [100%]
> =================================== FAILURES ===================================
> _ test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it[story] _
> 
> record_property = <function record_property.<locals>.append_property at 0x7f19c744cc20>
> check = <function check.<locals>.run at 0x7f19c744ccc0>
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_story_with_more_than_fi0')
> base = {'kind': 'user_story', 'summary': 'Slow calls hand back a job id instead of timing out.', 'user_story': 'Slow calls re...r/issues/9'}, {'text': 'Job ids never repeat.', 'source': 'https://github.com/o/r/issues/9#issuecomment-123456'}], ...}
> story = 1
> 
>     @pytest.mark.parametrize("base,story", [(STORY, 1), (FEATURE, 1), (FEATURE, 2)], ids=["story", "split-story-1", "split-story-2"])
>     def test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it(record_property, check, tmp_path, base, story):
>         """A story with more than five criteria, counting non-functional ones, is rejected, saying it should be split.
>     
>         On a first round, hands back a story (or a split whose first or second story is resized) with exactly five criteria, four acceptance
>         and one non-functional, and checks it passes. Then with six, and with seven, and checks each is rejected with a
>         reason saying "more than five criteria" and "split", naming the story for a split."""
>         record_property("pro

`11. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1|tail -1; cp tests/test_planner_handback.py tests/test_agent.py tests/test_fixer.py tests/test_plan_shape.py /tmp/mainwt/tests/; cp tests/samples/132/plan.json /tmp/mainwt/tests/samples/132/; cd /tmp/mainwt; timeout 300 python3 -m pytest -q tests/test_planner_handback.py tests/test_agent.py::test_each_round_answers_every_open_blocker tests/test_fixer.py tests/test_plan_shape.py 2>&1 | grep -E "FAILED|passed|failed" | cut -c1-400
```

> >           assert not ok, f"241.1: a {base['kind']} with concerns {concerns} passed the check"
> E           AssertionError: 241.1: a user_story with concerns [{'text': 'This overlaps #12.', 'evidence': 'dokima/board.py'}] passed the check
> >           assert not ok, f"241.1: a {base['kind']} with concerns {concerns} passed the check"
> E           AssertionError: 241.1: a feature with concerns [{'text': 'This overlaps #12.', 'evidence': 'dokima/board.py'}] passed the check
> >           assert not ok, f"241.2: a {base['kind']} with replies {replies} passed the check"
> E           AssertionError: 241.2: a user_story with replies [{'blocker': 'B1', 'answer': 'fixed', 'why': 'Fixed it.'}, {'blocker': 'B2', 'answer': 'fixed', 'why': 'Fixed it.'}] passed the check
> >           assert not ok, f"241.2: a {base['kind']} with replies {replies} passed the check"
> E           AssertionError: 241.2: a feature with replies [{'blocker': 'B1', 'answer': 'fixed', 'why': 'Fixed it.'}, {'blocker': 'B2', 'answer': 'fixed', 'why': 'Fixed it.'}] passed the check
> >           assert not ok, f"241.5: a {base['kind']} with {n} criteria (story {story}) passed the check"
> E           AssertionError: 241.5: a feature with 6 criteria (story 1) passed the check
> >           assert not ok, f"241.5: a {base['kind']} with {n} criteria (story {story}) passed the check"
> E           AssertionError: 241.5: a feature with 6 criteria (story 2) passed the check
> FAILED tests/test_planner_handback.py::test_a_plan_with_concerns

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def check\|test_jobs\|Proves\|9\.\d" tests/test_plan_check.py | head -30; git worktree remove --force /tmp/mainwt
```

> 26:NEW_TESTS = ('def test_id(record_property):\n    """A slow call returns a job id.\n\n    Proves 9.1.\n    """\n'
> 27:             '    record_property("proves", "9.1")\n    assert False, "9.1: no job id yet"\n\n\n'
> 28:             'def test_unique(record_property):\n    """Job ids never repeat.\n\n    Proves 9.2 and 9.3.\n    """\n'
> 29:             '    record_property("proves", "9.2")\n    assert False, "9.2: no job ids yet"\n')
> 36:         "tests": {"9.1": ["tests/test_jobs.py::test_id"], "9.2": ["tests/test_jobs.py::test_unique"],
> 37:                   "9.3": ["tests/test_jobs.py::test_unique"]},
> 49:def check(tmp_path, monkeypatch):
> 69:    (repo / "tests" / "test_jobs.py").write_text(NEW_TESTS)
> 214:@pytest.mark.parametrize("name", ["tests/test_jobs.py::test_ghost", "tests/test_nowhere.py::test_id"],
> 223:    rc, why = check({"plan.json": story(lambda s: s["tests"]["9.1"].append(name))}, "154.3")
> 229:    ("139.1", "tests/test_jobs.py::test_id"),
> 230:    ("9.4", "tests/test_jobs.py::test_id"),
> 231:    ("139.1", "tests/test_old.py::test_old"),
> 232:    ("9.4", "tests/test_old.py::test_old"),
> 237:    Files a new test, then an older test, under another issue's number (139.1) and under 9.4 (past the last of the
> 255:    rc, why = check({"plan.json": story(lambda s: s["tests"].update({"9.3": ["tests/test_old.py::test_old"]}))}, "154.4")
> 256:    assert "9.3 has no test" not in why, f"154.4: a criterion proven by an older test was called 'has no test': {why!r}"
> 257:    assert rc == 

**Agent:** Found the key problem (241.5's test still fails for the wrong reason); checking the test fixture so I can name the smallest fix.

`13. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 45,90p tests/test_plan_check.py
```

> "non_functional": [], "depends_on": [0]}]}
> 
> 
> @pytest.fixture
> def check(tmp_path, monkeypatch):
>     """A function that hands back the given files and runs the check on issue #9: returns (exit code, reason).
> 
>     Each call empties the hand-back folder first, so one test can run the check on a good plan and then a broken one.
>     """
>     repo, out = tmp_path / "repo", tmp_path / "out"
>     repo.mkdir()
>     out.mkdir()
>     git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True).stdout
>     git("init", "-q")
>     git("config", "user.name", "t")
>     git("config", "user.email", "t@t")
>     (repo / "tests").mkdir()
>     (repo / "tests" / "test_old.py").write_text(OLD_TESTS)
>     git("add", "-A")
>     git("commit", "-qm", "base")
>     # The planner's run starts at this commit too, so the check sees the new tests as its own (as a real run does).
>     monkeypatch.setenv("PLANNER_BASE", git("rev-parse", "HEAD").strip())
>     monkeypatch.setenv("PLANNER_RUN_BASE", git("rev-parse", "HEAD").strip())
>     monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
>     (repo / "tests" / "test_jobs.py").write_text(NEW_TESTS)
>     monkeypatch.chdir(repo)
> 
>     def run(files, crit):
>         for old in out.iterdir():
>             old.unlink()
>         for name, content in files.items():
>             (out / name).write_text(content if isinstance(content, str) else json.dumps(content))
>         try:
>             rc = planner.main(["x", "check", "9", str(out)])
>         except Exception a

`14. Bash`
```
cd /tmp/pack; grep -o "issuecomment-[0-9]*" issue.md | sort -u | head; grep -n "issuecomment" issue.md | head -5 | cut -c1-200; cat in/04-reviewer-plan.json | python3 -c "import json,sys;print(json.dumps(json.load(sys.stdin)['handback']['asks'],indent=1))"
```

> [
>  {
>   "ask": "A planner hand-back with concerns is rejected, saying a doubt about the ask goes in as a question.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.1"
>  },
>  {
>   "ask": "AGENTS.md's Roles line 'raises a concern only with evidence' changes with this story: the owner said a doubt about the ask goes in as a question.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.1"
>  },
>  {
>   "ask": "Yes, this issue asks you to change dokima/roles/planner.md: dropping concerns and replies from the planner's hand-back means removing them from its prompt.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.1"
>  },
>  {
>   "ask": "A planner hand-back with replies is rejected, saying replies are no longer part of a plan.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.2"
>  },
>  {
>   "ask": "A later-round plan with no replies passes, and the reviewer still resolves or keeps each open blocker.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.3"
>  },
>  {
>   "ask": "A plan's questions still pass the check and still reach the owner on its card.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.4"
>  },
>  {
>   "ask": "A story with more than five criteria is rejected, saying it should be split.",
>   "source": "https://github.com/dokima-dev/dokima/issues/241",
>   "criterion": "241.5"
>  },
>  {
>   "ask": 

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner handed back the same five criteria and the same tests as its last plan, on today's main.",
          "It added an out-of-scope line saying the word caps and docstring rules from #246 stay and its tests follow them."],
  "decided": ["The plan keeps every ask of the issue and changes no test file in this round."],
  "open": ["Test 241.5 still fails on a story with exactly five criteria, for the docstring rule from #246, not for the missing cap."]},
 "verdict": "block",
 "summary": "The owner asked for a re-plan because test 241.5 broke after #246, but the plan hands back the same test, and it still fails on a correct build for the same reason.",
 "blockers": [{"id": "B3", "criterion": "241.5",
   "test": "tests/test_planner_handback.py::test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it",
   "problem": "The owner asked to re-plan on today's main because 241.5's test fails once #255 is up to date. The test is unchanged: its good case, a user story with exactly five criteria, is rejected by the #246 rule that every new test's docstring names each criterion it proves. So the test fails on the worker's finished code as well as on main, and no build can ever turn it green.",
   "evidence": "Owner's comment of 2026-10-08T21:51:43Z on #241: 'Re-plan on today's main: #246 merged changes to the same planner check, and test 241.5 now fails on PR #255 once it is brought up to date.' git diff 41303e2 HEAD -- tests/test_planner_handback.py is empty. On this branch, which holds #255's code merged with main: `pytest -q tests/test_planner_handback.py` gives 1 failed, [story] case: '241.5: a user_story with exactly five criteria was rejected: tests/test_jobs.py::test_unique is a new test whose docstring does not name 9.4 ... 9.5'. sized() in tests/test_planner_handback.py files 9.2 to 9.5 under tests/test_jobs.py::test_unique, whose docstring in tests/test_
```

> rc=0

`16. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b895d2-6631-4afe-aa0a-3aefabb1092a/tasks/bndp1f7ot.output
```

> -                 "- Scope:", "- Test docstring:", "- Question:", "- Concern:"]:
> +                 "- Scope:", "- Test docstring:", "- Question:"]:
>          assert rule in PROMPT, f"138.1: no example for {rule!r}"
>      assert "Objective:" not in PROMPT and "Non-goals:" not in PROMPT, "138.1: the prompt still uses Objective or Non-goals"

**Agent:** I've blocked the plan for #241. The owner asked for a re-plan because test 241.5 broke after #246 merged, and the planner handed back the same test unchanged. It still fails for the same reason.

**What the planner did:** It kept the same five criteria and the same tests, and added one out-of-scope line saying #246's rules stay and its tests follow them. The test file is the same as in the first plan.

**Blocker B3 (criterion 241.5, the planner fixes it):**
- **The failure:** I ran the plan's tests on this branch, which already holds the worker's code from PR #255 brought up to date with main. 30 passed and 1 failed: the user-story case of `test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it`.
- **Why it fails:** That case first checks that a story with exactly five criteria passes. The check rejects it instead, because #246 requires every new test's description to name each criterion it proves. The test files 9.2 to 9.5 under a stand-in test that only names 9.2 and 9.3 (`tests/test_plan_check.py:28`).
- **What that means:** This test can never pass, however good the code is. It fails on main for the same wrong reason, not because the five-criteria cap is missing.
- **Smallest fix:** In `sized()`, file criteria 9.4 and up under the older stand-in test `tests/test_old.py::test_old`, which the check already accepts for 9.3 (`tests/test_plan_check.py:255`). Then confirm the case passes on this branch and still fails on main because the cap is missing.

**Everything else holds:** The other new tests fail on main for the right reason (the feature is missing) and pass on this branch. All nine of the owner's asks map to a criterion, including the re-plan comment, which maps to 241.5. The plan has no questions, so there were no assumptions to judge.

The full test suite was still running when I finished, so I have no result for it. The hand-back is `/tmp/dokima-out/review.json`, and both required checks on it pass.

`17. Bash`
```
grep -E "passed|failed|FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b895d2-6631-4afe-aa0a-3aefabb1092a/tasks/bndp1f7ot.output | cut -c1-250
```

> - Question: Should a failed run move its card to Needs you? Assumption: the plan assumes it does, so the owner sees it
>     "tests/test_failed_run_card.py::test_a_run_that_left_nothing_behind_still_marks_its_card"
> -   "text": "Most of this ask already holds on main: a failed planner, worker or code review run already ends in its stage's column with Needs you, through the always-run \"Move the card on the board\" step. The gap left is when \"Decide what follows
> -   "text": "A command that fails in the listener before any agent starts (route failure, split filing refused) posts a failed record that mentions the owner, but never touches the board. That breaks AGENTS.md's rule that Needs you is set exactly whe
> FAILED tests/test_planner_handback.py::test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it[story] - AssertionError: 241.5: a user_story with exactly five criteria was rejected: "tests/test_jobs.py::test_unique is a new test whose do
> 1 failed, 567 passed in 208.19s (0:03:28)

**Agent:** The full test suite has now finished on this branch: 567 passed and 1 failed. The one failure is the same test from the blocker, the user-story case of 241.5. A story with exactly five criteria is still rejected, because the test's stand-in test doesn't name 9.4 and 9.5 in its description.

Nothing else in the repo breaks, so the block stays as it is with the single blocker B3 for the planner. The hand-back in `/tmp/dokima-out/review.json` doesn't need any changes.
