# reviewer (plan) for #454

Run: https://github.com/dokima-dev/dokima/actions/runs/38086714977

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (48.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/c8e22aec-3ea9-421c-8a8e-f49ff61dac83/tool-results/bhx4cygkt.txt
> 
> Preview (first 2KB):
> # Issue #454: On a planned issue the Original issue fold sits right above the Definition of Done, a run comment ends with its stats line, and the autopilot icon is drawn
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 455, 456 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Planned issues end with their Definition of Done below the fold, run comments end with stats, and autopilot cards show its icon.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/454 · https://github.com/dokima-dev/dokima/pull/461 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/461/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Wrong plan:** Moving a planned issue's Definition of Done below the fold (454.1) breaks the play-through merged in #451: dokima/playthrough.py shown() reads Code review's state only from the card between its markers, so it no longer finds the issue's Definition of Done. dokima/playthrough.py is outside the plan's scope, so the build cannot fix 

`2. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; echo; sed -n 1,400p issue.md | cut -c1-1500
```

> <persisted-output>
> Output too large (37.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/c8e22aec-3ea9-421c-8a8e-f49ff61dac83/tool-results/bc56bseh5.txt
> 
> Preview (first 2KB):
> 01-planner.json
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> []
> # Issue #454: On a planned issue the Original issue fold sits right above the Definition of Done, a run comment ends with its stats line, and the autopilot icon is drawn
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 455, 456 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Planned issues end with their Definition of Done below the fold, run comments end with stats, and autopilot cards show its icon.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/454 · https://github.com/dokima-dev/dokima/pull/461 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/461/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Wrong plan:** Moving a planned issue's Definition of Done below the fold (454.1) breaks the play-through merged in #451: dokima/playthrough.py shown() reads Code review's state only from the card between its markers, so it no longer finds the issue's Def

**Agent:** Let me read the issue body ask and comments without the card noise.

`3. Bash`
```
cd /tmp/pack; grep -n "dokima-ask\|^## \|^### \|Original issue\|^---" issue.md | head -50; wc -l issue.md
```

> 1:# Issue #454: On a planned issue the Original issue fold sits right above the Definition of Done, a run comment ends with its stats line, and the autopilot icon is drawn
> 14:- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Wrong plan:** Moving a planned issue's Definition of Done below the fold (454.1) breaks the play-through merged in #451: dokima/playthrough.py shown() reads Code review's state only from the card between its markers, so it no longer finds the issue's Definition of Done. dokima/playthrough.py is outside the plan's scope, so the build cannot fix it; the scope needs dokima/playthrough.py (card_of or shown should also read the Definition of Done below the Original issue fold, as tests/card_view.py does). · for the planner
> 18:**User story:** The owner reads a planned issue's card, then its Original issue fold, then its Definition of Done last; reads every run comment down to Next with the stats line last; and sees the autopilot icon on every card that is on autopilot.
> 22:- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **<a href="https://github.com/dokima-dev/dokima/actions/runs/38085862722/job/114312129964">Acceptance criterion</a>:** On a planned issue the Original issue fold sits right after the card, right above the Definition of Done, which is the body's l

`4. Bash`
```
cd /tmp/pack; sed -n 63,92p issue.md; sed -n 290,305p issue.md | cut -c1-600; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1)[:12000])"
```

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
> **Context:** `dokima/body.py` `redraw` puts what the card holds after its `<!-- dokima-done -->` marker below the owner's part; `dokima/card.py` `render` uses that only when there is no plan, so a planned issue today has the Definition of Done inside the card, above the marker, and the fold below it. The owner's part must still be kept byte for byte, and a split's story keeps its fold. #394 (folded into #416 by the owner): `FIELD_ICONS` in `dokima/card.py` has an `autopilot` icon (dokima/icons/autopilot.svg) that no code draws; the card's status line shows the stage and Needs you only. The plan's reading: on an issue or PR on autopilot (the `autopilot` label), the status line shows the autopilot icon and the word Autopilot beside the stage, and never while it shows Needs you, as on the board's pills. Stats line (the owner's /plan comment of 2026-10-10T20:04:51Z): today `dokima/agent.py` `render` puts `stats_fold` (a Stats fold) right above 

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['02-reviewer-plan.json','04-reviewer-pr.json']:
  d=json.load(open('in/'+f));h=d.get('handback',d);print(f, json.dumps(h,indent=1)[:5000])
"; git -C /home/runner/work/dokima/dokima diff b703663 a205aaa --stat
```

> 02-reviewer-plan.json {
>  "previous_step": {
>   "did": [
>    "The planner wrote four criteria and one non-functional rule taken from story 3 of #416's approved plan, with new tests for each, and rewrote 27 older tests that pinned the old layout of the Definition of Done and the Stats fold.",
>    "The planner recorded GitHub's markdown API answers for today's code in tests/rendered/454.json; the build records its own in docs/rendered/454.json."
>   ],
>   "decided": [
>    "The pull request's description keeps its layout; only the planned issue moves its Definition of Done below the fold.",
>    "The autopilot icon follows the card's next redraw, not the moment the label changes (left to #438)."
>   ],
>   "open": []
>  },
>  "verdict": "approve",
>  "summary": "The plan carries every promise of story 3 of #416, and each of its new tests fails today because the feature is missing.",
>  "raises": [],
>  "answers": [],
>  "asks": [
>   {
>    "ask": "On a planned issue the Original issue fold sits right after the card, right above the Definition of Done, which is the body's last line. The owner's words stay unchanged, and an issue saved the old way is redrawn this way next time.",
>    "source": "https://github.com/dokima-dev/dokima/issues/416",
>    "criterion": "454.1"
>   },
>   {
>    "ask": "In every run comment Dokima posts, the stats line is the very last line, below the Next line. It holds the model, time, turns, tokens, cost and the conversation and run links.",
>    "source": "https://github.com/dokima-dev/dokim

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff b703663 a205aaa; python3 -m pytest -q tests/test_done_last.py 2>&1 | tail -30; sed -n 1,90p dokima/playthrough.py
```

> diff --git a/tests/test_done_last.py b/tests/test_done_last.py
> index 8735b25..86a8059 100644
> --- a/tests/test_done_last.py
> +++ b/tests/test_done_last.py
> @@ -174,3 +174,60 @@ def test_a_redraw_that_would_change_the_owners_part_is_still_refused(record_prop
>      assert github.saves == [], "454.5: the body was written although the owner's words would change"
>      assert len(github.comments) == 1 and str(refused.value) in (github.comments[0][1] or ""), \
>          f"454.5: the refusal was not said once on the issue: {github.comments}"
> +
> +
> +def icon(alt):
> +    """One card icon, as dokima/card.py draws it, with its alt text."""
> +    return f'<img src="https://example.invalid/{alt}.svg" width="16" height="16" align="absmiddle" alt="{alt}">'
> +
> +
> +def done_line(review):
> +    """A Definition of Done line whose Code review shows `review`."""
> +    return (f"**Definition of Done:** {icon('passed')} All tests · {icon(review)} {icon('code review')} Code review · "
> +            f"{icon('none')} {icon('owner approval')} Owner approval")
> +
> +
> +def review_card(done=""):
> +    """A card at Review, holding `done` as its last line when given, like a PR card."""
> +    return (f"{plan.CARD_START}\n{icon('review')} **Review**\n\n**User story:** Owners see a card.\n\n"
> +            + (done + "\n\n" if done else "") + plan.CARD_END)
> +
> +
> +def planned_issue(review, ask="My ask."):
> +    """A planned issue saved the #454 way, its Definition of Done last below the fold."""
> +    return (review_card() + "\n\n" + b

`7. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; cd /home/runner/work/dokima/dokima; DOKIMA_ALL_TESTS=1 timeout 900 python3 -m pytest -q -x -p no:cacheprovider tests/test_playthrough.py 2>&1 | tail -5
```

> 93:### dokima-runtime on issue #454 (2026-10-10T20:18:27Z)
> 97:### dokima-runtime on issue #454 (2026-10-10T20:18:42Z)
> 149:### dokima-runtime on issue #454 (2026-10-10T20:43:39Z)
> 169:### dokima-runtime on issue #454 (2026-10-10T20:50:45Z)
> 174:### dokima-runtime on issue #454 (2026-10-10T20:50:48Z)
> 206:### dokima-runtime on PR #461 (2026-10-10T20:59:15Z)
> 238:### dokima-runtime on issue #454 (2026-10-10T21:09:51Z)
> 297:### dokima-runtime on issue #454 (2026-10-10T21:12:14Z)
>   
>   - PASS: code review record posted
>   + FAIL: code review record posted: the issue card showed Review, Code review missing
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 2 passed in 0.86s

`8. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/02-reviewer-plan.json'))
prev=prev.get('handback',prev)
r={"previous_step":{"did":["The planner added dokima/playthrough.py to the scope and a new rule, 454.6: the play-through reads Code review's state from a planned issue's Definition of Done below the Original issue fold, never from one quoted in the owner's ask.","The planner added a test for 454.6 that fails today because the play-through finds no Code review state on a planned issue."],"decided":["The four criteria are unchanged, so an approved re-plan goes straight back to the worker."],"open":[]},
"verdict":"approve",
"summary":"The re-plan adds what the code review asked for: the play-through file is in scope and its new test fails today because the play-through cannot see Code review below the fold.",
"raises":[],"answers":[],"asks":prev["asks"]}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 454 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** My summary was too long for the checker, so I'm shortening it and running the checks again.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r["summary"]="The re-plan puts the play-through in scope, and its new test fails today because the play-through cannot see Code review below the fold."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 454 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the re-plan for [#454](https://github.com/dokima-dev/dokima/issues/454) (Definition of Done below the fold, stats line last, autopilot icon). It does what the last code review on [#461](https://github.com/dokima-dev/dokima/pull/461) (this issue's pull request) asked of the planner.

- **What changed:** the planner added `dokima/playthrough.py` to the scope, plus a new rule, 454.6. The play-through must read Code review's state from a planned issue's Definition of Done below the Original issue fold. It must never read a Definition of Done line quoted in the owner's ask.
- **The new test fails today for the right reason.** `tests/test_done_last.py::test_the_play_through_reads_code_review_below_the_fold` gets `review: None` on a planned issue because the play-through can't see Code review. The test checks both passed and running, on the issue card and the PR card. It also checks that a step that should fail does, and that a Definition of Done quoted in the owner's ask isn't read instead of the real one.
- **The play-through fails the same way.** `tests/test_playthrough.py` fails on this branch with "issue card showed Review, Code review missing", which this rule covers.
- **Owner's asks:** the four criteria are unchanged, and each of your asks still maps to one of them. You haven't commented since the last plan review.
- **Nothing raised:** no open raises were sent to me, and I raised none.

Since the criteria didn't change, the plan goes straight back to the worker. The worker still has to fix the other blocker from the code review: writing the Next line crashes when a run has no comment yet.

My `review.json` is in `/tmp/dokima-out` and passes both checks.
