# reviewer (plan) for #254

Run: https://github.com/dokima-dev/dokima/actions/runs/37881492739

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (48.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3badedf0-85ae-4797-8fbd-75366dd7da5c/tool-results/b3hbbm97b.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct  9 03:55 .
> drwxrwxrwt 18 root   root    4096 Oct  9 03:55 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 03:55 in
> -rw-r--r--  1 runner runner 44055 Oct  9 03:55 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 03:55 open_blockers.json
> -rw-r--r--  1 runner runner  5423 Oct  9 03:55 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner 4096 Oct  9 03:55 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 03:55 ..
> -rw-r--r-- 1 runner runner 5217 Oct  9 03:55 01-planner.json
> -rw-r--r-- 1 runner runner 4014 Oct  9 03:55 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6068 Oct  9 03:55 03-planner.json
> # Issue #254: A link added or removed by hand on GitHub updates the cards of both issues
> 
> <!-- dokima-card -->
> A blocked-by link someone adds or removes by hand on GitHub shows up on both issues' cards by itself, within 15 minutes.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #254](https://github.com/dokima-dev/dokima/issues/254)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="abs

`2. Bash`
```
cd /tmp/pack; sed -n '/<!-- dokima-card-end\|dokima-ask\|---/,$p' issue.md | head -50; grep -n "^##\|^### \|marker\|Original" issue.md | head -60
```

> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 5</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.
> 
> **Context:** The owner's answer on #231 (19:21): "a link I add or remove by hand on GitHub also updates the cards of both issues, the same as links from an approved plan." GitHub's only native link is blocked-by (read by blocked_by() in dokima/agent.py, REST repos/{repo}/issues/{n}/dependencies/blocked_by and .../blocking); relates-to has no native form, so a hand-made link here is always blocked-by. No workflow today runs when a dependency changes: card.yml runs on issues opened/edited and workflow_run, board.yml on labeled/unlabeled/closed and comments. This story's planner must find which GitHub event (if any) Actions receives when a blocked-by link is added or removed, and otherwise choose the nearest reliable trigger; a new or changed workflow file is part of this story, as the owner asked for the behavior. Story 2 draws the link lines and story 3 draws the other issue's side; this story only adds the trigger and reads hand-made links from GitHub when a card is drawn. The owner's 19:11 comment asks that a contradiction, l

`3. Bash`
```
cd /tmp/pack; sed -n 272,300p issue.md; sed -n 410,430p issue.md; sed -n 600,700p issue.md; cat plan.json; cat open_blockers.json; cat in/02-reviewer-plan.json
```

> ### dokima-runtime on issue #254 (2026-10-09T02:18:23Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer passed the plan.
> 
> **The plan's assumptions:**
> - GitHub Actions gets no event when a blocked-by link changes, so cards would catch up on a schedule: is a delay of up to about 15 minutes fine? Not accepted: It changes how the system works and what it costs: card.yml would run by itself about 96 times a day and read every open issue's links each time, and the owner never said how late a card may catch up; their words only ask that the cards show the change by themselves.
> 
> <details><summary><b>Details</b></summary>
> 
> - The plan covers every ask with tests failing today for the right reason; its 15-minute schedule adds an all-day job, so that choice is yours.
> 
> </details>
> 
> <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/note.svg" width="16" height="16" align="absmiddle" alt="note"> Notes</b></summary>
> 
> - The loop tests check that a card's loop line names at least the issues in the loop, so a line that also named an issue outside the loop would still pass. (tests/test_hand_links.py uses numbers(line) >= {N, 301, 302}; only #303's own card is 

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/03-planner.json'));h=d['handback'];print(json.dumps({k:v for k,v in h.items() if k not in ('acceptance_criteria','non_functional','tests','out_of_scope','scope')},indent=1)); print(d.get('check'))"; cd /home/runner/work/dokima/dokima; git diff --stat main..HEAD; git log --oneline -3; wc -l tests/test_hand_links.py
```

> {
>  "kind": "user_story",
>  "summary": "A blocked-by link added or removed by hand shows on both issues' cards once either issue changes, and within 15 minutes otherwise.",
>  "user_story": "When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.",
>  "test_changes": {},
>  "links": {
>   "blocked_by": [],
>   "blocks": [],
>   "relates_to": [
>    231,
>    253,
>    294
>   ]
>  }
> }
> {'passed': True, 'problems': []}
>  dokima/app.json          |   4 +-
>  dokima/board.py          |  13 +-
>  dokima/manifest.py       | 416 ------------------------------
>  tests/test_app.py        |   3 +-
>  tests/test_hand_links.py | 601 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_manifest.py   | 650 -----------------------------------------------
>  6 files changed, 608 insertions(+), 1079 deletions(-)
> 1cb032a planner for #254 (run 37880667428)
> 70679e1 planner for #254 (run 37872687021)
> bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
> 601 tests/test_hand_links.py

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat bf41093..HEAD; git diff 70679e1..HEAD --stat; cat tests/test_hand_links.py
```

> <persisted-output>
> Output too large (32.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3badedf0-85ae-4797-8fbd-75366dd7da5c/tool-results/b1mafaj0f.txt
> 
> Preview (first 2KB):
>  tests/test_hand_links.py | 601 +++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 601 insertions(+)
>  tests/test_hand_links.py | 252 +++++++++++++++++++++++++++++++++++++++++++----
>  1 file changed, 231 insertions(+), 21 deletions(-)
> """A blocked-by link added or removed by hand shows on both cards (#254).
> 
> Story 5 of #231.
> 
> GitHub Actions has no event for a blocked-by link being added or removed, so, as the owner answered on #254, the cards
> update on every event GitHub does announce on either issue, with a schedule only as a backstop. card.yml runs
> `python3 dokima/card.py` on every issues and issue_comment event a person causes on an issue (ISSUE_NUMBER is that
> issue, GITHUB_EVENT_NAME issues or issue_comment): it redraws that issue's card and the card of every issue it blocks
> or is blocked by, on GitHub now or on its card before, so a link removed by hand leaves the other card too. card.yml
> also runs on a cron (GITHUB_EVENT_NAME=schedule, no ISSUE_NUMBER), and then card.py sweeps every open issue. Both read
> GitHub's own blocked-by links (GET repos/o/r/issues/N/dependencies/blocked_by and .../blocking) and rewrite another
> issue's card only when its blocking links, or loop of issues blocking each other, differ from what its card shows.
> Every redraw dr

**Agent:** I'm reviewing the re-plan for #254 against the owner's answer. Next I'll read the planner's tests and run them.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,200p tests/test_hand_links.py
```

> """A blocked-by link added or removed by hand shows on both cards (#254).
> 
> Story 5 of #231.
> 
> GitHub Actions has no event for a blocked-by link being added or removed, so, as the owner answered on #254, the cards
> update on every event GitHub does announce on either issue, with a schedule only as a backstop. card.yml runs
> `python3 dokima/card.py` on every issues and issue_comment event a person causes on an issue (ISSUE_NUMBER is that
> issue, GITHUB_EVENT_NAME issues or issue_comment): it redraws that issue's card and the card of every issue it blocks
> or is blocked by, on GitHub now or on its card before, so a link removed by hand leaves the other card too. card.yml
> also runs on a cron (GITHUB_EVENT_NAME=schedule, no ISSUE_NUMBER), and then card.py sweeps every open issue. Both read
> GitHub's own blocked-by links (GET repos/o/r/issues/N/dependencies/blocked_by and .../blocking) and rewrite another
> issue's card only when its blocking links, or loop of issues blocking each other, differ from what its card shows.
> Every redraw draws the Blocked by and Blocks lines from GitHub's links read right then.
> 
> Every test runs the real `python3 dokima/card.py` as a subprocess against the fake GitHub of
> tests/test_plan_links_recorded.py (a `gh` first on PATH keeping its state in one JSON file), extended here with two
> things: GitHub failing to list one issue's blocked-by links (state "unreadable": {issue: GitHub's error}), and a
> project board reached through dokima.board.Board's own GraphQL call

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 200,601p tests/test_hand_links.py
```

> assert hub.card_links(301)["blocks"] == set(), f"254.1: #301's card still shows it blocks #252: {hub.card_links(301)}"
>     for n in (N, 301):
>         assert len(hub.comments(n)) == before[n], f"254.1: a comment was posted on #{n} for the removed link"
> 
> 
> def test_a_hand_link_between_two_other_issues_shows_on_their_cards_only(tmp_path, record_property):
>     """A hand link between two other issues shows on their two cards and nowhere else.
> 
>     GitHub gets #303 blocked by #302 by hand. After the scheduled run #303 shows Blocked by #302, #302 shows Blocks
>     #303, and #252's card shows no link. Proves 254.1."""
>     record_property("proves", "254.1")
>     hub = HandHub(tmp_path)
>     hub.set_links({303: [302]})
>     hub.sweep("254.1")
>     assert hub.card_links(303)["blocked_by"] == {302}, f"254.1: #303's card misses #302: {hub.card_links(303)}"
>     assert hub.card_links(302)["blocks"] == {303}, f"254.1: #302's card misses #303: {hub.card_links(302)}"
>     assert hub.card_links(N) == {k: set() for k in LABELS}, f"254.1: #252's card shows a link: {hub.card_links(N)}"
> 
> 
> def test_a_change_on_the_blocked_issue_redraws_the_blocker_right_away(tmp_path, record_property):
>     """A person's change on the blocked issue updates both cards right away, with no schedule.
> 
>     GitHub gets #252 blocked by #301 by hand, then a person changes #252 (an issues event). That one run, with no
>     scheduled run, shows #301 on #252's Blocked by line and #252 on #301's Blocks line, posts no comment, and leaves

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_hand_links.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | head -60; cat .github/workflows/card.yml
```

> f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> E           File "/home/runner/work/dokima/dokima/dokima/card.py", line 557, in <module>
> E             main()
> E           File "/home/runner/work/dokima/dokima/dokima/card.py", line 524, in main
> E             number, pr_number = find_work(repo)
> E                                 ^^^^^^^^^^^^^^^
> E           File "/home/runner/work/dokima/dokima/dokima/card.py", line 384, in find_work
> E             prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
> E                                                                ~~~~~~~~~~^^^^^^^^^^^^
> E           File "<frozen os>", line 714, in __getitem__
> E         KeyError: 'HEAD_SHA'
> E         
> E       assert 1 == 0
> E        +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3', 'dokima/card.py'], returncode=1, stdout=...                     ~~~~~~~~~~^^^^^^^^^^^^\n  File "<frozen os>", line 714, in __getitem__\nKeyError: \'HEAD_SHA\'\n').returncode
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> E           File "/home

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_hand_links.py -rA 2>&1 | grep -E "^(PASSED|FAILED|ERROR)|passed|failed" | cut -c1-260
```

> f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dok

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def redraw\|redraw(\|def draw_card\|card.py\|blocked_by(" dokima/agent.py dokima/board.py dokima/*.py | head -40; grep -n "workflow\|on:" -A0 .github/workflows/*.yml | grep -i "issue_comment\|issues:" 
```

> dokima/agent.py:1126:def blocked_by(repo, number):
> dokima/agent.py:1188:            known[i] = {b["number"]: b["id"] for b in blocked_by(repo, i)}
> dokima/agent.py:1263:        blockers = blocked_by(repo, n)
> dokima/agent.py:1126:def blocked_by(repo, number):
> dokima/agent.py:1188:            known[i] = {b["number"]: b["id"] for b in blocked_by(repo, i)}
> dokima/agent.py:1263:        blockers = blocked_by(repo, n)
> dokima/body.py:42:def redraw(body, top):
> dokima/body.py:62:        new = redraw(current, top)
> dokima/planner.py:436:    return issue_body.redraw(body, plan_text(number, plan, tags, older))

`11. Bash`
```
cd /tmp/pack; grep -n "issuecomment" issue.md | head; sed -n 418,421p issue.md; grep -o '"source": "[^"]*"' in/03-planner.json
```

> ### RezaSoleymanifar on issue #254 (2026-10-09T03:44:38Z)
> 
> /plan Answer: a short delay is fine, but make it trigger-based wherever GitHub announces something (any change on either issue starts the update), with a schedule only as a backstop for what GitHub never announces.
> 
> "source": "https://github.com/dokima-dev/dokima/issues/254"
> "source": "https://github.com/dokima-dev/dokima/issues/254"
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** All 16 new tests fail today, each because the feature is missing. Writing the review now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned after the owner's answer: two acceptance criteria and three non-functional requirements, with 16 tests in tests/test_hand_links.py that run the real card.py against a fake GitHub and read card.yml."],
  "decided": ["card.yml starts on every issue event and comment a person makes on an issue and redraws that issue and every issue it is linked to, with a run every 15 minutes as a backstop.",
              "The bot's own edits and comments, and comments on pull requests, start no card run; a run rewrites another issue's card only when its links or loop changed.",
              "On autopilot, a loop of issues blocking each other gets one comment mentioning the owner and the Needs you pill on each issue in it."],
  "open": []},
 "verdict": "approve",
 "summary": "The new plan does what the owner answered: any change a person makes on either issue updates both cards right away, and a 15-minute run catches the rest; every ask has a test, and all 16 tests fail today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Changes the bot makes on either issue, such as its own comments or labels, do not update the linked issue's card right away. The 15-minute backstop catches them. The plan bases this on the AGENTS.md rule that bots never start anything, and on avoiding a run that restarts itself every time the bot writes a card.",
   "evidence": "plan.json out_of_scope: 'Changes the bot itself makes start no extra card run'; tests/test_hand_links.py::test_card_yml_starts_on_every_change_a_person_makes_and_on_a_schedule asserts a bot comment or bot edit is stopped."},
  {"text": "The requirement says card.yml starts on every issue event, but the test only checks eight named kinds (opened, edited, closed, reopened, labeled, unlabeled, assigned, unassigned), or no type list at all. A card.yml listing just those eight would pass even though
```

> summary holds 44 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now updates both cards on any change a person makes, with a 15-minute backstop; every ask has a test that fails today."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 254 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the new plan for #254. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Why it passes:**
- **It follows your answer.** A blocked-by link added or removed by hand shows on both cards as soon as a person changes either issue. That covers opening, editing, closing, reopening, labelling, assigning and commenting. A run every 15 minutes is only the backstop.
- **Every ask is covered.** That includes your two new asks: update on every change GitHub announces, and use the schedule only as a backstop. Each one maps to a criterion with tests. No ask is missing, and the plan has no open questions.
- **The tests fail for the right reason.** All 16 new tests in `tests/test_hand_links.py` fail today because the feature doesn't exist yet. The scheduled-run tests stop at a missing `HEAD_SHA` in `card.py`, because it has no scheduled mode yet. That is the missing feature, not a broken test.
- **The note from last round is fixed.** The tests now check that a card's loop line names exactly the issues in the loop, not "at least" them.

**Three notes, none blocking:**
1. **Bot changes wait for the backstop.** If the bot comments on or labels one of the two issues, the other issue's card waits for the 15-minute run. The plan bases this on the AGENTS.md rule that bots never start anything. It also avoids a run that restarts itself every time the bot writes a card.
2. **The trigger test is narrower than the promise.** The plan promises card.yml starts on every issue event, but the test only checks eight kinds. A card.yml that lists just those eight would pass while missing others, such as milestoned.
3. **The scheduled-run crash is expected.** Point 3 above covers why the `HEAD_SHA` failure is the missing feature, not a broken test.
