# reviewer (plan) for #262

Run: https://github.com/dokima-dev/dokima/actions/runs/37846993884

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #262: The checks on a pull request read exactly like its Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> The checks on a pull request should repeat its Definition of Done, in the same words and order, so I read one thing in both places. "All done-whens passed" is a leftover name and reads badly.
> 
> What I want:
> - The checks are named like the Definition of Done rows: All tests (every test in the repo), Acceptance criteria (each criterion's own tests), then Acceptance test, or End-to-end test on a feature, once #233 adds them.
> - Code review and Owner approval show alongside them, as on the card.
> - No leftover names like "done-whens" anywhere a person reads.
> - Renaming a required check must not leave pull requests stuck waiting on the old name: the change says plainly that my branch rule needs the new names at merge, and nothing merges in between

`2. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rniI "done.when" --exclude-dir=.git -l; echo; grep -rniI "done.when" --exclude-dir=.git --exclude-dir=tests | grep -v "^\.github" | head -50
```

> dokima/plan.py
> dokima/checks.py
> .github/workflows/card.yml
> .github/workflows/board.yml
> .github/workflows/done-whens.yml
> tests/test_wiki.py
> tests/test_autopilot_board.py
> tests/test_body.py
> tests/test_card.py
> tests/test_plan.py
> tests/test_checks.py
> tests/test_terms.py
> tests/test_merge_check.py
> tests/test_planner.py
> tests/samples/132/plan.json
> 
> dokima/plan.py:28:# The older words (Goal, Done when) read the same.
> dokima/plan.py:31:CRITERION_PREFIX = re.compile(r"^(?:Acceptance criteria|Acceptance criterion|Done when|Criteria|Criterion):\s*", re.I)
> dokima/checks.py:69:def annotations(junit_xml, repo, sha, done_when):
> dokima/checks.py:77:        lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -niI "done.when" tests/test_terms.py tests/test_wiki.py | head; grep -n "S<s>\|non_functional\|asks\|def check_review\|assumption" dokima/agent.py | head -60
```

> tests/test_wiki.py:16:    assert "done when" not in text.lower()
> tests/test_terms.py:8:       "  - [ ] Done when: first thing works\n"
> tests/test_terms.py:10:       "  - [ ] Done when: second thing works\n"
> 164:    if story.get("non_functional"):
> 165:        lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', '')})" for n in story["non_functional"]]
> 334:        parts += [("Non-functional requirements", bullets(h.get("non_functional"), lambda n: f"{n.get('text', '')} "
> 356:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 378:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 381:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 441:        judged = [a for a in h.get("assumptions") or [] if isinstance(a, dict)]
> 443:            lines += ["", "**The plan's assumptions:**"]
> 457:        lines += [f"- {q.get('question', '')} Assumed: {q.get('assumption', '')}" if isinstance(q, dict) else f"- {q}"
> 575:QUESTION_SHAPE = '{"question": "...?", "assumption": "..."}'
> 586:            bad.append(f"question {i} must be a question and its assumption, {QUESTION_SHAPE}")
> 588:        extra = sorted(str(k) for k in q if k not in ("question", "assumption"))
> 590:            bad.append(f"question {i} has {', '.joi

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -niI "done.when" .github/workflows/*.yml dokima/checks.py
```

> .github/workflows/board.yml:16:    workflows: [done-whens]
> .github/workflows/done-whens.yml:1:name: done-whens
> .github/workflows/done-whens.yml:12:    name: list done-whens
> .github/workflows/done-whens.yml:45:      - name: Run this done-when's tests
> .github/workflows/done-whens.yml:51:          if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi
> .github/workflows/done-whens.yml:61:    name: all done-whens passed
> .github/workflows/done-whens.yml:71:            echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
> .github/workflows/card.yml:8:    workflows: [done-whens, full suite, worker]
> dokima/checks.py:69:def annotations(junit_xml, repo, sha, done_when):
> dokima/checks.py:77:        lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner split the issue into two stories: renaming the checks to All tests and Acceptance criteria, and showing Code review and Owner approval beside them.",
          "It asked the owner three questions, about separate Code review and Owner approval checks, an Acceptance criteria circle on the card, and the order of the checks list."],
  "decided": ["The Acceptance test and End-to-end test checks are only written down in AGENTS.md; #233 builds them.",
              "Autopilot merges only when checks named All tests and Acceptance criteria both passed, and the rename pull request tells the owner to switch the branch rule when it merges."],
  "open": ["Story 2 may need the owner to give Dokima write access to checks or statuses."]
 },
 "verdict": "block",
 "summary": "The plan covers the owner's asks except one: it promises no done-when names only in a short list of places on a pull request, so a step still called \"Run this done-when's tests\" would pass, while the owner asked for none anywhere a person reads.",
 "blockers": [
  {"id": "B1", "criterion": "S1.3", "test": null,
   "problem": "The owner asked for no leftover names like done-whens anywhere a person reads. S1.3 narrows that to check names, workflow names, workflow file names, error messages and test annotations on a pull request, so a worker can leave other text a person reads, such as a workflow step name or a code name, and still pass.",
   "evidence": "Issue #262: \"No leftover names like \\\"done-whens\\\" anywhere a person reads.\" .github/workflows/done-whens.yml:45 has the step \"Run this done-when's tests\", shown in the check's run log and in none of S1.3's listed places; dokima/checks.py:69 names its parameter done_when, which the plan's own context points out but no criterion covers.",
   "fix": "Widen S1.3 to the owner's words: no text a person reads in Dokima's workflows, checks, step nam
```

> 0

**Agent:** I've blocked the plan for #262 and sent it back to the planner over one criterion. The review is at `/tmp/dokima-out/review.json`, and both checks on it pass.

**The blocker:** criterion S1.3 is narrower than what you asked for. You wrote "No leftover names like 'done-whens' anywhere a person reads." The plan only promises that in five places on a pull request: check names, workflow names, workflow file names, error messages and test annotations. A worker could pass it and still leave:
- the step "Run this done-when's tests" in `.github/workflows/done-whens.yml:45`, which shows in the check's run log;
- the `done_when` parameter name in `dokima/checks.py:69`.

The fix I proposed is to widen S1.3 to anything a person reads, and test it by searching the whole repo. The one exception is `dokima/plan.py`, which still has to recognise the older "Done when" wording in issues.

**Your asks:** all ten are matched to a criterion; none is missing.

**The planner's three questions:** I accepted none of their assumptions, so on autopilot each one will stop and wait for you.
1. **Code review and Owner approval as their own checks:** this adds two new checks and may mean giving the app write access to checks or statuses. That's your call.
2. **An Acceptance criteria circle on the card:** this changes the card on every issue, and you never asked for the card to change.
3. **No numbers in the check names:** you asked for the checks "in the same words and order". This assumption keeps the order only on the card and in AGENTS.md, not in the pull request's checks list.

**Two notes, not blockers:**
- Story 1 has six promises, one more than the split rule's limit of five.
- S1.5 promises text in the rename pull request's description. The worker doesn't write that, so its test will need to read what Dokima posts there, or the criterion should be marked manual with a reason.
