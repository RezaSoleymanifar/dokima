# reviewer (plan) for #331

Run: https://github.com/dokima-dev/dokima/actions/runs/37958794566

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (91.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/72d3e1a4-c34c-43a8-8a69-0feeaaac8f28/tool-results/bkf39e9r1.txt
> 
> Preview (first 2KB):
> .:
> total 128
> drwxr-xr-x  3 runner runner  4096 Oct  9 16:23 .
> drwxrwxrwt 18 root   root    4096 Oct  9 16:24 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 16:23 in
> -rw-r--r--  1 runner runner 91751 Oct  9 16:23 issue.md
> -rw-r--r--  1 runner runner  1401 Oct  9 16:23 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 16:23 parent.json
> -rw-r--r--  1 runner runner 13142 Oct  9 16:23 plan.json
> 
> in:
> total 60
> drwxr-xr-x 2 runner runner  4096 Oct  9 16:23 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 16:23 ..
> -rw-r--r-- 1 runner runner   838 Oct  9 16:23 01-planner.json
> -rw-r--r-- 1 runner runner  4435 Oct  9 16:23 02-planner.json
> -rw-r--r-- 1 runner runner 13174 Oct  9 16:23 03-planner.json
> -rw-r--r-- 1 runner runner  6273 Oct  9 16:23 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13817 Oct  9 16:23 05-planner.json
> # Issue #331: The board's column and pills are always computed from the issue's state right now
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 332, 333, 334 -->
> <!-- dokima-blocking: {"blocked_by": [334], "blocks": [333], "loop": []} -->
> The board puts every card in the column and pill its issue's state on GitHub gives now, on every event and every 15 minutes.
> 
> **Plan**
> 
> [issue #331](https://github.com/dokima-dev/dokima/issues/331)
> 
> <img src="https://ra

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json parent.json; echo; grep -n "^## \|^### \|^---\|^\*\*@\|^> " issue.md | head -80; wc -l issue.md
```

> [
>  {
>   "id": "B1",
>   "criterion": "331.2",
>   "test": "tests/test_board_state.py::test_the_15_minute_sweep_puts_every_card_where_its_state_says",
>   "problem": "The owner added to scope after the plan was written: the 15-minute sweep rechecks only issues and pull requests updated since the last sweep, not every open issue, and an event still rebuilds its own issue right away. No criterion keeps this; criterion 2 says the sweep sets every issue and pull request card on the board, and no test proves an untouched issue is skipped or that an updated one is rechecked.",
>   "evidence": "Owner's comment on #331 at 2026-10-09T15:42:48Z: 'Also in scope: the 15-minute sweep rechecks only issues and PRs updated since the last sweep, not every open issue, so it stays cheap on a large repo. An event still rebuilds its own issue right away.' The plan's record was posted at 15:33:37Z, before it. plan.json criterion 2: 'Every 15 minutes a sweep sets every issue and pull request card on the board'.",
>   "fix": "Rewrite criterion 2 so the 15-minute sweep rechecks only issues and pull requests updated since the last sweep, sourced to the owner's comment, and add tests: an issue updated since the last sweep is put right; one not updated is not read; an event still rebuilds its own issue at once. Ask the owner how 'since the last sweep' is remembered if that has two readings.",
>   "fixer": "planner"
>  }
> ]{"number": 330}
> 99:## Comments
> 101:### dokima-runtime on issue #331 (2026-10-09T06:25:42Z)
> 105:### 

`3. Bash`
```
cd /tmp/pack; sed -n 1,160p issue.md
```

> # Issue #331: The board's column and pills are always computed from the issue's state right now
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 332, 333, 334 -->
> <!-- dokima-blocking: {"blocked_by": [334], "blocks": [333], "loop": []} -->
> The board puts every card in the column and pill its issue's state on GitHub gives now, on every event and every 15 minutes.
> 
> **Plan**
> 
> [issue #331](https://github.com/dokima-dev/dokima/issues/331)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #334
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #330, #332, #135
> 
> **User story:** The owner sees every card on the board in the column and with the pill its issue's state on GitHub says now, whichever events were dropped or late.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:

`4. Bash`
```
cd /tmp/pack; sed -n 310,330p issue.md; sed -n 570,585p issue.md; sed -n 745,760p issue.md; sed -n 995,1009p issue.md
```

> <sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 19.1 min · 61 turns · 6,836,829 tokens in, 59,942 out · $3.81 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/331/37895128912-planner.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37895128912)</sub>
> 
> **Next:** @RezaSoleymanifar The hand-back was rejected by code, see the problems above. Fix the cause, then start the stage again.
> 
> 
> ### RezaSoleymanifar on issue #331 (2026-10-09T15:27:50Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #331 (2026-10-09T15:28:20Z)
> 
> Autopilot is on for #331. No stage was started.
> 
> 
> ### RezaSoleymanifar on issue #331 (2026-10-09T15:33:13Z)
> 
> /plan
> 
> ### dokima-runtime on issue #331 (2026-10-09T15:33:37Z)
> 
> <!-- dokima-record -->
> <sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 3.4 min · 15 turns · 3,528,193 tokens in, 12,770 out · $5.91 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/331/37952599629-planner.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37952599629)</sub>
> 
> **Next:** The reviewer starts now.
> 
> 
> ### RezaSoleymanifar on issue #331 (2026-10-09T15:42:48Z)
> 
> Also in scope: the 15-minute sweep rechecks only issues and PRs updated since the last sweep, not every open issue, so

`5. Bash`
```
cd /tmp/pack; cat plan.json; echo; python3 -c "
import json
a=json.load(open('in/03-planner.json'));b=json.load(open('in/05-planner.json'))
print(b.keys()); print(json.dumps({k:v for k,v in b.items() if k!='handback'},indent=1)[:3000])
pa=a['handback'].get('plan') or a['handback']; pb=b['handback'].get('plan') or b['handback']
print(pa==pb)
"; git -C /home/runner/work/dokima/dokima show --stat HEAD HEAD~1 | head -40
```

> {
>  "kind": "user_story",
>  "summary": "The board puts every card in the column and pill its issue's state on GitHub gives now, on every event and every 15 minutes.",
>  "user_story": "The owner sees every card on the board in the column and with the pill its issue's state on GitHub says now, whichever events were dropped or late.",
>  "acceptance_criteria": [
>   {
>    "text": "Any event about an issue or its pull request, and the end of every run that did not fail, sets both cards from its state now. So the next event fixes a dropped or late one. An open issue with no record is in Backlog; otherwise it is in the column the river placed it in after its newest record. Its pill is Needs you while it waits on the owner, else Autopilot on autopilot, else none, and its pull request goes with it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/330"
>   },
>   {
>    "text": "Every 15 minutes a sweep rechecks only the issues and pull requests updated since the last sweep that succeeded. Each comes with its pull request or issue, and nothing about any other open issue is read; an event still rebuilds its own issue at once. Closed cards go to Done with no pill from the board's own list. When GitHub lists no earlier sweep that succeeded, or cannot say when it ran or what changed since, the sweep rechecks every card.",
>    "source": "https://github.com/dokima-dev/dokima/issues/331"
>   },
>   {
>    "text": "A closed issue, and a merged or closed pull request, sits in Done with no Action pill, w

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json
r=json.load(open('in/04-reviewer-plan.json'))['handback']
print(json.dumps(r.get('asks'),indent=1)); print(json.dumps(r.get('assumptions'),indent=1)); print(json.dumps(r.get('notes'),indent=1))
"
```

> [
>  {
>   "ask": "Any event about an issue or its PR sets both cards to the column and Action pill GitHub's state gives now. So the next event fixes a dropped one.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.1"
>  },
>  {
>   "ask": "Every 15 minutes a sweep sets every issue and PR card on the board to its computed column and Action pill.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.2"
>  },
>  {
>   "ask": "A closed issue, and a merged or closed PR, sits in Done with no Action pill, whatever its labels.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.3"
>  },
>  {
>   "ask": "An issue and its PR share one board queue that keeps the newest recompute. One issue's run never cancels another issue's.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.4"
>  },
>  {
>   "ask": "The per-event board rules this replaces are removed, and the board code has fewer lines than before.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.5"
>  },
>  {
>   "ask": "A card whose state GitHub cannot give keeps its column and pill, and the run fails naming it.",
>   "source": "https://github.com/dokima-dev/dokima/issues/331",
>   "criterion": "331.6"
>  },
>  {
>   "ask": "the 15-minute sweep rechecks only issues and PRs updated since the last sweep, not every open issue, so it stays cheap on a large repo.",
>   "source": "https://github.com/dokima-dev/dokima

**Agent:** Checking the owner's answers against the new plan; running the tests next.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_board_state.py tests/test_failed_run_card.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -60
```

> Proves 331.2. The last sweep that succeeded started at 15:15; a newer sweep failed at 15:30 and an event's run
>         (only this one, running, and a failed one); GitHub refuses the list of runs; GitHub refuses the list of what
>         assert done.returncode == 0, f"331.4: `python3 -m dokima.board queue` failed on a {event} event: {done.stderr or done.stdout}"
> __ test_a_failed_run_shows_needs_you_at_once_even_when_github_cannot_be_read ___
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_a_failed_run_shows_needs_0')
>     def test_a_failed_run_shows_needs_you_at_once_even_when_github_cannot_be_read(record_property, make, monkeypatch, tmp_path):
>         """A failed run shows Needs you at once, even when GitHub cannot be read.
>         hand-back code rejected, and whose deciding step failed too (no board.txt): #63 ends in Work with Needs you. A code
>         them the good case: a plan review on #67 whose hand-back passed and decided (board.txt "Work none") keeps its card
>         rejected = {"check": {"passed": False, "problems": ["the hand-back is missing"]}, "handback": {}}
>                                                            "check": {"passed": True, "problems": []}}, "board.txt": "Work none\n"}, 1,
> FAILED tests/test_board_state.py::test_any_event_puts_both_cards_where_the_issues_state_says - AssertionError: 331.1: after a issues labeled event about #57, the cards are at {'issue #57': ('Work', None), 'pr #60': ('Done', 'Needs you')}, not {'issue #57': ('Review', 'N

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_board_state.py tests/test_failed_run_card.py -rA 2>&1 | grep PASSED; grep -n "def test_the_15_minute_sweep_rechecks_only" -A120 tests/test_board_state.py
```

> PASSED tests/test_failed_run_card.py::test_a_failed_run_lands_in_its_stage_column_with_needs_you
> PASSED tests/test_failed_run_card.py::test_a_failed_code_review_marks_the_issue_and_its_pr_even_when_deciding_failed
> PASSED tests/test_failed_run_card.py::test_a_run_that_left_nothing_behind_still_marks_its_card
> 327:def test_the_15_minute_sweep_rechecks_only_what_changed_since_the_last_sweep(record_property, make, monkeypatch):
> 328-    """Every 15 minutes the sweep rechecks only what changed since the last good sweep.
> 329-
> 330-    Proves 331.2. The last sweep that succeeded started at 15:15; a newer sweep failed at 15:30 and an event's run
> 331-    ended at 15:20, and neither counts. Updated since 15:15: #57 at 15:25 (its PR #60 not), #58's PR #61 at 15:40 (#58
> 332-    not) and #62 at 15:18. Not updated: #59 at 15:05 (after the older sweep at 15:00, before 15:15), #63 at 14:00,
> 333-    which GitHub cannot read, and #67. Every card starts in the wrong place. After the run: #57 and PR #60 in Review
> 334-    with Needs you, #58 and PR #61 in Plan with Autopilot, #62 in Backlog with no pill; closed #66, never updated,
> 335-    in Done with no pill, read from the board alone; #59, #63 and #67 left exactly where they were, with no read of
> 336-    their history, pull request or state, and the run passes though #63 cannot be read. Then a comment on #67
> 337-    arrives and puts it in Backlog with no pill at once."""
> 338-    record_property("proves", "331.2")
> 339-    wrong = {("issue", 57): ("

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def test_agents_md_says" -A25 tests/test_board_state.py; grep -n "def test_a_failed_run_shows_needs_you_at_once" -A50 tests/test_board_state.py
```

> 515:def test_agents_md_says_a_closed_item_shows_no_pill_whatever_its_labels(record_property):
> 516-    """AGENTS.md says a closed issue or PR shows no pill, whatever its labels.
> 517-
> 518-    Proves 331.3. Reads AGENTS.md's board section: one sentence must say that a closed issue, and a merged or closed
> 519-    pull request, shows no pill (neither Needs you nor Autopilot) whatever its labels, and the old rule that the merge's
> 520-    sweep puts Autopilot on every item on autopilot "open or closed" must be gone."""
> 521-    record_property("proves", "331.3")
> 522-    section = board_section()
> 523-    assert "open or closed" not in section, \
> 524-        "331.3: AGENTS.md still says the merge's sweep puts Autopilot on items on autopilot, open or closed"
> 525-    said = [x for x in re.split(r"(?<=\.)\s", section)
> 526-            if re.search(r"\bclosed\b", x) and re.search(r"\bpull request\b", x) and re.search(r"\bno (Action )?pill\b", x)
> 527-            and "whatever its labels" in x]
> 528-    assert said, ("331.3: AGENTS.md's board section has no sentence saying a closed issue or pull request shows no pill "
> 529-                  "whatever its labels")
> 530-
> 531-
> 532-# 331.4: an issue and its pull request share one board queue that keeps the newest recompute
> 533-
> 534-def queue_of(event, payload, tmp_path):
> 535-    """The board queue `python3 -m dokima.board queue` names for this event, read from GITHUB_OUTPUT's group=."""
> 536-    path, out = tmp_path / "event.json", tmp_path / "outpu

`10. Bash`
```
cd /tmp/pack; grep -o "issuecomment-[0-9]*" issue.md | sort -u | head; grep -n "AGENTS.md\|board section" /home/runner/work/dokima/dokima/tests/test_board_state.py | head -5
```

> 510:    """AGENTS.md's "The board" section, as one paragraph of text."""
> 511:    text = open(os.path.join(ROOT, "AGENTS.md")).read()
> 516:    """AGENTS.md says a closed issue or PR shows no pill, whatever its labels.
> 518:    Proves 331.3. Reads AGENTS.md's board section: one sentence must say that a closed issue, and a merged or closed
> 524:        "331.3: AGENTS.md still says the merge's sweep puts Autopilot on items on autopilot, open or closed"
> Shell cwd was reset to /home/runner/work/dokima/dokima

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote criterion 2 so the 15-minute sweep rechecks only issues and pull requests updated since the last sweep that succeeded, and added two tests for it.",
          "It added AGENTS.md's board section to criterion 3, saying a closed issue or pull request shows no pill whatever its labels.",
          "It added to the non-functional rule that a failed run shows Needs you on its cards at once, even when GitHub cannot be read."],
  "decided": ["'Since the last sweep' counts from the start of the last board sweep that succeeded, read from GitHub's list of the board workflow's runs; with none, or when GitHub refuses either list, the sweep rechecks every card."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now keeps all of your asks, including the cheaper 15-minute sweep and both answers from your last comment, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 2 settles how 'since the last sweep' is remembered (the start of the last board run that succeeded) without asking; it follows from your words and fails safe to a full sweep, so it is not a guess that could hide a card.",
   "evidence": "plan.json criterion 331.2; tests/test_board_state.py::test_with_no_sweep_to_count_from_the_sweep_rechecks_every_card covers no earlier sweep, refused runs and refused changes."},
  {"text": "AGENTS.md's wording is checked by matching a sentence in the board section, which is the right proof for a docs change but only proves the sentence, not the behavior; the behavior is proven by the other two 331.3 tests.",
   "evidence": "tests/test_board_state.py:515-529"}
 ],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "Any event about an issue or its PR sets both cards to the column and Action pill GitHub's state gives now. So the next event fixes a dropped one.", "source": "https://
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`12. Bash`
```
python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="The plan now keeps every ask, including the cheaper 15-minute sweep and both answers in your last comment, and each new test fails today."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 331 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #331. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **Last round's blocker (B1) is fixed.** Criterion 2 now says the 15-minute sweep rechecks only issues and PRs updated since the last sweep, and that an event still rebuilds its own issue right away. Two new tests prove it:
  - Only issues updated since the last sweep are put right.
  - An issue that wasn't updated is never read.
  - A later comment on that issue still fixes its card at once.
  - When there's no earlier sweep, or GitHub refuses either list, the sweep checks every card.
- **Both answers in your 16:08 comment made it into the plan:**
  - **Closed items show no pill:** criterion 3 now says a closed issue or PR gets no pill whatever its labels, and requires AGENTS.md's board section to say so. A test checks that wording.
  - **Failed runs show Needs you right away:** the non-functional rule now says a failed run puts Needs you on its cards at once, even when GitHub can't be read. A test covers a worker, a code review and a planner run, plus a run that didn't fail, for contrast.
- **Your asks:** all ten are matched to a criterion; none are missing.
- **Tests:** I ran them. All 19 new tests fail today because the feature isn't built yet, not from crashes or bad paths. The 3 existing failed-run tests from #132 still pass.

**Your call:** the planner decided how "since the last sweep" is counted without asking you. It counts from the start of the last sweep that succeeded, and falls back to checking every card when GitHub can't say. That fits your words and errs toward checking more, so I accepted it. I've left it as a note in the review rather than a blocker.
