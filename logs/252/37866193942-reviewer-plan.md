# reviewer (plan) for #252

Run: https://github.com/dokima-dev/dokima/actions/runs/37866193942

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (69.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/91b76db2-29e7-4c77-9633-39071b7a4ca5/tool-results/bo7lakgxw.txt
> 
> Preview (first 2KB):
> .:
> total 88
> drwxr-xr-x  3 runner runner  4096 Oct  9 00:43 .
> drwxrwxrwt 18 root   root    4096 Oct  9 00:43 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 00:43 in
> -rw-r--r--  1 runner runner 64875 Oct  9 00:43 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 00:43 open_blockers.json
> -rw-r--r--  1 runner runner  5913 Oct  9 00:43 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  9 00:43 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 00:43 ..
> -rw-r--r-- 1 runner runner 6094 Oct  9 00:43 01-planner.json
> -rw-r--r-- 1 runner runner 3796 Oct  9 00:43 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2667 Oct  9 00:43 03-worker.json
> -rw-r--r-- 1 runner runner 3573 Oct  9 00:43 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 6575 Oct  9 00:43 05-planner.json
> # Issue #252: Once the plan passes review, code records its links on both issues and redraws both cards
> 
> <!-- dokima-card -->
> When a plan passes review, code puts its links on GitHub and on the cards of both issues.
> 
> **Review**
> 
> [issue #252](https://github.com/dokima-dev/dokima/issues/252) · [PR #290](https://github.com/dokima-dev/dokima/pull/290) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files c

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> {
>  "kind": "user_story",
>  "summary": "When a plan passes review, code puts its links on GitHub and on the cards of both issues.",
>  "user_story": "When a plan passes review, the owner sees its links on both issues: blocking ones as GitHub's own blocked-by links, and every kind on the cards of both issues, kept up to date when a later approved plan adds or drops one.",
>  "acceptance_criteria": [
>   {
>    "text": "When the reviewer approves a plan, its blocking links appear as GitHub's own blocked-by links on both issues. Blocked by goes on this issue; blocks goes on the other issue, blocked by this one. A plan the review blocks records nothing, a link GitHub already has is not added twice, and a blocking link the previous approved plan had but the new one dropped is removed. A link a person made by hand stays.",
>    "source": "https://github.com/dokima-dev/dokima/issues/252"
>   },
>   {
>    "text": "When an approved plan adds or drops any link, code redraws the cards of this issue and of every issue added or dropped. The other card shows the link from its own side: #X blocked by this issue shows Blocked by on #X's card, and relates to shows Relates to on both. It keeps showing it when that card is redrawn later, and no longer shows a dropped one. No comment is posted on the other issue for any link.",
>    "source": "https://github.com/dokima-dev/dokima/issues/252"
>   },
>   {
>    "text": "When the plan's links would make issues block each other, code records none of them and the river stops

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show 14124e7 --stat; git show 14124e7 -- tests | head -40; grep -n "^## \|^### \|^\*\*.*commented\|^---" /tmp/pack/issue.md | head -80
```

> commit 14124e728c63cf6988b3cbaab681b01b9a6b512b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 00:42:55 2026 +0000
> 
>     planner for #252 (run 37866052028)
> 
>  tests/test_plan_links_recorded.py | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> commit 14124e728c63cf6988b3cbaab681b01b9a6b512b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 00:42:55 2026 +0000
> 
>     planner for #252 (run 37866052028)
> 
> diff --git a/tests/test_plan_links_recorded.py b/tests/test_plan_links_recorded.py
> index f074c7d..d24ee62 100644
> --- a/tests/test_plan_links_recorded.py
> +++ b/tests/test_plan_links_recorded.py
> @@ -612,7 +612,7 @@ def test_links_with_no_loop_are_recorded_and_autopilot_goes_on(tmp_path, record_
>      hub = Hub(tmp_path, deps={302: [301]}, autopilot=True)
>      hub.post(plan(links([301], [302])))
>      step, comment, out = hub.next(review())
> -    assert hub.blocked_by(N) == [301] and hub.blocked_by(302) == [301, N], \
> +    assert hub.blocked_by(N) == [301] and hub.blocked_by(302) == sorted([301, N]), \
>          f"252.3: links with no loop were not recorded: #252 {hub.blocked_by(N)}, #302 {hub.blocked_by(302)}"
>      assert step == "start worker", f"252.3: autopilot should start the worker, the river said {step!r}"
>  
> 95:## Comments
> 97:### dokima-runtime on issue #252 (2026-10-08T23:57:23Z)
> 101:### dokima-runtime on issue #252 (2026-10-08T23:57:35Z)
> 283:### dokima-runtime on issue 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,96p /tmp/pack/issue.md | sed -n '/Original\|dokima-card-end\|<!-- dokima/,$p' | tail -60; PYTHONPATH=$PWD python -m pytest -q tests/test_plan_links_recorded.py 2>&1 | tail -3; git stash list >/dev/null; mkdir -p /tmp/mainwt; git worktree add -f /tmp/mainwt/m origin/main -q 2>&1|tail -1; cp tests/test_plan_links_recorded.py /tmp/mainwt/m/tests/; cd /tmp/mainwt/m && PYTHONPATH=$PWD python -m pytest -q tests/test_plan_links_recorded.py 2>&1 | grep -E "passed|failed|^FAILED" | tail -25
```

> <details><summary><b>Non-functional requirements</b></summary>
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Non-functional requirement:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37865365806/job/113610734170">Links are written only by code, from the approved plan's checked links field. Never from a rejected hand-back, a review, or a record someone pasted.</a>
>   - *<a href="https://github.com/dokima-dev/dokima/blob/5222b00cf1a1fa53497e631f146c7d5bca08ba7a/tests/test_plan_links_recorded.py#L635"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: Only the approved plan's checked links are recorded, never a review's or a pasted one.*
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Non-functional requirement:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37865365806/job/113610734124">When GitHub refuses or fails to record or remove a link, the river stops for the owner. The issue names that link and GitHub's reason, and on autopilot the worker does not start.</a>
>   - *<a href="https://github.com/dokima-dev/dokima/blob/5222b00cf1a1fa53497e631f146c7d5bca08ba7a/tests/test_plan_links_recorded.py#L655"><img src="https://raw.gi

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt/m; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Changed one 252.3 test so it checks that #302 is blocked by both #301 and #252, in any order, instead of in one order the fake GitHub never gives."
  ],
  "decided": [
   "The rest of the plan stays as approved: the same three criteria, two non-functional ones, 18 tests and links (blocks #253 and #254, relates to #269)."
  ],
  "open": [
   "Concern for the owner, unchanged: #269 would write the same links earlier, when the plan passes its check; the planner recommends #269 leaves that to this story."
  ]
 },
 "verdict": "approve",
 "summary": "The re-plan only fixes the order check the code review blocked on; the test still fails when either link is missing, and all 18 tests fail on main because nothing records links there.",
 "blockers": [],
 "notes": [
  {
   "text": "The changed test still catches a missing link: with only #301 recorded on #302 it compares [301] to [252, 301] and fails; with the worker's code on this branch all 18 tests pass.",
   "evidence": "tests/test_plan_links_recorded.py:615; `PYTHONPATH=$PWD pytest -q tests/test_plan_links_recorded.py` on try/issue-252 -> 18 passed; the same file on origin/main -> 18 failed, this one with '252.3: links with no loop were not recorded: #252 [], #302 [301]'"
  }
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {
   "ask": "once the plan passes review, code records each link on both issues using GitHub's own blocked-by relationships, so the other issue shows it too",
   "source": "https://github.com/dokima-dev/dokima/issues/231",
   "criterion": "252.1"
  },
  {
   "ask": "Nothing is recorded for a plan the review blocks, a link GitHub already has is not added twice, and a blocking link the previous approved plan had but the new approved plan dropped is removed from GitHub.",
   "source": "https://github.com/dokima-dev/dok
```

> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

**Agent:** The review is written, but the format check flagged the summary as too long. Shortening it now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The re-plan only fixes the order check the code review blocked on; the test still catches a missing link, and all 18 fail on main."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 252 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-plan for #252. My review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **What changed:** the planner changed one line, `tests/test_plan_links_recorded.py:615`. That test used to expect #302's blockers in one fixed order, and the fake GitHub in the tests never gives that order. It now checks that both links are there, in any order. This fixes the problem the code review blocked on (B1).
- **The test still proves something:** if #302 got only one of its two blockers, the test would still fail.
- **Test runs:** on this branch, with the worker's code, all 18 tests pass. On main all 18 fail, each because links aren't recorded or drawn there yet, not from a crash or a bad path.
- **Nothing else changed:** the three criteria, the two non-functional ones, the scope and the links (blocks #253 and #254, relates to #269) are the same as the plan approved before. All seven owner asks still map to a criterion.
- **No new owner input:** since the last plan review, every comment on the issue was posted by the bot. There were no open blockers at this stage.

One concern from the planner is still waiting for the owner: #269 would write the same links earlier, when the plan passes code's check rather than after review. The planner recommends that #269 drops its link writing and leaves it to this story.
