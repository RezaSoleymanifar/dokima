# reviewer (plan) for #333

Run: https://github.com/dokima-dev/dokima/actions/runs/37954859617

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (41.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9856eebb-1291-4825-ad29-3fe376a113be/tool-results/bmzyliltw.txt
> 
> Preview (first 2KB):
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
> # Issue #333: A scan of the whole board and every card names anything that does not match its state
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 332 -->
> <!-- dokima-blocking: {"blocked_by": [331, 332], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #333](https://github.com/dokima-dev/dokima/issues/333)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #331, #332
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="no

`2. Bash`
```
cd /tmp/pack; sed -n 20,400p issue.md
```

> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #330, story 3</summary>
> 
> **Part of:** #330 Cards and the board always show what is true right now
> 
> **User story:** The owner can run one scan that proves the board and cards are true, and it names every card that is not.
> 
> **Context:** Split from #330 (rule R2). The owner's test: after #330 ships, a scan of the whole board finds no closed card outside Done or with a pill, no open card in the wrong column, and the PR cards of #246 and #312 show Merged with every check passed. Board.cards() in dokima/board.py already pages every card with its Action and state; it needs Status too. The scan reuses the column and pill computation from story 1 and the card state from story 2, so it lands after both.
> 
> **Acceptance criteria:**
> - A scan names every closed card outside Done or with a pill, every open card in the wrong column, and every stale card. It exits non-zero when it names any, and exits 0 saying all is true otherwise. ([source](https://github.com/dokima-dev/dokima/issues/330))
> - After this ships, the scan of this repo finds nothing, and the PR cards of #246 and #312 show Merged with every check passed. (manual: the owner runs the scan once on the live board and opens both PRs) ([source](https://github.com/dokima-dev/dokima/issues/330))
> 
> **Non-functional:**
> - The scan only reads: it never moves a card or edits a body. (a check that changes what it checks proves nothing)
> 
> </details>
> 
> 
> </de

`3. Bash`
```
cd /tmp/pack; sed -n 400,600p issue.md | head -80; echo ----; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items()},indent=1))" | head -150; cat parent.json | head -50
```

> <details><summary><b>Out of scope</b></summary>
> 
> - Fixing what the scan finds: the board and cards are put right by #331 and #332; the scan only names.
> - A workflow or Run workflow button for the scan; the owner runs the command with their own GitHub login.
> - Checking an open card's pill or its Priority, and items missing from the board; the owner asked for closed cards outside Done or with a pill, open cards in the wrong column and stale cards.
> - Draft items on the board; they are no issue or pull request.
> 
> </details>
> 
> <details><summary><b>Tests</b></summary>
> 
> - 333.1: tests/test_scan.py::test_the_scan_names_every_closed_card_outside_done_or_with_a_pill, tests/test_scan.py::test_the_scan_names_every_open_card_in_the_wrong_column, tests/test_scan.py::test_the_card_the_scan_expects_is_drawn_from_the_state_now, tests/test_scan.py::test_the_scan_names_every_stale_issue_card_and_pr_card, tests/test_scan.py::test_the_scan_of_a_true_board_exits_0_saying_all_is_true, tests/test_scan.py::test_the_board_lists_every_card_with_its_column, tests/test_scan.py::test_the_scan_names_an_open_card_with_no_column
> - 333.2: tests/test_scan.py::test_the_owners_two_pr_cards_pass_only_showing_merged_with_every_check_passed
> - 333.3: tests/test_scan.py::test_the_scan_checks_the_board_and_repo_the_owner_names
> - 333.4: tests/test_scan.py::test_the_scan_never_moves_a_card_or_edits_a_body
> - 333.5: tests/test_scan.py::test_a_card_the_scan_cannot_read_is_named_and_the_scan_fails, tests/test_scan.py::test_a_

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat 034fee4 HEAD; git diff 034fee4 HEAD -- tests/ | head -400; python3 -m pytest -q tests/test_scan.py 2>&1 | tail -30
```

> tests/test_scan.py | 85 +++++++++++++++++++++++++++++++++++++++++-------------
>  1 file changed, 65 insertions(+), 20 deletions(-)
> diff --git a/tests/test_scan.py b/tests/test_scan.py
> index 86d1ab8..e335430 100644
> --- a/tests/test_scan.py
> +++ b/tests/test_scan.py
> @@ -78,6 +78,7 @@ class World:
>          self.prs = {}  # n -> {"issue", "state" (OPEN, MERGED, CLOSED), "body", "sha", "checks"}
>          self.refused = set()  # numbers GitHub will not answer about
>          self.writes, self.calls, self.unknown = [], [], []
> +        self.opened = []  # (board spec, repo) each time a board was opened
>  
>      def issue(self, n, state="open", records=(), card=None, labels=()):
>          self.issues[n] = {"state": state, "records": list(records), "labels": list(labels),
> @@ -109,7 +110,8 @@ def fake_board(world):
>      """A stand-in for dokima.board.Board that reads the World's cards and logs every write."""
>  
>      class FakeBoard:
> -        def __init__(self, *a, **k):
> +        def __init__(self, spec=None, repo=None, *a, **k):
> +            world.opened.append((spec, repo))
>              self.fields = {"Status": ("S", {o: "s-" + o for o in ("Backlog", "Plan", "Work", "Review", "Done")}),
>                             "Action": ("W", {NEEDS: "w-1", AUTO: "w-2"}), "Priority": ("P", {})}
>  
> @@ -556,17 +558,60 @@ def test_the_board_lists_every_card_with_its_column(monkeypatch, record_property
>      assert got == want, f"333.1: the board listed its cards' (column, pill) as {got}, not {want}"
>  
>  
> -# 33

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def run\b\|def run(\|REPO\b\|REPO =\|monkeypatch.setenv\|DOKIMA_BOARD" tests/test_scan.py | head -30; grep -rn "DOKIMA_BOARD" dokima/*.py .github/workflows/ | head
```

> 7:    DOKIMA_BOARD=org/number REPO=owner/name python3 -m dokima.scan
> 13:How the tests run it. dokima.scan.main() is called in-process with DOKIMA_BOARD and REPO set; it returns the exit code
> 47:REPO, SPEC = "o/r", "o/1"
> 290:    monkeypatch.setenv("DOKIMA_BOARD", SPEC)
> 291:    monkeypatch.setenv("REPO", REPO)
> 292:    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
> 307:    return scan.card_now(REPO, kind, n).strip()
> 320:def run(w, capsys):
> 585:    `DOKIMA_BOARD=dokima-dev/N REPO=dokima-dev/dokima python3 -m dokima.scan` once, sees it find nothing, and opens the
> 586:    PRs of #246 and #312 to see Merged with every check passed. This part runs the scan with DOKIMA_BOARD set to o/9
> 595:        monkeypatch.setenv("DOKIMA_BOARD", spec)
> 598:        assert w.opened and set(w.opened) == {(spec, REPO)}, \
> 599:            f"333.3: with DOKIMA_BOARD={spec} and REPO={REPO} the scan opened {w.opened}"
> dokima/board.py:6:    python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")
> dokima/board.py:8:Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing.
> dokima/board.py:430:    spec = os.environ.get("DOKIMA_BOARD", "").strip()
> dokima/board.py:432:        print("No DOKIMA_BOARD set; nothing to sync.")
> dokima/audit.py:3:    python3 -m dokima.audit OWNER/REPO   # reads DOKIMA_BOARD ("org/number") and .github/CODEOWNERS where it runs
> dokima/audit.py:276:    spec = os.environ.get("DOKIMA_BOARD", "").strip()
> doki

**Agent:** I'm checking the new board-and-repo test against the real board code, then I'll write the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "class Board\|def __init__" dokima/board.py | head; sed -n 280,330p tests/test_scan.py
```

> 114:class Board:
> 115:    def __init__(self, spec, repo, q=gql, rest=api):
> 
> 
> @pytest.fixture
> def world(monkeypatch):
>     """A fresh World wired into the board and every `gh` helper, with the scan's settings."""
>     w = World()
>     monkeypatch.setattr(board, "Board", fake_board(w))
>     for mod in (agent, card, plan, scan):
>         if mod is not None and hasattr(mod, "gh"):
>             monkeypatch.setattr(mod, "gh", fake_gh(w))
>     monkeypatch.setenv("DOKIMA_BOARD", SPEC)
>     monkeypatch.setenv("REPO", REPO)
>     monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
>     return w
> 
> 
> def need_scan(criterion):
>     """Fail, naming the criterion, while dokima/scan.py does not exist."""
>     if scan is None:
>         pytest.fail(f"{criterion}: there is no scan yet (dokima/scan.py is missing)")
>     for name in ("main", "card_now"):
>         if not callable(getattr(scan, name, None)):
>             pytest.fail(f"{criterion}: dokima/scan.py has no {name}()")
> 
> 
> def true_card(w, kind, n):
>     """The card Dokima draws now for this issue or PR, as the scan sees it."""
>     return scan.card_now(REPO, kind, n).strip()
> 
> 
> def make_true(w, *items):
>     """Write into each body the card Dokima draws now, so that card matches its state."""
>     for kind, n in items:
>         text = true_card(w, kind, n)
>         if kind == "pr":
>             w.prs[n]["body"] = text + f"\n\nCloses #{w.prs[n]['issue']}"
>         else:
>             w.issues[n]["body"] = text + "\n\n<!-- dokima-ask -->" + w.issues[n]["body"].split("<!-- doki

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Split the old 333.2 in two: 333.2 now says the PR cards of #246 and #312 pass the scan only when they show Merged with every check passed, and a new 333.3, marked (manual), has the owner run the scan once on the live board after #330 ships and open both PRs.",
          "Added a test that the scan checks exactly the board and repo the owner names, and a test that an open card in no column is named.",
          "Renumbered the read-only and unreadable-card requirements to 333.4 and 333.5; all twelve tests fail today because dokima/scan.py does not exist yet."],
  "decided": ["The live scan of this repo's board stays a manual check by the owner, as the owner wrote."],
  "open": ["If #332 changes which GitHub calls the card code makes, the fake GitHub fails naming the call and the tests need a re-plan."]},
 "verdict": "approve",
 "summary": "The plan now keeps the live-board scan as the owner's manual check and proves every other promise with a test that fails today because the scan does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "Criteria 333.3 to 333.5 were renumbered since the last round. No plan was approved and no test was merged under the old numbers, so no criterion number that was ever in force is reused.",
   "evidence": "git diff 034fee4 HEAD -- tests/test_scan.py: 'Proves 333.3' became 'Proves 333.4' and 'Proves 333.4' became 'Proves 333.5'; tests/test_scan.py is not on main"},
  {"text": "The tests swap in a fake board for dokima.board.Board, so the worker must reach the board as board.Board, not import Board by name, or the scan would try to reach the real GitHub.",
   "evidence": "tests/test_scan.py:285 monkeypatch.setattr(board, \"Board\", fake_board(w))"}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "A scan names every closed card outside Done or with a pill, every open card in the wrong column, and 
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The live-board scan is now the owner's manual check, and every other promise has a test that fails today because the scan is missing."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 333 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #333, and the review is saved at `/tmp/dokima-out/review.json`. It passed both hand-back checks.

**The last blocker (B1) is fixed.** The old 333.2 is now two criteria:
- **333.2:** the PR cards of #246 and #312 pass the scan only when they show Merged with every check passed. The same test as before proves this.
- **333.3 (manual):** after #330 ships, you run the scan once on the live board and open both PRs, as you wrote in the issue. Its automated part checks that the scan reads exactly the board and repo you name.

**Tests:** I ran all 12 in `tests/test_scan.py`. Each one fails today for the right reason: `dokima/scan.py` doesn't exist yet. The planner also added a test from my last note, so an open card with no column at all is now named.

All six of your asks map to a criterion, and none is missing. The plan has no questions for you.

**Two notes, neither blocking:**
- The read-only and unreadable-card requirements moved from 333.3 and 333.4 to 333.4 and 333.5. That doesn't break the rule that criterion numbers are never reused, because no plan was approved and no tests were merged under the old numbers.
- The tests replace the board with a fake one, so the worker has to reach it as `board.Board`. If the scan imports `Board` by name, it would bypass the fake and try to reach the real GitHub.

The planner's earlier concern still stands: if #332 changes which GitHub calls the card code makes, these tests will fail by naming the unknown call, and they'll need a re-plan rather than a worker fix.
