# reviewer (plan) for #180

Run: https://github.com/dokima-dev/dokima/actions/runs/37742094015

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:13 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:13 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:13 in
> -rw-r--r--  1 runner runner 15819 Oct  8 07:13 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:13 open_blockers.json
> -rw-r--r--  1 runner runner  9196 Oct  8 07:13 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:13 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:13 ..
> -rw-r--r-- 1 runner runner 9877 Oct  8 07:13 01-planner.json
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
> **Context:** Keeps the issue body of #143 and the moves from #99 and #104. Today dokima/card.py builds the card by parsing issue text (plan.parse on the body), shows a '### title' heading, uses 'Objective' and 'Full suite' (card.FULL_SUITE is 'all tests'), and the PR shows the approved plan while the issue shows the current one. Records are bot comments marked <!-- dokima-record --> (dokima/agent.py records(), latest(), approved()); the plan.json in the newest passed planner record holds user_story, acceptance

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_card_records.py dokima/card.py; cat tests/test_card_records.py
```

> commit b75607153c1cc20b142dff3ac6c72a5d92017ca1
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:03:47 2026 +0000
> 
>     planner for #180 (run 37739651538)
> 
>  tests/test_body.py         |   7 +
>  tests/test_card.py         |  77 +++-----
>  tests/test_card_records.py | 458 +++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_terms.py        |  30 +--
>  4 files changed, 493 insertions(+), 79 deletions(-)
>   458 tests/test_card_records.py
>   206 dokima/card.py
>   664 total
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
>     card.test_entry(repo, ref, path, source, name)   one entry of found["tests"], read from a test file's s

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_card_records.py 2>&1 | tail -30; python -m pytest -q 2>&1 | tail -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bqod6wfp0). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/5fa718a7-5c84-43ae-86a3-6b201848200f/tasks/bqod6wfp0.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat dokima/card.py; git show HEAD -- tests/test_card.py tests/test_terms.py tests/test_body.py
```

> #!/usr/bin/env python3
> """Build the Dokima card and write it at the top of both the issue and its PR.
> 
> The card shows the plan's goals and criteria, each with GitHub's own verdict
> from that criterion's check. It computes no verdicts itself: a pass appears only
> when GitHub recorded the criterion's check as passed on the PR's latest commit.
> 
> It runs from the default branch, never from a PR's own code, so the work being
> judged cannot change how it is reported. No AI writes the card. On the issue,
> the card is the issue's text: its words are the plan, and only the icons and
> links change as checks run.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
> from dokima import body, plan  # noqa: E402
> 
> WORKER_ACTIVE = {"queued", "in_progress", "requested", "pending", "waiting"}
> FULL_SUITE = "all tests"
> INDENT = "&emsp;"  # used for the list of edits at the bottom of the card
> CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #\d+", re.I)
> 
> 
> def icon(repo, name):
>     """One of GitHub's own circle icons (Octicons, MIT), served from this repo, centered on its line."""
>     url = f"https://raw.githubusercontent.com/{repo}/main/dokima/icons/{name}.svg"
>     return f'<img src="{url}" width="16" height="16" align="absmiddle" alt="{name}">'
> 
> 
> def state(check):
>     """GitHub's verdict for one check run (already filtered to the PR's latest commit)."""
>     if check is None:
>         return "

`5. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/5fa718a7-5c84-43ae-86a3-6b201848200f/tasks/bqod6wfp0.output
```

> FAILED tests/test_card_records.py::test_the_issue_text_never_changes_the_card - Failed: 180.1: the card is not drawn from the records yet: card.gather does not exist
> FAILED tests/test_card_records.py::test_the_issue_and_its_pr_show_the_same_card - Failed: 180.1: the card is not drawn from the records yet: card.gather does not exist
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
> FAILED tests/test_card_records.py::test_the_user_story_comes_first_then_the_criteria - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_each_criterion_has_its_circle_hanging_outside_linked_to_its_check - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_verified_by_is_each_tests_first_docstring_line_linking_to_the_test - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_verified_by_is_hidden_when_there_is_none - Failed: the card is not drawn from the records yet: card.render(repo, issue, found) does not exist
> FAILED tests/test_card_records.py::test_a_tests_verified_by_is_its_first_docstring_line - AssertionErr

**Agent:** Grading the plan now: the 17 new tests all fail today for the right reason. Next I'm checking whether anything proves the step that fetches data from GitHub (`card.gather`).

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def \|CODEOWNERS\|dokima-record" dokima/agent.py | head -60; grep -rn "CODEOWNERS\|def owners\|code_owners" dokima/*.py | head; grep -h "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/5fa718a7-5c84-43ae-86a3-6b201848200f/tasks/bqod6wfp0.output | grep -v card_records | sort -u
```

> 24:def gh(*args):
> 29:MARK = "<!-- dokima-record -->"
> 35:def linked_prs(repo, number):
> 43:def conversation(repo, number):
> 59:def issue_text(d, items):
> 67:def records(items):
> 82:def latest(recs, role, passed=True):
> 90:def approved(recs):
> 100:def is_record(c, role=None, stage=None):
> 108:def open_blockers(recs, stage):
> 116:def blockers_for(recs, role):
> 131:def problems_round(role, h, pack_dir):
> 154:def story_body(parent, i, story, parent_title):
> 168:def file_split(repo, parent, recs):
> 195:def build_record(role, stage, out, check_text, passed, meta):
> 210:def not_started(role, stage, why, meta):
> 217:def cancelled(role, stage, started, meta):
> 224:def live_card(role, stage, state, ahead=None):
> 255:def where_card(repo, number, role, stage):
> 262:def run_ahead(repo, number):
> 280:def queue(role, stage, number, state):
> 292:def render(rec):
> 352:def jsonl_files(root):
> 357:def scrub(text, secrets):
> 364:def transcript(log_dir, secrets=()):
> 390:def run_report(path):
> 402:def footnote(rec):
> 421:def models_used(log_dir):
> 435:def pack(repo, number, role, stage, dest):
> 462:def problems_questions(qs):
> 484:def problems_review(r):
> 521:def problems_work(w):
> 541:def filled(v):
> 546:def problems_items(h, field, keys, name=None):
> 563:def problems_shape(kind, h):
> 607:def plan_criteria(plan, number):
> 616:def problems_plan(kind, h, plan, number):
> 639:def load(path, name):
> 652:def check(kind, path, plan_path=None, number=None):
> 681:def problems_pack(role, stage, dest):
> 728:def command_of(body):
> 734:def issue_o

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_card.py tests/test_body.py tests/test_terms.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-220; sed -n 60,100p dokima/agent.py
```

> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...ng works', 'source': 'https://github.com/o/r/issues/40'}], 'non_functional': [], ...}, 'chec
> _____________ test_title_asks_for_approval_when_all_checks_passed ______________
>     def test_title_asks_for_approval_when_all_checks_passed(record_property):
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'chec
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'chec
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'chec
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'chec
> recs = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'user_story': 'Owners see a card.', 'acceptance...True}, ...}, {'role': 'reviewer', 'stage': 'plan', 'handback': {'verdict': 'approve'}, 'chec
> recs = [{'role'

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five acceptance criteria and one non-functional requirement for a card drawn from the agents' records and GitHub's checks, with 17 new tests in tests/test_card_records.py.",
          "It rewrote nine older card tests for the new way of drawing and deleted four whose promises this issue replaces, each with a reason."],
  "decided": ["Only dokima/card.py changes; no workflow changes, and the stage title and links row stay as they are.",
              "It planned on five assumptions, among them: queued shows as not started, review means the reviewer's code review, and owner approval means a code owner's Approve."],
  "open": ["Nothing redraws the card when an agent posts a record, until card.yml is changed (raised as a concern)."]},
 "verdict": "block",
 "summary": "The tests prove how the card is drawn, but no test ever runs the part that fetches the records, checks, reviews and code owners from GitHub, so a card still read from the issue's text, or one that counts anyone's approval, would pass.",
 "blockers": [{"id": "B1", "criterion": "180.1",
   "test": "tests/test_card_records.py::test_the_issue_text_never_changes_the_card",
   "problem": "Every test that runs the card replaces card.gather (the step that fetches the agents' records, the PR's check runs, its reviews, the code owners and each test's Verified by) with a fixed answer, and no test runs the real one. So 180.1's 'drawn only from the agents' records' and 180.6's 'an approval from someone who is not a code owner never shows as passed' are proven only for data handed in by the test. A gather that reads the plan from the issue's text, counts any pasted comment as a record, takes the check runs of an old commit, or calls every reviewer a code owner would pass every test.",
   "evidence": "tests/test_card_records.py write_main: monkeypatch.setattr(card, 'gather', lambda repo, n, pr: found), so 
```

> (Bash completed with no output)

**Agent:** I've blocked the plan for #180 and sent it back to the planner with one blocker. The hand-back is `/tmp/dokima-out/review.json`, and it passes both checks with no problems.

**What I checked:**
- All 17 new tests in `tests/test_card_records.py` fail today for the right reason: `card.render(repo, issue, found)`, `card.gather` and `card.test_entry` don't exist yet, and `find_work` doesn't look at `try/issue-N`.
- The 9 rewritten tests in `tests/test_card.py` also fail today. That's only because `render` doesn't take the new arguments yet, which the plan's test changes expect. The other 317 tests pass.
- Every ask in the issue maps to a criterion, 180.1 to 180.6. None is missing.

**Blocker B1 (criterion 180.1, also affects 180.6, for the planner):** No test runs the step that fetches data from GitHub (`card.gather`). That step fetches the agents' records, the PR's checks, its reviews, the code owners and each test's "Verified by" line. Every test either swaps it for a fixed answer or builds the data by hand. So the tests can't fail on the things that matter most here:
- reading the plan from the issue's text;
- counting a comment someone pasted as a record;
- using checks from an older commit;
- treating any reviewer as a code owner.

The fix is one more test that runs the real fetch step against a fake GitHub, the way the existing PR-lookup test does. It should check that only the bot's records, the latest commit's checks and the code owners listed in the repo's CODEOWNERS file get through.

**Notes:**
- Criterion 180.1 adds something you didn't write: the card must find the PR on either a `try/issue-N` or a `work/issue-N` branch. I accepted it, because without it the card wouldn't reach today's PRs at all.
- The planner raised that nothing redraws the card when an agent posts a record. I proposed a separate issue for it: "Redraw the card when an agent posts a record".
