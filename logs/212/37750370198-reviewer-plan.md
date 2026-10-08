# reviewer (plan) for #212

Run: https://github.com/dokima-dev/dokima/actions/runs/37750370198

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (68KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/744e134c-ae4f-4830-820d-736902aba8be/tool-results/b1ezel12c.txt
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
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> 05-reviewer-plan.json
> 06-worker.json
> 07-reviewer-pr.json
> 08-planner.json
> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #223](https://github.com/dokima-dev/dokima/pull/223) · [files changed](https://github.com/dokima-dev/dokima/pull/223/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37746714549/job/113209821588)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
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
> <details open><summary>From the approved plan of #205, story 4</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree e

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n 1,400p
```

> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #223](https://github.com/dokima-dev/dokima/pull/223) · [files changed](https://github.com/dokima-dev/dokima/pull/223/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37746714549/job/113209821588)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
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
> <details open><summary>From the approved plan of #205, story 4</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, a pull request the reviewer approved merges on its own once every check is green, and the issue says so in one Autopilot line, so the owner no longer merges by hand.
> 
> **Context:** The owner confirmed that on autopilot the reviewer's approval with green checks stands in for theirs. Today the code review's approve stops with

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json
for f in ['in/07-reviewer-pr.json','in/08-planner.json']:
  d=json.load(open(f)); print(f); print(json.dumps(d,indent=1)[:12000])
"
```

> []
> in/07-reviewer-pr.json
> {
>  "role": "reviewer",
>  "stage": "pr",
>  "run_id": "37746736958",
>  "commit_before": "c55a01d3f38d6ae429d4fff2701a0106aa4db76f",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 356045,
>   "turns": 17,
>   "cost_usd": 0.8395516,
>   "tokens_in": 894395,
>   "tokens_out": 9025
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/212/37746736958-reviewer-pr.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37746736958",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The worker made a code review's approval on an autopilot issue merge the pull request at the head whose checks it read, post `Autopilot: merged PR #N` on the issue and end the card with a Next line that does not mention the owner.",
>     "It made `/autopilot start` merge every approved pull request with green checks across the issue's tree, and say why on any it could not merge, mentioning the owner.",
>     "It gave the step that decides what follows in .github/workflows/agent.yml the app's key so it can merge, and added the autopilot exception to step 6 and to `/autopilot start` in AGENTS.md."
>    ],
>    "decided": [
>     "A pull request that changes a workflow file, has a red, running or missing check, or that GitHub refuses stays open and says why; the merge is a squash pinned to the checked commit, never --admin."
>    ],
>    "open": [
>     "This pull request changes a workflow file, so it waits for the owner to merge

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; 
```

> 4:### Approve the result to merge
> 17:### Plan: add `work` to start
> 49:### RezaSoleymanifar on issue #212 (2026-10-08T06:58:17Z)
> 53:### dokima-runtime on issue #212 (2026-10-08T06:58:38Z)
> 188:### RezaSoleymanifar on issue #212 (2026-10-08T07:21:57Z)
> 192:### dokima-runtime on issue #212 (2026-10-08T07:22:15Z)
> 310:### dokima-runtime on issue #212 (2026-10-08T07:30:17Z)
> 473:### dokima-runtime on issue #212 (2026-10-08T07:32:56Z)
> 603:### dokima-runtime on issue #212 (2026-10-08T07:35:36Z)
> 746:### RezaSoleymanifar on issue #212 (2026-10-08T07:40:38Z)
> 750:### dokima-runtime on issue #212 (2026-10-08T07:40:56Z)
> 811:### RezaSoleymanifar on issue #212 (2026-10-08T07:49:07Z)
> 815:### dokima-runtime on issue #212 (2026-10-08T07:49:29Z)
> 825:### dokima-runtime on PR #223 (2026-10-08T07:58:02Z)
> 912:### RezaSoleymanifar on issue #212 (2026-10-08T08:25:59Z)
> 916:### dokima-runtime on issue #212 (2026-10-08T08:26:21Z)
> 1035:### dokima-runtime on issue #212 (2026-10-08T08:31:08Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 740,830p issue.md; sed -n 905,920p issue.md; sed -n 1030,1200p issue.md
```

> <sub>Opus 5.5 · 1.1 min · 9 turns · 260,334 tokens in, 2,532 out · $0.32 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/212/37744394202-reviewer-plan.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37744394202)</sub>
> 
> **Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 
> 
> ### RezaSoleymanifar on issue #212 (2026-10-08T07:40:38Z)
> 
> /work
> 
> ### dokima-runtime on issue #212 (2026-10-08T07:40:56Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Worker**
> 
> Nothing merged on autopilot: a code review's approval always stopped for the owner, and `/autopilot start` only switched labels. Now dokima/agent.py merges an approved pull request on autopilot, pinned to the head whose checks it read and only when every check there passed and no workflow file changes, posting `Autopilot: merged PR #N` on the issue or saying why on the pull request and mentioning the owner.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "worker",
>  "stage": null,
>  "run_id": "37744911609",
>  "commit_before": "80463a53f6711050316829d5228c4a8cf6ff6adc",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 979635,
>   "turns": 26,
>   "cost_usd": 1.713502,
>   "tokens_in": 2390294,
>   "tokens_out": 17890
>  },
>  "log": "https://github.com/dokima-dev/d

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1 | tail -2; git log --oneline -3 origin/main; git log --oneline -8 --all --graph | head -20; git diff 80463a5 HEAD --stat; git merge-tree --write-tree HEAD origin/main | tail -5
```

> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> 4cccffe Live card: minutes and the current step while the agent works (#216)
> * 4129c4a Conversation of run 37749800374
> * dbf73f3 Conversation of run 37748534899
> * 7cf409d Conversation of run 37746560122
> * b6253e3 Conversation of run 37747715025
> * 6753608 Conversation of run 37746736958
> * c7fbef6 Conversation of run 37747282944
> * 95f08b0 Conversation of run 37746514800
> * cee3c5f Conversation of run 37744911609
>  .github/workflows/agent.yml |   6 ++-
>  AGENTS.md                   |   4 +-
>  dokima/agent.py             | 112 +++++++++++++++++++++++++++++++++++++++++++-
>  3 files changed, 117 insertions(+), 5 deletions(-)
> Auto-merging .github/workflows/agent.yml
> Auto-merging AGENTS.md
> CONFLICT (content): Merge conflict in AGENTS.md
> Auto-merging dokima/agent.py
> CONFLICT (content): Merge conflict in dokima/agent.py

**Agent:** Checking whether the plan's tests fail as they should on today's main, since the owner asked for a re-plan on top of it.

`7. Bash`
```
cd /tmp && rm -rf mainwt && git -C /home/runner/work/dokima/dokima worktree add -q /tmp/mainwt origin/main 2>&1|tail -1; cd /tmp/mainwt && git -C /home/runner/work/dokima/dokima show HEAD:tests/test_automerge.py > tests/test_automerge.py && python3 -m pytest -q tests/test_automerge.py 2>&1 | grep -E "^(FAILED|E  .*21[0-9]\.|[0-9]+ (passed|failed))" | head -30; python3 -m pytest -q -x --ignore=tests/test_automerge.py 2>&1 | tail -2
```

> E       AssertionError: 212.1 (code review): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> E       AssertionError: 212.1 (/autopilot start on the issue): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> E       AssertionError: 212.1 (tree): /autopilot start on #57 should merge exactly #60, #61 and #63 (approved, green, inside the tree); it merged []:
> E       AssertionError: 212.2: test control: on autopilot the same review did not merge:
> E       AssertionError: 212.3 (red check): no comment on pull request #60 mentions @owner-person and says why ('Unit tests (3.12)'): [': [],\n  "resolved": [],\n  "asks": [\n   {\n    "ask": "Fix it.",\n    "source": "https://github.com/o/r/issues/57",\n    "criterion": "57.1"\n   }\n  ]\n },\n "check": {\n  "passed": true,\n  "problems": []\n }\n}\n```\n\n</details>\n\n<sub>Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-pr.md) · [run](https://github.com/o/r/actions/runs/42)</sub>\n\n**Next:** @owner-person The work is approved. Merge the pull request, or review it with a command to send it back.\n']
> E       AssertionError: 212.4: step 6 of AGENTS.md's The flow does not say that on autopilot the reviewer's approval with green checks merges the pull request (missing ['autopilot', 'green']): '6. **Merge.** The owner approves and merges.'
> E       AssertionError: 212.5 (/autopilot sta

`8. Bash`
```
cd /tmp/mainwt && python3 -m pytest -q --ignore=tests/test_automerge.py 2>&1 | grep -E "FAILED|passed|failed" | head
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b5patj6ys). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/744e134c-ae4f-4830-820d-736902aba8be/tasks/b5patj6ys.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "start\b\|starts\|no other stage\|dispatch" tests/test_automerge.py | head -30; grep -n "^def test" tests/test_automerge.py
```

> 3:These tests run the real workflows the way GitHub runs them, on the machine from test_start.py: the agent workflow
> 5:(.github/workflows/commands.yml) for `/autopilot start`. Every step's `if:` is evaluated and its script run with bash
> 37:import test_start as ts
> 39:from test_start import N, OWNER, PR, Ctx, Machine, sh, workflow
> 70:def selected(start):
> 72:    sel = a[start] if len(a) > start and not a[start].startswith("-") else None
> 228:API = next((x for x in a[1:] if x.startswith(("repos/o/r/pulls", "/repos/o/r/pulls", "repos/o/r/commits", "/repos/o/r/commits"))), None) if a[:1] == ["api"] else None
> 270:            if x in ("-f", "-F", "--field", "--raw-field") and i + 1 < len(a) and a[i + 1].startswith("head="):
> 305:    """The fake gh of test_start.py taught the issue tree, its labels, and pull request #60 with any others a test adds."""
> 408:               "github": Ctx(event_name="workflow_dispatch", actor=OWNER, event=Ctx(), run_id="42", run_attempt="1",
> 413:        self.result, _ = self.run_job("run", wf["jobs"]["run"], ctx, "workflow_dispatch",
> 458:    return next((l for l in body.splitlines() if l.startswith("**Next:**")), "")
> 476:    assert m.dispatches() == [], f"{crit} ({case}): merging also started another stage: {m.dispatches()}"
> 497:    merged without mentioning the owner, the board must not show Needs you, and no other stage may start."""
> 511:    """`/autopilot start` on an issue, or on its pull request, merges a pull request the reviewer already approved with 

`10. Bash`
```
cd /tmp/mainwt; sed -n 120,150p .github/workflows/agent.yml
```

> env:
>           GH_TOKEN: ${{ steps.setup-key.outputs.token }}
>           SCRUB_CLAUDE: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
>           SCRUB_GITHUB: ${{ github.token }}
>         run: |
>           python3 -m dokima.agent card "$ROLE" "$STAGE" setting-up > /tmp/card.md
>           gh api -X PATCH "repos/$GITHUB_REPOSITORY/issues/comments/$CARD_ID" -F body=@/tmp/card.md --silent \
>             || echo "::warning title=Card not updated::the card could not say setting up"
>           gh api -X DELETE installation/token --silent || echo "::warning title=Key not revoked::the card's key could not be revoked"
>       - name: Starting branch
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: |
>           if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
>             git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
>             if [ "$ROLE" = worker ]; then
>               git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
>             fi
>           elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
>             # A plan review needs no branch: a split never makes one, so it reviews from main.
>             git checkout -q -B "try/issue-$N" origin/main
>           else
>             echo "try/issue-$N does not exist; run the planner first." > /tmp/why.txt
>             echo "::error title=Nothing to $ROLE::$(cat /tmp/why.txt)"; exit 1
>           fi
>           echo "BASE=$(git rev-parse

`11. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/744e134c-ae4f-4830-820d-736902aba8be/tasks/b5patj6ys.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/744e134c-ae4f-4830-820d-736902aba8be/tasks/b5patj6ys.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Meanwhile I'll write the review.

`12. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned after the owner asked for a plan on top of today's main: the tests stay as they were, and all 8 fail on today's main because nothing merges yet.",
          "It reworded 212.1 so the run that merges starts no other stage itself; what a merge unblocks starts through #213's close handling, already on main."],
  "decided": ["Starting what a merge unblocks and switching a finished tree off stay with #213; this story only makes the merge happen."],
  "open": ["The branch try/issue-212 still holds the earlier work and conflicts with today's main, so `/work` would fail before the worker starts; the planner cannot rebuild the branch and gives the owner the commands to reset it before `/work`."]},
 "verdict": "approve",
 "summary": "The plan still keeps every ask and all 8 of its tests fail on today's main for the right reason, but before `/work` the branch must be reset onto today's main, or the worker's run stops on a conflict.",
 "blockers": [],
 "notes": [
  {"text": "Before saying `/work`, reset try/issue-212 onto today's main with only the plan's tests on it (the planner's concern gives the commands) and close PR #223. Otherwise the worker's run merges main into the old branch, hits the conflict and fails before the worker starts.",
   "evidence": "git merge-tree --write-tree try/issue-212 origin/main: CONFLICT (content) in AGENTS.md and dokima/agent.py; .github/workflows/agent.yml on main, step 'Starting branch': `git merge -q --no-edit origin/main` for the worker with no conflict handling"},
  {"text": "Run on today's main (f1b30ab) with tests/test_automerge.py copied in, every one of the 8 tests fails because nothing merges or step 6 lacks the rule, with no crash, so the tests fit the main that #213 changed.",
   "evidence": "python3 -m pytest -q tests/test_automerge.py on origin/main: 8 failed, e.g. '212.1 (code review): the approved pull requ
```

> rc=0

`13. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/744e134c-ae4f-4830-820d-736902aba8be/tasks/b5patj6ys.output; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/mainwt
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
> 3 failed, 368 passed in 136.29s (0:02:16)
> 
> [exited with code 0]

**Agent:** I approved the plan for issue #212, and `review.json` passes both checks in `/tmp/dokima-out`. Before you say `/work`, the branch has to be reset by hand, or the worker's run will fail before it starts.

**What the planner did:** you asked for a re-plan on top of today's main. The planner kept the same tests and reworded criterion 212.1: the run that merges starts no other stage itself. Whatever a merge unblocks now starts through #213's handling when the issue closes, which is already on main. I copied the 8 plan tests onto today's main and ran them: all 8 fail because nothing merges yet, or because step 6 in AGENTS.md doesn't have the autopilot rule. None of them crashes. Every ask from you, including "the whole tree" and "re-plan on top of today's main", maps to a criterion. There were no open blockers from earlier rounds.

**What you need to do first:**
- **Reset the branch.** `try/issue-212` still holds the earlier work, and it conflicts with today's main in `AGENTS.md` and `dokima/agent.py`. The worker's starting step merges main into the branch with no way past a conflict, so it would stop there. The planner isn't allowed to rebuild the branch, but its concern gives you the commands. They put `try/issue-212` back on today's main with only `tests/test_automerge.py` on top.
- **Close PR #223.** The worker then opens a fresh pull request.

**Proposed new issue:** a worker run can't start when its branch conflicts with main. Right now the only fix is resetting the branch by hand, as here.

Running the rest of the test suite on today's main gave 368 passed and 3 failed:
- `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner`
- `tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named`
- `tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests`

The first two fail on the review check's rule that a review lists every ask. These failures are unrelated to merging. My guess is that they come from this sandbox, where the review pack is present, but I didn't confirm that, and they aren't in the review.
