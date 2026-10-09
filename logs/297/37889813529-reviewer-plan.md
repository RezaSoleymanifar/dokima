# reviewer (plan) for #297

Run: https://github.com/dokima-dev/dokima/actions/runs/37889813529

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (138.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/62e85f11-3c0a-4a9d-bf89-5c255b603f4b/tool-results/bwnp1bkeb.txt
> 
> Preview (first 2KB):
> total 88
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:42 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:42 ..
> -rw-r--r-- 1 runner runner 5917 Oct  9 05:42 01-planner.json
> -rw-r--r-- 1 runner runner 7502 Oct  9 05:42 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 9417 Oct  9 05:42 03-planner.json
> -rw-r--r-- 1 runner runner 6680 Oct  9 05:42 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8471 Oct  9 05:42 05-planner.json
> -rw-r--r-- 1 runner runner 4501 Oct  9 05:42 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2096 Oct  9 05:42 07-worker.json
> -rw-r--r-- 1 runner runner 4032 Oct  9 05:42 08-reviewer-pr.json
> -rw-r--r-- 1 runner runner 8830 Oct  9 05:42 09-planner.json
> -rw-r--r-- 1 runner runner  359 Oct  9 05:42 10-updater.json
> # Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> The board's Needs you pill shows only while something truly waits on the owner, and Autopilot shows otherwise.
> 
> **Review**
> 
> [issue #297](https://github.com/dokima-dev/dokima/issues/297) · [PR #319](https://github.com/dokima-dev/dokima/pull/319) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt

`2. Bash`
```
cd /tmp/pack; wc -c issue.md; cat open_blockers.json; echo ----; cat in/08-reviewer-pr.json; echo; cat in/09-planner.json | python3 -m json.tool | head -150; cat in/10-updater.json
```

> 133035 issue.md
> []----
> {
>  "role": "reviewer",
>  "stage": "pr",
>  "run_id": "37888113763",
>  "commit_before": "5638e2649110c0cd2d844c2f56c6d6654c3ac60b",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 102036,
>   "turns": 18,
>   "cost_usd": 0.8560426,
>   "tokens_in": 939530,
>   "tokens_out": 9672
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/297/37888113763-reviewer-pr.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37888113763",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The worker made finished checks stop marking pull requests Needs you, and made a Needs you stay through new commits and checks.",
>     "The worker made a code owner's /plan, /work or /review, in a comment or a review summary, clear Needs you on the issue and its pull request at once, and made the board run on submitted reviews.",
>     "The worker added a sweep at every merge that sets each card's pill from its issue's history, keeps the pill of a card it cannot read and fails the run naming it."
>    ],
>    "decided": [
>     "A closed issue or pull request never gets Needs you; when GitHub cannot say whether it is closed, Needs you shows.",
>     "A parent whose split is filed no longer waits on the owner."
>    ],
>    "open": []
>   },
>   "verdict": "block",
>   "summary": "All tests pass, but the merge sweep treats an owner's Approve starting with a command as an answer and clears a real Needs you.",
>   "blockers": [
>    {
>     "id"

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/05-planner.json'))['handback'];b=json.load(open('in/09-planner.json'))['handback']
print(a['acceptance_criteria']==b['acceptance_criteria'], a['non_functional']==b['non_functional'], a['scope']==b['scope'])
print(a.get('questions'),b.get('questions'))
"; python3 -m json.tool in/06-reviewer-plan.json | sed -n '/\"asks\"/,/assumptions/p'; diff <(python3 -m json.tool plan.json) <(python3 -c "import json;print(json.dumps(json.load(open('in/09-planner.json'))['handback'],indent=4))") | head
```

> True True True
> None None
>         "asks": [
>             {
>                 "ask": "Needs you shows only while the flow is actually stopped waiting for me on that item: a question, an approval, a merge, an escalation.",
>                 "source": "https://github.com/dokima-dev/dokima/issues/297",
>                 "criterion": "297.1"
>             },
>             {
>                 "ask": "It clears the moment that is answered",
>                 "source": "https://github.com/dokima-dev/dokima/issues/297",
>                 "criterion": "297.2"
>             },
>             {
>                 "ask": "and always when the item closes.",
>                 "source": "https://github.com/dokima-dev/dokima/issues/297",
>                 "criterion": "297.3"
>             },
>             {
>                 "ask": "A parent issue shows Needs you only when the parent itself waits on me (for example its split before it is filed, or its end-to-end test hitting a blocker), never just because its children are in progress.",
>                 "source": "https://github.com/dokima-dev/dokima/issues/297",
>                 "criterion": "297.4"
>             },
>             {
>                 "ask": "Autopilot and Needs you are complementary: an item on autopilot shows Autopilot unless it needs me, then Needs you, never both and never neither.",
>                 "source": "https://github.com/dokima-dev/dokima/issues/297",
>                 "criterion": "297.6"
>             },
>             {
>                 "ask": "The existing wron

`4. Bash`
```
cd /tmp/pack; grep -nE '^(#+ |\*\*@|### Comment|---)' issue.md | head -80; grep -n 'issuecomment' issue.md | head -40
```

> 1:# Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 80:## Comments
> 82:### RezaSoleymanifar on issue #297 (2026-10-09T03:44:40Z)
> 86:### dokima-runtime on issue #297 (2026-10-09T03:45:04Z)
> 90:### dokima-runtime on issue #297 (2026-10-09T03:45:07Z)
> 95:### dokima-runtime on issue #297 (2026-10-09T03:45:18Z)
> 278:### RezaSoleymanifar on issue #297 (2026-10-09T03:52:03Z)
> 284:### dokima-runtime on issue #297 (2026-10-09T03:52:23Z)
> 294:### dokima-runtime on issue #297 (2026-10-09T04:07:18Z)
> 478:### RezaSoleymanifar on issue #297 (2026-10-09T04:26:33Z)
> 482:### dokima-runtime on issue #297 (2026-10-09T04:26:55Z)
> 712:### dokima-runtime on issue #297 (2026-10-09T04:39:53Z)
> 901:### RezaSoleymanifar on issue #297 (2026-10-09T04:47:00Z)
> 905:### dokima-runtime on issue #297 (2026-10-09T04:47:19Z)
> 1122:### dokima-runtime on issue #297 (2026-10-09T04:56:15Z)
> 1288:### dokima-runtime on issue #297 (2026-10-09T04:57:49Z)
> 1293:### dokima-runtime on issue #297 (2026-10-09T04:57:51Z)
> 1361:### dokima-runtime on PR #319 (2026-10-09T05:20:27Z)
> 1472:### dokima-runtime on issue #297 (2026-10-09T05:28:42Z)
> 1690:### dokima-runtime on PR #319 (2026-10-09T05:29:22Z)
> 1694:### dokima-runtime on issue #297 (2026-10-09T05:29:24Z)
> 1733:### dokima-runtime on issue #297 (2026-10-09T05:41:50Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 20,95p issue.md; sed -n 278,284p issue.md; sed -n 478,482p issue.md; sed -n 901,905p issue.md
```

> - <a href="https://github.com/dokima-dev/dokima/issues/297">Source</a>
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Acceptance criterion:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37888090407/job/113682559990">Needs you clears the moment the owner answers. A code owner's `/plan`, `/work` or `/review`, as a comment on the issue or its pull request or as the summary of a pull request review submitted as a comment or a change request, takes it off both cards at once, with Autopilot in its place on autopilot. An Approve, and a comment or review from anyone else, from a bot, or with no command, leaves it.</a>
>   - *<a href="https://github.com/dokima-dev/dokima/blob/5638e2649110c0cd2d844c2f56c6d6654c3ac60b/tests/test_needs_you.py#L264"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: A code owner's command clears Needs you at once; no other comment does.*
>   - *<a href="https://github.com/dokima-dev/dokima/blob/5638e2649110c0cd2d844c2f56c6d6654c3ac60b/tests/test_needs_you.py#L295"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: A code owner's command in a review summary clears Needs you at once.*
>   - *<a href="http

**Agent:** Checking the planner's new test fails on the current code for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; python3 -m pytest -q tests/test_needs_you.py 2>&1 | tail -30
```

> commit 805d255aa2916c492baf5fcacd85dfb20df2f03c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:41:33 2026 +0000
> 
>     planner for #297 (run 37888758011)
> 
>  tests/test_needs_you.py | 43 +++++++++++++++++++++++++++++++++++++++----
>  1 file changed, 39 insertions(+), 4 deletions(-)
> E         ?                  -  --------
> E         +     'issue #59': None,
> E         ?                   ++
> E         -     'pr #62': 'Needs you',
> E         ?               -  --------
> E         +     'pr #62': None,
> E         ?                ++
> E           }
> 
> tests/test_needs_you.py:495: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_needs_you.py::test_an_approve_starting_with_a_command_never_clears_needs_you_in_the_sweep - AssertionError: 297.5: the owner's Approve starting with /work was taken as an answer: after the sweep #59 and PR #62 show {'issue #59': None, 'pr #62': None}, not Needs you
> assert {'issue #59':...pr #62': None} == {'issue #59':...: 'Needs you'}
>   
>   Differing items:
>   {'pr #62': None} != {'pr #62': 'Needs you'}
>   {'issue #59': None} != {'issue #59': 'Needs you'}
>   
>   Full diff:
>     {
>   -     'issue #59': 'Needs you',
>   ?                  -  --------
>   +     'issue #59': None,
>   ?                   ++
>   -     'pr #62': 'Needs you',
>   ?               -  --------
>   +     'pr #62': None,
>   ?                ++
>     }
> 1 failed, 14 passed in 0.36s

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_needs_you.py; grep -n "def test_an_approve" -A60 tests/test_needs_you.py | head -80
```

> commit 805d255aa2916c492baf5fcacd85dfb20df2f03c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:41:33 2026 +0000
> 
>     planner for #297 (run 37888758011)
> 
> diff --git a/tests/test_needs_you.py b/tests/test_needs_you.py
> index 0218b3b..605c02f 100644
> --- a/tests/test_needs_you.py
> +++ b/tests/test_needs_you.py
> @@ -36,7 +36,7 @@ import pytest
>  sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
>  import test_autopilot_board as tab  # noqa: E402
>  from dokima import agent, board, card, plan  # noqa: E402
> -from test_agent import GOOD_REVIEW, SPLIT, rec  # noqa: E402
> +from test_agent import GOOD_REVIEW, GOOD_WORK, SPLIT, rec  # noqa: E402
>  
>  LABEL = "autopilot"
>  SPEC, REPO = "o/1", "o/r"
> @@ -66,16 +66,24 @@ def plan_blocked():
>      return [rec("planner", handback={"kind": "user_story"}), rec("reviewer", "plan", GOOD_REVIEW)]
>  
>  
> +def code_approved():
> +    """Records up to an approving code review, so the pull request waits to be merged."""
> +    return plan_approved() + ["/work", rec("worker", handback=GOOD_WORK),
> +                              rec("reviewer", "pr", {**GOOD_REVIEW, "stage": "pr", "verdict": "approve", "blockers": []})]
> +
> +
>  def escalated(stage="pr"):
>      """Records ending in a reviewer's escalation, which stops for the owner even on autopilot."""
>      return [rec("planner", handback={"kind": "user_story"}), rec("reviewer", stage, {**GOOD_REVIEW, "stage": stage, "verdict": "escalate"})]
>  
>  
>  class Wo

**Agent:** The new test fails on today's code for the right reason, and the criteria haven't changed. Writing the review.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
asks=json.load(open('in/06-reviewer-plan.json'))['handback']['asks']
r={"previous_step":{"did":["The planner added a test under 297.5: after a merge, the code owner's Approve starting with /work leaves Needs you on the issue and its pull request, while a comment review /work and a change request /review clear it.",
 "The planner made the test's fake GitHub return the code owner's pull request reviews."],
 "decided":["The acceptance criteria stay as they were: 297.5 already says the owner answers with a command, and 297.2 and AGENTS.md say an Approve is never one."],
 "open":[]},
 "verdict":"approve",
 "summary":"The plan now has a test showing that an Approve starting with a command never clears Needs you during a merge's sweep. It fails on today's branch for exactly that reason, and the criteria are unchanged.",
 "blockers":[],
 "notes":[{"text":"The new test checks both directions: an Approve must keep Needs you, and a comment review or change request carrying a command must clear it. So code that skipped every review would also fail.",
   "evidence":"tests/test_needs_you.py:478-499; pytest -q tests/test_needs_you.py -> 1 failed (the new test: {'issue #59': None, 'pr #62': None}, not Needs you), 14 passed"},
  {"text":"No criterion changed since the approved plan, so this re-plan can go straight to the worker.",
   "evidence":"acceptance_criteria, non_functional and scope of in/05-planner.json and in/09-planner.json compare equal"}],
 "outside_plan":[],"resolved":[],"issues_found":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 297 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> rc=1

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The plan now proves an Approve starting with a command never clears Needs you in the sweep, and that test fails today as it should."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 297 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-plan for #297. Both checks on the hand-back pass, and the review is in `/tmp/dokima-out/review.json`.

- **What the planner did:** they added one test under 297.5. It covers three pull requests waiting to be merged, each getting a code owner's review that starts with a command, and then a merge triggers the sweep:
  - An Approve saying `/work looks good` must leave Needs you on the issue and its pull request.
  - A comment review `/work` and a change request `/review` must clear it.
- **The test catches mistakes both ways:** code that wrongly counts the Approve fails it, and so does code that ignores all reviews.
- **It fails today for the right reason:** on the branch, the new test fails with "the owner's Approve starting with /work was taken as an answer: … {'issue #59': None, 'pr #62': None}". The other 14 tests in `tests/test_needs_you.py` pass.
- **Nothing else changed:** the criteria, requirements and scope are the same as the plan approved before. The re-plan can go straight to the worker without waiting for `/work`.
- **Open blockers:** none at the plan stage. B4 from the code review is the gap this test fills; the worker still has to make the code skip Approve reviews.
- **Owner's asks:** all ten are still matched to a criterion, none missing. Since the last review the owner has posted no new comments.
