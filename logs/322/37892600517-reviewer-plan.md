# reviewer (plan) for #322

Run: https://github.com/dokima-dev/dokima/actions/runs/37892600517

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (35.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2e725ca2-6452-4c11-a622-da5a3e058ce9/tool-results/b45owxhtx.txt
> 
> Preview (first 2KB):
> # Issue #322: A PR's card shows its true state after merge, however fast I merge
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A PR's card can stay frozen after merge: a late check can't find the merged PR, and merging never redraws the card.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #322](https://github.com/dokima-dev/dokima/issues/322)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #315, #183
> 
> **User story:** Every merged PR and its issue show Merged with the true Definition of Done, however soon after the checks the owner merges.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** A check th

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-body-marker\|^---/,$p' issue.md | head -0; grep -n "" issue.md | sed -n '1,400p' | cut -c1-600 | grep -v "^[0-9]*:<img\|icons" | head -150
```

> 1:# Issue #322: A PR's card shows its true state after merge, however fast I merge
> 2:
> 3:<!-- dokima-card -->
> 4:<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> 5:A PR's card can stay frozen after merge: a late check can't find the merged PR, and merging never redraws the card.
> 6:
> 8:
> 9:[issue #322](https://github.com/dokima-dev/dokima/issues/322)
> 10:
> 12:
> 13:**User story:** Every merged PR and its issue show Merged with the true Definition of Done, however soon after the checks the owner merges.
> 14:
> 16:
> 19:  - <a href="https://github.com/dokima-dev/dokima/issues/322">Source</a>
> 22:  - <a href="https://github.com/dokima-dev/dokima/issues/322">Source</a>
> 25:  - <a href="https://github.com/dokima-dev/dokima/issues/322">Source</a>
> 28:  - <a href="https://github.com/dokima-dev/dokima/issues/322">Source</a>
> 29:
> 30:<details><summary><b>Non-functional requirements</b></summary>
> 31:
> 34:
> 35:</details>
> 36:
> 37:**Scope:**
> 38:
> 39:- .github/workflows/card.yml
> 40:- dokima/card.py
> 41:- tests/test_card_after_merge.py
> 42:
> 43:**Out of scope:**
> 44:
> 45:- Redrawing every other stale card in the repo; that is #315's last ask and #183's backfill.
> 46:- Redrawing the card on review records or approvals; #315 asks for that.
> 47:- Changing what the card shows or how it is drawn; only when it is drawn and for which PR.
> 48:
> 50:
> 51:<!-- /dokima-card -->
> 52:
> 53:<!-- dokima-ask -->
> 54:
> 55:A PR's card can stay frozen after merge. On #246 the tests finished at 21:36:42 and I merged at 21:36:5

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; ls in; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> 65:### RezaSoleymanifar on issue #322 (2026-10-09T05:37:29Z)
> 69:### dokima-runtime on issue #322 (2026-10-09T05:37:51Z)
> 73:### dokima-runtime on issue #322 (2026-10-09T05:37:54Z)
> 78:### dokima-runtime on issue #322 (2026-10-09T05:38:03Z)
> 248:### dokima-runtime on issue #322 (2026-10-09T05:55:25Z)
> 384:### RezaSoleymanifar on issue #322 (2026-10-09T06:06:50Z)
> 388:### dokima-runtime on issue #322 (2026-10-09T06:07:09Z)
> 554:### dokima-runtime on issue #322 (2026-10-09T06:15:28Z)
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> []{
>  "kind": "user_story",
>  "summary": "A PR's card can stay frozen after merge: a late check can't find the merged PR, and merging never redraws the card.",
>  "user_story": "Every merged PR and its issue show Merged with the true Definition of Done, however soon after the checks the owner merges.",
>  "acceptance_criteria": [
>   {
>    "text": "A check that finishes after its PR merged still writes the card into that PR and its issue. Before, the run found no PR and wrote no card, as on #246. A commit with no PR still gets no card.",
>    "source": "https://github.com/dokima-dev/dokima/issues/322"
>   },
>   {
>    "text": "Merging a PR, by the owner or by autopilot, redraws its card and its issue's card. Both show Merged, with All tests, Code review and Owner approval as they truly ended.",
>    "source": "https://github.com/dokima-dev/dokima/issues/322"
>   },
>   {
>    "text": "The card run a merge starts always has the last word. It waits for a card run already going 

`4. Bash`
```
cd /tmp/pack; sed -n 248,300p issue.md | cut -c1-1500; sed -n 384,420p issue.md|cut -c1-1500; sed -n 554,600p issue.md | cut -c1-2000
```

> ### dokima-runtime on issue #322 (2026-10-09T05:55:25Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer passed the plan.
> 
> **The plan's assumptions:**
> - Should #246 and #312 be redrawn by you pressing Run workflow once for each after this ships, or should code redraw them by itself with no click from you? Not accepted: The owner wrote '#246 and #312 show the right state once this ships', which does not say who redraws them. The assumption gives the owner a manual step and adds a new way to start the card workflow, so it changes how the system works. The owner has to choose.
> 
> <details><summary><b>Details</b></summary>
> 
> - Every ask is covered and all five tests fail today for the missing feature; the owner still decides how #246 and #312 get redrawn.
> 
> </details>
> 
> <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/note.svg" width="16" height="16" align="absmiddle" alt="note"> Notes</b></summary>
> 
> - This work changes .github/workflows/card.yml, so on autopilot the pull request will stop for the owner before it merges, as AGENTS.md step 6 says. (Plan scope lists .github/workflows/card.yml; AGENTS.md: 'a pull request that changes a workflow file 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -30; wc -l tests/test_card_after_merge.py; cat tests/test_card_after_merge.py
```

> <persisted-output>
> Output too large (30.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2e725ca2-6452-4c11-a622-da5a3e058ce9/tool-results/bber3m3gg.txt
> 
> Preview (first 2KB):
> commit 71787500f9c720aad92f1fd4cde3ea6638f125e6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 06:15:16 2026 +0000
> 
>     planner for #322 (run 37891855247)
> 
>  tests/test_card_after_merge.py | 315 +++++++++++++++++++++++++++++++----------
>  1 file changed, 243 insertions(+), 72 deletions(-)
> 
> commit f3bc2e8300fbb45de83f85c9e43962745eb70ff6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:55:13 2026 +0000
> 
>     planner for #322 (run 37889496489)
> 
>  tests/test_card_after_merge.py | 445 +++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 445 insertions(+)
> 
> commit 1b0cda68b38d1f50d7119bf0eab9ec60953186fb
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 00:29:07 2026 -0500
> 
>     The audit runs once a day in the background, and on the Run workflow button (#318)
>     
>     * planner for #285 (run 37885355622)
>     
>     * worker for #285 (run 37886228614)
>     
>     ---------
>     
> 616 tests/test_card_after_merge.py
> """A PR's card shows its true state after merge, however fast the owner merges (#322).
> 
> On #246 the owner merged twelve seconds after the tests finished; the card run that followed could no longer find 

**Agent:** Checking the planner's revised tests for #322, then running them.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,330p tests/test_card_after_merge.py
```

> """A PR's card shows its true state after merge, however fast the owner merges (#322).
> 
> On #246 the owner merged twelve seconds after the tests finished; the card run that followed could no longer find the
> PR (GitHub's event names no PR once it is merged, and GitHub lists only open PRs for a squash-merged commit), so the
> PR card kept saying All tests was running. These tests read the real `.github/workflows/card.yml`: they work out, for
> one GitHub event, whether the card job runs, its concurrency group and the env its "Write the card" step gets, the way
> GitHub would, then run the real `dokima/card.py` main() with that env against a fake GitHub.
> 
> The fake GitHub (FakeGitHub below) answers `gh` the way GitHub does for these reads:
>     gh api repos/o/r/commits/SHA/pulls          open PRs whose head is SHA, plus the merged PR of a commit on main
>     gh api repos/o/r/pulls?head=o:BRANCH&state=open|closed|all   (any order of query parameters)
>     gh api repos/o/r/pulls?state=...            every PR in that state
>     gh api repos/o/r/pulls/N                    one PR
>     gh api repos/o/r/issues/N/dependencies/blocked_by|blocking, .../sub_issues   none
>     gh api search/issues?q=...SHA...            the PRs whose head is SHA, open or merged
>     gh api graphql ... -F p=N                   the issue PR N closes (closingIssuesReferences)
>     gh api -X PATCH repos/o/r/pulls/N -F body=@FILE   writes the PR's description
> Anything else fails as a refused call would, and is logged in `refuse

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 330,616p tests/test_card_after_merge.py
```

> def pr(number, issue, state="open", merged=False, sha=None, merge_commit=None, card_text=None):
>     """One PR as GitHub's API gives it, closing `issue`.
> 
>     `card_text` puts an older card on top of its description, as code wrote it before."""
>     text = f"Closes #{issue}"
>     if card_text:
>         text = f"{plan.CARD_START}\n{card_text}\n{plan.CARD_END}\n\n{text}"
>     return {"number": number, "state": state, "merged": merged, "merged_at": "2026-10-08T21:36:54Z" if merged else None,
>             "merged_by": {"login": OWNER} if merged else None, "body": text,
>             "html_url": f"https://github.com/{REPO}/pull/{number}", "merge_commit_sha": merge_commit,
>             "head": {"ref": f"try/issue-{issue}", "sha": sha or f"head{number}"}, "base": {"ref": "main"}}
> 
> 
> class FakeGitHub:
>     """GitHub with a few PRs, answering `gh` as described at the top of this file."""
> 
>     def __init__(self, prs, closes):
>         self.prs, self.closes = prs, closes
>         self.refused, self.pr_bodies = [], {}
> 
>     def refuse(self, args):
>         self.refused.append(args)
>         raise subprocess.CalledProcessError(1, ["gh", *args], "", "gh: Not Found (HTTP 404)")
> 
>     def __call__(self, *args, **kw):
>         import json
>         args = [str(a) for a in args]
>         if args[:1] != ["api"]:
>             return self.refuse(args)
>         rest = args[1:]
>         method = "GET"
>         if "-X" in rest:
>             method = rest[rest.index("-X") + 1]
>         path = next((a for a in rest if a.startsw

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_after_merge.py 2>&1 | grep -E "^E .*322|passed|failed|Error" | head -30; cat .github/workflows/card.yml | head -60
```

> E       AssertionError: 322.1: a check finishing after PR #5 merged drew nothing, not issue #40 with its merged PR #5
> /home/runner/work/dokima/dokima/tests/test_card_after_merge.py:507: AssertionError
>         with All tests, Code review and Owner approval passed."""
> E       AssertionError: 322.2: card.yml does not start on a PR closing (pull_request_target types: None)
> tests/test_card_after_merge.py:535: AssertionError
> E       AssertionError: 322.3: card runs for other issues share the merge's group 'card', so they can drop its waiting run
> tests/test_card_after_merge.py:565: AssertionError
>         with All tests, Code review and Owner approval passed. Nothing is run by hand: no Run workflow event is sent."""
> E           AssertionError: 322.4: PR #246's stale card was not redrawn when this change landed on main (drew nothing)
> /home/runner/work/dokima/dokima/tests/test_card_after_merge.py:593: AssertionError
> E       AssertionError: 322.5: card.yml has no pull_request_target trigger
> tests/test_card_after_merge.py:610: AssertionError
> FAILED tests/test_card_after_merge.py::test_a_check_finishing_after_the_merge_still_writes_the_pr_card - AssertionError: 322.1: a check finishing after PR #5 merged drew nothing, not issue #40 with its merged PR #5
> FAILED tests/test_card_after_merge.py::test_merging_a_pr_redraws_its_card_and_its_issues_card - AssertionError: 322.2: card.yml does not start on a PR closing (pull_request_target types: None)
> FAILED tests/test_card_after_merge.py::test_th

`9. Bash`
```
cd /tmp/pack; grep -o "issuecomment-[0-9]*" issue.md | sort -u; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d.get('handback',d)['asks'],indent=0))"; grep -n "315" /home/runner/work/dokima/dokima/AGENTS.md | head
```

> [
> {
> "ask": "The PR card is written whether the PR is open or merged.",
> "source": "https://github.com/dokima-dev/dokima/issues/322",
> "criterion": "322.1"
> },
> {
> "ask": "Merging a PR redraws its card and its issue's card",
> "source": "https://github.com/dokima-dev/dokima/issues/322",
> "criterion": "322.2"
> },
> {
> "ask": "so the last word always comes after the merge and shows it as merged with the true Definition of Done.",
> "source": "https://github.com/dokima-dev/dokima/issues/322",
> "criterion": "322.3"
> },
> {
> "ask": "#246 and #312 show the right state once this ships.",
> "source": "https://github.com/dokima-dev/dokima/issues/322",
> "criterion": "322.4"
> }
> ]
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote criterion 322.4: once this change lands on main, code redraws #246 and #312 and their issues by itself, with no click from the owner.",
          "It rewrote that criterion's test to send only the merge and the push to main, never a Run workflow event; all five tests fail today for the missing feature."],
  "decided": ["The Run workflow button is out of scope, as the owner chose.",
              "This issue waits for #315 (blocked by), since #315's open PR changes the same triggers and queues of the card workflow."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now has code redraw #246 and #312 by itself as the owner asked, every ask has a criterion, and all five tests fail today for the missing feature.",
 "blockers": [],
 "notes": [
  {"text": "On autopilot this issue's worker now waits until #315 closes, because the planner linked it as blocked by #315. The owner did not ask for that order; it only changes when the work starts, not what ships.",
   "evidence": "plan.json links.blocked_by [315]; concerns[0]"},
  {"text": "This work changes .github/workflows/card.yml, so on autopilot its pull request stops for the owner before it merges.",
   "evidence": "plan.json scope; AGENTS.md step 6: 'a pull request that changes a workflow file ... stops for the owner'"},
  {"text": "The test for 322.4 also passes if code redraws every merged PR on each push to main, which is wider than asked but harmless, and is what #315 plans anyway.",
   "evidence": "tests/test_card_after_merge.py::test_landing_this_change_redraws_246_and_312_by_itself checks only that #246 and #312 were redrawn"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The PR card is written whether the PR is open or merged.", "source": "https://github.com/dokima-dev/dokima/issues/322", "criterion": "322.1"},
  {"ask": "Merging a PR redraws its card and its issue's 
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Code now redraws #246 and #312 by itself as the owner asked; every ask has a criterion and all five tests fail today."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 322 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I've approved the revised plan for #322, and both review checks pass on the hand-back (`/tmp/dokima-out/review.json`).

- **Your answer is in the plan:** you wrote "Code redraws them by itself, no click from me," and criterion 322.4 now says that. When this change lands on main, code redraws #246 and #312 and their issues, and you press nothing. The Run workflow button is now out of scope.
- **Every ask has a criterion:** I matched your four asks and your `/plan` answer to criteria 322.1 to 322.4. The plan has no questions left.
- **All five tests fail today for the missing feature:** a late check draws nothing for the merged PR, the card workflow doesn't start when a PR merges, every card run shares one queue, #246 isn't redrawn, and the workflow doesn't run on a PR merge with main's copy.
- **No open blockers:** there were none from the last round, and I raised none.

Three notes, none blocking:
1. The planner marked this issue as blocked by #315. You didn't ask for that, and on autopilot the work won't start until #315 closes. It changes when the work starts, not what ships.
2. This work changes `.github/workflows/card.yml`, so on autopilot its pull request will stop for you before it merges.
3. The 322.4 test would also pass if code redrew every merged PR on every push to main. That's wider than you asked but does no harm, and #315 plans to do it anyway.
