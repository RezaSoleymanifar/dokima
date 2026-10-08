# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37851929554

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (69.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fce24043-cb0e-4c92-b696-1bcd53e16d5f/tool-results/bhkcsehe9.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> Issues the planner, the worker or the reviewer find outside their own issue are filed on GitHub by code at the end of the run, parked and labeled filed-by-dokima.
> 
> **Review**
> 
> [PR #274](https://github.com/dokima-dev/dokima/pull/274) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/274/files)
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> <table>
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokim

`2. Bash`
```
cd /tmp/pack; sed -n '/Original issue\|dokima-card-end\|<!-- dokima/,$p' issue.md | grep -v '^$' | head -400 | tail -330
```

> <details><summary><b>Scope</b></summary>
> - dokima/agent.py
> - dokima/planner.py
> - dokima/roles/planner.md
> - dokima/roles/worker.md
> - dokima/roles/reviewer.md
> - .github/workflows/agent.yml
> - AGENTS.md
> </details>
> <details><summary><b>Out of scope</b></summary>
> - Triaging, prioritizing or planning a filed issue: it stays parked until the owner picks it up.
> - A /issue command: filing needs no command now.
> - Filing findings from a split's stories or from any run other than the planner, the worker and the reviewer.
> - Re-filing or editing an issue Dokima filed earlier when a later run finds it again with a new why.
> </details>
> <details><summary><b>Tests</b></summary>
> - 268.1: tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled
> - 268.2: tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record
> - 268.3: tests/test_filed_issues.py::test_a_filed_issue_gets_nothing_more_than_filing
> - 268.4: tests/test_filed_issues.py::test_the_same_finding_is_never_filed_twice
> - 268.5: tests/test_filed_issues.py::test_the_card_names_each_filed_issue, tests/test_filed_issues.py::test_a_finding_github_refuses_to_file_says_why_on_the_card
> - 268.6: tests/test_filed_issues.py::test_a_rejected_handback_files_nothing
> - 268.7: tests/test_filed_issues.py::test_the_key_that_files_is_made_only_after_the_agent_and_the_check
> </details>
> <details><summary>Full record</summary>
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37846

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/05-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:1500]);h=d['handback'];print(h.get('test_changes'));print(h.get('questions'));print(h.get('summary'))"; diff <(python3 -c "import json;print(json.dumps(json.load(open('in/01-planner.json'))['handback'],indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1,sort_keys=True))")
```

> []{
>  "role": "planner",
>  "stage": null,
>  "run_id": "37850995733",
>  "commit_before": "50b543c3cc11ea7de02cbad9636c9ee24fc982fa",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 393270,
>   "turns": 10,
>   "cost_usd": 0.427213,
>   "tokens_in": 351071,
>   "tokens_out": 5083
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/268/37850995733-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37850995733",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> {'tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled': "The planner check merged in #246 now requires every new test's docstring to name its criterion below a short first line; this test's first line was shortened and 'Proves 268.k.' added, with its checks unchanged. Also, the fake planner test (PLANNER_TEST) shared by every test in this file now says 'Proves 57.1.' under its first line; without it every fake planner run was rejected by the same check and all 8 tests failed before checking any filing (B1).", 'tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record': "The planner check merged in #246 now requires every new test's docstring to name its criterion below a short first line; this test's first line was shortened and 'Proves 268.k.' added, with its checks unchanged.", 'tests/test_filed_issues.py::test_a_filed_issue_gets_nothing_more_than_filing': "Th

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 50b543c fbc77f5 --stat; git diff 50b543c fbc77f5 -- tests/ | head -150
```

> tests/test_filed_issues.py | 52 +++++++++++++++++++++++++++++++++-------------
>  1 file changed, 38 insertions(+), 14 deletions(-)
> diff --git a/tests/test_filed_issues.py b/tests/test_filed_issues.py
> index 5699d6e..87286bb 100644
> --- a/tests/test_filed_issues.py
> +++ b/tests/test_filed_issues.py
> @@ -1,4 +1,4 @@
> -"""Every issue an agent finds outside its own is filed by code at the end of its run, parked and labeled (#268).
> +"""Issues any agent finds outside its own are filed at the end of its run (#268).
>  
>  Before this, only a review could list issues it found, and they stayed proposals on its card until someone filed them
>  by hand (a `/issue` command was only planned). #222 showed the cost: the no-PR bug was found, never filed, and broke
> @@ -57,7 +57,10 @@ FIND_D = {"title": "The wiki step skips renamed pages", "why": "A renamed page k
>            "evidence": "dokima/trail.py:40 matches pages by file name only"}
>  
>  PLANNER_TEST = '''def test_a(record_property):
> -    """The fix is in."""
> +    """The fix is in.
> +
> +    Proves 57.1.
> +    """
>      record_property("proves", "57.1")
>      assert False, "57.1: the fix is not built yet"
>  '''
> @@ -194,7 +197,9 @@ def fake_gh():
>  
>  
>  def keyed(job):
> -    """The job with each app-token step giving its own key, `key-<step id>`, so a filed issue shows which key made it."""
> +    """The job with each app-token step giving its own key, `key-<step id>`.
> +
> +    So a filed issue shows which key made it."""
>      steps = []
>      for s in job["steps"]:

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 500 python -m pytest -q tests/test_filed_issues.py 2>&1 | tail -3; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1|tail -1; cp tests/test_filed_issues.py /tmp/mainwt/tests/; cd /tmp/mainwt && timeout 500 python -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^E .*(268|Error)|passed|failed" | head -20
```

> ........                                                                 [100%]
> 8 passed in 86.69s (0:01:26)
> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: worker (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: code review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: planner (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: worker (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: code review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: dokima/roles/planner.md does not give the planner's hand-back the field "issues_found": [{"title": ..., "why": ..., "evidence": ...}]
> E         268.1: dokima/roles/worker.md does not give the worker's hand-back the field "issues_found": [{"title": ..., "why": ..., "evidence": ...}]
> E       AssertionError: 268.2: plan

**Agent:** The new tests pass on this branch (8 passed) and fail on main because nothing is filed yet. Next I'll write the review.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/02-reviewer-plan.json'))['handback']['asks']
r={"previous_step":{"did":["Added 'Proves 57.1.' to the fake planner's test that every test in tests/test_filed_issues.py uses, so the planner check from #246 no longer rejects it (B1 of the code review).",
"Shortened each test's docstring first line and added 'Proves 268.k.', with the checks unchanged, and listed every change in test_changes."],
"decided":["Reworded criterion 268.3 with the same meaning: no sub-issue, no blocked-by link, no stage starting on it, and off autopilot."],
"open":[]},
"verdict":"approve",
"summary":"The planner fixed the test that stopped all eight proofs from running and changed nothing they check; they now pass against the worker's code and still fail on main because nothing is filed there.",
"blockers":[],
"notes":[{"text":"Only docstrings changed in tests/test_filed_issues.py since the worker's run, and the criteria are unchanged in meaning, so the code review can go on with the same tests.","evidence":"git diff 50b543c fbc77f5 -- tests/: docstring lines only; pytest -q tests/test_filed_issues.py on try/issue-268: 8 passed; the same file on main: 8 failed, e.g. '268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []'"}],
"outside_plan":[],"resolved":[],"issues_found":[],"asks":prev}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #268 again. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **What the planner changed:** The code review had blocked the work (B1): the shared fake planner test in `tests/test_filed_issues.py` didn't name its criterion. The planner check added in #246 now requires that, so it rejected the fake planner and all 8 proofs failed before they tested any filing. The planner added "Proves 57.1." to that test. It also shortened each test's first docstring line and added "Proves 268.k.", and listed every change with its reason.
- **What it left alone:** Since the worker's run, only docstrings changed in the test file, and nothing the tests check. Criterion 268.3 was reworded but means the same thing.
- **Tests on this branch:** all 8 pass against the worker's code.
- **Tests on main:** all 8 fail for the right reason. Nothing gets filed there, for example: "268.1: planner … did not file exactly those two by their titles; filed: []".
- **Owner's asks:** every one still has its criterion (268.1 to 268.7). The plan has no questions for the owner.

I listed B1 as fixed in a note, not as resolved: it came from the code review, and this plan review had no open blockers of its own. It should be closed when the code review runs again.
