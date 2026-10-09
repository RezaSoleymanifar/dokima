# reviewer (plan) for #298

Run: https://github.com/dokima-dev/dokima/actions/runs/37881700063

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #298: Three kinds of raise and one table of who raises to whom, checked by code
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #298](https://github.com/dokima-dev/dokima/issues/298)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 1</summary>
> 
> **Part of:** #289 Every agent raises things and answers them through the same two fields
> 
> **User story:** The owner knows every judgment an agent raises is a question, a blocker

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_raises.py; ls dokima/raises.py; python -m pytest -q tests/test_raises.py 2>&1 | tail -30
```

> """Three kinds of raise and one table of who raises to whom (#298).
> 
> The owner wants every judgment an agent raises to be a question, a blocker or an issue, sent only where a fixed table
> in code allows, stamped by code with who raised it and an ID, and answered by whoever it was sent to. This story adds
> that shared model alone, in dokima/raises.py; no hand-back, card or prompt changes yet (story 3, #300, wires it in).
> 
> The module these tests run, as the plan fixes it:
> - `KINDS`: the tuple ("question", "blocker", "issue").
> - `TABLE`: a read-only mapping from each raiser to the tuple of whom it may send a question or blocker:
>   planner -> owner; worker -> planner; reviewer -> planner, worker, owner. An issue is for no one.
> - `check_raises(role, raises)`: the problems with the raises an agent of that role wrote, as plain sentences; empty
>   when they are fine. A raise is {"kind", "to", "label", "text", "evidence"}; label and evidence are optional and an
>   issue has no "to".
> - `sent_to(raise_)`: the one who must answer a raise first: its "to", except the reviewer for a worker's raise to the
>   planner (it goes through the reviewer); None for an issue.
> - `stamp(role, raises, taken)`: copies of the raises with "raised_by" set to the role and an "id" unique among
>   `taken` (the IDs already on the issue) and each other.
> - `check_answers(role, answers, open_raises)`: the problems with an agent's answers, each {"raise": ID, "answer":
>   "done" or "disagree", "why": text}, given the stampe

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; rm -rf /tmp/rv && mkdir /tmp/rv && cp -r dokima tests /tmp/rv/ && cat > /tmp/rv/dokima/raises.py <<'EOF'
from types import MappingProxyType
import itertools
KINDS = ("question", "blocker", "issue")
TABLE = MappingProxyType({"planner": ("owner",), "worker": ("planner",), "reviewer": ("planner", "worker", "owner")})
ALLOWED = {"kind", "to", "label", "text", "evidence"}

def check_raises(role, raises):
    out = []
    for i, r in enumerate(raises, 1):
        for f in ("raised_by", "id"):
            if f in r:
                out.append(f"raise {i}: {f} is written by code, not the agent")
        for f in r:
            if f not in ALLOWED and f not in ("raised_by", "id"):
                out.append(f"raise {i}: unknown field {f}")
        k = r.get("kind")
        if k not in KINDS:
            out.append(f"raise {i}: kind {k!r} is not one of question, blocker or issue")
            continue
        to = r.get("to")
        if k == "issue":
            if to:
                out.append(f"raise {i}: an issue is for no one, not {to}")
        elif not to:
            out.append(f"raise {i}: the {role}'s {k} names no one")
        elif to not in TABLE.get(role, ()):
            out.append(f"raise {i}: the {role}'s {k} to {to} is outside the table")
    return out

def sent_to(r):
    if r["kind"] == "issue":
        return None
    if r["raised_by"] == "worker" and r["to"] == "planner":
        return "reviewer"
    return r["to"]

def stamp(role, raises, taken):
    used = set(taken); out = []; n = itertools.count(1)
    for r in raises:
        while (i := f"r{next(n)}") in used: pass
        used.add(i); out.append({**r, "raised_by": role, "id": i})
    return out

def check_answers(role, answers, open_raises):
    ids = {r["id"] for r in open_raises}; out = []; answered = set()
    for i, a in enumerate(answers, 1):
        if not isinstance(a, dict) or a.get("raise") not in ids or a.get("answer") not
```

> commit 8a2e8ed748569995389c321246a51dfafe77202d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 03:58:06 2026 +0000
> 
>     planner for #298 (run 37881386661)
> 
>  tests/test_raises.py | 329 +++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 329 insertions(+)
> ............                                                             [100%]
> 12 passed in 0.04s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner wrote four acceptance criteria and one non-functional requirement for one new module, dokima/raises.py, with twelve tests in tests/test_raises.py."],
  "decided": ["A worker's question or blocker for the planner is answered first by the reviewer; an issue sent to anyone is rejected.", "A bad answer is named by its place in the list (answer 2), and a skipped raise by its ID.", "No hand-back, card or prompt changes in this story; those stay with #299 to #302."],
  "open": ["The plan has no questions for the owner."]
 },
 "verdict": "approve",
 "summary": "The plan keeps every criterion of the story as written, and each of its twelve tests fails today only because dokima/raises.py does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "No test checks that an answer to a raise that was not sent to this agent, or a second answer to the same raise, is rejected; the story does not ask for either, so it is left open for #300.", "evidence": "tests/test_raises.py::test_a_malformed_answer_is_rejected_naming_it uses only a missing ID (zz9) as the wrong-ID case."},
  {"text": "Ran all twelve tests on this branch: 12 failed, each with 'dokima/raises.py does not exist yet'. Against a small sketch of the module in a scratch copy, all twelve passed, so the tests can be met.", "evidence": "pytest -q tests/test_raises.py -> 12 failed in 0.19s; scratch copy in /tmp/rv -> 12 passed"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The checker rejects a raise of any kind but question, blocker or issue, naming the kind and the three allowed; each of the three passes. A raise may carry a short label such as weak test or missing ask; any label passes, and two raises that differ only in label are checked and routed the same.", "source": "https://github.com/dokima-dev/dokima/issues/298", "criterion": "298.1"},
  {"ask": "The checker rej
```

> 0

**Agent:** I approved the plan for #298. Both hand-back checks passed, and the review is in `/tmp/dokima-out/review.json`.

- **Criteria:** All four acceptance criteria and the non-functional requirement come straight from the story's own words, mapped to 298.1–298.5. The plan adds one rule the story only implies: an issue sent to someone is rejected, because "an issue is for no one". The plan has no questions for the owner and no blockers were open from earlier rounds.
- **Tests fail today for the right reason:** I ran the 12 tests in `tests/test_raises.py` and all 12 failed with "dokima/raises.py does not exist yet".
- **Tests can be met:** I wrote a rough version of the module in a scratch copy of the repo, outside the repo itself, and all 12 tests passed against it.
- **Tests cover both directions:** Each criterion has tests that reject the bad case and pass the good case. That covers every row of the table and every pair outside it, a raise for no one, labels that change nothing, IDs already used on the issue, a raiser or ID the agent writes itself, each kind of malformed answer, and a raise left unanswered. A worker's raise to the planner goes to the reviewer first.

I left two notes, neither a blocker:
- No test checks that answering a raise sent to someone else, or answering the same raise twice, is rejected. The story doesn't ask for either, so I left it for #300.
- The test run results above.
