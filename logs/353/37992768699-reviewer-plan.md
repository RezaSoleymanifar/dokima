# reviewer (plan) for #353

Run: https://github.com/dokima-dev/dokima/actions/runs/37992768699

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (34.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/47d80bac-94cd-489f-8e30-7e2bebf3ddb1/tool-results/briu41loi.txt
> 
> Preview (first 2KB):
> # Issue #353: On autopilot, a blocked issue plans only after its blockers merge (reverses #253)
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #353](https://github.com/dokima-dev/dokima/issues/353)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> On autopilot, a blocked issue does not get a plan until every issue blocking it has merged. This reverses #253

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md; ls in; cat open_blockers.json
```

> <!-- dokima-ask -->
> 
> On autopilot, a blocked issue does not get a plan until every issue blocking it has merged. This reverses #253 (PR #296), where a blocked issue planned early and only its build waited.
> 
> Owner's words (2026-10-09): "Yes, don't plan a blocked issue until its blockers merge. And it, I think, honestly, default was that way. I changed it to, hey, you should plan preemptively, but I think that wasn't a good issue. ... It shouldn't be a document rule ... This is like machinery. It's in the code. And I want you to reverse what I already did."
> 
> Why: a plan written while its blockers are still open goes stale when they merge (#236's plan predates #289, which changes how cards show raises).
> 
> What changes:
> - On autopilot, an issue with an open blocker does not start its planner. This is already true for issues whose blockers are known before planning (start_waiting).
> - When the planner's own plan finds an open blocker, the issue stops after plan review instead of waiting with an approved plan: the card says it waits for those issues, and nothing is built.
> - When the last blocker closes, autopilot starts a fresh planner run, never the worker from the old plan.
> - Remove the code #253 added for a waiting worker (WAIT_LINE, GO_LINE, worker_waits, start_worker, start_blocked_workers and the waiting branch in main), and the #343 rule (PR #348) that keeps an approved but blocked plan in the Plan column, since an approved plan no longer waits.
> - A /plan or /work the owner ty

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k not in ('test_changes',)},indent=1))" | head -150; python3 -c "import json;d=json.load(open('in/03-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> {
>  "kind": "user_story",
>  "summary": "On autopilot, a blocked issue is planned only after its blockers merge, so no plan goes stale while it waits.",
>  "user_story": "On autopilot, an issue blocked by open issues is planned fresh once they merge, so nothing is ever built from a plan written before its blockers landed.",
>  "acceptance_criteria": [
>   {
>    "text": "On autopilot, an issue with an open blocker never starts its planner by itself. This holds when autopilot is switched on, when a split files it, and after any close that leaves a blocker open.",
>    "source": "https://github.com/dokima-dev/dokima/issues/353"
>   },
>   {
>    "text": "On autopilot, a plan approved while the issue has an open blocker builds nothing: no worker starts and no line stands in for `/work`. The card's Next line names each open blocker, says the issue plans again when they close, and mentions no one; the card stays in Plan without Needs you.",
>    "source": "https://github.com/dokima-dev/dokima/issues/353"
>   },
>   {
>    "text": "When the last open blocker of such an issue closes, autopilot starts a fresh planner once, never the old plan's worker. It posts `Autopilot: blockers merged, starting plan`. A `/plan` or `/work` the owner types by hand still runs as today, and no later close overrides it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/353"
>   },
>   {
>    "text": "The waiting worker that #253 added is gone. dokima.agent has no WAIT_LINE, GO_LINE, worker_waits, start_worker or start_blocke

**Agent:** Let me read the new test and run it.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 7f3ac14 HEAD --stat; grep -n "def test_" tests/test_blocked_worker.py; grep -n "test_blocked_worker" tests/conftest.py
```

> tests/test_blocked_worker.py | 39 +++++++++++++++++++++++++++++++++++++++
>  1 file changed, 39 insertions(+)
> 87:def test_an_approved_plan_with_an_open_blocker_builds_nothing_and_says_what_it_waits_for(tmp_path, record_property):
> 127:def test_when_github_cannot_list_the_blockers_the_worker_waits_and_the_issue_says_why(tmp_path, record_property):
> 201:def test_the_last_blocker_closing_starts_a_fresh_plan_never_the_old_plans_worker(tmp_path, record_property):
> 235:def test_a_command_the_owner_types_while_it_waits_runs_and_no_close_overrides_it(tmp_path, record_property):
> 252:def test_a_close_that_cannot_list_the_blockers_starts_nothing_and_says_why(tmp_path, record_property):
> 273:def test_a_blocked_issue_on_autopilot_never_starts_its_planner_by_itself(tmp_path, record_property):
> 314:def test_the_code_253_added_for_a_waiting_worker_is_gone(record_property):
> 333:def test_agents_md_says_a_blocked_issue_plans_only_after_its_blockers_merge(record_property):
> 45:    "test_blocked_worker.py::test_a_worker_already_started_is_never_started_again",
> 46:    "test_blocked_worker.py::test_on_autopilot_a_blocked_plan_waits_with_one_line_and_mentions_no_one",
> 47:    "test_blocked_worker.py::test_only_an_approved_newest_plan_starts_its_worker",
> 48:    "test_blocked_worker.py::test_the_last_blocker_closing_starts_the_waiting_worker_once",

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,86p tests/test_blocked_worker.py; sed -n 195,320p tests/test_blocked_worker.py
```

> """On autopilot, a blocked issue plans only after its blockers merge (#353, which reverses #253).
> 
> Before #353 a blocked issue on autopilot planned early, and its approved plan waited for its blockers with the bot's
> line `Autopilot: plan approved, waiting for #A to close`; when they closed, its worker built that old plan, with
> `Autopilot: blockers closed, starting work`. A plan written while its blockers are still open goes stale when they
> merge, so now nothing waits with an approved plan. Each moment runs the real code against a fake GitHub:
> 
> - The plan review approves. `python3 -m dokima.agent next N OUT` (the step of agent.yml that decides what follows a
>   run) runs on the review's record, on the fake GitHub of test_plan_links_recorded.py (issue #252 there). An issue on
>   autopilot that GitHub still has blocked by an open issue builds nothing: no worker starts, no line stands in for
>   `/work`, and the card's Next line names the open issues it waits for and says it plans again, mentioning no one.
> - An issue closes. autopilot.yml runs the way GitHub runs it, on the machine of test_autopilot_close.py (issue #57
>   there). When the last open blocker of such an issue closes, autopilot starts a fresh planner run once, with
>   `Autopilot: blockers merged, starting plan`, and never the worker of the old plan.
> - A command the owner types by hand runs as today, through commands.yml, and a later close never overrides it.
> 
> Where GitHub cannot list an issue's blockers, the fake answers t

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_blocked_worker.py tests/test_work_column.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|353\.[0-9]" | head -40
```

> Proves 353.2.
>         record_property("proves", "353.2")
>         step, comment, out = approve_on(h, pl.links([301, 302]), "353.2", "blocked")
>         assert not step.startswith("start"), f"353.2: a plan approved with open blockers started {step!r}"
>         assert not os.path.exists(os.path.join(out, "autopilot.md")), "353.2: the worker's Autopilot line was still written"
>         assert h.writes("dispatch") == [], f"353.2: a stage was signalled: {h.writes('dispatch')}"
> >       assert old_lines(new_comments(h)) == [], f"353.2: #253's waiting-worker lines were posted: {new_comments(h)}"
> E       AssertionError: 353.2: #253's waiting-worker lines were posted: ['Autopilot: plan approved, waiting for #301 and #304 to close']
>         Proves 353.3.
>         record_property("proves", "353.3")
> >       assert_plans_again_once(m, "353.3", "last blocker closed")
> m = <test_autopilot_close.Repo object at 0x7f25749b9160>, crit = '353.3'
>         assert not m.failed, f"{crit} ({case}): a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 353.3 (last blocker closed): #57's worker started on its old plan, though only a fresh plan may follow
> E        +  where 1 = workers(<test_autopilot_close.Repo object at 0x7f25749b9160>, '353.3')
>         Proves 353.3.
>         record_property("proves", "353.3")
>             assert not m.failed and called, f"353.3: the owner's {said} on the waiting #57 did not start its stage:\n{m.tail()}"
> >           assert_starts_nothing(m, "353.3", f"the owner sa

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_blocked_worker.py tests/test_work_column.py 2>&1 | grep -E "^E .*353\.1|short test summary" -A0; timeout 600 python3 -m pytest -q tests/test_blocked_worker.py tests/test_work_column.py -rA 2>&1 | grep -E "^(FAILED|PASSED|SKIPPED)"
```

> E       AssertionError: 353.1 (plan approved while blocked, last blocker closed): #57's worker started on its old plan, though only a fresh plan may follow
> E        +  where 1 = workers(<test_autopilot_close.Repo object at 0x7f6d4dc1f2f0>, '353.1')
> =========================== short test summary info ============================
> PASSED tests/test_blocked_worker.py::test_when_github_cannot_list_the_blockers_the_worker_waits_and_the_issue_says_why
> PASSED tests/test_work_column.py::test_an_approved_plan_stays_in_plan_until_its_worker_starts
> PASSED tests/test_work_column.py::test_an_issue_is_in_work_once_its_worker_starts
> PASSED tests/test_work_column.py::test_a_built_issue_stays_in_work_until_its_code_review_starts
> PASSED tests/test_work_column.py::test_words_anyone_could_paste_start_no_worker_and_no_code_review
> PASSED tests/test_work_column.py::test_a_rebuilt_issue_stays_in_work_until_its_next_code_review_starts
> FAILED tests/test_blocked_worker.py::test_an_approved_plan_with_an_open_blocker_builds_nothing_and_says_what_it_waits_for - AssertionError: 353.2: #253's waiting-worker lines were posted: ['Autopilot: plan approved, waiting for #301 and #304 to close']
> FAILED tests/test_blocked_worker.py::test_the_last_blocker_closing_starts_a_fresh_plan_never_the_old_plans_worker - AssertionError: 353.3 (last blocker closed): #57's worker started on its old plan, though only a fresh plan may follow
> FAILED tests/test_blocked_worker.py::test_a_command_the_owner_types_while_it_waits_runs_a

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git show c16b878:tests/test_blocked_worker.py | grep -n "def test_"; sed -n 127,160p tests/test_blocked_worker.py; git show c16b878:tests/conftest.py | grep -n blocked_worker
```

> 77:def test_on_autopilot_a_blocked_plan_waits_with_one_line_and_mentions_no_one(tmp_path, record_property):
> 118:def test_when_github_cannot_list_the_blockers_the_worker_waits_and_the_issue_says_why(tmp_path, record_property):
> 198:def test_the_last_blocker_closing_starts_the_waiting_worker_once(tmp_path, record_property):
> 218:def test_a_worker_already_started_is_never_started_again(tmp_path, record_property):
> 236:def test_only_an_approved_newest_plan_starts_its_worker(tmp_path, record_property):
> 253:def test_a_close_that_cannot_list_the_blockers_starts_no_worker_and_says_why(tmp_path, record_property):
> 275:def test_agents_md_says_a_blocked_issue_plans_and_its_worker_waits(record_property):
> def test_when_github_cannot_list_the_blockers_the_worker_waits_and_the_issue_says_why(tmp_path, record_property):
>     """When GitHub cannot list the blockers, no worker starts and the card says why.
> 
>     #252 is on autopilot with a plan that has no links, and every read of #252's blocked-by list fails with
>     "HTTP 502: Server Error (blocked_by)". When the review approves, no stage starts, no Autopilot line is written,
>     and the record's comment, which the workflow posts on the issue, quotes GitHub's error. Beside it, the same plan
>     with the list readable starts the worker. Proves 253.4."""
>     record_property("proves", "253.4")
>     h = hub(tmp_path / "readable")
>     step, _, _ = approve_on(h, pl.links(), "253.4", "readable")
>     assert step == "start worker", f"253.4 (readable): with 

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "blockers closed\|GO_LINE\|WAIT_LINE\|waits on a blocker" dokima/ | head -20
```

> dokima/agent.py:1364:WAIT_LINE = "Autopilot: plan approved, waiting for {} to close"
> dokima/agent.py:1365:GO_LINE = "Autopilot: blockers closed, starting work"
> dokima/agent.py:1391:    gh("issue", "comment", str(number), "-R", repo, "--body", GO_LINE)
> dokima/agent.py:1762:    if who in owners and command_of(body) == "worker" and "(approved)" not in c.get("where", "") or who in (BOT, f"{BOT}[bot]") and body in (AUTOPILOT_LINES["worker"], GO_LINE):
> dokima/agent.py:1961:                    gh("issue", "comment", str(number), "-R", repo, "--body", WAIT_LINE.format(named(left)))

**Agent:** I re-ran the plan's tests: the old blocker is fixed. Writing the approval now.

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added a test for criterion 1 that runs in the normal test suite. It covers switching autopilot on, a split being filed, and a close that leaves a blocker open, and checks the good case beside each one.",
          "Stopped naming the three skipped slow tests as proof for criterion 1."],
  "decided": ["Kept the four criteria, the fail-closed requirement, the scope and the test changes from the first plan."],
  "open": ["Still recommends closing #313 as replaced by #353, since #313 asks for the opposite."]},
 "verdict": "approve",
 "summary": "Every criterion now has a test that runs in the normal suite and fails today for the right reason, so the plan is ready to build.",
 "blockers": [],
 "notes": [
  {"text": "The first of the two tests for the fail-closed requirement is an older test that still records itself as proving 253.4, not 353.5. It passes today, which is right, because that behavior is kept. The other test for that requirement does record 353.5, so the requirement still has proof.",
   "evidence": "tests/test_blocked_worker.py:133 record_property(\"proves\", \"253.4\")"},
  {"text": "tests/conftest.py still lists the four test_blocked_worker.py tests this plan deletes as slow. The stale names do no harm, but they could be cleaned up.",
   "evidence": "tests/conftest.py lines 45-48"},
  {"text": "Criterion 2 reads 'stops after plan review' as waiting quietly in Plan, with no Needs you and no mention of the owner. That fits 'the card says it waits for those issues', but the owner may want to confirm it.",
   "evidence": "Issue #353, 'What changes', item 2; plan criterion 2"}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [
  {"title": "Skipped slow tests still count as proof in the per-criterion check",
   "why": "A plan can name only tests on tests/conftest.py's SLOW list for a criterion. done-whens.yml then passes that criterion without runni
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="Every criterion now has a test that runs in the normal suite and fails today for the right reason; the plan is ready to build."
r["summary"]="Every criterion now has a test that runs in the normal suite and fails today for the right reason."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 353 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #353; the review is in `/tmp/dokima-out/review.json` and passes both checks.

**Last round's blocker (B1) is fixed.** Before, all three tests for criterion 1 ("a blocked issue on autopilot never starts its planner by itself") were skipped as slow, so that criterion would have passed without anything being run. The planner replaced them with one new test that runs in the normal suite. It covers all three moments: autopilot being switched on, a split being filed, and a close that leaves a blocker open. Beside each one it checks the good case, where the blocker has closed and the planner starts once.

**Test run:** I ran the plan's tests. Every new test fails today for the right reason, because the old code is still there:
- A plan approved while blocked still posts the old waiting line.
- When the last blocker closes, the worker builds the old plan instead of a fresh plan starting.
- The old waiting-worker code is still in `dokima/agent.py`.
- `AGENTS.md` doesn't describe the new rule yet.

The new test for criterion 1 fails on the case where a plan was approved while blocked. Its other cases pass today; they are there to catch the behavior breaking while the old code is removed.

**Notes (not blockers):**
- One of the two tests for the rule "when GitHub can't list the blockers, nothing starts" is an older test. It still labels itself as proof for 253.4, not 353.5. It passes today, which is correct because that behavior stays, and the second test does count for 353.5.
- `tests/conftest.py` still lists, as slow, four tests this plan deletes. The stale names do no harm.
- The plan reads the issue's "stops after plan review" as "waits quietly in Plan": no "Needs you" pill and no mention of you. That fits "the card says it waits for those issues", but you may want to confirm it's what you meant.

**One problem outside this issue, proposed for its own issue:** a plan could name only skipped slow tests for a criterion, and the per-criterion check would pass it without running anything.

The planner still recommends closing #313 as replaced by #353, since #313 asks for the opposite behavior.
