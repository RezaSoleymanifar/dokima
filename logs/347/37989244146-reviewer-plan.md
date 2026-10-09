# reviewer (plan) for #347

Run: https://github.com/dokima-dev/dokima/actions/runs/37989244146

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #347: Every 15 minutes, any card that does not match its issue's state is redrawn
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 344, 345, 346 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> **Backlog**
> 
> [issue #347](https://github.com/dokima-dev/dokima/issues/347)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #344, #345, #346
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/own

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff HEAD~1 -- tests/test_hand_links.py; cat /tmp/pack/parent.json | head -50; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> commit 308721c020d0126e9f1d4c13dde1b6abdf335d42
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 20:46:25 2026 +0000
> 
>     planner for #347 (run 37987210127)
> 
>  tests/test_card_sweep.py | 331 +++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_hand_links.py |   9 +-
>  2 files changed, 336 insertions(+), 4 deletions(-)
> diff --git a/tests/test_hand_links.py b/tests/test_hand_links.py
> index 0005a53..41d9a94 100644
> --- a/tests/test_hand_links.py
> +++ b/tests/test_hand_links.py
> @@ -568,16 +568,17 @@ def test_card_yml_starts_on_every_change_a_person_makes_and_on_a_schedule(record
>  # 254.5 ---------------------------------------------------------------------------------------------------------------
>  
>  def test_the_scheduled_run_redraws_only_cards_whose_links_changed(tmp_path, record_property):
> -    """The scheduled run rewrites only the cards whose links changed.
> +    """The scheduled run rewrites the cards whose links changed, and nothing when nothing changed.
>  
> -    A person adds #252 blocked by #301 by hand: the scheduled run rewrites the cards of #252 and #301 only. The next
> -    scheduled run, with nothing changed, writes nothing on GitHub at all. Proves 254.5."""
> +    A person adds #252 blocked by #301 by hand: the scheduled run rewrites the cards of #252 and #301 (since #347 it
> +    also draws any card that does not show its issue's state, such as an issue with no card yet). The next scheduled
> +    run, with nothing c

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_sweep.py
```

> """Every 15 minutes, any card that does not match its issue's state is redrawn (#347).
> 
> The scheduled run of card.yml used to redraw only the cards whose blocked-by links changed, so a card whose redraw was
> missed (a dropped event, a merge before the PR card was written) stayed wrong for good. Now the sweep also redraws
> every issue card and PR card that does not show its issue's state now, looking only at the issues and pull requests
> GitHub says were updated since the last sweep that succeeded, so it stays cheap on a large repo. When GitHub cannot
> say what changed, or no sweep has succeeded yet, it rechecks every card instead of none.
> 
> These tests reuse the player and fake GitHub of tests/card_player.py (lifted from #332's tests on branch
> try/issue-332, whose sweep tests these adapt): card.yml is played the way GitHub runs it for the 15-minute schedule,
> running the real `python3 dokima/card.py` against the fake GitHub. The fake is extended here with two things GitHub
> has and the sweep needs:
> - `gh api repos/o/r/actions/workflows/card.yml/runs` (and the repo-wide `repos/o/r/actions/runs`) lists the runs
>   of card.yml the test recorded (newest first), filtered by the `event`, `status` and `branch` query parameters as
>   GitHub filters them (`status` matches a run's status or its conclusion); it can be told to refuse with HTTP 502.
>   Other workflows' runs are answered by the player's fake as before (none).
> - `gh api repos/o/r/issues?since=T` lists only the issues and pull request

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_card_sweep.py tests/test_hand_links.py 2>&1 | tail -30
```

> +  where True = stale(<test_card_sweep.SweepHub object at 0x7f574be26bd0>, 312)
> FAILED tests/test_card_sweep.py::test_a_card_that_already_shows_its_state_is_not_rewritten - AssertionError: 347.1: the first sweep did not put the stale cards of #246, #320 and PR #314 right, so nothing can be compared
> assert (not True)
>  +  where True = stale(<test_card_sweep.SweepHub object at 0x7f574be25e20>, 246)
> FAILED tests/test_card_sweep.py::test_the_sweep_only_looks_at_issues_and_prs_updated_since_the_last_sweep - AssertionError: 347.2: #246 was updated since the last sweep but its cards were not redrawn: '<!-- dokima-card -->\n**Review**\n\nAn old card, drawn before the last event.\n\n<!-- /dokima-card -->', '<!-- dokima-card -->\n**Review**\n\nAn old card, drawn before the last event.\n\n<!-- /dokima-card -->'
> assert (not True)
>  +  where True = stale(<test_card_sweep.SweepHub object at 0x7f574be19640>, 246)
> FAILED tests/test_card_sweep.py::test_a_failed_sweep_does_not_count_as_the_last_sweep - AssertionError: 347.2: #246 was updated after the last sweep that succeeded, but a newer failed sweep kept it from a redraw
> assert (not True)
>  +  where True = stale(<test_card_sweep.SweepHub object at 0x7f574be1acf0>, 246)
> FAILED tests/test_card_sweep.py::test_when_github_cannot_say_what_changed_every_card_is_rechecked - AssertionError: 347.3: GitHub could not say what changed, and the sweep left closed #246 or merged PR #260 stale
> assert ('Review' == 'Merged'
>   
>   - Merged
>   + Review)
> FAILED test

`5. Bash`
```
cd /home/runner/work/dokima/dokima; ls tests/ | head -80; git log --oneline -3 -- tests/card_player.py; timeout 300 python3 -m pytest -q tests/test_card_sweep.py tests/test_hand_links.py -rfs 2>&1 | grep -E "^(FAILED|SKIPPED|PASSED)" | cut -c1-250
```

> __pycache__
> card_player.py
> conftest.py
> fake_gh.py
> samples
> test_agent.py
> test_all_tests_judge.py
> test_answered_questions.py
> test_app.py
> test_assign.py
> test_audit.py
> test_audit_cli.py
> test_audit_workflow.py
> test_automerge.py
> test_autopilot.py
> test_autopilot_board.py
> test_autopilot_close.py
> test_autopilot_river.py
> test_autopilot_start.py
> test_blocked_worker.py
> test_blocker_pill.py
> test_board.py
> test_board_state.py
> test_body.py
> test_cancelled_run.py
> test_card.py
> test_card_bullets.py
> test_card_guard.py
> test_card_merge.py
> test_card_queue.py
> test_card_records.py
> test_card_status.py
> test_card_sweep.py
> test_checks.py
> test_clash.py
> test_design.py
> test_failed_run_card.py
> test_feature_check.py
> test_fence.py
> test_field_icons.py
> test_fixer.py
> test_gitignore.py
> test_hand_links.py
> test_handback_check.py
> test_issue_links.py
> test_keys.py
> test_link_lines.py
> test_live_card.py
> test_live_queue.py
> test_manifest.py
> test_merge_check.py
> test_merge_queue.py
> test_needs_you.py
> test_new_test_check.py
> test_open_ask.py
> test_parent_source.py
> test_pitch.py
> test_plan.py
> test_plan_check.py
> test_plan_check_rerun.py
> test_plan_links_recorded.py
> test_plan_shape.py
> test_planner.py
> test_planner_prompt.py
> test_progress_card.py
> test_questions.py
> test_raises.py
> test_replan_check.py
> test_review_asks.py
> test_run_cards.py
> test_sanity.py
> test_start.py
> test_summary_caps.py
> test_terms.py
> test_trail.py
> test_uptodate.py
> test_where_specs_go.py
> test_wiki.py
> test_word_caps.py
> test_work_column.py
> c16b878 One issue's card redraw nev

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git branch -a | grep 332; git fetch origin try/issue-332 2>&1 | tail -2; git show origin/try/issue-332 --stat 2>&1 | head; git ls-tree -r --name-only origin/try/issue-332 tests | grep -E "card_now|hand_links|card_player"
```

> remotes/origin/try/issue-332
> From https://github.com/dokima-dev/dokima
>  * branch            try/issue-332 -> FETCH_HEAD
> commit 3384ccb8fc751d041589b0eac33f3379a2e3c095
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 07:09:24 2026 +0000
> 
>     planner for #332 (run 37896965230)
> 
>  tests/test_card_now.py | 165 +++++++++++++++++++++++++++++++++++++++++--------
>  1 file changed, 138 insertions(+), 27 deletions(-)
> tests/test_card_now.py
> tests/test_hand_links.py

**Agent:** Checking how the plan's tests relate to #332's sweep tests, which the owner asked to reuse.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/try/issue-332:tests/test_card_now.py | grep -nE "^def test_|sweep|since" | head -60; git diff main origin/try/issue-332 -- tests/test_hand_links.py | head -40
```

> 5:redraw for good. Now any event about an issue or its pull request, and a sweep every 15 minutes, redraws both cards from
> 950:def test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now(tmp_path, record_property):
> 972:def test_an_event_redraws_an_open_issue_and_its_pr_from_the_records_now(tmp_path, record_property):
> 1010:def test_records_redraw_the_cards_and_the_cards_own_writes_redraw_nothing(tmp_path, record_property):
> 1042:def test_card_yml_starts_on_every_kind_of_event_about_an_issue_or_its_pr(tmp_path, record_property):
> 1104:def test_the_sweep_puts_right_every_stale_issue_card_and_pr_card_open_or_closed(tmp_path, record_property):
> 1105:    """Every 15 minutes a sweep puts right every stale card, open or closed.
> 1109:    and #320's card shows its plan. Then a person's event on each issue changes no card: the sweep left each one as
> 1113:    assert gap is not None and gap <= 15, f"332.2: card.yml's schedule leaves {gap} minutes between sweeps, not 15 or less"
> 1117:        f"332.2: the sweep left closed #246 or merged PR #260 showing an old card: " \
> 1120:        f"332.2: the sweep did not write #312's card on PR #314: {hub.pr_body(314)!r}"
> 1122:        f"332.2: the sweep left #320's card without its plan: {card_of(hub.issue_body(320))!r}"
> 1128:        "332.2: a redraw after the sweep changed an issue card, so the sweep did not leave it as GitHub's state draws it"
> 1130:        "332.2: a redraw after the sweep changed a PR card, so the sweep did not leave

`8. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/rv && cat > /tmp/rv/probe.py <<'EOF'
import sys, os
sys.path.insert(0, "tests")
import test_card_sweep as t
from card_player import schedule
def run(tmp):
    hub = t.SweepHub(tmp)
    hub.touch("issue", 246, "2026-10-09T06:00:00Z")
    hub.last_sweep("2026-10-09T05:00:00Z")
    hub.clear_calls()
    t.must_redraw(hub, schedule(), "x")
    calls = hub.calls()
    print("total calls", len(calls))
    for n in (312, 314):
        print(n, t.looked_at(calls, n)[:10])
import tempfile; run(tempfile.mkdtemp())
EOF
python3 -I /tmp/rv/probe.py 2>&1 | tail -20
```

> total calls 5
> 312 []
> 314 []

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/print("total calls", len(calls))/print("total calls", len(calls)); [print(c) for c in calls]/' /tmp/rv/probe.py; python3 -I /tmp/rv/probe.py 2>&1 | tail -12; grep -n "def merge\|def no_pr_card\|def add_issue\|updated_at\|def refuse" tests/card_player.py | head -30
```

> total calls 5
> ['api', 'repos/o/r/issues?state=open&per_page=100', '--paginate']
> ['api', 'repos/o/r/issues/246/dependencies/blocked_by', '--paginate']
> ['api', 'repos/o/r/issues/246/dependencies/blocking', '--paginate']
> ['api', 'repos/o/r/issues/312/dependencies/blocked_by', '--paginate']
> ['api', 'repos/o/r/issues/312/dependencies/blocking', '--paginate']
> 312 []
> 314 []
> 101:def refuse(op, n):
> 180:                "updated_at": x["updated_at"], "closed_at": x.get("closed_at"), "comments": len(x.get("comments", [])),
> 187:            "user": {"login": OWNER_LOGIN, "type": "User"}, "updated_at": i["updated_at"],
> 194:             "body": c["body"], "created_at": c["at"], "updated_at": c["at"]} for k, c in enumerate(cs)]
> 207:            "user": {"login": BOT_LOGIN, "type": "Bot"}, "updated_at": x["updated_at"],
> 216:            "url": f"https://github.com/{REPO}/pull/{p}", "updatedAt": x["updated_at"],
> 227:            "url": f"https://github.com/{REPO}/issues/{n}", "updatedAt": i["updated_at"], "closedAt": i.get("closed_at")}
> 255:    issue(n)["updated_at"] = tick()
> 263:    pr(p)["updated_at"] = tick()
> 484:    def add_issue(self, n, p=None, records=True):
> 491:            "title": f"Issue {n}", "state": "open", "labels": [], "updated_at": "2026-10-09T01:00:00Z",
> 499:                "updated_at": "2026-10-09T01:00:00Z"}
> 515:    def merge(self, n, p, by=OWNER):
> 519:                                closed_at="2026-10-09T09:00:00Z", updated_at="2026-10-09T09:00:00Z")
> 520:        s["issues"][st

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main origin/try/issue-332 -- tests/test_hand_links.py | sed -n 40,80p; grep -n "event\|workflow_run\|schedule\|cron" .github/workflows/card.yml | head -30
```

> @@ -568,16 +565,17 @@ def test_card_yml_starts_on_every_change_a_person_makes_and_on_a_schedule(record
>  # 254.5 ---------------------------------------------------------------------------------------------------------------
>  
>  def test_the_scheduled_run_redraws_only_cards_whose_links_changed(tmp_path, record_property):
> -    """The scheduled run rewrites only the cards whose links changed.
> +    """The scheduled run rewrites the cards whose links changed, and nothing when nothing changed.
>  
> -    A person adds #252 blocked by #301 by hand: the scheduled run rewrites the cards of #252 and #301 only. The next
> -    scheduled run, with nothing changed, writes nothing on GitHub at all. Proves 254.5."""
> +    A person adds #252 blocked by #301 by hand: the scheduled run rewrites the cards of #252 and #301 (since #332 it
> +    also draws any card that does not show its issue's state, such as an issue with no card yet). The next scheduled
> +    run, with nothing changed, writes nothing on GitHub at all. Proves 254.5."""
>      record_property("proves", "254.5")
>      hub = HandHub(tmp_path)
>      hub.set_links({N: [301]})
>      hub.sweep("254.5")
>      first = {w["issue"] for w in hub.writes("body")}
> -    assert first == {N, 301}, f"254.5: the scheduled run should rewrite only #252 and #301, it rewrote {sorted(first)}"
> +    assert {N, 301} <= first, f"254.5: the scheduled run should rewrite #252 and #301, it rewrote {sorted(first)}"
>      count = len(hub.writes())
>      hub.sweep("254.5")
>      ass

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote one user story with two criteria and two non-functional requirements, and eight new tests in tests/test_card_sweep.py.",
   "It adapted #332's sweep tests and fake GitHub from branch try/issue-332, and took #332's change to the 254.5 test in tests/test_hand_links.py."
  ],
  "decided": [
   "The sweep looks only at issues and pull requests updated since the last sweep that succeeded, and rechecks every card when GitHub cannot list earlier sweeps or none has succeeded.",
   "card.yml, the board and the stale-card scan of #333 stay out of scope; card.py is not rewritten."
  ],
  "open": []
 },
 "verdict": "block",
 "summary": "The plan matches the owner's two asks and every new test fails today for the right reason, but no test tells a sweep apart from card.yml's other runs, so code that starts from any run of card.yml that succeeded would pass while missing stale cards.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "347.2",
   "test": "tests/test_card_sweep.py::test_a_failed_sweep_does_not_count_as_the_last_sweep",
   "problem": "\"The last sweep that succeeded\" means the last scheduled run of card.yml. card.yml also runs on every issue event, comment, merge and worker run, and those runs succeed all the time. Every test records only scheduled runs (last_sweep defaults to event=\"schedule\"), so code that asks GitHub for the newest successful run of card.yml of any kind passes every test. On the real repo that would mean a redraw missed at 06:00 is skipped as soon as any other issue's event run succeeds at 06:05, which is the case the owner wants fixed.",
   "evidence": "tests/test_card_sweep.py SweepHub.last_sweep(at, conclusion=\"success\", event=\"schedule\"): no test calls it with another event. .github/workflows/card.yml lines 14-34 start the same workflow on workflow_run, pull_request_target, issues and issue_comment as well as the 1
```

> Exit code 1
> summary holds 45 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`12. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan covers both asks, but no test stops a sweep from counting card.yml's other runs as the last sweep."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 347 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #347 and sent it back to the planner over one weak test. The review is in `/tmp/dokima-out/review.json`, and it passes both checks.

**Blocker B1 (criterion 347.2, fixed by the planner):** "The last sweep that succeeded" should mean the last 15-minute run of card.yml. But card.yml also runs on every issue event, comment, merge and worker run, and those succeed constantly. Every test records only 15-minute runs. So code that counts any successful card.yml run as the last sweep would pass every test, yet skip a card whose redraw was missed whenever an unrelated event run finished after it. That is exactly the case the owner wants fixed.

The smallest fix is one more 347.2 case:
- the last 15-minute run succeeded at 05:00;
- an event-triggered card.yml run succeeded at 07:00;
- #246 was updated at 06:00;
- after one 15-minute run, #246's and PR #260's cards must be redrawn.

**What holds up:**
- Both of the owner's asks map to a criterion: 347.1 (redraw any card that doesn't match its issue's state) and 347.2 (only look at what changed since the last sweep).
- The planner reused #332's sweep tests and its change to `tests/test_hand_links.py`, as the owner asked.
- All 8 new tests in `tests/test_card_sweep.py` fail today for the right reason: stale cards aren't redrawn, and an unreadable card doesn't fail the run. None of them crash.
- I ran today's code against the 347.2 test's "makes no call about issues that weren't updated" check, and it passes. So the test can be met without touching the existing link check.
- The changed 254.5 test in `tests/test_hand_links.py` is skipped today (parked as slow), so I couldn't run it.

**Notes (not blockers):**
- The fake GitHub gives each recorded run the same start and end time. Code that counts from when the last sweep ended, rather than when it started, would also pass, and it would miss changes made while that sweep was running.
- The 254.5 test now accepts "at least #252 and #301 rewritten" instead of "only those two". Its "only" now rests on the second run writing nothing. This is #332's own change, reused as the owner asked.
