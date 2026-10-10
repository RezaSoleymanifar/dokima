# reviewer (plan) for #478

Run: https://github.com/dokima-dev/dokima/actions/runs/38093317903

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
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
> 02-reviewer-plan.json
> 03-planner.json
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
> Autopilo

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -4 --stat; git diff b755a9a --stat; cat tests/test_raised_earlier_by.py; git diff b755a9a -- tests/test_raised_cards.py; python3 -c "
import json;[print(json.dumps(json.load(open(f'/tmp/pack/in/{f}')),indent=1)[:3000]) for f in ['01-planner.json','02-reviewer-plan.json']]"
```

> bab9b7d planner for #478 (run 38093254869)
>  tests/test_raised_earlier_by.py | 1 +
>  1 file changed, 1 insertion(+)
> 685a659 planner for #478 (run 38092710998)
>  tests/test_raised_cards.py      |   7 +-
>  tests/test_raised_earlier_by.py | 213 ++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 219 insertions(+), 1 deletion(-)
> b755a9a Raises come off the card; the status line says what needs the owner and links to where it was raised (#465)
>  docs/rendered/455.json           |  12 ++
>  dokima/card.py                   |  37 ++--
>  tests/github_rendering.json      |  10 +
>  tests/record_rendering.py        |   9 +-
>  tests/test_card_raises_status.py | 432 +++++++++++++++++++++++++++++++++++++++
>  tests/test_raised_cards.py       |  64 +-----
>  6 files changed, 493 insertions(+), 71 deletions(-)
> d674b58 Every commit Dokima makes names Reza as co-author (#459) (#474)
>  .github/workflows/agent.yml   | 2 +-
>  .github/workflows/planner.yml | 2 +-
>  .github/workflows/wiki.yml    | 2 +-
>  .github/workflows/worker.yml  | 2 +-
>  4 files changed, 4 insertions(+), 4 deletions(-)
>  tests/test_raised_cards.py      |   7 +-
>  tests/test_raised_earlier_by.py | 214 ++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 220 insertions(+), 1 deletion(-)
> """Each "Raised earlier" item says who raised it, linked to where (#478).
> 
> The owner's words: each item under "Raised earlier" says who raised it, with a link, e.g. "Code review on #462
> raised:". A run comment's Raised earlier section lists the earlier r

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raised_earlier_by.py 2>&1 | grep -E "^(FAILED|E  .*478)|passed|failed" | head -20; python3 -m pytest -q tests/test_raised_cards.py 2>&1 | tail -2; grep -n "Raised earlier" dokima/*.py | head; grep -n '"url"' dokima/agent.py | head
```

> handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
> E           AssertionError: 478.1: in a code review's comment, the raise P1 must open with who raised it and where, '- Planner on [#9](https://github.com/o/r/issues/9#issuecomment-101) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question">'; it reads:
>             handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
> E           AssertionError: 478.1: in a plan review's comment, the raise P1 must open with who raised it and where, '- Planner on [#9](https://github.com/o/r/issues/9#issuecomment-101) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question">'; it reads:
>             handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", raises=[], answers=answers)
> E           AssertionError: 478.1: in a worker's comment, the raise R4 must open with who raised it and where, '- Code review on [#12](https://github.com/o/r/pull/12#issuecomment-204) raised: <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker">'; it reads:
>             handback = dict(summary="Sped it up.", criteria={f"{N}.1": "fast"}, evidence="3 passed", r

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def pack\b\|def pack(" -A60 dokima/agent.py | grep -n "url\|in/\|json.dump\|records" | head -20; sed -n 640,700p dokima/agent.py
```

> 2:1102-    """Build the starting pack from GitHub's records: the issue and its PRs' conversation, every agent record so far,
> 6:1106-    recs = records(items)
> 9:1109-    json.dump({"number": parent_of(repo, number)}, open(os.path.join(dest, "parent.json"), "w"))
> 11:1111-        json.dump(listed, open(os.path.join(dest, "open_issues.json"), "w"), indent=1)
> 13:1113-    json.dump(raises_for(recs, role), open(os.path.join(dest, "open_blockers.json"), "w"), indent=1)
> 17:1117-        json.dump(r, open(os.path.join(dest, "in", name), "w"), indent=1)
> 22:1122-        json.dump(plan["handback"], open(os.path.join(dest, "plan.json"), "w"), indent=1)
>         return {"approve": f"{name} passed {what}.",
>                 "block": f"{name} blocked {what} with {k} blocker{'s' if k != 1 else ''}." if k else f"{name} blocked {what}.",
>                 "escalate": f"{name} escalated {what} to you."}.get(h.get("verdict"), f"{name} judged {what}.")
>     if role == "split":
>         return f"Code filed the split as {len(h.get('stories') or [])} stories."
>     return h["summary"].strip() if filled(h.get("summary")) else ""
> 
> 
> def record_fold(rec):
>     """The full JSON record, always the last fold of a run comment: later packs are built from it."""
>     return ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>"]
> 
> 
> def answered_lines(repo, rec, earlier):
>     """A passed run's answers to earlier raises, drawn the same for every agent.
> 
>     They go 

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added a plan review's comment to the test of 478.1, as the last plan review asked; the test now runs a code review, a plan review, a worker and a planner."],
  "decided": ["The plan is otherwise unchanged: one criterion, one fail-closed rule for a raise whose comment is not known, and only dokima/agent.py changes."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps to the owner's words in one file, and its tests now check every kind of run comment and fail today because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Each item under \"Raised earlier\" says who raised it, with a link, e.g. \"Code review on #462 raised:\".", "source": "https://github.com/dokima-dev/dokima/issues/478", "criterion": "478.1"},
  {"ask": "Keep to my words; smallest change.", "source": "https://github.com/dokima-dev/dokima/issues/478", "criterion": "478.1"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 478 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan keeps to the owner's words in one file, and its tests now cover every kind of run comment and fail today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 478 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> exit 0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan keeps to the owner's words in one file; its tests cover every kind of run comment and fail today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 478 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> exit 0

**Agent:** I approved the plan for issue [#478](https://github.com/dokima-dev/dokima/issues/478) (say who raised each "Raised earlier" item). Both hand-back checks pass on `/tmp/dokima-out/review.json`.

- **Last round's blocker is fixed:** the planner added the missing plan-review case to `tests/test_raised_earlier_by.py`. The test for 478.1 now covers a code review's, a plan review's, a worker's and the planner's comments.
- **The new tests fail today for the right reason:** all 5 fail because the "who raised it and where" opening is missing, not because of a crash or a bad path.
  - 478.1 expects, for example, `- Planner on [#9](…#issuecomment-101) raised:`.
  - 478.2 expects `- Planner raised:` with no link when the comment isn't known.
- **The changed helper still holds:** the helper in `tests/test_raised_cards.py` now allows the new opening before the raise, and those 22 tests still pass.
- **Your asks are covered:** both your issue text and your "Keep to my words; smallest change." are carried by 478.1. The plan changes only `dokima/agent.py` and adds nothing outside your words beyond one rule: if the comment a raise came from isn't known, the item names who raised it and shows no link.

No blockers, questions or outside problems raised.
