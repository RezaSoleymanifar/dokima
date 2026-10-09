# reviewer (plan) for #300

Run: https://github.com/dokima-dev/dokima/actions/runs/38005790703

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (30.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3535f80d-4b62-4b18-ab27-c1295c22622e/tool-results/b0r7flhhg.txt
> 
> Preview (first 2KB):
> .:
> total 52
> drwxr-xr-x  3 runner runner  4096 Oct  9 23:43 .
> drwxrwxrwt 18 root   root    4096 Oct  9 23:43 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 23:43 in
> -rw-r--r--  1 runner runner 19588 Oct  9 23:43 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 23:43 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 23:43 parent.json
> -rw-r--r--  1 runner runner 11412 Oct  9 23:43 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner  4096 Oct  9 23:43 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 23:43 ..
> -rw-r--r-- 1 runner runner 12096 Oct  9 23:43 01-planner.json
> # Issue #300: Every agent's hand-back raises and answers through the same two fields, and nothing raised is skipped
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299 -->
> <!-- dokima-blocking: {"blocked_by": [298, 299], "blocks": [301, 302], "loop": []} -->
> **Backlog**
> 
> [issue #300](https://github.com/dokima-dev/dokima/issues/300)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298, #299
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #301, #302
> <img src="https://raw

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-card/,$p' issue.md | sed -n '15,400p'
```

> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 3</summary>
> 
> **Part of:** #289 Every agent raises things and answers them through the same two fields
> 
> **User story:** The planner, the worker and the reviewer each start with the exact list of raises they must answer, hand back their work plus raises and answers, and the river routes by them, so nothing any of them raises is dropped.
> 
> **Context:** Owner's words: the issue body (two fields; the rest is the agent's work; answered next turn; three blocks still stop; one shared prompt section with examples of each kind) and the comments of 2026-10-09T01:27:26Z (links stay the planner's own field; notes are dropped) and 01:39:55Z (only model judgments; autopilot-only tier). Fields to retire: the planner's questions, concerns and replies (dokima/roles/planner.md, dokima/planner.py), the worker's suspect_tests, outside_scope and replies (dokima/roles/worker.md; dokima/agent.py problems_work() 802), and the reviewer's blockers, notes, outside_plan, resolved, issues_found and assumptions (dokima/roles/reviewer.md; problems_shape() 844, problems_assumptions() 763). Work that stays: summary, user_story or stories, criteria, scope, tests, test_changes, links (planner); summary, criteria, evidence (worker); previous_step, verdict, summary, asks (reviewer). The river reads the old fields in dokima/ag

`3. Bash`
```
cd /tmp/pack; cat parent.json; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k not in ('test_changes',)},indent=1))"; python3 -c "
import json;p=json.load(open('in/01-planner.json'));print(list(p.keys())); print(json.dumps({k:v for k,v in p.items() if k!='handback'},indent=1)[:3000])"
```

> {"number": 289}[]{
>  "kind": "user_story",
>  "summary": "The planner, worker and reviewer raise and answer only through raises and answers, and code makes sure nothing raised is skipped.",
>  "user_story": "Every agent starts with the exact list of raises it must answer, hands back its work plus raises and answers, and the river routes by them, so nothing any agent raises is dropped.",
>  "acceptance_criteria": [
>   {
>    "text": "Every planner, worker and reviewer hand-back raises and answers only through two fields, raises and answers. The checker rejects questions, concerns, replies, suspect_tests, outside_scope, blockers, notes, assumptions, issues_found, outside_plan or resolved, even when empty, naming each one. Everything else stays the agent's work: summary, plan, criteria built, verdict and links. A doubt the planner has about the ask reaches you as a question for you, its evidence shown on the planner's comment.",
>    "source": "https://github.com/dokima-dev/dokima/issues/289"
>   },
>   {
>    "text": "Before an agent runs, its starting pack lists exactly the open raises addressed to it, each with its ID. The reviewer's list also holds raises passing through it, such as a worker's raise for the planner. The checker rejects a hand-back unless every raise on that list has an answer naming its ID, done or disagree with why, and names each one skipped. A raise already answered is not on the next list. A record posted before this change is never rejected or rewritten: the next pack st

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -40; timeout 10 curl -s https://api.github.com/repos/dokima-dev/dokima/issues/289 | head -c 600
```

> commit cbb1e7ae4a9a04d78cd4d589a15eb32fddf71d08
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 23:42:57 2026 +0000
> 
>     planner for #300 (run 38002030735)
> 
>  tests/samples/132/plan.json      |  11 +-
>  tests/samples/132/review-pr.json |  12 +-
>  tests/samples/132/work.json      |   5 +-
>  tests/test_agent.py              |  83 ++---
>  tests/test_automerge.py          |   7 +-
>  tests/test_autopilot_river.py    |  95 ++----
>  tests/test_cancelled_run.py      |   4 +-
>  tests/test_failed_run_card.py    |   4 +-
>  tests/test_fixer.py              |  48 +--
>  tests/test_handback_check.py     | 100 ++----
>  tests/test_live_queue.py         |   4 +-
>  tests/test_parent_source.py      |  38 ++-
>  tests/test_plan_check.py         |  20 +-
>  tests/test_plan_check_rerun.py   |   4 +-
>  tests/test_questions.py          |  87 +-----
>  tests/test_raise_handbacks.py    | 642 +++++++++++++++++++++++++++++++++++++++
>  tests/test_review_asks.py        |  18 +-
>  tests/test_start.py              |   2 +-
>  tests/test_work_column.py        |   2 +-
>  19 files changed, 834 insertions(+), 352 deletions(-)
> {
>   "url": "https://api.github.com/repos/dokima-dev/dokima/issues/289",
>   "repository_url": "https://api.github.com/repos/dokima-dev/dokima",
>   "labels_url": "https://api.github.com/repos/dokima-dev/dokima/issues/289/labels{/name}",
>   "comments_url": "https://api.github.com/repos/dokima-dev/dokima/issues/289/comments",
>   "events_url": "https://api.github.com/r

**Agent:** Public API is reachable; I'll read the parent's owner words.

`5. Bash`
```
cd /tmp; timeout 20 curl -s https://api.github.com/repos/dokima-dev/dokima/issues/289 | python3 -c "import json,sys;d=json.load(sys.stdin);b=d['body'];i=b.find('<!-- /dokima-card -->');print(b[i:])"; timeout 20 curl -s "https://api.github.com/repos/dokima-dev/dokima/issues/289/comments?per_page=100" | python3 -c "
import json,sys
for c in json.load(sys.stdin):
  if 'bot' in c['user']['login']: continue
  print('=====',c['user']['login'],c['created_at'],c['html_url']);print(c['body'])"
```

> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Agents raise things through about ten different fields today (questions, concerns, replies, suspect tests, outside scope, blockers, notes, assumptions, issues found, outside plan, resolved). They are the same few ideas in different clothes. I want the smallest set that covers every case.
> 
> What I want:
> - Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).
> - A raise is exactly one of three kinds: question (for me; on autopilot the reviewer answers it for me when my own words settle it, with them as evidence), blocker (names who must fix it), or issue (outside this one; code files it). The list is closed: the checker rejects any other kind, and adding a kind is a code change I approve, never something an agent invents.
> - Who can raise to whom is a fixed table in code: the planner raises questions to me; the worker raises blockers for the planner only through the reviewer, who judges whether they are real; the reviewer raises to the planner, the worker or me; anyone can raise an issue. The checker rejects anything outside the table.
> - Every raise addressed to an agent is answered by that agent in its next turn, done or disagree with why. The checker rejects a turn that skips one, so nothing is ever dropped. Three blocks in a row still stop and come to me.
> - Cards show one Raised section, each line with its kind'

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_raise_handbacks.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|Error" | head -40
```

> E           AssertionError: 300.1: a good review hand-back raising and answering through the two fields was rejected:
> /home/runner/work/dokima/dokima/tests/test_raise_handbacks.py:197: AssertionError
> E       AssertionError: 300.1: the planner's raise of kind note was not rejected: 0 ''
> /home/runner/work/dokima/dokima/tests/test_raise_handbacks.py:230: AssertionError
>         assert code == 0, f"300.1: the record step failed on a plan with a question:\n{said[-800:]}"
> E       AssertionError: 300.1: the planner's comment does not show the doubt's evidence:
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> E       assert 'dokima/board.py, column(), line 120' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...> **Doubt about the ask:** Is this already fixed? The board draws the column from the record since #339. · for you\n\n'
> /home/runner/work/dokima/dokima/tests/test_raise_handbacks.py:268: AssertionError
>         assert code == 0, f"300.2: the record step failed:\n{said[-800:]}"
> E       AssertionError: 300.2: the worker's raises were not stamped with who raised them: [{'kind': 'blocker', 'to': 'planner', 'label': 'Weak test', 'text': 'The test for 9.1 p

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,260p tests/test_raise_handbacks.py
```

> """Every agent's hand-back raises and answers through two fields, and nothing raised is skipped (#300).
> 
> The owner wants the planner, the worker and the reviewer to raise what they judge only as raises (a question, a
> blocker or an issue, dokima/raises.py from #298) and to answer what was raised to them only as answers, with every
> old field for this gone; each agent starts with the exact list it must answer, and code rejects a hand-back that
> skips one; the river routes by raises; and on autopilot the reviewer may answer a planner's question for the owner
> only with the owner's own words, checked by code.
> 
> What the code these tests run must do, as the plan pins it:
> - The old fields are questions, concerns, replies, suspect_tests, outside_scope, blockers, notes, assumptions,
>   issues_found, outside_plan and resolved. A planner hand-back (`python3 -m dokima.planner check N OUT`, a story or a
>   split) or a worker or reviewer hand-back (`python3 -m dokima.agent check work|review FILE PLAN N`) holding any of
>   them, even empty, is rejected with a reason naming each one it holds. Its "raises" are checked with
>   raises.check_raises for its role; "raises" and "answers" are lists and may be left out when empty.
> - A review that blocks raises at least one blocker; one that approves raises none.
> - `python3 -m dokima.agent record ROLE STAGE OUT CHECK PASSED LOGS` stamps the hand-back's raises in record.json
>   (raises.stamp): each gets "raised_by" and an ID that no raise or old blocker in the

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 260,642p tests/test_raise_handbacks.py
```

> assert code == 0, f"300.1: the record step failed on a plan with a question:\n{said[-800:]}"
>     rec_ = json.load(open(out / "record.json"))
>     kept = [r for r in rec_["handback"].get("raises") or [] if r.get("kind") == "question"]
>     assert len(kept) == 1 and kept[0].get("evidence") == DOUBT["evidence"] and kept[0].get("to") == "owner", \
>         f"300.1: the record does not keep the doubt as a question for the owner with its evidence: {kept}"
>     shown = (out / "comment.md").read_text().split("<details", 1)[0]
>     assert DOUBT["text"] in shown and "for you" in shown, \
>         f"300.1: the planner's comment does not show the doubt as a question for you:\n{shown}"
>     assert DOUBT["evidence"] in shown, f"300.1: the planner's comment does not show the doubt's evidence:\n{shown}"
>     step = agent.next_step([], rec_, [OWNER], autopilot=lambda: False)
>     assert step[0] == "stop", f"300.1: a plan with a doubt for the owner did not stop for them off autopilot: {step}"
> 
> 
> # 300.2: the exact list to answer, each by its ID; nothing skipped; old records still read.
> 
> def test_the_record_step_stamps_every_raise_with_who_raised_it_and_a_new_id(record_property, tmp_path):
>     """Code stamps each raise with who raised it and an ID new on the issue.
> 
>     Runs the record step for a worker raising two things, with earlier records in the pack holding raises P1 and R1
>     and an old review's blocker B1, and checks record.json gives each raise raised_by worker and an ID of its own.
> 
>     Proves

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def \|^[A-Z_]* = " dokima/raises.py; sed -n 1,40p dokima/raises.py
```

> 10:KINDS = ("question", "blocker", "issue")
> 12:TABLE = MappingProxyType({
> 18:THROUGH = MappingProxyType({("worker", "planner"): "reviewer"})
> 19:FIELDS = ("kind", "to", "label", "text", "evidence")
> 20:STAMPED = ("raised_by", "id")
> 21:ANSWERS = ("done", "disagree")
> 22:PREFIX = MappingProxyType({"planner": "P", "worker": "W", "reviewer": "R"})
> 25:def _kinds():
> 29:def check_raises(role, raises):
> 64:def sent_to(raise_):
> 72:def stamp(role, raises, taken):
> 90:def check_answers(role, answers, open_raises):
> """Raises: questions, blockers and issues an agent hands up, sent only where one table allows.
> 
> The kinds and the table live here alone, read-only: adding a kind or a row is a code change the owner approves, never
> something a hand-back carries. An agent writes a raise as {"kind", "to", "label", "text", "evidence"}; label and
> evidence are optional, a label never changes how a raise is checked or routed, and an issue has no "to". Code stamps
> who raised it and an ID; an agent that writes either is rejected. Whoever a raise is sent to answers it by its ID.
> """
> from types import MappingProxyType
> 
> KINDS = ("question", "blocker", "issue")
> # Who may send a question or blocker to whom. An issue is for no one.
> TABLE = MappingProxyType({
>     "planner": ("owner",),
>     "worker": ("planner",),
>     "reviewer": ("planner", "worker", "owner"),
> })
> # A worker's raise to the planner goes through the reviewer, who answers it first.
> THROUGH = MappingProxyType({("worker", "planner"): "reviewer"})
> FIELDS

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -nE '"?(questions|concerns|replies|suspect_tests|outside_scope|blockers|notes|assumptions|issues_found|outside_plan|resolved)"?' dokima/roles/plan-grade.md dokima/roles/result-grade.md | head; ls dokima/roles; grep -n "open_blockers\|check-round" .github/workflows/agent.yml | head
```

> dokima/roles/plan-grade.md:23:   readings, or an ask cannot be tested, the plan asks the owner in its questions; it never picks one silently and
> dokima/roles/plan-grade.md:32:Notes, never blockers:
> dokima/roles/result-grade.md:35:Notes, never blockers: readability, naming, docstrings, simpler ways to the same result. At most three.
> plan-grade.md
> planner.md
> result-grade.md
> reviewer.md
> worker.md
> 225:          CHECK="$CHECK && python3 -m dokima.agent check-round $ROLE $OUT/$FILE $PACK"
> 234:          - $PACK/open_blockers.json: the open blockers from the newest review at your stage. Answer every one by id.$( [ "$STAGE" = pr ] && echo "

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "agent record\|PACK=\|PACK:" .github/workflows/*.yml | head; grep -n "def record\|def main\|\"record\"\|PACK" dokima/agent.py | head -20
```

> .github/workflows/agent.yml:5:# conversation (comments, reviews, line notes) and every earlier agent record. The agent runs its own check before it
> .github/workflows/agent.yml:53:      PACK: /tmp/pack
> .github/workflows/agent.yml:287:            python3 -m dokima.agent record "$ROLE" "$STAGE" "$OUT" "$OUT/check.txt" "${PASSED:-false}" /home/runner/.claude/projects
> 79:def records(items):
> 462:def record_fold(rec):
> 1039:                parent = pack_parent(os.environ.get("PACK"), os.path.dirname(os.path.abspath(plan_path)))
> 1251:def record_links(repo, number, items):
> 1857:def main(argv):
> 1881:    if argv[1] == "record":
> 1890:        reviewed = os.path.join(os.environ.get("PACK", ""), "plan.json")
> 1892:        if role == "reviewer" and stage == "plan" and os.environ.get("PACK") and os.path.exists(reviewed):
> 1898:        folder = os.path.join(os.environ.get("PACK", ""), "in")
> 1899:        for name in sorted(os.listdir(folder)) if os.environ.get("PACK") and os.path.isdir(folder) else []:

**Agent:** Tests all fail on the missing feature so far; now running the full suite to check the modified older tests.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -x --co -q 2>&1 | tail -2; timeout 900 python3 -m pytest -q -n auto 2>/dev/null | tail -3 || true
```

> tests/test_worker_pr.py: 2

`13. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1200 python3 -m pytest -q tests/test_agent.py tests/test_autopilot_river.py tests/test_fixer.py tests/test_handback_check.py tests/test_parent_source.py tests/test_plan_check.py tests/test_questions.py tests/test_review_asks.py tests/test_start.py tests/test_live_queue.py tests/test_cancelled_run.py tests/test_failed_run_card.py tests/test_plan_check_rerun.py tests/test_automerge.py tests/test_work_column.py 2>&1 | grep -E "^FAILED|^ERROR|passed|failed" | cut -c1-260
```

> "a work.json with the old replies field passed"
> E       AssertionError: a work.json with the old replies field passed
>         """On autopilot the river still stops on an escalation, three blocks in a row, a rejected hand-back and a run that failed or never started.
> E         "https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md\",\n \"run\": \"https://github.com/o/r/actions/runs/42\",\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Planned one criterion.\"\n   ],\n   \"decided\": [],\n   \"open\":
>         Every cancelled run (including one cancelled after its blocking review had passed code's check, which the river
>         would otherwise send back to the planner), a review code rejected and a run whose tools failed to install must
>         make no call that starts or re-runs a run, and each must still have been seen as cancelled or failed. Beside them,
>             assert r.failed, f"188.3 ({name}): setup: the run did not fail:\n{r.tail()}"
> >       assert [(x["role"], x["stage"], x["check"]["passed"]) for x in recs] == [("reviewer", "plan", True)], \
> E       AssertionError: 215.1: code's check rejected the fake blocking review, so it never reached the river: [{'passed': False, 'problems': ['a block needs at least one blocker']}]
> __________ test_a_failed_run_lands_in_its_stage_column_with_needs_you __________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_failed_run_lands_in_its0')
>     def test_a_failed_run_lands_in_its_stage_column_with_nee

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 270,310p dokima/card.py; grep -n "questions" dokima/card.py dokima/agent.py | head -30
```

> def checks_passed(number, h, check_runs):
>     """True when every criterion's check of plan `h`, and All tests, passed on the PR's latest commit."""
>     count = len(h.get("acceptance_criteria") or []) + len(h.get("non_functional") or []) if h else 0
>     by_key = checks_by_key(check_runs)
>     runs = [by_key.get(f"{number}.{k}") for k in range(1, count + 1)]
>     runs.append(next((r for r in check_runs if r["name"] == ALL_TESTS), None))
>     return count > 0 and all(state(r) == "passed" for r in runs)
> 
> 
> def todo(issue, found, rec):
>     """What the owner must do now that the river stopped for them on the record `rec`."""
>     from dokima import agent
>     role, h = rec.get("role"), rec.get("handback") or {}
>     if role == "not-started":
>         return TODO["not started"]
>     if not rec.get("check", {}).get("passed"):
>         return TODO["rejected"]
>     if role == "planner" and h.get("questions"):
>         return TODO["questions"]
>     verdict = h.get("verdict") if role == "reviewer" else None
>     if verdict == "escalate":
>         return TODO["escalated"]
>     if verdict == "block":
>         return TODO["three blocks"]
>     if verdict == "approve" and rec.get("stage") == "plan":
>         return TODO["plan approved"]
>     if verdict == "approve":
>         planned = agent.latest(found["recs"], "planner")
>         h = planned["handback"] if planned else None
>         return TODO["ready"] if checks_passed(issue["number"], h, found["check_runs"]) else TODO["not every check passed"]
>     return "See t

**Agent:** Reviewed the tests and the owner's words; writing the hand-back.

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned five criteria: raises and answers replace every old field, each agent's pack lists the raises it must answer, the river routes by raises, autopilot answers a question for the owner only with the owner's words, and one shared prompt section.",
          "Wrote 13 new tests in tests/test_raise_handbacks.py and moved the older tests' sample hand-backs to raises and answers, deleting the tests of the retired questions and assumptions fields."],
  "decided": ["The pack keeps the file name open_blockers.json so no workflow changes; dokima/card.py is not changed.",
              "A reading that changes how the system works or what it costs still waits for the owner on autopilot, as AGENTS.md says today."],
  "open": ["The issue card's to-do line still reads the old questions field, and #241 overlaps this story's retirement of questions, concerns and replies."]},
 "verdict": "approve",
 "summary": "Every ask of this story has a criterion and tests that run the real check, pack and river and fail today because the feature is missing; nothing blocks.",
 "blockers": [],
 "notes": [
  {"text": "300.3 proves a question or blocker for the owner stops only after a plan review; a code review raising one for the owner is not run, so code stopping only at the plan stage would pass.",
   "evidence": "tests/test_raise_handbacks.py::test_the_river_sends_each_blocker_to_the_agent_it_names_and_stops_for_yours: the owner cases all use rec('reviewer', 'plan', ...)"},
  {"text": "The 'no prompt asks for an old field' check looks only for quoted names in the three role files; plan-grade.md, which is in scope, still says the plan asks the owner 'in its questions'.",
   "evidence": "dokima/roles/plan-grade.md:23; tests/test_raise_handbacks.py::test_the_shared_section_shows_a_real_example_of_each_kind checks f'\"{field}\"' in planner.md, worker.md and reviewer.md only"},
  {"text": "Criteri
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> the ask "Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links)." is matched to 1, which is not a criterion of the plan (300.1, 300.2, 300.3, 300.4, 300.5)
> the ask "outside plan and outside scope are blockers for me; suspect tests are blockers for the planner, through the reviewer; notes are dropped." is matched to 1, which is not a criterion of the plan (300.1, 300.2, 300.3, 300.4, 300.5)
> the ask "Blocked by, blocks and relates to are not raises; they stay the planner's own links field." is matched to 1, which is not a criterion of the plan (300.1, 300.2, 300.3, 300.4, 300.5)
> the ask "a doubt about the ask becomes a question for me, with its evidence." is matched to 1, which is not a criterion of the plan (300.1, 300.2, 300.3, 300.4, 300.5)
> the ask "Code records who raised each item (from the agent that ran, never the model) and gives it an ID that only lives in the JSON, never on a card. Answers point at that ID." is matched to 2, which is not a criterion of the plan (300.1, 300.2, 300.3, 300.4, 300.5)
> the ask "Before an agent runs, code puts the exact list of open raises addressed to it (or passing through it, for the reviewer) into its starting pack, and the checker rejects its hand-back unless every item on that list has an answer pointing at its ID." is matched to 2, which is not a criteri

`16. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
for a in r['asks']: a['criterion']='300.'+a['criterion']
r['summary']="Every ask has a criterion, and each test runs the real check, pack or river and fails today because the feature is missing."
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 300 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#300](https://github.com/dokima-dev/dokima/issues/300) (raises and answers replace the old hand-back fields). The review is in `/tmp/dokima-out/review.json` and passes both of code's checks.

**Why it passes:**
- **Every ask is covered.** I read the owner's own words in parent [#289](https://github.com/dokima-dev/dokima/issues/289) (one set of raise and answer fields for every agent): the issue text and their comments. I found 12 asks that belong to this story, and each one maps to one of the plan's five criteria. None is missing.
- **Every new test fails for the right reason.** All 13 tests in `tests/test_raise_handbacks.py` fail today on an assertion that the feature is missing, not on a crash or a bad path. They run the real checker, the record step, the starting pack and the routing code. Each "rejects the bad case" test has a "passes the good case" test beside it.
- **The changed older tests also fail for the right reason.** 15 older tests that use the moved sample hand-backs now fail because the old code doesn't accept the new format yet.

**Notes (not blockers):**
1. The routing test only checks that a question or blocker for the owner stops after a plan review. Nothing checks the same after a code review, so code that stopped only at the plan stage would still pass.
2. The "no prompt asks for an old field" test looks only in the three role files, and only for field names in quotes. `dokima/roles/plan-grade.md:23`, which is in scope, still says the plan asks the owner "in its questions".
3. Criterion 4 adds a rule that the story text doesn't state: on autopilot, a reading that changes how the system works or what it costs still waits for the owner. It comes from AGENTS.md and keeps today's behaviour, so I didn't block on it.

**Proposed issue:** once the old questions field is gone, the issue card's to-do line (`dokima/card.py:289`) no longer says "Answer the questions" for a plan that asks the owner something. It falls back to "See the newest record below". This plan can't fix it because `card.py` may only change when an issue asks.

The planner also flagged that open [#241](https://github.com/dokima-dev/dokima/issues/241) (the planner keeps its questions field) is largely overturned by this story. Only its five-criteria cap would be left.
