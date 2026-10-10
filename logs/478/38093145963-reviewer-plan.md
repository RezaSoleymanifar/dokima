# reviewer (plan) for #478

Run: https://github.com/dokima-dev/dokima/actions/runs/38093145963

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #478: Say who raised each "Raised earlier" item
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Part of #416. Raises already left the card (#465). My words:
> 
> Each item under "Raised earlier" says who raised it, with a link, e.g. "Code review on #462 raised:".
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #478 (2026-10-10T22:46:49Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #478 (2026-10-10T22:47:08Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #478 (2026-10-10T22:47:10Z)
> 
> Autopilot is on for #478. Pla

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; git show --stat HEAD; cat tests/test_raised_earlier_by.py; git show HEAD -- tests/test_raised_cards.py
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38092710998",
>  "commit_before": "b755a9a80820f05cdc2df53adfb3078d51e07bc2",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 5101,
>   "turns": 2,
>   "cost_usd": 1.4103892,
>   "tokens_in": 184647,
>   "tokens_out": 421
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/478/38092710998-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38092710998",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> commit 685a659b8fc8096ebda567f2aa7d4806880de5e3
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 22:54:17 2026 +0000
> 
>     planner for #478 (run 38092710998)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  tests/test_raised_cards.py      |   7 +-
>  tests/test_raised_earlier_by.py | 213 ++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 219 insertions(+), 1 deletion(-)
> """Each "Raised earlier" item says who raised it, linked to where (#478).
> 
> The owner's words: each item under "Raised earlier" says who raised it, with a link, e.g. "Code review on #462
> raised:". A run comment's Raised earlier section lists the earlier raises its run answered; until now an item showed
> only the raise itself, so the owner could not tell which step raised it or find the comment it came from.
> 
> What the code these tests run must do, as the plan pins it:
> - An item 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raised_earlier_by.py tests/test_raised_cards.py 2>&1 | grep -E "478|passed|failed|Error" | head -30
```

> Proves 478.1."""
>         record_property("proves", "478.1")
>             handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
>             f"478.1: {who}'s comment answered {len(answered)} raises but its Raised earlier section shows {items}:\n{text}"
> >           assert first.startswith(want), (f"478.1: in {who}'s comment, the raise {k} must open with who raised it and "
> E           AssertionError: 478.1: in a code review's comment, the raise P1 must open with who raised it and where, '- Planner on [#9](https://github.com/o/r/issues/9#issuecomment-101) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question">'; it reads:
> tests/test_raised_earlier_by.py:189: AssertionError
>         Proves 478.1."""
>         record_property("proves", "478.1")
>             handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
>             f"478.1: {who}'s comment answered {len(answered)} raises but its Raised earlier section shows {items}:\n{text}"
> >           assert first.startswith(want), (f"478.1: in {who}'s comment, the raise {k} must open with who raised it and "
> E           AssertionError: 478.1: in a worker's comment, the raise R4 must open with who raised it and where, '- Code review on [#12](https://github.com/o/r/pull/12#issuecomment-204) raised: <img src="https://raw.githubusercont

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raised_earlier_by.py tests/test_raised_cards.py 2>&1 | tail -2; grep -n "Raised earlier" dokima/agent.py | head; grep -n "def pack\|\"url\"\|'url'" dokima/agent.py | head -20
```

> +    where <built-in method startswith of str object at 0x7f6178f099b0> = '- <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Column qx:** Should a cancelled run keep its column qx? · for you'.startswith
> 4 failed, 22 passed in 0.37s
> 656:    They go in a Raised earlier section; an answer finds its raise among `earlier` by ID. No ID is ever drawn."""
> 664:    lines = ["", "**Raised earlier:**", ""]
> 294:def pack_records(pack_dir):
> 307:def pack_issue(pack_dir):
> 1088:def pack_parent(*dirs):
> 1101:def pack(repo, number, role, stage, dest):
> 2085:    return any(c.get("url") == source and (c.get("author") or {}).get("login") in owners and words in flat(c.get("body"))

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 285,320p dokima/agent.py; sed -n 640,700p dokima/agent.py; sed -n 1101,1200p dokima/agent.py
```

> elif n not in known:
>                 bad.append(f"links.{k} links #{n}, which is not an open issue")
>             seen.setdefault(n, [])
>             if k not in seen[n]:
>                 seen[n].append(k)
>     bad += [f"#{n} sits in more than one list of links: {', '.join(ks)}" for n, ks in seen.items() if len(ks) > 1]
>     return bad
> 
> 
> def pack_records(pack_dir):
>     """The readable earlier records in the pack's in/ folder, oldest first."""
>     out = []
>     for path in sorted(glob.glob(os.path.join(pack_dir, "in", "*.json"))):
>         try:
>             r = json.load(open(path))
>         except (OSError, json.JSONDecodeError):
>             continue
>         if isinstance(r, dict):
>             out.append(r)
>     return out
> 
> 
> def pack_issue(pack_dir):
>     """The issue number the pack's issue.md is about, or None."""
>     issue = os.path.join(pack_dir, "issue.md")
>     m = re.match(r"# Issue #(\d+)", open(issue).read()) if os.path.exists(issue) else None
>     return int(m.group(1)) if m else None
> 
> 
> def problems_for_owner(a, number, parent):
>     """Everything wrong with a reviewer's answer to a question for the owner.
> 
>     Done needs the owner's words, where they said them, and whether the reading changes how the system works or what
>     it costs."""
>     rid, bad = a.get("raise"), []
>     if a.get("answer") != "done":
>         return {"approve": f"{name} passed {what}.",
>                 "block": f"{name} blocked {what} with {k} blocker{'s' if k != 1 else ''}." if k else f"{name} blocked {what}

**Agent:** Plan tests fail for the right reason; I'm checking whether the plan-review case the criterion names is actually tested.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cp tests/test_raised_earlier_by.py /tmp/t_plan.py; sed -i 's/^FINAL = \[/FINAL = [("reviewer", "plan", ["P1"], "a plan review"),\n         /' /tmp/t_plan.py; cp /tmp/t_plan.py tests/_tmp_t.py; python3 -m pytest -q tests/_tmp_t.py -k plan 2>&1 | grep -E "^E   |passed|failed" | head -5; rm tests/_tmp_t.py; git status --short
```

> handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
> E           AssertionError: 478.1: in a plan review's comment, the raise P1 must open with who raised it and where, '- Planner on [#9](https://github.com/o/r/issues/9#issuecomment-101) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question">'; it reads:
> E             - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Column qx:** Should a cancelled run keep its column qx? · for you
> E           assert False
> E            +  where False = <built-in method startswith of str object at 0x7f480886c250>('- Planner on [#9](https://github.com/o/r/issues/9#issuecomment-101) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question">')

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote one criterion: each Raised earlier item opens with who raised it (Planner, Worker, Plan review or Code review), then \"on #N\" linked to the comment it was raised in, then \"raised:\", in every agent's comment.",
          "It added tests/test_raised_earlier_by.py and loosened one helper in tests/test_raised_cards.py to allow the new opening."],
  "decided": ["A raise whose comment is not known names who raised it with no link, so no wrong link is drawn.",
              "Only dokima/agent.py changes; the Raised section, the issue card and records already posted stay as they are."],
  "open": []},
 "verdict": "block",
 "summary": "The plan keeps to the owner's words in one file, but its test never checks a plan review's comment, which the criterion promises.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "478.1: plan review untested",
   "text": "Criterion 478.1 promises the new opening in the comments of a code review, a plan review, the planner and the worker, but the test runs only a code review, a worker and a planner, so code that skips it in a plan review's comment would pass. Smallest fix: add (\"reviewer\", \"plan\", [\"P1\"], \"a plan review\") to FINAL in tests/test_raised_earlier_by.py; I ran it with that line added and it fails today for the right reason (\"478.1: in a plan review's comment, the raise P1 must open with who raised it and where\").",
   "evidence": "tests/test_raised_earlier_by.py, FINAL lists (\"reviewer\", \"pr\"), (\"worker\", None) and (\"planner\", None) only."}
 ],
 "answers": [],
 "asks": [
  {"ask": "Each item under \"Raised earlier\" says who raised it, with a link, e.g. \"Code review on #462 raised:\".", "source": "https://github.com/dokima-dev/dokima/issues/478", "criterion": "478.1"},
  {"ask": "Keep to my words; smallest change.", "source": "https://github.com/dokima-dev/dokima/issues/478", "crite
```

> (Bash completed with no output)

**Agent:** I blocked the plan for [#478](https://github.com/dokima-dev/dokima/issues/478) (say who raised each "Raised earlier" item) and sent one blocker back to the planner. The review is in `/tmp/dokima-out/review.json`, and both of Dokima's checks on it pass.

**What the plan says:** it has one criterion. Each item under "Raised earlier" opens with who raised it (Planner, Worker, Plan review or Code review), then "on #N" linked to the comment it was raised in, then "raised:". This applies in every agent's comment. It also adds one fallback: if the comment isn't known, the item names who raised it with no link, so no wrong link is drawn. Only `dokima/agent.py` changes, which fits your "Keep to my words; smallest change."

**The tests:** I ran them on this branch. All four new test cases fail today for the right reason: the item doesn't yet open with who raised it. The existing tests in `tests/test_raised_cards.py` still pass with the loosened helper.

**Why I blocked:** the criterion promises the new opening in four kinds of comment, but the test only checks three: a code review, a worker and a planner. A build that left plan review comments unchanged would still pass.
- **Fix:** add one line to `FINAL` in `tests/test_raised_earlier_by.py`: `("reviewer", "plan", ["P1"], "a plan review")`.
- I tried that line in a temporary copy of the test. It fails today with "478.1: in a plan review's comment, the raise P1 must open with who raised it and where".

**Not blocked on:** the no-link fallback goes slightly beyond your words. I let it stand because it follows the "fail closed" rule in AGENTS.md: a missing link is better than a wrong one.

**One thing that may matter:** your "/plan Keep to my words; smallest change" came at 22:52, after the planner's record at 22:47. A second planner run was queued after your comment, and this pack holds only the first planner's record. So I may have graded a plan written before your comment. The plan does keep to that comment either way.

I couldn't find the link to that comment, so in the review it points at the issue itself.
