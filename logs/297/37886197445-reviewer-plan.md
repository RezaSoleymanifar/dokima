# reviewer (plan) for #297

Run: https://github.com/dokima-dev/dokima/actions/runs/37886197445

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (88KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a700871d-e603-4cad-80d5-c2f4859e5d1e/tool-results/bhqkx8sqw.txt
> 
> Preview (first 2KB):
> .:
> total 112
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:56 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:56 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:56 in
> -rw-r--r--  1 runner runner 87715 Oct  9 04:56 issue.md
> -rw-r--r--  1 runner runner  1619 Oct  9 04:56 open_blockers.json
> -rw-r--r--  1 runner runner  7810 Oct  9 04:56 plan.json
> 
> in:
> total 56
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:56 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:56 ..
> -rw-r--r-- 1 runner runner 5917 Oct  9 04:56 01-planner.json
> -rw-r--r-- 1 runner runner 7502 Oct  9 04:56 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 9417 Oct  9 04:56 03-planner.json
> -rw-r--r-- 1 runner runner 6680 Oct  9 04:56 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8471 Oct  9 04:56 05-planner.json
> # Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> The board's Needs you pill shows only while something truly waits on the owner, and Autopilot shows otherwise.
> 
> **Plan**
> 
> [issue #297](https://github.com/dokima-dev/dokima/issues/297)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #135, #294
> 

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json
```

> [
>  {
>   "id": "B3",
>   "criterion": "297.5",
>   "test": "tests/test_needs_you.py::test_a_merge_sweeps_every_pill_on_the_board_to_what_it_should_be",
>   "problem": "The owner asked for a one-time sweep that clears the backlog of wrong pills once. Criterion 297.5 adds 'Every later merge's board run sweeps the same way', and 297.4 leans on it ('loses an old Needs you at the next merge'). That adds work the owner did not ask for: every merge reads the history of every issue on the board. The owner's words leave only one reading, so the planner should plan for it and offer every-merge sweeps as the alternative in the question, not the other way round.",
>   "evidence": "Owner's /plan comment on #297 (2026-10-09T03:52:03Z): 'Right after this merges, a one-time sweep goes over every item on the board and sets each pill to what it should be by these rules, so the backlog of wrong pills is cleared once.' plan.json criteria 4 and 5; the plan's own question says 'Each merge then also reads the history of every open issue on the board.' Tests for 297.4 (third part) and 297.5 run the sweep at the merge of some unrelated PR #70, so they cannot tell a one-time sweep from one at every merge.",
>   "fix": "Make 297.5 a sweep that runs once, right after this change merges, and say what starts it and how it knows it already ran. Drop 'every later merge' from 297.4 and 297.5. Add a test that a second merge after the sweep leaves a wrong pill it would have fixed alone, beside the test that the first swee

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|Comment\|^---" issue.md | head -80; wc -l issue.md
```

> 65:## Comments
> 67:### RezaSoleymanifar on issue #297 (2026-10-09T03:44:40Z)
> 71:### dokima-runtime on issue #297 (2026-10-09T03:45:04Z)
> 75:### dokima-runtime on issue #297 (2026-10-09T03:45:07Z)
> 80:### dokima-runtime on issue #297 (2026-10-09T03:45:18Z)
> 263:### RezaSoleymanifar on issue #297 (2026-10-09T03:52:03Z)
> 269:### dokima-runtime on issue #297 (2026-10-09T03:52:23Z)
> 279:### dokima-runtime on issue #297 (2026-10-09T04:07:18Z)
> 463:### RezaSoleymanifar on issue #297 (2026-10-09T04:26:33Z)
> 467:### dokima-runtime on issue #297 (2026-10-09T04:26:55Z)
> 697:### dokima-runtime on issue #297 (2026-10-09T04:39:53Z)
> 886:### RezaSoleymanifar on issue #297 (2026-10-09T04:47:00Z)
> 890:### dokima-runtime on issue #297 (2026-10-09T04:47:19Z)
> 1107:### dokima-runtime on issue #297 (2026-10-09T04:56:15Z)
> 1115 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 1,70p issue.md; sed -n 263,268p issue.md; sed -n 463,466p issue.md; sed -n 886,889p issue.md; sed -n 1107,1115p issue.md
```

> # Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> The board's Needs you pill shows only while something truly waits on the owner, and Autopilot shows otherwise.
> 
> **Plan**
> 
> [issue #297](https://github.com/dokima-dev/dokima/issues/297)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #135, #294
> 
> **User story:** The owner trusts Needs you on the board: it shows only on items that truly wait on them, leaves the moment they answer or the item closes, and Autopilot shows in its place on everything else that runs by itself.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Needs you appears only where the river stops for the owner. Finished checks never set it, and a Needs you the river set stays through new commits and checks until answered.
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-297/tests/test_needs_you.py#L187"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" wid

`5. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['04-reviewer-plan.json','05-planner.json']:
    d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:5000]); print()
"
```

> 04-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37884936324",
>  "commit_before": "df29d01145888f67d2622dc86f6168395e515b11",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 66916,
>   "turns": 10,
>   "cost_usd": 0.5949936000000001,
>   "tokens_in": 395688,
>   "tokens_out": 6289
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/297/37884936324-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37884936324",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner rewrote the plan to seven criteria with thirteen tests in tests/test_needs_you.py, all failing today because the feature is missing, and adds board.yml runs on pull request reviews."
>    ],
>    "decided": [
>     "A code owner's command in a pull request review's summary clears Needs you at once, as the owner answered.",
>     "The board run of this change's merge sweeps every card on the board, and so does the board run of every later merge.",
>     "An item on autopilot shows Autopilot or Needs you, never both and never neither, after every board moment."
>    ],
>    "open": [
>     "Whether the sweep runs only once, as the owner wrote, or at every merge (planned for every merge)."
>    ]
>   },
>   "verdict": "block",
>   "summary": "The plan now covers the full sweep and the one-pill rule, but it sweeps at every merge where the owner asked for a one-time sweep.",
>   "blockers": [
>    {
>     "id": "B3",
>     "crite

**Agent:** The earlier blocker (one-time sweep) is settled by the owner's newer answer. Now I'm running the plan's tests to confirm they fail today for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat df29d01 HEAD; timeout 300 python -m pytest -q tests/test_needs_you.py 2>&1 | grep -E "^(FAILED|ERROR|PASSED)|passed|failed" | head -30; timeout 300 python -m pytest -q tests/test_board.py tests/test_autopilot_board.py 2>&1 | tail -2
```

> tests/test_needs_you.py | 21 +++++++++++++++++++++
>  1 file changed, 21 insertions(+)
> FAILED tests/test_needs_you.py::test_a_check_finishing_never_marks_a_pull_request_for_the_owner - AssertionError: 297.1: after the checks finished, the pull requests show {'pr #60': 'Needs you', 'pr #61': 'Needs you', 'pr #62': 'Needs you'}; a finished check must not mark one for the owner
> FAILED tests/test_needs_you.py::test_needs_you_set_by_the_river_stays_through_new_commits_and_checks - AssertionError: 297.1: a new commit on PR #62 took Needs you away though the owner answered nothing: {'issue #59': None, 'pr #62': None}
> FAILED tests/test_needs_you.py::test_a_code_owners_command_clears_needs_you_at_once_and_nothing_else_does - AssertionError: 297.2: the code owner said /work on #57, on autopilot, and the cards show {'issue #57': 'Needs you', 'pr #60': 'Needs you'}, not Autopilot
> FAILED tests/test_needs_you.py::test_a_code_owners_command_in_a_review_summary_clears_needs_you_at_once - AssertionError: 297.2: RezaSoleymanifar's changes_requested review 'Please rename the helper.' on PR #61 answered nothing, yet the pills changed to {'issue #58': None, 'pr #61': None, 'issue #57': 'Needs you', 'pr #60': 'Needs you'}
> FAILED tests/test_needs_you.py::test_the_board_runs_when_a_pull_request_review_is_submitted - AssertionError: 297.2: board.yml does not run on pull_request_review, so a review's command never reaches the board
> FAILED tests/test_needs_you.py::test_needs_you_never_lands_on_a_closed_i

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff df29d01 HEAD; grep -n "def test_every_later_merge_sweeps_again" -B2 -A2 tests/test_needs_you.py
```

> diff --git a/tests/test_needs_you.py b/tests/test_needs_you.py
> index 566ca6c..0218b3b 100644
> --- a/tests/test_needs_you.py
> +++ b/tests/test_needs_you.py
> @@ -443,6 +443,27 @@ def test_a_merge_sweeps_every_pill_on_the_board_to_what_it_should_be(record_prop
>      assert not wrong, f"297.5: after the merge's sweep these cards show the wrong pill: {wrong}"
>  
>  
> +def test_every_later_merge_sweeps_again(record_property, make):
> +    """A pill that drifts after one merge is put right again at the next merge.
> +
> +    Proves 297.5. PR #70 (closing #71) merges and its sweep sets #66 (on autopilot, nothing waits) to Autopilot and
> +    #67 (not on autopilot) to nothing. Then both drift: #66 shows Needs you and #67 shows Autopilot. PR #74 (closing
> +    #75) merges, and its sweep must put #66 back to Autopilot and #67 back to nothing. A sweep that runs only once,
> +    at the first merge, leaves both wrong. Today neither merge sweeps."""
> +    record_property("proves", "297.5")
> +    w = make(labels={("issue", 66): {LABEL}}, closed={("pr", 70), ("issue", 71), ("pr", 74), ("issue", 75)},
> +             cards={("issue", 66): {"Status": "Plan"}, ("issue", 67): {"Status": "Plan", "Action": AUTO}})
> +    board.sync("pull_request_target", pr_event("closed", 70, 71, merged=True), SPEC, REPO)
> +    got = pills(w, ("issue", 66), ("issue", 67))
> +    assert got == {"issue #66": AUTO, "issue #67": None}, f"297.5: after the first merge's sweep the cards show {got}"
> +    w.cards[("issue", 66)]["Action"] = NEEDS
> + 

`8. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
d=json.load(open('04-reviewer-plan.json'))['handback']; print(json.dumps(d['asks'],indent=1)); print(d.get('assumptions'))"; python3 -c "import json;print(json.load(open('/tmp/pack/plan.json')).get('questions'))"
```

> [
>  {
>   "ask": "Needs you shows only while the flow is actually stopped waiting for me on that item: a question, an approval, a merge, an escalation.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.1"
>  },
>  {
>   "ask": "It clears the moment that is answered",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.2"
>  },
>  {
>   "ask": "and always when the item closes.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.3"
>  },
>  {
>   "ask": "A parent issue shows Needs you only when the parent itself waits on me (for example its split before it is filed, or its end-to-end test hitting a blocker), never just because its children are in progress.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.4"
>  },
>  {
>   "ask": "Autopilot and Needs you are complementary: an item on autopilot shows Autopilot unless it needs me, then Needs you, never both and never neither.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.6"
>  },
>  {
>   "ask": "The existing wrong pills are cleared too.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.5"
>  },
>  {
>   "ask": "A closed issue or merged or closed pull request can never get Needs you, whichever job runs last.",
>   "source": "https://github.com/dokima-dev/dokima/issues/297",
>   "criterion": "297.3"
>  },
>  {
>   "ask": "Right after this merges, a one-time sweep goes over e

`9. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack/in; python3 - <<'EOF'
import json
asks=json.load(open('04-reviewer-plan.json'))['handback']['asks']
asks.append({"ask":"the sweep runs at every merge, not just once, so a pill that drifts is corrected again.","source":"https://github.com/dokima-dev/dokima/issues/297","criterion":"297.5"})
r={"previous_step":{"did":["The planner rewrote criterion 297.5 so the board run of every merge, starting with this change's merge, sweeps every card's pill, as the owner answered.","The planner added a test that a second merge puts drifted pills right again, and removed the plan's question."],
 "decided":["The sweep runs at every merge, not only once.","A parent whose split is filed loses an old Needs you at the next merge's sweep."],"open":[]},
"verdict":"approve",
"summary":"The plan now sweeps the board at every merge as the owner answered, and all fourteen new tests fail today because the feature is missing.",
"blockers":[],
"notes":[{"text":"All fourteen new tests fail today for the right reason, including the new test that a second merge sweeps again; the edited board tests still pass.","evidence":"pytest -q tests/test_needs_you.py -> 14 failed with 297.N messages; pytest -q tests/test_board.py tests/test_autopilot_board.py -> 39 passed."},
 {"text":"Criterion 297.2 needs .github/workflows/board.yml to run on pull request reviews, so this build pauses for the owner's approval on GitHub before it can be pushed.","evidence":"plan.json scope; tests/test_needs_you.py::test_the_board_runs_when_a_pull_request_review_is_submitted; AGENTS.md Identity and safety."},
 {"text":"Every merge's sweep reads the history of every issue on the board, so merge board runs get slower as the board grows; the owner chose this.","evidence":"Owner's comment 2026-10-09T04:47:00Z; plan.json criterion 297.5."}],
"outside_plan":[],"resolved":["B3"],"issues_found":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
cd /home/runner/work/
```

> rc=0

**Agent:** I approved the plan for #297. Both checks on the review passed, and the review is in `/tmp/dokima-out/review.json`.

- **The earlier blocker (B3) is resolved.** I had blocked because the plan swept the board at every merge, while you had asked for a one-time sweep. Your later comment (2026-10-09 04:47) settled it: "the sweep runs at every merge, not just once, so a pill that drifts is corrected again." The plan now says that in criterion 297.5, and its question to you is gone.
- **Tests:** the planner added a test where two pills go wrong after one merge and a second merge has to put both right. A sweep that ran only once would fail it. All 14 new tests fail today because the feature isn't built yet, not because they crash. The 39 existing board tests the plan edits still pass.
- **Your asks:** I matched every ask in the issue and in your comments to a criterion, and none are missing.

Notes for you:
- **You'll need to approve one file change on GitHub.** Clearing Needs you from a review summary (297.2) requires `.github/workflows/board.yml` to also run on pull request reviews. The bot can't push a workflow change on its own, so the build will pause until you approve that change on GitHub.
- **Merge board runs get slower as the board grows.** Every merge's sweep reads the history of every issue on the board; that's the cost of the every-merge choice.
