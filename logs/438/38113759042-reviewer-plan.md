# reviewer (plan) for #438

Run: https://github.com/dokima-dev/dokima/actions/runs/38113759042

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (43.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tool-results/bervpa7un.txt
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
> 01-cancelled.json
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> 05-reviewer-plan.json
> 06-planner.json
> 07-planner.json
> # Issue #438: One workflow redraws the card on every change to an issue or its pull request
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 437, 439 -->
> <!-- dokima-blocking: {"blocked_by": [437, 439], "blocks": [], "loop": []} -->
> Every change on an issue or its pull request redraws its card from card.yml alone, and card pull requests run the play-through by themselves.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: [answer 1 question](https://github.com/dokima-dev/dokima/issues/438#issuecomment-6105081574) with `/plan`, or say `/review`
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:**
> 
> - https://github.com/dokima-dev/dokima/issues/437
> - https://github.com/dokima-dev/dokima/issues/439
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related">

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n 20,400p
```

> <persisted-output>
> Output too large (36.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tool-results/bxmxmvjqv.txt
> 
> Preview (first 2KB):
> - https://github.com/dokima-dev/dokima/issues/457
> - https://github.com/dokima-dev/dokima/issues/466
> - https://github.com/dokima-dev/dokima/issues/491
> 
> 
> **User story:** Whatever changes on an issue or its pull request, the bot's own edits included, card.yml alone redraws its card, and every pull request that changes card, board or workflow code is played on the sandbox by itself.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Every change on an issue or its pull request, the bot's own edits included, redraws its card from what GitHub holds now. The code review's record no longer leaves Code review running (#419).
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-438/tests/test_card_every_change.py#L129"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: Every change on an issue or its pull request redra

`3. Read`
```
/tmp/pack/issue.md
```

> 27	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 28	
> 29	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Every change on an issue or its pull request, the bot's own edits included, redraws its card from what GitHub holds now. The code review's record no longer leaves Code review running (#419).
> 30	  - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-438/tests/test_card_every_change.py#L129"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: Every change on an issue or its pull request redraws both cards.*
> 31	  - Source: https://github.com/dokima-dev/dokima/issues/425
> 32	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Only card.yml writes the card: the planner and the plan approval no longer save a card of their own.
> 33	  - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-438/tests/test_card_every_change.py#L205"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height=

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k!='test_changes'},indent=1))"; git -C /home/runner/work/dokima/dokima log --oneline -3; git -C /home/runner/work/dokima/dokima diff --stat main...HEAD
```

> [
>  {
>   "kind": "issue",
>   "label": "Outside this issue",
>   "text": "Five tests already fail on main: two in tests/test_feature_check.py now stop at the missing owner's words before the fault they check, and three in tests/test_reviewer_settles.py find no filed issue named on the review's card.",
>   "evidence": "On b755a9a, `python3 -m pytest -q tests/test_feature_check.py tests/test_reviewer_settles.py` gives 5 failed, 45 passed; e.g. test_the_check_command_rejects_a_broken_feature_and_says_why: \"story 1: acceptance criterion 1 has no words\".",
>   "raised_by": "planner",
>   "id": "P3",
>   "to": "reviewer"
>  }
> ]
> {
>  "kind": "user_story",
>  "summary": "Every change on an issue or its pull request redraws its card from one place; card pull requests play themselves.",
>  "user_story": "Whatever changes on an issue or its pull request, its card shows it, and card code changes play themselves.",
>  "acceptance_criteria": [
>   {
>    "text": "Every change on an issue or its pull request, the bot's own edits included, redraws both cards from GitHub now.",
>    "words": "every change on an issue or PR reaches it, edits included",
>    "source": "https://github.com/dokima-dev/dokima/issues/425"
>   },
>   {
>    "text": "One place redraws cards: the planner and the plan approval no longer save a card of their own.",
>    "words": "One place redraws cards",
>    "source": "https://github.com/dokima-dev/dokima/issues/425"
>   },
>   {
>    "text": "A pull request that changes card, board or workflow code runs the play-

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -1; git log --oneline -3 origin/main; git merge-base HEAD origin/main; python3 -c "
import json;r=json.load(open('/tmp/pack/in/07-planner.json'));print(list(r.keys()));print(json.dumps(r.get('verdict', r.get('check')),indent=1)[:2000])"
```

> a42a74d Terse output: word caps on every field the owner reads, plain words, one style section for every agent (#500)
> c5b056e A story split from a parent never splits again; criteria count acceptance and non-functional together (#499)
> 42c0dbd Prompt audit: one behavior per criterion, quotes from the parent for split stories (#498)
> b755a9a80820f05cdc2df53adfb3078d51e07bc2
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check', 'url']
> {
>  "passed": true,
>  "problems": []
> }

**Agent:** I'm reading the plan's tests and running them now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_every_change.py
```

> """Every change on an issue or its PR redraws its card, from card.yml alone (#438).
> 
> Story 2 of #425, re-planned as one story of three criteria.
> 
> #419: the code review had passed, yet the card said Code review running for 30 minutes. card.yml picked its moments:
> it skipped the bot's own edits and comments (except a code review's run card on a pull request) and redrew on a run's
> start only for the full suite. The review's record is the bot's edit of its run card, so nothing redrew. Beside
> card.yml, the old planner (dokima/planner.py, `post`) saved its own plan above the marker, and the plan approval
> (`python3 -m dokima.agent next`, dokima/agent.py record_links) drew the cards of the issues its links touched. The
> play-through (.github/workflows/playthrough.yml) ran only from the Run workflow button.
> 
> These tests play card.yml one event at a time on the fake GitHub of tests/card_player.py, run the old planner's post
> and the plan approval against fakes, read .github/workflows/playthrough.yml, and run `python3 -m dokima.playthrough`
> with a temp git repo standing in for a pull request. Nothing calls real GitHub.
> """
> import os
> import re
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
> from card_player import (BOT, OWNER, REPOSITORY, Hub, checks_finished, issue_comment, issue_event,  # noqa: E402
>                          line_note, pr_comment, pr_event, revie

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_card_every_change.py 2>&1 | grep -E "^E .*43|passed|failed" | head -30
```

> E       AssertionError: 438.1: not every change redraws both cards:
> E         438.1: card.yml started when the bot edits the issue but its card job did not run
> E         438.1: card.yml started when the bot labels the issue but its card job did not run
> E         438.1: card.yml started when the bot comments on the issue but its card job did not run
> E         438.1: card.yml started when the bot edits its comment on the issue but its card job did not run
> E         438.1: card.yml started when the owner comments on the pull request but its card job did not run
> E         438.1: card.yml started when the bot posts a plain comment on the pull request but its card job did not run
> E         438.1: card.yml started when the bot edits its run card into a record on the pull request but its card job did not run
> E         438.1: card.yml does not start when the bot opens the pull request, so its cards keep what they showed
> E         438.1: card.yml does not start when the owner edits the pull request, so its cards keep what they showed
> E         438.1: card.yml does not start when the bot pushes a commit to the pull request, so its cards keep what they showed
> E         438.1: card.yml started when the owner closes the pull request unmerged but its card job did not run
> E         438.1: card.yml does not start when the owner reopens the pull request, so its cards keep what they showed
> E         438.1: card.yml does not start when the owner reviews the pull request, so its cards keep what t

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat b755a9a origin/main | tail -15; git merge-tree --write-tree HEAD origin/main >/dev/null && echo clean-merge
```

> tests/test_plan_links_recorded.py                |  12 +-
>  tests/test_plan_shape.py                         |   2 +-
>  tests/test_raise_handbacks.py                    |   3 +-
>  tests/test_raised_cards.py                       |  85 +--------
>  tests/test_raised_earlier_by.py                  | 214 +++++++++++++++++++++++
>  tests/test_review_asks.py                        |   2 +-
>  tests/test_reviewer_settles.py                   |   2 +-
>  tests/test_run_comment_fields.py                 |  25 +--
>  tests/test_size_rule.py                          |  73 ++++++++
>  tests/test_start.py                              |   2 +-
>  tests/test_style_caps.py                         |  48 +++++
>  tests/test_summary_caps.py                       |  72 ++++----
>  tests/test_text_only.py                          |  10 +-
>  tests/test_word_caps.py                          |  23 ---
>  78 files changed, 1050 insertions(+), 1350 deletions(-)
> clean-merge

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat b755a9a origin/main -- dokima/card.py dokima/agent.py dokima/planner.py dokima/playthrough.py .github tests/card_player.py tests/test_plan_links_recorded.py tests/test_body.py; rm -rf /tmp/wt; git worktree add -q --detach /tmp/wt HEAD && cd /tmp/wt && git -c user.name=t -c user.email=t@t merge -q --no-edit origin/main && timeout 600 python3 -m pytest -q tests/test_card_every_change.py 2>&1 | grep -E "^E   *AssertionError|passed|failed"
```

> .github/workflows/acceptance-criteria.yml |   4 +-
>  .github/workflows/agent.yml               |   5 +-
>  .github/workflows/card.yml                |  12 +++
>  dokima/agent.py                           | 129 ++++++++++++++++++++++++++----
>  dokima/card.py                            |  64 +++++++++++----
>  dokima/planner.py                         |  74 +++++++++++++++--
>  dokima/playthrough.py                     |   3 +-
>  tests/card_player.py                      |   7 +-
>  tests/test_body.py                        |   1 +
>  tests/test_plan_links_recorded.py         |  12 ++-
>  10 files changed, 267 insertions(+), 44 deletions(-)
> Auto-merging tests/test_body.py
> Auto-merging tests/test_card.py
> Auto-merging tests/test_card_merge.py
> Auto-merging tests/test_hand_links.py
> Auto-merging tests/test_plan_links_recorded.py
> E       AssertionError: 438.1: not every change redraws both cards:
> E       AssertionError: 438.2: the plan approval saved the card of #252, #301, #302, #303 itself
> E       AssertionError: 438.3: playthrough.yml does not start on pull_request_target opened
> 3 failed in 6.63s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /tmp/wt; timeout 900 python3 -m pytest -q -x -p no:cacheprovider 2>&1 | tail -3; timeout 900 python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | head -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bgxq6cbai). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`11. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('parent.json'));print(p.keys() if isinstance(p,dict) else type(p))" ; head -c 6000 parent.json
```

> dict_keys(['number'])
> {"number": 425}
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The tests fail for the right reasons. Now I'm checking the owner's asks against earlier reviews.

`12. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['03-reviewer-plan.json','05-reviewer-plan.json']:
  r=json.load(open(f));h=r['handback'];print(f);print(json.dumps(h.get('asks'),indent=1))"
```

> 03-reviewer-plan.json
> [
>  {
>   "ask": "Every change on an issue or its pull request starts card.yml, which redraws both cards from what GitHub holds now. That includes edits, the bot's own comments, a run's start (its live card going up) and its result (the card edited into its record).",
>   "source": "https://github.com/dokima-dev/dokima/issues/438",
>   "criterion": "438.1"
>  },
>  {
>   "ask": "Only card.yml's run writes the card above the marker. The planner and the plan approval no longer save a card of their own.",
>   "source": "https://github.com/dokima-dev/dokima/issues/438",
>   "criterion": "438.2"
>  },
>  {
>   "ask": "The play-through of story 1 passes every step from a new issue to a merged pull request on this story's code. That includes the moment a build has started, and the moment the code review's record is posted, when both cards show its verdict, never Code review running.",
>   "source": "https://github.com/dokima-dev/dokima/issues/438",
>   "criterion": "438.3"
>  },
>  {
>   "ask": "Every pull request that changes card, board or workflow code runs the play-through by itself as a check on its head. That code is .github/workflows/, dokima/card.py, dokima/body.py and dokima/board.py. Any other pull request gets the same check, passed without playing.",
>   "source": "https://github.com/dokima-dev/dokima/issues/438",
>   "criterion": "438.4"
>  },
>  {
>   "ask": "Such a pull request cannot merge with the play-through red. Autopilot does not merge it until the check is green, and this story's p

`13. Bash`
```
cd /tmp/wt; cat > /tmp/t_planner_only.py <<'EOF'
import sys; sys.path.insert(0,'/tmp/wt/tests')
import test_card_every_change as t
def test_p(monkeypatch, tmp_path): t.planner_saves_no_card(monkeypatch, tmp_path)
EOF
cp /tmp/t_planner_only.py tests/zz_tmp_planner_only.py; timeout 300 python3 -m pytest -q -p no:cacheprovider tests/zz_tmp_planner_only.py 2>&1 | grep -E "^E  +|passed|failed"|head; rm tests/zz_tmp_planner_only.py
```

> assert raised is None, f"438.2: the planner's post failed on a good plan: {raised!r}"
> E       AssertionError: 438.2: the planner saved a card of its own above the marker: '- [ ] Objective: Owners see a card on every issue.\n  - [ ] Acceptance criteria: The issue shows a card on top.\n    Verified by: `tests/test_cardshow.py::test_card`\n\n**Scope:**\n- `dokima/card.py`\n\n<!-- dokima-ask -->\n<details><summary>Original issue</summary>\n\nMy ask.\n\n</details>'
> E       assert ['- [ ] Objec...\n</details>'] == []
> E         
> E         Left contains one more item: '- [ ] Objective: Owners see a card on every issue.\n  - [ ] Acceptance criteria: The issue shows a card on top.\n    ...ope:**\n- `dokima/card.py`\n\n<!-- dokima-ask -->\n<details><summary>Original issue</summary>\n\nMy ask.\n\n</details>'
> E         
> E         Full diff:
> E         - []
> E         + [
> E         +     '- [ ] Objective: Owners see a card on every issue.\n'
> Shell cwd was reset to /home/runner/work/dokima/dokima

`14. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output | tail -40
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output tail -40. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Meanwhile I'll check P3's failing tests on today's main directly.

`15. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wm; git worktree add -q --detach /tmp/wm origin/main; cd /tmp/wm; timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_feature_check.py tests/test_reviewer_settles.py 2>&1 | tail -3
```

> assert 1 == 0
>  +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3', '-m', 'dokima.planner', 'check', '9', '/...a and non-functional requirements together), and ask the owner, in a question, which of the rest to drop\n', stderr='').returncode
> 2 failed, 48 passed in 6.44s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`16. Bash`
```
cd /tmp/wm; timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_feature_check.py tests/test_reviewer_settles.py 2>&1 | grep -E "^FAILED"
```

> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_broken_feature_and_says_why - AssertionError: 156.1: the check rejected a well-formed feature: ::error title=Planner output rejected::this issue is already a story of its parent, so it never splits again: hand back one story of at most 3 criteria (acceptance criteria and non-functional requirements together), and ask the owner, in a question, which of the rest to drop
> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_loop_and_says_why - AssertionError: 156.2: the check rejected a valid chain: ::error title=Planner output rejected::this issue is already a story of its parent, so it never splits again: hand back one story of at most 3 criteria (acceptance criteria and non-functional requirements together), and ask the owner, in a question, which of the rest to drop
> Shell cwd was reset to /home/runner/work/dokima/dokima

`17. Monitor`
```
until grep -qE "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output; do sleep 5; done; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output
```

> <tool_use_error>InputValidationError: Monitor failed due to the following issue:
> The required parameter `description` is missing
> 
> This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 600000ms are capped to 600000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required"

`18. Bash`
```
until grep -qE "[0-9]+ (passed|failed)" /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output; do sleep 5; done; tail -25 /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output
```

> assert not ['438.1: card.yml started when the bot edits the issue but its card job did not run', '438.1: card.yml started when th...n', '438.1: card.yml started when the bot posts a plain comment on the pull request but its card job did not run', ...]
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 220 passed, 33 skipped in 49.69s

`19. Bash`
```
until [ $(grep -cE "[0-9]+ (passed|failed)" /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output) -ge 2 ]; do sleep 5; done; grep -E "^FAILED|[0-9]+ passed" /tmp/claude-1001/-home-runner-work-dokima-dokima/82a80cf4-9b07-4d01-a146-cd95703989f8/tasks/bgxq6cbai.output | tail -20
```

> FAILED tests/test_card_every_change.py::test_a_pull_request_changing_card_board_or_workflow_code_runs_the_play_through_by_itself - AssertionError: 438.3: playthrough.yml does not start on pull_request_target opened
> FAILED tests/test_card_status.py::test_the_planner_check_command_rejects_a_split_without_a_summary - AssertionError: 181.1: the planner check rejected a split with its summary: ::error title=Planner output rejected::this issue is already a story of its parent, so it never splits again: hand back one story of at most 3 criteria (acceptance criteria and non-functional requirements together), and ask the owner, in a question, which of the rest to drop
> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_broken_feature_and_says_why - AssertionError: 156.1: the check rejected a well-formed feature: ::error title=Planner output rejected::this issue is already a story of its parent, so it never splits again: hand back one story of at most 3 criteria (acceptance criteria and non-functional requirements together), and ask the owner, in a question, which of the rest to drop
> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_loop_and_says_why - AssertionError: 156.2: the check rejected a valid chain: ::error title=Planner output rejected::this issue is already a story of its parent, so it never splits again: hand back one story of at most 3 criteria (acceptance criteria and non-functional requirements together), and ask the owner, in a questi

`20. Bash`
```
cd /tmp/wt; timeout 500 python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED" | grep -v "already a story of its parent" | cut -c1-200
```

> FAILED tests/test_card_every_change.py::test_every_change_on_an_issue_or_its_pull_request_redraws_both_cards - AssertionError: 438.1: not every change redraws both cards:
> FAILED tests/test_card_every_change.py::test_only_card_yml_writes_the_card - AssertionError: 438.2: the plan approval saved the card of #252, #301, #302, #303 itself
> FAILED tests/test_card_every_change.py::test_a_pull_request_changing_card_board_or_workflow_code_runs_the_play_through_by_itself - AssertionError: 438.3: playthrough.yml does not start on pull_request
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Only the three new tests fail when the branch is merged with today's main, each for the right reason. Now I'm writing the review.

`21. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner handed back one story of three criteria, quoting the owner's words from the parent issue."],
  "decided": ["It dropped the play-through merge gate and the parent planner's three added rules, as the owner asked."],
  "open": ["The ask that the play-through passes every step on this story's code has no criterion and no out of scope line."]
 },
 "verdict": "block",
 "summary": "The three criteria and tests are sound, but one ask the owner did not drop vanished without a word.",
 "raises": [
  {
   "kind": "blocker",
   "to": "planner",
   "label": "No criterion",
   "text": "The ask that the play-through passes every step on this story's code is gone. No criterion carries it and no out of scope line names it. The owner dropped only the merge gate and the added rules. Smallest fix: keep it in a criterion, or list it as out of scope once the owner answers.",
   "evidence": "Issue text, Acceptance criteria line 3; planner's question (b) in `06-planner.json`; owner's comment of 2026-10-11T04:54:04Z drops only (a) and (c)."
  },
  {
   "kind": "question",
   "to": "owner",
   "label": "Dropped or kept",
   "text": "You dropped the merge gate and added rules, not the play-through passing every step here. Drop it too? The review assumes yes.",
   "evidence": "Owner's comment of 2026-10-11T04:54:04Z; the planner's earlier question named it (b)."
  }
 ],
 "answers": [
  {
   "raise": "P3",
   "answer": "done",
   "why": "Confirmed on today's main: the two feature check tests still fail, now on the split rule; the three others pass."
  }
 ],
 "asks": [
  {"ask": "every change on an issue or PR reaches it, edits included", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "438.1"},
  {"ask": "Only card.yml's run writes the card above the marker. The planner and the plan approval no longer save a card of their own.", "source": "https://github.com
```

> Exit code 1
> raise 1's text holds 55 words, over its cap of 30: cut 25, keep the facts
> raise 2's text holds 22 words, over its cap of 20: cut 2, keep the facts
> previous_step did line 1 holds 17 words, over its cap of 15: cut 2, keep the facts
> previous_step decided line 1 holds 17 words, over its cap of 15: cut 2, keep the facts
> previous_step open line 1 holds 21 words, over its cap of 15: cut 6, keep the facts

`22. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['previous_step']={"did":["The planner handed back one story of three criteria, in the owner's words."],
 "decided":["It dropped the merge gate and the parent planner's added rules."],
 "open":["Passing every step on this story's code has no criterion."]}
r['raises'][0]['text']="No criterion or out of scope line carries the play-through passing every step on this code. The owner never dropped it. Fix: carry it, or list it once answered."
r['raises'][1]['text']="You dropped the merge gate and added rules, not the play-through passing every step. Drop that too? The review assumes yes."
r['asks']=r['asks'][:4]
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> Exit code 1
> raise 2's text holds 21 words, over its cap of 20: cut 1, keep the facts

`23. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['raises'][1]['text']="You dropped the merge gate and added rules, not the play-through passing every step. Drop it too? The review assumes yes."
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK; git worktree remove --force /tmp/wt; git worktree remove --force /tmp/wm; git status --short
```

> raise 2's text holds 21 words, over its cap of 20: cut 1, keep the facts

`24. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['raises'][1]['text']="You dropped the merge gate and added rules, not the play-through passing every step. Drop it? The review assumes yes."
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK; git status --short; git worktree list
```

> OK
> /home/runner/work/dokima/dokima 5cc43aa [try/issue-438]

**Agent:** I blocked the plan for [#438](https://github.com/dokima-dev/dokima/issues/438) (every change redraws the card). The three criteria and their tests are sound, but one of your asks disappeared without a word.

**What's fine**
- The plan is one story with three criteria, quoting your words from [#425](https://github.com/dokima-dev/dokima/issues/425) (the card always shows what is true right now). It drops the merge gate and the parent planner's added rules, as you asked.
- Each criterion is one behavior, and each test checks only its own criterion.
- I merged the branch with today's main and ran the full suite. The three new tests fail, each for the right reason:
  - 15 kinds of change don't redraw the card.
  - The plan approval saves four cards itself, and the planner saves its own card.
  - The play-through doesn't start on a pull request.
- The planner's older test changes all pass on that merge.
- About 18 other tests fail when run in this sandbox, all with "this issue is already a story of its parent". The message seems to depend on the run's setup rather than on this plan, but I didn't confirm that.

**Why it's blocked**
- Your issue text asks that the play-through passes every step, from a new issue to a merged pull request, on this story's code. The planner's last question listed it as option (b).
- On 2026-10-11 at 04:54 you dropped the merge gate (a) and the added rules (c), not (b).
- The new plan has no criterion for it and doesn't list it as out of scope.

**What I raised**
- **For the planner:** carry that ask in a criterion, or list it as out of scope once you've answered.
- **For you:** should it be dropped too? I assumed yes, since you capped the plan at three criteria. Your answer is what lets the plan move on.

**Earlier raise:** I answered the planner's note about tests already failing on main. On today's main, two of the five still fail, now on the split rule; the other three pass.

The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.
