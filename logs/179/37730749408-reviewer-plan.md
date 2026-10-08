# reviewer (plan) for #179

Run: https://github.com/dokima-dev/dokima/actions/runs/37730749408

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
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
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests/test_card.py; cat tests/test_body.py
```

> commit 1be32e5ea3e0a4f222305c5adf1a3505e4673ce7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:03:09 2026 +0000
> 
>     planner for #179 (run 37729957222)
> 
>  tests/test_body.py | 369 +++++++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_card.py |   1 -
>  2 files changed, 369 insertions(+), 1 deletion(-)
> commit 1be32e5ea3e0a4f222305c5adf1a3505e4673ce7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:03:09 2026 +0000
> 
>     planner for #179 (run 37729957222)
> 
> diff --git a/tests/test_card.py b/tests/test_card.py
> index 3343a6d..1764215 100644
> --- a/tests/test_card.py
> +++ b/tests/test_card.py
> @@ -136,7 +136,6 @@ def test_same_card_on_issue_and_pr_and_only_icons_change(record_property):
>      assert plan.parse(issue_text) == plan.parse(later) == WORDS
>      assert card.pr_body(render(), "Closes #40.\n\nSome prose.") == render() + "\n\nCloses #40"
>      src = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "card.py")).read()
> -    assert 'f"repos/{repo}/issues/{number}", "-F", "body=@issue.md"' in src
>      assert 'f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md"' in src
>      yml = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "card.yml")).read()
>      assert "types: [opened, edited]" in yml and "github.event.sender.type != 'Bot'" in yml
> """The issue body: code's card above one fixed marker, the owner's ask folded below it

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_body.py 2>&1 | tail -25; python -m pytest -q 2>&1 | tail -3; grep -n "def main" -A60 dokima/card.py | head -100
```

> def helper(k):
>         """The body helper, or a plain failure naming criterion k when it does not exist yet."""
>         try:
>             from dokima import body
>         except ImportError:
> >           pytest.fail(f"{k}: dokima/body.py, the one helper that owns the issue body, does not exist yet")
> E           Failed: 179.5: dokima/body.py, the one helper that owns the issue body, does not exist yet
> 
> /home/runner/work/dokima/dokima/tests/test_body.py:53: Failed
> =========================== short test summary info ============================
> FAILED tests/test_body.py::test_body_is_the_card_above_one_marker_and_the_ask_folded_below - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_marker_is_the_same_after_every_redraw - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_writes_its_card_above_the_marker - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_owner_part_is_byte_for_byte_the_same_after_many_redraws - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_never_changes_the_owner_part - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_replanning_never_changes_the_owner_part - Failed: 179.2: doki

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def render\|def original\|dokima-original\|PATCH\|issue edit\|body=@\|def gh\|^from\|^import" dokima/planner.py dokima/card.py dokima/plan.py; grep -rn "planner.render\|render(" dokima/*.py | grep -v "def " | head -20
```

> dokima/plan.py:15:import difflib
> dokima/plan.py:16:import json
> dokima/plan.py:17:import os
> dokima/plan.py:18:import re
> dokima/plan.py:19:import subprocess
> dokima/plan.py:20:import sys
> dokima/plan.py:154:def gh(*args):
> dokima/card.py:5:from that criterion's check. It computes no verdicts itself: a pass appears only
> dokima/card.py:13:import json
> dokima/card.py:14:import os
> dokima/card.py:15:import re
> dokima/card.py:16:import subprocess
> dokima/card.py:17:import sys
> dokima/card.py:20:from dokima import plan  # noqa: E402
> dokima/card.py:107:def render(repo, issue, words, pr, check_runs, worker, page="issue"):
> dokima/card.py:145:def gh(*args):
> dokima/card.py:195:    gh("api", "-X", "PATCH", f"repos/{repo}/issues/{number}", "-F", "body=@issue.md")
> dokima/card.py:200:        gh("api", "-X", "PATCH", f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md")
> dokima/planner.py:14:import json
> dokima/planner.py:15:import os
> dokima/planner.py:16:import re
> dokima/planner.py:17:import subprocess
> dokima/planner.py:18:import sys
> dokima/planner.py:20:from dokima.checks import PROVES, TEST_DEF
> dokima/planner.py:21:from dokima.agent import problems_questions  # noqa: E402
> dokima/planner.py:23:ORIGINAL_START = "<!-- dokima-original -->"
> dokima/planner.py:24:ORIGINAL_END = "<!-- /dokima-original -->"
> dokima/planner.py:271:def original(body):
> dokima/planner.py:281:def render(number, body, plan, tags, older=()):
> dokima/planner.py:311:def gh(*args, **kw):
> dokima/card.py:194:        f.write(issue_body(re

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 260,380p dokima/planner.py; grep -rn "planner.py\|planner import\|planner\.main\|dokima.planner" .github/workflows dokima | head
```

> proven |= {k for k, ts in declared.items() if ts}
>     out += [f"criterion {k} has no test" for k in sorted(keys - proven)]
>     out += [f"{t} proves {k}, which is not a criterion of this plan" for t, ks in tc["added"].items() for k in ks if k not in keys]
>     out += [f"{t} now proves {k}, which is neither a criterion of this plan nor what it proved before"
>             for t, (old, new) in tc["changed"].items() for k in new if k not in keys and k not in old]
>     older = [t for t in tc["changed"] if not set(tc["changed"][t][0]) <= keys] + list(tc["deleted"])
>     out += [f"{t} is an older test the planner changed or deleted, with no reason in test_changes"
>             for t in older if t not in plan["test_changes"]]
>     return out
> 
> 
> def original(body):
>     """The owner's own text: kept from an earlier plan's fold, else the body as it is."""
>     body = body or ""
>     if ORIGINAL_START in body and ORIGINAL_END in body:
>         inner = body.split(ORIGINAL_START, 1)[1].split(ORIGINAL_END, 1)[0]
>         lines = [l for l in inner.splitlines() if l.startswith(">")]
>         return "\n".join(l[2:] if l.startswith("> ") else l[1:] for l in lines)
>     return body.strip()
> 
> 
> def render(number, body, plan, tags, older=()):
>     """The issue body for a plan, in the format dokima.plan reads, with the owner's text folded below."""
>     lines = [f"- [ ] Objective: {plan['objective'].strip()}"]
>     for k, c in enumerate(plan["criteria"], 1):
>         tests = sorted(t for t, ks in tags.items() if f"{nu

**Agent:** Plan's tests all fail today for the right reason; now checking whether every code path that rewrites the issue body is covered.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -n "issue\", \"edit\|PATCH\|--body-file\|issues/{" dokima/*.py | grep -v "comment"; sed -n 100,125p .github/workflows/planner.yml; head -20 .github/workflows/planner.yml
```

> agent.yml
> assign.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> wiki.yml
> worker.yml
> dokima/plan.py:166:    events = json.loads(gh("api", f"repos/{repo}/issues/{number}/events?per_page=100", "--paginate"))
> dokima/card.py:195:    gh("api", "-X", "PATCH", f"repos/{repo}/issues/{number}", "-F", "body=@issue.md")
> dokima/card.py:200:        gh("api", "-X", "PATCH", f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md")
> dokima/agent.py:177:        node = json.loads(gh("api", f"repos/{repo}/issues/{number}"))["id"]
> dokima/agent.py:178:        gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues", "-F", f"sub_issue_id={node}")
> dokima/agent.py:185:                gh("api", "-X", "POST", f"repos/{repo}/issues/{f['issue']}/dependencies/blocked_by", "-F", f"issue_id={by_story[d]['id']}")
> dokima/planner.py:38:    return f"{server}/{os.environ.get('GITHUB_REPOSITORY', '')}/issues/{number}"
> dokima/planner.py:363:            gh("issue", "edit", number, "-R", repo, "--body-file", "-", input=render(number, body, result, dict(proving(tc), **declared_by_test(result["declared"])), older))
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Push the tests
>         if: success() && steps.who.outputs.ok == 'true'
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           SLUG: ${{ steps.app.outputs.app-slug }}
>           N: ${{ github.event.issue.number }}
>         run: |
>           [ -f /tmp/dokima-out/plan.json ] || exit 0
>      

**Agent:** I'm blocking on one gap; writing the review now.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a four-criterion plan for keeping the owner's ask below one fixed marker, with 14 new tests in tests/test_body.py that all fail today because the body helper does not exist yet.",
          "Dropped one source-reading line from an older card test, with a reason."],
  "decided": ["One new helper, dokima/body.py, saves the issue body for both the card and the planner.",
              "An issue with an older layout keeps its whole existing body below the marker, as it is; the owner went on with this assumption."],
  "open": ["Whether the issue's wording counts as asking to change dokima/card.py; the plan assumes it does and the owner went on with that assumption."]},
 "verdict": "block",
 "summary": "The plan says every redraw by the card or the planner is checked, but only the card is shown to refuse and comment; the planner's own save of the issue body could still overwrite the owner's ask or fail silently.",
 "blockers": [
  {"id": "B1", "criterion": "179.3", "test": "tests/test_body.py::test_the_card_refuses_rather_than_change_the_owner_part",
   "problem": "179.2 names two code paths that redraw the issue body, the card's and the planner's, and 179.3 and 179.5 promise that code refuses, leaves the body alone and comments why. Only the card's path is tested for that. The planner writes the issue body itself in dokima/planner.py main ('post'), with its own gh issue edit call. A build that leaves that call as it is, or lets the helper's refusal crash the planner run with no comment on the issue, passes every test.",
   "evidence": "dokima/planner.py:362-363 saves the body with gh(\"issue\", \"edit\", number, ..., \"--body-file\", \"-\", input=render(...)), run by .github/workflows/planner.yml:119. The planner's tests (test_replanning_never_changes_the_owner_part, test_a_first_plan_adds_the_marker_to_a_fresh_ask) only call planner.render; no test runs planner.main(
```

> (Bash completed with no output)

**Agent:** I've blocked the plan for #179 and sent it back to the planner with one blocker. The review is saved at `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What I checked:** All 14 new tests in `tests/test_body.py` fail today for the right reason: the body helper doesn't exist yet, so nothing crashes on a bad path or a missing tool. The rest of the suite still passes (270 tests). The planner removed one line from an older card test and gave a reason, which I accept. Its four criteria match the story's wording. The owner went on with the planner's two assumptions: an issue with an older layout keeps its whole existing body below the marker, and the issue's wording counts as asking to change `dokima/card.py`.

**Blocker B1 (criteria 179.3 and 179.5):** The plan says both the card and the planner redraw the issue body through the new helper. But only the card is tested for refusing a save and leaving a comment on the issue. The planner saves the issue body itself, with its own edit call at `dokima/planner.py:362-363`, which the `plan` label still runs through `planner.yml`. The planner's tests only check the text its render produces, never its save. So a build could leave that save as it is, or let a refusal crash the planner run with no comment on the issue, and still pass every test. The fix I proposed: add tests that run the planner's `post` step on a faked GitHub with the helper set to refuse, checking that nothing is saved and one comment with the reason lands on the issue, plus a matching good run that saves with no comment.

**One note (not a blocker):** Every refusal test triggers the refusal the same way, with a card that contains the marker. A helper that only looks for the marker, without comparing the owner's part before and after the redraw, would pass them all.
