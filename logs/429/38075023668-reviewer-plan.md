# reviewer (plan) for #429

Run: https://github.com/dokima-dev/dokima/actions/runs/38075023668

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
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
> # Issue #429: A board or card update the budget stopped is retried once the budget is back
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/429
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #368, story 4</summary>
> 
> **Part of:** #368 Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> **User story:** When GitHub's budget runs out, every board card and issue card the outage left behind is put right by itself once the budget resets, with no comment needed.
> 
> **Context:** After the 2026-10-09 outage (22:10Z to 22:29Z), #330 (closed at 22:24Z) and PR #327 stayed in the wrong columns until a comment forced a redraw. Main already has 15-minute sweeps that recheck what changed since the last sweep that succeeded: dokima/board.py changed() (about line 296) reads board.yml's newest successful schedule run, and card.yml sweeps the same way (from #356, merged 2026-10-09 21:10Z, before the outage). Why those sweeps did not catch #330 and #327 is the first thing to find: event-started runs that failed are not swept again unless the item was updated after the last successful sweep started, and a sweep that itself hits the limit fails as a whole. #417 is the sam

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/parent.json | head -50; git show --stat HEAD; wc -l tests/test_budget_retry.py
```

> {"number": 368}commit f6275674048bb92f549dc037ed32c199ffb491ee
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:14:54 2026 +0000
> 
>     planner for #429 (run 38073951824)
> 
>  tests/test_budget_retry.py | 483 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 483 insertions(+)
> 483 tests/test_budget_retry.py

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_budget_retry.py 2>&1 | tail -40
```

> def test_the_budget_is_read_from_githubs_rate_limit_endpoint(record_property, tmp_path, monkeypatch):
>         """The budget and its reset come from GitHub's free rate-limit endpoint.
>     
>         That endpoint costs nothing from either budget.
>     
>         Proves 429.4. A stand-in `gh` on PATH logs its arguments and answers as GitHub's GET /rate_limit does.
>         dokima.retry.rate_limit() must call exactly `gh api rate_limit` and return GitHub's answer, resets included; when
>         GitHub refuses, it must raise subprocess.CalledProcessError."""
>         record_property("proves", "429.4")
> >       retry = retry_module("429.4")
>                 ^^^^^^^^^^^^^^^^^^^^^
> 
> tests/test_budget_retry.py:463: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> 
> criterion = '429.4'
> 
>     def retry_module(criterion):
>         """dokima.retry, or a failure naming the criterion when it does not exist yet."""
>         try:
>             return importlib.import_module("dokima.retry")
>         except ImportError as e:
> >           pytest.fail(f"{criterion}: there is no dokima/retry.py with rate_limit(), sleep() and now() to wait for "
>                         f"GitHub's budget to reset ({e})")
> E           Failed: 429.4: there is no dokima/retry.py with rate_limit(), sleep() and now() to wait for GitHub's budget to reset (No module named 'dokima.retry')
> 
> tests/test_budget_retry.py:46: Failed
> =========================== short test summary info ============================
> FAI

**Agent:** Fails for the right reason. Now the test content.

`4. Read`
```
/home/runner/work/dokima/dokima/tests/test_budget_retry.py
```

> 1	"""Board and card updates the API budget stopped run again once it is back (#429).
> 2	
> 3	On 2026-10-09 the Dokima app's GraphQL budget hit zero at about 22:10Z and reset at 22:29Z. Board and card runs that
> 4	fell in that window failed, and #330 and PR #327 stayed in the wrong columns until a comment forced a redraw. Now
> 5	every board update (board.yml's event runs and 15-minute sweeps, and the board step at the end of an agent run) and
> 6	every card update (card.yml's redraws and sweeps) that fails while a budget is empty waits for GitHub's reported reset
> 7	time, then runs once more from scratch, so its cards show the state on GitHub then. Any other failure fails as today.
> 8	
> 9	The code under test is reached through three seams in dokima/retry.py, which every update must call through the
> 10	module, so a test can replace them:
> 11	    retry.rate_limit()  GitHub's `GET /rate_limit` answer as JSON ({"resources": {"core": {...}, "graphql": {...}}});
> 12	                        raises subprocess.CalledProcessError when GitHub refuses.
> 13	    retry.sleep(s)      waits s seconds.
> 14	    retry.now()         the time now, in epoch seconds.
> 15	Budget below fakes all three on one clock: a budget is empty until its reset time, and GitHub refuses the reads the
> 16	test names while any budget is empty, with GitHub's own words ("API rate limit already exceeded"). time.sleep is
> 17	made to fail, so a real wait can never hang the suite. The board is test_needs_you's in-memory world, as in
> 18	test

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 270,360p dokima/board.py; cat .github/workflows/card.yml | head -80; grep -n "^def \|^    def main\|__main__" dokima/card.py | head -60
```

> board.label("pr", pr, on)
>     if not on:
>         return
>     # Only the top of a tree switched on adds the view: its sub-issues' board runs may overlap it and read no view yet.
>     up = board.parent(number)
>     if up and board.autopilot("issue", up):
>         return
>     try:
>         if "Autopilot" not in board.views():
>             view = manifest.VIEWS["Autopilot"]
>             board.add_view("Autopilot", view["layout"], view["filter"])
>     except subprocess.CalledProcessError as e:
>         raise RuntimeError(f"Could not add the Autopilot view to the board: {reason(e)}") from e
> 
> 
> def fix_view(board):
>     """Move an Autopilot view still on label:autopilot to the manifest's filter; others are the owner's."""
>     new = manifest.VIEWS["Autopilot"]["filter"]
>     try:
>         for v in board.view_nodes():
>             if v["name"] == "Autopilot" and v.get("filter") == f"label:{AUTOPILOT}":
>                 board.set_view_filter(v["id"], new)
>     except subprocess.CalledProcessError as e:
>         raise RuntimeError(f"Could not fix the Autopilot view's filter to {new}: {reason(e)}") from e
> 
> 
> def changed(repo):
>     """[(kind, number)] updated since the last sweep that succeeded, or None to recheck every card."""
>     try:
>         runs = json.loads(agent.gh("api", f"repos/{repo}/actions/workflows/board.yml/runs?event=schedule&status=success&per_page=1"))["workflow_runs"]
>         found = json.loads(agent.gh("api", f"repos/{repo}/issues?state=all&since={runs[0]['run_started_at']}&per_page=100",

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 760,870p dokima/card.py; grep -n "refuse\|closed\b\|self.closed\|def fake_board\|def fake_gh\|class World" tests/test_needs_you.py | head -30; grep -n "def main" -A40 dokima/board.py | head -70
```

> try:
>             draw(repo, n, pr_number or issue_pr(repo, n), cache=cache, changed_only=True)
>         except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
>             print(f"::error title=Card not updated::the card of #{n} could not be updated: {reason(e)}")
>             failed += 1
>     return failed
> 
> 
> def sweep(repo):
>     """The scheduled run: close finished parents, redraw cards whose links changed, then stale cards.
> 
>     A finished parent is an open one whose sub-issues are all closed (see agent.close_done_trees).
> 
>     The link check looks at every open issue and every issue linked to one; the stale cards are looked for only among
>     the issues and PRs updated since the last sweep (see stale_cards)."""
>     from dokima import agent
>     cache, failed = {}, 0
>     try:
>         # The safety net for a close whose run never went: every open parent whose sub-issues are all closed closes.
>         for line in agent.close_done_trees(repo):
>             print(line)
>     except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
>         print(f"::error title=Parents not closed::the open parents whose sub-issues are all closed could not be closed: {reason(e)}")
>         failed += 1
>     bodies = {i["number"]: i["body"] for i in agent.open_issues(repo)}
>     numbers = set(bodies)
>     for n, text in bodies.items():
>         got = blocking(repo, n, cache)
>         numbers |= {m for links in (got if i

`7. Bash`
```
mkdir -p /tmp/rv && cat > /tmp/rv/fakeretry.py <<'EOF'
import sys, types, time
m = types.ModuleType("dokima.retry")
m.rate_limit = lambda: {}
m.sleep = time.sleep
m.now = time.time
import dokima
sys.modules["dokima.retry"] = m
dokima.retry = m
EOF
cd /home/runner/work/dokima/dokima; PYTHONPATH=/tmp/rv timeout 600 python -m pytest -q -p fakeretry tests/test_budget_retry.py 2>&1 | grep -E "^(FAILED|PASSED|E  )|passed|failed" | cut -c1-300
```

> (Bash completed with no output)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; PYTHONPATH=/tmp/rv:. timeout 600 python -m pytest -q -p fakeretry tests/test_budget_retry.py -rA 2>&1 | tail -20 | cut -c1-300
```

> ==================================== PASSES ====================================
> =========================== short test summary info ============================
> PASSED tests/test_budget_retry.py::test_a_board_update_failing_for_another_reason_fails_as_today
> PASSED tests/test_budget_retry.py::test_a_card_update_failing_for_another_reason_fails_as_today
> FAILED tests/test_budget_retry.py::test_a_board_event_run_the_budget_stopped_runs_again_after_the_reset - subprocess.CalledProcessError: Command '['gh', 'api', 'graphql']' returned non-zero exit status 1.
> FAILED tests/test_budget_retry.py::test_a_board_sweep_the_budget_stopped_runs_again_after_the_reset - AssertionError: 429.1: the sweep was stopped by the empty budget and exited 1, not 0 after the reset
> assert 1 == 0
> FAILED tests/test_budget_retry.py::test_the_board_step_at_the_end_of_a_run_runs_again_after_the_reset - AssertionError: 429.1: the end-of-run board step was stopped by the empty budget and exited 1, not 0
> assert 1 == 0
> FAILED tests/test_budget_retry.py::test_a_card_redraw_the_budget_stopped_is_redrawn_after_the_reset - AssertionError: 429.2: the card redraw was stopped by the empty budget and the run ended with CalledProcessError(1, ['gh', 'issue', 'view', '57']), not 0
> assert CalledProcessError(1, ['gh', 'issue', 'view', '57']) == 0
> FAILED tests/test_budget_retry.py::test_a_card_sweep_the_budget_stopped_runs_again_after_the_reset - AssertionError: 429.2: the card sweep was stopped by the empty budget and the run 

`9. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print(d.keys());print({k:v for k,v in d.items() if k!='handback' and k!='plan'})" | cut -c1-1500
```

> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> {'role': 'planner', 'stage': None, 'run_id': '38073951824', 'commit_before': 'da897bc1861cfb03502c1a4c1b9ebdd3ac11d00c', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 884966, 'turns': 36, 'cost_usd': 2.8904425999999996, 'tokens_in': 3622584, 'tokens_out': 53433}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/429/38073951824-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/38073951824', 'check': {'passed': True, 'problems': []}}
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** I've checked the plan's tests: they fail today for the right reason. Now I'm writing the review and running the hand-back check.

`10. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Wrote three criteria and one non-functional rule: board and card updates stopped by an empty GitHub budget wait for the reset and run once more; any other failure fails as today.",
   "Wrote ten tests in tests/test_budget_retry.py; every one fails today because dokima/retry.py does not exist."
  ],
  "decided": [
   "A failure counts as a budget failure only when GitHub's rate-limit endpoint reports 0 left right after it; the wait is inside the update's own step, so no workflow file changes.",
   "Finding out why the 2026-10-09 sweeps missed #330 and PR #327 is left out of scope, since every board and card run now waits out the outage itself."
  ],
  "open": [
   "The owner decides whether the board step at the end of an agent run also waits, which can start the next stage up to an hour later."
  ]
 },
 "verdict": "approve",
 "summary": "The plan carries every ask of story 4, and its tests fail today because the retry is missing and would fail on any run that does not wait for the reported reset, waits twice, or retries a failure that is not the budget's.",
 "raises": [
  {
   "kind": "issue",
   "label": "Sweeps that missed the outage",
   "text": "Why the 15-minute board and card sweeps after the 2026-10-09 outage did not put #330 and PR #327 right is still not explained. This plan leaves it out of scope and relies on the next sweep to fix a card whose second try also fails, so a gap in the sweeps would still leave a card stale.",
   "evidence": "Issue #429's Context: 'Why those sweeps did not catch #330 and #327 is the first thing to find'; the plan's out of scope: 'the next 15-minute sweep puts those cards right'. dokima/board.py changed() reads only issues updated since the last successful schedule run started."
  }
 ],
 "answers": [],
 "asks": [
  {"ask": "When GitHub's budget runs out, every board card and issue card the outage left behind is put right b
```

> Exit code 1
> summary holds 43 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan carries every ask of story 4, and its tests fail today only because the wait for GitHub's budget reset is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 429 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#429](https://github.com/dokima-dev/dokima/issues/429) (board and card updates retried once the API budget is back). The review is in `/tmp/dokima-out/review.json`, and it passes both hand-back checks.

**Why it passes:**
- **Every ask is covered.** The user story, the three acceptance criteria and the "wait for GitHub's reported reset" rule each map to a criterion (429.1 to 429.4), and nothing is missing.
- **The new tests fail today for the right reason.** All ten fail because `dokima/retry.py` doesn't exist yet. I also ran them against a stand-in retry module that never waits:
  - The 8 tests for the new behaviour fail on that behaviour being missing: exit code 1 or a crash instead of 0, no wait, or one try instead of two.
  - The 2 tests for "any other failure fails as it does today" (429.3) pass, as they should.
- **The tests would catch a wrong build.** They fail if a run doesn't wait, retries before the reset, waits for the wrong one of the two budgets, waits twice or retries a non-budget failure. The fake clock means a real wait can't hang the test suite.
- **`dokima/card.py` is in scope, which is acceptable.** AGENTS.md normally forbids changing it, but the issue asks for card redraws to be retried. Those redraws run in that file, and the plan leaves the workflow files alone.

**Left for you:**
- **The planner's question P1 is still open.** It asks whether the board step at the end of an agent run should also wait for the reset, which could delay the next stage by up to an hour. On autopilot I could have answered it for you, but only if the answer changed nothing about how the system works. This one changes when stages start, so you decide.
- **I proposed one new issue.** The issue's Context says that finding why the 15-minute sweeps missed #330 and PR #327 after the 2026-10-09 outage is "the first thing to find". The plan puts that out of scope instead, and relies on the next sweep to fix any card whose second try also fails. That sweep fallback hasn't been shown to work, so I raised it as its own issue rather than a blocker.
