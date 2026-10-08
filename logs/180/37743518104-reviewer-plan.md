# reviewer (plan) for #180

Run: https://github.com/dokima-dev/dokima/actions/runs/37743518104

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (49.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/06528fb5-c052-4067-9fbd-50b234b6a534/tool-results/bk2vlisal.txt
> 
> Preview (first 2KB):
> # Issue #180: The issue and PR card shows the plan and its proof, drawn only from the records
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 2</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners see the same card on an issue and its PR, built by code from the agents' records and GitHub's checks, showing each promise next to its proof.
> 
> **Context:** Keeps the issue body of #143 and the moves from #99 and #104. Today dokima/card.py builds the card by parsing issue text (plan.parse on the body), shows a '### title' heading, uses 'Objective' and 'Full suite' (card.FULL_SUITE is 'all tests'), and the PR shows the approved plan while the issue shows the current one. Records are bot comments marked <!-- dokima-record --> (dokima/agent.py records(), latest(), approved()); the plan.json in the newest passed planner record holds user_story, acceptance_criteria, non_functional, scope, out_of_scope and tests (criterion -> test ids). Criterion checks are named 'N.k · ...' (dokima/checks.py check_name). 'Verified by' is the first docstring line of each test. The issue explicitly asks for the card, so dokima/card.py may change. The body is writ

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (37.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/06528fb5-c052-4067-9fbd-50b234b6a534/tool-results/b5e2aq57j.txt
> 
> Preview (first 2KB):
> # Issue #180: The issue and PR card shows the plan and its proof, drawn only from the records
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 2</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners see the same card on an issue and its PR, built by code from the agents' records and GitHub's checks, showing each promise next to its proof.
> 
> **Context:** Keeps the issue body of #143 and the moves from #99 and #104. Today dokima/card.py builds the card by parsing issue text (plan.parse on the body), shows a '### title' heading, uses 'Objective' and 'Full suite' (card.FULL_SUITE is 'all tests'), and the PR shows the approved plan while the issue shows the current one. Records are bot comments marked <!-- dokima-record --> (dokima/agent.py records(), latest(), approved()); the plan.json in the newest passed planner record holds user_story, acceptance_criteria, non_functional, scope, out_of_scope and tests (criterion -> test ids). Criterion checks are named 'N.k · ...' (dokima/checks.py check_name). 'Verified by' is the first docstring line of each test. The issue explicitly asks for the card, so dokima/card.py may change. The body is writ

`3. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; cat plan.json
```

> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> [
>  {
>   "id": "B1",
>   "criterion": "180.1",
>   "test": "tests/test_card_records.py::test_the_issue_text_never_changes_the_card",
>   "problem": "Every test that runs the card replaces card.gather (the step that fetches the agents' records, the PR's check runs, its reviews, the code owners and each test's Verified by) with a fixed answer, and no test runs the real one. So 180.1's 'drawn only from the agents' records' and 180.6's 'an approval from someone who is not a code owner never shows as passed' are proven only for data handed in by the test. A gather that reads the plan from the issue's text, counts any pasted comment as a record, takes the check runs of an old commit, or calls every reviewer a code owner would pass every test.",
>   "evidence": "tests/test_card_records.py write_main: monkeypatch.setattr(card, 'gather', lambda repo, n, pr: found), so the two issue texts in test_the_issue_text_never_changes_the_card can never reach the card; tests/test_body.py run_card does the same; every other test calls card.render with a hand-built 'found'. grep finds no test that calls card.gather.",
>   "fix": "Add a test (proving 180.1, and 180.6 for the owners) that runs the real card.gather against a faked card.gh, as test_the_card_finds_the_pr_on_either_branch does for find_work: the issue's comments hold a bot record, a person's comment pasting a record and an issue text with its own plan; the PR has a head commit with check runs, a

`4. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> # Issue #180: The issue and PR card shows the plan and its proof, drawn only from the records
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 2</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners see the same card on an issue and its PR, built by code from the agents' records and GitHub's checks, showing each promise next to its proof.
> 
> **Context:** Keeps the issue body of #143 and the moves from #99 and #104. Today dokima/card.py builds the card by parsing issue text (plan.parse on the body), shows a '### title' heading, uses 'Objective' and 'Full suite' (card.FULL_SUITE is 'all tests'), and the PR shows the approved plan while the issue shows the current one. Records are bot comments marked <!-- dokima-record --> (dokima/agent.py records(), latest(), approved()); the plan.json in the newest passed planner record holds user_story, acceptance_criteria, non_functional, scope, out_of_scope and tests (criterion -> test ids). Criterion checks are named 'N.k · ...' (dokima/checks.py check_name). 'Verified by' is the first docstring line of each test. The issue explicitly asks for the card, so dokima/card.py may change. The body is written through story 1's marker helper. The status line, summary sentence and children are story 3. The owner's comment of 2026-10-07 23:54 adds the four check states (passed, failed, running, not started); GitHub's che

`5. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; tail -20 issue.md | cut -c1-500
```

> 29:### RezaSoleymanifar on issue #180 (2026-10-08T06:48:13Z)
> 33:### dokima-runtime on issue #180 (2026-10-08T06:48:35Z)
> 200:### RezaSoleymanifar on issue #180 (2026-10-08T07:13:10Z)
> 204:### dokima-runtime on issue #180 (2026-10-08T07:13:26Z)
> 353:### dokima-runtime on issue #180 (2026-10-08T07:17:06Z)
> 529:### RezaSoleymanifar on issue #180 (2026-10-08T07:27:11Z)
> 533:### dokima-runtime on issue #180 (2026-10-08T07:27:34Z)
> </details>
> 
> <sub>Opus 5.5 · 4.3 min · 14 turns · 733,856 tokens in, 16,406 out · $0.97 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/180/37742488821-planner.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37742488821)</sub>
> 
> **Next:** @RezaSoleymanifar The plan has questions for you. Answer with `/plan` and your words, or say `/review` to go on with its assumptions.
> 
> 
> ### RezaSoleymanifar on issue #180 (2026-10-08T07:27:11Z)
> 
> /review
> 
> ### dokima-runtime on issue #180 (2026-10-08T07:27:34Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> **Reviewer (plan)** · getting ready
> 
> The machine is getting ready. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37743518104)</sub>
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Now look at the new tests and run them.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat 481ca21 HEAD; python -m pytest -q tests/test_card_records.py 2>&1 | tail -30
```

> tests/test_body.py         |   7 +
>  tests/test_card.py         |  77 ++----
>  tests/test_card_records.py | 620 +++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_terms.py        |  30 +--
>  4 files changed, 655 insertions(+), 79 deletions(-)
> FAILED tests/test_card_records.py::test_the_card_finds_the_pr_on_either_branch - AssertionError: 180.1: the card did not find the PR built on try/issue-40
> assert (40, None) == (40, 7)
>   
>   At index 1 diff: None != 7
>   
>   Full diff:
>     (
>         40,
>   -     7,
>   +     None,
>     )
> FAILED tests/test_card_records.py::test_the_card_fetches_only_the_bots_records_and_the_latest_commits_checks - Failed: 180.1: the card is not drawn from the records yet: card.gather does not exist
> FAILED tests/test_card_records.py::test_the_user_story_comes_first_then_the_criteria - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_each_criterion_has_its_circle_hanging_outside_linked_to_its_check - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_verified_by_is_each_tests_first_docstring_line_linking_to_the_test - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_verified_by_is_hidden_when_there_is_none - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does no

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff b756071 HEAD --stat; grep -n "^def \|^    def " tests/test_card_records.py
```

> tests/test_card_records.py | 162 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 162 insertions(+)
> 66:def rec(role, stage=None, passed=True, n=1, **handback):
> 85:def review(state, login="boss", url=APPROVAL):
> 90:def run(name, status="completed", conclusion="success", n=7):
> 96:def job(n):
> 107:def draw(page="issue", **kw):
> 115:def block(text):
> 121:def rows(text):
> 126:def row_of(text, words, k):
> 133:def alts(html):
> 137:def circle(text, words, k):
> 146:def dod(text, k):
> 155:def write_main(monkeypatch, tmp_path, current, found=FOUND):
> 163:    def gh(*args, **kw):
> 197:def record_comment(login, r, at):
> 203:def fake_github(monkeypatch, tmp_path, issue_text, reviews):
> 226:    def rest(c):
> 230:    def cli(c):
> 233:    def content(path, ref, raw):
> 241:    def gh(*args, **kw):
> 287:def gather(monkeypatch, tmp_path, issue_text="My ask.", reviews=(), k="180.1"):
> 296:def run_ids(recs):
> 302:def test_the_issue_text_never_changes_the_card(record_property, monkeypatch, tmp_path):
> 320:def test_the_issue_and_its_pr_show_the_same_card(record_property, monkeypatch, tmp_path):
> 335:def test_the_card_finds_the_pr_on_either_branch(record_property, monkeypatch):
> 348:def test_the_card_fetches_only_the_bots_records_and_the_latest_commits_checks(record_property, monkeypatch, tmp_path):
> 377:def test_the_user_story_comes_first_then_the_criteria(record_property):
> 389:def test_each_criterion_has_its_circle_hanging_outside_linked_to_its_check(record_property):
> 401:def test_verified_by_is_each_tests_

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,376p tests/test_card_records.py; sed -n 600,640p tests/test_card_records.py
```

> """The issue and PR card shows the plan and its proof, drawn only from the agents' records and GitHub's checks.
> 
> Issue #180 (story 2 of #143). The card is drawn by `dokima/card.py` from what GitHub holds, never from the issue's text:
> 
>     card.render(repo, issue, found, page="issue")
>         issue  {"number": 40, "url": ...}
>         found  {"recs":       the agents' records, oldest first (dokima.agent.records),
>                 "pr":         the PR (GitHub's pulls API) or None,
>                 "check_runs": GitHub's check runs on the PR's latest commit,
>                 "reviews":    GitHub's reviews of the PR, oldest first,
>                 "owners":     the code owners' logins,
>                 "tests":      {"path::name": {"verified_by": first docstring line or None, "url": link to the test}},
>                 "worker":     the latest worker run or None}
>     card.test_entry(repo, ref, path, source, name)   one entry of found["tests"], read from a test file's source
>     card.gather(repo, number, pr_number)             fetches `found` from GitHub; main draws the card from it
>         It reads GitHub only through `gh` (card.gh, or agent.gh / plan.gh when it reuses their helpers): the REST API
>         (`gh api repos/...`, files through `contents/<path>?ref=<sha>`), `gh issue view`, `gh pr view`, `gh pr list`.
>         The code owners are the ones named on the default branch, never on the PR's own commit.
>     card.find_work(repo)                             the issue and its PR, asked

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "BOT\b\|^BOT\|def records\|def gh" -A6 dokima/agent.py | head -60
```

> 24:def gh(*args):
> 25-    """Run the GitHub CLI and return its output."""
> 26-    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 27-
> 28-
> 29-MARK = "<!-- dokima-record -->"
> 30-LIVE = "<!-- dokima-live -->"
> 31:BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
> 32-HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 33-
> 34-
> 35-def linked_prs(repo, number):
> 36-    """Pull requests built for the issue: from its work or try branch."""
> 37-    found = []
> --
> 67:def records(items):
> 68-    """Every agent record in the conversation, oldest first. Only comments the bot posted count: anyone can paste text."""
> 69-    out = []
> 70-    for c in items:
> 71-        body = c.get("body") or ""
> 72:        if (c.get("author") or {}).get("login") != BOT or MARK not in body:
> 73-            continue
> 74-        m = re.search(r"```json\n(.*?)\n```", body, re.S)
> 75-        try:
> 76-            out.append(json.loads(m.group(1)) if m else None)
> 77-        except json.JSONDecodeError:
> 78-            continue
> --
> 102:    if (c.get("author") or {}).get("login") != BOT or MARK not in (c.get("body") or ""):
> 103-        return False
> 104-    r = records([c])
> 105-    return bool(r) and (role is None or (r[0].get("role") == role and (r[0].get("stage") or "") == (stage or "")))
> 106-
> 107-
> 108-def open_blockers(recs, stage):
> --
> 270:            if (c.get("user") or {}).get("login") not in (BOT, f"{BOT}[bot]") or LIVE not in body or MARK in body:
> 271-

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | grep -E "FAILED|passed|failed" | grep -v test_card_records | cut -c1-250
```

> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...ng works', 'source': 'https://github.com/o/r/issues/40'}], 'non_functional': [], ...}, 'check': {'passed': True}, ...}]
> _____________ test_title_asks_for_approval_when_all_checks_passed ______________
>     def test_title_asks_for_approval_when_all_checks_passed(record_property):
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'check': {'passed': True}, ...}]
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'check': {'passed': True}, ...}]
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'check': {'passed': True}, ...}]
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'check': {'passed': True}, ...}]
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners s

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added two tests that run the card's real fetching step against a faked GitHub: one for which records, checks and Verified by lines the card is drawn from (180.1), one for whose approval counts as the owner's (180.6).",
          "It left the five acceptance criteria, the tests already planned and the five questions unchanged."],
  "decided": ["Only an approval by someone named in CODEOWNERS on the default branch counts as the owner's; a CODEOWNERS changed on the PR's own commit does not."],
  "open": ["Nothing redraws the card when an agent posts a record until card.yml is changed (raised as a concern)."]},
 "verdict": "approve",
 "summary": "The plan now proves the card is fetched only from the bot's records, the PR's latest checks and code owners named on main, so every promise has a test that fails today for the right reason.",
 "blockers": [],
 "notes": [
  {"text": "180.6 now also says the approving code owner must be named on the default branch. The owner did not say this, but it follows from 'fail closed': otherwise a PR could name its own approver.",
   "evidence": "plan.json non_functional[0]; tests/test_card_records.py::test_only_a_code_owner_on_main_makes_the_approval_pass (CODEOWNERS names intruder on the PR's commit)."},
  {"text": "The faked GitHub in the new tests stops on any request it does not know, so the worker has to fetch through the REST API or gh issue/pr view the way Dokima already does; that is a narrow but workable shape.",
   "evidence": "tests/test_card_records.py fake_github: raises '180.1: card.gather asked GitHub something the fake does not serve'."},
  {"text": "All 19 new tests fail today because card.gather, card.render(repo, issue, found) and card.test_entry do not exist yet, and because find_work misses try/issue-N; the nine rewritten card tests fail because render does not yet take the records.",
   "evidence": "pytest 
```

> (Bash completed with no output)

**Agent:** I approved the plan for #180. The review is saved as `/tmp/dokima-out/review.json` and passed both hand-back checks.

**Why it's approved:** the one open blocker from last round (B1) is fixed. Before, every test handed the card ready-made data, so nothing proved where that data came from. The planner added two tests that run the card's real fetching step against a faked GitHub:
- **180.1:** the card takes only the bot's records, never a record a person pasted into a comment, and never the plan written in the issue's text. It uses only the checks on the PR's latest commit, and reads each Verified by line from the test file at that commit. A different issue text changes nothing it fetches.
- **180.6:** only an approval by someone named in CODEOWNERS on main counts as the owner's. A CODEOWNERS changed on the PR's own commit doesn't count.

**Tests:** all 19 new tests fail today because the feature doesn't exist yet, not because of a crash or a broken setup. The full suite shows 28 failed and 317 passed. The other 9 failures are older card tests rewritten for the new card, which can't run until it exists.

**Notes I left (not blockers):**
- The plan adds one thing you didn't say: the approving code owner must be named on main. I accepted it because without it a PR could name its own approver.
- The faked GitHub stops on any request it doesn't know. That forces the worker to fetch data the ways Dokima already does. It's narrow but workable.

**Proposed new issue:** redraw the card when an agent posts a record. Today a new plan, review or approval only reaches the card after some check finishes, and fixing that means changing `card.yml`, which this issue leaves alone.

The planner's five questions are unchanged, and the plan goes ahead on its stated assumptions unless you answer them.
