# reviewer (plan) for #315

Run: https://github.com/dokima-dev/dokima/actions/runs/37887986607

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (38.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/88aa2d0f-2d81-4172-8bef-6373daf9584a/tool-results/bln5lpsxx.txt
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
> 03-planner.json
> # Issue #315: The PR card is redrawn after merge and shows the true Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #315](https://github.com/dokima-dev/dokima/issues/315)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> PR #312 merged at 04:44, but its card still shows All tests running, Code review blan

`2. Bash`
```
cd /tmp/pack; sed -n '/## Comments/,$p' issue.md | head -150
```

> ## Comments
> 
> ### RezaSoleymanifar on issue #315 (2026-10-09T04:47:23Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #315 (2026-10-09T04:47:52Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #315 (2026-10-09T04:47:54Z)
> 
> Autopilot is on for #315. Planning started for #315, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #315 (2026-10-09T04:48:04Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** The owner can trust the card on any issue or pull request, merged or not, to show where it truly stands.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 
> 1. The issue and pull request cards are redrawn when a check finishes, an agent posts a record, the owner approves or it merges. A command in an issue comment and the card's own edit of the issue redraw nothing.
> 2. After a code owner merges, both cards say Merged with All tests, Code review and Owner approval passed. Code review is found on the pull request, where the review's record is, and links to its run; the owner's merge counts as O

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d,indent=1)[:8000])"
```

> [
>  {
>   "id": "B1",
>   "criterion": "315.5",
>   "test": "tests/test_card_redraw.py::test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run",
>   "problem": "The test only checks that the bot's edit of issue #40 does not share a group with redraws of other targets (PR #5, #6, #7, issue #41). A card.yml that keys every run on its issue or pull request number puts the bot's edit of #40 in the same queue as the owner's edit of #40, so each card write (which edits the issue) cancels a redraw of that issue still waiting its turn. That is the bug the owner described, and the requirement says a waiting redraw is replaced only by a newer redraw.",
>   "evidence": "In a copy of the repo, card.yml's group changed to `card-${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}` makes `pytest -q tests/test_card_redraw.py -k never_dropped` pass (1 passed), while the bot's edit of issue #40 and an owner's edit of issue #40 both land in group 'card-40'.",
>   "fix": "Add an owner's edit of issue #40 to the events, and assert the bot's edit of issue #40 (and the command in an issue comment) does not share its group; fail with '315.5: the bot's edit of issue #40 waits in the group of a redraw of issue #40, so it cancels that redraw'.",
>   "fixer": "planner"
>  }
> ]{
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37887682905",
>  "commit_before": "0f8ea73117858ccbce71f5de1d603c8c1dc1d4e5",
>  "started_by": "dok

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; grep -n -i "queue" issue.md | head; python3 -c "
import json;d=json.load(open('in/03-planner.json'));h=d['handback'];print(json.dumps({k:v for k,v in h.items() if k not in('acceptance_criteria',)},indent=1)[:5000])"; diff <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1))") <(python3 -c "import json;print(json.dumps(json.load(open('in/03-planner.json'))['handback'],indent=1))") | head -30
```

> 26:### RezaSoleymanifar on issue #315 (2026-10-09T04:47:23Z)
> 30:### dokima-runtime on issue #315 (2026-10-09T04:47:52Z)
> 34:### dokima-runtime on issue #315 (2026-10-09T04:47:54Z)
> 39:### dokima-runtime on issue #315 (2026-10-09T04:48:04Z)
> 200:### RezaSoleymanifar on issue #315 (2026-10-09T04:52:37Z)
> 204:### dokima-runtime on issue #315 (2026-10-09T04:52:59Z)
> 214:### dokima-runtime on issue #315 (2026-10-09T05:15:03Z)
> 363:### dokima-runtime on issue #315 (2026-10-09T05:17:02Z)
> 531:### dokima-runtime on issue #315 (2026-10-09T05:18:51Z)
> 57:- Every redraw runs main's copy of the card code. A redraw waiting its turn is only ever replaced by a newer redraw of the same pull request or issue. (A pull request must never draw its own card. Today every card write edits the issue, which starts a card run in the one shared queue and cancels the redraw waiting there (card.yml concurrency group `card`), so cards go stale.; Humans are free; bots are compliant)
> 137:    "why": "A pull request must never draw its own card. Today every card write edits the issue, which starts a card run in the one shared queue and cancels the redraw waiting there (card.yml concurrency group `card`), so cards go stale.",
> 202:/plan Found the cause: every card redraw in the repo shares one queue (the card workflow's concurrency group is just "card"), and GitHub keeps only one waiting run per queue. During a busy stretch, newer redraws for other issues replaced the waiting redraw for #312, so its card kept an older 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 0f8ea73 15432fc --stat; git diff 0f8ea73 15432fc -- tests/ | head -200; timeout 600 pytest -q tests/test_card_redraw.py 2>&1 | tail -20
```

> tests/test_card_redraw.py | 20 +++++++++++++-------
>  1 file changed, 13 insertions(+), 7 deletions(-)
> diff --git a/tests/test_card_redraw.py b/tests/test_card_redraw.py
> index 01fc104..b1dd06a 100644
> --- a/tests/test_card_redraw.py
> +++ b/tests/test_card_redraw.py
> @@ -817,10 +817,11 @@ def test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run(record_
>      """A waiting redraw is never dropped for another PR's redraw or an idle run.
>  
>      GitHub keeps one waiting run per concurrency group and cancels it when a newer one arrives. card.yml's group
> -    is read for redraws of PR #5 (two checks), PR #6 (merge), PR #7 (approval) and issue #41 (an owner's edit), and
> -    for two runs that draw nothing: the bot's own edit of an issue (each card write makes one) and a command typed
> -    in an issue comment. The two redraws of PR #5 must share a group, each other target must have its own, no run
> -    that draws nothing may sit in a redraw's group, and no run may cancel one already running. Proves 315.5."""
> +    is read for redraws of PR #5 (two checks), PR #6 (merge), PR #7 (approval), issue #41 and issue #40 (an owner's
> +    edit of each), and for two runs that draw nothing: the bot's own edit of issue #40 (each card write makes one)
> +    and a command typed in an issue comment. The two redraws of PR #5 must share a group, each other issue and pull
> +    request must have its own, no run that draws nothing may sit in a redraw's group (not even the group of the
> +    issue i

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -B2 -A4 concurrency .github/workflows/card.yml; sed -n 780,816p tests/test_card_redraw.py
```

> 10-  issues:
> 11-    types: [opened, edited]
> 12:concurrency:
> 13-  group: card
> 14-  cancel-in-progress: false
> 15-permissions:
> 16-  contents: read
>     pull_request_review, pull_request_review_comment) and must never check out a pull request's code; agent.yml's
>     redraw after a record must run the runtime copied from main, not the branch it has checked out. Proves 315.5."""
>     record_property("proves", "315.5")
>     wf = card_yml()
>     on = wf.get("on")
>     for ev in ("pull_request", "pull_request_review", "pull_request_review_comment"):
>         assert listed(on, ev) is None, f"315.5: card.yml listens to {ev}, which runs the pull request's own copy"
>     for job in (wf.get("jobs") or {}).values():
>         for step in job.get("steps") or []:
>             if "checkout" in str(step.get("uses")):
>                 assert not (step.get("with") or {}).get("ref"), \
>                     f"315.5: card.yml checks out {step['with']['ref']}, so a pull request's code could draw its card"
>     found = agent_card_steps(tmp_path)
>     assert found, "315.5: agent.yml runs no card redraw after it posts the run's record"
>     wheres = [card_call(calls)[0] for _, calls in found]
>     assert "main" in wheres and "branch" not in wheres, \
>         f"315.5: agent.yml's redraw runs the card code from {wheres}, not only from main's copy in /tmp/runtime"
> 
> 
> def groups(events):
>     """The card job's concurrency group for each event, and whether it cancels a running run."""
>     wf = card_yml()
>     job = next(iter(w

**Agent:** Checking whether the queue test now catches the bug from last round.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cp .github/workflows/card.yml /tmp/card.bak
sed -i "s/^  group: card$/  group: card-\${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}/" .github/workflows/card.yml; grep -n group: .github/workflows/card.yml; pytest -q tests/test_card_redraw.py -k never_dropped 2>&1 | grep -E "315.5|passed|failed"
sed -i "s/^  group: card-.*/  group: card-\${{ (github.event_name == 'issues' \&\& github.event.sender.type == 'Bot') \&\& github.run_id || github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}/" .github/workflows/card.yml; grep -n group: .github/workflows/card.yml; pytest -q tests/test_card_redraw.py -k never_dropped 2>&1 | grep -E "315.5|passed|failed"
cp /tmp/card.bak .github/workflows/card.yml; git status --short
```

> 13:  group: card-${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}
>         issue it edits), and no run may cancel one already running. Proves 315.5."""
>         record_property("proves", "315.5")
>             assert group, f"315.5: {name} waits in no concurrency group"
>             assert not cancels, f"315.5: {name} cancels a card run already drawing"
>             f"315.5: two redraws of PR #5 wait in different groups ({g['all tests on PR #5'][0]!r}, " \
>                 f"315.5: {name} and {seen.get(g[name][0])} share the group {g[name][0]!r}, so one drops the other's redraw"
>                 f"315.5: the {name} waits in the group {g[name][0]!r} of a redraw of issue #40, so it cancels that redraw"
> E           AssertionError: 315.5: the bot's edit of issue #40 waits in the group 'card-40' of a redraw of issue #40, so it cancels that redraw
> FAILED tests/test_card_redraw.py::test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run - AssertionError: 315.5: the bot's edit of issue #40 waits in the group 'card-40' of a redraw of issue #40, so it cancels that redraw
> 1 failed, 8 deselected in 0.06s
> 13:  group: card-${{ (github.event_name == 'issues' && github.event.sender.type == 'Bot') && github.run_id || github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}
> 1 passed, 8 deselected in 0.03s

**Agent:** B1 is fixed: the per-number group now fails the test, and a group that keeps the bot's edit separate passes. Writing the review.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added an owner's edit of issue #40 to the queue test, which now fails when the card's own edit of issue #40 or a command waits in the same queue as that redraw."],
  "decided": ["The requirement now says each issue and pull request has its own redraw queue, and a waiting redraw is replaced only by a newer redraw of the same issue or pull request, never by another one's redraw, the card's own edit of the issue or a command."],
  "open": []},
 "verdict": "approve",
 "summary": "Every ask is planned, and the queue test now fails when the card's own edit of an issue would cancel a waiting redraw of that issue.",
 "blockers": [],
 "notes": [
  {"text": "The approval case in 315.1 relies on the commands workflow finishing after a pull request review, so the worker should keep card.yml listening to the commands workflow, not to pull_request_review.",
   "evidence": "tests/test_card_redraw.py 315.1 approval case uses workflow_run('commands', event='pull_request_review'); the plan's out of scope names this route."}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "A card is redrawn whenever anything it shows changes: a check finishing, a review record, an approval, a merge.", "source": "https://github.com/dokima-dev/dokima/issues/315", "criterion": "315.1"},
  {"ask": "Its last drawing always matches the truth, including after merge.", "source": "https://github.com/dokima-dev/dokima/issues/315", "criterion": "315.2"},
  {"ask": "The PR card finds the code review on the PR exactly as the issue card does", "source": "https://github.com/dokima-dev/dokima/issues/315", "criterion": "315.2"},
  {"ask": "a merge by the owner counts as Owner approval", "source": "https://github.com/dokima-dev/dokima/issues/315", "criterion": "315.2"},
  {"ask": "On each acceptance criterion, only the criterion sentence itself is the link to its run, not the explan
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"Every ask is planned, and the queue test now fails when the card.s own edit of an issue would cancel a waiting redraw of that issue."/"Every ask is planned, and the queue test now fails when the card'"'"'s own issue edit would cancel a waiting redraw of that issue."/' /tmp/dokima-out/review.json; grep summary /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 315 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> "summary": "Every ask is planned, and the queue test now fails when the card's own issue edit would cancel a waiting redraw of that issue.",
> rc=0

**Agent:** I approved the plan for #315. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass with no warnings.

- **Last round's blocker (B1) is resolved.** I tried two versions of the redraw queue setting in `card.yml`:
  - **Bug kept:** one queue per issue or pull request number, with the card's own edit of issue #40 sharing a queue with a redraw of #40. The test now fails with: "the bot's edit of issue #40 waits in the group 'card-40' of a redraw of issue #40, so it cancels that redraw".
  - **Bug fixed:** the same setting, but the bot's edit gets a queue of its own. The test passes.

  I put `card.yml` back afterwards, and the working tree is clean.
- **Every new test fails today, for the right reason.** All 9 tests in `tests/test_card_redraw.py` fail because the feature is missing, not from a crash or a bad path.
- **All 7 of the owner's asks are covered.** The new one, "Give each issue and pull request its own redraw queue", from the owner's `/plan` comment, is now spelled out in the plan's queue rule (the non-functional requirement tied to 315.5).
- **One note for the worker:** keep `card.yml` listening to the commands workflow, not to pull request reviews directly. The approval case in 315.1 depends on that.

The plan has no questions for the owner, so there were no assumptions to judge.
