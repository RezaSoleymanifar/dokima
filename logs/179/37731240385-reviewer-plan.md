# reviewer (plan) for #179

Run: https://github.com/dokima-dev/dokima/actions/runs/37731240385

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #179: The owner's ask is kept below a fixed marker and never rewritten
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 1</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners can trust that whatever code redraws on an issue, their original ask below the marker stays exactly as they wrote it.
> 
> **Context:** Split rules R1, R2 and R3: #143 holds several independent goals (body protection, the issue/PR card's content, its status and children, run cards, a backfill), needs well over five criteria, and spans dokima/planner.py, dokima/card.py, dokima/agent.py, dokima/roles/ and AGENTS.md. This story keeps the promise moved in from #48. Today dokima/planner.py render() folds the owner's text between <!-- dokima-original --> and <!-- /dokima-original --> and original() reads it back, but dokima/card.py main() rewrites the whole body via issue_body(card, notes) from plan.parse(), with no check that the owner's part survived and nothing that refuses a save. AGENTS.md 'The issue body' marks the check-and-refuse part as planned. Make one helper own the body: card above the marker, owner's ask f

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff ad72396 --stat; grep -n "def test_the_planner" -A80 tests/test_body.py | head -220
```

> tests/test_body.py | 454 +++++++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_card.py |   1 -
>  2 files changed, 454 insertions(+), 1 deletion(-)
> 337:def test_the_planner_refuses_rather_than_change_the_owner_part(record_property, monkeypatch, tmp_path, github):
> 338-    """When the planner writes its plan, it never saves a body that would change the owner's part; it comments why.
> 339-
> 340-    Runs the planner's post, the step that writes a plan into the issue, on an issue where the helper finds the owner's
> 341-    part would change, and checks the body is not written and the issue gets a comment carrying the helper's reason.
> 342-    Beside it, a good post on the same issue saves the plan above the marker with the owner's ask unchanged."""
> 343-    record_property("proves", "179.3")
> 344-    body = helper("179.3")
> 345-    current = body.redraw("My ask.", PLAN_TOP)
> 346-    run_planner_post(monkeypatch, tmp_path / "good", github, current)
> 347-    assert len(github.saves) == 1, f"179.3: a good plan post made {len(github.saves)} saves of the issue body, not one"
> 348-    assert body.ask(github.saves[0]) == "My ask.", "179.3: a good plan post changed the owner's ask"
> 349-    assert "The issue shows a card on top." in github.saves[0].split(body.MARKER, 1)[0], \
> 350-        "179.3: a good plan post did not write the plan above the marker"
> 351-    assert not any(REASON in (t or "") for _, t in github.comments), "179.3: a good plan post posted a refusal"
> 352-    github.saves.cl

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,140p tests/test_body.py; grep -n "def run_planner_post\|def refuse" -A40 tests/test_body.py | head -100
```

> """The issue body: code's card above one fixed marker, the owner's ask folded below it, never rewritten.
> 
> Issue #179. One helper, dokima/body.py, owns the issue body:
> 
>     MARKER                      the fixed marker that splits the body in two
>     ask(body)                   the owner's part below the first marker, byte for byte (the whole body when there
>                                 is no marker yet)
>     redraw(body, top)           the new body: `top` above the marker, the owner's part folded below it;
>                                 raises Refused(reason) when the owner's part would change
>     save(repo, number, current, top)
>                                 saves redraw(current, top) on the issue and returns True, or, when refused,
>                                 leaves the body alone, comments the reason on the issue and returns False
>     Refused                     the exception redraw raises, its message saying why
> 
> Every code path that redraws the issue body goes through it: the card (dokima/card.py main) and the planner's
> post (dokima/planner.py render, saved by planner.main "post"). GitHub is faked in every test by a recorder standing in
> for the `gh` calls; the planner's post runs inside a temp git repo holding the plan's tests, as a real run does.
> """
> import json
> import os
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import card, plan, planner  # noqa: E402
> 
> REPO = "o/r"
> NUMBER = 40
> 
> # 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_body.py 2>&1 | grep -E "FAILED|passed|failed" | head -30; python -m pytest -q tests/ 2>&1 | tail -3; sed -n 330,380p dokima/planner.py
```

> FAILED tests/test_body.py::test_body_is_the_card_above_one_marker_and_the_ask_folded_below - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_marker_is_the_same_after_every_redraw - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_writes_its_card_above_the_marker - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_owner_part_is_byte_for_byte_the_same_after_many_redraws - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_never_changes_the_owner_part - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_replanning_never_changes_the_owner_part - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_a_redraw_that_would_change_the_owner_part_is_refused - Failed: 179.3: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_a_refused_save_leaves_the_body_and_comments_why - Failed: 179.3: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_refuses_rather_than_change_the_owner_part - Failed: 179.3: dokima/body.py, the on

`5. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && cat > dokima/body.py <<'EOF'
import os, subprocess
MARKER = "<!-- dokima-ask -->"
OPEN, CLOSE = "<details><summary>Original ask</summary>\n\n", "\n\n</details>\n"
class Refused(Exception): pass
def gh(*a, input=None):
    return subprocess.run(["gh", *a], input=input, capture_output=True, text=True, check=True).stdout
def ask(body):
    if MARKER not in body: return body
    below = body.split(MARKER, 1)[1]
    s = below.index(OPEN) + len(OPEN); e = below.rindex(CLOSE)
    return below[s:e]
def redraw(current, top):
    if MARKER in top: raise Refused("the owner's part below the marker would change")
    old = ask(current)
    new = top.rstrip("\n") + "\n\n" + MARKER + "\n" + OPEN + old + CLOSE
    if ask(new) != old: raise Refused("the owner's part below the marker would change")
    return new
def save(repo, number, current, top):
    try:
        new = redraw(current, top)
    except Refused as e:
        gh("issue", "comment", str(number), "-R", repo, "--body", f"Refused: {e}")
        return False
    gh("issue", "edit", str(number), "-R", repo, "--body-file", "-", input=new)
    return True
EOF
python -m pytest -q tests/test_body.py 2>&1 | grep -E "^(FAILED|E )|passed|failed" | head -40
```

> E       ValueError: substring not found
> E       ValueError: substring not found
> E       AssertionError: 179.2: the first plan changed the owner's ask
> E       assert '- [ ] Object...n</details>\n' == '\r\n\r\nPlea...ne\r\n\r\n   '
> E         
> E         - 
> E         - 
> E         + - [ ] Objective: Slow calls return a job id
> E         +   - [ ] Acceptance criteria: A slow call returns a job id within 20 s
> E         +     Verified by: no test
> E         + 
> E         + **Scope:**
> E         + - `dokima/jobs.py`
> E         + 
> E         + <details><summary>Original issue</summary>
> E         + 
> E         + <!-- dokima-original -->
> E         - Please make the card keep my words.  
> E         ?                                      -
> E         + > Please make the card keep my words.  
> E         ? ++
> E         - - [ ] Goal: an old goal
> E         ?                        -
> E         + > - [ ] Goal: an old goal
> E         ? ++
> E         -   - [ ] Done when: an old criterion
> E         ?                                    -
> E         + >   - [ ] Done when: an old criterion
> E         ? ++
> E         -     Verified by: nothing
> E         ?                         -
> E         + >     Verified by: nothing
> E         ? ++
> E         - <!-- dokima-card -->
> E         ?                     -
> E         + > <!-- dokima-card -->
> E         ? ++
> E         - </details>
> E         ?           -
> E         + > </details>
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** I'm checking that the planner's two new tests can pass once the work is built. I'm using a throwaway copy with a rough stand-in helper.

`6. Bash`
```
cd /tmp/rv && python -m pytest -q tests/test_body.py -k planner 2>&1 | grep -E "^(FAILED|E  )|passed|failed" | head; python - <<'EOF'
import re
p=open('dokima/planner.py').read()
p=p.replace('''            gh("issue", "edit", number, "-R", repo, "--body-file", "-", input=render(number, body, result, dict(proving(tc), **declared_by_test(result["declared"])), older))''','''            from dokima import body as B
            top = render(number, "", result, dict(proving(tc), **declared_by_test(result["declared"])), older)
            if not B.save(repo, number, body, top):
                return 1''')
open('dokima/planner.py','w').write(p)
EOF
python -m pytest -q tests/test_body.py -k planner 2>&1 | grep -E "^(FAILED|E  )|passed|failed" | head
```

> E       ValueError: substring not found
> E       AssertionError: 179.5: expected one refusal comment on the issue, got 0
> E       assert 0 == 1
> E        +  where 0 = len([])
> FAILED tests/test_body.py::test_the_planner_refuses_rather_than_change_the_owner_part - ValueError: substring not found
> FAILED tests/test_body.py::test_the_planner_posts_its_refusal_on_the_issue - AssertionError: 179.5: expected one refusal comment on the issue, got 0
> 2 failed, 14 deselected in 0.11s
> 2 passed, 14 deselected in 0.65s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** B1 is fixed: both new planner tests run the real planner post, fail today because the feature is missing, and pass once it's wired to the helper. Writing the approval.

`7. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added two tests that run the planner's own save of a plan on a faked GitHub: one for 179.3, one for 179.5. A good save writes one body with the owner's ask unchanged; a refused save writes nothing and posts one comment with the reason on the issue.",
          "Kept the four criteria, the scope and the two questions as they were."],
  "decided": ["Both the card and the planner save the issue body through the one helper, dokima/body.py."],
  "open": ["Whether the issue's wording counts as asking to change dokima/card.py; the plan assumes it does and the owner went on with that assumption."]},
 "verdict": "approve",
 "summary": "The plan now proves that both the card and the planner refuse to change the owner's ask and say why on the issue; every criterion has tests that fail today only because the helper is missing.",
 "blockers": [],
 "notes": [
  {"text": "Every direct refusal test still makes the refusal happen the same way, with a card that contains the marker, and the card and planner tests force the refusal by replacing the helper's redraw. A helper that only looks for the marker in the new card, without comparing the owner's part before and after, would still pass. One more case where the owner's part reads back differently would prove the comparison itself.",
   "evidence": "tests/test_body.py:171-175 refuse() replaces body.redraw; test_a_redraw_that_would_change_the_owner_part_is_refused, test_a_refused_save_leaves_the_body_and_comments_why and test_a_refusal_is_a_comment_on_the_issue all use a card quoting body.MARKER."},
  {"text": "The refusal tests replace body.redraw on the module, so the worker must call it as body.redraw from save, the card and the planner. A copy taken with 'from dokima.body import redraw' would skip the forced refusal.",
   "evidence": "tests/test_body.py:175 monkeypatch.setattr(body, \"redraw\", refused)."}
 ],
 "outside_plan": [],

```

> rc=0

**Agent:** I approved the plan for #179. The one earlier blocker (B1) is fixed, and the review is saved in `/tmp/dokima-out/review.json`. It passes both hand-back checks.

- **B1 is resolved.** The planner added two tests that run the planner's own save of a plan, using a stand-in for GitHub. One is for 179.3 and one for 179.5:
  - **Normal save:** the body is saved once, the plan sits above the marker, the owner's ask is unchanged, and no refusal comment is posted.
  - **Refused save:** nothing is saved, and one comment with the reason lands on the issue.
- **The two new tests can pass.** In a throwaway copy I added a rough stand-in helper and pointed the planner's save at it; both tests passed. On today's code they fail because the planner still saves the body directly.
- **The new tests fail for the right reason today.** All 16 tests in `tests/test_body.py` fail only with "dokima/body.py … does not exist yet". The other 270 tests in the suite pass.

The review carries two notes; neither blocks:
- **The refusal is only ever triggered one way.** In the tests that call the helper directly, it's always a card that contains the marker. The card and planner tests skip the comparison by forcing the refusal. A helper that only looked for the marker in the new card, without comparing the owner's part before and after, would still pass.
- **The tests force a refusal by replacing the helper's redraw function.** So the worker has to call it through the helper (`body.redraw`). If the code keeps its own copy of the function, the forced refusal never happens.

The question about whether this issue counts as asking to change `dokima/card.py` is still open. You went on with the planner's assumption that it does.

The next step is yours: `/work` approves the plan and starts the build.
