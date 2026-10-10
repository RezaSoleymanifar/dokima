# reviewer (plan) for #438

Run: https://github.com/dokima-dev/dokima/actions/runs/38094071797

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #438: One workflow redraws the card on every change to an issue or its pull request
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 437, 439 -->
> <!-- dokima-blocking: {"blocked_by": [437, 439], "blocks": [], "loop": []} -->
> **Plan**
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #437, #439
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #425, story 2</summary>
> 
> **Part of:** #425 The card always shows what is true right now: one rule, one place
> 
> **User story:** Whatever changes on an issue or its pull request, including the bot's own edits, its card and its pull request's card are redrawn from GitHub's state now, by card.yml alone.
> 
> **Context:** Today card.yml (.github/workflows/card.yml line 33) picks moments: it skips the bot's edits and comments except a code review's live card on a pull request, and redraws on run start only for the full suite. That is the #419 bug: the code review's record is an edit of its live card by the bot, so no redraw followed. Other writers: dokima/planner.py line 545 saves its own plan_text above the marker, and dokima/agent.py line 1388 calls card.draw for linked issues when a plan is approved. card.draw already has changed_only (dokima/card.py line 854), which keeps the bot's own card

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; wc -l tests/test_card_every_change.py; ls .github/workflows/; cat .github/workflows/playthrough.yml 2>/dev/null | head -60
```

> commit e496c72783684d4bc136d8d4a69734974937b542
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 23:09:54 2026 +0000
> 
>     planner for #438 (run 38092841362)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  tests/test_body.py                |  44 +--
>  tests/test_card.py                |   1 -
>  tests/test_card_every_change.py   | 693 ++++++++++++++++++++++++++++++++++++++
>  tests/test_card_guard.py          |   1 -
>  tests/test_card_merge.py          |  43 ---
>  tests/test_card_queue.py          |   9 +-
>  tests/test_card_running.py        |   6 +-
>  tests/test_hand_links.py          |   8 +-
>  tests/test_plan_links_recorded.py |   2 +
>  tests/test_playthrough.py         |  28 --
>  10 files changed, 701 insertions(+), 134 deletions(-)
> 693 tests/test_card_every_change.py
> acceptance-criteria.yml
> agent.yml
> assign.yml
> audit.yml
> autopilot.yml
> board.yml
> card.yml
> commands.yml
> full-suite.yml
> planner.yml
> playthrough.yml
> reviews.yml
> uptodate.yml
> wiki.yml
> worker.yml
> name: playthrough
> run-name: "play-through of ${{ inputs.commit }}"
> # Plays one issue on the sandbox repo dokima-dev/card-gallery from opened to merged with the Dokima commit given, and
> # says after each step whether both cards showed what had just happened (dokima/playthrough.py). Stand-in agents
> # call no model. The play-through installs the commit on the sandbox with SANDBOX_TOKEN, its own key that can write
> # only to card-gallery

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_every_change.py
```

> <persisted-output>
> Output too large (39.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/17069114-ec29-4cbe-972f-0ca546b42a94/tool-results/bbz5127j5.txt
> 
> Preview (first 2KB):
> """Every change on an issue or its PR redraws both cards from card.yml alone (#438).
> 
> Story 2 of #425.
> 
> #419: the code review had passed, yet the card said Code review running for 30 minutes. card.yml picked its moments:
> it skipped the bot's own edits and comments (except a code review's run card on a pull request) and redrew on a run's
> start only for the full suite. The review's record is the bot's edit of its run card, so nothing redrew. Beside
> card.yml, the old planner (dokima/planner.py, `post`) saved its own plan above the marker, and the plan approval
> (`python3 -m dokima.agent next`, dokima/agent.py record_links) drew the cards of the issues its links touched.
> 
> These tests play card.yml one event at a time on the fake GitHub of tests/card_player.py, run the play-through's
> steps there and judge them with dokima/playthrough.py's own judge, run the old planner's post and the plan approval
> against fakes, read .github/workflows/playthrough.yml, and run `python3 -m dokima.playthrough` with a temp git repo
> standing in for a pull request. Nothing calls real GitHub.
> """
> import json
> import os
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 30,400p tests/test_card_every_change.py
```

> from dokima import agent, body  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> PLAYTHROUGH_YML = os.path.join(ROOT, ".github", "workflows", "playthrough.yml")
> N, P = 246, 260
> # The activity types GitHub starts a workflow on when its `on:` names the event with no `types:`.
> DEFAULT_TYPES = {"pull_request_target": ("opened", "synchronize", "reopened"),
>                  "pull_request": ("opened", "synchronize", "reopened"),
>                  "workflow_run": ("requested", "completed")}
> SETTING = "Require status checks to pass before merging"
> 
> 
> # --- helpers -------------------------------------------------------------------------------------------------------
> 
> def github_starts(wf, event_name, event):
>     """True when GitHub itself would start `wf` on this event, default activity types included.
> 
>     tests/card_player.py starts a workflow on any action when its `on:` lists no types; GitHub does not for
>     pull_request_target and workflow_run, so this checks the types GitHub really uses."""
>     if not card_player.starts(wf, event_name, event):
>         return False
>     t = card_player.triggers(wf)[event_name]
>     types = card_player.listed(t.get("types")) if isinstance(t, dict) else []
>     action = event.get("action")
>     return bool(types) or event_name not in DEFAULT_TYPES or action in DEFAULT_TYPES[event_name]
> 
> 
> def reaches_card(event_name, event):
>     """True when GitHub starts card.yml on this event, itself or through a relay."""
>     if gith

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 400,693p tests/test_card_every_change.py
```

> Fails naming k when the workflow never starts on it."""
>     assert github_starts(wf, event_name, event), \
>         f"{k}: playthrough.yml does not start on {event_name} {event.get('action') or ''}".rstrip()
>     ctx, out = ctx_for(event_name, event), []
>     for key, job in (wf.get("jobs") or {}).items():
>         if card_player.listed(job.get("needs")):
>             continue
>         if evaluate(condition(job.get("if")), ctx, {"failed": False}):
>             out.append((fill(job.get("name") or key, ctx, {"failed": False}), job))
>     return out
> 
> 
> def play_step(job, ctx):
>     """The step of `job` running the play-through, with its env filled in."""
>     for step in job.get("steps") or []:
>         if "dokima.playthrough" in str(step.get("run") or ""):
>             env = {**(job.get("env") or {}), **(step.get("env") or {})}
>             return step, {k: fill(v, ctx, {"failed": False}) for k, v in env.items()}
>     raise AssertionError("no step runs python3 -m dokima.playthrough")
> 
> 
> def played_checkout(job, ctx):
>     """The checkout of the played commit (path `played`): its ref and fetch-depth, filled in."""
>     for step in job.get("steps") or []:
>         w = step.get("with") or {}
>         if "actions/checkout" in str(step.get("uses") or "") and str(w.get("path") or "") == "played":
>             return fill(w.get("ref") or "", ctx, {"failed": False}), fill(w.get("fetch-depth") or "1", ctx, {"failed": False})
>     raise AssertionError("no checkout has path `played`")
> 
> 
> def the_check(k):
>     "

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_card_every_change.py -x -q 2>&1 | tail -5; timeout 900 python3 -m pytest -q tests/test_card_every_change.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|AssertionError: 438" | head -40
```

> 438.1: card.yml does not start when the owner reviews the pull request, so its cards keep what they showed
>   438.1: card.yml does not start when the owner writes a note on a line, so its cards keep what they showed
>   438.1: card.yml started when the Acceptance criteria run starts but its card job did not run
> assert not ['438.1: card.yml started when the bot edits the issue but its card job did not run', '438.1: card.yml started when th...n', '438.1: card.yml started when the bot posts a plain comment on the pull request but its card job did not run', ...]
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> E       AssertionError: 438.1: not every change redraws both cards:
> E       AssertionError: 438.1: card.yml started when the bot edits the run card into the code review's record but its card job did not run
> E       AssertionError: 438.2: the plan approval saved the card of #252, #301, #302, #303 itself
> E       AssertionError: 438.2: the planner saved a card of its own above the marker: '- [ ] Objective: Owners see a card on every issue.\n  - [ ] Acceptance criteria: The issue shows a card on top.\n    Verified by: `tests/test_cardshow.py::test_card`\n\n**Scope:**\n- `dokima/card.py`\n\n<!-- dokima-ask -->\n<details><summary>Original issue</summary>\n\nMy ask.\n\n</details>'
> E       AssertionError: 438.3: the play-through does not pass every step:
> E       AssertionError: 438.4: playthrough.yml does not start on pull_request_target opened
> E       

**Agent:** Checked the plan's 12 new tests: each one fails today because the feature is missing. Next I'm running the full test suite to check the old tests the plan changed.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1500 python3 -m pytest -q -x -n auto 2>/dev/null | tail -3 || true; timeout 1700 python3 -m pytest -q --deselect tests/test_card_every_change.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -30
```

> 960 passed, 77 skipped, 12 deselected in 175.77s (0:02:55)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_body.py tests/test_hand_links.py tests/test_card_queue.py | head -150
```

> commit e496c72783684d4bc136d8d4a69734974937b542
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 23:09:54 2026 +0000
> 
>     planner for #438 (run 38092841362)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
> diff --git a/tests/test_body.py b/tests/test_body.py
> index ca316a9..f0853eb 100644
> --- a/tests/test_body.py
> +++ b/tests/test_body.py
> @@ -242,8 +242,10 @@ def test_the_card_never_changes_the_owner_part(record_property, monkeypatch, git
>      current = body.redraw(TRICKY, PLAN_TOP)
>      below = current.split(body.MARKER, 1)[1]
>      for k in range(3):
> +        # A card already current is not saved again (#438), so a later run that saves nothing keeps the body as it was.
>          saved = run_card(monkeypatch, github, current)
> -        assert saved is not None, f"179.2: card run {k + 1} saved nothing"
> +        assert saved is not None or k > 0, "179.2: the first card run saved nothing"
> +        saved = current if saved is None else saved
>          assert body.ask(saved) == TRICKY, f"179.2: card run {k + 1} changed the owner's ask"
>          assert saved.split(body.MARKER, 1)[1] == below, f"179.2: card run {k + 1} changed the part below the marker"
>          assert "first thing works" in saved.split(body.MARKER, 1)[0], f"179.2: card run {k + 1} lost the plan above"
> @@ -322,30 +324,6 @@ def test_the_card_refuses_rather_than_change_the_owner_part(record_property, mon
>      assert REASO

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned against today's main: five criteria and four non-functional rules, each with a test in tests/test_card_every_change.py, and 16 older tests changed or deleted with a reason each."],
  "decided": ["The pull request names the branch protection setting and the check's name in the header of playthrough.yml.",
              "The play-through also runs as the same check in the merge queue (438.9), a rule the owner did not write."],
  "open": ["A third play-through queued behind two cancels the one still waiting; raised as an issue outside this one."]},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the issue, and all 12 new tests fail today because the work is missing. It adds one rule the owner did not write, that the check also runs in the merge queue, and asks the owner about it.",
 "raises": [
  {"kind": "question", "to": "owner", "label": "Added rule",
   "text": "The plan adds a rule you did not write: the play-through check also runs in the merge queue, on the queued commit (438.9). Without it, a required play-through could hold every queued pull request forever once the merge queue is on. You asked to keep to your words and make the smallest change. Should 438.9 stay? The review assumes it stays, because it adds one trigger to playthrough.yml and nothing else.",
   "evidence": "plan.json non_functional[3] and tests/test_card_every_change.py::test_the_play_through_check_also_reports_in_the_merge_queue; the owner's comment of 2026-10-10T22:49:22Z: \"Keep to my words; smallest change.\""}
 ],
 "answers": [
  {"raise": "P1", "answer": "done", "why": "Confirmed: playthrough.yml uses the concurrency group playthrough with cancel-in-progress false, and GitHub keeps only one pending run per group, so a newer queued run cancels the older pending one. Once every card, board or workflow pull request plays, this is a real problem outside th
```

> Exit code 1
> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan keeps every ask and its 12 new tests fail today for the right reason; one added merge-queue rule goes to the owner."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for [#438](https://github.com/dokima-dev/dokima/issues/438) (one workflow redraws the card on every change), and asked you one question about it. Autopilot is off on this issue, so it now waits for your `/work`.

- **Your asks:** all eight asks in the issue (five criteria, three non-functional rules) are each covered by one criterion, 438.1 to 438.8.
- **Tests:** all 12 new tests in `tests/test_card_every_change.py` fail today, each because the work is missing, not because of a crash or a bad path. The rest of the suite passes with the planner's changes to 16 older tests: 960 passed, 77 skipped.
- **Your question:** the plan adds a rule you didn't write (438.9). The play-through check would also run on the queued commit in the merge queue. Without it, once the check is required and the merge queue is on, a queued pull request could wait forever. You asked to keep to your words and make the smallest change, so it's your call whether 438.9 stays. I assumed it stays, since it only adds one trigger to `playthrough.yml`. If you want it gone, answer with `/plan` before `/work`.
- **One reading the planner chose:** the pull request names the branch protection setting and the check's exact name in the header comment of `playthrough.yml`. I accepted that, because it lands with the code and a test can check it.
- **The planner's problem outside this issue:** I confirmed it. If three play-throughs queue up at once, GitHub cancels the one still waiting, and that pull request's check has to be re-run by hand. It's worth its own issue.

The review is in `/tmp/dokima-out/review.json` and passes both checks.
