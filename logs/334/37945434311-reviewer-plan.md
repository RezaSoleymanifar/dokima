# reviewer (plan) for #334

Run: https://github.com/dokima-dev/dokima/actions/runs/37945434311

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (54.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9b520c13-49c9-42da-8cd3-beeeaf7e04b3/tool-results/bawvwg4d8.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  9 14:36 .
> drwxrwxrwt 18 root   root    4096 Oct  9 14:36 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 14:36 in
> -rw-r--r--  1 runner runner 45585 Oct  9 14:36 issue.md
> -rw-r--r--  1 runner runner  2890 Oct  9 14:36 open_blockers.json
> -rw-r--r--  1 runner runner  6727 Oct  9 14:36 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner 4096 Oct  9 14:36 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 14:36 ..
> -rw-r--r-- 1 runner runner 3055 Oct  9 14:36 01-planner.json
> -rw-r--r-- 1 runner runner 6620 Oct  9 14:36 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7433 Oct  9 14:36 03-planner.json
> # Issue #334: A split story may point to my words in its parent issue
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A story split from a bigger issue may cite the owner's words in its parent issue, and code accepts it.
> 
> **Plan**
> 
> [issue #334](https://github.com/dokima-dev/dokima/issues/334)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #331
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="rel

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json; echo; grep -n "dokima-card\|^---\|^## \|^### \|Original\|owner\|^\*\*" issue.md | head -80
```

> [
>  {
>   "id": "B1",
>   "criterion": "334.1",
>   "test": null,
>   "problem": "The owner changed the scope after this plan: a criterion's source may be anywhere in this repo, not only the story's own issue or its parent. The plan still allows only the own issue and the parent, and 334.2 still rejects every other issue, which the owner's new words now permit.",
>   "evidence": "Owner's comment on #334 at 2026-10-09T14:17:50Z: \"/plan Change of scope: a criterion's source may be anywhere in this repo, not only the parent.\" plan.json criteria 1 and 2 and out_of_scope (\"The parent's parent, or any issue further up the tree, does not count as a source\") contradict it.",
>   "fix": "Re-plan: a criterion's source may be any issue in this repo or a comment on one; replace 334.2's 'any other issue is rejected' with what is still rejected (a source outside this repo, or words the owner did not write), with a passes-the-good-case test beside each rejection.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "334.2",
>   "test": null,
>   "problem": "The owner asked code to check that the source was written by the owner and that the quoted words are really there; no criterion or test covers this.",
>   "evidence": "Owner's comment at 2026-10-09T14:17:50Z: \"Code checks that the source was written by me and that the quoted words are really there.\" No criterion in plan.json mentions authorship or quoted words.",
>   "fix": "Add a criterion with tests: a source whose text or comment was not writt

`3. Bash`
```
cd /tmp/pack; sed -n 52,80p issue.md; sed -n 220,250p issue.md; sed -n 600,900p issue.md | grep -v "^\s*$" | head -150
```

> <!-- dokima-ask -->
> 
> A story split from a bigger issue can't point to my words. On #331 the planner linked its criteria to #330, the parent issue where I wrote them, and code rejected the plan twice because a source must be the story's own issue or one of its comments.
> 
> What I want:
> - A criterion's source may be the story's own issue, its parent issue, or a comment on either.
> - Any other issue is still rejected, naming the criterion and the source.
> - The reviewer's check that my words were really said there accepts the parent too.
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #334 (2026-10-09T14:15:10Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #334 (2026-10-09T14:15:33Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #334 (2026-10-09T14:15:35Z)
> 
> Autopilot is on for #334. Planning started for #334, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #334 (2026-10-09T14:15:45Z)
> 
> <!-- dokima-record -->
> 
> 
> ### RezaSoleymanifar on issue #334 (2026-10-09T14:17:50Z)
> 
> /plan Change of scope: a criterion's source may be anywhere in this repo, not only the parent. Code checks that the source was written by me and that the quoted words are really there. The reviewer checks it is my latest word on that point, so the reviewer's starter pack gets the same open-issues list the planner gets, plus the full text and comments of every issue a plan cites. Wider context like closed issues and PR comments can come later.
> 
> ### dokima-runtime on issue #334 (2026-10-09T1

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['01-planner.json','02-reviewer-plan.json','03-planner.json']:
    d=json.load(open('in/'+f)); print(f, {k:(v if k!='handback' else '...') for k,v in d.items()})
"; cd /home/runner/work/dokima/dokima; git log --format='%h %ad %s' --date=iso -5; git show --stat HEAD | head -20
```

> 01-planner.json {'role': 'planner', 'stage': None, 'run_id': '37942837033', 'commit_before': 'e934cfe776d407a74874661164ad0718617dae63', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 344731, 'turns': 30, 'cost_usd': 2.0793978, 'tokens_in': 2263267, 'tokens_out': 36484}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/334/37942837033-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/37942837033', 'handback': '...', 'check': {'passed': True, 'problems': []}}
> 02-reviewer-plan.json {'role': 'reviewer', 'stage': 'plan', 'run_id': '37943645525', 'commit_before': '15673a5210c5493feb86d6e4aef54aa354cea9c0', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 40766, 'turns': 7, 'cost_usd': 0.32346440000000004, 'tokens_in': 232242, 'tokens_out': 4010}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/334/37943645525-reviewer-plan.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/37943645525', 'handback': '...', 'check': {'passed': True, 'problems': []}}
> 03-planner.json {'role': 'planner', 'stage': None, 'run_id': '37943810996', 'commit_before': '15673a5210c5493feb86d6e4aef54aa354cea9c0', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 727222, 'turns': 40, 'cost_usd': 3.6016044000000003, 'tokens_in': 4807006, 'tokens_out': 64874}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/334/379

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_parent_source.py 2>&1 | tail -15; git diff 15673a5 HEAD -- tests/test_autopilot_river.py
```

> assert False
>  +  where False = <function exists at 0x7f02c91ef600>('/tmp/pytest-of-runner/pytest-0/test_the_plan_reviewers_pack_h0/reviewer/pack/open_issues.json')
>  +    where <function exists at 0x7f02c91ef600> = <module 'posixpath' (frozen)>.exists
>  +      where <module 'posixpath' (frozen)> = os.path
> FAILED tests/test_parent_source.py::test_the_plan_reviewers_pack_holds_every_cited_issue_in_full - AssertionError: 334.7: the plan reviewer's pack lacks 'A second paragraph of the parent.' from #330, which the plan cites
> assert 'A second paragraph of the parent.' in '{\n "kind": "feature",\n "summary": "Two stories.",\n "feature": "Cards show what is true now.",\n "stories": [\n  {\...ues/331"}]}], "links": {"blocked_by": [], "blocks": [], "relates_to": []}}, "check": {"passed": true, "problems": []}}'
> FAILED tests/test_parent_source.py::test_the_reviewers_prompt_asks_it_to_check_the_owners_latest_word - AssertionError: 334.8: the reviewer's prompt does not ask it to check the owner's latest word
> assert 'latest word' in "# where you are you are dokima's reviewer for one github issue. in dokima nothing merges until it is proven. a planne...e owner: you judge from the records, and a disagreement that survives three rounds reaches the owner as an escalation."
> FAILED tests/test_parent_source.py::test_when_github_cannot_give_a_cited_issues_words_nothing_counts - AssertionError: 334.9: with GitHub failing to give the cited #300, the pack built anyway or did not name #300 (exit 0): '

**Agent:** The plan I'm reviewing follows the owner's wider-scope comments, which the owner withdrew at 14:24, so I'm writing a block.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner re-planned one user story: a criterion may cite the owner's words in any issue of this repo, code checks a code owner wrote them and the quote is really there, and the plan reviewer's pack gets the open-issues list and every cited issue in full."],
  "decided": ["Closed issues and pull requests are rejected as sources for now; the story's own issue is checked as today."],
  "open": ["The plan was written before the owner's comment that goes back to the small fix and parks the wider version."]
 },
 "verdict": "block",
 "summary": "This plan builds the wider version the owner has since withdrawn; it must go back to the small fix: own issue, parent issue, or a comment on either, and nothing else.",
 "blockers": [
  {"id": "B4", "criterion": "334.1", "test": "tests/test_parent_source.py::test_a_criterion_may_cite_the_owners_words_in_any_issue_of_this_repo",
   "problem": "The owner replaced the wider scope with the small fix, but the plan still accepts any issue of this repo as a source, so a criterion citing an unrelated issue would pass where the owner said it must be rejected.",
   "evidence": "Owner's comment at 2026-10-09T14:24:33Z: \"/plan Back to the small fix, replacing my two comments above: a criterion's source may be the story's own issue, its parent issue, or a comment on either. Anything else is still rejected. Keep it one user story. The wider version is parked in its own issue.\" plan.json criterion 1 says \"citing any issue of this repo\"; the test change in tests/test_autopilot_river.py turns the 'another issue' rejection (o/r/issues/58) into 'another repo', so a different issue of this repo is no longer proven rejected.",
   "fix": "Re-plan to the issue's three asks: (1) the planner's check accepts the own issue, the parent issue, or a comment on either; (2) any other issue, including another issue of this repo, is rejected naming the criter
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="This plan builds the wider version the owner withdrew; it must return to the small fix: own issue, parent issue, or a comment on either."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 334 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #334. It builds the wider version of the fix, which you withdrew in your comment at 14:24:33. I wrote the review to `/tmp/dokima-out/review.json` and it passes both checks.

**Why it's blocked:**
- **B4:** The plan accepts any issue in this repo as a source. You said a source may only be the story's own issue, its parent issue, or a comment on either, and "Anything else is still rejected." The plan also edits a test in `tests/test_autopilot_river.py` so that a different issue in this repo is no longer proven to be rejected. The fix is to go back to the issue's three asks and undo that test edit.
- **B5:** Five criteria and both fail-closed items come only from the comments you replaced: the check that you wrote the words, the check that the quote is really there, the fuller reviewer pack, and the "latest word" instruction to the reviewer. The fix is to drop them and their tests, and take `dokima/roles/` out of scope.

**Other parts of the review:**
- **Earlier blockers:** B1, B2 and B3 are marked resolved. They asked for the wider scope you have since withdrawn, so they no longer apply.
- **Your asks:** Two of your asks have no criterion in this plan: "Any other issue is still rejected" and your "Back to the small fix" comment.
- **The plan's two questions:** I did not accept either assumption. Both are about the work you parked.
- **Tests:** I ran the planner's new tests and all 12 fail today, but they test the withdrawn version, so they can't be kept as they are.

The plan I reviewed is the one committed on this branch. The planner run started by your 14:24:33 comment (run 37943956132) has not committed anything to the branch yet. Its plan may already be the small fix.
