# reviewer (plan) for #334

Run: https://github.com/dokima-dev/dokima/actions/runs/37947339296

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (71KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6352ef91-9cd0-4cd1-a712-d9a9411c0c37/tool-results/b1lzkrpw2.txt
> 
> Preview (first 2KB):
> .:
> total 92
> drwxr-xr-x  3 runner runner  4096 Oct  9 14:52 .
> drwxrwxrwt 18 root   root    4096 Oct  9 14:52 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 14:52 in
> -rw-r--r--  1 runner runner 69825 Oct  9 14:52 issue.md
> -rw-r--r--  1 runner runner  2115 Oct  9 14:52 open_blockers.json
> -rw-r--r--  1 runner runner  3364 Oct  9 14:52 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner 4096 Oct  9 14:52 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 14:52 ..
> -rw-r--r-- 1 runner runner 3055 Oct  9 14:52 01-planner.json
> -rw-r--r-- 1 runner runner 6620 Oct  9 14:52 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7433 Oct  9 14:52 03-planner.json
> -rw-r--r-- 1 runner runner 5380 Oct  9 14:52 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4002 Oct  9 14:52 05-planner.json
> # Issue #334: A split story may point to my words in its parent issue
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A plan's criterion may point to the owner's words anywhere in this repo, and code checks they are really the owner's.
> 
> **Plan**
> 
> [issue #334](https://github.com/dokima-dev/dokima/issues/334)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #331, 

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json; echo; grep -n "Original issue\|^## \|^### \|dokima-ask\|<!-- dokima" issue.md | head -80
```

> [
>  {
>   "id": "B4",
>   "criterion": "334.1",
>   "test": "tests/test_parent_source.py::test_a_criterion_may_cite_the_owners_words_in_any_issue_of_this_repo",
>   "problem": "The owner replaced the wider scope with the small fix, but the plan still accepts any issue of this repo as a source, so a criterion citing an unrelated issue would pass where the owner said it must be rejected.",
>   "evidence": "Owner's comment at 2026-10-09T14:24:33Z: \"/plan Back to the small fix, replacing my two comments above: a criterion's source may be the story's own issue, its parent issue, or a comment on either. Anything else is still rejected. Keep it one user story. The wider version is parked in its own issue.\" plan.json criterion 1 says \"citing any issue of this repo\"; the test change in tests/test_autopilot_river.py turns the 'another issue' rejection (o/r/issues/58) into 'another repo', so a different issue of this repo is no longer proven rejected.",
>   "fix": "Re-plan to the issue's three asks: (1) the planner's check accepts the own issue, the parent issue, or a comment on either; (2) any other issue, including another issue of this repo, is rejected naming the criterion and source, with a passing parent case beside it; (3) the plan review's check of the owner's words accepts the parent too. Revert the test_autopilot_river.py change.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B5",
>   "criterion": "334.2",
>   "test": null,
>   "problem": "Criteria 2, 3, 6, 7, 8 and the two non-functional items (aut

`3. Bash`
```
cd /tmp/pack; sed -n 70,100p issue.md; sed -n 240,270p issue.md; sed -n 694,712p issue.md; sed -n 870,882p issue.md; sed -n 1036,1060p issue.md
```

> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> A story split from a bigger issue can't point to my words. On #331 the planner linked its criteria to #330, the parent issue where I wrote them, and code rejected the plan twice because a source must be the story's own issue or one of its comments.
> 
> What I want:
> - A criterion's source may be the story's own issue, its parent issue, or a comment on either.
> - Any other issue is still rejected, naming the criterion and the source.
> - The reviewer's check that my words were really said there accepts the parent too.
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #334 (2026-10-09T14:15:10Z)
> 
> /autopilot start
> 
> ### dokima-r

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('04-reviewer-plan.json'));print(json.dumps(d,indent=1)[:5000])"; python3 -c "
import json;d=json.load(open('05-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:1500])"; grep -o 'issuecomment-[0-9]*' /tmp/pack/issue.md | sort -u
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37945434311",
>  "commit_before": "0dbcc09cb8e616e842deee9b35ae0149456759ac",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 44514,
>   "turns": 8,
>   "cost_usd": 0.41937579999999997,
>   "tokens_in": 309965,
>   "tokens_out": 4298
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/334/37945434311-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37945434311",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner re-planned one user story: a criterion may cite the owner's words in any issue of this repo, code checks a code owner wrote them and the quote is really there, and the plan reviewer's pack gets the open-issues list and every cited issue in full."
>    ],
>    "decided": [
>     "Closed issues and pull requests are rejected as sources for now; the story's own issue is checked as today."
>    ],
>    "open": [
>     "The plan was written before the owner's comment that goes back to the small fix and parks the wider version."
>    ]
>   },
>   "verdict": "block",
>   "summary": "This plan builds the wider version the owner withdrew; it must return to the small fix: own issue, parent issue, or a comment on either.",
>   "blockers": [
>    {
>     "id": "B4",
>     "criterion": "334.1",
>     "test": "tests/test_parent_source.py::test_a_criterion_may_cite_the_owners_words_in_any_issue_of_this_repo",
>     "problem": "The owner replaced the wider scope

**Agent:** Now the tests and the code.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff e934cfe --stat; cat tests/test_parent_source.py
```

> commit 0ad073ded1fc684eb8dfc9fa7037926749ef0aff
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 14:51:22 2026 +0000
> 
>     planner for #334 (run 37946986707)
> 
>  tests/test_autopilot_river.py |   4 +-
>  tests/test_parent_source.py   | 916 +++++++++++++++---------------------------
>  2 files changed, 336 insertions(+), 584 deletions(-)
>  tests/test_parent_source.py | 403 ++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 403 insertions(+)
> """A split story may cite the owner's words in its parent issue (#334).
> 
> On #331 the planner linked its criteria to #330, the parent where the owner wrote them, and code rejected the plan
> twice: a source had to be the story's own issue or one of its comments. These tests hold code to the new rule: a
> criterion's source may be the story's own issue, its parent issue (GitHub's native sub-issue parent), or a comment
> on either; any other issue is still rejected, naming the criterion and the source; and the reviewer's check that the
> owner's words were really said there accepts the parent too.
> 
> How the parent reaches each check:
> - The starting pack (`python3 -m dokima.agent pack N ROLE STAGE DEST`, built while the run holds a GitHub key) writes
>   `parent.json` holding {"number": P}, P the issue's parent on GitHub. With no parent, or when GitHub cannot say,
>   parent.json is absent or holds {"number": null}.
> - The planner's check (`python3 -m dokima.planner check N OUT`) and the plan review's 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_parent_source.py 2>&1 | grep -E "^(E  .*33[0-9]?\.|FAILED|PASSED|[0-9]+ (passed|failed))|AssertionError" | head -40
```

> E       AssertionError: 334.1 (a story): the planner's check rejected acceptance criterion 3, whose source is https://github.com/o/r/issues/330:
> tests/test_parent_source.py:91: AssertionError
> E           AssertionError: 334.2 (another issue): the rejection does not name acceptance criterion 2 and its source https://github.com/o/r/issues/329:
> tests/test_parent_source.py:127: AssertionError
> E           AssertionError: 334.3 (the parent): the plan review's check rejected the owner's words sourced to https://github.com/o/r/issues/56:
> tests/test_parent_source.py:276: AssertionError
> E           AssertionError: 334.3 (the parent's own text): the owner's words in the parent did not let the worker start: 'stop' '**Next:** @owner-person The reviewer did not accept the plan\'s assumption for: "Should the card name the step that failed?" Answer with `/plan` and your words, or say `/work` to build it on its assumptions.'
> tests/test_parent_source.py:301: AssertionError
> E           AssertionError: 334.1: the planner 's pack does not name #330 as #331's parent: None
> tests/test_parent_source.py:380: AssertionError
> E       AssertionError: 334.4: setup: with GitHub answering, the pack does not name #330: None
> tests/test_parent_source.py:394: AssertionError
> FAILED tests/test_parent_source.py::test_a_criterion_may_cite_its_own_issue_its_parent_or_a_comment_on_either - AssertionError: 334.1 (a story): the planner's check rejected acceptance criterion 3, whose source is https://github.com/o/r/issue

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_parent_source.py -k any_other 2>&1 | grep -B2 -A12 "334.2 (another issue)" | head -40; grep -n "source" dokima/planner.py | head -30
```

> >           assert "acceptance criterion 2" in text and bad in text, \
>                 f"334.2 ({case}): the rejection does not name acceptance criterion 2 and its source {bad}:\n{text[-1500:]}"
> E           AssertionError: 334.2 (another issue): the rejection does not name acceptance criterion 2 and its source https://github.com/o/r/issues/329:
> E             ::error title=Planner output rejected::acceptance criterion 1 has the source https://github.com/o/r/issues/330, which is not this issue (https://github.com/o/r/issues/331) or one of its comments
> E             acceptance criterion 1 has the source https://github.com/o/r/issues/330, which is not this issue (https://github.com/o/r/issues/331) or one of its comments
> E           assert ('acceptance criterion 2' in '::error title=Planner output rejected::acceptance criterion 1 has the source https://github.com/o/r/issues/330, which... https://github.com/o/r/issues/330, which is not this issue (https://github.com/o/r/issues/331) or one of its comments')
> 
> tests/test_parent_source.py:127: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_parent_source.py::test_any_other_issue_is_still_rejected_naming_the_criterion_and_the_source - AssertionError: 334.2 (another issue): the rejection does not name acceptance criterion 2 and its source https://github.com/o/r/issues/329:
>   ::error title=Planner output rejected::acceptance criterion 1 has the source https://github.com/o/r

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned the small fix as one user story: a criterion's source may be the story's own issue, its parent issue, or a comment on either; any other issue is rejected naming the criterion and source; the plan review's check of the owner's words accepts the parent too.",
          "It reverted its change to tests/test_autopilot_river.py and dropped the wider checks and the prompt changes."],
  "decided": ["When GitHub cannot say which issue is the parent, only the story's own issue counts.",
              "Only the direct parent counts, not issues further up the tree; the wider version stays in #335."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now covers exactly the owner's small fix, every criterion has a test that fails today because the feature is missing, and both earlier blockers are resolved.",
 "blockers": [],
 "notes": [
  {"text": "The planner's check learns the parent from a parent.json file in the starting pack; the worker should make sure only code writes that file, since a planner that could write it could name any issue as its parent.",
   "evidence": "tests/test_parent_source.py docstring: the planner's check reads parent.json from the pack named by $PACK; the plan's scope is dokima/planner.py and dokima/agent.py."}
 ],
 "resolved": ["B4", "B5"],
 "issues_found": [],
 "asks": [
  {"ask": "A criterion's source may be the story's own issue, its parent issue, or a comment on either.", "source": "https://github.com/dokima-dev/dokima/issues/334", "criterion": "334.1"},
  {"ask": "Any other issue is still rejected, naming the criterion and the source.", "source": "https://github.com/dokima-dev/dokima/issues/334", "criterion": "334.2"},
  {"ask": "The reviewer's check that my words were really said there accepts the parent too.", "source": "https://github.com/dokima-dev/dokima/issues/334", "criterion": "334.3"},
  {"ask": "Back to th
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"summary": "The plan now covers.*resolved.",/"summary": "The plan now covers exactly the owner'"'"'s small fix, each criterion has a test failing today for the right reason, and both blockers are resolved.",/' /tmp/dokima-out/review.json; grep '"summary"' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 334 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> "summary": "The plan now covers exactly the owner's small fix, each criterion has a test failing today for the right reason, and both blockers are resolved.",
> rc=0

**Agent:** I approved the plan for #334, and both earlier blockers (B4 and B5) are resolved. The hand-back at `/tmp/dokima-out/review.json` passes both code checks.

**What the plan now covers.** The plan now holds only the small fix you asked for in your 14:24 comment and confirmed at 14:48, as one user story:
- **334.1:** A criterion's source may be the story's own issue, its parent issue, or a comment on either.
- **334.2:** Any other issue is rejected, and the rejection names the criterion and the source. That includes another issue in this repo, a comment on it, and #3301, whose number starts with the parent's. A passing parent case sits next to each rejection.
- **334.3:** The reviewer's check that your words were really said there accepts the parent too. That covers both the code check of a plan review and the autopilot decision. A comment on the parent by someone who isn't a code owner is still rejected.
- **334.4:** If GitHub can't say which issue is the parent, only the story's own issue counts.

**Earlier blockers.**
- **B4:** The planner undid its change to `tests/test_autopilot_river.py`. Only `tests/test_parent_source.py` differs from main.
- **B5:** The planner dropped the wider checks, the reviewer-pack additions and the prompt changes, and took `dokima/roles/` out of the files it will touch. The plan says they belong to #335.

**Tests.** I ran `pytest -q tests/test_parent_source.py` and all 6 tests fail today because the feature is missing, not because of a crash or bad setup. For example, today's check rejects a criterion citing the parent #330, and the starting pack doesn't name the parent yet.

**One note for the worker (not a blocker).** The planner's check will learn the parent from a `parent.json` file in the starting pack. If the planner itself could write that file, it could name any issue as its parent, so only code should write it.

All four of your asks map to a criterion. The plan has no questions, so there were no assumptions to judge.
