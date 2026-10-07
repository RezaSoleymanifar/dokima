# reviewer (plan) for #168

Run: https://github.com/dokima-dev/dokima/actions/runs/37681958329

`1. Bash`
```
cd /tmp/pack; ls in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (32.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/914e63c3-9335-4bad-a5ba-2a37222a329c/tool-results/by3lcfw9m.txt
> 
> Preview (first 2KB):
> 01-planner.json
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> # Issue #168: Merge check reads the criteria from the approved plan, not the issue text
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> The merge check "all done-whens passed" fails on every pull request from the new flow, so every merge needs my admin override. It looks for the acceptance criteria in the issue's text, but plans now live in the agents' record comments. It found nothing on #160, #161, #162, #163 and #165.
> 
> What I want. The check reads the criteria and their tests from the newest plan the reviewer approved, and passes only when every criterion's tests pass. A pull request with no approved plan, like a hand built one, still fails, and my override stays the explicit way through. The reason for a failure says which criterion failed or that no approved plan was found.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #168 (2026-10-07T19:16:59Z)
> 
> /plan
> 
> 
> ### dokima-runtime on issue #168 (2026-10-07T19:20:55Z)
> 
> <!-- dokima-record -->
> **Plan

`2. Bash`
```
cd /tmp/pack; sed -n '/## Comments/,$p' issue.md | grep -v '^$' | cut -c1-600 | head -150
```

> ## Comments
> ### RezaSoleymanifar on issue #168 (2026-10-07T19:16:59Z)
> /plan
> ### dokima-runtime on issue #168 (2026-10-07T19:20:55Z)
> <!-- dokima-record -->
> **Planner**
> Pull requests from the new flow pass the merge check on their own proof, so the owner no longer needs an admin override to merge them.
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - When the reviewer approved a plan and the planner has since handed back a newer plan that is not reviewed yet, which plan should the merge check use? (A) The newest approved one, as your words say ("the newest plan the reviewer approved"); I planned for this. (B) None: fail with "No approved plan found" until the newer plan is approved, so a pull request never merges on a plan already superseded.
> <details><summary>Full record</summary>
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37673302893",
>  "commit_before": "acfbaa71555f8fb187d080aa32eddaa3ef69e204",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 198830,
>   "turns": 17,
>   "cost_usd": 0.9735966,
>   "tokens_in": 718280,
>   "tokens_out": 20335
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/168/37673302893-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37673302893",
>  "handback": {
>   "kind": "user_story",
>   "user_story": "Pull requests from the new flow pass the merge check on their own proof, so the owner no longe

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/03-reviewer-plan.json'));print(json.dumps(d,indent=1)[:5000])"
```

> [
>  {
>   "id": "B1",
>   "criterion": "168.1",
>   "test": "tests/test_merge_check.py::test_one_check_per_criterion_of_the_approved_plan_running_exactly_its_tests",
>   "problem": "Every passing case ends with the plan review approval as the very last record. On a real issue the worker's record, and code-stage reviewer records, come after the approval (agent.yml posts the worker's record on the issue when no PR is open yet). A check that takes 'the newest record must be a plan approval', or treats a code-stage block as overturning the plan, passes every test here and still fails every pull request from the flow: the exact bug the owner reported.",
>   "evidence": "tests/test_merge_check.py: the passing cases use [planned(PLAN), reviewed(APPROVE)] or end with reviewed(APPROVE); no worker record and no record with stage 'pr' appears anywhere. .github/workflows/agent.yml:236-240 posts worker and pr-stage records on the issue whenever no open PR exists.",
>   "fix": "In the 168.1 test, add a case [planned(PLAN), reviewed(APPROVE), record('worker', {...}), record('reviewer', BLOCK-like handback, stage='pr'), record('reviewer', APPROVE-like handback, stage='pr')] and assert the three checks of PLAN still come out."
>  }
> ]{
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37681547556",
>  "commit_before": "22d15e5f46325780186f32b495381b736f4d8d16",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 56077,
>   "turns": 10,
>   "cost_usd": 0.4767538

`4. Bash`
```
cd /tmp/pack; cat plan.json; python3 -c "
import json;d=json.load(open('in/04-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); print(d.keys())"
```

> {
>  "kind": "user_story",
>  "user_story": "Pull requests from the new flow pass the merge check on their own proof, so the owner no longer needs an admin override to merge them.",
>  "acceptance_criteria": [
>   {
>    "text": "The merge check reads the criteria from the newest plan, and only once the reviewer approved it, not from the issue's text: the pull request shows one check per criterion (acceptance criteria first, then non-functional requirements), named \"168.k \u00b7 <the criterion's words>\" (long words cut short, as check names are today), and each runs exactly the tests that plan lists for that criterion. The worker's records and code reviews that follow the approval do not replace or overturn it. When a newer plan is handed back, the merge check fails until that plan is approved; nothing merges on an older plan.",
>    "source": "https://github.com/dokima-dev/dokima/issues/168"
>   },
>   {
>    "text": "A criterion the approved plan gives no test still gets its own named check, and that check fails. \"all done-whens passed\" passes only when every criterion's check passes, so a failure always shows, by number and words, which criterion failed.",
>    "source": "https://github.com/dokima-dev/dokima/issues/168"
>   },
>   {
>    "text": "A pull request with no approved plan fails the merge check with one check named \"No approved plan found for issue #N\", or \"No approved plan found: no issue linked\" when it names no issue (a hand-built pull request). This covers no plan, a plan not 

**Agent:** Let me look at the tests and the diff of the last planner run.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff 22d15e5 HEAD -- tests | head -150; pytest -q tests/test_merge_check.py 2>&1 | tail -15
```

> commit 295a29d978dee9f20eab7aab049aeb57dfadbe51
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 20:25:52 2026 +0000
> 
>     planner for #168 (run 37681726443)
> 
>  tests/test_merge_check.py | 17 ++++++++++++++++-
>  1 file changed, 16 insertions(+), 1 deletion(-)
> diff --git a/tests/test_merge_check.py b/tests/test_merge_check.py
> index 89d7929..d6dcdc5 100644
> --- a/tests/test_merge_check.py
> +++ b/tests/test_merge_check.py
> @@ -101,8 +101,23 @@ def test_one_check_per_criterion_of_the_approved_plan_running_exactly_its_tests(
>  
>      The issue holds a plan and an approving plan review, both posted by the bot. The check list must name 168.1, 168.2
>      and 168.3 (acceptance criteria, then the non-functional one) with their words, and run exactly the tests the plan
> -    lists for each, in order: no more, no fewer."""
> +    lists for each, in order: no more, no fewer. Then the same plan is checked on the records a real issue holds at
> +    merge time: the owner's `/work`, the worker's record, and code reviews (a block, then an approval) after the plan
> +    approval. None of those replaces or overturns the approved plan, so the same three checks come out."""
>      record_property("proves", "168.1")
> +    real = [planned(PLAN), reviewed(APPROVE),
> +            {"author": {"login": "owner"}, "body": "/work", "createdAt": ""},
> +            record("worker", {"summary": "Built it.", "replies": []}),
> +            record("reviewer", {**BLOCK, "stage":

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,100p tests/test_merge_check.py; grep -n "stage" dokima/*.py | grep -i "review\|record" | head -20
```

> """The merge check reads its criteria and their tests from the newest plan the reviewer approved (issue #168).
> 
> Every test here runs the real command the "done-whens" workflow runs, `python3 -m dokima.checks matrix`, from the repo
> root, with GitHub faked: a stub `gh` on PATH answers from a JSON file in a temp folder, and the pull request event is a
> temp file. The issue's records are real record comments, drawn by dokima.agent.render, so the check reads exactly what
> the bot posts. Nothing here touches the network.
> """
> import json
> import os
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent  # noqa: E402
> 
> ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
> BOT = "dokima-runtime"
> REPO = "o/r"
> 
> STUB_GH = '''#!/usr/bin/env python3
> """A stand-in for the GitHub CLI: answers from $STUB_DATA."""
> import json, os, sys
> data = json.load(open(os.environ["STUB_DATA"]))
> a = sys.argv[1:]
> if a[:2] == ["issue", "view"]:
>     print(json.dumps(data["issues"][a[2]]))
> elif a[:2] == ["api", "graphql"]:
>     print(json.dumps({"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": []}}}}}))
> elif a[:2] == ["pr", "view"]:
>     print(json.dumps({"comments": [], "reviews": [], "headRefName": "", "body": ""}))
> else:
>     print("[]")
> '''
> 
> PLAN = {"kind": "user_story", "user_story": "Owners merge without an override.",
>         "acceptance_criteria": [{"text": "First thing works", "source": "#168"},
>      

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added to the 168.1 test the records an issue really holds at merge time: the owner's /work, worker records, and a blocking then an approving code review after the plan approval.",
          "Stated in 168.1 that the worker's records and code reviews after the approval do not replace or overturn it, and that long criterion words are cut short in check names as today."],
  "decided": ["Only dokima/checks.py changes; the done-whens workflow stays as it is."],
  "open": ["The planner still flags that a pull request changing dokima/checks.py also changes the check that judges it, for a separate issue."]},
 "verdict": "approve",
 "summary": "The plan now proves the merge check keeps the approved plan through the worker's records and code reviews that follow it, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "All six new tests fail today for the right reason: the merge check still reads the issue's text and builds no checks.",
   "evidence": "pytest -q tests/test_merge_check.py: 6 failed, each showing matrix=[] from the old reader."}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [
  {"title": "Run the merge check from main's code, not the pull request's",
   "why": "The done-whens workflow checks out the pull request and runs its own dokima/checks.py, so a pull request can change the check that judges it.",
   "evidence": ".github/workflows/done-whens.yml: actions/checkout@v5 on pull_request, then python3 -m dokima.checks matrix (raised by the planner as a concern)."}
 ]}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 168 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for #168, so it now waits for your `/work`.

- **Last blocker, B1, is fixed.** Before, every test ended right after the plan approval, so none looked like an issue on the day it merges. The planner has added that case to the 168.1 test. After the plan approval it adds your `/work`, two worker records, and a code review that blocks and then one that approves. The test checks that the approved plan's three checks still come out. It checks this once with the full set of records and once with the blocking code review as the newest record. It now fails a merge check that only accepts a plan approval as the newest record, and one that lets a code-review block cancel the approved plan.
- **Your answer B is in the plan.** If a newer plan is handed back, the merge check fails until that plan is approved, so nothing merges on an older plan.
- **Wording added to 168.1:** the worker's records and code reviews after the approval don't replace or cancel it. Long criterion words are still cut short in check names, as they are today.
- **Tests:** I ran `pytest -q tests/test_merge_check.py`. All 6 new tests fail today because the feature is missing: the merge check still reads your issue text and builds no checks (`matrix=[]`). None of them fails because of a crash or a bad path.
- **Proposed issue:** run the merge check from main's code instead of the pull request's. The `done-whens` workflow runs the pull request's own `dokima/checks.py`, so a pull request can change the check that judges it. That matters here because this plan changes exactly that file. The planner raised this concern; it stays a proposal until you file it.

My review is in `/tmp/dokima-out/review.json`, and it passes both hand-back checks.
