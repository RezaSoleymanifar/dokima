# reviewer (plan) for #252

Run: https://github.com/dokima-dev/dokima/actions/runs/37863910932

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  9 00:16 .
> drwxrwxrwt 18 root   root    4096 Oct  9 00:16 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 00:16 in
> -rw-r--r--  1 runner runner 17240 Oct  9 00:16 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 00:16 open_blockers.json
> -rw-r--r--  1 runner runner  5444 Oct  9 00:16 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  9 00:16 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 00:16 ..
> -rw-r--r-- 1 runner runner 6094 Oct  9 00:16 01-planner.json
> # Issue #252: Once the plan passes review, code records its links on both issues and redraws both cards
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 3</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** When a plan passes review, its links show on both issues: blocking as GitHub's own blocked-by links, and every kind (blocked by, blocks, relates to) on the cards of both issues, kept up to date when a later plan adds or drops a link.
> 
> **Context:** From the owner's comments on #231: "once the plan passes review, code records each link on both issues using GitHub's own blocked-by relationships, so the other issue shows it too ... The model never writes them itself" (18:48), and "Relates to is never written as a comment. Code updates the cards of both issues whenever any link (blocked by, blocks, relates to) is added or removed, and handles a contradic

`2. Bash`
```
cd /home/runner/work/dokima/dokima; wc -l tests/test_plan_links_recorded.py; cat tests/test_plan_links_recorded.py
```

> <persisted-output>
> Output too large (35.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2ed7059c-7607-4afd-9648-168b12dff5c1/tool-results/br8ioyo7o.txt
> 
> Preview (first 2KB):
> 707 tests/test_plan_links_recorded.py
> """Once a plan passes review, code records its links and redraws both cards (#252).
> 
> Story 3 of #231.
> 
> The planner's plan.json carries `links`: three lists of open issue numbers, `blocked_by`, `blocks` and `relates_to`.
> When the plan reviewer approves the plan, `python3 -m dokima.agent next N OUT` (the step of agent.yml that decides
> what follows a run, given the run's record in OUT/record.json) records them: each blocked_by link as GitHub's own
> blocked-by link on this issue, each blocks link as the other issue blocked by this one, and it removes a blocking link
> the previous approved plan had and the new one dropped. Then it redraws the card of this issue and of every issue a
> link was added to or dropped from, so the other issue's card shows the link from its own side. Relates to has no
> GitHub link and no comment is ever posted for it; how the other card learns of it is the worker's choice, but the
> link must still show after that card is redrawn again by `python3 dokima/card.py` (card.yml's own redraw).
> 
> When recording would make issues block each other, directly or through other issues, nothing is recorded and the
> river stops for the owner, saying which issues. When GitHub refuses a link, the river stops and says which link an

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/2ed7059c-7607-4afd-9648-168b12dff5c1/tool-results/br8ioyo7o.txt
```

> 1	707 tests/test_plan_links_recorded.py
> 2	"""Once a plan passes review, code records its links and redraws both cards (#252).
> 3	
> 4	Story 3 of #231.
> 5	
> 6	The planner's plan.json carries `links`: three lists of open issue numbers, `blocked_by`, `blocks` and `relates_to`.
> 7	When the plan reviewer approves the plan, `python3 -m dokima.agent next N OUT` (the step of agent.yml that decides
> 8	what follows a run, given the run's record in OUT/record.json) records them: each blocked_by link as GitHub's own
> 9	blocked-by link on this issue, each blocks link as the other issue blocked by this one, and it removes a blocking link
> 10	the previous approved plan had and the new one dropped. Then it redraws the card of this issue and of every issue a
> 11	link was added to or dropped from, so the other issue's card shows the link from its own side. Relates to has no
> 12	GitHub link and no comment is ever posted for it; how the other card learns of it is the worker's choice, but the
> 13	link must still show after that card is redrawn again by `python3 dokima/card.py` (card.yml's own redraw).
> 14	
> 15	When recording would make issues block each other, directly or through other issues, nothing is recorded and the
> 16	river stops for the owner, saying which issues. When GitHub refuses a link, the river stops and says which link and why.
> 17	
> 18	Every test runs the real commands as subprocesses against a fake GitHub: a `gh` program put first on PATH that keeps
> 19	its state in one JSON file (issues with the

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_plan_links_recorded.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ (passed|failed))|Error|assert" | head -60
```

> >       assert hub.blocked_by(N) == [301], f"252.1: #252 should be blocked by #301 on GitHub, has {hub.blocked_by(N)}"
> E       AssertionError: 252.1: #252 should be blocked by #301 on GitHub, has []
> E       assert [] == [301]
> tests/test_plan_links_recorded.py:407: AssertionError
> >       assert hub.blocked_by(N) == [301], f"252.1: the approved plan's link was not recorded: {hub.blocked_by(N)}"
> E       AssertionError: 252.1: the approved plan's link was not recorded: []
> E       assert [] == [301]
> tests/test_plan_links_recorded.py:423: AssertionError
>         assert (N, 301) not in added, "252.1: a link GitHub already had was added again"
> >       assert added == [(302, N)], f"252.1: expected only #302 blocked by #252 to be added, got {added}"
> E       AssertionError: 252.1: expected only #302 blocked by #252 to be added, got []
> E       assert [] == [(302, 252)]
> tests/test_plan_links_recorded.py:441: AssertionError
> >       assert hub.blocked_by(N) == [301, 304, 305] and hub.blocked_by(302) == [N], \
> E       AssertionError: 252.1: the first approved plan's links were not recorded
> E       assert ([305] == [301, 304, 305]
> tests/test_plan_links_recorded.py:454: AssertionError
> >       assert hub.blocked_by(N) == [301], f"252.1: a blocked re-plan removed a link: {hub.blocked_by(N)}"
> E       AssertionError: 252.1: a blocked re-plan removed a link: []
> E       assert [] == [301]
> tests/test_plan_links_recorded.py:473: AssertionError
> >       assert hub.card_links(N) == {"blocked_by": {301}, "

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_plan_links_recorded.py 2>&1 | tail -22
```

> - ]
> FAILED tests/test_plan_links_recorded.py::test_a_link_github_refuses_stops_the_river_and_says_why - AssertionError: 252.5: the river should stop for the owner, it said 'start worker'
> assert 'start worker' == 'stop'
>   
>   - stop
>   + start worker
> FAILED tests/test_plan_links_recorded.py::test_a_link_github_fails_to_remove_stops_the_river_and_says_why - AssertionError: 252.5: the river should stop for the owner, it said 'start worker'
> assert 'start worker' == 'stop'
>   
>   - stop
>   + start worker
> FAILED tests/test_plan_links_recorded.py::test_recorded_links_let_autopilot_go_on - AssertionError: 252.5: the links were not recorded: #252 [], #302 []
> assert ([] == [301]
>   
>   Right contains one more item: 301
>   
>   Full diff:
>   + []
>   - [
>   -     301,
>   - ])
> 18 failed in 3.57s

**Agent:** All 18 new tests fail today; I'm checking each fails for the right reason, then the owner's asks against the criteria.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_plan_links_recorded.py 2>&1 | grep -E "^FAILED" | cut -c1-230; git log --oneline -3 -- tests/test_plan_links_recorded.py; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.keys());print(d.get('check'))"
```

> FAILED tests/test_plan_links_recorded.py::test_an_approved_plan_records_its_blocking_links_on_github - AssertionError: 252.1: #252 should be blocked by #301 on GitHub, has []
> FAILED tests/test_plan_links_recorded.py::test_a_plan_the_review_blocks_records_nothing - AssertionError: 252.1: the approved plan's link was not recorded: []
> FAILED tests/test_plan_links_recorded.py::test_a_link_github_already_has_is_not_added_twice - AssertionError: 252.1: expected only #302 blocked by #252 to be added, got []
> FAILED tests/test_plan_links_recorded.py::test_a_blocking_link_the_new_approved_plan_dropped_is_removed - AssertionError: 252.1: the first approved plan's links were not recorded
> FAILED tests/test_plan_links_recorded.py::test_a_replan_the_review_blocks_removes_nothing - AssertionError: 252.1: a blocked re-plan removed a link: []
> FAILED tests/test_plan_links_recorded.py::test_both_cards_show_every_new_link_from_their_own_side - AssertionError: 252.2: #252's card does not show its links: {'blocked_by': set(), 'blocks': set(), 'relates_to': set()}
> FAILED tests/test_plan_links_recorded.py::test_the_other_card_keeps_the_link_after_its_own_redraw - AssertionError: 252.2: #302 lost Blocked by #252 on redraw: {'blocked_by': set(), 'blocks': set(), 'relates_to': set()}
> FAILED tests/test_plan_links_recorded.py::test_a_dropped_link_leaves_both_cards - AssertionError: 252.2: #303's card never showed the link: {'blocked_by': set(), 'blocks': set(), 'relates_to': set()}
> FAILED tests/test_plan_

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "comment.md\|autopilot.md\|board.txt\|def next_step\|def main\|blocked_by\|def file_split" dokima/agent.py | head -60; grep -n "agent next\|comment.md\|board.txt" .github/workflows/agent.yml | head
```

> 132:LINKS = ("blocked_by", "blocks", "relates_to")
> 213:def file_split(repo, parent, recs, labels=()):
> 231:                      "blocked_by": [d + 1 for d in st.get("depends_on", [])]})
> 234:        for d in f["blocked_by"]:
> 236:                gh("api", "-X", "POST", f"repos/{repo}/issues/{f['issue']}/dependencies/blocked_by", "-F", f"issue_id={by_story[d]['id']}")
> 511:        lines += [""] + [f"{f['story']}. #{f['issue']} {f['title']}" + (f" ({field_icon(repo, 'blocked by')} blocked by {', '.join('#' + str(num[d]) for d in f['blocked_by'])})" if f["blocked_by"] else "")
> 1107:def blocked_by(repo, number):
> 1109:    return json.loads(gh("api", f"repos/{repo}/issues/{number}/dependencies/blocked_by", "--paginate") or "[]")
> 1140:        blockers = blocked_by(repo, n)
> 1344:def next_step(items, rec, owners, rounds=3, autopilot=lambda: False, body="", number=""):
> 1498:def main(argv):
> 1500:    agent record ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR  (writes OUT/record.json and OUT/comment.md) |
> 1506:    switched; with OUT, `start` writes what it picks up to OUT/next.txt and its Autopilot line to OUT/autopilot.md) |
> 1537:        open(os.path.join(out, "comment.md"), "w").write(render(rec, plan=plan if isinstance(plan, dict) else None))
> 1545:        open(os.path.join(out, "comment.md"), "w").write(render(rec))
> 1556:        open(os.path.join(out, "comment.md"), "w").write(render(rec))
> 1609:            start_waiting(repo, [f["issue"] for f in rec["handback"]["stories"] if not f["blocked_by

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1615,1665p dokima/agent.py
```

> print(plan["handback"].get("kind", "") if plan and approved(recs) else "")
>         return 0
>     if argv[1] == "next":
>         number, out = argv[2], argv[3]
>         owners = [o for o in os.environ.get("OWNERS", "").split(",") if o]
>         rec = json.load(open(os.path.join(out, "record.json")))
>         repo = os.environ["GITHUB_REPOSITORY"]
>         # A run that never started stops for the owner, and a cancelled one stops, whatever the conversation says,
>         # so it is not read.
>         d, items = ({}, []) if rec.get("role") in ("not-started", "cancelled") else conversation(repo, number)
>         read = []
> 
>         def autopilot():
>             # Read once, and only when the river's decision turns on it.
>             if not read:
>                 read.append(on_autopilot(repo, number))
>             return read[0]
>         step = next_step(items, rec, owners, autopilot=autopilot, body=d.get("body") or "", number=number)
>         if approves_work(rec):
>             # On autopilot the code review's approval stands in for the owner's: the pull request merges by itself.
>             on = autopilot()
>             if on is None:
>                 step = ("stop", f"{UNREAD} {step[1]}")
>             elif on:
>                 pr, merged, why = automerge(repo, number)
>                 step = ("merged", f"Autopilot merged PR #{pr}; what it unblocks starts when the issue closes.") if merged else \
>                     ("stop", f"Autopilot did not merge the pull request: {why}. It waits for you: merge 

`9. Bash`
```
cd /home/runner/work/dokima/dokima; cat > /tmp/t_card.py <<'EOF'
import sys; sys.path.insert(0, "/home/runner/work/dokima/dokima/tests"); sys.path.insert(0, "/home/runner/work/dokima/dokima")
import test_plan_links_recorded as t, tempfile, pathlib
d = pathlib.Path(tempfile.mkdtemp())
h = t.Hub(d)
h.approve(t.links([301],[302],[303]))
for n in (302, t.N): h.redraw(n); print(n, repr(h.body(n)[:300]))
print(h.writes())
EOF
python3 /tmp/t_card.py
```

> 302 '<!-- dokima-card -->\n**Backlog**\n\n[issue #302](https://github.com/o/r/issues/302)\n\nThis issue has no plan yet.\n\n**Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https:'
> 252 '<!-- dokima-card -->\nLinks are recorded on both issues.\n\n**Plan** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan\n\n[issue #252](https://github.com/o/r/issues/252)\n\n<img'
> [{'op': 'body', 'issue': 302}, {'op': 'body', 'issue': 252}]

`10. Bash`
```
cd /home/runner/work/dokima/dokima; cat >> /tmp/t_card.py <<'EOF'
print(h.card_links(t.N)); print(h.card_links(302))
EOF
python3 /tmp/t_card.py | tail -2; grep -n "asks\|source" dokima/agent.py | grep -i "ask" | head -20
```

> {'blocked_by': {301}, 'blocks': {302}, 'relates_to': {303}}
> {'blocked_by': set(), 'blocks': set(), 'relates_to': set()}
> 396:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 418:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 421:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 669:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 706:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 710:def problems_asks(r, ids):
> 711:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 713:    asks = r.get("asks")
> 714:    if not isinstance(asks, list) or not asks:
> 715:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 717:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 718:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 799:        bad.append("the worker never asks the owner; the plan is the contract")
> 938:                bad += problems_asks(data, plan_criteria(plan, number))

`11. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 710,730p dokima/agent.py; grep -n "def plan_criteria" -A15 dokima/agent.py
```

> def problems_asks(r, ids):
>     """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
>     they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
>     asks = r.get("asks")
>     if not isinstance(asks, list) or not asks:
>         return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
>                 "\"source\": \"a link to where they said it\", \"criterion\": \"N.k\" or \"missing\"}"]
>     bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
>     good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
>     for a in good:
>         c = a["criterion"].strip()
>         if c != "missing" and c not in ids:
>             bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
>                        f"({', '.join(ids) or 'none'})")
>     gone = [a["ask"] for a in good if a["criterion"].strip() == "missing"]
>     if r.get("verdict") == "approve" and gone:
>         bad.append("an approve keeps every ask, but these are marked missing: " + "; ".join(f'"{g}"' for g in gone))
>     return bad
> 
> 
> ASSUMPTION_SHAPE = ('{"question": "the plan\'s question", "accepted": true | false, "changes": true | false, '
> 869:def plan_criteria(plan, number):
> 870-    """The plan's criteria ids: N.k for a story (acceptance criteria, then non-f

**Agent:** The plan holds up: every new test fails today because the feature is missing. Writing the hand-back now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Planned #252 as one story with three acceptance criteria and two non-functional ones, each with its own tests in tests/test_plan_links_recorded.py (18 tests).",
   "Listed the plan's own links: blocks #253 and #254, relates to #269."
  ],
  "decided": [
   "A loop of blocking links records none of the plan's links and stops for the owner, naming every issue in the loop.",
   "A blocked-by link a person made by hand stays when an approved re-plan drops other links.",
   "How the other issue's card learns of a relates-to link is left to the worker, as long as it still shows after that card is redrawn."
  ],
  "open": [
   "Concern for the owner: #269 would write the same links earlier, when the plan passes its check; the planner recommends #269 leaves that to this story."
  ]
 },
 "verdict": "approve",
 "summary": "The plan keeps every ask of the owner, and each of its 18 tests fails today because the links are not yet recorded or drawn.",
 "blockers": [],
 "notes": [
  {
   "text": "The loop tests check that the stop names the issues and mentions the owner, but not that it says they would block each other; any stop naming those numbers would pass. A check for words like \"block each other\" or \"loop\" would close that.",
   "evidence": "tests/test_plan_links_recorded.py:583-587 and 601-604"
  },
  {
   "text": "The direct-loop test checks only #303's card for a leaked link; it does not check #301's or #252's card stay without the plan's links.",
   "evidence": "tests/test_plan_links_recorded.py:580-582"
  }
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {
   "ask": "once the plan passes review, code records each link on both issues using GitHub's own blocked-by relationships, so the other issue shows it too",
   "source": "https://github.com/dokima-dev/dokima/issues/231",
   "criterion": "252.1"
  },
  {
   "ask": "Nothing is recorded for a plan the revie
```

> previous_step holds at most five lines
> rc=1

`13. Bash`
```
python3 - <<'EOF'
import json
p="/tmp/dokima-out/review.json"; r=json.load(open(p))
r["previous_step"]={"did":["Planned #252 as one story with three acceptance criteria and two non-functional ones, each proven by tests in tests/test_plan_links_recorded.py (18 tests); the plan blocks #253 and #254 and relates to #269."],
 "decided":["A loop of blocking links records none of the plan's links and stops for the owner, naming every issue in the loop.",
  "A blocked-by link a person made by hand stays when an approved re-plan drops other links.",
  "How the other issue's card learns of a relates-to link is left to the worker, as long as it still shows after that card is redrawn."],
 "open":["Concern for the owner: #269 would write the same links earlier, when the plan passes its check; the planner recommends #269 leaves that to this story."]}
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 252 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #252. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**Tests:** I ran all 18 new tests in `tests/test_plan_links_recorded.py` and all 18 fail today for the right reason. Each one fails because links aren't yet recorded on GitHub, the cards aren't redrawn, or the river doesn't stop. None fails from a crash or a broken setup. I also confirmed that `dokima/card.py` runs against the tests' fake GitHub without crashing, so the redraw tests can pass once the feature is built.

**Your asks:** I found 7 asks in the issue and in your comments on #231, and each one maps to a criterion:
- Record blocking links on both issues → 252.1
- Don't record for a blocked plan, don't add a link twice, remove a dropped one → 252.1
- Relates to is never a comment → 252.2
- Redraw the cards of both issues when any link is added or removed → 252.2
- Handle two issues blocking each other → 252.3
- The model never writes the links → 252.4
- A link GitHub refuses or fails to remove stops the river → 252.5

**Notes (not blockers):**
1. The loop tests check that the river stops and names the right issues, but not that the message says they would block each other. Any stop naming those numbers would pass.
2. The direct-loop test only checks #303's card for links that shouldn't be there. It doesn't check #301's or #252's cards.

**Open for you:** the planner raised a concern that #269 would write the same links earlier, as soon as a plan passes its check and before any review. It recommends #269 drops its link writing and leaves it to this story.

The plan has no questions for you.
