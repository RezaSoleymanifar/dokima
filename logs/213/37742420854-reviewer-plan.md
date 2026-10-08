# reviewer (plan) for #213

Run: https://github.com/dokima-dev/dokima/actions/runs/37742420854

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #213: Autopilot: children start once their blockers merge, and the tree switches itself off when done
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
> <details open><summary>From the approved plan of #205, story 5</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, each child of a split starts planning by itself as soon as everything it waits on has merged, with one Autopilot line where the owner would have typed `/plan`, and when the whole tree is done the parent closes and autopilot ends, with no one switching it off.
> 
> **Context:** Both halves react to the same event, an issue closing when its pull request merges, which needs a workflow trigger, so this story must say so explicitly. Overlaps #86 (start children when blockers merge); fold #86 in or close it as a duplicate of this story, per AGENTS.md Changing scope. AGENTS.md Splitting already says 'When a child merges, every sibling whose needs have landed starts'. Blocked-by links are native GitHub issue dependencies (repos/{repo}/issues/N/dependencies/blocked_by, filed by file_split in dokima/agent.py). The planner is started by the same dokima-next signal

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; wc -l tests/test_autopilot_close.py; cat tests/test_autopilot_close.py
```

> <persisted-output>
> Output too large (38.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b765fc80-925e-4697-b446-6f75c1ca7ec6/tool-results/b50kcfsso.txt
> 
> Preview (first 2KB):
> commit cc3b6488516d51ec9e162215e28ac097a8a2df0d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:16:14 2026 +0000
> 
>     planner for #213 (run 37742100259)
> 
>  tests/test_autopilot_close.py | 118 ++++++++++++++++++++++++++++++++++++++++--
>  1 file changed, 114 insertions(+), 4 deletions(-)
> 
> commit 36df088dd15204cf1eb01004da2269a53f555efb
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:10:55 2026 +0000
> 
>     planner for #213 (run 37740608574)
> 
>  tests/test_autopilot.py       |  24 +-
>  tests/test_autopilot_close.py | 529 ++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 546 insertions(+), 7 deletions(-)
> 
> commit 60dee993eef1d5ed4463d19badcd4f91ea281b6a
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 01:58:03 2026 -0500
> 
>     Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off (#214)
>     
>     * planner for #209 (run 37738831571)
>     
>     * worker for #209 (run 37739600049)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
> 
>  .github/workflows

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_close.py tests/test_autopilot.py 2>&1 | grep -E "^(FAILED|PASSED|E  )|passed|failed" | head -40
```

> assert not m.failed, f"213.1: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E           AssertionError: 213.1 (close): #102's planner was started 0 times, expected once; started: {}
> E             
> E           assert None == 1
> E            +  where None = <built-in method get of dict object at 0x7fb296d49480>(102)
> E            +    where <built-in method get of dict object at 0x7fb296d49480> = {}.get
>         assert not m.failed, f"213.1 (split on autopilot): the listener failed on /work:\n{m.tail()}"
> E           AssertionError: 213.1 (split on autopilot): #900's planner was started 0 times, expected once; started: {}
> E             ## route: r (exit 0)
> E             role=worker
> E             stage=
> E             issue=57
> E             
> E             ## queue: Put up the run's queued card (exit 0)
> E             
> E             ## split: File the approved split's stories as sub-issues (exit 0)
> E             
> E           assert None == 1
> E            +  where None = <built-in method get of dict object at 0x7fb296e46f40>(900)
> E            +    where <built-in method get of dict object at 0x7fb296e46f40> = {}.get
>         assert not m.failed, f"213.1 (/autopilot start): the listener failed:\n{m.tail()}"
> E           AssertionError: 213.1 (/autopilot start): #101's planner was started 0 times, expected once; started: {}
> E             ## route: r (exit 0)
> E             autopilot=start
> E             issue=57
> E             
> E             ## autopilot: Switch the issue tree 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_close.py tests/test_autopilot.py 2>&1 | tail -15
```

> assert ('open', None) == ('closed', 'completed')
>   
>   At index 0 diff: 'open' != 'closed'
>   
>   Full diff:
>     (
>   -     'closed',
>   ?      -- ^ ^
>   +     'open',
>   ?       ^ ^
>   -     'completed',
>   +     None,
>     )
> 10 failed, 5 passed in 11.00s

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_close.py tests/test_autopilot.py 2>&1 | grep -E "^(FAILED|ERROR)"; timeout 600 python -m pytest -q -rA tests/test_autopilot_close.py tests/test_autopilot.py 2>&1 | grep -E "^PASSED"
```

> FAILED tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged - AssertionError: 213.1 (close): #102's planner was started 0 times, expected once; started: {}
> FAILED tests/test_autopilot_close.py::test_a_split_filed_on_autopilot_starts_its_unblocked_stories - AssertionError: 213.1 (split on autopilot): #900's planner was started 0 times, expected once; started: {}
> FAILED tests/test_autopilot_close.py::test_autopilot_start_on_a_parent_picks_up_the_children_waiting - AssertionError: 213.1 (/autopilot start): #101's planner was started 0 times, expected once; started: {}
> FAILED tests/test_autopilot_close.py::test_the_parent_closes_when_its_last_sub_issue_closes - AssertionError: 213.2 (last one): #57 is ('open', None) after its last open sub-issue closed, expected closed as completed
> FAILED tests/test_autopilot_close.py::test_autopilot_goes_off_for_the_whole_tree_when_it_is_done - AssertionError: 213.3 (tree): the done tree left these issues on autopilot: [57, 101, 102]
> FAILED tests/test_autopilot_close.py::test_a_close_off_autopilot_does_nothing - AssertionError: 213.4 (on autopilot, sibling): #102 should start once when #101 closes: {}
> FAILED tests/test_autopilot_close.py::test_a_child_planned_running_or_done_is_never_started_again - AssertionError: 213.5 (first close): #102's planner was started 0 times, expected once; started: {}
> FAILED tests/test_autopilot_close.py::test_autopilot_start_picks_up_waiting_issues_at_every_level - Asserti

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,330p tests/test_autopilot_close.py
```

> """On autopilot, children start once their blockers merge, and the tree switches itself off when done (#213).
> 
> These tests run the workflows the way GitHub runs them, on the machine from test_start.py: every job's `if:` is
> evaluated and its scripts run with bash against a fake `gh`. When an issue closes, every workflow in
> .github/workflows/ that GitHub would start on `issues: closed` runs, with the event GitHub sends (github.event_name
> `issues`, github.event.action `closed`, github.event.issue with its number, state, state_reason, labels and
> parent_issue_url), started by the code owner who merged. The project board's variable is unset, so the board does
> nothing. A command runs the listener, commands.yml, as test_autopilot.py does. Job and step `if:` expressions can use
> what test_start.evaluate knows (no toJSON, no `.*` filters): read labels and the tree in a step's script.
> 
> The fake GitHub knows an issue tree and keeps it in tree.json, labels.json, states.json and deps.json:
>   - `gh api repos/o/r/issues/N` gives the issue (id N*10, number, title, state, state_reason, labels,
>     parent_issue_url); PATCH or POST on it with -f/-F state=closed (and state_reason=...) or --input closes it.
>   - `gh api repos/o/r/issues/N/parent` gives its parent issue (404 when it has none).
>   - `gh api repos/o/r/issues/N/sub_issues` lists its sub-issues; POST with sub_issue_id=ID adds one.
>   - `gh api repos/o/r/issues/N/dependencies/blocked_by` lists the issues blocking it, each with its state; PO

**Agent:** I'm reading the planner's tests now. All 10 new tests fail today because the feature is missing, so I'm checking that each one would actually catch a wrong build.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 330,639p tests/test_autopilot_close.py
```

> return [json.loads(l) for l in open(path)] if os.path.exists(path) else []
> 
>     def planners_started(self, crit):
>         """{issue number: how many times its planner was started}, counting only signals that start agent.yml."""
>         started = {}
>         for s in self.signals():
>             p = s["payload"]
>             if s["event_type"] != "dokima-next" or p.get("role") != "planner":
>                 continue
>             assert s["token"] == "fake-token", (f"{crit}: the planner for #{p.get('issue')} was signalled with the "
>                                                 f"workflow's own token, which GitHub ignores; only Dokima's app key starts agent.yml")
>             started[int(p["issue"])] = started.get(int(p["issue"]), 0) + 1
>         return started
> 
>     def new_comments(self, n):
>         """The bodies of the comments written on issue n since the test began, as they stand now."""
>         return [c["versions"][-1] for c in self.comments()[self.seeded:] if c["kind"] == "issue" and c["number"] == int(n)]
> 
>     def autopilot_lines(self, n):
>         """How many comments on issue n read exactly the Autopilot line."""
>         return sum(1 for b in self.new_comments(n) if b.strip() == LINE)
> 
>     def filed_labels(self):
>         """Every issue's labels now, counting the labels each new issue was created with: {number: [names]}."""
>         labels = self.labels()
>         for i, c in enumerate(self.created_issues()):
>             given = [c[j + 1] for j, x in enumerate(c[:-1]) if x in 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -n -A3 "concurrency" .github/workflows/*.yml | head -30; grep -n "blocked_by\|sub_issue_id" dokima/agent.py | head
```

> agent.yml
> assign.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> wiki.yml
> worker.yml
> .github/workflows/board.yml:20:concurrency:
> .github/workflows/board.yml-21-  group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
> .github/workflows/board.yml-22-  cancel-in-progress: false
> .github/workflows/board.yml-23-jobs:
> .github/workflows/agent.yml:36:concurrency:
> .github/workflows/agent.yml-37-  group: agent-${{ (inputs.issue || github.event.client_payload.issue) }}
> .github/workflows/agent.yml-38-  cancel-in-progress: false
> .github/workflows/agent.yml-39-permissions:
> .github/workflows/card.yml:12:concurrency:
> .github/workflows/card.yml-13-  group: card
> .github/workflows/card.yml-14-  cancel-in-progress: false
> .github/workflows/card.yml-15-permissions:
> .github/workflows/planner.yml:11:concurrency:
> .github/workflows/planner.yml-12-  group: plan-${{ github.event.issue.number }}-${{ github.event.label.name }}
> .github/workflows/planner.yml-13-  cancel-in-progress: true
> .github/workflows/planner.yml-14-permissions:
> .github/workflows/worker.yml:12:concurrency:
> .github/workflows/worker.yml-13-  group: work-${{ github.event.issue.number }}-${{ github.event.label.name }}
> .github/workflows/worker.yml-14-  cancel-in-progress: true
> .github/workflows/worker.yml-15-permissions:
> 182:        gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues", "-F", f"sub_issue_id={node}")
> 184:                      "blocked_by": [

`9. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/rv && cat > /tmp/rv/test_chk.py <<'EOF'
import json, test_autopilot_close as c, test_start as ts
def test_x(tmp_path):
    m = c.Repo(tmp_path/"on", {}, {57:[c.LABEL]}, history=ts.SPLIT_APPROVED)
    m.listen("/work")
    print("DEPS", open(f"{m.tmp}/gh/deps.json").read(), "TREE", open(f"{m.tmp}/gh/tree.json").read())
EOF
cp /tmp/rv/test_chk.py tests/zz_rv_chk.py; timeout 300 python -m pytest -q -s tests/zz_rv_chk.py 2>&1 | grep -E "DEPS|passed|failed"; rm tests/zz_rv_chk.py; git status --short
```

> DEPS {
> 1 passed in 1.61s

`10. Bash`
```
cd /home/runner/work/dokima/dokima; cp /tmp/rv/test_chk.py tests/zz_rv_chk.py; timeout 300 python -m pytest -q -s tests/zz_rv_chk.py 2>&1 | head -30; rm tests/zz_rv_chk.py
```

> DEPS {
>  "901": [
>   900
>  ]
> } TREE {
>  "57": [
>   900,
>   901
>  ]
> }
> .
> 1 passed in 1.60s

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 60dee99 -- tests/test_autopilot.py
```

> diff --git a/tests/test_autopilot.py b/tests/test_autopilot.py
> index 07c7ed8..bdcc3fd 100644
> --- a/tests/test_autopilot.py
> +++ b/tests/test_autopilot.py
> @@ -56,6 +56,9 @@ m_sub = re.fullmatch(r"/?repos/o/r/issues/(\d+)/sub_issues(?:\?.*)?", API_PATH o
>  m_lab = re.fullmatch(r"/?repos/o/r/issues/(\d+)/labels(?:\?.*)?", API_PATH or "")
>  m_one = re.fullmatch(r"/?repos/o/r/issues/(\d+)/labels/([^?]+)", API_PATH or "")
>  m_iss = re.fullmatch(r"/?repos/o/r/issues/(\d+)(?:\?.*)?", API_PATH or "")
> +if a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/\d+/dependencies/blocked_by", x) for x in a[1:]):
> +    print("[]")
> +    sys.exit(0)
>  if m_sub and method() == "GET":
>      print(json.dumps([issue_obj(c) for c in TREE.get(m_sub.group(1), [])]))
>      sys.exit(0)
> @@ -211,11 +214,12 @@ def test_autopilot_stop_takes_the_same_tree_off_autopilot(record_property, tmp_p
>  
>  
>  def test_autopilot_starts_no_stage_and_says_which_issues_it_switched(record_property, tmp_path):
> -    """`/autopilot start` and `/autopilot stop` start no planner, worker or reviewer, and leave one comment naming every issue switched.
> +    """`/autopilot start` and `/autopilot stop` start no stage on the issue they were said about, and leave one comment there naming every issue switched.
>  
>      Runs the listener on the code owner's `/autopilot start` and `/autopilot stop`, each on issue #57 and on pull
> -    request #60. None may call the agent workflow, send a start signal or run an agent. Each must leave exactly one
> 

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "#86\b" --include=*.md --include=*.py . | head; git log --oneline | grep -i "86\b" | head
```

> 9928586 Store the planner prompt in the repo (#91)
> 923246f loop work-verification-1790909086: README: you check the verification, not the work (Reza 2026-10-01)

**Agent:** The tests are thorough and fail today for the right reason. I found one gap, in how the plan tests the "two merges at once" promise. Writing the review now.

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner re-planned after the owner answered: criteria 213.1 to 213.3 now cover every level under the issue autopilot was started on.",
   "It added three tests that use trees two and three levels deep: /autopilot start, a close deep in the tree, and a tree closing level by level."
  ],
  "decided": [
   "Stories filed by /work under a parent on autopilot go on autopilot too.",
   "When code closes a parent, that close counts as a close one level up."
  ],
  "open": [
   "Closing #86 as a duplicate is left to the owner."
  ]
 },
 "verdict": "block",
 "summary": "The plan covers every level as the owner asked, and all ten new tests fail today because the feature is missing. One gap remains: the owner said two merges that close together must not start the same planner twice, but the plan only tests two closes one after the other.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "213.5",
   "test": "tests/test_autopilot_close.py::test_a_child_planned_running_or_done_is_never_started_again",
   "problem": "The owner wrote 'Two merges close together must not start the same planner twice.' The plan narrowed this to 'two closes in a row'. The test runs the second close only after the first has finished and posted its Autopilot line, so the second run can always see that #102 already started. On GitHub, two merges close together, two close workflows run at the same moment, and neither sees the other's line. A build with no guard against that passes this test and still starts #102's planner twice.",
   "evidence": "Issue #213 non-functional: '(Two merges close together must not start the same planner twice.)'. plan.json non_functional[0]: 'two closes in a row start a waiting child only once'. In the test, m.close(101) runs to the end before m.close(108) starts (tests/test_autopilot_close.py, end of test_a_child_planned_running_or_done_is_never_started_again). agent.
```

> rc=0

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's|https://github.com/dokima-dev/dokima/issues/213#issuecomment (RezaSoleymanifar, 2026-10-08T07:13:13Z)|https://github.com/dokima-dev/dokima/issues/213 (owner comment of 2026-10-08 07:13)|' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 213 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for #213 on one gap. Everything else holds up, and the hand-back is in `/tmp/dokima-out/review.json`. It passes both checks.

**What the planner did:** it re-planned after your answer. Criteria 213.1 to 213.3 now cover every level under the issue autopilot was started on. It added three tests on trees two and three levels deep: `/autopilot start`, a close deep in the tree, and a tree closing level by level. I ran all 10 new tests and each one fails today because the feature is missing, not because of a crash or bad setup. The 5 existing autopilot tests still pass. I also confirmed the fake GitHub records the split's blocked-by link (#901 waits on #900), so the split test is sound.

**Blocker B1 (213.5), for the planner to fix:** the issue says "Two merges close together must not start the same planner twice." The plan narrowed this to "two closes in a row." The test only runs the second close after the first has finished and posted its Autopilot line, so a build with no guard against two closes running at the same moment would pass it. The per-issue concurrency setting in `agent.yml` only queues the two planner runs one after the other; it doesn't drop the second. The fix is to put "together" back in the criterion and add a test for it. That test can either interleave two closes or require that the close workflow never runs two at once.

**Notes (not blocking):**
- The tests for 213.2 and 213.3 require the code to close the parent and take the whole tree off autopilot during the same close. A build that relied on GitHub's follow-up close event for the parent would fail those tests, even though it would end up the same on GitHub.
- The updated check in `test_autopilot.py` only catches a start signal for #57 when it's sent with `-f client_payload[issue]=57`. One sent as JSON through `--input` would get past it.

All 11 of your asks map to a criterion, none missing. That includes "every level" and "test at least two levels." Folding #86 in maps to 213.1; actually closing it as a duplicate is left for you to do on GitHub.
