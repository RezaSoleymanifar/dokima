# reviewer (plan) for #417

Run: https://github.com/dokima-dev/dokima/actions/runs/38081128518

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (41.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5090eb29-19b0-4ab3-ab25-a005db472df9/tool-results/bzyn4rfjg.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct 10 19:46 .
> drwxrwxrwt 18 root   root    4096 Oct 10 19:46 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 19:46 in
> -rw-r--r--  1 runner runner 41870 Oct 10 19:46 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 19:46 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 19:46 parent.json
> -rw-r--r--  1 runner runner  3986 Oct 10 19:46 plan.json
> 
> in:
> total 52
> drwxr-xr-x 2 runner runner 4096 Oct 10 19:46 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 19:46 ..
> -rw-r--r-- 1 runner runner 3461 Oct 10 19:46 01-planner.json
> -rw-r--r-- 1 runner runner 3990 Oct 10 19:46 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4554 Oct 10 19:46 03-planner.json
> -rw-r--r-- 1 runner runner 2069 Oct 10 19:46 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2341 Oct 10 19:46 05-worker.json
> -rw-r--r-- 1 runner runner 3557 Oct 10 19:46 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 1964 Oct 10 19:46 07-worker.json
> -rw-r--r-- 1 runner runner 3584 Oct 10 19:46 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4623 Oct 10 19:46 09-planner.json
> # Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 368, 425 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> <persisted-output>
> Output too large (34.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5090eb29-19b0-4ab3-ab25-a005db472df9/tool-results/b8y4eapq6.txt
> 
> Preview (first 2KB):
> # Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 368, 425 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/417 · https://github.com/dokima-dev/dokima/pull/447 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/447/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #429, #368, #380, #425
> 
> **User story:** On autopilot no step is lost silently: when deciding what runs next fails, the record says why, and when GitHub's rate limit ran out the step waits for it to reset and starts what it would have started.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <

**Agent:** Let me find the owner's original text and comments.

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|Original issue\|dokima-ask\|^---" issue.md | head -60; wc -l issue.md
```

> 52:<!-- dokima-ask -->
> 53:<details><summary>Original issue</summary>
> 68:## Comments
> 70:### RezaSoleymanifar on issue #417 (2026-10-10T18:37:20Z)
> 74:### dokima-runtime on issue #417 (2026-10-10T18:37:43Z)
> 78:### dokima-runtime on issue #417 (2026-10-10T18:37:46Z)
> 83:### dokima-runtime on issue #417 (2026-10-10T18:37:55Z)
> 140:### dokima-runtime on issue #417 (2026-10-10T18:43:05Z)
> 184:### dokima-runtime on issue #417 (2026-10-10T18:45:02Z)
> 241:### dokima-runtime on issue #417 (2026-10-10T18:47:26Z)
> 280:### dokima-runtime on issue #417 (2026-10-10T18:49:12Z)
> 285:### dokima-runtime on issue #417 (2026-10-10T18:49:13Z)
> 316:### dokima-runtime on PR #447 (2026-10-10T18:56:25Z)
> 362:### dokima-runtime on PR #447 (2026-10-10T19:04:50Z)
> 386:### RezaSoleymanifar on issue #417 (2026-10-10T19:41:39Z)
> 390:### dokima-runtime on issue #417 (2026-10-10T19:41:58Z)
> 433:### dokima-runtime on issue #417 (2026-10-10T19:43:45Z)
> 490:### dokima-runtime on issue #417 (2026-10-10T19:46:23Z)
> 498 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 52,80p issue.md; sed -n 386,392p issue.md; sed -n 490,498p issue.md | cut -c1-600; cat plan.json; cat parent.json
```

> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> On autopilot the next step sometimes never starts, and nothing says so. Twice on 10-10, both on #301, both between 14:32Z and 15:32Z: after the planner's re-plan (14:58Z) and after the plan review passed (15:12Z).
> 
> Root cause, from the 14:58Z run's log: the step that decides what runs next (`python3 -m dokima.agent next`) failed with "GraphQL: API rate limit already exceeded for installation ID 168252268". The app's GraphQL allowance (5,000 an hour, shared by all of Dokima's workflows) ran out in that hour. agent.yml runs it as `NEXT=$(...) || NEXT=stop`, so the failure became a silent stop: no Next line, no warning, nothing started. Earlier guesses (the raise path from #300) were wrong.
> 
> (Not this bug: #388 stopping on its question for me is by design, and adding the autopilot label alone never starts a planner; /autopilot start does.)
> 
> Done when
> - When deciding what runs next fails, the record says so on the issue in one line, with GitHub's reason, instead of stopping silently.
> - When the failure is GitHub's rate limit, the step is tried again after the limit resets, and starts what it would have started.
> - See #380 and #368 for using less of the allowance; this issue is about never losing a step when it runs out.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #417 (2026-10-10T18:37:20Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #417 (2026-10-10T18:37:43Z)
> 
> Autopilot: switched on, starting plan
> 
> #

`5. Bash`
```
cd /tmp/pack/in; for f in 06* 07* 08* 09*; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f'));print(json.dumps({k:v for k,v in d.items()},indent=1)[:5000])"; done
```

> == 06-reviewer-pr.json
> {
>  "role": "reviewer",
>  "stage": "pr",
>  "run_id": "38077796373",
>  "commit_before": "9397d35b2882febf4088055a49cdcfd1697f6e5d",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 201450,
>   "turns": 18,
>   "cost_usd": 0.7370109999999999,
>   "tokens_in": 921734,
>   "tokens_out": 6534
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/417/38077796373-reviewer-pr.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38077796373",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "Changed `next` so that a GitHub call refused while deciding what runs next stops with GitHub's reason in one Next line that mentions the owner.",
>     "Made a rate-limited call wait once for the reported reset of the limit that ran out (GraphQL or REST), then try again.",
>     "Let the autopilot label read pass GitHub's refusal on, so a refused later read also says GitHub's reason."
>    ],
>    "decided": [
>     "A second rate-limit refusal after the wait stops the step with GitHub's words; it never waits twice."
>    ],
>    "open": [
>     "A failed decision now writes the card's place, so while GitHub still refuses, the card does not show Needs you."
>    ]
>   },
>   "verdict": "block",
>   "summary": "It says GitHub's reason and waits out the rate limit, but a failed decision no longer shows Needs you, breaking a test passing on main.",
>   "raises": [
>    {
>     "kind": "blocker",
>     "to": "worker",
>     "label": "417.3: car

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --stat | head -50; git diff main --stat; echo $PYTHONPATH
```

> d99ad64 planner for #417 (run 38080950433)
>  tests/test_next_rate_limit.py | 49 ++++++++++++++++++++++++++++++++++++++-----
>  1 file changed, 44 insertions(+), 5 deletions(-)
> 190fae3 Merge branch 'main' into try/issue-417
> 566dbf7 When a plan is approved, its pull request's checks run again by themselves (#448)
>  dokima/agent.py                | 102 +++++++---
>  tests/conftest.py              |   1 -
>  tests/test_checks_rerun.py     | 420 +++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_check_rerun.py |  29 +--
>  4 files changed, 494 insertions(+), 58 deletions(-)
> b06ca89 In the merge queue, a pull request's own copy of the checks judges it (#421)
>  .github/workflows/done-whens.yml |   4 +
>  tests/test_queue_judge.py        | 219 +++++++++++++++++++++++++++++++++++++++
>  2 files changed, 223 insertions(+)
> 120fdb5 Merge branch 'main' into try/issue-417
> 8275689 Once a build has started, the card shows Work and no longer asks for /work (#444)
>  dokima/card.py                   |   7 ++-
>  tests/test_build_started_card.py | 117 +++++++++++++++++++++++++++++++++++++++
>  2 files changed, 123 insertions(+), 1 deletion(-)
> 9397d35 worker for #417 (run 38077321070)
>  dokima/agent.py | 169 +++++++++++++++++++++++++++++++++++++-------------------
>  1 file changed, 112 insertions(+), 57 deletions(-)
> c7a131d planner for #417 (run 38077037746)
>  tests/test_next_rate_limit.py | 104 +++++++++++++++++++++++++++++++++++++-----
>  1 file changed, 92 insertions(+), 12 deletions(-)
>  dokima/agent.py       

`7. Bash`
```
cd /home/runner/work/dokima/dokima; PYTHONPATH=. timeout 600 pytest -q tests/test_next_rate_limit.py 2>&1 | tail -30
```

> workflow's board step runs on what the run left behind, with GitHub still refusing reads of the issue, and the
>         issue's card must end in Plan, the planner's column, showing Needs you. A run that only writes 'needs' in its
>         board line, so the board step tries to rebuild the card from GitHub and leaves it as it was, fails here."""
>         record_property("proves", "417.3")
>         printed, text, board, hub, escaped = decide(tmp_path, monkeypatch, capsys, failure, until=float("inf"))
>         assert escaped is None, f"417.3: the error escaped the step, so the record has no Next line: {escaped}"
>         assert printed == "stop", f"417.3: a failed decision printed {printed!r}, not 'stop'"
>         nexts = next_lines(text)
>         assert len(nexts) == 1 and nexts[0].startswith(f"**Next:** @{OWNER}"), \
>             f"417.3: a failed decision's Next lines do not mention the owner once: {nexts!r}"
>         p, card = board_step(tmp_path, tmp_path / "out", failure)
> >       assert card == ("Plan", True), (f"417.3: after a failed decision, with GitHub still refusing, the board step left "
>                                         f"the issue's card at {card} (column, Needs you), not ('Plan', True):\n"
>                                         f"{p.stdout}{p.stderr}")
> E       AssertionError: 417.3: after a failed decision, with GitHub still refusing, the board step left the issue's card at None (column, Needs you), not ('Plan', True):
> E         ::error::Could not read the state of #

**Agent:** Now against main's agent.py.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1|tail -1; cp tests/test_next_rate_limit.py /tmp/mainwt/tests/; cd /tmp/mainwt; PYTHONPATH=. timeout 600 pytest -q tests/test_next_rate_limit.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-400
```

> assert escaped is None, f"417.1: deciding what runs next failed though GitHub answered every call: {escaped}"
> E           "passed": true,
> E           "passed": true,
> E        +  where [] = lines_with('<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w... width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · [run](https://github.com/o/r/actions/runs/1)</sub>\n', 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)')
> _________ test_a_failed_decision_stops_for_the_owner[rate-limit-again] _________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_failed_decision_stops_f0')
>     def test_a_failed_decision_stops_for_the_owner(record_property, tmp_path, monkeypatch, capsys, failure):
> ___________ test_a_failed_decision_stops_for_the_owner[server-error] ___________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_failed_decision_stops_f1')
>     def test_a_failed_decision_stops_for_the_owner(record_property, tmp_path, monkeypatch, capsys, failure):
> E         sercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer passed the plan.
> E           "passed": true,
> FAILED tests/test_next_rate_limit.py::test_a_decision_github_refuses_says_so_in_one_line_with_githubs_reason - AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 225,300p tests/test_next_rate_limit.py; grep -n "board.txt\|board.stopped\|board.rebuild\|undecided" dokima/agent.py | head -30
```

> def board_step(tmp_path, out, failure):
>     """Run the workflow's board step on what `next` left in out.
> 
>     The step is `python3 -m dokima.agent board 57 OUT`.
> 
>     The board step runs right after `next` in agent.yml, in the same hour, so GitHub still refuses reads of the issue
>     (`gh issue view`, `gh pr view` and the issue's REST read) with failure's words; the board's own GraphQL calls are
>     answered by the fake board of tests/test_failed_run_card.py, which records every field set. Returns the step and
>     where the issue's card ended: (Status column, shows Needs you), or None when the step never touched it."""
>     import sys
>     sys.path.insert(0, os.path.dirname(__file__))
>     import test_start as T
>     from test_failed_run_card import GH_EXTRA, board_state
>     root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
>     gh, bin_ = tmp_path / "board-gh", tmp_path / "board-bin"
>     gh.mkdir()
>     bin_.mkdir()
>     refuse = (f'if a[:2] in (["issue", "view"], ["pr", "view"]) or (a[:1] == ["api"] and any(x.split("?")[0].strip("/") '
>               f'== "repos/o/r/issues/{N}" for x in a[1:])):\n'
>               f'    sys.stderr.write({failure + chr(10)!r})\n'
>               f'    sys.exit(1)\n')
>     anchor = 'if a[:2] == ["issue", "view"]:'
>     fake = T.FAKE_GH.replace(anchor, refuse + GH_EXTRA + anchor, 1)
>     (bin_ / "gh").write_text(fake.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
>     os.chmod(bin_ / "gh", 0o755)
>     env = {**os.environ, "PATH":

`10. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 2325,2390p dokima/agent.py
```

> "GitHub answers.")
>         if rec.get("role") == "worker":
>             # The pull request is opened after the record is written, so the worker's sentence links it only now.
>             try:
>                 pr = gh("pr", "list", "-R", repo, "--head", f"try/issue-{number}", "--state", "open", "--json", "number",
>                         "-q", ".[0].number").strip()
>             except subprocess.CalledProcessError:
>                 pr = ""
>             if pr.isdigit():
>                 url = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/pull/{pr}"
>                 open(os.path.join(out, "comment.md"), "w").write(render(rec, url))
>         filed = file_issues(repo, number, rec, records(items))
>         if filed:
>             # The issues filed in this run go on its record, above the full record, whatever GitHub answered.
>             text = open(os.path.join(out, "comment.md")).read()
>             fold = "\n<details><summary>Full record</summary>"
>             at = text.find(fold)
>             at = len(text.rstrip("\n")) if at < 0 else at
>             open(os.path.join(out, "comment.md"), "w").write(text[:at] + "\n".join(filed) + "\n" + text[at:])
>         with open(os.path.join(out, "comment.md"), "a") as f:
>             f.write("\n" + next_line(step, owners) + "\n")
>         if step[3:] == ("autopilot",):
>             # The line the owner would have typed `/work` in place of; the workflow posts it on the issue.
>             open(os.path.join(out, "autopilot.md"), "w").writ

`11. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 2290,2326p dokima/agent.py
```

> step = ("merged", f"Autopilot merged PR #{pr}; what it unblocks starts when the issue closes.")
>                         elif how == "queued":
>                             step = ("queued", f"PR #{pr} is in the merge queue; GitHub merges it when the queue's checks pass.")
>                         elif how == "waits":
>                             step = ("stop", f"PR #{pr} waits for your approval before it merges. Approve it on GitHub, or "
>                                             "review it with a command to send it back.")
>                         elif how == "unconfirmed":
>                             unconfirmed_comment(repo, pr, why, " ".join(f"@{o}" for o in owners))
>                             step = ("stop", f"Autopilot could not confirm PR #{pr} merged: {why}. Check it on GitHub and merge "
>                                             "it if it did not merge.")
>                         else:
>                             step = ("stop", f"Autopilot did not merge the pull request: {why}. It waits for you: merge it, or "
>                                             "review it with a command to send it back.")
>                 if rec.get("role") == "reviewer" and (rec.get("stage") or "") == "plan" and rec.get("check", {}).get("passed") \
>                         and (rec.get("handback") or {}).get("verdict") == "approve":
>                     # Code records the approved plan's links on GitHub and redraws the cards they touch; anything that keeps
>                     # a link from be

**Agent:** Quick throwaway fix to confirm the 417.3 test can pass on a correct build.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; cp dokima/agent.py /tmp/agent.bak; python3 - <<'EOF'
p='dokima/agent.py';s=open(p).read()
s=s.replace('''                            "GitHub answers.")
        if rec.get("role") == "worker":''','''                            "GitHub answers.")
            open(os.path.join(out, "undecided"), "w").write("")
        if rec.get("role") == "worker":''',1)
s=s.replace('''os.path.exists(os.path.join(argv[3], "board.txt")) and (rec''','''os.path.exists(os.path.join(argv[3], "board.txt")) and not os.path.exists(os.path.join(argv[3], "undecided")) and (rec''',1)
open(p,'w').write(s)
EOF
PYTHONPATH=. timeout 600 pytest -q tests/test_next_rate_limit.py tests/test_failed_run_card.py 2>&1 | tail -3; cp /tmp/agent.bak dokima/agent.py; git status --short
```

> .............                                                            [100%]
> 13 passed in 11.44s

`13. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Changed the test for 417.3 so it follows a failed decision through the board step, with GitHub still refusing, and checks the issue's card ends in Plan with Needs you.",
   "Kept the two criteria, the two requirements, the scope and the other nine tests as they were."
  ],
  "decided": [
   "The test reuses the fake GitHub and fake board of tests/test_start.py and tests/test_failed_run_card.py without changing them, so the scope stays the same."
  ],
  "open": []
 },
 "verdict": "approve",
 "summary": "The test for Needs you now checks the card itself: it fails on the build that lost Needs you and passes once a failed decision keeps it.",
 "raises": [],
 "answers": [],
 "asks": [
  {
   "ask": "When deciding what runs next fails, the record says so on the issue in one line, with GitHub's reason, instead of stopping silently.",
   "source": "https://github.com/dokima-dev/dokima/issues/417",
   "criterion": "417.1"
  },
  {
   "ask": "When the failure is GitHub's rate limit, the step is tried again after the limit resets, and starts what it would have started.",
   "source": "https://github.com/dokima-dev/dokima/issues/417",
   "criterion": "417.2"
  },
  {
   "ask": "this issue is about never losing a step when it runs out.",
   "source": "https://github.com/dokima-dev/dokima/issues/417",
   "criterion": "417.2"
  }
 ]
}
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"summary": "The test for Needs you.*",/"summary": "The Needs you test now checks the card: it fails on the build that lost Needs you and passes once that is fixed.",/' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; git status --short
```

> rc=0

**Agent:** I approved the plan for [#417](https://github.com/dokima-dev/dokima/issues/417) (autopilot losing a step when GitHub refuses a call). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks with no problems reported.

- **The blocker from last round is fixed.** That blocker said the test for 417.3 was too weak. It now runs the board step with GitHub still refusing reads and checks the issue's card ends in Plan with Needs you.
  - On the worker's first build, which is still on `try/issue-417`, both of its cases fail with "the board step left the issue's card at None".
  - With a quick throwaway fix that makes a failed decision skip rebuilding the card from GitHub, that file and `tests/test_failed_run_card.py` pass (13 passed). I then put `dokima/agent.py` back, and the working tree is clean.
  - The worker's second build ([#447](https://github.com/dokima-dev/dokima/pull/447), the pull request) isn't on this branch, so I haven't run these tests against it.
- **Every new test fails today for the right reason.** Against main's code, all 10 tests in `tests/test_next_rate_limit.py` fail because the feature is missing: GitHub's error escapes, nothing is retried, or no line gives GitHub's reason. None fail from a crash or a bad path.
- **Every ask is covered.** All three of your asks in the issue map to a criterion (417.1, 417.2, 417.2). Your only comment since the last review was `/review`, which asks for nothing new.
- **Nothing was left to answer or raise.** There were no open blockers to answer, and I found nothing new.

I ran the tests with `PYTHONPATH=.` because this machine's `PYTHONPATH` points to `/tmp/runtime`. A plain `pytest -q` here would test that copy, not the code in the repo.
