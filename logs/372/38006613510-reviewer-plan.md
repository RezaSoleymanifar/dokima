# reviewer (plan) for #372

Run: https://github.com/dokima-dev/dokima/actions/runs/38006613510

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #372: The card's Definition of Done shows a code review as running from the moment it is queued
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #372](https://github.com/dokima-dev/dokima/issues/372)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The Definition of Done on the issue and PR card shows Code review as running from the moment it is queued until it finishes, the same moment the board counts it as started (#343), and the card is redrawn when it starts, not only when it ends.
> 
> Owner's words (2026-10-09): "367 DoD is not up to date why? i thought we f

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print({k:v for k,v in d.items() if k!='handback'})" | head -50; git show --stat HEAD; cat tests/test_card_running.py
```

> {'role': 'planner', 'stage': None, 'run_id': '38006279439', 'commit_before': '39825a662f7f1107a85d897006f18f49fd757b6c', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 215223, 'turns': 22, 'cost_usd': 1.3970924, 'tokens_in': 1504978, 'tokens_out': 20487}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/372/38006279439-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/38006279439', 'check': {'passed': True, 'problems': []}}
> commit 60dce4d14098a52722ee01ddb752a10cd871fd59
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 23:53:29 2026 +0000
> 
>     planner for #372 (run 38006279439)
> 
>  tests/test_card_running.py | 209 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 209 insertions(+)
> """The Definition of Done shows Code review and All tests running while they run (#372).
> 
> Seen on #367: All tests had passed and the code review had been running for a minute, yet the card still said Code
> review "not started". dokima/card.py's code_review() knew only a finished review, and card.yml skipped the bot's own
> comments, so the review's live run card never redrew the card; and card.yml redrew only when the full suite finished,
> never when it started.
> 
> The first test draws the card from records and comments alone, through dokima/card.py's render(). The others play
> card.yml for one event at a time against a fake GitHub with tests/card_player.py, and re

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_card_running.py 2>&1 | grep -E "^(E  |FAILED|PASSED|[0-9]+ (passed|failed))|AssertionError|Error" | head -40
```

> E           AssertionError: 372.1: with the code review's run card up and queued, the Definition of Done should show Code review running, not 'not started': '<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review'
> E           assert 'not started' == 'running'
> E             
> E             - running
> E             + not started
> tests/test_card_running.py:88: AssertionError
> E           AssertionError: 372.2: the full suite started on PR #260, but issue #246's card shows All tests as None, not running; card.yml redraws only when the suite ends:
> E             
> E           assert None == 'running'
> tests/test_card_running.py:140: AssertionError
> E       AssertionError: 372.3: card.yml started on issue_comment created but its card job was skipped
> tests/card_player.py:938: AssertionError
> E       AssertionError: 372.4: card.yml started on issue_comment created but its card job was skipped
> tests/card_player.py:938: AssertionError
> FAILED tests/test_card_running.py::test_code_review_shows_running_from_its_queued_card_until_its_record - AssertionError: 372.1: with the code review's run card up and queued, the Definition of Done should show Code review running, not 'not started': '<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "running\|def code_review\|def all_tests\|in_progress" dokima/card.py | head -40; sed -n 1,80p .github/workflows/card.yml
```

> 34:ICON_FILE = {"passed": "passed", "failed": "failed", "running": "running", "not started": "none"}
> 196:    """GitHub's verdict for one check run (already filtered to the PR's latest commit): passed, failed, running or not started."""
> 201:    return "running" if check["status"] == "in_progress" else "not started"
> 379:def code_review(recs):
> 632:                     [run(n, "in_progress", None) for n in names],
> 633:                     dict(done, status="in_progress", conclusion=None), []),
> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, or a person changes or comments on an issue; the cards of the
> # issues it blocks or is blocked by follow when their links changed. GitHub
> # announces no event for a blocked-by link added or removed by hand, so a run
> # every 15 minutes catches up the cards whose links changed. A merged pull request redraws its card and its issue's,
> # whoever merged it. These triggers
> # always use the default branch's copy of this file and of dokima/card.py, so
> # the work being judged cannot change how it is reported.
> # An issue and its pull request share one queue, so the newest redraw waits for the
> # running one and is never cancelled, while other issues' redraws and the sweep go
> # on beside it.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [completed]
>   issues:
>   issue_comment:
>   pull_request_target:
>     types: [closed]
>   schedule:
>     - cron: '*/15 * * * *'
> permissio

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "live_card\|dokima-live" dokima/*.py .github/workflows/*.yml | head -30
```

> dokima/agent.py:32:LIVE = "<!-- dokima-live -->"
> dokima/agent.py:300:def live_card(role, stage, state, ahead=None):
> dokima/agent.py:371:    body = live_card(role, stage, state, ahead)
> dokima/agent.py:1946:        sys.stdout.write(scrub(live_card(argv[2], argv[3], argv[4]), secrets))

**Agent:** I'm checking where the bot posts the code review's run card, so I can tell whether the plan's redraw trigger covers it.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 295,400p dokima/agent.py; grep -n "live\b\|agent live\|live-card\|post_live\| live " .github/workflows/agent.yml | head -30
```

> is used, and the river starts nothing after it."""
>     return {"role": "cancelled", "attempt": role, "stage": stage or None, "agent_started": started, **meta,
>             "handback": {}, "check": {"passed": False, "problems": []}}
> 
> 
> def live_card(role, stage, state, ahead=None):
>     """The run's card while it is still running: queued (or waiting for the run `ahead` of it), setting up, agent
>     working since the agent started, then checking the hand-back.
> 
>     It carries its own marker and no JSON fold, so it never reads as a record; at the end of the run code edits this
>     same comment into the run's record. A hand-off's queued card is put up before its run exists, so it links none.
>     While the agent works the card is not edited, so it links the run's live page for detail."""
>     head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker",
>             "split": "Filing the split"}.get(role, "Command")
>     repo = os.environ.get("GITHUB_REPOSITORY", "")
>     run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
>     head = role_icon(repo, role, stage) + f"**{head}**"
>     if state in ("queued", "handoff"):
>         if ahead:
>             line = f"{icon(repo, 'queued')} {head} · waiting for [this run]({ahead})"
>             what = (f"Queued, and waiting for [this run]({ahead}) on the same issue to end; this run starts after it. "
>                     "This card says working when the agen

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Definition of Done" dokima/card.py | head; grep -n "def done_of" -A15 tests/card_player.py
```

> 401:    """The Definition of Done: All tests, the code review and the owner's approval, each with its verdict and proof.
> 408:    return ("**Definition of Done:** "
> 450:def done_of(text):
> 451-    """The Definition of Done a card shows: {All tests, Code review, Owner approval: passed/failed/...}."""
> 452-    line = next((l for l in (card_of(text) or "").splitlines() if l.startswith("**Definition of Done:**")), "")
> 453-    found = {}
> 454-    for part in line.split(" · "):
> 455-        alt = re.search(r'alt="([^"]+)"', part)
> 456-        for name in ("All tests", "Code review", "Owner approval"):
> 457-            if part.rstrip().endswith(name) and alt:
> 458-                found[name] = alt.group(1)
> 459-    return found
> 460-
> 461-
> 462-STALE_CARD = "<!-- dokima-card -->\n**Review**\n\nAn old card, drawn before the last event.\n\n<!-- /dokima-card -->"
> 463-
> 464-
> 465-class Hub:

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["The planner wrote three criteria: Code review shows running from the code review's queued run card until its record, All tests shows running once the full suite starts, and the code review's run card redraws the issue and PR cards.", "The planner wrote four tests in tests/test_card_running.py, one per criterion and one for the queue the new redraw waits in."],
  "decided": ["A running row uses dokima/icons/running.svg, as the owner said; Owner approval and the criterion rows' own circles stay as they are.", "The fix changes .github/workflows/card.yml, so the pull request stops for the owner to merge even on autopilot."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the owner and each of its four tests fails today because the card does not yet show or redraw a running code review or test suite.",
 "blockers": [],
 "notes": [{"text": "Today All tests already draws running for a check in progress; what 372.2 proves is the new redraw when the full suite starts, which is what the owner asked for.", "evidence": "dokima/card.py:201 maps an in_progress check to running; .github/workflows/card.yml listens to workflow_run types [completed] only"}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The Definition of Done on the issue and PR card shows Code review as running from the moment it is queued until it finishes", "source": "https://github.com/dokima-dev/dokima/issues/372", "criterion": "372.1"},
  {"ask": "the same moment the board counts it as started (#343)", "source": "https://github.com/dokima-dev/dokima/issues/372", "criterion": "372.1"},
  {"ask": "the card is redrawn when it starts, not only when it ends", "source": "https://github.com/dokima-dev/dokima/issues/372", "criterion": "372.3"},
  {"ask": "The same holds for every row that has a running state (All tests while the suite runs).", "source": "https://github.com/dokima
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan keeps every ask of the owner, and each of its four tests fails today because the card neither shows nor redraws a running row."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 372 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan keeps every ask of the owner, and its four tests fail today because the card neither shows nor redraws a running row."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 372 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#372](https://github.com/dokima-dev/dokima/issues/372) (the card's Definition of Done shows a queued code review as not started). It passes both checks, and `review.json` is in `/tmp/dokima-out`.

**Every ask is covered.** I found five asks in the issue and your comment, and each one has a criterion:
- **372.1:** Code review shows running from its queued run card until its record. That is the same moment the board counts it as started ([#343](https://github.com/dokima-dev/dokima/issues/343), when a queued code review counts as started), and it uses `dokima/icons/running.svg`.
- **372.3:** the card is redrawn when the code review starts.
- **372.2:** All tests shows running while the suite runs.

**All four new tests fail today, for the right reason:**
- **372.1:** with the code review's run card queued, Code review still shows not started.
- **372.2:** the cards are not redrawn when the full suite starts; `card.yml` only redraws when it ends.
- **372.3 and 372.4:** `card.yml` skips the bot's code review run card on the pull request, so its card job never runs.

**Tests that would catch a wrong build:** 372.1 also checks that a plan review's run card, a worker's run card, a card from before the newest build, and the same text posted by someone else all leave Code review not started. 372.3 checks that any other bot comment on the pull request still redraws nothing. 372.4 checks that the new redraw waits in the issue's own queue and never cancels a running one.

**One note, not a blocker:** the card already draws All tests as running when the check is in progress. The real fix for 372.2 is the redraw when the suite starts, which is what you asked for.

The fix changes `.github/workflows/card.yml`. The plan says this up front, so its pull request will stop for you to merge even on autopilot.
