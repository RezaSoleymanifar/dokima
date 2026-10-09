# reviewer (plan) for #369

Run: https://github.com/dokima-dev/dokima/actions/runs/38002536058

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #369: Bug: a pull request that clashes with main is re-planned on every merge but never rebuilt
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #369](https://github.com/dokima-dev/dokima/issues/369)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> When an open pull request clashes with main and the planner re-plans, the work is rebuilt from the new plan (or the pull request is closed), so the clash is resolved once instead of re-planned on every later merge.
> 
> Seen on 2026-10-09 on #284 / PR #323 (audit): PR #323 clashed with main in AGENTS.md. Each merge to ma

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_clash_once.py tests/test_autopilot_stop_pr.py; git show HEAD -- tests/test_clash.py
```

> commit 001c838514893566ef80baf3f270712d827fa2de
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 23:03:51 2026 +0000
> 
>     planner for #369 (run 38002018950)
> 
>  tests/test_autopilot_stop_pr.py |  30 +++++++
>  tests/test_clash.py             |  32 +++++--
>  tests/test_clash_once.py        | 182 ++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 236 insertions(+), 8 deletions(-)
> """A clash with main is re-planned once, on autopilot only, then rebuilt (#369).
> 
> On 2026-10-09 PR #323 clashed with main, and every later merge sent issue #284 back to its planner again: the re-plan
> passed review but nothing rebuilt the pull request, so the clash stayed and the next merge started the same round.
> These tests hold the owner's rule: a clash starts the planner by itself only on autopilot; off autopilot the issue says
> it needs a re-plan and waits for `/plan`; a clash already sent back and not rebuilt since (no worker record after the
> newest clash record) is not sent back again; and an approved clash re-plan goes to the worker on autopilot, or stops
> for the owner saying `/work` rebuilds the pull request off autopilot.
> 
> `dokima.uptodate.clash(repo, base, sha, pr, rest=..., files=..., owners=...)` is driven with the in-process fake
> GitHub from test_clash.py, which also answers GET repos/o/r/issues/N with the issue's labels (autopilot is the issue's
> own `autopilot` label) or GitHub's refusal. The river is `dokima.agent.next_step`; the ca

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_clash_once.py tests/test_autopilot_stop_pr.py tests/test_clash.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed|AssertionError|Error" | head -40
```

> E       AssertionError: 369.1: off autopilot the clash started a stage: [('dokima-next', {'role': 'planner', 'stage': 'plan', 'issue': '7'})]
> tests/test_clash_once.py:67: AssertionError
> E           AssertionError: 369.2 (re-planned and approved): the next merge sent the clash back again with a new comment on #7
> E             +     '  "passed": true,\n'
> tests/test_clash_once.py:106: AssertionError
> E       AssertionError: 369.3: off autopilot the stop does not say the pull request clashes with main and `/work` rebuilds it: 'The plan is approved. Say `/work` to build it, or `/plan` with changes.'
> tests/test_clash_once.py:153: AssertionError
>         except subprocess.CalledProcessError:
> E       AssertionError: 369.5: with autopilot unreadable the clash started a stage: [('dokima-next', {'role': 'planner', 'stage': 'plan', 'issue': '7'})]
> tests/test_clash_once.py:176: AssertionError
>         assert not m.failed, f"369.4: the listener failed on /autopilot stop:\n{m.tail()}"
> E       AssertionError: 369.4: /autopilot stop on #60 left the autopilot label on it: {50: ['autopilot'], 60: ['autopilot']}
> tests/test_autopilot_stop_pr.py:26: AssertionError
> E       AssertionError: 190.6: the second clash posted again on #7: [(7, '<!-- dokima-record -->\nPull request #70 clashes with `main` since d00dd00 (#301) merged, so the planner re-plans against the new main. The files that clashed:\n\n- `docs/notes.md`\n- `dokima/app.py`\n\n<details><summary>Full record</summary>\n\n```json\n{\n "role": "

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 120,175p .github/workflows/agent.yml; grep -n "def clash" -A80 dokima/uptodate.py | head -140
```

> - name: The card says setting up
>         if: env.CARD_ID != ''
>         env:
>           GH_TOKEN: ${{ steps.setup-key.outputs.token }}
>           SCRUB_CLAUDE: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
>           SCRUB_GITHUB: ${{ github.token }}
>         run: |
>           python3 -m dokima.agent card "$ROLE" "$STAGE" setting-up > /tmp/card.md
>           gh api -X PATCH "repos/$GITHUB_REPOSITORY/issues/comments/$CARD_ID" -F body=@/tmp/card.md --silent \
>             || echo "::warning title=Card not updated::the card could not say setting up"
>           gh api -X DELETE installation/token --silent || echo "::warning title=Key not revoked::the card's key could not be revoked"
>       - name: Starting branch
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: |
>           if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
>             git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
>             # A worker's branch that clashes with main still starts: the merge is committed with its conflict markers,
>             # the clashed files are listed for the fence, and the worker resolves them. Main's changes are in BASE.
>             if [ "$ROLE" = worker ] && ! git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main; then
>               git diff --name-only --diff-filter=U > /tmp/clashed.txt
>               if [ ! -s /tmp/clashed.txt ]; then
>                 echo "Merging main into try/iss

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rln "autopilot stop\|def autopilot\|No issue in" dokima/ .github/workflows/ | head; grep -n "No issue in" -r dokima | head
```

> dokima/board.py
> dokima/agent.py
> .github/workflows/autopilot.yml
> .github/workflows/commands.yml
> dokima/agent.py:1190:        said = f"Autopilot is off for {names}." if switched else f"No issue in #{number}'s tree was on autopilot."

**Agent:** Checking the last thing, how the card reads a clash record, before I write the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 300,335p dokima/card.py; grep -n "updater" dokima/agent.py | head -20
```

> h = planned["handback"] if planned else None
>         return TODO["ready"] if checks_passed(issue["number"], h, found["check_runs"]) else TODO["not every check passed"]
>     return "See the newest record below"
> 
> 
> def status(issue, found):
>     """(stage, to-do): the board's column and, exactly when the board shows Needs you, what the owner must do; None
>     when nothing is theirs. It follows the board's own rule on the newest record, as the river decided it."""
>     from dokima import agent
>     pr = found.get("pr")
>     if pr and pr.get("merged"):
>         return "Merged", None
>     items = found.get("items")
>     if items is None:
>         items = as_items(found["recs"])
>     at = [i for i, c in enumerate(items) if agent.is_record(c)]
>     if not at:
>         return "Backlog", None
>     rec = agent.records([items[at[-1]]])[0]
>     if rec.get("role") == "split":
>         return "Work", None
>     column, needs = agent.board_place(rec, agent.next_step(items[:at[-1]], rec, found.get("owners") or set()))
>     return column, todo(issue, found, rec) if needs else None
> 
> 
> def status_line(repo, stage, todo):
>     """The small status line under the summary: the stage, then Needs you and the owner's to-do when there is one."""
>     head = f"{field_icon(repo, 'merged')} **{stage}**" if stage == "Merged" else f"**{stage}**"
>     return head + (f" · {field_icon(repo, 'needs you')} Needs you: {todo}" if todo else "")
> 
> 
> def child_row(repo, child):
>     """One child of a split: its link, its title and its stage, 

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["Planned four criteria and one non-functional requirement, with five new tests and two changed clash tests.", "Made the shared fake GitHub in the clash tests answer an issue's labels, on autopilot by default."],
  "decided": ["A clash counts as sent back until the worker posts a record after it; until then a later merge posts and starts nothing.", "Off autopilot, an approved clash re-plan stops saying the pull request clashes with main and `/work` rebuilds it; when autopilot cannot be read, a clash starts nothing and says why."],
  "open": ["The plan asks the owner nothing."]},
 "verdict": "approve",
 "summary": "The plan covers all four of the owner's asks, each with a test that runs the clash handler, the river or the command listener and fails today because the change is missing.",
 "blockers": [],
 "notes": [
  {"text": "369.4 is tested only where the issue has no autopilot label. The owner said `/autopilot stop` should 'also' take the label off the pull request, so the worker should make sure the pull request loses its label when the issue has one too.", "evidence": "tests/test_autopilot_stop_pr.py::test_autopilot_stop_on_a_pull_request_takes_the_label_off_it labels only #50 and #60; the reply comes from dokima/agent.py:1190"},
  {"text": "On autopilot, 369.3 already passes today: an approved plan starts the worker. That half guards against a regression, and the off-autopilot half is the part that fails today.", "evidence": "pytest tests/test_clash_once.py: the 369.3 failure is on the second assert, the off-autopilot words"},
  {"text": "Any worker record ends a clash's sent-back state, including a worker run that stopped without resolving the clash. The next merge then handles the clash again, so the repeat is limited to once per worker run.", "evidence": "plan.json criterion 2; .github/workflows/agent.yml 'Starting branch' commits the merge with its conflict markers
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> 1

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers all four of the owner's asks, and each test fails today because the change is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 369 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for [#369](https://github.com/dokima-dev/dokima/issues/369) (a pull request that clashes with main is re-planned on every merge but never rebuilt). The review is saved as `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Your asks and where the plan covers them:**
- **Start the planner only on autopilot (369.1):** off autopilot, the issue says it needs a re-plan and waits for `/plan`.
- **Don't send a clash back twice (369.2):** a clash already sent back to planning is not sent back again by the next merge. It counts as handled again once the worker has run after it.
- **After an approved re-plan (369.3):** on autopilot the worker starts and rebuilds the pull request. Off autopilot the issue stops for you and says `/work` rebuilds it.
- **`/autopilot stop` on a pull request (369.4):** it takes the label off that pull request.
- **Added by the planner (369.5):** when GitHub can't say whether the issue is on autopilot, a clash starts nothing and says why. This follows the "fail closed" principle.

**Tests:** all five new tests and the two changed clash tests fail today because the change is missing, not because of a crash or a bad path. The other 9 tests in those files pass.

**Three notes in the review (none of them block it):**
- **369.4 tests only one case:** the one where the issue itself has no autopilot label. The worker should make sure the pull request loses its label when the issue has one too.
- **Half of 369.3 already works:** on autopilot an approved plan already starts the worker today, so that half only guards against breaking it. The off-autopilot half is what fails today.
- **Any worker run counts:** a worker run that stops without resolving the clash still resets it. A later merge would then send the clash back once more, so it can repeat at most once per worker run.

The plan has no questions for you, and the reviewer found nothing outside this issue to propose.
