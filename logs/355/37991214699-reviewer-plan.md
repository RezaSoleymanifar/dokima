# reviewer (plan) for #355

Run: https://github.com/dokima-dev/dokima/actions/runs/37991214699

`1. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #355: AGENTS.md: every issue reference is a link plus a few plain words
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #355](https://github.com/dokima-dev/dokima/issues/355)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> AGENTS.md says: whenever an agent or assistant refers the owner to an issue or pull request, it writes the number as a clickable link followed by a few plain words saying what it is about, e.g. [#289](https://github.com/dokima-dev/dokima/issues/289) (raises and answers). Never a bare number.
> 
> Owner's words (2026-10-09): "these numbers are g

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_issue_refs_rule.py; python -m pytest -q tests/test_issue_refs_rule.py 2>&1 | tail -30; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); print(d.keys())"
```

> """AGENTS.md tells agents to name an issue with a link and a few plain words.
> 
> Issue #355 asks for a rule in AGENTS.md: whenever an agent or assistant refers the owner to an issue or pull request,
> it writes the number as a clickable link followed by a few plain words saying what it is about, never a bare number,
> with the owner's example. These tests read AGENTS.md and look for one paragraph or bullet that states the whole rule,
> and for the example as a real markdown link. Matching ignores case, line breaks and repeated spaces inside a
> paragraph, so the worker may wrap lines freely.
> """
> import os
> import re
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> EXAMPLE = "[#289](https://github.com/dokima-dev/dokima/issues/289) (raises and answers)"
> 
> 
> def blocks():
>     """Returns AGENTS.md split into paragraphs and bullets, each flattened to one lower-case line."""
>     text = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
>     parts = re.split(r"\n\s*\n|\n(?=\s*[-*] )", text)
>     return [re.sub(r"\s+", " ", part).strip().lower() for part in parts if part.strip()]
> 
> 
> def test_rule_says_link_plus_plain_words_never_bare(record_property):
>     """AGENTS.md says every issue reference is a link plus plain words, never a bare number.
> 
>     Looks for one paragraph or bullet of AGENTS.md that says, together, that an agent or assistant referring the owner
>     to an issue or pull request writes the number as a clickable link, followed by a few plain words saying what it is
>     a

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -ln "AGENTS.md" tests/*.py | head; python -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: baep859fg). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/70752200-0e3a-48c9-a68f-f1628020bd7e/tasks/baep859fg.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -ln "AGENTS.md" tests/*.py | head
```

> tests/test_autopilot.py
> tests/test_blocked_worker.py
> tests/test_answered_questions.py
> tests/test_run_cards.py
> tests/test_automerge.py
> tests/test_issue_refs_rule.py
> tests/test_autopilot_river.py
> tests/test_board_state.py
> tests/test_design.py
> tests/test_start.py

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "AGENTS" tests/test_design.py | head -20
```

> 8:    text = open(os.path.join(ROOT, "AGENTS.md")).read()
> 10:        assert heading in text, f"78.1: AGENTS.md is missing {heading}"
> 12:    assert not os.path.exists(os.path.join(ROOT, "DESIGN.md")), "78.1: the design must live only in AGENTS.md"
> 17:    assert open(os.path.join(ROOT, "CLAUDE.md")).read().strip() == "@AGENTS.md", "78.2: CLAUDE.md must only point to AGENTS.md"

**Agent:** Both new tests fail today for the right reason: the rule isn't in AGENTS.md yet. Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned one change to AGENTS.md: a rule that every issue or pull request named to the owner is a clickable link plus a few plain words, never a bare number, with the owner's #289 example.",
          "The planner wrote two tests that read AGENTS.md for the whole rule in one paragraph and for the example as a real link."],
  "decided": ["Cards, records and Autopilot lines that code writes stay as they are; only what agents and assistants tell the owner is covered.",
              "The issue numbers AGENTS.md already mentions and the role prompts stay unchanged."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers everything the owner asked for, and both tests fail today only because AGENTS.md doesn't have the rule yet.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 1 adds that the rule sits in one place. The owner didn't ask for that. It only shapes where the worker writes the rule, so it lets the test check the whole rule together.",
   "evidence": "plan.json acceptance_criteria[0]; tests/test_issue_refs_rule.py::test_rule_says_link_plus_plain_words_never_bare picks the single best-matching paragraph"},
  {"text": "Test 355.1 needs the owner's own phrases word for word ('agent or assistant', 'refers the owner to an issue or pull request', 'clickable link', 'a few plain words', 'what it is about', 'never a bare number'). A rule that drops any part turns it red. The worker has to keep the owner's wording.",
   "evidence": "pytest -q tests/test_issue_refs_rule.py on try/issue-355: 2 failed, 355.1 lacking all six phrases and 355.2 'AGENTS.md has no paragraph saying never a bare number'"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "whenever an agent or assistant refers the owner to an issue or pull request, it writes the number as a clickable link followed by a few plain words saying what it is abou
```

> (Bash completed with no output)

**Agent:** I approved the plan for issue #355, which adds a rule to AGENTS.md that any issue or pull request named to you is a clickable link plus a few plain words. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **Asks covered:** I found five asks in your words on the issue. Each one maps to one of the plan's two criteria, and none is missing:
  - a link with a few plain words saying what the issue is about;
  - never a bare number;
  - put the rule in AGENTS.md;
  - add the link too;
  - your #289 "(raises and answers)" example.
- **Tests:** I ran the two new tests on `try/issue-355`. Both fail today because AGENTS.md doesn't have the rule yet, which is the right reason. They require your own phrases word for word, all in one paragraph, and the #289 example written as a real link. Leaving out any part of the rule makes them fail.
- **Notes (not blocking):**
  - Criterion 1 adds that the rule must sit in one place. You didn't ask for that; it only lets the test check the whole rule together.
  - The worker has to keep your exact wording, or the test fails.
- **Out of scope, by the planner's choice:** comments and cards written by code, the issue numbers AGENTS.md already mentions (#205, #164), and the role prompts. Your issue text says "agent or assistant" and asks for the rule in AGENTS.md, so this reading fits your words.

I also started a run of the full test suite as a side check. It didn't finish within the two-minute limit, so I don't have its result; the review doesn't depend on it.

`7. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/70752200-0e3a-48c9-a68f-f1628020bd7e/tasks/baep859fg.output
```

> FAILED tests/test_issue_refs_rule.py::test_rule_carries_the_owners_example - AssertionError: 355.2: AGENTS.md has no paragraph saying 'never a bare number', so the example has no rule to sit in
> assert []
> 2 failed, 740 passed, 83 skipped in 174.48s (0:02:54)
> 
> [exited with code 0]

**Agent:** The full test suite finished: 740 passed, 83 skipped and 2 failed. The 2 failures are the two new tests for issue #355 (the link-and-plain-words rule), which should fail until AGENTS.md has the rule. No existing test breaks, so my approval of the plan stands.
