# reviewer (plan) for #315

Run: https://github.com/dokima-dev/dokima/actions/runs/37887682905

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #315: The PR card is redrawn after merge and shows the true Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #315](https://github.com/dokima-dev/dokima/issues/315)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> PR #312 merged at 04:44, but its card still shows All tests running, Code review blank and Owner approval blank. In truth all tests passed, code review passed the work at 04:32 (its record is on the PR), and I approved and merged it.
> 
> What I want:
> - A card is redrawn whenever anything it shows changes: a check finishing, a review record,

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print({k:v for k,v in d.items() if k!='handback'})"; git show --stat HEAD | head -20; wc -l tests/test_card_redraw.py; cat .github/workflows/card.yml
```

> {'role': 'planner', 'stage': None, 'run_id': '37885551794', 'commit_before': '02a6d8d9ec51e879188d7c8739e6b1e86a7f01b9', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 1591850, 'turns': 39, 'cost_usd': 3.741536, 'tokens_in': 4469726, 'tokens_out': 74018}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/315/37885551794-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/37885551794', 'check': {'passed': True, 'problems': []}}
> commit 0f8ea73117858ccbce71f5de1d603c8c1dc1d4e5
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:14:52 2026 +0000
> 
>     planner for #315 (run 37885551794)
> 
>  tests/test_card_redraw.py | 853 ++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 853 insertions(+)
> 853 tests/test_card_redraw.py
> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, or a person opens or edits an issue. These triggers always use
> # the default branch's copy of this file and of dokima/card.py, so the work being
> # judged cannot change how it is reported.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [completed]
>   issues:
>     types: [opened, edited]
> concurrency:
>   group: card
>   cancel-in-progress: false
> permissions:
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   card:
>     environment: keys
>     # The bot's own ed

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_redraw.py
```

> <persisted-output>
> Output too large (44.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a41cad30-3fbf-46c3-8225-ab280360f58d/tool-results/bbfgoqayi.txt
> 
> Preview (first 2KB):
> """The PR card is redrawn after merge and shows the true Definition of Done (#315).
> 
> These tests run what GitHub runs. An event (a check finishing, an agent's record, the owner's Approve, a merge, a push
> to main) is evaluated against the workflows' own files, .github/workflows/card.yml and agent.yml, with the expression
> evaluator of test_start.py: the trigger must list the event, the job's and the step's `if:` must hold, and the step's
> `${{ }}` env and arguments are filled in. The card code that step runs (`dokima/card.py`, or `-m dokima.card`, with
> the step's arguments) then runs here, in this process, as `card.main()` against a fake GitHub, and the tests read what
> it wrote on the issue and the pull request.
> 
> The fake GitHub is in this file (FakeGitHub). It stands in for `gh` in dokima.card, dokima.agent, dokima.plan and
> dokima.body, and answers what the card reads today:
>     gh issue view N --json ...                      the issue with its comments (agent records among them)
>     gh issue edit N --body-file - (input=...)       writes the issue body
>     gh pr list --head BRANCH --state S --json ...   PRs by head branch; state open, closed, merged or all
>     gh pr view N --json comments,reviews            the PR's comments (records) and reviews
>     gh api graphql 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 30,400p tests/test_card_redraw.py
```

> """
> import copy
> import json
> import os
> import re
> import shlex
> import subprocess
> import sys
> 
> import pytest
> 
> import test_start as ts
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent, body, card, plan  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> REPO = "o/r"
> OWNER = "boss"
> HEAD = "a" * 40          # PR #5's newest commit
> MAIN = "m" * 40          # main's head: the merge commit of the older PR #4
> STATES = {"passed", "failed", "running", "not started"}
> CARD_CODE = re.compile(r"dokima[/.]card(?:\.py)?\b")
> 
> 
> def rec(role, stage=None, n=1, **handback):
>     """One agent record, as dokima.agent.records reads it from a bot comment."""
>     return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
>             "run": f"https://github.com/o/r/actions/runs/{n}"}
> 
> 
> def plan_for(number):
>     """A one-criterion plan for issue `number`."""
>     src = f"https://github.com/o/r/issues/{number}"
>     return {"kind": "user_story", "summary": "Owners see one card.", "user_story": "Owners see one card.",
>             "acceptance_criteria": [{"text": "First thing works.", "source": src}], "non_functional": [],
>             "scope": ["x.py"], "out_of_scope": [], "tests": {f"{number}.1": ["tests/test_a.py::test_one"]},
>             "test_changes": {}, "links": {"blocked_by": [], "blocks": [], "relates_to": []}}
> 
> 
> REVIEW_RUN = "https://github.com/o/r/actions/runs/14"
> 
> 
> def bot(r, at):
>  

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 400,853p tests/test_card_redraw.py
```

> if isinstance(v, str):
>             monkeypatch.setenv(k, v)
>     monkeypatch.setattr(sys, "argv", ["card.py", *args])
>     card.main()
> 
> 
> def card_yml():
>     """card.yml, read."""
>     return ts.workflow("card.yml")
> 
> 
> def redraw_by_card_yml(monkeypatch, g, event_name, event, run_id="1"):
>     """Run card.yml for one event and return the writes it made on the fake GitHub.
> 
>     Returns [] when GitHub would not start it, or no step that runs the card code would run."""
>     wf = card_yml()
>     if not fires(wf, event_name, event):
>         return []
>     steps = card_steps(wf, context(event_name, event, run_id))
>     for step, env, text in steps:
>         args = card_args(text)
>         assert args is not None, f"test setup: cannot read how this card.yml step runs the card code: {text}"
>         run_card(monkeypatch, args, {**env, "GITHUB_EVENT_NAME": event_name})
>     return list(g.writes)
> 
> 
> def workflow_run(name, pr=5, event="pull_request_target", head=HEAD, title=""):
>     """A workflow_run event: workflow `name` completed for PR `pr` (None: for main)."""
>     return {"action": "completed", "sender": {"login": "o", "type": "User"},
>             "workflow": {"name": name},
>             "workflow_run": {"name": name, "event": event, "head_sha": head, "conclusion": "success",
>                              "head_branch": f"try/issue-40" if pr else "main", "display_title": title,
>                              "pull_requests": [{"number": pr, "head": {"sha": head}}] if pr else []}}
> 
> 
> def pr_event(acti

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_redraw.py 2>&1 | grep -E "^(FAILED|E  +[0-9]|E   AssertionError|E   .*315)|passed|failed" | head -40; ls .github/workflows; grep -n "^on:" -A12 .github/workflows/commands.yml 2>/dev/null | head -20
```

> assert done_row(g.prs[5]["body"])[2][0] == "passed", \
>                         "315.1: the card redrawn after the owner's Approve does not show Owner approval passed"
> E       AssertionError: 315.1: the owner approved the PR: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E         315.1: the PR merged: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E         315.1: the code review's record was posted: agent.yml runs no card redraw after it posts the run's record
> _ test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed _
>     def test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed(record_property, monkeypatch,
>         """After the owner merges, both cards say Merged with every Definition of Done item passed.
>         Merged; All tests must link its check; Code review must be passed and link the review's run; Owner approval
>         must be passed and link the PR. The same merge by someone who is not a code owner must not show Owner approval
>         passed. Proves 315.2."""
> E       AssertionError: 315.2: the owner merged PR #5: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the non-functional requirement reads <a href="https://github.com/o/r/actions/runs/9/j

**Agent:** Tests all fail for the right reasons today; now checking whether the queue test lets a bot's own edit drop a waiting redraw of the same issue.

`7. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && python3 - <<'E'
p='.github/workflows/card.yml'
s=open(p).read()
s=s.replace("  group: card\n","  group: card-${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}\n")
open(p,'w').write(s)
E
python3 -m pytest -q tests/test_card_redraw.py -k never_dropped 2>&1 | tail -3
```

> .                                                                        [100%]
> 1 passed, 8 deselected in 0.12s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`8. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["Planned four criteria and one non-functional requirement: redraw both cards on a check, a record, an approval and a merge; show every Definition of Done item passed after the owner merges; link only a criterion's first sentence; redraw stale merged cards once when this lands.",
          "Wrote nine tests in tests/test_card_redraw.py that run the real card.yml and agent.yml against a fake GitHub."],
  "decided": ["Every redraw runs main's copy of the card code, and a waiting redraw is replaced only by a newer redraw of the same issue or pull request.",
              "Stale merged cards are redrawn by the push to main that changes the card code, not on demand or on a schedule."],
  "open": []},
 "verdict": "block",
 "summary": "The plan covers every ask, but the queue test still passes when the card's own edit of an issue cancels a redraw of that same issue waiting its turn, so the owner's 'no redraw is ever dropped' is not fully proven.",
 "blockers": [{"id": "B1", "criterion": "315.5",
   "test": "tests/test_card_redraw.py::test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run",
   "problem": "The test only checks that the bot's edit of issue #40 does not share a group with redraws of other targets (PR #5, #6, #7, issue #41). A card.yml that keys every run on its issue or pull request number puts the bot's edit of #40 in the same queue as the owner's edit of #40, so each card write (which edits the issue) cancels a redraw of that issue still waiting its turn. That is the bug the owner described, and the requirement says a waiting redraw is replaced only by a newer redraw.",
   "evidence": "In a copy of the repo, card.yml's group changed to `card-${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}` makes `pytest -q tests/test_card_redraw.py -k never_dropped` pass (1 pa
```

> Exit code 1
> summary holds 41 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
python3 - <<'E'
import json
p='/tmp/dokima-out/review.json'; d=json.load(open(p))
d['summary']="Every ask is planned, but the queue test still passes when the card's own issue edit cancels a waiting redraw of that same issue."
json.dump(d,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 315 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I've blocked the plan for #315 and sent it back to the planner over one weak test. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What holds up**
- **Every ask is covered.** All seven asks have a criterion: the six in the issue and your follow-up comment asking for a separate redraw queue per issue and pull request.
- **The tests fail for the right reason today.** I ran all nine; each fails because the feature is missing, not because the test is broken:
  - nothing redraws the cards on approval or merge;
  - `agent.yml` doesn't redraw after posting a record;
  - the whole criterion text is linked, not just its first sentence;
  - nothing redraws stale merged cards when the change lands on main;
  - every redraw waits in the one shared `card` queue.

**The blocker (B1, criterion 315.5)**
`test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run` only checks that the card's own edit of issue #40 doesn't share a queue with redraws of *other* issues and pull requests. It never checks it against a waiting redraw of issue #40 itself.

That leaves your bug possible. Every time the card is written, the issue is edited, and that edit starts a run. If queues are named by issue number, that run lands in the same queue as a waiting redraw of the same issue and cancels it.

I confirmed this in a scratch copy of the repo. I set `card.yml`'s queue to `card-<issue or pull request number>`. The test passed, while the bot's edit of #40 and an owner's edit of #40 both landed in queue `card-40`.

**Suggested fix for the planner:** add an owner's edit of issue #40 to the test's events. Then assert that neither the bot's edit of #40 nor a command typed in an issue comment shares that redraw's queue.

**One note, not a blocker:** the approval case only works if `card.yml` listens for the commands workflow finishing. It must not listen for pull request reviews directly, which the plan already rules out.
