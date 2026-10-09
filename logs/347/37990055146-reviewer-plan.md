# reviewer (plan) for #347

Run: https://github.com/dokima-dev/dokima/actions/runs/37990055146

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 48
> drwxr-xr-x  3 runner runner  4096 Oct  9 20:54 .
> drwxrwxrwt 18 root   root    4096 Oct  9 20:54 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 20:54 in
> -rw-r--r--  1 runner runner 17337 Oct  9 20:54 issue.md
> -rw-r--r--  1 runner runner  1280 Oct  9 20:54 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 20:54 parent.json
> -rw-r--r--  1 runner runner  4380 Oct  9 20:54 plan.json
> 
> in:
> total 24
> drwxr-xr-x 2 runner runner 4096 Oct  9 20:54 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 20:54 ..
> -rw-r--r-- 1 runner runner 4011 Oct  9 20:54 01-planner.json
> -rw-r--r-- 1 runner runner 4076 Oct  9 20:54 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5011 Oct  9 20:54 03-planner.json
> # Issue #347: Every 15 minutes, any card that does not match its issue's state is redrawn
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 344, 345, 346 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> **Backlog**
> 
> [issue #347](https://github.com/dokima-dev/dokima/issues/347)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #344, #345, #346
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="1

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 --stat; git diff HEAD~1 -- tests/test_card_sweep.py; timeout 600 python -m pytest -q tests/test_card_sweep.py 2>&1 | tail -30
```

> tests/test_card_sweep.py | 47 ++++++++++++++++++++++++++++++++++++++++++++---
>  1 file changed, 44 insertions(+), 3 deletions(-)
> diff --git a/tests/test_card_sweep.py b/tests/test_card_sweep.py
> index 14103b7..a12e94e 100644
> --- a/tests/test_card_sweep.py
> +++ b/tests/test_card_sweep.py
> @@ -74,13 +74,15 @@ class SweepHub(Hub):
>          head = open(gh).read().split(FAKE_GH, 1)[0]
>          open(gh, "w").write(head + fake)
>  
> -    def last_sweep(self, at, conclusion="success", event="schedule"):
> -        """Record a finished run of card.yml started at `at`, as GitHub lists it."""
> +    def last_sweep(self, at, conclusion="success", event="schedule", ended=None):
> +        """Record a finished run of card.yml started at `at`, as GitHub lists it.
> +
> +        It ended at `ended` when given, else at `at`."""
>          s = self.load()
>          runs = s.setdefault("runs", {}).setdefault("card.yml", [])
>          runs.append({"id": 1000 + len(runs), "name": "card", "path": ".github/workflows/card.yml", "event": event,
>                       "status": "completed", "conclusion": conclusion, "head_branch": "main",
> -                     "run_started_at": at, "created_at": at, "updated_at": at,
> +                     "run_started_at": at, "created_at": at, "updated_at": ended or at,
>                       "html_url": f"https://github.com/o/r/actions/runs/{1000 + len(runs)}"})
>          self.save()
>  
> @@ -269,6 +271,45 @@ def test_a_failed_sweep_does_not_count_as_the_last_sweep(tmp_path, record_proper
>    

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,140p tests/test_card_sweep.py; cat /tmp/pack/parent.json; cat /tmp/pack/in/03-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:2500])"
```

> """Every 15 minutes, any card that does not match its issue's state is redrawn (#347).
> 
> The scheduled run of card.yml used to redraw only the cards whose blocked-by links changed, so a card whose redraw was
> missed (a dropped event, a merge before the PR card was written) stayed wrong for good. Now the sweep also redraws
> every issue card and PR card that does not show its issue's state now, looking only at the issues and pull requests
> GitHub says were updated since the last sweep that succeeded, so it stays cheap on a large repo. When GitHub cannot
> say what changed, or no sweep has succeeded yet, it rechecks every card instead of none.
> 
> These tests reuse the player and fake GitHub of tests/card_player.py (lifted from #332's tests on branch
> try/issue-332, whose sweep tests these adapt): card.yml is played the way GitHub runs it for the 15-minute schedule,
> running the real `python3 dokima/card.py` against the fake GitHub. The fake is extended here with two things GitHub
> has and the sweep needs:
> - `gh api repos/o/r/actions/workflows/card.yml/runs` (and the repo-wide `repos/o/r/actions/runs`) lists the runs
>   of card.yml the test recorded (newest first), filtered by the `event`, `status` and `branch` query parameters as
>   GitHub filters them (`status` matches a run's status or its conclusion); it can be told to refuse with HTTP 502.
>   Other workflows' runs are answered by the player's fake as before (none).
> - `gh api repos/o/r/issues?since=T` lists only the issues and pull request

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["The planner added two tests to 347.2: one where card.yml runs on an issue event and a comment after the last scheduled sweep, and one where an issue changes while the last sweep is still running.", "It let the fake GitHub record a sweep that ends later than it starts."],
  "decided": ["Only the 15-minute sweep counts as the last sweep; card.yml's runs on issue events, comments and merges do not.", "The sweep counts from when the last sweep that succeeded started, not from when it ended."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves that only the 15-minute sweep counts as the last sweep and that a change made while a sweep runs is not missed; every test fails today for the right reason.",
 "blockers": [],
 "notes": [{"text": "All ten tests in tests/test_card_sweep.py fail today because the feature is missing: stale cards stay stale and the run passes although a card could not be redrawn. None fail on a crash or a missing tool.", "evidence": "python -m pytest -q tests/test_card_sweep.py: 10 failed in 2.82s, each with its own 347.x message"}],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [{"ask": "Every 15 minutes a sweep redraws any issue card or PR card that does not show its issue's state now.", "source": "https://github.com/dokima-dev/dokima/issues/347", "criterion": "347.1"},
          {"ask": "It only looks at issues and PRs updated since the last sweep, so it stays cheap on a large repo.", "source": "https://github.com/dokima-dev/dokima/issues/347", "criterion": "347.2"}]}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 347 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`5. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now proves only the 15-minute sweep counts as the last sweep, and every new test fails today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 347 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #347. The one blocker from last round is fixed, and the review is in `/tmp/dokima-out/review.json`. It passes both hand-back checks.

- **Blocker B1, resolved:** a new test runs a scheduled sweep that succeeds at 05:00 and updates #246 at 06:00. Then card.yml runs successfully for an issue event at 07:00 and a comment at 07:30. The test requires #246's and PR #260's cards to be redrawn anyway. Code that took the newest successful card.yml run of any kind would fail it.
- **Last round's note, also taken up:** a second new test has the last sweep start at 05:00 and end at 05:10, with #246 changed at 05:05. The next sweep must still redraw #246's cards, so it has to count from when the last sweep started, not when it ended.
- **Tests fail today for the right reason:** I ran `pytest -q tests/test_card_sweep.py` and all 10 tests fail with their own 347.x messages. Stale cards stay stale, and a run passes although a card could not be redrawn. None fail on a crash or a missing tool.
- **Both of your asks are covered:** the sweep every 15 minutes is criterion 347.1, and "only looks at issues and PRs updated since the last sweep" is 347.2.

The plan had no questions for you, and I found no problems outside this issue.
