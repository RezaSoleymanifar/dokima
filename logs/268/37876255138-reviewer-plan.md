# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37876255138

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (283KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/af9244e5-246c-46ab-aa9a-5ff1d23c650d/tool-results/byqul4g39.txt
> 
> Preview (first 2KB):
> total 192
> drwxr-xr-x 2 runner runner  4096 Oct  9 02:48 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 02:48 ..
> -rw-r--r-- 1 runner runner  5150 Oct  9 02:48 01-planner.json
> -rw-r--r-- 1 runner runner  4552 Oct  9 02:48 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  3910 Oct  9 02:48 03-worker.json
> -rw-r--r-- 1 runner runner  2965 Oct  9 02:48 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner  8223 Oct  9 02:48 05-planner.json
> -rw-r--r-- 1 runner runner  4332 Oct  9 02:48 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner   333 Oct  9 02:48 07-not-started.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:48 08-updater.json
> -rw-r--r-- 1 runner runner  8647 Oct  9 02:48 09-planner.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:48 10-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:48 11-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:48 12-updater.json
> -rw-r--r-- 1 runner runner  5440 Oct  9 02:48 13-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11812 Oct  9 02:48 14-planner.json
> -rw-r--r-- 1 runner runner  5673 Oct  9 02:48 15-reviewer-plan.json
> -rw-r--r-- 1 runner runner 15025 Oct  9 02:48 16-planner.json
> -rw-r--r-- 1 runner runner  5435 Oct  9 02:48 17-reviewer-plan.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:48 18-updater.json
> -rw-r--r-- 1 runner runne

`2. Bash`
```
cd /tmp/pack; wc -c issue.md; cat open_blockers.json; echo; cat plan.json
```

> 273092 issue.md
> []
> {
>  "kind": "user_story",
>  "summary": "Issues any agent finds outside its own issue are filed by code at the end of the run, parked and labeled filed-by-dokima.",
>  "user_story": "Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.",
>  "acceptance_criteria": [
>   {
>    "text": "Every agent hands back the issues it finds as raises of kind issue (title, why, evidence), in the shared field #289 brings. The planner's, the worker's and the reviewer's prompts each describe it. No hand-back gains a new issues_found or other raise-type field, and a finding handed back any other way is not filed. Every issue raised that way is filed during that agent's own run, with no command, as its own GitHub issue. The issue takes the finding's title and has exactly two labels, parked and filed-by-dokima, even on a repo that doesn't have those labels yet. A hand-back that raises no issues files none.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268"
>   },
>   {
>    "text": "Each filed issue says where it was found (the issue the run worked on, plus its pull request when there is one) and which agent found it. It carries the finding's why and evidence, and links the comment that holds the record of the run that found it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268

`3. Bash`
```
cd /tmp/pack; grep -n '^#\|^## \|^### \|^---' issue.md | head -100
```

> 1:# Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 95:## Comments
> 97:### dokima-runtime on issue #268 (2026-10-08T21:27:32Z)
> 101:### dokima-runtime on issue #268 (2026-10-08T21:27:46Z)
> 270:### dokima-runtime on issue #268 (2026-10-08T21:40:31Z)
> 411:### dokima-runtime on issue #268 (2026-10-08T21:43:11Z)
> 416:### dokima-runtime on issue #268 (2026-10-08T21:43:13Z)
> 497:### dokima-runtime on PR #274 (2026-10-08T21:54:27Z)
> 597:### dokima-runtime on issue #268 (2026-10-08T22:03:21Z)
> 795:### dokima-runtime on PR #274 (2026-10-08T22:07:27Z)
> 799:### dokima-runtime on issue #268 (2026-10-08T22:11:55Z)
> 932:### dokima-runtime on PR #274 (2026-10-08T22:13:23Z)
> 936:### dokima-runtime on issue #268 (2026-10-08T22:15:43Z)
> 941:### dokima-runtime on PR #274 (2026-10-08T22:15:45Z)
> 975:### dokima-runtime on PR #274 (2026-10-08T22:19:15Z)
> 979:### dokima-runtime on PR #274 (2026-10-08T22:52:23Z)
> 983:### dokima-runtime on PR #274 (2026-10-08T23:47:03Z)
> 987:### dokima-runtime on issue #268 (2026-10-08T23:47:05Z)
> 1024:### dokima-runtime on issue #268 (2026-10-08T23:47:20Z)
> 1225:### dokima-runtime on PR #274 (2026-10-08T23:51:08Z)
> 1229:### dokima-runtime on issue #268 (2026-10-08T23:51:10Z)
> 1266:### dokima-runtime on PR #274 (2026-10-08T23:56:57Z)
> 1270:### dokima-runtime on issue #268 (2026-10-08T23:57:00Z)
> 1307:### dokima-runtime on PR #274 (2026-10-09T00:02:40Z)
> 1311:### dokima-runtime on issue #268 (2026-10-09T00:02:42Z)
> 1348:### dokima-run

`4. Bash`
```
cd /tmp/pack; sed -n 1,96p issue.md | grep -n -A200 'dokima-card-end\|<!-- dokima' | tail -80; echo ======; sed -n 1700,1707p issue.md; sed -n 2240,2246p issue.md
```

> 17-- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Acceptance criterion:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37874831313/job/113640957203">Every agent hands back the issues it finds as raises of kind issue (title, why, evidence), in the shared field #289 brings. The planner's, the worker's and the reviewer's prompts each describe it. No hand-back gains a new issues_found or other raise-type field, and a finding handed back any other way is not filed. Every issue raised that way is filed during that agent's own run, with no command, as its own GitHub issue. The issue takes the finding's title and has exactly two labels, parked and filed-by-dokima, even on a repo that doesn't have those labels yet. A hand-back that raises no issues files none.</a>
> 18-  - *<a href="https://github.com/dokima-dev/dokima/blob/d620ceca4bc15dd54ab83d3afd713db06bea1a6f/tests/test_filed_issues.py#L368"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: Each issue any agent finds is filed in that run, parked and labeled filed-by-dokima.*
> 19-  - <a href="https://github.com/dokima-dev/dokima/issues/268">Source</a>
> 20-- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="pass

`5. Bash`
```
cd /tmp/pack/in; for f in 20-reviewer-plan.json 21-worker.json 22-reviewer-pr.json; do echo "== $f"; python3 -c "import json,sys;d=json.load(open('$f'));print(json.dumps(d,indent=1)[:5000])"; done
```

> == 20-reviewer-plan.json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37873445169",
>  "commit_before": "87af78ccad68dea780d5a0585e43cf951a8fcf0b",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 235231,
>   "turns": 13,
>   "cost_usd": 0.5634788000000002,
>   "tokens_in": 547974,
>   "tokens_out": 6140
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/268/37873445169-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37873445169",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "Re-planned on the newest main (bf41093, #290) and on the owner's answer to wait for #289.",
>     "Added checks that the reviewer, in plan review and code review, handing findings back in an issues_found field files nothing, like the planner and the worker."
>    ],
>    "decided": [
>     "Found issues are raises of kind issue for all three agents, with no question left for the owner.",
>     "Marked the issue blocked by #289 and said the worker should start only after #289 merges, merging main first."
>    ],
>    "open": []
>   },
>   "verdict": "approve",
>   "summary": "The plan builds found issues on #289's raises shape and waits for #289; all eight tests fail on main only because nothing is filed.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "The tests pin the raise shape {\"kind\": \"issue\", \"title\", \"why\", \"evidence\"} before #289 has merged; if #289 lands with other names, the tests need a re-plan be

**Agent:** Reading the plan and history is done. Next I'll check the newest comments, then run the plan's tests on this branch and on main.

`6. Bash`
```
cd /tmp/pack; sed -n 2872,2890p issue.md; echo ...; sed -n 3100,3130p issue.md; cd /home/runner/work/dokima/dokima; git fetch -q origin 2>&1|tail -2; git log --oneline -5 origin/main; git diff --stat origin/main...HEAD | tail -5; git diff 87af78c 70b2910 --stat
```

> ### dokima-runtime on issue #268 (2026-10-09T02:39:12Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 
> 1. Every agent hands back the issues it finds as raises of kind issue (title, why, evidence), in the shared field #289 brings. The planner's, the worker's and the reviewer's prompts each describe it. No hand-back gains a new issues_found or other raise-type field, and a finding handed back any other way is not filed. Every issue raised that way is filed during that agent's own run, with no command, as its own GitHub issue. The issue takes the finding's title and has exactly two labels, parked and filed-by-dokima, even on a repo that doesn't have those labels yet. A hand-back that raises no issues files none.
> 2. Each fil

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show 70b2910 --stat; git show 70b2910 -- tests/test_plan_check.py; git diff origin/main HEAD -- tests/test_plan_check.py
```

> commit 70b29100af935c3ce44ea6d18740aa4050b1f467
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:47:31 2026 +0000
> 
>     planner for #268 (run 37875588130)
> 
>  tests/test_plan_check.py | 6 ++++--
>  1 file changed, 4 insertions(+), 2 deletions(-)
> commit 70b29100af935c3ce44ea6d18740aa4050b1f467
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:47:31 2026 +0000
> 
>     planner for #268 (run 37875588130)
> 
> diff --git a/tests/test_plan_check.py b/tests/test_plan_check.py
> index cf33fa3..2bd21b1 100644
> --- a/tests/test_plan_check.py
> +++ b/tests/test_plan_check.py
> @@ -128,7 +128,8 @@ def test_anything_but_a_story_or_a_feature_is_rejected_saying_the_planner_always
>  def test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question(record_property):
>      """The planner's prompt offers only the user_story and feature kinds, and the planner workflow never looks for question.md.
>  
> -    Reads dokima/roles/planner.md: every "kind" it shows is user_story or feature (both still shown), the line naming the
> +    Reads dokima/roles/planner.md: every plan "kind" it shows (kinds inside a raises list are a raise's kind, not the
> +    plan's, and are left out) is user_story or feature (both still shown), the line naming the
>      kinds and the line saying how the planner ends never offer a question, no heading offers "one question" for the owner,
>      no line says a question is shown as handed bac

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_filed_issues.py tests/test_plan_check.py -x -q 2>&1 | tail -5; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt origin/main 2>&1|tail -1; cp tests/test_filed_issues.py tests/test_plan_check.py /tmp/mainwt/tests/; cd /tmp/mainwt; timeout 600 python3 -m pytest -q tests/test_filed_issues.py tests/test_plan_check.py 2>&1 | grep -E 'Error|passed|failed' | cut -c1-300
```

> ............................................................             [100%]
> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> tests/test_filed_issues.py:417: AssertionError
> E       AssertionError: 268.2: planner: expected 2 filed issues, got []
> tests/test_filed_issues.py:454: AssertionError
> E       AssertionError: 268.3: planner: the run did not file its two findings; filed: []
> tests/test_filed_issues.py:490: AssertionError
> E       AssertionError: 268.4: a planner listing a finding twice did not file it exactly once beside the other; filed: []
> tests/test_filed_issues.py:507: AssertionError
> E       AssertionError: 268.5: planner: the run did not file its two findings; filed: []
> tests/test_filed_issues.py:550: AssertionError
> E       AssertionError: 268.5: planner: the card does not say the finding was not filed and GitHub's reason:
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned th
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmid

`9. Bash`
```
cd /tmp/mainwt; cp /home/runner/work/dokima/dokima/dokima/roles/planner.md dokima/roles/planner.md; grep -n '"kind"' dokima/roles/planner.md | head; sed -i '0,/"kind": "feature"/s//"kind": "question"/' dokima/roles/planner.md; python3 -m pytest -q tests/test_plan_check.py -k lone_question 2>&1 | grep -E '154.1|passed|failed' | head -3; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt
```

> 115:  {"kind": "user_story",
> 128:- A feature: {"kind": "feature", "summary": "...", "feature": "...", "stories": [{"title": "...", "user_story": "...",
> 136:Any kind may add "raises": [{"kind": "issue", "title": "...", "why": "...", "evidence": "a file, line or issue number"}]:
>         record_property("proves", "154.1")
> >       assert shown == {"user_story", "feature"}, f"154.1: the prompt shows the kinds {sorted(shown)}, not exactly user_story and feature"
> E       AssertionError: 154.1: the prompt shows the kinds ['question', 'user_story'], not exactly user_story and feature

**Agent:** B2's fix holds up. Next I'll write the hand-back, reusing the earlier review's links to the owner's comments.

`10. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('20-reviewer-plan.json'))['handback'];print(json.dumps(d['asks'][7:],indent=1)); print(d.get('assumptions'))"; grep -o 'issuecomment-[0-9]*' /tmp/pack/issue.md | sort -u | head
```

> [
>  {
>   "ask": "Heads up: #289 replaces the many raise-type fields with two shared ones, raises and answers. Build this toward that shape and add no new raise-type field.",
>   "source": "https://github.com/dokima-dev/dokima/issues/268",
>   "criterion": "268.1"
>  },
>  {
>   "ask": "Answer: wait for #289. Found issues become the issue kind of raises there, so build this once, on that shape, after #289 merges.",
>   "source": "https://github.com/dokima-dev/dokima/issues/268",
>   "criterion": "268.1"
>  }
> ]
> None
> Shell cwd was reset to /home/runner/work/dokima/dokima

`11. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack/in; python3 - <<'EOF'
import json
prev=json.load(open('20-reviewer-plan.json'))['handback']
r={"previous_step":{"did":["Changed the older planner prompt test (154.1) so a raise of kind issue in the prompt no longer counts as a plan kind, as the code review asked (B2)."],
 "decided":["Kept the plan's five criteria and their eight tests unchanged.","Kept the issue blocked by #289: the worker starts only after #289 merges, merging main first."],"open":[]},
 "verdict":"approve",
 "summary":"The re-plan fixes the clash between the older planner prompt test and this plan; all eight tests still fail on main only because nothing is filed.",
 "blockers":[],
 "notes":[{"text":"The changed 154.1 test still catches a prompt that offers a question kind, and passes on main's prompt and on this branch's prompt.","evidence":"With this branch's planner.md and its feature kind changed to question: '154.1: the prompt shows the kinds ['question', 'user_story'], not exactly user_story and feature'. pytest tests/test_plan_check.py on this branch: all passed."},
  {"text":"#289 has not merged yet. The code review's blocker B3 for the worker (wait for #289 and use its raises field) still stands, and the tests pin the raise shape {\"kind\": \"issue\", \"title\", \"why\", \"evidence\"}; if #289 lands with other names, the tests need another re-plan.","evidence":"git log origin/main ends at bf41093 (#290); plan.json links.blocked_by is [289]."}],
 "resolved":["B2"],
 "issues_found":[],
 "asks":prev["asks"]}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The re-plan fixes the clash with the older planner prompt test; all eight tests still fail on main only because nothing is filed."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> exit 0

**Agent:** I approved the plan for #268, and the review is saved to `/tmp/dokima-out/review.json`. It passes both hand-back checks.

**What the planner changed:** a code review had asked the planner to fix one older test (blocker B2). The older test (154.1) checks that the planner's instructions offer only two kinds of plan. It failed because this plan also adds found issues to those instructions as "raises of kind issue". The planner changed it to ignore kinds inside a raises list. The plan's five criteria and eight tests are unchanged, and the issue is still blocked by #289.

**What I ran:**
- **This branch:** the eight new tests and the planner-check tests (154.1 among them) all pass.
- **Main:** the same eight tests fail only because nothing gets filed (`filed: []`), which is the right reason. The changed 154.1 test passes there.
- **Does 154.1 still catch the bad case:** I changed the instructions on this branch to offer a "question" kind. The test failed, naming `['question', 'user_story']`.

**Blockers:** I marked B2 as resolved. There were no earlier plan-review blockers left open, and every ask from your issue and your two comments still matches a criterion.

**Notes for you:**
- #289 hasn't merged; main still ends at #290. The code review's other blocker, B3, still stands for the worker: wait for #289 and use its shared raises field.
- The tests assume found issues look like `{"kind": "issue", "title", "why", "evidence"}`. If #289 lands with different names, the tests will need another re-plan before the worker starts.
