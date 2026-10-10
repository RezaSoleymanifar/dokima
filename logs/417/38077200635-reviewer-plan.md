# reviewer (plan) for #417

Run: https://github.com/dokima-dev/dokima/actions/runs/38077200635

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct 10 18:47 .
> drwxrwxrwt 18 root   root    4096 Oct 10 18:47 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 18:47 in
> -rw-r--r--  1 runner runner 15574 Oct 10 18:47 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 18:47 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 18:47 parent.json
> -rw-r--r--  1 runner runner  3927 Oct 10 18:47 plan.json
> 
> in:
> total 24
> drwxr-xr-x 2 runner runner 4096 Oct 10 18:47 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 18:47 ..
> -rw-r--r-- 1 runner runner 3461 Oct 10 18:47 01-planner.json
> -rw-r--r-- 1 runner runner 3990 Oct 10 18:47 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4554 Oct 10 18:47 03-planner.json
> # Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 368, 425 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/417
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #368, #425
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> On autopilot the next step sometimes never starts, and nothing says so. Twice on 10-10, both on #301, both between 14:32Z and 15:32Z: after the planner's re-plan (14:58Z) and after the plan review passed (15:12Z).
> 
> Root cause, from the 14:58Z run's log: the step that decides what runs next (`python3 -m dokima

`2. Bash`
```
cd /tmp/pack; cat plan.json; cat in/03-planner.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('handback',d).get('answers',d),indent=1)[:3000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_next_rate_limit.py
```

> {
>  "kind": "user_story",
>  "summary": "When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.",
>  "user_story": "On autopilot no step is lost silently: when deciding what runs next fails, the record says why, and when GitHub's rate limit ran out the step waits for it to reset and starts what it would have started.",
>  "acceptance_criteria": [
>   {
>    "text": "When GitHub refuses a call while deciding what runs next, the record says so in one line with GitHub's reason. No stage starts, and runs GitHub answers get no such line.",
>    "source": "https://github.com/dokima-dev/dokima/issues/417"
>   },
>   {
>    "text": "When the refusal is GitHub's rate limit, GraphQL or REST, the step waits until that limit's reported reset, then starts what it would have started. The Next line is the same as a run that never hit the limit, and any other refusal is said at once, with no wait.",
>    "source": "https://github.com/dokima-dev/dokima/issues/417"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "A decision that still fails stops for the owner: the record's one Next line mentions the owner and the card shows Needs you.",
>    "why": "Nothing starts by itself after a failed decision, so only the owner can move the issue on.",
>    "principle": "Fail closed"
>   },
>   {
>    "text": "A run waits for the rate limit at most once. If GitHub still refuses after the reset, the step says so and stops, never retrying in a loop.",
>    "why": "The run's GitH

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_next_rate_limit.py 2>&1 | grep -E "Error|assert|passed|failed" | head -40
```

> GitHub answers every call of the run with "HTTP 502: Server Error". The run's record must then hold exactly one
>         assert escaped is None, f"417.1: deciding what runs next failed though GitHub answered every call: {escaped}"
>         assert printed == "start reviewer plan", f"417.1: with GitHub answering, the run printed {printed!r}, not 'start reviewer plan'"
>         assert text == agent.render(PLANNER) + "\n**Next:** The reviewer starts now.\n", \
> >       assert len(said) == 1, (f"417.1: GitHub refused a call while deciding what runs next, and the record holds "
> E       AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)', not one (the error escaped the step: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)):
> E           "passed": true,
> E       assert 0 == 1
> tests/test_next_rate_limit.py:181: AssertionError
> >       assert escaped is None, f"417.2: the rate-limited decision was never tried again; GitHub's error escaped: {escaped}"
> E       AssertionError: 417.2: the rate-limited decision was never tried again; GitHub's error escaped: GraphQL: API rate limit already exceeded for installation ID 168252268
> E       assert 'GraphQL: API rate limit already exceeded for installation ID 168252268' is None
> tests/test_next_rate_limit.py:201: AssertionError
> >       assert escaped is None, f"417.2: the rate-limited decision 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_next_rate_limit.py 2>&1 | grep -E "^E   +AssertionError|passed|failed" | tail -20
```

> def test_a_failed_decision_stops_for_the_owner(record_property, tmp_path, monkeypatch, capsys, failure):
> E       AssertionError: 417.3: the error escaped the step, so the record has no Next line: GraphQL: API rate limit already exceeded for installation ID 168252268
> ___________ test_a_failed_decision_stops_for_the_owner[server-error] ___________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_failed_decision_stops_f1')
>     def test_a_failed_decision_stops_for_the_owner(record_property, tmp_path, monkeypatch, capsys, failure):
> E       AssertionError: 417.3: the error escaped the step, so the record has no Next line: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)
> E       AssertionError: 417.4: the rate-limited run did not end with a decision: GraphQL: API rate limit already exceeded for installation ID 168252268
> E       AssertionError: 417.2: after GitHub's rate limit on 'api repos/o/r/issues/57' reset, the run printed 'stop', not 'start worker' (it waited 0 s for a reset 300 s away); its Next lines: ['**Next:** @owner-person Autopilot could not be read from GitHub, so nothing starts by itself. The plan is approved. Say `/work` to build it, or `/plan` with changes.']
> E       AssertionError: 417.2: after GitHub's rate limit on 'api repos/o/r/issues/57/dependencies/blocked_by' reset, the run printed 'stop', not 'start worker' (it waited 0 s for a reset 300 s away); its Next lines: ['**Next:** @owner-person GitHub could not list the issues blocking

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["Added two tests where a plan review approves the plan on an issue on autopilot and GitHub refuses a later read: the issue's labels or its blocked-by links.", "Kept the two criteria, the two requirements and the scope (dokima/agent.py and the test file) unchanged."],
  "decided": ["A rate limit on a later read waits for the REST limit's reset and then starts the worker with 'Autopilot: plan approved, starting work'.", "A server error on the labels read puts GitHub's words on the record in one line, starts nothing and does not wait."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves the 15:12Z case too: every new test fails today because the step stops or the error escapes, and each passes only when the step says GitHub's reason or waits for the reset and starts what it would have.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "When deciding what runs next fails, the record says so on the issue in one line, with GitHub's reason, instead of stopping silently.", "source": "https://github.com/dokima-dev/dokima/issues/417", "criterion": "1.1"},
  {"ask": "When the failure is GitHub's rate limit, the step is tried again after the limit resets, and starts what it would have started.", "source": "https://github.com/dokima-dev/dokima/issues/417", "criterion": "1.2"},
  {"ask": "this issue is about never losing a step when it runs out.", "source": "https://github.com/dokima-dev/dokima/issues/417", "criterion": "1.2"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds 42 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> the ask "When deciding what runs next fails, the record says so on the issue in one line, with GitHub's reason, instead of stopping silently." is matched to 1.1, which is not a criterion of the plan (417.1, 417.2, 417.3, 417.4)
> the ask "When the failure is GitHub's rate limit, the step is tried again after the limit resets, and starts what it would have started." is matched to 1.2, which is not a criterion of the plan (417.1, 417.2, 417.3, 417.4)
> the ask "this issue is about never losing a step when it runs out." is matched to 1.2, which is not a criterion of the plan (417.1, 417.2, 417.3, 417.4)

**Agent:** The checker flagged two fixes in my review file: the summary is too long, and I numbered the criteria wrong (the plan calls them 417.1 and 417.2). I'm fixing both now.

`6. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['summary']="The plan now proves the 15:12Z case: every test fails today, and passes only if the step says GitHub's reason or waits and starts."
for a in d['asks']: a['criterion']='417.'+a['criterion'].split('.')[1]
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the revised plan for [#417](https://github.com/dokima-dev/dokima/issues/417) (autopilot stops silently when GitHub refuses a call), and both hand-back checks pass on `/tmp/dokima-out/review.json`.

- **My earlier blocker is fixed.** Last round, every test had GitHub refuse the very first call, so nothing covered the 15:12Z case. The planner added two tests for that case: a plan review passes on an issue on autopilot, and GitHub then refuses a later call that checks the issue's labels or what it is waiting on.
  - When the refusal is the rate limit, the step must wait until the limit resets, then start the worker with "Autopilot: plan approved, starting work".
  - When the refusal is a server error, the record must show GitHub's reason in one line, start nothing and not wait.
- **The tests fail today for the right reason.** I ran all 10 test cases in `tests/test_next_rate_limit.py`; every one fails because the feature is missing. On the later reads, the step either stops at once or never shows GitHub's reason. On the first read, the error escapes the step entirely.
- **Each test also checks the run where GitHub answers.** That run must start the same step and leave no extra line, so a fix that always stops couldn't pass.
- **Nothing the owner asked for is missing.** Both "Done when" lines and "never losing a step when it runs out" each map to a criterion (417.1 or 417.2).

There were no open blockers to answer, and I raised nothing new.
