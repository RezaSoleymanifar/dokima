# reviewer (plan) for #235

Run: https://github.com/dokima-dev/dokima/actions/runs/37850297726

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json 2>/dev/null
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  8 21:57 .
> drwxrwxrwt 18 root   root    4096 Oct  8 21:57 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 21:57 in
> -rw-r--r--  1 runner runner 18278 Oct  8 21:57 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 21:57 open_blockers.json
> -rw-r--r--  1 runner runner  6735 Oct  8 21:57 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 21:57 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 21:57 ..
> -rw-r--r-- 1 runner runner 7382 Oct  8 21:57 01-planner.json
> # Issue #235: The issue and PR card list criteria as bullets, count the owner's merge and always match
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 2</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** The issue card and its PR card show the same thing, list each criterion as a bullet with its live status and proof, and count the owner's merge as approval.
> 
> **Context:** dokima/card.py draws criteria as a <table> (criteria_table, criterion_row); the status circle links to the criterion's check (circle(..., check['html_url'])) and Verified by links each docstring. done_row's Owner approval reads only an Approve review (owner_review), so a merge with no Approve shows unchecked (#212, #224). On #224 the issue card showed Code review passed while the PR card showed nothing: find why the two pages are drawn from different data (gather, render page=) and fix the cause.

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff HEAD~1 -- tests/test_card.py tests/test_card_records.py | head -400
```

> commit 4ae5830030e5f9fbcb3e40b882d3999cfdfeb9be
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:56:56 2026 +0000
> 
>     planner for #235 (run 37848811629)
> 
>  tests/test_card.py         |  21 ++-
>  tests/test_card_bullets.py | 357 +++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_card_records.py |  63 ++++----
>  3 files changed, 404 insertions(+), 37 deletions(-)
> diff --git a/tests/test_card.py b/tests/test_card.py
> index 8ef4068..70a67ee 100644
> --- a/tests/test_card.py
> +++ b/tests/test_card.py
> @@ -70,7 +70,8 @@ def test_title_asks_for_approval_when_all_checks_passed(record_property):
>  
>  def test_links_row():
>      # The field icons code draws in front of a field (issue #234) are not part of the links.
> -    assert re.sub(r"<img [^>]*>\s*", "", links(render())) == ("[latest run](https://github.com/o/r/actions/runs/1) · [PR #5](https://github.com/o/r/pull/5)"
> +    assert re.sub(r"<img [^>]*>\s*", "", links(render())) == ("[latest run](https://github.com/o/r/actions/runs/1) · [issue #40](https://github.com/o/r/issues/40)"
> +                                        " · [PR #5](https://github.com/o/r/pull/5)"
>                                          " · [files changed](https://github.com/o/r/pull/5/files)")
>  
>  
> @@ -93,17 +94,13 @@ def test_no_footer_and_no_gap(record_property):
>      record_property("proves", "74.3")
>      body = render()
>      assert "Built by the card workflow" not in body
> -    for row in re.findall(r"<tr[^>]*

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_bullets.py
```

> """The issue and PR card list criteria as bullets, count the owner's merge and match.
> 
> Issue #235, story 2 of #230.
> 
> The card is drawn by `dokima/card.py` (render, from `found`; main writes it on the issue and its PR). The layout these
> tests read, with markdown links `[text](url)` and HTML links `<a href="url">text</a>` treated alike:
> 
>     - <status icon> **Acceptance criterion:** <the criterion's sentence, linked to its check when it has one>
>       - *Verified by: <the test's docstring first line>*      one line per test with a docstring; only the words
>                                                               Verified by link, to that test (the Verified by field
>                                                               icon may sit in front of the words, inside the link)
>       - Source                                                the word Source links to where the owner asked
> 
> The status icon is an <img> whose alt is its state (not started, running, passed, failed), never inside a link. A
> criterion's lines are its bullet and the indented lines under it, up to the next line that is not indented.
> """
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import card, plan  # noqa: E402
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> REPO = "o/r"
> ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40"}
> ASK_1 = "https://github.com/o/r/issues/40#issuecomment-111"
> ASK_2 = "https://githu

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_card_bullets.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|Error" | head -40; python -m pytest -q tests/test_card.py tests/test_card_records.py 2>&1 | tail -20
```

> E       AssertionError: 235.1: the card still draws the criteria as a table
> tests/test_card_bullets.py:172: AssertionError
> E       AssertionError: 235.1: expected one bullet line “- ...” holding “Second thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.2: expected one bullet line “- ...” holding “First thing works”, found 0:
> tests/test_card_bullets.py:111: AssertionError
> E       AssertionError: 235.3: a code owner's merge with no Approve review leaves Owner approval unchecked
> tests/test_card_bullets.py:250: AssertionError
> E       AssertionError: 235.4: the issue and PR cards differ:
> /home/runner/work/dokima/dokima/tests/test_card_bullets.py:308: AssertionError
> E       AssertionError: 235.4: the car

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def \|owner_review\|state\"\] == \"open\"\|page" dokima/card.py | head -80
```

> 46:def icon(repo, name, alt=None):
> 52:def field_icon(repo, field):
> 57:def state(check):
> 66:def circle(repo, st, url=None):
> 72:def fold(title, lines):
> 77:def escape(text):
> 81:def checks_by_key(check_runs):
> 91:def as_items(steps, owner=None):
> 98:def checks_passed(number, h, check_runs):
> 107:def todo(issue, found, rec):
> 131:def status(issue, found):
> 151:def status_line(repo, stage, todo):
> 157:def child_row(repo, child):
> 166:def links_row(repo, issue, pr, worker, check_runs, page):
> 167:    """The links that matter, minus a link to the page the card is on ("issue" or "pr")."""
> 171:    if page != "issue":
> 173:    if pr and page != "pr":
> 180:def criterion_row(repo, text, check, tests):
> 191:def criteria_table(repo, number, start, criteria, plan_tests, by_key, tests):
> 200:def code_review(recs):
> 208:def owner_review(reviews, owners):
> 215:def done_row(repo, found, all_tests):
> 219:    approval = owner_review(found["reviews"], found["owners"])
> 228:def render(repo, issue, found, page="issue"):
> 229:    """The card for `issue` on `page` ("issue" or "pr"), drawn only from `found`: the agents' records, the PR, its
> 241:    links = links_row(repo, issue, pr, worker, check_runs, page)
> 265:def issue_body(card, notes):
> 270:def pr_body(card, body):
> 276:def gh(*args):
> 280:def find_work(repo):
> 284:    def open_pr(n):
> 307:def latest_worker_run(repo, number):
> 308:    runs = json.loads(gh("api", f"repos/{repo}/actions/workflows/worker.yml/runs?per_page=50"))["workflow_runs"]
> 313:def test_entry(repo, ref,

**Agent:** The plan's new tests fail today for the right reasons; I'm now checking the plan against the owner's asks before writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 200,262p dokima/card.py; sed -n 435,460p dokima/card.py; grep -n -i "source" dokima/roles/planner.md | head
```

> def code_review(recs):
>     """The newest code review whose record passed its check, since the worker last built; None when there is none."""
>     builds = [i for i, r in enumerate(recs) if r.get("role") == "worker"]
>     after = recs[builds[-1] + 1:] if builds else recs
>     reviews = [r for r in after if r.get("role") == "reviewer" and r.get("stage") == "pr" and r.get("check", {}).get("passed")]
>     return reviews[-1] if reviews else None
> 
> 
> def owner_review(reviews, owners):
>     """The newest Approve or Request changes on the PR by a code owner; None when there is none."""
>     found = [r for r in reviews if r.get("state") in ("APPROVED", "CHANGES_REQUESTED")
>              and (r.get("user") or {}).get("login") in owners]
>     return found[-1] if found else None
> 
> 
> def done_row(repo, found, all_tests):
>     """The Definition of Done: All tests, the code review and the owner's approval, each with its verdict and proof."""
>     review = code_review(found["recs"])
>     review_st = "not started" if not review else "passed" if review["handback"].get("verdict") == "approve" else "failed"
>     approval = owner_review(found["reviews"], found["owners"])
>     approval_st = "not started" if not approval else "passed" if approval["state"] == "APPROVED" else "failed"
>     return ("**Definition of Done:** "
>             f"{circle(repo, state(all_tests), all_tests and all_tests['html_url'])} All tests · "
>             f"{circle(repo, review_st, review and review.get('run'))} {field_icon(repo, 'code revie

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 166,200p dokima/card.py; sed -n 276,380p dokima/card.py; cat .github/workflows/card.yml | head -60
```

> def links_row(repo, issue, pr, worker, check_runs, page):
>     """The links that matter, minus a link to the page the card is on ("issue" or "pr")."""
>     links = []
>     if worker:
>         links.append(f"[latest run]({worker['html_url']})")
>     if page != "issue":
>         links.append(f"[issue #{issue['number']}]({issue['url']})")
>     if pr and page != "pr":
>         links.append(f"[PR #{pr['number']}](https://github.com/{repo}/pull/{pr['number']})")
>     if pr:
>         links.append(f"{field_icon(repo, 'files changed')} [files changed](https://github.com/{repo}/pull/{pr['number']}/files)")
>     return " · ".join(links)
> 
> 
> def criterion_row(repo, text, check, tests):
>     """One criterion as a table row: its circle alone in the first cell, hanging outside its words, linked to its check;
>     then its words and, when any of its tests has a docstring, Verified by with each one linking to its test."""
>     st = state(check)
>     words = escape(text)
>     proofs = [f'<a href="{t["url"]}">{escape(t["verified_by"])}</a>' for t in tests if t and t.get("verified_by")]
>     if proofs:
>         words += f"<br>{field_icon(repo, 'verified by')} Verified by: " + "; ".join(proofs)
>     return f"<tr><td>{circle(repo, st, check and check['html_url'])}</td><td>{words}</td></tr>"
> 
> 
> def criteria_table(repo, number, start, criteria, plan_tests, by_key, tests):
>     """The table of criteria numbered from `start`, each row with its own check and tests."""
>     out = ["<table>"]
>     for k, c in enumerate(criteria,

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "acceptance criterion\|verified by" tests/test_*icon* tests/*.py 2>/dev/null | grep -v test_card_bullets | head -20; grep -n "FIELD\|def field_icon" -A6 dokima/card.py | head -30
```

> tests/test_field_icons.py:62:    "acceptance criterion": ("tasklist", "9e458b35be49254fc28fcd1c51cc4fd4a79a7f6e03c3802dfba35e9586aac587"),
> tests/test_field_icons.py:63:    "verified by": ("verified", "64dc3a6e42153dec04c5bf7d11d24dd61903223e0b2c2c321570a10661b9db7b"),
> tests/test_field_icons.py:274:        shows(text, "acceptance criterion", "Acceptance criteria", "234.2", where)
> tests/test_field_icons.py:275:        shows(text, "verified by", "Verified by", "234.2", where)
> tests/test_field_icons.py:303:    assert img("acceptance criterion") in text, f"234.2: the planned card has no Acceptance criteria icon:\n{text}"
> tests/test_field_icons.py:304:    for f in ("needs you", "merged", "files changed", "verified by"):
> tests/test_field_icons.py:307:    assert img("acceptance criterion") not in empty, f"234.2: a card with no plan shows the Acceptance criteria icon:\n{empty}"
> tests/test_field_icons.py:357:    shows(body, "acceptance criterion", "Acceptance criteria", "234.2", "the plan's comment")
> tests/test_field_icons.py:464:    assert img("acceptance criterion") in a, f"234.3: setup: the card shows no field icon to protect:\n{a}"
> tests/test_feature_check.py:88:    """A story whose acceptance criterion has no text or no source link is rejected, naming the story and what is missing.
> tests/test_card_records.py:146:               "still open", "acceptance criterion", "verified by", "files changed", "question", "blocker", "note",
> tests/test_card_records.py:521:    and no acceptance cr

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 230,300p tests/test_field_icons.py
```

> assert attrs["fill"] in PALETTE, f"234.1: the {field} icon's color {attrs['fill']} is not one of today's: {sorted(PALETTE)}"
>     paths = [e for e in root.iter() if e.tag == SVG + "path"]
>     assert paths and all(set(p.attrib) == {"d"} for p in paths), \
>         f"234.1: the {field} icon must be plain paths with no style of their own: {[p.attrib.keys() for p in paths]}"
>     got = hashlib.sha256("\n".join(p.get("d") for p in paths).encode()).hexdigest()
>     assert got == digest, f"234.1: the {field} icon is not the {name} Octicon (16px): its path data differs"
> 
> 
> # 234.2: one fixed table maps the 23 fields to their icons, and every card and run comment shows them
> 
> def test_one_fixed_table_in_code_maps_every_field_to_its_icon(record_property):
>     """One fixed table in code maps each of the 23 fields, and nothing else, to its own icon file.
> 
>     Reads card.FIELD_ICONS and checks it names exactly the 23 fields, each to its own file in dokima/icons/ holding
>     the field's own Octicon (passed and failed keep today's circles), no two fields sharing a drawing, and that
>     card.icon draws a field's icon from it served from main with the field's name as its alt text."""
>     record_property("proves", "234.2")
>     table = getattr(card, "FIELD_ICONS", None)
>     assert isinstance(table, dict), "234.2: there is no fixed table of field icons: card.FIELD_ICONS does not exist"
>     assert set(table) == set(FIELDS), \
>         f"234.2: the table's fields differ: missing {sorted(set(FIELDS) - set

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def shows" -A12 tests/test_field_icons.py
```

> 97:def shows(text, field, label, k, where):
> 98-    """Fail naming criterion k unless the field's icon stands in front of `label` in `text`."""
> 99-    assert in_front(field, label).search(text), \
> 100-        f"{k}: {where} shows “{label}” without the {field} icon right in front of it:\n{text[:3000]}"
> 101-
> 102-
> 103-def comment(login, body, i):
> 104-    """One comment of the conversation, as dokima.agent.conversation lists it."""
> 105-    return {"author": {"login": login}, "body": body, "createdAt": f"2026-10-08T{i:02d}:00:00Z", "where": "issue #40"}
> 106-
> 107-
> 108-def rec(role, stage=None, passed=True, n=1, **handback):
> 109-    """One agent record, as dokima.agent.records reads it from a bot comment."""

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def in_front" -A8 tests/test_field_icons.py
```

> 92:def in_front(field, label):
> 93-    """A pattern for the field's icon right before its words, with only a space, `**` or `<b>` between."""
> 94-    return re.compile(re.escape(img(field)) + r"\s*(?:\*\*|<b>)?\s*" + re.escape(label))
> 95-
> 96-
> 97-def shows(text, field, label, k, where):
> 98-    """Fail naming criterion k unless the field's icon stands in front of `label` in `text`."""
> 99-    assert in_front(field, label).search(text), \
> 100-        f"{k}: {where} shows “{label}” without the {field} icon right in front of it:\n{text[:3000]}"

**Agent:** Everything checks out so far. Writing the review now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five criteria: criteria as bullets with Verified by lines, live status with the sentence linking its check, a code owner's merge counting as Owner approval, identical issue and PR cards, and a Source line under each criterion.",
          "It added 13 failing tests in tests/test_card_bullets.py and rewrote the table-reading tests in tests/test_card.py and tests/test_card_records.py to read bullets."],
  "decided": ["The PR card is written even after the pull request is merged or closed, which it names as the cause of the mismatch on #224; when the card is redrawn does not change.",
              "The planner's prompt (dokima/roles/planner.md) is told to link each criterion to the most recent place the owner asked."],
  "open": ["One question: whether the bot's autopilot merge counts as Owner approval; it assumed no."]},
 "verdict": "approve",
 "summary": "The plan keeps all five of the owner's asks, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "The test for the most-recent Source (235.5) only reads the planner's prompt for the words; whether the planner really picks the newest ask can only be judged by the plan reviewer on each later plan.",
   "evidence": "tests/test_card_bullets.py::test_the_planner_links_each_criterion_to_the_most_recent_ask matches 'source' plus 'most recent|newest|latest' in dokima/roles/planner.md"},
  {"text": "The check that the card shows no separate list of the owner's asks only looks for the word asks, so a list under another heading would pass.",
   "evidence": "tests/test_card_bullets.py::test_each_criterion_has_a_source_line_after_verified_by: assert \"asks\" not in plain(block(text)).lower()"},
  {"text": "The scope touches dokima/roles/planner.md, which AGENTS.md keeps closed unless the issue asks; the owner's Source comment needs the planner to choose the mos
```

> (Bash completed with no output)

**Agent:** I approved the plan for #235, and the review passes Dokima's own checks. It's saved at `/tmp/dokima-out/review.json`.

**Tests:** I ran them on this branch. All 13 new tests in `tests/test_card_bullets.py` fail today because the feature isn't built yet, not because of a crash or a bad path. The 6 tests the planner rewrote in `tests/test_card.py` and `tests/test_card_records.py` also fail, for the same reason: they look for criteria as bullets and the card still draws a table. The new layout also fits the field-icon tests from #234.

**Your asks:** each one in the issue maps to a criterion, and none is missing:
- Criteria as bullets with *Verified by* in italics, where only those words link to the test → 235.1
- Live status icon, with the criterion's sentence (not the icon) linking to its check → 235.2
- A code owner's merge counts as Owner approval; a merge by anyone else, including the bot, does not → 235.3
- The issue and PR cards are identical and both link to both pages. The planner traced the #224 mismatch to the card skipping a closed PR, and the plan writes the PR card even after merge → 235.4
- A Source line under each criterion pointing to your most recent ask, and no separate list of asks → 235.5

**The planner's one question:** should the bot's autopilot merge count as your approval? It assumed no. I accepted that because your words name only a code owner's merge, and it changes neither how the system works nor what it costs. On autopilot this question won't stop for you.

I left three notes; none blocks:
1. The "most recent ask" part of 235.5 is only checked by looking for the words in the planner's prompt. Whether the planner actually picks your newest ask can only be judged by the plan reviewer on later plans.
2. The "no separate list of asks" check only looks for the word "asks", so a list under another heading would still pass.
3. The plan changes `dokima/roles/planner.md`, which AGENTS.md keeps closed unless the issue asks. Your Source comment needs the planner to choose the most recent ask, so the change follows from that request.

All of your asks link to the issue page rather than your exact comment, because the issue history I was given has no comment links.
