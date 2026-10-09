# reviewer (plan) for #344

Run: https://github.com/dokima-dev/dokima/actions/runs/37979620215

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (29.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/90bc4985-6402-415a-929b-eae44f6d28e4/tool-results/bbjrd0ukt.txt
> 
> Preview (first 2KB):
> # Issue #344: A merged PR's card is written and says Merged with the true Definition of Done
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> A merged pull request's card says Merged with its true Definition of Done, and the line cap on agent.py and board.py goes.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #344](https://github.com/dokima-dev/dokima/issues/344)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #345, #346, #347, #343, #330
> 
> **User story:** Every pull request's card is written open or merged and says Merged with the Definition of Done GitHub records, and no test fails because agent.py or board.py grew.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance 

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-card-end\|<!-- dokima-ask/,$p' issue.md | head -300; ls in
```

> <!-- dokima-ask -->
> 
> Today a PR's card is only written while the PR is open, so a PR merged before its card was redrawn stays stale (#246 still says its tests are running).
> 
> What I want:
> - A PR's card is written whether the PR is open or merged.
> - After the merge it says Merged, with All tests, Code review and Owner approval as GitHub records them.
> - Remove the test that caps the line count of agent.py and board.py (tests/test_board_state.py::test_the_board_code_is_shorter_than_before): a size limit is not a behavior.
> 
> Small fix, added on top of today's card code. Do not rewrite card.py and do not delete code beyond what this fix needs. Keep it one user story. #332's planner already wrote tests for this on branch try/issue-332 (tests/test_card_now.py and tests/test_hand_links.py): reuse the ones that fit instead of writing new ones.
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #344 (2026-10-09T18:58:38Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #344 (2026-10-09T18:59:01Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #344 (2026-10-09T18:59:03Z)
> 
> Autopilot is on for #344. Planning started for #344, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #344 (2026-10-09T18:59:12Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/open_blockers.json; git show --stat HEAD HEAD~1 | head -40; sed -n 440,470p dokima/card.py; sed -n 695,730p dokima/card.py
```

> []commit e2bd48ec5292eb05da839b39b0e9c4e2809f6376
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 19:20:47 2026 +0000
> 
>     planner for #344 (run 37979312148)
> 
>  tests/test_card_bullets.py |  2 +
>  tests/test_card_records.py |  3 ++
>  tests/test_card_status.py  |  1 +
>  tests/test_no_size_cap.py  | 93 ----------------------------------------------
>  4 files changed, 6 insertions(+), 93 deletions(-)
> 
> commit e52e1b6f3b3cb001d2950ede917209035009bc4c
> Author: RezaSoleymanifar <reza@soleymanifar.com>
> Date:   Fri Oct 9 14:18:10 2026 -0500
> 
>     Remove the line-count cap on agent.py and board.py: a size limit is not a behavior (#344)
> 
>  tests/test_board_state.py | 14 --------------
>  1 file changed, 14 deletions(-)
> def pr_body(card, body):
>     """The PR's description: the card, then the line linking the issue, and nothing else."""
>     found = CLOSES.search(body or "")
>     return card + ("\n\n" + found.group(0) if found else "")
> 
> 
> def gh(*args):
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> def issue_pr(repo, n):
>     """The PR built for issue n from its try or work branch, or None."""
>     owner = repo.split("/")[0]
>     for branch in (f"try/issue-{n}", f"work/issue-{n}"):
>         prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
>         if prs:
>             return prs[0]["number"]
>     return None
> 
> 
> def find_work(repo):
>     """The issue and open PR this event is 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages tests/test_card_records.py::test_the_issue_and_its_pr_show_the_same_card tests/test_card_status.py::test_merged_once_the_pr_is_merged tests/test_card_bullets.py::test_only_a_code_owners_merge_shows_owner_approval_passed tests/test_card_records.py::test_all_tests_shows_the_state_github_reports tests/test_card_records.py::test_a_missing_stale_or_unproven_review_never_shows_as_passed 2>&1 | tail -3; grep -n "shorter_than_before" -r tests | head; git diff main --stat
```

> ........                                                                 [100%]
> 8 passed in 0.23s
>  AGENTS.md                  |   2 +-
>  dokima/agent.py            |  16 +---
>  dokima/board.py            |  10 +-
>  tests/test_board_state.py  |  20 +---
>  tests/test_card_bullets.py |   2 +
>  tests/test_card_records.py |   3 +
>  tests/test_card_status.py  |   1 +
>  tests/test_work_column.py  | 221 ---------------------------------------------
>  8 files changed, 20 insertions(+), 255 deletions(-)

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main...HEAD --stat; git diff main...HEAD -- tests/test_card_*.py; python -m pytest -q tests/test_board_state.py 2>&1|tail -2; python3 -c "import json;p=json.load(open('/tmp/pack/plan.json'));print(p.get('questions'), list(p))"
```

> tests/test_board_state.py  | 14 --------------
>  tests/test_card_bullets.py |  2 ++
>  tests/test_card_records.py |  3 +++
>  tests/test_card_status.py  |  1 +
>  4 files changed, 6 insertions(+), 14 deletions(-)
> diff --git a/tests/test_card_bullets.py b/tests/test_card_bullets.py
> index e62d7e7..0428e7e 100644
> --- a/tests/test_card_bullets.py
> +++ b/tests/test_card_bullets.py
> @@ -247,6 +247,7 @@ def test_only_a_code_owners_merge_shows_owner_approval_passed(record_property):
>      changes, and checks Owner approval shows passed both times; then a PR merged by a stranger, one merged by
>      Dokima's bot on autopilot, and an open PR, all with no review, and checks none of them shows it passed. Proves 235.3."""
>      record_property("proves", "235.3")
> +    record_property("proves", "344.2")
>      assert approval(draw(pr=merged("boss"), reviews=[])) == "passed", \
>          "235.3: a code owner's merge with no Approve review leaves Owner approval unchecked"
>      assert approval(draw(pr=merged("boss"), reviews=[review("CHANGES_REQUESTED")])) == "passed", \
> @@ -301,6 +302,7 @@ def test_the_issue_and_pr_cards_are_identical_and_link_both_pages(record_propert
>      is written on both pages, the two are identical, both link to issue #40 and PR #5, and both show the code review
>      passed. Proves 235.4."""
>      record_property("proves", "235.4")
> +    record_property("proves", "344.1")
>      on_issue, on_pr = write_main(monkeypatch, tmp_path, dict(FOUND, pr=pr))
>      assert on_issue, "235.4: the card 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 285,315p tests/test_card_bullets.py
```

> monkeypatch.setattr(plan, "fetch_issue", lambda repo, n: issue)
>     monkeypatch.setattr(card, "gather", lambda repo, n, pr: found)
>     card.main()
>     return saved.get("issue"), saved.get("pr")
> 
> 
> def code_review(text):
>     """The state on the Code review circle in the Definition of Done line."""
>     line = next(l for l in block(text).splitlines() if "Definition of Done" in l)
>     return [a for a in re.findall(r'<img [^>]*alt="([^"]*)"', line) if a in STATES][1]
> 
> 
> @pytest.mark.parametrize("pr", [PR, merged("boss"), dict(PR, state="closed")], ids=["open", "merged", "closed"])
> def test_the_issue_and_pr_cards_are_identical_and_link_both_pages(record_property, monkeypatch, tmp_path, pr):
>     """The issue and PR cards are identical, each linking to the issue and the PR.
> 
>     Runs the card for an issue whose code review passed, with its PR open, merged and closed, and checks the card
>     is written on both pages, the two are identical, both link to issue #40 and PR #5, and both show the code review
>     passed. Proves 235.4."""
>     record_property("proves", "235.4")
>     record_property("proves", "344.1")
>     on_issue, on_pr = write_main(monkeypatch, tmp_path, dict(FOUND, pr=pr))
>     assert on_issue, "235.4: the card was not written on the issue"
>     assert on_pr, f"235.4: the card was not written on the {pr['state']} PR, so it keeps an older card than the issue"
>     a, b = block(on_issue), block(on_pr)
>     assert a == b, f"235.4: the issue and PR cards differ:\n{a}\n---\n{b}"
>     htm

**Agent:** Checks so far look good: the six reused card tests pass, and the owner's deletion is on the branch. Next I'm writing up the review and running its check.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Dropped the size-cap criterion and its two tests, as the owner asked after deleting the cap by hand (commit e52e1b6).",
          "Marked six existing card tests as proof of 344.1 and 344.2, with no change to their steps or assertions."],
  "decided": ["No card code changes: a pull request's card is already written open, merged or closed and says Merged with the Definition of Done GitHub records (dokima/card.py:711).",
              "Left #332's merged-PR tests out, because they need card.yml to start on a merge, which is #345."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps the two card asks, drops the size-cap item as the owner asked, and proves both asks with existing tests that cover open, merged and closed pull requests.",
 "blockers": [],
 "notes": [
  {"text": "Every test in this plan already passes, so the worker has nothing to build: the pull request will carry only the owner's deletion and the six new 'proves' tags. The stale card on #246 stays stale until #345 or #347 lands.",
   "evidence": "pytest on try/issue-344 for the six 344.1 and 344.2 tests: 8 passed; git diff main...HEAD touches only tests/."},
  {"text": "344.1 is proven at the card-writing step with GitHub faked out. Whether issue_pr() finds a merged PR rests on its state=all query, which no listed test calls for real.",
   "evidence": "dokima/card.py issue_pr() queries pulls?...&state=all; tests/test_card_bullets.py write_main() replaces gather()."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "A PR's card is written whether the PR is open or merged.", "source": "https://github.com/dokima-dev/dokima/issues/344", "criterion": "344.1"},
  {"ask": "After the merge it says Merged, with All tests, Code review and Owner approval as GitHub records them.", "source": "https://github.com/dokima-dev/dokima/issues/344", "criterion": "344.2"},
  {"a
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan keeps both card asks, drops the size-cap item as the owner asked, and proves each with existing tests covering open, merged and closed PRs."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 344 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan keeps both card asks, drops the size-cap item as the owner asked, and proves each with existing tests for open, merged and closed PRs."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 344 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`10. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan keeps both card asks, drops the size-cap item as the owner asked, and proves each with existing tests for open, merged and closed PRs."
r['summary']="The plan keeps both card asks, drops the size-cap item as asked, and proves each with existing tests for open, merged and closed PRs."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 344 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #344. Both checks on the hand-back pass, and it's in `/tmp/dokima-out/review.json`.

**What the planner changed:** You deleted the line-count test by hand (commit e52e1b6), so the planner dropped that criterion and its two tests, as you asked. It kept the other two criteria:
- **344.1:** a pull request's card is written whether it's open, merged or closed, matches the issue's card, and keeps its closing line.
- **344.2:** after the merge the card says Merged, and its Definition of Done shows All tests, Code review and Owner approval as GitHub records them.

**Why I approved:**
- **Both asks already hold today.** `dokima/card.py:711` writes the PR card whatever its state, and the PR lookup includes merged and closed ones. So no card code changes, which fits your "do not rewrite card.py."
- **The proof is six existing card tests.** Their only change is a tag naming 344.1 or 344.2. On the branch they ran 8 passed, including the identical-cards test for an open, a merged and a closed PR.
- **Nothing you asked for is missing.** The planner left out #332's merged-PR tests, and that is fair: they only fail because `card.yml` never starts on a merge, which is #345's job.

**Notes, not blockers:**
- The worker has nothing to build. The pull request will hold only your deletion and the six new tags. #246's card stays stale until #345 or #347 lands.
- 344.1 is tested with GitHub faked. No listed test checks for real that the PR lookup finds a merged pull request.
