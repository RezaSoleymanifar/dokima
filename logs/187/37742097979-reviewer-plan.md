# reviewer (plan) for #187

Run: https://github.com/dokima-dev/dokima/actions/runs/37742097979

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> .:
> total 48
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:13 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:13 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:13 in
> -rw-r--r--  1 runner runner 25303 Oct  8 07:13 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:13 open_blockers.json
> -rw-r--r--  1 runner runner  3597 Oct  8 07:13 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:13 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:13 ..
> -rw-r--r-- 1 runner runner 5962 Oct  8 07:13 01-planner.json
> -rw-r--r-- 1 runner runner 7146 Oct  8 07:13 02-planner.json
> -rw-r--r-- 1 runner runner 4207 Oct  8 07:13 03-planner.json
> # Issue #187: Live card: minutes and the current step while the agent works
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #164, story 3</summary>
> 
> **Part of:** #164 Visibility: one live card per run, from queued to done
> 
> **User story:** While an agent works, its card shows how many minutes it has run and the step it is on, so the owner can tell a slow run from a stuck one.
> 
> **Context:** The agent runs as one long step in agent.yml ('The agent (Claude Code)'), and Claude Code writes its session log under /home/runner/.claude/projects as it goes. transcript() in dokima/agent.py already reads those logs. A small loop beside the agent can read the newest tool call and edit the card every minute or so. Examples the owner gave: reading the issue, writing tests, checking its output. The step names come from what the

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/plan.json; git log --stat -3 | head -40; cat tests/test_progress_card.py
```

> {
>  "kind": "user_story",
>  "user_story": "Each run's card shows which coarse stage it is in (queued, setting up, agent working since HH:MM, checking, done), set by the run's own steps before and after the agent, with a link to the live run page while the agent works. No ticking minutes, no second job and no key on the agent's machine.",
>  "acceptance_criteria": [
>   {
>    "text": "A run's card goes through queued, setting up, agent working since HH:MM UTC, checking, then done (the run's record), each stage once, in that order. It says setting up by the time the run installs its tools, agent working when the agent starts, and checking when code starts checking the hand-back. A run that stops before its agent goes from queued (and setting up, if it got that far) straight to its record, never saying working or checking. The run's own job writes every stage; agent.yml keeps one job.",
>    "source": "https://github.com/dokima-dev/dokima/issues/187"
>   },
>   {
>    "text": "While the agent works, the card says agent working since the time it started (HH:MM UTC) and links to this run's live page on GitHub, with link words that say it is live, for detail. The card is not edited again until the agent ends, and no card ever counts minutes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/187"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "No key is on the agent's machine while the agent or the hand-back check runs: each key that moves the card is made for that one edit and revoked befo

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_progress_card.py 2>&1 | grep -E "^E   .*18[7]|passed|failed|Error" | head -30
```

> assert s.run.agent_started(), f"187.1 ({name}): setup: the agent never started; stopped at '{s.run.failed_step}':\n{s.tail()}"
> E           AssertionError: 187.1 (pass): the card went ["unknown: 'getting ready'", "unknown: 'working since 2026-10-08 07:14 UTC'", 'record'], expected ['queued', 'setting up', 'working', 'checking', 'record']:
> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (plan)**
> tests/test_progress_card.py:161: AssertionError
> E       AssertionError: 187.2: when the agent started the card did not say agent working since:
> tests/test_progress_card.py:193: AssertionError
> E       AssertionError: 187.3: no edit was made with the bot key between the agent's end and the hand-back check: the card never said checking
> tests/test_progress_card.py:235: AssertionError
>         posted exactly one record: the review's passed record."""
>         assert s.run.agent_started(), f"187.4: the agent never started once the card could not be edited; stopped at '{s.run.failed_step}':\n{s.tail()}"
> E       AssertionError: 187.4: the run tried 1 edits of the card before the agent and 1 after, expected at least two each (setting up and working; checking and the record)
> tests/test_progress_card.py:252: AssertionError
> FAILED tests/test_progress_card.py::test_the_card_goes_queued_setting_up_working_checking_done - AssertionError: 187.1 (pass): the card went ["unknown: 'getting ready'", "

`4. Bash`
```
cd /home/runner/work/dokima/dokima; ls tests; grep -n "getting ready\|working since\|Working since\|said\b" tests/*.py | grep -v test_progress_card | head -30; grep -n "def \(live\|card\)\|getting ready\|working since" dokima/agent.py | head
```

> __pycache__
> test_agent.py
> test_app.py
> test_assign.py
> test_board.py
> test_card.py
> test_card_guard.py
> test_checks.py
> test_design.py
> test_failed_run_card.py
> test_feature_check.py
> test_fence.py
> test_fixer.py
> test_gitignore.py
> test_handback_check.py
> test_keys.py
> test_live_card.py
> test_merge_check.py
> test_new_test_check.py
> test_pitch.py
> test_plan.py
> test_plan_check.py
> test_plan_shape.py
> test_planner.py
> test_planner_prompt.py
> test_progress_card.py
> test_questions.py
> test_sanity.py
> test_start.py
> test_terms.py
> test_trail.py
> test_wiki.py
> test_worker.py
> tests/test_agent.py:259:    """The transcript shows what the agent said, the tools it used and their results, and every secret value is removed."""
> tests/test_live_card.py:6:and the tests read what it left behind: which comments exist, what each said at each moment, and which key made each
> tests/test_live_card.py:155:    each leave exactly one comment: the very comment that said working when the agent started, now edited (not a new
> tests/test_plan_check.py:166:    "the owner said so",
> tests/test_plan_check.py:192:    "the owner said so",
> 217:def live_card(role, stage, state):
> 218:    """The run's card while it is still running: getting ready, then working since the agent started.
> 226:        line = f"{icon(repo, 'running')} **{head}** · working since {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC"
> 229:        line = f"{icon(repo, 'queued')} **{head}** · getting ready"
> 230:        what = "The machine is getting ready. This card says w

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,140p tests/test_live_card.py
```

> """Each agent run has one live card that turns from working into its result (#185).
> 
> These tests run the agent workflow (.github/workflows/agent.yml) the way GitHub runs it, with the machine from
> test_start.py: a fake GitHub that keeps every comment the run writes and every version of it, a fake Claude Code that
> notes what GitHub showed the moment it started, and nothing leaving the machine. Each scenario runs once per module
> and the tests read what it left behind: which comments exist, what each said at each moment, and which key made each
> call.
> """
> import calendar
> import json
> import os
> import re
> import time
> 
> import pytest
> 
> import test_start as ts
> from test_start import N, OWNER, PR, PIP_BROKEN, STORY_APPROVED, STORY_PLANNED, Run
> 
> from dokima import agent
> 
> ROOT = ts.ROOT
> ICON = re.compile(r'<img[^>]*src="https://raw\.githubusercontent\.com/[^/"]+/[^/"]+/main/dokima/icons/([A-Za-z0-9_-]+)\.svg"')
> TIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?(?:\.\d+)?\s*(?:UTC|Z)(?!\w)")
> EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‼⁉ℹ⌚-⏿Ⓜ"
>                    "▪-◾〰〽㊗㊙]")
> SHORTCODE = re.compile(r"(?<![\w/]):[a-z_+-][a-z0-9_+-]*:(?![\w/])")
> NEXT_STEP_FIX = "Fix the cause, then give the command again."
> BAD_REVIEW = {"verdict": "maybe"}
> 
> 
> class Scenario:
>     """One finished run of the agent workflow, with the time just before it started."""
> 
>     def __init__(self, tmp, *args, **kw):
>         self.t0 = time.time()
>         self.run = Run(tmp, *args, **kw)
>         gh

**Agent:** Checking whether the existing live-card tests from #185 would conflict with the new stages.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "versions\|proves\|queued\|revoke" tests/test_live_card.py | sed -n 1,80p
```

> 115:                             f"card: {[(where(c), c['versions'][-1][:200]) for c in cards]}\n{s.tail()}")
> 129:    record_property("proves", "185.1")
> 132:    body = c["versions"][-1]
> 146:    body = c["versions"][-1]
> 159:    record_property("proves", "185.2")
> 166:                              f"{[(where(c), c['versions'][-1][:150]) for c in cs]}")
> 169:        assert len(c["versions"]) > len(card["versions"]), f"185.2 ({name}): the working card was never edited into the result"
> 171:        final = c["versions"][-1]
> 195:    record_property("proves", "185.3")
> 202:                              f"{[(where(c), c['versions'][-1][:150]) for c in cs]}\n{s.tail()}")
> 205:            assert len(c["versions"]) >= 2 and not recs_of(c["versions"][0]) and icons(c["versions"][0]), \
> 207:                 f"version was:\n{c['versions'][0][:600]}")
> 208:        final = c["versions"][-1]
> 223:    record_property("proves", "185.4")
> 229:            for i, body in enumerate(c["versions"]):
> 239:    assert seen >= 10, f"185.4: setup: only {seen} card versions were written, too few to check every state"
> 248:    record_property("proves", "185.5")
> 252:            for body in c["versions"][:-1]:
> 256:            assert len(recs_of(c["versions"][-1])) == 1, f"185.5 ({name}): the finished card does not read as one record"
> 257:    assert earlier >= 6, f"185.5: only {earlier} versions of a card were written before its result: the runs put up no live card"
> 271:    record_property("proves", "185.6")
> 278:        

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 140,160p tests/test_live_card.py; sed -n 215,245p tests/test_live_card.py
```

> (f"185.1: the card's start time {m.group(0)} is not when the run started: the run began at "
>          f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s.t0))} UTC and the agent at "
>          f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s.agent_at))} UTC")
> 
>     s = runs["pr"]
>     c = working_card(s, "185.1", "pr", PR)
>     body = c["versions"][-1]
>     assert "working" in body.lower() and "running" in icons(body), \
>         f"185.1: the card on pull request #60 does not say working with the running icon:\n{body[:800]}"
> 
> 
> def test_the_same_comment_becomes_the_result_and_is_the_runs_only_comment(record_property, runs):
>     """At the end of the run its card, edited in place, becomes its record: done, or failed with why.
> 
>     A plan review that passes, one whose hand-back code rejects, and a worker run on an issue with an open pull request
>     each leave exactly one comment: the very comment that said working when the agent started, now edited (not a new
>     one), posted by Dokima's bot, holding exactly the run's own record and its Next line. The passed run shows the
>     passed icon; the rejected run shows the failed icon and lists the check's problems; neither still shows the
>     running icon."""
>     record_property("proves", "185.2")
>     for name, kind, number, role, passed in (("pass", "issue", N, "reviewer", True), ("fail", "issue", N, "reviewer", False),
> 
> 
> def test_every_state_of_the_card_shows_one_of_dokimas_own_icons_and_no_emoji(record_property, runs):
>     """Every ver

**Agent:** All four new tests fail today for the right reason, and they don't clash with #185's tests. One owner ask from the issue body was dropped without a word, so I'm writing the hand-back now.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote the plan to the owner's newest comment: the card goes queued, setting up, agent working since HH:MM UTC, checking, then the run's record, each stage set by the run's own single job, with a link to the live run page while the agent works.",
          "It replaced the tests in tests/test_progress_card.py with four that run the agent workflow end to end; all four fail today because the card still says getting ready and working since."],
  "decided": ["No ticking minutes, no step name, no second job; each key that moves the card is revoked before the agent starts and before the hand-back check.",
              "Queued is shown by the run's first step, not before its machine starts."],
  "open": ["It asks whether queued should show before the run's machine starts, which would need the listener to post the card with a key."]},
 "verdict": "block",
 "summary": "The plan follows your newest comment and its four tests fail today for the right reason, but it quietly drops the issue's rule that everything the card shows passes through scrub() first.",
 "blockers": [{"id": "B1", "criterion": "missing", "test": null,
   "problem": "The issue asks that the progress updates never leak a secret onto the card, with everything they show passed through scrub() first. The plan keeps the other non-functional ask (187.4) but has no criterion, no test and no question for this one, and its out-of-scope list does not mention it either. The owner's newest comment changed what the card shows but did not withdraw this rule.",
   "evidence": "Issue #187 body, Non-functional: 'The progress updates never leak a secret onto the card: everything they show passes through scrub() first.' plan.json non_functional holds only 187.3 (no key) and 187.4 (a refused edit never stops the run); out_of_scope lists only minutes, step, second job, early queued and the record's look.",
   "fix": "
```

> Exit code 1
> blocker B1 names missing, which is not a criterion of the plan (187.1, 187.2, 187.3, 187.4)

`9. Bash`
```
sed -i 's/"id": "B1", "criterion": "missing"/"id": "B1", "criterion": "187.1"/' /tmp/dokima-out/review.json && sed -i 's/"problem": "The issue asks/"problem": "No criterion holds this ask; it is filed under 187.1, the criterion for what the card shows. The issue asks/' /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 187 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #187 and sent it back to the planner over one dropped ask. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What holds up:**
- The plan follows your newest comment. The card goes queued, setting up, agent working since HH:MM UTC, checking, then the run's record. The run's own single job sets every stage, and the card links to the live run page while the agent works. There are no ticking minutes and no key on the agent's machine.
- I ran the four new tests and all four fail today for the right reason. For example, the card still says "getting ready" and "working since" instead of the new stage words. None of them failed because of a crash or a bad path.
- Each of your current asks is kept by one of 187.1–187.4. That includes the issue's other non-functional rule: if a card update fails, the run still finishes and posts its result.
- The new tests don't conflict with the existing #185 live-card tests.

**Blocker B1 (for the planner):** the issue says everything the progress updates show must pass through `scrub()` first, so no secret reaches the card. The plan has no criterion, test or question for this. Your newest comment changed what the card shows but didn't withdraw that rule. The fix is either:
- keep it as a rule with a test that puts a secret somewhere the stage cards are built from and checks no card version shows it, or
- ask you in the plan's questions whether it no longer matters, since the card now shows only fixed words, a time and the run link.

The check tool only accepts a blocker tied to one of the plan's criteria, so B1 is filed under 187.1, the criterion for what the card shows. The list of your asks marks this one as "missing".

**Note:** the new working card must still pass #185's test. That test needs the running icon and a full date with the time (YYYY-MM-DD HH:MM UTC). 187.2's time check doesn't require the date, so the worker should keep it.

The plan's one open question is still yours to answer: whether "queued" should show before the run's machine starts. The plan assumes no.
