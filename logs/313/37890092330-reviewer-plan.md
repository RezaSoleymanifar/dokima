# reviewer (plan) for #313

Run: https://github.com/dokima-dev/dokima/actions/runs/37890092330

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (91.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f8cf0338-abbb-462a-891f-0bc93d0fbffc/tool-results/bx28tr3xh.txt
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
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-planner.json
> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #313](https://github.com/dokima-dev/dokima/issues/313)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #311, #86
> 
> **User story:** On autopilot, every story starts planning the moment it exists, blocked or not, so only building waits for blockers and a stuck story like #311 gets going.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dok

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-card -->/,$p' issue.md | grep -n "dokima-card-end\|^---\|^## \|^### " | head -50; wc -l issue.md
```

> 60:## Comments
> 62:### RezaSoleymanifar on issue #313 (2026-10-09T04:40:02Z)
> 66:### dokima-runtime on issue #313 (2026-10-09T04:40:25Z)
> 70:### dokima-runtime on issue #313 (2026-10-09T04:40:27Z)
> 75:### dokima-runtime on issue #313 (2026-10-09T04:40:39Z)
> 265:### dokima-runtime on issue #313 (2026-10-09T05:11:13Z)
> 412:### RezaSoleymanifar on issue #313 (2026-10-09T05:25:50Z)
> 416:### dokima-runtime on issue #313 (2026-10-09T05:26:48Z)
> 624:### dokima-runtime on issue #313 (2026-10-09T05:40:14Z)
> 780:### dokima-runtime on issue #313 (2026-10-09T05:43:42Z)
> 991:### dokima-runtime on issue #313 (2026-10-09T05:45:20Z)
> 1001 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n '1,80p' issue.md; sed -n '405,420p' issue.md; sed -n '985,1001p' issue.md
```

> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #313](https://github.com/dokima-dev/dokima/issues/313)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #311, #86
> 
> **User story:** On autopilot, every story starts planning the moment it exists, blocked or not, so only building waits for blockers and a stuck story like #311 gets going.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** When a split is filed on autopilot (by `/work`, by autopilot itself or by `/autopilot start`), every story starts planning at once, blocked or not. An unblocked story gets `Autopilot: blockers merged, starting plan` as today; a bl

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['in/04-reviewer-plan.json','in/05-planner.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:9000]); print('=====')
"
```

> [
>  {
>   "id": "B1",
>   "criterion": "313.3",
>   "test": "tests/test_blocked_plans.py::test_a_sub_issue_attached_by_hand_joins_autopilot_and_plans_at_the_next_look",
>   "problem": "The owner asked that a sub-issue attached by hand start planning 'right away'. The plan says that can't be done and changes it to 'at the next look', from a new schedule that runs about 288 times a day for good. That changes how the system works and what it costs, and the owner never chose it. The plan raises it only as a concern, so the owner never decides. On autopilot, approving this plan would start the worker on that choice.",
>   "evidence": "Owner's comment on #313 (2026-10-09T05:25:50Z): 'sub-issues I attach by hand on GitHub. Anything in a tree on autopilot starts planning right away.' plan.json concerns[0] says 'right away' for a hand-attached issue can only mean the next scheduled look. plan.json out_of_scope[0] says it waits 'at most about 5 minutes, later if GitHub runs the schedule late'. The test asserts a cron of '*/5 * * * *' (test_blocked_plans.py, crons() check). .github/workflows/autopilot.yml runs today only on issues: closed.",
>   "fix": "Add a question for the owner with the reading planned for. For example: 'A story you attach by hand can't start the same minute, because GitHub sends no event for it. Is a check every 5 minutes (about 288 short runs a day, sometimes late) fine, or should it wait for the next close or /autopilot start, or something else?' Assume the 5-minute check, an

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
d=json.load(open('plan.json')); print(json.dumps({k:d[k] for k in d if k not in ('test_changes',)},indent=1))
"; sed -n '416,430p;624,640p;780,800p' issue.md
```

> {
>  "kind": "user_story",
>  "summary": "On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.",
>  "user_story": "On autopilot, every story starts planning the moment it is in the tree, blocked or not, whether Dokima filed it or you attached it by hand, so only building waits for blockers and a stuck story like #311 gets going.",
>  "acceptance_criteria": [
>   {
>    "text": "When a split is filed on autopilot (by `/work`, by autopilot itself or by `/autopilot start`), every story starts planning at once, blocked or not. An unblocked story gets `Autopilot: blockers merged, starting plan` as today; a blocked story gets one line naming its open blockers, `Autopilot: starting plan, its worker waits for #A and #B to close`.",
>    "source": "https://github.com/dokima-dev/dokima/issues/313"
>   },
>   {
>    "text": "`/autopilot start` starts planning every issue in the tree that has no sub-issues and nothing started on it, blocked or not, the issue itself included. A blocked one gets the line naming its open blockers, and the comment naming what was switched no longer says the started issues wait on nothing open.",
>    "source": "https://github.com/dokima-dev/dokima/issues/313"
>   },
>   {
>    "text": "Every open story on autopilot that was never started begins planning, blocked or not, with no command. This happens when this merges and #313 closes (so #311 gets going), at every later close, and at autopilot's regular look every 5

**Agent:** Grading the round-3 plan: B1 now looks resolved as a question. Next I'll run the tests to check they fail for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 --stat | head -20; grep -n "^def test" tests/test_blocked_plans.py; timeout 600 python -m pytest -q tests/test_blocked_plans.py 2>&1 | grep -E "^(FAILED|ERROR|PASSED)|passed|failed|Error" | head -30
```

> 253bf7a planner for #313 (run 37888536409)
>  tests/test_blocked_plans.py | 230 +++++++++++++++++++++++++++++++++++++++++++-
>  1 file changed, 228 insertions(+), 2 deletions(-)
> 0fb503c planner for #313 (run 37884977913)
>  tests/test_autopilot_close.py |  56 +++++---
>  tests/test_autopilot_river.py |  11 +-
>  tests/test_autopilot_start.py |  25 ++--
>  tests/test_blocked_plans.py   | 322 ++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 373 insertions(+), 41 deletions(-)
> e1a21e7 Three kinds of raise and one table of who raises to whom, checked by code (#304)
>  dokima/raises.py     | 117 ++++++++++++++++++
>  tests/test_raises.py | 329 +++++++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 446 insertions(+)
> 70:def test_a_split_on_autopilot_starts_planning_every_story_blocked_or_not(record_property, tmp_path):
> 106:def test_autopilot_start_starts_planning_blocked_issues_too(record_property, tmp_path):
> 170:def test_when_this_merges_every_stuck_story_on_autopilot_starts_planning(record_property, tmp_path):
> 232:def test_a_split_on_autopilot_plans_its_blocked_story_and_builds_it_once_the_blocker_closes(record_property, tmp_path):
> 272:def test_a_blocked_story_that_started_planning_never_starts_again(record_property, tmp_path):
> 307:def test_agents_md_says_every_story_on_autopilot_plans_as_soon_as_it_exists(record_property):
> 454:def test_a_sub_issue_attached_by_hand_joins_autopilot_and_plans_at_the_next_look(record_property, tmp_path):
> 497:def test_a_sub_issue_created_und

**Agent:** All nine new tests fail today for the reason they should. Writing the hand-back.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner turned the 5-minute check into a question for the owner, naming its cost: about 288 short runs a day, sometimes late, and a failed check says why only in its run log."],
  "decided": ["It plans on the 5-minute check: autopilot.yml also runs every 5 minutes and whenever an issue opens. The criteria and tests stay as they were."],
  "open": ["Whether a story attached by hand waits for a 5-minute check, for the next close or `/autopilot start`, or something else is the owner's to answer."]},
 "verdict": "approve",
 "summary": "The plan now asks you about the 5-minute check instead of choosing it for you, and every test fails today for the right reason; it waits for your answer on that question.",
 "blockers": [],
 "notes": [
  {"text": "When someone uses GitHub's 'create sub-issue' button, the issue may open before GitHub links it to its parent. The 'opened' look could then miss it, and it would start at the next scheduled look instead. The test assumes the link is there the moment the issue opens.",
   "evidence": "tests/test_blocked_plans.py::test_a_sub_issue_created_under_an_issue_on_autopilot_plans_right_away builds the tree before firing issues: opened."}
 ],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "On autopilot, every story starts planning as soon as it exists, blocked or not: when a split files its stories", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.1"},
  {"ask": "on `/autopilot start`", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.2"},
  {"ask": "and when a story is added to a tree on autopilot", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.3"},
  {"ask": "Only its worker waits for its blockers, as #253 already does.", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.4"},
  {"ask": "Right after t
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan now asks you about the 5-minute check instead of choosing it, and every test fails today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #313, but it still needs your answer on one question before work starts. The review is saved to `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Your question:** a story you attach by hand as a sub-issue can't start planning the same minute, because GitHub sends no event when that happens. The plan assumes autopilot checks every 5 minutes instead. I did not accept that assumption for three reasons:
- It adds a schedule that runs about 288 times a day for good.
- It changes `.github/workflows/autopilot.yml`.
- When a scheduled check fails, it can say why only in its run log, not on an issue.

You asked for "right away" but never chose a schedule, so on autopilot this stops for you. Answer with `/plan` and your choice: the 5-minute check, waiting for the next close or `/autopilot start`, or something else.

**Last round's blocker is resolved:** the planner turned the 5-minute check into this question for you instead of choosing it. It kept the criteria and tests as they were.

**Tests:** I ran the 9 new tests in `tests/test_blocked_plans.py` and all of them fail today for the right reason: the feature isn't there yet, not a crash or a bad path. For example, the blocked story #901 doesn't start planning when its split is filed. Each of your asks in the issue and in your `/plan` reply is covered by a criterion.

**One note, not a blocker:** if you use GitHub's "create sub-issue" button, the issue may open before GitHub links it to its parent. Planning would then start at the next scheduled check rather than immediately. The test assumes the link is already there when the issue opens.
