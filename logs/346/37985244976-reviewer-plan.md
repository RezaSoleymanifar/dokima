# reviewer (plan) for #346

Run: https://github.com/dokima-dev/dokima/actions/runs/37985244976

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  9 20:11 .
> drwxrwxrwt 18 root   root   4096 Oct  9 20:11 ..
> drwxr-xr-x  2 runner runner 4096 Oct  9 20:11 in
> -rw-r--r--  1 runner runner 6121 Oct  9 20:11 issue.md
> -rw-r--r--  1 runner runner    2 Oct  9 20:11 open_blockers.json
> -rw-r--r--  1 runner runner   15 Oct  9 20:11 parent.json
> -rw-r--r--  1 runner runner 1871 Oct  9 20:11 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  9 20:11 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 20:11 ..
> -rw-r--r-- 1 runner runner 2483 Oct  9 20:11 01-planner.json
> # Issue #346: One issue's card redraw never cancels another issue's
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 344, 345 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> **Backlog**
> 
> [issue #346](https://github.com/dokima-dev/dokima/issues/346)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #344, #345
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" hei

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/in/01-planner.json; cat /tmp/pack/parent.json; cat .github/workflows/card.yml; cat tests/test_card_queue.py; git branch -a; git show --stat HEAD
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37984295419",
>  "commit_before": "10d9114047aeeb1f235ceea23a9a2b7109b02fe4",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 445441,
>   "turns": 33,
>   "cost_usd": 1.4483419999999998,
>   "tokens_in": 2039725,
>   "tokens_out": 21638
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/346/37984295419-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37984295419",
>  "handback": {
>   "kind": "user_story",
>   "summary": "Card redraws stop sharing one queue, so a redraw for one issue can no longer cancel a redraw for another.",
>   "user_story": "Every issue's card and its pull request's card get each update meant for them, because each issue's redraws wait in a queue of their own.",
>   "acceptance_criteria": [
>    {
>     "text": "Every card redraw about an issue or its pull request waits in that issue's own queue, which keeps the newest waiting redraw and never cancels the running one. This covers the issue changed or commented on, the pull request merged, its checks finishing and the worker finishing; events that draw no card today still draw none.",
>     "source": "https://github.com/dokima-dev/dokima/issues/346"
>    },
>    {
>     "text": "A redraw for one issue never shares a queue with another issue's redraws or with the 15-minute sweep. So a newer redraw never drops it.",
>     "source": "https://github.com/dokima-dev/dokima/issues/346"
>    }
>   ],
>   "non_f

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat main origin/try/issue-332 -- tests | tail -5; git show origin/try/issue-332:tests/test_card_now.py | grep -n "def test_\|queue\|concurren" | head -60; git show origin/try/issue-332:tests/test_hand_links.py | grep -n "def test_\|queue\|concurren" | head -40; diff <(git show origin/try/issue-332:tests/card_player.py) tests/card_player.py && echo SAME
```

> Exit code 1
>  tests/test_needs_you.py                        | 167 +++---
>  tests/test_parent_source.py                    | 403 --------------
>  tests/test_where_specs_go.py                   |  87 ---
>  tests/test_work_column.py                      | 221 --------
>  16 files changed, 676 insertions(+), 1883 deletions(-)
> 6:GitHub as it is, each issue in its own queue.
> 15:- Every concurrency group card.yml declares (the workflow's and each job's that runs) is evaluated for the event.
> 59:# GitHub runs these from the pull request's own copy (its merge ref, or the merge queue's).
> 801:    """The concurrency group a `concurrency:` setting gives, filled in; None when there is none."""
> 833:        self.groups["workflow"] = group_of(wf.get("concurrency"), {**base_ctx, "env": Context()}, {"failed": False})
> 850:            self.groups[name] = group_of(job.get("concurrency"), ctx, status)
> 913:        """The queue each job that wrote a card waited in."""
> 917:        """Every concurrency group this run and its relays took a place in."""
> 950:def test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now(tmp_path, record_property):
> 972:def test_an_event_redraws_an_open_issue_and_its_pr_from_the_records_now(tmp_path, record_property):
> 1010:def test_records_redraw_the_cards_and_the_cards_own_writes_redraw_nothing(tmp_path, record_property):
> 1042:def test_card_yml_starts_on_every_kind_of_event_about_an_issue_or_its_pr(tmp_path, record_property):
> 1104:def test_the_sweep_puts_right_e

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_card_queue.py 2>&1 | tail -30
```

> """One issue's redraw never shares a queue with another issue's or the sweep's.
>     
>         Proves 346.2.     Plays card.yml for every event about #246 or PR #260, every event about #312 or PR #314, and the 15-minute sweep,
>         and collects every concurrency group each run takes a place in (the workflow's and each job's). No group #246's
>         runs take may be one #312's or the sweep's take, and no group #312's runs take may be the sweep's, so a waiting
>         redraw for one is never dropped for a newer redraw of the other. Each issue's own runs still find a queue: a run
>         taking no group at all would let two redraws of one issue run at once."""
>         record_property("proves", "346.2")
>         hub = Hub(tmp_path)
>         places = {}
>         for who, events in ((246, events_about(246, 260)), (312, events_about(312, 314)), ("sweep", {"the sweep": schedule()})):
>             for what, event in events.items():
>                 card, taken, _ = play(hub, event, "346.2")
>                 if who != "sweep":
>                     assert card and None not in card, f"346.2: on {what} for #{who} the redraw waits in no queue"
>                 places.setdefault(who, set()).update(taken)
>         for a, b in ((246, 312), (246, "sweep"), (312, "sweep")):
>             shared = places[a] & places[b]
> >           assert not shared, (f"346.2: redraws for {'#' if a != 'sweep' else ''}{a} and {'#' if b != 'sweep' else ''}{b} "
>                                 f"share the queue {sorted(share

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p tests/card_player.py; grep -n "def \|needs\|outputs\|GITHUB_OUTPUT" tests/card_player.py | head -120
```

> """Plays card.yml as GitHub runs it, one event at a time, against a fake GitHub.
> 
> Lifted from the tests #332's planner wrote on branch try/issue-332 (tests/test_card_now.py), so #346's tests and #332's
> play card.yml the same way. For one event:
> - The event starts the workflow when card.yml's `on:` lists it (and its activity type, and for workflow_run the
>   workflow that finished). Then every job runs in the order its `needs` allow: a job's `if:` and every `${{ }}` are
>   evaluated with tests/test_start.py's evaluator (github, vars, secrets, needs, steps, env); `uses:` steps are skipped
>   (checkout is noted with the ref it would check out, and the app token step gives a fake token); `run:` steps run with
>   bash, from a copy of this repo's dokima/ and .github/, with a fake `gh` first on PATH. Values a step writes to
>   GITHUB_OUTPUT or GITHUB_ENV are read as KEY=value lines, and a job's `outputs:` reach later jobs through `needs`.
> - Every concurrency group card.yml declares (the workflow's and each job's that runs) is evaluated for the event, and
>   kept with its cancel-in-progress setting.
> - An event GitHub runs from the pull request's own copy reaches card.yml through a relay: any workflow card.yml's
>   workflow_run lists by name that starts on the event is played first, then card.yml for the workflow_run it sends.
> 
> The fake GitHub (repo o/r, code owner `boss` through CODEOWNERS, Dokima's bot `dokima-runtime`) keeps its state in one
> JSON file. It holds issue #246 with PR #260 fro

**Agent:** Both new tests fail today for the right reason (every redraw shares the one `card` queue). Now I'm checking that a correct fix can pass them.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 575,660p tests/card_player.py; sed -n 790,950p tests/card_player.py
```

> REPOSITORY = {"full_name": "o/r", "name": "r", "owner": {"login": "o"}, "default_branch": "main"}
> 
> 
> def sender(who):
>     """The sender of an event: the owner, or Dokima's bot."""
>     return {"login": BOT + "[bot]", "type": "Bot"} if who == "bot" else {"login": who, "type": "User"}
> 
> 
> def issue_event(n, action, who=OWNER):
>     """An issues event on issue n."""
>     return "issues", {"action": action, "issue": {"number": n, "title": f"Issue {n}", "state": "open"},
>                       "sender": sender(who), "repository": REPOSITORY}
> 
> 
> def issue_comment(n, who=OWNER, action="created", text="A thought."):
>     """A comment on issue n."""
>     return "issue_comment", {"action": action, "issue": {"number": n, "title": f"Issue {n}"},
>                              "comment": {"body": text, "user": {"login": sender(who)["login"]}},
>                              "sender": sender(who), "repository": REPOSITORY}
> 
> 
> def pr_payload(n, p, merged=False, state="open"):
>     """The pull_request object GitHub puts in a pull request event."""
>     return {"number": p, "title": f"Issue {n}", "state": state, "merged": merged, "body": f"Closes #{n}",
>             "head": {"ref": f"try/issue-{n}", "sha": f"sha{p}"}, "base": {"ref": "main"},
>             "user": {"login": BOT + "[bot]", "type": "Bot"}, "html_url": f"https://github.com/o/r/pull/{p}"}
> 
> 
> def pr_comment(n, p, who=OWNER, action="created", text="A thought."):
>     """A comment on PR p, which GitHub sends as an issue_comment."""
>     return "issue_comm

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "concurrency\|group: card\|\"card\"" tests/*.py | grep -v card_player | grep -iv "test_card_queue" | head -20
```

> tests/test_board_state.py:584:    that step's group output; the job that syncs the board needs that job, takes its concurrency group from that
> tests/test_board_state.py:586:    one. No workflow-wide concurrency group keyed by the event's issue or pull request number is left."""
> tests/test_board_state.py:605:    group = re.search(r"concurrency:\s*\n\s+group:\s*([^\n]+)\n\s+cancel-in-progress:\s*(\w+)", block)
> tests/test_board_state.py:606:    assert group, f"331.4: the sync job {sync!r} has no concurrency group with cancel-in-progress"
> tests/test_board_state.py:608:        f"331.4: the sync job's concurrency group is {group.group(1)!r}, not the queue job's group output"
> tests/test_autopilot_close.py:620:    """The concurrency group a job waits in when issue n closes, and whether a newer run cancels a running one.
> tests/test_autopilot_close.py:626:    levels = [c for c in (wf.get("concurrency"), job.get("concurrency")) if c]
> tests/test_autopilot_close.py:640:    close must wait in one concurrency group shared by the whole repo, which a newer run never cancels. #57 is on
> tests/test_autopilot_close.py:656:            assert group, (f"213.5 (together): {fname}:{name} acts on a close but waits in no concurrency group, so two "
> tests/test_card_merge.py:703:                 "actor": (event.get("sender") or {}).get("login", "github"), "workflow": "card",
> tests/test_card_merge.py:788:    """The concurrency group a `concurrency:` setting gives, filled in; None when there is none."""
> tes

`8. Bash`
```
rm -rf /tmp/proto && cp -r /home/runner/work/dokima/dokima /tmp/proto && cd /tmp/proto && python3 - <<'EOF'
p='.github/workflows/card.yml'
s=open(p).read()
s=s.replace("""concurrency:
  group: card
  cancel-in-progress: false
""","")
s=s.replace("""jobs:
  card:
""","""jobs:
  who:
    runs-on: ubuntu-24.04
    outputs:
      queue: ${{ steps.q.outputs.queue }}
    steps:
      - id: q
        env:
          N: ${{ github.event.issue.number }}
          REF: ${{ github.event.pull_request.head.ref || github.event.workflow_run.head_branch }}
          TITLE: ${{ github.event.workflow_run.display_title }}
          EV: ${{ github.event_name }}
        run: |
          if [ "$EV" = schedule ]; then echo queue=card-sweep >> "$GITHUB_OUTPUT"; exit 0; fi
          if [ -z "$N" ]; then N=$(echo "$REF" | sed -n 's#^try/issue-\\([0-9]*\\)$#\\1#p'); fi
          if [ -z "$N" ]; then N=$(echo "$TITLE" | sed -n 's/.*#\\([0-9]*\\).*/\\1/p'); fi
          echo "queue=card-issue-$N" >> "$GITHUB_OUTPUT"
  card:
    needs: who
    concurrency:
      group: ${{ needs.who.outputs.queue }}
      cancel-in-progress: false
""")
open(p,'w').write(s)
EOF
timeout 900 python -m pytest -q -x tests/test_card_queue.py 2>&1 | tail -8
```

> ..                                                                       [100%]
> 2 passed in 15.79s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`9. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner planned one user story with two criteria: each issue and its pull request get their own queue for card redraws, keeping the newest waiting redraw, and no issue shares that queue with another issue or the 15-minute sweep.",
          "The planner added two tests in tests/test_card_queue.py. They play card.yml against a fake GitHub using the player from #332's tests (tests/card_player.py)."],
  "decided": ["Only .github/workflows/card.yml changes. dokima/card.py stays as it is.",
              "The sweep's own fix (#347), removing old card code (#349) and redrawing on events card.yml ignores today are out of scope."],
  "open": []
 },
 "verdict": "approve",
 "summary": "The plan covers both asks. Both tests fail today because every redraw waits in the one shared 'card' queue, and a per-issue queue written into card.yml passes them.",
 "blockers": [],
 "notes": [
  {"text": "The fix changes a workflow file, card.yml. The issue asks for this, because that file is where the queue is set. On autopilot, though, the pull request will stop for the owner before it merges.",
   "evidence": ".github/workflows/card.yml:19-21 holds the single `concurrency: group: card`. AGENTS.md step 6 says a pull request that changes a workflow file stops for the owner."},
  {"text": "I checked that a correct fix can pass the tests. On a copy of the repo, I added a first job that works out the issue number (from the issue, the pull request's branch or the worker run's title) and a card job that waits in `card-issue-<n>` with cancel-in-progress false. Both tests passed. With the code as it is today, both fail.",
   "evidence": "Today: pytest -q tests/test_card_queue.py -> 2 failed (\"346.1: #246's and #312's redraws wait in the same queue 'card'\"; \"346.2: redraws for #246 and #312 share the queue ['card']\"). With the change on the copy: 2 passed."},
  {"text": "The tests reuse wh
```

> Exit code 1
> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> the ask "Card redraws for an issue and its PR wait in a queue of their own that keeps the newest redraw." is matched to 1, which is not a criterion of the plan (346.1, 346.2)
> the ask "A redraw for one issue never cancels a redraw for another." is matched to 2, which is not a criterion of the plan (346.1, 346.2)

`10. Bash`
```
cd /tmp/dokima-out && python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['summary']="The plan covers both asks, and both tests fail today because every card redraw shares one queue."
r['asks'][0]['criterion']="346.1"; r['asks'][1]['criterion']="346.2"
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 346 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #346. My review is in `/tmp/dokima-out/review.json`, and it passes both hand-back checks.

- **Both asks are covered.** "Card redraws for an issue and its PR wait in a queue of their own that keeps the newest redraw" is criterion 346.1. "A redraw for one issue never cancels a redraw for another" is criterion 346.2. The plan changes only `card.yml` and leaves `card.py` alone, as the owner asked.
- **The tests fail today for the right reason.** I ran `pytest -q tests/test_card_queue.py` and got 2 failed. Both say issues #246 and #312 wait in the same queue, `card`.
- **A correct fix can pass them.** On a throwaway copy of the repo, I gave `card.yml` a first job that works out the issue number. The card job then waits in a queue for that issue and never cancels the running redraw. Both tests passed. The repo itself is unchanged.
- **The tests reuse #332's work, as the owner asked.** They use the test player from #332's branch and split #332's queue test into this issue's two criteria. They also check that events which draw no card today still draw none: the bot's own comments, comments on a pull request, and a pull request closed without merging.

The fix changes a workflow file, `card.yml`. That is what this issue asks for, since the queue is set there. Because of it, the pull request will stop for the owner before it merges, even on autopilot.
