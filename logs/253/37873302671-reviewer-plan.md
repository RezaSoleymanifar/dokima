# reviewer (plan) for #253

Run: https://github.com/dokima-dev/dokima/actions/runs/37873302671

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct  9 02:10 .
> drwxrwxrwt 18 root   root    4096 Oct  9 02:10 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 02:10 in
> -rw-r--r--  1 runner runner 14439 Oct  9 02:10 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 02:10 open_blockers.json
> -rw-r--r--  1 runner runner  4918 Oct  9 02:10 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  9 02:10 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 02:10 ..
> -rw-r--r-- 1 runner runner 5550 Oct  9 02:10 01-planner.json
> # Issue #253: On autopilot, a blocked issue plans but its worker waits until every blocker closes
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 4</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** On autopilot, an issue that is still blocked gets its plan as usual, but its worker starts only when the last issue blocking it closes, by itself.
> 
> **Context:** The owner's answer on #231 (19:11): "On autopilot, a blocked issue still plans, but its worker waits until every blocker closes, then starts by itself." Today an approved plan on autopilot starts its worker at once (next_step() in dokima/agent.py, "Autopilot: plan approved, starting work"), and a close only ever starts planners (autopilot_closed() and start_waiting() in dokima/agent.py, run from autopilot.yml one close at a time). Blockers are GitHub's own blocked-by links (blocked_by()), which st

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_blocked_worker.py; git show HEAD -- tests/test_plan_links_recorded.py
```

> commit 5e856569ce3e415489054c225fe0e2bb6fcd2786
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:10:15 2026 +0000
> 
>     planner for #253 (run 37872681858)
> 
>  tests/test_blocked_worker.py      | 290 ++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_links_recorded.py |  10 +-
>  2 files changed, 298 insertions(+), 2 deletions(-)
> """On autopilot, a blocked issue plans, but its worker waits for every blocker (#253).
> 
> Story 4 of #231. Two moments matter, and each runs the real code against a fake GitHub:
> 
> - The plan review approves. `python3 -m dokima.agent next N OUT` (the step of agent.yml that decides what follows a
>   run) runs on the review's record, on the fake GitHub of test_plan_links_recorded.py (issue #252 there). An issue on
>   autopilot that GitHub still has blocked by an open issue must not start its worker: it gets one line naming the
>   open issues it waits on, and the card's Next line mentions no one.
> - An issue closes. autopilot.yml runs the way GitHub runs it, on the machine of test_autopilot_close.py (issue #57
>   there). When the last open blocker of an issue on autopilot closes, and its newest plan is approved and no worker
>   has started on it, its worker starts once, with one line `Autopilot: blockers closed, starting work`.
> 
> Where GitHub cannot list an issue's blockers, the fake answers that read with "HTTP 502: Server Error" and the worker
> must not start, with the reason on the issue.
> """
> import json
> im

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_blocked_worker.py tests/test_plan_links_recorded.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | head -40
```

> E       AssertionError: 253.1: a blocked plan on autopilot started 'start worker'
> E       assert not True
> E        +  where True = <built-in method startswith of str object at 0x7fdf537c3970>('start')
> E        +    where <built-in method startswith of str object at 0x7fdf537c3970> = 'start worker'.startswith
> E       AssertionError: 253.4: the worker started though GitHub could not list the blockers: 'start worker'
> E       assert not True
> E        +  where True = <built-in method startswith of str object at 0x7fdf537b1e30>('start')
> E        +    where <built-in method startswith of str object at 0x7fdf537b1e30> = 'start worker'.startswith
>         assert not m.failed, f"{crit} ({case}): a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 253.2 (last blocker closed): #57's worker started 0 times, expected once
> E         ## close1-autopilot.yml-closed: Close done parents, switch done trees off, start what the close unblocked (exit 0)
> E         #101 closed: nothing on autopilot to do.
> E         
> E       assert 0 == 1
> E        +  where 0 = workers(<test_autopilot_close.Repo object at 0x7fdf53efeb70>, '253.2')
>         assert not m.failed, f"{crit} ({case}): a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 253.2 (waiting): #57's worker started 0 times, expected once
> E         ## close1-autopilot.yml-closed: Close done parents, switch done trees off, start what the close unblocked (exit 0)
> E         #101 closed: nothing on autopilot to do.
> E       

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_blocked_worker.py tests/test_plan_links_recorded.py 2>&1 | tail -10; git stash list; git diff HEAD~1 --stat
```

> +  where 0 = workers(<test_autopilot_close.Repo object at 0x7fcf85c79e50>, '253.2')
> FAILED tests/test_blocked_worker.py::test_a_close_that_cannot_list_the_blockers_starts_no_worker_and_says_why - AssertionError: 253.4 (readable): #57's worker started 0 times, expected once
>   ## close1-autopilot.yml-closed: Close done parents, switch done trees off, start what the close unblocked (exit 0)
>   #101 closed: nothing on autopilot to do.
>   
> assert 0 == 1
>  +  where 0 = workers(<test_autopilot_close.Repo object at 0x7fcf85c5a570>, '253.4')
> FAILED tests/test_blocked_worker.py::test_agents_md_says_a_blocked_issue_plans_and_its_worker_waits - AssertionError: 253.3: no paragraph of AGENTS.md's The flow says the new rule; the closest misses ['a blocked issue still plans', 'its worker waits until every blocker closes', 'then starts by itself', '`Autopilot: blockers closed, starting work`']
> assert not ['a blocked issue still plans', 'its worker waits until every blocker closes', 'then starts by itself', '`Autopilot: blockers closed, starting work`']
> 7 failed, 18 passed in 22.99s
>  tests/test_blocked_worker.py      | 290 ++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_links_recorded.py |  10 +-
>  2 files changed, 298 insertions(+), 2 deletions(-)

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "issues\"\]\|def __init__\|\"state\"\|def obj\|board.txt" tests/test_plan_links_recorded.py | head -40; grep -n "board.txt" dokima/agent.py | head; grep -n "def start_waiting\|def autopilot_closed\|def blocked_by\|def started_before\|plan approved, starting work" dokima/agent.py
```

> 104:    i = S["issues"].get(str(n))
> 110:def obj(n):
> 113:            "state": i.get("state", "open"), "labels": [{"name": l} for l in i.get("labels", [])],
> 239:        out([obj(int(k)) for k in sorted(S["issues"], key=int)])
> 291:    def __init__(self, tmp, others=(301, 302, 303, 304, 305), deps=None, autopilot=False, fail=()):
> 325:        comments = s["issues"][str(N)]["comments"]
> 332:        comments = s["issues"][str(N)]["comments"]
> 373:        return self.load()["issues"][str(n)]["body"]
> 377:        return self.load()["issues"][str(n)]["comments"]
> 587:    assert open(os.path.join(out, "board.txt")).read().split()[1] == "needs", "252.3: the card is not marked Needs you"
> 614:    hub.state["issues"]["301"]["state"] = "closed"
> 674:    assert open(os.path.join(out, "board.txt")).read().split()[1] == "needs", "252.5: the card is not marked Needs you"
> 686:    s["issues"][str(N)]["labels"] = ["autopilot"]
> 706:    hub.state["issues"]["301"]["state"] = "closed"
> 1789:        open(os.path.join(out, "board.txt"), "w").write(f"{column} {'needs' if needs else 'none'}\n")
> 1798:            column, needs = open(os.path.join(argv[3], "board.txt")).read().split()
> 1126:def blocked_by(repo, number):
> 1235:def started_before(repo, number):
> 1256:def start_waiting(repo, numbers, need_blocker=False, line=AUTOPILOT_LINE):
> 1278:def autopilot_closed(repo):
> 1311:AUTOPILOT_LINES = {"worker": "Autopilot: plan approved, starting work", "split": "Autopilot: split approved, filing its stories"}

**Agent:** Round one of the plan review: all 7 new tests fail today for the right reason. Now checking how a close starts work today, to judge the close tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1126,1150p dokima/agent.py; sed -n 1230,1310p dokima/agent.py; grep -n "def planners_started\|def signals\|def close\b\|def close(" tests/test_autopilot_close.py
```

> def blocked_by(repo, number):
>     """The issues blocking this one, from GitHub's native blocked-by links, each with its state."""
>     return json.loads(gh("api", f"repos/{repo}/issues/{number}/dependencies/blocked_by", "--paginate") or "[]")
> 
> 
> def link_edges(number, links):
>     """A plan's blocking links as GitHub's blocked-by links: (the issue blocked, the issue blocking it)."""
>     n = int(number)
>     return {(n, b) for b in links["blocked_by"]} | {(x, n) for x in links["blocks"]}
> 
> 
> def loop_through(add, drop, has):
>     """The issues that would block each other after `add` and `drop`; [] when none.
> 
>     `has(i)` gives what GitHub has issue i blocked by. A new link a blocked by b closes a loop when b is already
>     blocked, directly or through other issues, by a.
>     """
>     def blockers(i):
>         return (set(has(i)) - {b for a, b in drop if a == i}) | {b for a, b in add if a == i}
>     for a, b in add:
>         stack, seen = [[b]], set()
>         while stack:
>             path = stack.pop()
>             if path[-1] == a:
>                 return path
>         except (json.JSONDecodeError, KeyError, TypeError) as e:
>             failed.append(f"The links are recorded, but the card of #{m} could not be redrawn: {e}.")
>     return " ".join(failed) + after if failed else None
> 
> 
> def started_before(repo, number):
>     """True when GitHub's records show something already started on the issue: a record, a live card or an Autopilot
>     line the bot posted there. A planned, running or finishe

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 315,395p tests/test_autopilot_close.py; grep -n "dokima-next\|client_payload" .github/workflows/agent.yml | head
```

> def _effects(self):
>         """Everything a job can change on GitHub, as text: signals, comments, labels and states."""
>         out = []
>         for name in ("dispatches.jsonl", "comments.json", "labels.json", "states.json"):
>             path = f"{self.tmp}/gh/{name}"
>             out.append(open(path).read() if os.path.exists(path) else "")
>         return out
> 
>     def close(self, n):
>         """Issue n closes as completed (its pull request merged); every workflow GitHub starts on that runs.
> 
>         Returns the names of the jobs that ran (were not skipped). Every job that changed something on GitHub (sent a
>         signal, wrote a comment, changed a label or closed an issue) is kept in self.acted as (file, job name, job, workflow)."""
>         self.close_quietly(n)
>         base = self.close_context(n)
>         github = base["github"]
>         open(f"{self.tmp}/event.json", "w").write(json.dumps(github["event"]))
>         ran = []
>         for fname in sorted(os.listdir(WORKFLOWS)):
>             if not fname.endswith((".yml", ".yaml")):
>                 continue
>             wf = ts.load_yaml(open(os.path.join(WORKFLOWS, fname)).read())
>             if not closes_on_issue_close(wf):
>                 continue
>             jobs, results, outputs = wf.get("jobs") or {}, {}, {}
>             while len(results) < len(jobs):
>                 progressed = False
>                 for name, job in jobs.items():
>                     needs = job.get("needs") or []
>                     needs = [needs] if i

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -ln "plan approved, starting work\|AUTOPILOT_LINES\|start worker" tests/*.py; grep -n "deps=" tests/test_autopilot_river.py | head
```

> tests/test_autopilot_river.py
> tests/test_blocked_worker.py
> tests/test_autopilot_start.py
> tests/test_plan_links_recorded.py

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "blocked_by\|dependencies" tests/test_autopilot_river.py tests/test_autopilot_start.py | head -20
```

> tests/test_autopilot_river.py:60:               "handback": {"stories": [{"story": 1, "issue": 901, "title": "First", "id": 9010, "blocked_by": []},
> tests/test_autopilot_river.py:61:                                        {"story": 2, "issue": 902, "title": "Second", "id": 9020, "blocked_by": [1]}]},

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def \|dependencies\|fullmatch\|else:" tests/test_autopilot_river.py | head -60; grep -n "def record_links\|blocked_by(repo" dokima/agent.py
```

> 67:def current_labels():
> 69:label_path = next((x for x in a[1:] if re.fullmatch(r"/?repos/o/r/issues/57(?:/labels)?(?:\?.*)?", x)), None) if a[:1] == ["api"] else None
> 85:    else:
> 93:def fake_gh(labels):
> 105:def run(monkeypatch, tmp, role, stage, comments, labels, **kw):
> 114:    def __init__(self, monkeypatch, tmp, body, comments, labels):
> 149:def starts(m):
> 167:def lines(m, text):
> 172:def autopilot_lines(m):
> 177:def run_records(m):
> 182:def record_body(m, crit):
> 189:def next_of(body):
> 194:def decide(tmp, rec, comments, labels):
> 216:def assert_stops(r, why, crit, case):
> 227:def test_on_autopilot_an_approved_plan_starts_the_worker_with_one_autopilot_line(record_property, tmp_path, monkeypatch):
> 250:def test_autopilot_start_starts_the_worker_on_a_plan_already_waiting_for_work(record_property, tmp_path, monkeypatch):
> 275:def assert_stories_as_work_files_them(m, case):
> 286:def test_on_autopilot_an_approved_split_files_its_stories_with_one_autopilot_line(record_property, tmp_path, monkeypatch):
> 320:def test_off_autopilot_an_approved_plan_or_split_still_stops_for_the_owner(record_property, tmp_path, monkeypatch):
> 341:def test_on_autopilot_the_river_still_stops_where_the_owner_must_decide(record_property, tmp_path, monkeypatch):
> 374:def test_on_autopilot_a_plan_with_questions_goes_to_the_plan_reviewer(record_property, tmp_path):
> 391:def check_review(tmp, review, plan):
> 404:def test_the_plan_reviewer_judges_every_question_against_the_owners_words(record_property, tmp_path):
> 449:def t

`11. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 60,104p tests/test_autopilot_river.py; sed -n 194,250p tests/test_autopilot_river.py
```

> "handback": {"stories": [{"story": 1, "issue": 901, "title": "First", "id": 9010, "blocked_by": []},
>                                         {"story": 2, "issue": 902, "title": "Second", "id": 9020, "blocked_by": [1]}]},
>                "check": {"passed": True, "problems": []}}
> 
> LABEL_GH = r'''
> INITIAL_LABELS = __LABELS__
> LBL_FILE = os.path.join(d, "labels.json")
> def current_labels():
>     return json.load(open(LBL_FILE)) if os.path.exists(LBL_FILE) else INITIAL_LABELS
> label_path = next((x for x in a[1:] if re.fullmatch(r"/?repos/o/r/issues/57(?:/labels)?(?:\?.*)?", x)), None) if a[:1] == ["api"] else None
> reads_labels = (label_path is not None and (flag("-X", "--method") or "GET").upper() == "GET") or \
>     (a[:3] == ["issue", "view", "57"] and "labels" in (flag("--json") or ""))
> if opts.get("fail_labels") and reads_labels:
>     sys.stderr.write("HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)\n")
>     sys.exit(1)
> if a[:1] == ["api"] and any("dispatches" in x for x in a) and "--input" in a:
>     p = flag("--input")
>     open(os.path.join(d, "dispatch-inputs.jsonl"), "a").write(json.dumps(json.load(sys.stdin if p == "-" else open(p))) + "\n")
>     print("{}")
>     sys.exit(0)
> if a[:2] == ["issue", "view"]:
>     n = int(a[2].rstrip("/").rsplit("/", 1)[-1].lstrip("#")) if len(a) > 2 and not a[2].startswith("-") else 57
>     issue = json.load(open(os.path.join(d, "issue.json")))
>     if n == issue["number"]:
>         issue["comments"] = issue["comments"] + comments_on("

**Agent:** Checking whether existing autopilot tests' fake GitHub can answer a blocked-by read, since the new code will need one.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import sys; sys.path.insert(0,'tests')
import test_start as ts
s=ts.FAKE_GH
import re
for i,l in enumerate(s.splitlines()):
    if 'api' in l and ('a[:1]' in l or 'a[0]' in l or 'API' in l): print(i,l)
print(s.splitlines()[-25:])
E
```

> 115 elif a[:1] == ["api"] and any(x.startswith("users/") for x in a):
> 117 elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/\d+/comments", x) for x in a):
> 125 elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/comments/\d+", x) for x in a):
> 135 elif a[:1] == ["api"] and "--paginate" in a:
> 137 elif a[:1] == ["api"] and len(a) == 2 and a[1].startswith("repos/o/r/issues/"):
> 140 elif a[:1] == ["api"]:
> ['elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/\\d+/comments", x) for x in a):', '    path = next(x for x in a if re.fullmatch(r"/?repos/o/r/issues/\\d+/comments", x))', '    n = int(path.rstrip("/").split("/")[-2])', '    body = api_body()', '    if body is None and (flag("-X", "--method") or "GET").upper() == "GET":', '        print(json.dumps([shown(c) for c in load() if c["number"] == n]))', '    else:', '        out(shown(create("pr" if n == 60 else "issue", n, body)))', 'elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/comments/\\d+", x) for x in a):', '    cid = next(x for x in a if re.fullmatch(r"/?repos/o/r/issues/comments/\\d+", x)).rsplit("/", 1)[1]', '    if (flag("-X", "--method") or "GET").upper() in ("PATCH", "POST"):', '        out(shown(edit(cid, api_body())))', '    else:', '        c = next((c for c in load() if c["id"] == int(cid)), None)', '        if c is None:', '            sys.stderr.write("HTTP 404: Not Found\\n")', '            sys.exit(1)', '        out(shown(c))', 'elif a[:1] == ["api"] and "--

`13. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "autopilot.md" -B3 -A6 .github/workflows/agent.yml | head -40; grep -n "autopilot" .github/workflows/autopilot.yml | head
```

> 402-        run: |
> 403-          set -- $NEXT
> 404-          # On autopilot, one line on the issue where the owner would have typed `/work`.
> 405:          if [ -s "$OUT/autopilot.md" ]; then gh issue comment "$N" -R "$GITHUB_REPOSITORY" --body-file "$OUT/autopilot.md"; fi
> 406-          if [ "$2" = split ]; then
> 407-            # An approved split is filed by code, as `/work` files it; its Split filed record is a comment of its own.
> 408-            if ! CARD_ID= python3 -m dokima.agent split "$N" 2> /tmp/split-why.txt; then
> 409-              # Filing failed: one comment on the issue says why and mentions the owner.
> 410-              OWNERS=$(python3 -m dokima.plan approvers | tr ',' '\n' | sed 's/^/@/' | paste -sd' ')
> 411-              printf '%s\n' "**Filing the split failed:** $(tail -1 /tmp/split-why.txt)" "" \
> 1:name: autopilot
> 2:run-name: "autopilot after #${{ github.event.issue.number }} closed"
> 4:# autopilot from GitHub: a parent whose last sub-issue closed closes too, saying its whole tree is done, and that
> 5:# close counts one level up; a done tree (its top issue closed) goes off autopilot; and every issue left on autopilot
> 15:  group: autopilot
> 39:      - name: Say why autopilot stopped, on the issue that closed
> 46:          printf 'Autopilot could not finish after #%s closed: %s ([run](%s))\n' "$N" "$(paste -sd' ' /tmp/why.txt 2>/dev/null)" "$RUN" > /tmp/autopilot.md
> 47:          gh issue comment "$N" -R "$GITHUB_REPOSITORY" --body-file /tmp/autopilot.md

`14. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["Planned three criteria: on autopilot a blocked issue's approved plan waits with one line naming its open blockers; the last blocker closing starts its worker once with `Autopilot: blockers closed, starting work`; AGENTS.md says the rule.",
          "Wrote seven tests in tests/test_blocked_worker.py, plus one rule: when GitHub cannot list the blockers, the worker does not start and the issue quotes GitHub's error.",
          "Closed #301 in the setup of two tests in tests/test_plan_links_recorded.py, so they still show the worker starting once nothing open blocks it."],
  "decided": ["`/autopilot start` on a plan approved before the issue went on autopilot, and an approved split on a blocked issue, stay as they are today."],
  "open": ["`/autopilot start` can still start a blocked worker early; the planner flagged it as a possible issue of its own."]},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the story and each new test fails today because the feature is missing; it can go to work.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 2 says only a newest plan that is approved starts the worker. The tests cover a plan still under review and a re-plan not yet reviewed, but not a plan approved and then blocked by a later `/review`. Code that only looks for an approval after the newest plan would pass.",
   "evidence": "tests/test_blocked_worker.py::test_only_an_approved_newest_plan_starts_its_worker covers the 'under review' and 're-plan not reviewed' histories only"},
  {"text": "The waiting line has to be posted by `agent next` itself. agent.yml posts autopilot.md only on a start, and the test asserts autopilot.md is absent, so the worker can't route the line through that file.",
   "evidence": ".github/workflows/agent.yml:405; tests/test_blocked_worker.py asserts `not os.path.exists(out/autopilot.md)` and that new_comments == [WAIT...]"}],
 "resol
```

> (Bash completed with no output)

`15. Bash`
```
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 253; echo $?; python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0
> 0

**Agent:** I approved the plan for #253, so it can go to the worker. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**Tests run:**
- All 7 new tests in `tests/test_blocked_worker.py` fail today because the feature is missing, not because of a crash or bad setup:
  - A blocked plan still starts its worker.
  - A blocker closing starts nothing ("#101 closed: nothing on autopilot to do").
  - `AGENTS.md` doesn't state the rule yet.
- The two tests the planner changed in `tests/test_plan_links_recorded.py` still pass. It closed #301 in their setup so they keep proving the worker starts once nothing open blocks it.
- The existing autopilot tests won't break once the worker reads an issue's blockers. Their fake GitHub answers that read with an empty list.

**Asks:** all six asks in the issue match a criterion: four for the behaviour (253.1, 253.2), one for `AGENTS.md` (253.3), and one for the case where GitHub can't list the blockers (253.4). The plan has no questions for the owner.

**Two notes, not blocking:**
- The tests for "only a newest plan that is approved starts the worker" cover a plan still under review and a re-plan not yet reviewed. They don't cover a plan that was approved and then blocked by a later `/review`.
- The "waiting for #A and #B to close" line has to be posted by the `next` step itself. `agent.yml` posts `autopilot.md` only when a stage starts, and the test checks that file is absent.

**Proposed new issue:** `/autopilot start` can still start a blocked issue's worker right away. This happens when its plan was approved while the issue was off autopilot. It goes against the owner's rule on #231, but the planner put it out of scope for this story and flagged it, so it's a separate issue rather than a blocker.
