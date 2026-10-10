# reviewer (plan) for #301

Run: https://github.com/dokima-dev/dokima/actions/runs/38060414595

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 36
> drwxr-xr-x  3 runner runner 4096 Oct 10 14:38 .
> drwxrwxrwt 18 root   root   4096 Oct 10 14:38 ..
> drwxr-xr-x  2 runner runner 4096 Oct 10 14:38 in
> -rw-r--r--  1 runner runner 9914 Oct 10 14:38 issue.md
> -rw-r--r--  1 runner runner    2 Oct 10 14:38 open_blockers.json
> -rw-r--r--  1 runner runner   15 Oct 10 14:38 parent.json
> -rw-r--r--  1 runner runner 4065 Oct 10 14:38 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct 10 14:38 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 14:38 ..
> -rw-r--r-- 1 runner runner 4700 Oct 10 14:38 01-planner.json
> # Issue #301: The reviewer settles raises between agents and confirms issues before code files them
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299, 300 -->
> <!-- dokima-blocking: {"blocked_by": [298, 300], "blocks": [302], "loop": []} -->
> **Backlog**
> 
> [issue #301](https://github.com/dokima-dev/dokima/issues/301)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298, #300
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #302
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #299
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima

`2. Bash`
```
cd /tmp/pack; cat parent.json; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_reviewer_settles.py
```

> {"number": 289}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38059815663",
>  "commit_before": "e02bcb264bf540a81ee342e4d6eb36435fcaa4fa",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 1958,
>   "turns": 1,
>   "cost_usd": 2.2300613999999994,
>   "tokens_in": 134430,
>   "tokens_out": 127
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/301/38059815663-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38059815663",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> commit 09cd767470d2131909fa0ced3aaeae4fec910605
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 14:38:14 2026 +0000
> 
>     planner for #301 (run 38059815663)
> 
>  tests/test_reviewer_settles.py | 600 +++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 600 insertions(+)
> 600 tests/test_reviewer_settles.py

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_reviewer_settles.py
```

> <persisted-output>
> Output too large (31.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/dcbffef4-ec70-4feb-86ea-b97797207129/tool-results/bmwbqm6dk.txt
> 
> Preview (first 2KB):
> """The reviewer settles raises between agents and confirms issues before code files them (#301).
> 
> Story 4 of #289. A worker's raise for the planner ("this test is broken") goes to the reviewer first. When the reviewer
> answers it done, the planner starts with it as the reviewer's blocker; when the reviewer answers it disagree, the worker
> starts again with the reviewer's why. Neither waits for the owner, and on autopilot neither merges the pull request.
> 
> An issue raise (a real problem outside this issue) becomes its own GitHub issue only once the reviewer confirms it: the
> reviewer's own issue raises count as confirmed and are filed in its run, and its record says so; the planner's or the
> worker's are listed for the reviewer's next run, filed when it answers done and never when it answers disagree, and
> never in the planner's or worker's own run. Filing is done by `python3 -m dokima.agent next N OUT`, the step of
> agent.yml that runs after the agent finished, holds the app's key and finishes the run's record (OUT/comment.md). An
> issue GitHub refuses to file is named on the record with GitHub's reason, and the record and the river still stand.
> 
> The river tests call `agent.next_step` and `agent.raises_for` (what the pack writes to open_blockers.json) on records
> built her

`4. Read`
```
/home/runner/work/dokima/dokima/tests/test_reviewer_settles.py
```

> 1	"""The reviewer settles raises between agents and confirms issues before code files them (#301).
> 2	
> 3	Story 4 of #289. A worker's raise for the planner ("this test is broken") goes to the reviewer first. When the reviewer
> 4	answers it done, the planner starts with it as the reviewer's blocker; when the reviewer answers it disagree, the worker
> 5	starts again with the reviewer's why. Neither waits for the owner, and on autopilot neither merges the pull request.
> 6	
> 7	An issue raise (a real problem outside this issue) becomes its own GitHub issue only once the reviewer confirms it: the
> 8	reviewer's own issue raises count as confirmed and are filed in its run, and its record says so; the planner's or the
> 9	worker's are listed for the reviewer's next run, filed when it answers done and never when it answers disagree, and
> 10	never in the planner's or worker's own run. Filing is done by `python3 -m dokima.agent next N OUT`, the step of
> 11	agent.yml that runs after the agent finished, holds the app's key and finishes the run's record (OUT/comment.md). An
> 12	issue GitHub refuses to file is named on the record with GitHub's reason, and the record and the river still stand.
> 13	
> 14	The river tests call `agent.next_step` and `agent.raises_for` (what the pack writes to open_blockers.json) on records
> 15	built here. The filing tests run the real `agent next` as a subprocess against a fake GitHub: a `gh` program put first
> 16	on PATH that keeps its state in one JSON file and logs every call. 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_reviewer_settles.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | head -60
```

> E       AssertionError: 301.1: the planner should start with exactly the confirmed raise, gets []
> E       assert 0 == 1
> E        +  where 0 = len([])
> E       AssertionError: 301.1: an approving review that confirmed the worker's raise should start the planner, river says ('stop', 'The work is approved. Merge the pull request, or review it with a command to send it back.')
> E       assert ('stop', 'The...end it back.') == ('start', 'planner', '')
> E         
> E         At index 0 diff: 'stop' != 'start'
> E         Right contains one more item: ''
> E         
> E         Full diff:
> E           (
> E         -     'start',
> E         ?        ^^^
> E         +     'stop',
> E         ?        ^^
> E         -     'planner',
> E         -     '',
> E         +     'The work is approved. Merge the pull request, or review it with a command '
> E         +     'to send it back.',
> E           )
> E       AssertionError: 301.1: the planner should be handed the confirmed raise, gets []
> E       assert 0 == 1
> E        +  where 0 = len([])
> E           AssertionError: 301.1: the approve review that disagreed with the worker's raise should start the worker, river says ('stop', 'The work is approved. Merge the pull request, or review it with a command to send it back.')
> E           assert ('stop', 'The...end it back.') == ('start', 'worker', '')
> E             
> E             At index 0 diff: 'stop' != 'start'
> E             Right contains one more item: ''
> E             
> E             Full diff:
> E               (
> E  

**Agent:** Running the plan's tests on main's code: they fail for the right reasons so far. Checking the rest of the failures next.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_reviewer_settles.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed|AssertionError: 301" ; grep -n "def raises_for\|def next_step\|def check_answers" dokima/*.py
```

> E       AssertionError: 301.1: the planner should start with exactly the confirmed raise, gets []
> E       AssertionError: 301.1: an approving review that confirmed the worker's raise should start the planner, river says ('stop', 'The work is approved. Merge the pull request, or review it with a command to send it back.')
> E       AssertionError: 301.1: the planner should be handed the confirmed raise, gets []
> E           AssertionError: 301.1: the approve review that disagreed with the worker's raise should start the worker, river says ('stop', 'The work is approved. Merge the pull request, or review it with a command to send it back.')
> E           AssertionError: 301.1: on autopilot, a review answering the worker's raise done should start the planner, river said 'stop'
> E       AssertionError: 301.2: the reviewer's one issue raise should file exactly one issue, filed {}
> E       AssertionError: 301.2: the plan reviewer's pack should list the planner's issue P1, lists []
> E       AssertionError: 301.2: the worker's issue the reviewer confirmed should file exactly one issue, filed {}
> E       AssertionError: 301.2: the planner's issue the reviewer confirmed should file exactly one issue, filed {}
>             f"301.3: the run's record lost its full record or Next line when filing failed:\n{text}"
> E       AssertionError: 301.3: neither the record nor a comment on #301 names the finding with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues)'
> FAILED test

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "issue\", \"create\|issues_found\|filed-by-dokima" -r dokima | head; sed -n 170,215p dokima/agent.py; sed -n 80,130p dokima/raises.py
```

> dokima/audit.py:252:        url = gh("issue", "create", "--repo", repo, "--title", title, "--body", body)
> dokima/agent.py:25:              "issues_found", "outside_plan", "resolved")
> dokima/agent.py:360:        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
> dokima/agent.py:675:        if h.get("issues_found"):
> dokima/agent.py:677:            lines += [f"{i}. {f.get('title')}: {f.get('why')}" for i, f in enumerate(h["issues_found"], 1)]
>         out += [x for x in card.raises_of(h) if x.get("id") and x["id"] not in answered]
>         stage = r.get("stage") or ""
>         old = h.get("blockers") if isinstance(h.get("blockers"), list) else []
>         if r["role"] == "reviewer" and newest.get(stage) == i and h.get("verdict") != "approve":
>             out += [old_blocker(b, stage) for b in old if isinstance(b, dict) and filled(b.get("id"))
>                     and b["id"] not in answered]
>     return out
> 
> 
> def raises_for(recs, role):
>     """The open raises this role must answer by ID, oldest first."""
>     return [r for r in open_raises(recs) if raises.sent_to(r) == role]
> 
> 
> def taken_ids(recs):
>     """Every raise ID already on the issue, old blocker IDs included."""
>     ids = set()
>     for r in recs:
>         h = r.get("handback") if isinstance(r, dict) else None
>         if not isinstance(h, dict):
>             continue
>         for field in ("raises", "blockers"):
>             ids |= {x.get("id") for x in h.get(fi

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 230,250p dokima/card.py
```

> def answers_of(h):
>     """The answers a hand-back gives to earlier raises, by their IDs."""
>     v = h.get("answers") if isinstance(h, dict) else None
>     return [a for a in v if isinstance(a, dict) and a.get("raise")] if isinstance(v, list) else []
> 
> 
> def raise_line(repo, r):
>     """One raise as a list item: icon, label, words and who it is for.
> 
>     Its ID is never drawn."""
>     words = lambda s: escape(" ".join(str(s).split()))
>     label = f"**{words(r['label'])}:** " if isinstance(r.get("label"), str) and r["label"].strip() else ""
>     who = ("filed as an issue" if r["kind"] == "issue" else
>            "for you" if r.get("to") == "owner" else f"for the {words(r.get('to') or 'no one')}")
>     return f"- {field_icon(repo, RAISE_ICON[r['kind']])} {label}{words(r.get('text') or '')} · {who}"
> 
> 
> def waiting_raises(recs):
>     """Every raise on the issue still waiting for an answer, oldest first.
> 
>     Only records whose hand-back passed count: a rejected hand-back's raises are not drawn, and its answers

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote two criteria and one non-functional requirement for this story, and ten tests in tests/test_reviewer_settles.py, all failing today because the feature is missing.",
          "It raised one issue: the issue card says 'filed as an issue' for every issue raise, even one never filed."],
  "decided": ["A filed issue is titled with the raise's first sentence and its body holds the raise's words, its evidence and the issue it was found on.",
              "Labels on filed issues and never filing the same finding twice stay out of this story; #268 and #265 cover them."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the story, and each of its ten tests fails today because the reviewer does not yet settle raises or confirm issues before code files them.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "the worker raises blockers for the planner only through the reviewer, who judges whether they are real", "source": "https://github.com/dokima-dev/dokima/issues/289", "criterion": "301.1"},
  {"ask": "When the reviewer answers done, the planner starts with it as the reviewer's blocker; when the reviewer answers disagree, the worker starts again with the why. Neither waits for you.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.1"},
  {"ask": "Code files an issue raise as its own GitHub issue only once the reviewer confirms it.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.2"},
  {"ask": "The reviewer's own issue raises count as confirmed, and its card says so; the planner's or worker's are filed when it answers done, never when it answers disagree.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.2"},
  {"ask": "An issue that fails to file says why on this issue, and the run's record still stands.", "source": "https://github.
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`10. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan keeps every ask of the story, and all ten tests fail today because the feature is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 301 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#301](https://github.com/dokima-dev/dokima/issues/301) (the reviewer settles raises between agents and confirms issues before code files them). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Every ask is covered.** I went through the owner's words in the parent [#289](https://github.com/dokima-dev/dokima/issues/289) (agents raise and answer through the same two fields) and in this story, and found five asks. Each one maps to a criterion:
  - Routing a worker's raise for the planner (301.1).
  - Filing issues only once the reviewer confirms them (301.2).
  - A refused filing says why (301.3, the non-functional requirement).

  The planner added some precision but changed nothing the owner asked for. It says what a filed issue's title and body hold, and that 301.1 holds whether the review approves or blocks the code.
- **The tests fail for the right reason.** I ran `pytest -q tests/test_reviewer_settles.py` on the current code: all 10 fail on their own messages, because the feature is missing. None fails from a crash or a bad path. The part where the worker's raise goes to the reviewer first already works today; each test fails only on the new steps.
- **The planner's own raise is real.** It says the issue card writes "filed as an issue" for every issue raise, and `dokima/card.py:242` does exactly that. I didn't answer it: it isn't routed to the reviewer yet (that is what this story builds), so code would reject an answer naming it.

One gap I didn't block on: no test checks that a later run doesn't file the same confirmed raise a second time. Code that re-reads the whole history on every run could create duplicate issues and still pass. The criteria never promise "only once", so under the grading rules it isn't a blocker. The worker or the code review should watch for it.
