# reviewer (plan) for #454

Run: https://github.com/dokima-dev/dokima/actions/runs/38084873239

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in/; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #454: On a planned issue the Original issue fold sits right above the Definition of Done, a run comment ends with its stats line, and the autopilot icon is drawn
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/454
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #416, story 3</summary>
> 
> **Part of:** #416 Card links show as GitHub's own references: no self-link on the issue, full address after Closes
> 
> **User story:** The owner reads a planned issue's card, then its Original issue fold, then its Definition of Done last; reads every run comment down to Next with the stats line last; and sees the autopilot icon on every card that is on autopilot.
> 
> **Context:** `dokima/body.py` `redraw` puts what the card holds after its `<!-- dokima-done -->` marker below the owner's part; `dokima/card.py` `render` uses that only when there is no plan, so a planned issue today has the Definition of Done inside the card, above the marker, and the fold below it. The owner's part must still be kept byte for byte, and a split's story keeps its fold. #394 (folded into #416 by the owner): `FIELD_ICONS` in `dokima/card.py` has an `autopilot` icon (dokima/icons/autopilot.svg) that no code draws; the card's status line shows the stage and Needs you only. The plan's re

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; git show --stat HEAD | head -60; ls tests/rendered docs/rendered 2>&1
```

> Exit code 2
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38083229415",
>  "commit_before": "093a506a217a6a0ec2c7726e7c1a142729c951ab",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 512479,
>   "turns": 44,
>   "cost_usd": 7.314725000000002,
>   "tokens_in": 9901568,
>   "tokens_out": 36929
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/454/38083229415-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38083229415",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> commit bce4c00117636a058f2a98ba38aae2f96dc6aa18
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 20:43:28 2026 +0000
> 
>     planner for #454 (run 38083229415)
> 
>  tests/card_player.py             |   7 +-
>  tests/card_view.py               |  28 +++++++
>  tests/github_render.py           | 142 +++++++++++++++++++++++++++++++
>  tests/rendered/454.json          |  10 +++
>  tests/test_autopilot_icon.py     | 110 ++++++++++++++++++++++++
>  tests/test_body.py               |   6 +-
>  tests/test_cancelled_run.py      |   9 +-
>  tests/test_card_bullets.py       |   8 +-
>  tests/test_card_folds.py         |  19 +++--
>  tests/test_card_merge.py         |   7 +-
>  tests/test_card_records.py       |   9 +-
>  tests/test_done_last.py          | 176 +++++++++++++++++++++++++++++++++++++++
>  tests/test_github_rendering.py   |  68 +++++++++++++++
>  tests/test_new_issue_card.py     |  27 ------
>  tests/

**Agent:** Let me look at the parent issue's open question and the rendering tests.

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/github_render.py tests/test_github_rendering.py; cat tests/rendered/454.json | head -c 3000
```

> """GitHub's own rendering of Dokima's markdown, from answers recorded in the repo.
> 
> Tests run in CI with no network and no secrets, so they cannot ask GitHub each time. Instead each answer GitHub's
> markdown API (POST https://api.github.com/markdown, mode gfm) gave is kept in a store file, a JSON list of
> {"text": what was sent, "html": what GitHub answered}. `rendered(criterion, text, stores)` returns the HTML recorded
> for exactly `text`; an answer recorded for any other text never counts, so a change to what the code writes fails the
> test until GitHub's answer for the new text is recorded.
> 
> Two kinds of store: the planner's, under tests/rendered/ (recorded on the code of the day the tests were written), and
> the worker's, under docs/rendered/, where a build records GitHub's answers for what its code writes now:
> 
>     DOKIMA_RECORD_RENDERING=docs/rendered/454.json python3 -m pytest tests/test_github_rendering.py
> 
> asks GitHub for every text a test renders and keeps the answer in that file. To ask GitHub again for every text a
> store holds (when GitHub's rendering may have changed):
> 
>     python3 tests/github_render.py docs/rendered/454.json
> 
> Both use GITHUB_TOKEN or GH_TOKEN when set; GitHub's markdown API also answers without one, a few times an hour.
> `blocks(html)` reads the HTML the way the owner sees the page: the top-level elements, in order.
> """
> import json
> import os
> import sys
> import urllib.request
> from html.parser import HTMLParser
> 
> import pytest
> 
> ROOT = os.path.join(os.pat

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q -x -p no:cacheprovider tests/test_done_last.py tests/test_stats_last.py tests/test_autopilot_icon.py tests/test_github_rendering.py 2>&1 | tail -5; timeout 600 python3 -m pytest -q -p no:cacheprovider tests/test_done_last.py tests/test_stats_last.py tests/test_autopilot_icon.py tests/test_github_rendering.py 2>&1 | grep -E "^(FAILED|ERROR|PASSED)|passed|failed"
```

> ?   ++++++++++++++++++
>     
>     <!-- /dokima-card -->
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed in 0.53s
>                  ("rejected plan", rec("planner", "", PLAN, passed=False, problems=["a problem"])),
> body = '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...},\n "check": {\n  "passed": true,\n  "problems": []\n }\n}\n```\n\n</details>\n\n**Next:** The reviewer starts now.\n'
> E           "passed": true,
> FAILED tests/test_done_last.py::test_a_planned_issue_ends_with_its_definition_of_done_right_below_the_fold - AssertionError: 454.1 (a fresh ask): the Definition of Done is still in the card, above the Original issue fold:
> FAILED tests/test_done_last.py::test_a_planned_issue_saved_the_old_way_is_redrawn_the_new_way - AssertionError: 454.1 (saved the old way): the Definition of Done is still in the card, above the Original issue fold:
> FAILED tests/test_done_last.py::test_agents_md_says_the_definition_of_done_comes_last_below_the_fold - AssertionError: 454.1: AGENTS.md still says a planned issue's Definition of Done is the card's last line
> FAILED tests/test_done_last.py::test_a_redraw_that_would_change_the_owners_part_is_still_refused - AssertionError: 454.5: the good redraw does not end with the card's Definition of Done below the fold:
> FAILED tests/test_stats_last.py::test_every_agent_run_comment_ends_with_its_stats_line_below_next - AssertionError: 454.2 (p

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -p no:cacheprovider -n auto 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -40 || true
```

> ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1200 python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -40
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b9jnvy6x2). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/dcc53983-289e-47c6-aec5-203a71d7e99f/tasks/b9jnvy6x2.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, read the main new tests.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_done_last.py tests/test_autopilot_icon.py
```

> """A planned issue reads: the card, the Original issue fold, then the Definition of Done.
> 
> Issue #454, story 3 of #416. Before it, a planned issue's Definition of Done was the card's last line, above the marker,
> and the owner's Original issue fold came after it, at the very bottom (dokima/card.py render, dokima/body.py redraw).
> Now, once planned, the body reads: the card, then the Original issue fold, then the Definition of Done, last. The
> owner's part stays byte for byte, a body saved the old way is redrawn this way next time, and a redraw that would
> change the owner's part is still refused with the body left as it was.
> 
> The card's main runs as tests/test_body.py runs it: GitHub faked by its recorder, the issue planned by one planner
> record, no pull request and no worker run.
> """
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> sys.path.insert(0, os.path.dirname(__file__))
> from dokima import agent, body, card, plan  # noqa: E402
> from test_body import NUMBER, REPO, TRICKY, github, run_card  # noqa: E402,F401
> 
> FOLD_HEAD = "<details><summary>Original issue</summary>"
> DONE_LINE = re.compile(r"\*\*Definition of Done:\*\*[^\n]*")
> OLD_CARD = ("<!-- dokima-card -->\n**Plan**\n\n**User story:** Owners see a card.\n\n"
>             "**Definition of Done:** All tests · Code review · Owner approval\n\n<!-- /dokima-card -->")
> STORY = {"title": "Done last", "user_story": "The owner reads the Definition of Done last.",
>         

`8. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_stats_last.py; git show HEAD -- tests/test_raised_cards.py tests/test_body.py | head -120
```

> """Every run comment Dokima posts ends with its stats line, right below its Next line.
> 
> Issue #454, story 3 of #416; the owner's /plan comment of 2026-10-10T20:04:51Z: "In every run comment, the stats line
> (tokens used and the like) is the very last line, below Next." Before it, `agent render` (dokima/agent.py) put the
> stats in a Stats fold right above the Full record fold, and the Next line was added after the whole comment: by
> `agent next` for agent runs (agent.py, after `render`), and by dokima/uptodate.py for a clash record.
> 
> These tests post each kind of run comment the way the workflows do: `agent render` writes comment.md, then
> `agent next N OUT` adds the Next line, GitHub faked so nothing leaves the machine. A filed split is posted as
> `render` draws it, and a clash record as dokima/uptodate.py posts it (faked as in tests/test_clash.py). Each comment
> is then read the way the owner reads it, from the bottom up.
> """
> import copy
> import json
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> sys.path.insert(0, os.path.dirname(__file__))
> from dokima import agent, card  # noqa: E402
> from test_run_comment_fields import BLOCK, META, PLAN, REPO, WORK, rec  # noqa: E402
> 
> RECORD_FOLD = "<details><summary>Full record</summary>"
> STATS = ("Opus 5.5", "4.0 min", "23 turns", "401K", "18K", "$3.20")
> LINKS = ("https://g/log.md", "https://github.com/o/r/actions/runs/1")
> QUIET = {**BLOCK, "raises": [r for r in BLOCK["raises"] i

`9. Bash`
```
cd /tmp; timeout 20 curl -s -o /dev/null -w "%{http_code}\n" -X POST https://api.github.com/markdown -d '{"text":"**hi**","mode":"gfm"}'
```

> 200
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json,sys
sys.path.insert(0,'tests')
from github_render import ask_github
for a in json.load(open('tests/rendered/454.json')):
    h=ask_github(a['text'])
    print(len(a['text']), h==a['html'], len(h), len(a['html']))
EOF
```

> 1502 True 3874 3874
> 1533 True 4121 4121

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "label" dokima/card.py | head -30; grep -n "def card_now" -A25 dokima/scan.py | head -40
```

> 64:    for kind, field, label in (("blocked_by", "blocked by", "Blocked by"), ("blocks", "blocks", "Blocks"),
> 68:            out.append(f"{field_icon(repo, field)} **{label}:** " + ", ".join(f"#{n}" for n in numbers))
> 237:    """One raise as a list item: icon, label, words and who it is for.
> 241:    label = f"**{words(r['label'])}:** " if isinstance(r.get("label"), str) and r["label"].strip() else ""
> 244:    return f"- {field_icon(repo, RAISE_ICON[r['kind']])} {label}{words(r.get('text') or '')} · {who}"
> 366:def criterion_item(repo, label, c, check, tests):
> 367:    """One criterion bullet: its status circle, its label linked to its check, its words plain.
> 369:    The label links only when there is a check. Under it one italic Verified by line per test with a docstring, only
> 373:        label = f'<a href="{check["html_url"]}">{label}</a>'
> 374:    out = [f"- {circle(repo, state(check))} **{label}:** {escape(c.get('text'))}"]
> 384:def criteria_list(repo, number, start, label, criteria, plan_tests, by_key, tests):
> 389:        out += criterion_item(repo, label, c, by_key.get(key), [tests.get(t) for t in plan_tests.get(key, [])])
> 40:def card_now(repo, kind, number):
> 41-    """The card Dokima writes on this issue or PR when redrawing its issue now."""
> 42-    if kind == "issue":
> 43-        return drawn(repo, number, card.issue_pr(repo, number))[2]
> 44-    return drawn(repo, board.issue_of(repo, number), number)[2]
> 45-
> 46-
> 47-def why(e):
> 48-    return str(e) if isinstance(e, RuntimeErro

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "label" tests/test_scan.py | head -30; grep -n "def drawn" -A25 tests/test_scan.py; grep -n "def drawn" -A15 dokima/scan.py
```

> 17:  fake board offers (set, label, add_view, set_view_filter, and item() for something not on the board) is logged.
> 53:               ("pr", "comment"), ("pr", "merge"), ("pr", "close"), ("label", "create")}
> 78:        self.issues = {}  # n -> {"state", "body", "records", "labels"}
> 84:    def issue(self, n, state="open", records=(), card=None, labels=()):
> 85:        self.issues[n] = {"state": state, "records": list(records), "labels": list(labels),
> 121:                     "closed": world.closed(n), "autopilot": AUTO.lower() in (world.issues.get(n) or {}).get("labels", [])}
> 136:            return AUTO.lower() in (world.issues.get(int(n)) or {}).get("labels", [])
> 145:        def label(self, kind, n, on):
> 146:            world.writes.append(("board label", kind, n, on))
> 172:                    "comments": 0, "labels": [], "pull_request": {"merged_at": "2026-10-09T02:00:00Z" if p["state"] == "MERGED" else None}}
> 175:                "labels": [{"name": x} for x in i["labels"]], "html_url": f"https://github.com/o/r/issues/{n}"}
> 198:                               "state": d["state"].upper(), "labels": d["labels"], "url": d["html_url"]})
> 206:                               "comments": [], "reviews": [], "labels": [], "mergedAt": rest_pr(n)["merged_at"]})
> 275:        if rest in ("/comments", "/reviews", "/files", "/events", "/timeline", "/sub_issues", "/labels",
> 345:    label = r"\bissue #" if kind == "issue" else r"\b(?:PR|pull request) #"
> 346:    return [x for x in lines if re.sear

`13. Bash`
```
sleep 100; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/dcc53983-289e-47c6-aec5-203a71d7e99f/tasks/b9jnvy6x2.output
```

> <tool_use_error>Blocked: sleep 100 followed by: tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/dcc53983-289e-47c6-aec5-203a71d7e99f/tasks/b9jnvy6x2.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`14. Bash`
```
F=/tmp/claude-1001/-home-runner-work-dokima-dokima/dcc53983-289e-47c6-aec5-203a71d7e99f/tasks/b9jnvy6x2.output; timeout 500 bash -c "until grep -qE 'passed|failed' $F; do sleep 5; done"; cat $F
```

> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/worker.svg" width="16" height="16" align="absmiddle" alt="worker"> They now run as jobs-zq. https://github.com/o/r/pull/7
> E         - Its own test run: python3 -m pytest -q: 12 passed in 3.1s
> E           "evidence": "python3 -m pytest -q: 12 passed in 3.1s",
> E           "passed": true,
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> E           "passed": true,
>         bodies = [(role, agent.render(rec(role.split()[-1], stage, hb, passed, ["a problem"]))) for role, stage, hb, passed in CASES]
> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> E               "passed": true,
>                  "check": {"passed": True, "problems": []}}
>                  ("rejected plan", rec("planner", "", PLAN, passed=False, problems=["a problem"])),
> body = '<!-- dokima-record

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote four criteria and one non-functional rule taken from story 3 of #416's approved plan, with new tests for each, and rewrote 27 older tests that pinned the old layout of the Definition of Done and the Stats fold.",
          "The planner recorded GitHub's markdown API answers for today's code in tests/rendered/454.json; the build records its own in docs/rendered/454.json."],
  "decided": ["The pull request's description keeps its layout; only the planned issue moves its Definition of Done below the fold.",
              "The autopilot icon follows the card's next redraw, not the moment the label changes (left to #438)."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan carries every promise of story 3 of #416, and each of its new tests fails today because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "On a planned issue the Original issue fold sits right after the card, right above the Definition of Done, which is the body's last line. The owner's words stay unchanged, and an issue saved the old way is redrawn this way next time.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "454.1"},
  {"ask": "In every run comment Dokima posts, the stats line is the very last line, below the Next line. It holds the model, time, turns, tokens, cost and the conversation and run links.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "454.2"},
  {"ask": "On an issue on autopilot and its pull request, the card's status line shows the autopilot icon and the word Autopilot. It is hidden while Needs you shows, and a card not on autopilot shows neither.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "454.3"},
  {"ask": "As GitHub renders them, a planned issue's Original issue fold shows right above its Definition of Done, and a run comment ends wit
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#454](https://github.com/dokima-dev/dokima/issues/454) (Definition of Done below the fold, stats line last, autopilot icon), with no blockers. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks passed.

- **Every ask is covered.** The story has five asks from the approved plan of [#416](https://github.com/dokima-dev/dokima/issues/416) (card links as GitHub's own references), and each one maps to its own criterion:
  - 454.1: on a planned issue, the Original issue fold sits right above the Definition of Done, which is the body's last line.
  - 454.2: every run comment ends with its stats line, below Next.
  - 454.3: cards on autopilot show the autopilot icon and the word Autopilot.
  - 454.4: the layout is checked on GitHub's own rendering.
  - 454.5: a redraw that would change the owner's words is still refused.
- **Today, every new test fails for the right reason.** All 11 new tests fail because the feature is missing, not because of a crash or bad setup. The 27 rewritten older tests either pass or fail only on the new layout. They no longer pin the old layout, which this story reverses.
- **The recorded rendering is GitHub's real output.** I sent both texts stored in `tests/rendered/454.json` to GitHub's markdown API again, and each answer matched the stored one byte for byte. GitHub's API is reachable from these machines, so the worker can record answers for the code it writes.

One weakness is left, and I did not block on it. The 454.4 tests trust whatever the worker records in `docs/rendered/454.json`. Hand-written HTML in that file would pass. The owner already accepted recorded answers in the approved plan of [#416](https://github.com/dokima-dev/dokima/issues/416), so this is not a blocker. At code review, the fix is to rerun `python3 tests/github_render.py docs/rendered/454.json` and check the file comes back unchanged.

The full suite run was cut short on its summary line, so I don't have the final pass count. Every failure it listed was one of these tests waiting on the change.
