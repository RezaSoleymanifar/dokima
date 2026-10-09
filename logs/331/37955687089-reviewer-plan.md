# reviewer (plan) for #331

Run: https://github.com/dokima-dev/dokima/actions/runs/37955687089

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (53.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/34ba3793-34fb-4d6e-ba1f-71c5b06b90b4/tool-results/b1q4py3xs.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-planner.json
> 03-planner.json
> # Issue #331: The board's column and pills are always computed from the issue's state right now
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 332, 333, 334 -->
> <!-- dokima-blocking: {"blocked_by": [334], "blocks": [333], "loop": []} -->
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Fix the rejected hand-back
> 
> [issue #331](https://github.com/dokima-dev/dokima/issues/331)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #334
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #332
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" heig

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask\|-->$/,$p' issue.md | head -300 | tail -250; echo; cat open_blockers.json
```

> Autopilot: blockers merged, starting plan
> 
> ### dokima-runtime on issue #331 (2026-10-09T06:25:53Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner's run ended with its hand-back rejected by code.
> 
> - ::error title=Planner output rejected::found no plan.json: the planner always hands back a plan, a plan.json of kind user_story or feature, with its questions listed inside it
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37893471328",
>  "commit_before": "e934cfe776d407a74874661164ad0718617dae63",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 798220,
>   "turns": 61,
>   "cost_usd": 4.6820798,
>   "tokens_in": 8261814,
>   "tokens_out": 72568
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/331/37893471328-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37893471328",
>  "handback": {
>   "missing": "plan.json: [Errno 2] No such file or directory: '/tmp/dokima-out/plan.json'"
>  },
>  "check": {
>   "passed": false,
>   "problems": [
>    "::error title=Planner output rejected::found no plan.json: the planner always hands back a plan, a plan.json of kind user_story or feature

`3. Bash`
```
cd /tmp/pack; grep -n "dokima-ask\|^### \|<!-- " issue.md | head -40; cat parent.json | head -c 6000
```

> 3:<!-- dokima-card -->
> 4:<!-- dokima-linked-from: 332, 333, 334 -->
> 5:<!-- dokima-blocking: {"blocked_by": [334], "blocks": [333], "loop": []} -->
> 18:<!-- /dokima-card -->
> 20:<!-- dokima-ask -->
> 23:<!-- dokima-card -->
> 24:<!-- /dokima-card -->
> 51:### dokima-runtime on issue #331 (2026-10-09T06:25:42Z)
> 55:### dokima-runtime on issue #331 (2026-10-09T06:25:53Z)
> 57:<!-- dokima-record -->
> 102:### RezaSoleymanifar on issue #331 (2026-10-09T06:44:34Z)
> 106:### dokima-runtime on issue #331 (2026-10-09T06:44:57Z)
> 108:<!-- dokima-record -->
> 265:### RezaSoleymanifar on issue #331 (2026-10-09T15:27:50Z)
> 269:### dokima-runtime on issue #331 (2026-10-09T15:28:20Z)
> 274:### RezaSoleymanifar on issue #331 (2026-10-09T15:33:13Z)
> 278:### dokima-runtime on issue #331 (2026-10-09T15:33:37Z)
> 280:<!-- dokima-record -->
> 525:### RezaSoleymanifar on issue #331 (2026-10-09T15:42:48Z)
> 529:### dokima-runtime on issue #331 (2026-10-09T15:58:28Z)
> 531:<!-- dokima-live -->
> {"number": 330}
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 18,50p issue.md; sed -n 500,600p issue.md
```

> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #330, story 1</summary>
> 
> **Part of:** #330 Cards and the board always show what is true right now
> 
> **User story:** The owner sees every card on the board in the column and with the pill its issue's state on GitHub says now, whichever events were dropped or late.
> 
> **Context:** Split from #330 by rule R2 (more than five criteria) and R3 (the board in dokima/board.py, the cards in dokima/card.py, each with its own workflow). Today the column is set in three places, each trusting the event that started it: board.decide() maps each event to a column (dokima/board.py, decide, keeps, answered), agent.move_card() sets it after each agent run (dokima/agent.py, board_place and move_card), and card.status() works it out again for the card (dokima/card.py, status). board.sweep() already computes the pill from state on each merge; this story makes one function compute column and pill from state (open or closed, PR merged or not, check results, the agent records via agent.board_place, whether a code owner spoke since via agent.waits_on_owner) and calls it from every event and the 15-minute schedule. board.yml's concurrency group is keyed by the event's issue or PR number, so an issue and its PR run in different queues; GitHub's concurrency keeps only the newest pending run per group, which is the 'keeps the newes

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items()},indent=1))" | head -150; ls in; python3 -c "
import json
for f in ['01','02','03']:
  d=json.load(open(f'in/{f}-planner.json'));print(f,d.get('run_id'),d.get('check',{}).get('passed'))"
```

> {
>  "kind": "user_story",
>  "summary": "The board puts every card in the column and pill its issue's state on GitHub gives now, on every event and every 15 minutes.",
>  "user_story": "The owner sees every card on the board in the column and with the pill its issue's state on GitHub says now, whichever events were dropped or late.",
>  "acceptance_criteria": [
>   {
>    "text": "Any event about an issue or its pull request, and every agent run's end, sets both cards to the column and pill its state gives now. So the next event fixes a dropped or late one. An open issue with no record is in Backlog; otherwise it is in the column the river placed it in after its newest record. Its pill is Needs you while it waits on the owner, else Autopilot on autopilot, else none, and its pull request goes with it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/330"
>   },
>   {
>    "text": "Every 15 minutes a sweep sets every issue and pull request card on the board to its computed column and Action pill.",
>    "source": "https://github.com/dokima-dev/dokima/issues/330"
>   },
>   {
>    "text": "A closed issue, and a merged or closed pull request, sits in Done with no Action pill, whatever its labels.",
>    "source": "https://github.com/dokima-dev/dokima/issues/330"
>   },
>   {
>    "text": "An issue and its pull request share one board queue that keeps the newest recompute, and one issue's run never cancels another issue's.",
>    "source": "https://github.com/dokima-dev/dokima/issues/330"
>   },
>   {
>    "te

**Agent:** Reading the plan done; the owner added a scope comment after the plan was written. Now running the planner's tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python -m pytest -q tests/test_board_state.py 2>&1 | grep -E "FAILED|ERROR|passed|failed" | head -30; grep -n "sweep\|updated\|since" tests/test_board_state.py | head -30
```

> assert done.returncode == 0, f"331.4: `python3 -m dokima.board queue` failed on a {event} event: {done.stderr or done.stdout}"
> FAILED tests/test_board_state.py::test_any_event_puts_both_cards_where_the_issues_state_says - AssertionError: 331.1: after a issues labeled event about #57, the cards are at {'issue #57': ('Work', None), 'pr #60': ('Done', 'Needs you')}, not {'issue #57': ('Review', 'Needs you'), 'pr #60': ('Review', 'Needs you')}
> FAILED tests/test_board_state.py::test_the_next_event_fixes_what_a_dropped_or_late_event_left_wrong - AssertionError: 331.1: the close and merge events were dropped and the next event left the cards at {'issue #57': ('Review', 'Needs you'), 'pr #60': ('Review', 'Needs you')}, not Done with no pill
> FAILED tests/test_board_state.py::test_the_end_of_a_run_places_the_cards_from_state_not_from_the_run - AssertionError: 331.1: #57's approved plan waits for /work, yet the end of its run put it at ('Work', None)
> FAILED tests/test_board_state.py::test_needs_you_and_autopilot_follow_the_history_whichever_event_comes - AssertionError: 331.1: #57 on autopilot goes on, yet its cards show {'issue #57': ('Plan', 'Needs you'), 'pr #60': ('Plan', 'Needs you')}
> FAILED tests/test_board_state.py::test_the_board_runs_on_every_event_about_an_issue_or_its_pull_request - AssertionError: 331.1: board.yml does not run on these events about an issue or its pull request: {'issues': ['edited', 'opened'], 'pull_request_review_comment': ['created']}
> FAILED tests/test_boa

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five criteria and one non-functional requirement for computing every board card's column and pill from the issue's state, with 15 new tests that all fail today for the missing feature.",
          "The planner rewrote 27 older board tests whose per-event rules this story removes, each with a reason."],
  "decided": ["The planner added AGENTS.md to scope so its board lines match #330."],
  "open": ["The planner asks whether #330's words replace AGENTS.md's closed-item and unreadable-card lines, and whether they replace #132's failed-run placement."]},
 "verdict": "block",
 "summary": "The plan misses the owner's later ask that the 15-minute sweep recheck only issues and pull requests updated since the last sweep; its criterion 2 promises the opposite, a sweep over every card.",
 "blockers": [{"id": "B1", "criterion": "331.2", "test": "tests/test_board_state.py::test_the_15_minute_sweep_puts_every_card_where_its_state_says",
   "problem": "The owner added to scope after the plan was written: the 15-minute sweep rechecks only issues and pull requests updated since the last sweep, not every open issue, and an event still rebuilds its own issue right away. No criterion keeps this; criterion 2 says the sweep sets every issue and pull request card on the board, and no test proves an untouched issue is skipped or that an updated one is rechecked.",
   "evidence": "Owner's comment on #331 at 2026-10-09T15:42:48Z: 'Also in scope: the 15-minute sweep rechecks only issues and PRs updated since the last sweep, not every open issue, so it stays cheap on a large repo. An event still rebuilds its own issue right away.' The plan's record was posted at 15:33:37Z, before it. plan.json criterion 2: 'Every 15 minutes a sweep sets every issue and pull request card on the board'.",
   "fix": "Rewrite criterion 2 so the 15-minute sweep rechecks only issues and pull requests 
```

> Exit code 1
> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan misses the owner's later ask that the 15-minute sweep recheck only items updated since the last sweep; criterion 2 sweeps every card."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 331 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #331 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**Blocker (B1, for the planner):** the plan misses something you asked for. At 15:42 you added: "the 15-minute sweep rechecks only issues and PRs updated since the last sweep, not every open issue." The plan was posted at 15:33, before that comment. Its criterion 2 says the opposite: the sweep sets every card on the board. No test checks that an issue nobody touched is skipped. The fix I gave:
- Rewrite criterion 2 so the sweep only rechecks what changed since the last sweep.
- Add three tests: an updated issue gets put right, an untouched one isn't read, and an event still rebuilds its own issue at once.
- If "since the last sweep" can be read two ways, ask you which one you mean.

**Tests:** I ran the planner's 15 new tests in `tests/test_board_state.py` and all of them fail today because the feature doesn't exist yet. None fails from a crash or a bad path.

**Your other asks:** each one in the story text maps to a criterion (331.1 to 331.6).

**The plan's two questions:** I didn't accept either assumption, because each changes how the board works and overrides an earlier decision of yours. Since the issue is on autopilot, both will stop and wait for you:
1. Should AGENTS.md change to match #330? That means a closed item shows no pill even on autopilot, and a card GitHub can't read keeps its place instead of showing Needs you.
2. Should #330's rule replace #132's? Then a failed run that GitHub can't read no longer gets Needs you, and could sit unnoticed until the next sweep.

One note, not a blocker: criterion 1 packs about five promises into one sentence. The tests cover each of them, but splitting the text would make the card easier to read.
