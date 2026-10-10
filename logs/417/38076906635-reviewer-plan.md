# reviewer (plan) for #417

Run: https://github.com/dokima-dev/dokima/actions/runs/38076906635

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> Root cause, from the 14:58Z run's log: the step that decides what runs next (`python3 -m dokima.agent next`) failed with "GraphQL: API rate limit already exceeded for installation ID 168252268". The app's GraphQL allowance (5,000 an hour, shared by all of Dokima's workflows) ran out in that hour. agent.yml runs it as `NEXT=$(...) || NEXT=stop`, so the failure became a silent stop: no Next line, no warning, nothing started. Earlier guesses (the raise path from #300) were wrong.
> 
> (Not this bug: #388 stopping on its question for me is by design, and adding the autopilot label alone never starts a planner; /autopilot start does.)
> 
> Done when
> - When deciding what runs next fails, the record says so on the issu

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_next_rate_limit.py; git show --stat HEAD; grep -n "NEXT" .github/workflows/agent.yml | head -30
```

> """Deciding what runs next says why GitHub failed, and waits out its rate limit (#417).
> 
> agent.yml runs `python3 -m dokima.agent next N OUT` as `NEXT=$(...) || NEXT=stop`, so before #417 a GitHub call that
> failed inside it (on 10-10, "GraphQL: API rate limit already exceeded for installation ID ...") became a stop with no
> Next line and no word on the issue. These tests run the same `next` command in-process on a passed planner record,
> whose decision is to start the plan reviewer, against a fake GitHub that stands in for `dokima.agent.gh`:
> 
> - `gh issue view` gives the issue and its comments, `gh pr list` gives no pull requests, and `gh api rate_limit`
>   gives GitHub's rate limit answer (`resources.graphql.reset` and `resources.core.reset`, epoch seconds), the one
>   call GitHub answers even when the limit has run out.
> - A fake clock replaces `time.time`, and `time.sleep` only moves it forward, so a wait of an hour takes no time.
> - Every other call fails, the way gh fails (CalledProcessError with GitHub's words on stderr), while the fake clock
>   is before the reset of the limit that ran out, or always, or never, as each test says.
> 
> What the run decided is what `next` printed (the workflow reads it as NEXT) and the Next line it added to the
> record (OUT/comment.md, which the workflow posts on the issue); OUT/board.txt says whether the card shows Needs you.
> So the fakes reach the code, `next` reads GitHub only through `dokima.agent.gh` and reads the clock and waits only
> through `ti

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_next_rate_limit.py 2>&1 | tail -40; sed -n 355,420p .github/workflows/agent.yml
```

> "kind": "user_story",
>     "summary": "s",
>     "user_story": "u",
>     "acceptance_criteria": [
>      {
>       "text": "a",
>       "source": "https://github.com/o/r/issues/57"
>      }
>     ],
>     "non_functional": [],
>     "scope": [
>      "x.py"
>     ],
>     "out_of_scope": [],
>     "tests": {
>      "57.1": [
>       "tests/test_x.py::test_a"
>      ]
>     }
>    },
>    "check": {
>     "passed": true,
>     "problems": []
>    }
>   }
>   ```
>   
>   </details>
>   
>   <sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · [run](https://github.com/o/r/actions/runs/1)</sub>
>   
> assert []
>  +  where [] = lines_with('<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w... width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · [run](https://github.com/o/r/actions/runs/1)</sub>\n', 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)')
> FAILED tests/test_next_rate_limit.py::test_a_failed_decision_stops_for_the_owner[rate-limit-again] - AssertionError: 417.3: the error escaped the step, so the record has no Next line: GraphQL: API rate limit already exceeded for installation ID 168252268
> assert 'GraphQL: API rate limit already exceeded for installation ID 168252268' is None
> FAILED tests/test_next_rate_limit.py::test_a_failed_decision_stops_for_the_owner[server-error] - AssertionError: 417.3: the error escaped the step, so the

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_next_rate_limit.py 2>&1 | grep -E "^(FAILED|E )" | head -30; grep -n "def cmd_next\|def next_\|\"next\"\|def decide\|board.txt" dokima/agent.py | head
```

> E       AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)', not one (the error escaped the step: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)):
> E         nner planned this issue.
> E         
> E         **User story:** u
> E         
> E         <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> E         
> E         1. a
> E         
> E         <details><summary><b>Scope</b></summary>
> E         
> E         - x.py
> E         
> E         </details>
> E         
> E         <details><summary><b>Tests</b></summary>
> E         
> E         - 57.1: tests/test_x.py::test_a
> E         
> E         </details>
> E         
> E         <details><summary>Full record</summary>
> E         
> E         ```json
> E         {
> E          "role": "planner",
> E          "stage": null,
> E          "run_id": "1",
> E          "run": "https://github.com/o/r/actions/runs/1",
> E          "models": [
> 1842:def next_step(items, rec, owners, rounds=3, autopilot=lambda: False, body="", number="", parent=lambda: None):
> 2026:def next_line(step, owners):
> 2168:    if argv[1] == "next":
> 2253:        open(os.path.join(out, "board.txt"), "w").write(f"{column} {'needs' if needs else 'none'}\n")
> 2275:        if rec.get("role") == "cancelle

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_next_rate_limit.py -rf 2>&1 | grep "^FAILED" | cut -c1-260; sed -n 2160,2260p dokima/agent.py
```

> FAILED tests/test_next_rate_limit.py::test_a_decision_github_refuses_says_so_in_one_line_with_githubs_reason - AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 'HTTP 502: Server Error
> FAILED tests/test_next_rate_limit.py::test_a_rate_limited_decision_waits_for_the_reset_and_starts_the_step[graphql] - AssertionError: 417.2: the rate-limited decision was never tried again; GitHub's error escaped: GraphQL: API rate limit already exceeded for i
> FAILED tests/test_next_rate_limit.py::test_a_rate_limited_decision_waits_for_the_reset_and_starts_the_step[rest] - AssertionError: 417.2: the rate-limited decision was never tried again; GitHub's error escaped: API rate limit exceeded for installation ID 16825
> FAILED tests/test_next_rate_limit.py::test_a_failure_that_is_not_the_rate_limit_does_not_wait - AssertionError: 417.2: the server error was not said on the record:
> FAILED tests/test_next_rate_limit.py::test_a_failed_decision_stops_for_the_owner[rate-limit-again] - AssertionError: 417.3: the error escaped the step, so the record has no Next line: GraphQL: API rate limit already exceeded for installation ID 168252268
> FAILED tests/test_next_rate_limit.py::test_a_failed_decision_stops_for_the_owner[server-error] - AssertionError: 417.3: the error escaped the step, so the record has no Next line: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)
> FAILED tests/test_next_rate_limit.py::test_a_rate_

**Agent:** Tests all fail for the right reason (the error escapes `next`). Now checking whether later GitHub calls in `next` are already caught, to judge if first-call-only tests are enough.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; for f in on_autopilot parent_words record_links automerge file_issues conversation unconfirmed_comment; do echo "== $f"; awk "/^def $f\\(/,/^def [a-z_]+\\(/" dokima/agent.py | grep -n "except\|gh(\|graphql\|return" | head -12; done
```

> == on_autopilot
> == parent_words
> == record_links
> == automerge
> == file_issues
> == conversation
> == unconfirmed_comment

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "^def on_autopilot\|^def parent_words\|^def record_links\|^def automerge\|^def file_issues\|^def conversation\|^def unconfirmed_comment\|^from\|^import" dokima/agent.py | head -30
```

> dokima/agent.py:8:import contextlib
> dokima/agent.py:9:import glob
> dokima/agent.py:10:import json
> dokima/agent.py:11:import os
> dokima/agent.py:12:import re
> dokima/agent.py:13:import shutil
> dokima/agent.py:14:import subprocess
> dokima/agent.py:15:import sys
> dokima/agent.py:16:import time
> dokima/agent.py:18:from dokima import card, raises, words
> dokima/agent.py:19:from dokima.card import field_icon, icon
> dokima/agent.py:47:def conversation(repo, number):
> dokima/agent.py:839:def parent_words(repo, number):
> dokima/agent.py:1299:def file_issues(repo, number, rec, recs):
> dokima/agent.py:1330:def record_links(repo, number, items):
> dokima/agent.py:1613:def on_autopilot(repo, number):
> dokima/agent.py:1730:def automerge(repo, number):
> dokima/agent.py:1751:def unconfirmed_comment(repo, pr, why, mention):

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 47,75p dokima/agent.py; sed -n 839,860p dokima/agent.py; sed -n 1299,1360p dokima/agent.py; sed -n 1613,1630p dokima/agent.py; sed -n 1730,1765p dokima/agent.py
```

> def conversation(repo, number):
>     """The issue and its pull requests as one list of comments, oldest first, each saying where it was written."""
>     d = json.loads(gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,comments"))
>     items = [{**c, "where": f"issue #{number}"} for c in d["comments"]]
>     for pr in linked_prs(repo, number):
>         p = json.loads(gh("pr", "view", str(pr), "-R", repo, "--json", "comments,reviews"))
>         items += [{**c, "where": f"PR #{pr}"} for c in p["comments"]]
>         items += [{"author": r["author"], "body": r["body"], "createdAt": r["submittedAt"], "where": f"PR #{pr} review ({r['state'].lower()})"}
>                   for r in p["reviews"] if r.get("body")]
>         for n in json.loads(gh("api", f"repos/{repo}/pulls/{pr}/comments", "--paginate")):
>             items.append({"author": {"login": n["user"]["login"]}, "body": n["body"], "createdAt": n["created_at"],
>                           "where": f"PR #{pr} line note on {n['path']}:{n.get('line') or n.get('original_line')}"})
>     items.sort(key=lambda c: c["createdAt"])
>     return d, items
> 
> 
> def issue_text(d, items):
>     """The issue as it stands: title, body and every comment, oldest first. A record's JSON is in in/ as its own file,
>     so its comment points there instead of repeating it."""
>     parts, n = [f"# Issue #{d['number']}: {d['title']}", "", d["body"] or "", "", "## Comments"], 0
>     for c in items:
>         b = c["body"] or ""
>         if rs := records([c])

`9. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; grep -n "^UNREAD" dokima/agent.py; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan with two criteria and two requirements, and five tests in tests/test_next_rate_limit.py that run `next` against a fake GitHub and a fake clock."],
  "decided": ["A decision GitHub refuses says GitHub's reason in one line, starts nothing and stops for the owner with Needs you.",
              "A rate-limited decision waits once, to the reported reset of the limit that ran out, then decides again; agent.yml is left as it is."],
  "open": ["Every test has GitHub fail on its first read; none fails a read made later in the decision, such as the autopilot label after a plan review passed."]},
 "verdict": "block",
 "summary": "The tests prove the first GitHub read is waited out and reported, but not the reads `next` makes later on autopilot, which is where the 15:12Z failure after the plan review happened, so a fix that covers only the first read would pass.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Weak test",
   "text": "1.2 promises that a rate-limited step waits for the reset and starts what it would have started, and 1.1 that any refused call says GitHub's reason. Every test uses a passed planner record, whose decision makes one GitHub read (the issue and its comments), and fails every call from the first one. On autopilot, `next` makes more reads after that: the issue's labels (on_autopilot), its blocked-by links (record_links, open_blockers_of) after a plan review passes. Each of these already catches GitHub's error and stops at once: on_autopilot returns None, which becomes the 'cannot say whether on autopilot' stop with no GitHub reason, and record_links returns a stop. So a worker that waits and retries only around the first read passes all five tests, while a rate limit hit on the autopilot read after a plan review, the owner's 15:12Z case, still stops without 
```

> Exit code 1
> 1610:UNREAD = "Autopilot could not be read from GitHub, so nothing starts by itself."
> summary holds 43 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The tests cover only GitHub's first read, not the autopilot reads after a plan review, where the 15:12Z failure happened."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#417](https://github.com/dokima-dev/dokima/issues/417) (autopilot stops silently when GitHub's rate limit runs out) and sent it back to the planner with one blocker. The hand-back passed both checks.

**Why it's blocked:** the tests only cover a failure on GitHub's first read, but the second failure you saw (15:12Z, after the plan review passed) happened on a later read.
- All five new tests fail today for the right reason: GitHub's error escapes `next`.
- Every test has GitHub refuse calls from the very first one, which is the read of the issue and its comments.
- On autopilot, after a plan review passes, `next` makes more reads: the `autopilot` label and the blocked-by links. Those reads already catch GitHub's error and stop at once. They don't wait for the reset, and the label read doesn't give GitHub's reason (`dokima/agent.py:1613` and `dokima/agent.py:1330`).
- So a fix that only waits and retries around the first read would pass every test, and the 15:12Z failure would still happen.

**Fix I asked for:** add a test where the plan review approves the plan on an autopilot issue and GitHub hits the rate limit only on the later read (the label, and in a second case the blocked-by links). It must wait for the reset and start the worker with the `Autopilot: plan approved, starting work` line. A second case has a server error on that later read, and the record must give GitHub's reason.

**Your asks:** I found three in the issue, and the plan's criteria cover all of them, so none is missing:
- Saying the failure in one line with GitHub's reason is criterion 417.1.
- Retrying after the reset and starting the step is 417.2.
- "Never losing a step when it runs out" is also 417.2.

The plan raised no questions for you, and I found no problems outside this issue.
