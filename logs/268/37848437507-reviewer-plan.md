# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37848437507

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #265, story 1</summary>
> 
> **Part of:** #265 Issues the reviewer finds are filed automatically, parked and labeled filed by Dokima
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue the moment its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> **Context:** Today only a review's hand-back has issues_found (title, why, evidence): dokima/agent.py problems_shape() checks it at line 773 and render() lists it as propos

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -20; wc -l tests/test_filed_issues.py; cat tests/test_filed_issues.py
```

> <persisted-output>
> Output too large (33.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/1357baa9-0cae-4183-a903-9c83ecbbe31e/tool-results/bfl9l3aa5.txt
> 
> Preview (first 2KB):
> commit 8f2c6eaf83c6fbec592ed0bbb04651643f8fef1e
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:40:20 2026 +0000
> 
>     planner for #268 (run 37846922154)
> 
>  tests/test_filed_issues.py | 590 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 590 insertions(+)
> 590 tests/test_filed_issues.py
> """Every issue an agent finds outside its own is filed by code at the end of its run, parked and labeled (#268).
> 
> Before this, only a review could list issues it found, and they stayed proposals on its card until someone filed them
> by hand (a `/issue` command was only planned). #222 showed the cost: the no-PR bug was found, never filed, and broke
> main. Now the planner's plan.json, the worker's work.json and the reviewer's review.json all take the same field,
> issues_found ({title, why, evidence}), and the run that hands them back files each one once its hand-back passes.
> 
> These tests run the agents through the whole agent workflow (.github/workflows/agent.yml), the way GitHub runs it,
> with the machine from test_start.py and the fake GitHub of test_automerge.py, on issue #57. The "plan" machine holds
> #57 planned, its plan approved and `/work` said, with no pull request; the "pr" machine holds the same story built a

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,330p tests/test_filed_issues.py
```

> """Every issue an agent finds outside its own is filed by code at the end of its run, parked and labeled (#268).
> 
> Before this, only a review could list issues it found, and they stayed proposals on its card until someone filed them
> by hand (a `/issue` command was only planned). #222 showed the cost: the no-PR bug was found, never filed, and broke
> main. Now the planner's plan.json, the worker's work.json and the reviewer's review.json all take the same field,
> issues_found ({title, why, evidence}), and the run that hands them back files each one once its hand-back passes.
> 
> These tests run the agents through the whole agent workflow (.github/workflows/agent.yml), the way GitHub runs it,
> with the machine from test_start.py and the fake GitHub of test_automerge.py, on issue #57. The "plan" machine holds
> #57 planned, its plan approved and `/work` said, with no pull request; the "pr" machine holds the same story built as
> pull request #60. The fake Claude Code hands back what the test chose, in the file of the run's role; a planner also
> writes its one test (tests/test_x.py::test_a, failing today), so its hand-back passes the planner's check. Runs can
> follow one another on the same machine, so a later run sees what an earlier one filed.
> 
> Every key the workflow makes is told apart: each app-token step gives the key `key-<its id>` (key-app for the one
> made after the agent), so a test can see which key filed an issue.
> 
> The fake GitHub is taught to keep the issues code files (filed.json: 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 330,590p tests/test_filed_issues.py
```

> """The titles of every issue filed so far, oldest first."""
>     return [i["title"] for i in m.filed()]
> 
> 
> def shown(m):
>     """The newest run's record comment as the owner reads it, without its folded JSON."""
>     return re.sub(r"```json\n.*?\n```", "", m.record()["body"], flags=re.S)
> 
> 
> def every_agent(tmp_path, *found, **kw):
>     """One run of each agent on its own fresh machine, each handing back these findings: [(case, machine)]."""
>     out = []
>     for case, role, stage, handback in (("planner", "planner", "plan", plan_handback(*found)),
>                                         ("plan review", "reviewer", "plan", plan_review(*found)),
>                                         ("worker", "worker", "pr", work_handback(*found)),
>                                         ("code review", "reviewer", "pr", code_review(*found))):
>         m = Agents(tmp_path / case.replace(" ", "-"), stage, **kw)
>         m.run(role, handback)
>         out.append((case, m))
>     return out
> 
> 
> def test_every_issue_any_agent_finds_is_filed_parked_and_labeled(record_property, tmp_path):
>     """Each issue the planner, the worker or a review finds is filed by itself in that run, parked and labeled filed-by-dokima.
> 
>     Runs the planner, a plan review, the worker and a code review of #57, each finding two issues, with no owner
>     command after any, and checks each run filed exactly one issue per finding, titled with the finding's own title,
>     carrying exactly the labels parked and filed-by-dokima and nothing 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_filed_issues.py -x -q 2>&1 | tail -5; timeout 1200 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E  +(Assertion|268)|[0-9]+ (passed|failed))|passed|failed" | head -40
```

> 268.1: code review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
>   268.1: dokima/roles/planner.md does not give the planner's hand-back the field "issues_found": [{"title": ..., "why": ..., "evidence": ...}]
>   268.1: dokima/roles/worker.md does not give the worker's hand-back the field "issues_found": [{"title": ..., "why": ..., "evidence": ...}]
> assert not ['planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []', 'pla... review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []', ...]
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: worker (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: code review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: planner (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo without the labels) found two issues but did not file exactly tho

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn -i "propos\|issues_found" tests/*.py | grep -v test_filed_issues | head -20; grep -n "issues_found\|propos" dokima/roles/*.md AGENTS.md | head
```

> tests/test_agent.py:25:    assert agent.problems_review({**GOOD_REVIEW, "issues_found": found}) == []
> tests/test_agent.py:26:    assert agent.problems_review({**GOOD_REVIEW, "issues_found": [{"title": "x"}]}) == ["issue found 1 needs a title, why and evidence"]
> tests/test_agent.py:27:    assert "1. Board ignores closed PRs: cards go stale" in agent.render(rec("reviewer", "plan", {**GOOD_REVIEW, "issues_found": found}))
> tests/test_automerge.py:306:         "blockers": [], "notes": [], "outside_plan": [], "resolved": [], "issues_found": []}
> tests/test_autopilot_river.py:296:    r = run(monkeypatch, tmp_path / "river", "reviewer", "plan", ts.SPLIT_PROPOSED, ON)
> tests/test_autopilot_river.py:335:    r = run(monkeypatch, tmp_path / "split", "reviewer", "plan", ts.SPLIT_PROPOSED, off)
> tests/test_feature_check.py:1:"""The planner's check on a proposed split: every story is well formed and its dependencies form no loop.
> tests/test_run_cards.py:83:APPROVE = review("approve", issues_found=[{"title": "Board ignores closed PRs", "why": "cards go stale", "evidence": "board.py:40"}])
> tests/test_run_cards.py:163:    """The planner's card shows on top the plan, or its questions beside the plan, or the proposed split.
> tests/test_run_cards.py:288:    """The reviewer's card says it passed, or lists only the criteria it blocks on with their notes, and its proposed issues.
> tests/test_run_cards.py:290:    Draws a plan review that approves, with asks on 9.1 to 9.4 and one proposed issue, and checks

**Agent:** All seven new tests fail today for the right reason: nothing gets filed yet, and the planner and worker prompts don't have the field yet. I'm writing the review now.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned five criteria and two non-functional requirements, one for each line of the story #265 handed down.",
          "Wrote seven tests in tests/test_filed_issues.py. They run the planner, a plan review, the worker and a code review through agent.yml against a fake GitHub that can file issues."],
  "decided": ["Filing happens in the code that checks the hand-back, with the key made after the agent. No /issue command is added."],
  "open": ["Filing findings from a split's stories, and editing an earlier filed issue, are out of scope."]},
 "verdict": "approve",
 "summary": "The plan keeps every line of the story, and each test runs all four agent runs through the real workflow. Today every test fails because nothing is filed yet.",
 "blockers": [],
 "notes": [
  {"text": "Existing card tests still expect a review's findings listed as plain lines on top of the card. The worker should keep that wording for a card drawn with no filed numbers, because tests/test_run_cards.py is outside the plan's scope.",
   "evidence": "tests/test_run_cards.py:299 and tests/test_agent.py:27 assert '1. Board ignores closed PRs: cards go stale' in render() output"},
  {"text": "The rejected hand-back test covers a planner, a worker and a plan review, but not a rejected code review. The code path is shared, so this is not a blocker.",
   "evidence": "tests/test_filed_issues.py::test_a_rejected_handback_files_nothing runs three cases"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The planner's, the worker's and the reviewer's hand-backs each take the same found-issues field, and every issue listed there is filed in that agent's own run, with no command, as its own GitHub issue titled with the finding's title and labeled exactly parked and filed-by-dokima, also on a repo that has neither label yet; a hand-back that lists none files none.", "source": "ht
```

> rc=0

**Agent:** I approved the plan for #268. The review is saved at `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **Every ask is covered.** I matched all five acceptance criteria and both non-functional requirements from the issue to the plan's criteria 268.1 to 268.7. None are missing, and the plan has no questions for the owner.
- **The tests fail today for the right reason.** I ran `tests/test_filed_issues.py` and all seven tests fail. In every agent run nothing gets filed (`filed: []`), and the planner and worker prompts don't have the `issues_found` field yet. The hand-backs themselves pass today's checks, so no test fails just because its setup is broken.
- **The tests should catch any departure from the plan.** They:
  - run all four agent runs through the real `agent.yml`;
  - require exactly the two labels, including on a repo that has neither yet;
  - check that each filed issue links the exact comment holding the run's record;
  - cover a repeated finding in different letter case and spacing, an already filed issue that was closed, and later runs by other agents;
  - check that nothing gets linked to a filed issue, put on autopilot or started on it;
  - check that the key used to file is made only after the agent and the hand-back check.

I left two notes, neither blocking:

1. `tests/test_run_cards.py:299` and `tests/test_agent.py:27` still expect a review's findings listed as plain lines on its card. That file isn't in the plan's scope, so the worker should keep that wording for a card drawn with no filed issue numbers.
2. The test for rejected hand-backs covers the planner, the worker and a plan review, but not a code review. The two review types share the same filing code, so I didn't block on it.
