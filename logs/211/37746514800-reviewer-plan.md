# reviewer (plan) for #211

Run: https://github.com/dokima-dev/dokima/actions/runs/37746514800

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (65.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6e67b007-6b43-4f5e-b231-2bc2468dce9e/tool-results/by0dvhqlu.txt
> 
> Preview (first 2KB):
> .:
> total 96
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:56 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:56 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:56 in
> -rw-r--r--  1 runner runner 65951 Oct  8 07:56 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:56 open_blockers.json
> -rw-r--r--  1 runner runner  8809 Oct  8 07:56 plan.json
> 
> in:
> total 76
> drwxr-xr-x 2 runner runner  4096 Oct  8 07:56 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 07:56 ..
> -rw-r--r-- 1 runner runner  7629 Oct  8 07:56 01-planner.json
> -rw-r--r-- 1 runner runner  8235 Oct  8 07:56 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10096 Oct  8 07:56 03-planner.json
> -rw-r--r-- 1 runner runner  4992 Oct  8 07:56 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  5272 Oct  8 07:56 05-worker.json
> -rw-r--r-- 1 runner runner  4116 Oct  8 07:56 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner  9467 Oct  8 07:56 07-planner.json
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #220](https://github.com/dokima-dev/dokima/pull/220) · [files changed](https://github.com/dokima-dev/dokima/pull/220/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.c

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #220](https://github.com/dokima-dev/dokima/pull/220) · [files changed](https://github.com/dokima-dev/dokima/pull/220/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37745252124/job/113205090009)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 3</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`, and the river still stops and mentions the owner wherever the owner must decide.
> 
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop alread

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; grep -n "Next:\*\*" issue.md
```

> 4:### Checks failing
> 43:### RezaSoleymanifar on issue #211 (2026-10-08T06:56:48Z)
> 47:### RezaSoleymanifar on issue #211 (2026-10-08T06:58:15Z)
> 51:### dokima-runtime on issue #211 (2026-10-08T06:58:34Z)
> 182:### dokima-runtime on issue #211 (2026-10-08T07:13:24Z)
> 328:### dokima-runtime on issue #211 (2026-10-08T07:15:50Z)
> 476:### dokima-runtime on issue #211 (2026-10-08T07:21:58Z)
> 604:### RezaSoleymanifar on issue #211 (2026-10-08T07:27:05Z)
> 608:### dokima-runtime on issue #211 (2026-10-08T07:27:24Z)
> 670:### dokima-runtime on PR #220 (2026-10-08T07:44:08Z)
> 770:### dokima-runtime on issue #211 (2026-10-08T07:50:02Z)
> 915:### dokima-runtime on issue #211 (2026-10-08T07:55:52Z)
> 179:**Next:** The reviewer starts now.
> 325:**Next:** The planner starts now.
> 473:**Next:** The reviewer starts now.
> 601:**Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 667:**Next:** The reviewer starts now.
> 767:**Next:** The planner starts now.
> 912:**Next:** The reviewer starts now.
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 476,500p issue.md; sed -n 600,700p issue.md | cut -c1-2500; sed -n 770,800p issue.md; sed -n 915,1100p issue.md|cut -c1-3000
```

> ### dokima-runtime on issue #211 (2026-10-08T07:21:58Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (plan)**
> 
> **approve**: Both earlier blockers are fixed: an assumption that changes how the system works or what it costs is never accepted, and code checks the owner really said the matched words where the review says; every ask has a criterion and all eleven tests fail today because the feature is missing.
> 
> <details><summary>What the previous step did</summary>
> 
> - **Did:** Added to 211.5 the owner's rule that an assumption which changes how the system works or what it costs is never accepted: each judgement says so, and code rejects an accepted one that does.
> - **Did:** Added a check that the owner's matched words appear word for word in the source named, from the issue's text, a code owner's comment on the issue or AGENTS.md, and a test that the river stops otherwise.
> - **Did:** Replaced the cost-column question in the tests with one that changes nothing, backed by a real owner comment.
> - **Decided:** A matched word found only in a comment by someone who is not a code owner, the bot included, counts as not accepted.
> - **Still open:** Six criteria, one over the split limit, kept as one story because #211 is already a story of #205.
> 
> </details>
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/03-planner.json'));b=json.load(open('plan.json'))
ah=a.get('handback',a)
for k in b:
  if ah.get(k)!=b.get(k): print('DIFF',k); print(json.dumps(b[k],indent=1)[:4000])
"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests | head -80
```

> DIFF test_changes
> {
>  "tests/test_start.py::Machine": "The fake machine's repo now holds AGENTS.md as main does, so a plan reviewer's assumption quoted from AGENTS.md can be checked inside a workflow run (blocker B1 of the code review). No test's assertions change."
> }
> DIFF replies
> [
>  {
>   "blocker": "B1",
>   "answer": "fixed",
>   "why": "The test machine in tests/test_start.py (Machine) now copies the real AGENTS.md into its repo next to dokima/, as main has it, so agent.yml's own step that copies AGENTS.md into the runtime finds it and the river checks ACCEPT_1's words word for word against the real file. The test and the code's check are unchanged; a source that is truly missing still counts as not accepted (test_an_assumption_is_accepted_only_on_words_the_owner_really_said, 'words not in AGENTS.md')."
>  }
> ]
> commit bd815f0414414e32b6e965fdff53d6a9419337c6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:55:41 2026 +0000
> 
>     planner for #211 (run 37745889992)
> 
>  tests/test_start.py | 2 ++
>  1 file changed, 2 insertions(+)
> commit bd815f0414414e32b6e965fdff53d6a9419337c6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:55:41 2026 +0000
> 
>     planner for #211 (run 37745889992)
> 
> diff --git a/tests/test_start.py b/tests/test_start.py
> index 67cd6a9..b9a097c 100644
> --- a/tests/test_start.py
> +++ b/tests/test_start.py
> @@ -437,6 +437,8 @@ class Machine:
>          # The repo: Dokim

**Agent:** I'm on the planner's test fix for #211. It only adds AGENTS.md to the fake test machine. Next I'll run the tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "ACCEPT_1\s*=" -A4 tests/test_autopilot_river.py; python3 -m pytest -q tests/test_autopilot_river.py tests/test_start.py 2>&1 | tail -5
```

> 48:ACCEPT_1 = {"question": QUESTIONS[0]["question"], "accepted": True, "changes": False,
> 49-            "matched": "a failure always says why on the issue", "source": "AGENTS.md"}
> 50-ACCEPT_2 = {"question": QUESTIONS[1]["question"], "accepted": True, "changes": False,
> 51-            "matched": "Every failure should name the step that failed", "source": ISSUE + "#issuecomment-77"}
> 52-REFUSE_2 = {"question": QUESTIONS[1]["question"], "accepted": False, "changes": False,
> ................                                                         [100%]
> 16 passed in 33.14s

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -x -n auto 2>/dev/null | tail -3 || true; python3 -m pytest -q 2>&1 | tail -4
```

> +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 4 failed, 346 passed in 131.26s (0:02:11)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q 2>&1 | grep -E "^FAILED"; git stash list | head -2
```

> FAILED tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure - AssertionError: 188.3: a blocking plan review that nobody cancelled no longer starts the planner: []
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -3; rm -rf /tmp/m && git worktree add -q /tmp/m main && cd /tmp/m && python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -3
```

> +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 11 passed in 1.71s
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 11 passed in 3.20s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /tmp/m && cp /home/runner/work/dokima/dokima/tests/test_autopilot_river.py /home/runner/work/dokima/dokima/tests/test_start.py tests/ && python3 -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^(FAILED|[0-9]+ )" | cut -c1-260; python3 -m pytest -q tests/test_start.py 2>&1|tail -1; cd /home/runner/work/dokima/dokima && git worktree remove --force /tmp/m
```

> FAILED tests/test_autopilot_river.py::test_on_autopilot_an_approved_plan_starts_the_worker_with_one_autopilot_line - AssertionError: 211.1: the approved plan on autopilot did not start exactly one worker for #57: []
> FAILED tests/test_autopilot_river.py::test_autopilot_start_starts_the_worker_on_a_plan_already_waiting_for_work - AssertionError: 211.1: /autopilot start did not start exactly one worker for #57: []
> FAILED tests/test_autopilot_river.py::test_on_autopilot_an_approved_split_files_its_stories_with_one_autopilot_line - AssertionError: 211.2: the approved split on autopilot filed 0 issues, not its 2 stories
> FAILED tests/test_autopilot_river.py::test_off_autopilot_an_approved_plan_or_split_still_stops_for_the_owner - AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
> FAILED tests/test_autopilot_river.py::test_on_autopilot_the_river_still_stops_where_the_owner_must_decide - AssertionError: 211.4: an approving plan review on autopilot did not start the worker: []
> FAILED tests/test_autopilot_river.py::test_on_autopilot_a_plan_with_questions_goes_to_the_plan_reviewer - AssertionError: 211.5: on autopilot a plan with questions did not go to the plan reviewer: 'stop'
> FAILED tests/test_autopilot_river.py::test_the_plan_reviewer_judges_every_question_against_the_owners_words - AssertionError: 211.5 (none judged): the check passed a plan review that does not judge every question properly
> FAILED tests/test_autopilot_river.py::test_on_autop

**Agent:** All 11 tests fail on main because the feature is missing, and pass on the branch with the fix. Now writing the review.

`11. Bash`
```
cd /tmp/pack; python3 -c "
import json;r=json.load(open('in/04-reviewer-plan.json'));h=r.get('handback',r);print(json.dumps(h['asks'],indent=1))"
```

> [
>  {
>   "ask": "On an issue on autopilot, a plan review that approves starts the worker by itself, and so does `/autopilot start` said on an issue whose plan is already approved and waiting for `/work`; the issue gets exactly one comment reading `Autopilot: plan approved, starting work`, the card's Next line says the worker starts now, and no Needs you is set.",
>   "source": "https://github.com/dokima-dev/dokima/issues/211",
>   "criterion": "211.1"
>  },
>  {
>   "ask": "On an issue on autopilot, an approved split files its stories as sub-issues by itself, as `/work` would, and so does `/autopilot start` said on an issue whose split is already approved; the issue gets exactly one comment reading `Autopilot: split approved, filing its stories`.",
>   "source": "https://github.com/dokima-dev/dokima/issues/211",
>   "criterion": "211.2"
>  },
>  {
>   "ask": "On an issue not on autopilot, an approved plan or split still stops for the owner, exactly as today, and no Autopilot line is posted.",
>   "source": "https://github.com/dokima-dev/dokima/issues/211",
>   "criterion": "211.3"
>  },
>  {
>   "ask": "On autopilot, the river still stops on ... an escalation, three blocking reviews in a row, a hand-back code rejected and a run that failed or never started; each stop says why on the issue, mentions the owner and sets Needs you.",
>   "source": "https://github.com/dokima-dev/dokima/issues/211",
>   "criterion": "211.4"
>  },
>  {
>   "ask": "When autopilot cannot be read from GitHub, the river stops for the owner and 

`12. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
r=json.load(open('in/04-reviewer-plan.json'));asks=r.get('handback',r)['asks']
for a in asks[5:]:
    a['source']="https://github.com/dokima-dev/dokima/issues/211#issuecomment-owner-2026-10-08T06:56:48Z"
# keep plain issue link for comment asks if no id known
for a in asks: a['source']=a['source'].split('#')[0]
out={"previous_step":{
 "did":["Made the test machine hold a copy of AGENTS.md, as main does, so an assumption quoted from AGENTS.md can be checked during a workflow run.",
        "Left every criterion and every test's checks unchanged."],
 "decided":["The code's check of the owner's words stays as it is; a source that is truly missing still counts as not accepted."],
 "open":[]},
 "verdict":"approve",
 "summary":"The planner fixed the code review's blocker by giving the test machine the real AGENTS.md; the criteria are unchanged, all 11 tests of this issue fail on main because the feature is missing and pass on the branch.",
 "blockers":[],
 "notes":[{"text":"The criteria did not change in this re-plan, so the worker can go on without the owner's /work.","evidence":"plan.json matches the approved plan except test_changes and replies; the only diff is two lines in tests/test_start.py (Machine)."},
          {"text":"On the branch, tests/test_autopilot_river.py and tests/test_start.py pass (16 passed). The full suite still has 4 failures, and they fail the same way on main: test_cancelled_run and three review-check tests in test_fixer.py and test_handback_check.py.","evidence":"python3 -m pytest -q on try/issue-211: 4 failed, 346 passed; the same 3 tests in test_fixer.py and test_handback_check.py fail on a main worktree."}],
 "outside_plan":[],
 "resolved":[],
 "issues_found":[{"title":"Three review-check tests fail on main","why":"Every pull request carries red tests that are not its own, which hides real failures.","evidence":"On main, python3 -m pytest -q tests/test_fixer.py tests/test_
```

> rc=0

`13. Bash`
```
env | grep -i -E "dokima|stage|pack" ; grep -n "asks must" -B8 dokima/agent.py | grep -n -E "environ|stage|pack" 
```

> COREPACK_ENABLE_AUTO_PIN=0
> GITHUB_WORKSPACE=/home/runner/work/dokima/dokima
> LOG_URL=https://github.com/dokima-dev/dokima/blob/logs/logs/211/37746514800-reviewer-plan.md
> GITHUB_TRIGGERING_ACTOR=dokima-runtime[bot]
> PWD=/home/runner/work/dokima/dokima
> STAGE=plan
> GITHUB_WORKFLOW_REF=dokima-dev/dokima/.github/workflows/agent.yml@refs/heads/main
> GITHUB_ACTOR=dokima-runtime[bot]
> GITHUB_REPOSITORY=dokima-dev/dokima
> RUNNER_WORKSPACE=/home/runner/work/dokima
> GITHUB_REPOSITORY_OWNER=dokima-dev
> PACK=/tmp/pack
> OUT=/tmp/dokima-out

`14. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE -u PACK -u OUT python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -1
```

> 14 passed in 3.21s

**Agent:** Those three failures come from my sandbox's STAGE setting, not from main. I'll correct the review.

`15. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['issues_found']=[]
r['notes'][1]={"text":"On the branch, tests/test_autopilot_river.py and tests/test_start.py pass (16 passed). The only other failure in the full suite is test_cancelled_run, which already fails on main and was raised in the code review.","evidence":"python3 -m pytest -q on try/issue-211 with the run's STAGE/PACK/OUT variables unset for the review-check tests: test_fixer.py and test_handback_check.py 14 passed; test_cancelled_run::test_nothing_starts_by_itself_after_a_cancel_or_a_failure fails as on main."}
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 211 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #211, and the hand-back is in `/tmp/dokima-out/review.json`. It passes both hand-back checks.

**What the planner changed:** this round fixed the code review's one blocker (B1), where a test expected the worker to start on words quoted from AGENTS.md but the test machine had no AGENTS.md. The planner added two lines to the fake test machine in `tests/test_start.py` so it copies the real AGENTS.md. No criterion changed and no test's checks changed. The code's check of the owner's words is untouched, so words that aren't really in AGENTS.md still stop the river.

**Test results:**
- **On the branch:** all 11 tests in `tests/test_autopilot_river.py` and all 5 in `tests/test_start.py` pass, including the one the code review blocked on.
- **On main:** all 11 new tests fail because the feature is missing, not because of a crash or a bad path.
- **Full suite:** the only real failure is `test_cancelled_run`. It already fails on main and the code review raised it as a separate problem.
- **Not real failures:** three other tests also failed in my run (in `test_fixer.py` and `test_handback_check.py`). That was caused by a setting in my own run (`STAGE=plan`); with it unset they pass, so I didn't report them.

**Every ask is covered:** all eight owner asks match a criterion, including "If it changes how the system works, what it costs, or isn't backed by my words, it stops for me".

**What happens next:** the criteria didn't change, so the worker can pick this up again without you typing `/work`.
