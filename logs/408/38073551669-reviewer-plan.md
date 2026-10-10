# reviewer (plan) for #408

Run: https://github.com/dokima-dev/dokima/actions/runs/38073551669

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct 10 17:53 .
> drwxrwxrwt 18 root   root    4096 Oct 10 17:54 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 17:53 in
> -rw-r--r--  1 runner runner 14541 Oct 10 17:53 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 17:53 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 17:53 parent.json
> -rw-r--r--  1 runner runner  4116 Oct 10 17:53 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner 4096 Oct 10 17:53 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 17:53 ..
> -rw-r--r-- 1 runner runner 4743 Oct 10 17:53 01-planner.json
> -rw-r--r-- 1 runner runner  370 Oct 10 17:53 02-not-started.json
> # Issue #408: A PR that cannot be updated with main gets one comment, updated in place
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A pull request that cannot be updated with main keeps one bot comment about it, edited in place, instead of a new one per merge.
> 
> **Work** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Fix why nothing ran
> 
> https://github.com/dokima-dev/dokima/issues/408
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #376
> 
> **User story:** When GitHub refuses to bring a pull request up to date with main, the owner sees one comment on it that always shows the new

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/in/01-planner.json | head -c 2500; echo; git show --stat HEAD | head -20; cat dokima/uptodate.py
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38062103512",
>  "commit_before": "e02bcb264bf540a81ee342e4d6eb36435fcaa4fa",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 200876,
>   "turns": 13,
>   "cost_usd": 1.0893472,
>   "tokens_in": 723749,
>   "tokens_out": 21802
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/408/38062103512-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38062103512",
>  "handback": {
>   "kind": "user_story",
>   "summary": "A pull request that cannot be updated with main keeps one bot comment about it, edited in place, instead of a new one per merge.",
>   "user_story": "When GitHub refuses to bring a pull request up to date with main, the owner sees one comment on it that always shows the newest main commit and GitHub's reason, and that same comment says so once the pull request updates cleanly again.",
>   "acceptance_criteria": [
>    {
>     "text": "A pull request refused on several merges in a row carries exactly one refusal comment, showing the newest main commit and GitHub's newest reason. It is posted on the first refusal and edited after, and names no older commit.",
>     "source": "https://github.com/dokima-dev/dokima/issues/408"
>    },
>    {
>     "text": "A pull request that already carries several refusal comments, as #287 does, gets no new one on its next refusal. Its newest refusal comment is edited to the newest commit and reason, the bot's older refusal commen

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat -n tests/test_uptodate_once.py; git show HEAD -- tests/test_uptodate.py
```

> 1	"""A PR that cannot be updated with main carries one comment, edited in place (#408).
>      2	
>      3	After every merge to main, `dokima.uptodate.run(repo, base, sha, rest=...)` tries GitHub's Update branch on every open
>      4	PR behind main. Before #408, every refusal posted a new "could not be updated" comment, so PR #287 got 23 identical
>      5	ones in a day. These tests fake GitHub through the same `rest(method, path, **fields)` seam as tests/test_uptodate.py,
>      6	but keep each PR's comments as GitHub would, so several merges in a row can be run against one PR and the comments it
>      7	ends up carrying can be counted. One test runs the real module from outside against a fake `gh` on PATH.
>      8	
>      9	The fake GitHub answers:
>     10	  - GET .../pulls: the open PRs; GET .../compare/BASE...HEAD: behind by one commit;
>     11	  - PUT .../pulls/N/update-branch: 202, or 422 with GitHub's refusal for that PR (set per run in `refuse`);
>     12	  - GET .../issues/N/comments (paged with page=): the PR's comments as REST returns them, oldest first;
>     13	  - POST .../issues/N/comments, PATCH .../issues/comments/ID, DELETE .../issues/comments/ID.
>     14	"""
>     15	import json
>     16	import os
>     17	import re
>     18	import stat
>     19	import subprocess
>     20	import sys
>     21	
>     22	import pytest
>     23	
>     24	sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
>     25	
>     26	from dokima import agent  # noqa: E402
>     27	
>     28	ROOT = os.path.abspath(os.path

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_uptodate_once.py 2>&1 | grep -E "^(FAILED|E  .*408|[0-9]+ )" | head -30; python3 -m pytest -q tests/test_uptodate.py 2>&1 | tail -3
```

> E           AssertionError: 408.1: PR 81 got 3 comments posted over three refusals, expected one
> E       AssertionError: 408.2: a new comment was posted on a PR that already had refusal comments
> E       AssertionError: 408.3: after a clean update the comment still says it could not be updated: 'This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head'
> E       AssertionError: 408.4: expected one comment posted and carried, got 2 posted: ['This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head', 'This pull request could not be updated with `main` (c3d4e5f). GitHub said: refusing to allow a GitHub App to create or update workflow `.github/workflows/ci.yml` without `workflows` permission']
> E       AssertionError: 408.5: expected the bot to post and keep one comment of its own, got 2 posted: [{'id': 1002, 'user': {'login': 'dokima-runtime[bot]', 'type': 'Bot'}, 'body': 'This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head', 'created_at': '2026-10-10T10:42:00Z'}, {'id': 1003, 'user': {'login': 'dokima-runtime[bot]', 'type': 'Bot'}, 'body': 'This pull request could not be updated with `main` (b2c3d4e). GitHub said: merge conflict between base and head', 'created_at': '2026-10-10T10:43:00Z'}]
> E       AssertionError: 408.6: PR 92 was not updated after PR 91's comments could not be read
> FAILED tests/test_uptodate_once

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan of four criteria and two non-functional requirements for keeping one refusal comment per pull request, with six new tests in tests/test_uptodate_once.py.",
          "Taught the two fakes in tests/test_uptodate.py to answer a request for a pull request's comments with none."],
  "decided": ["A pull request that updates cleanly keeps its comment, edited to say it is up to date at the newest commit, rather than having it removed.",
              "Older refusal comments from before, as on #287, are deleted on the pull request's next update attempt, keeping only the newest, edited."],
  "open": []},
 "verdict": "block",
 "summary": "The plan keeps every ask, but the test for 408.6 never makes editing a comment fail and would pass on a run that never names the broken pull request in its error.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "408.6",
   "text": "408.6 promises that when GitHub cannot list or change a refused pull request's comments, the others still update and the run fails with an error naming it. The test only proves the listing half, and its naming check passes on the line the run already prints today. First, in its fake gh only the listing of comments ever fails, and since it lists no comments, no edit or delete is ever tried, so code that stops the whole run when an edit is refused still passes. Second, it checks only that '#91' appears anywhere in the output, but every run already prints '::warning::uptodate: #91 could not be updated' for a refused pull request, so a run that fails with an error not naming #91 still passes. Smallest fix: add a case where PR 91 already carries the bot's refusal comment and GitHub answers 502 to editing it (PATCH .../issues/comments/ID), with PR 92 placed after it and still updated and the run exiting non-zero; and in both cases check that an '::error::' line names #91, not just any output.",

```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** The checker wants a shorter summary, so I'm trimming it and running the check again.

`6. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan keeps every ask, but 408.6's test never makes editing a comment fail and passes even when the error omits the pull request."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 408 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#408](https://github.com/dokima-dev/dokima/issues/408) (one comment per pull request that can't be updated with main). The hand-back passes both checks. The only problem is one weak test, so it goes back to the planner.

**What holds up:**
- Every ask in the issue has a criterion. The criteria are 408.1 and 408.2 (one comment, edited in place, showing the newest main commit, with older duplicates like those on #287 removed) and 408.3 (a clean update edits that comment and posts none).
- I ran all six new tests and each one fails today because the feature is missing, not because of a crash or a bad path.
- The existing `tests/test_uptodate.py` still passes (8 tests) with the planner's changes to its fakes.
- The plan has no questions for you, so nothing needed answering on autopilot.

**The blocker, sent to the planner:** criterion 408.6 promises that when GitHub can't list or change a pull request's comments, the other pull requests still update and the run fails with an error naming the broken one. Its test only proves part of that:
- **Editing never fails in the test.** Only reading the comments fails, and since that returns nothing, no edit or delete is ever tried. Code that stops the whole run when an edit is refused would still pass.
- **The naming check passes on today's output.** It only looks for `#91` anywhere in the output. The run already prints `::warning::uptodate: #91 could not be updated`, so an error that never names the pull request would still pass.

The smallest fix is two changes to the test:
- Add a case where GitHub refuses the edit of the bot's existing comment, and check that the next pull request still updates and the run fails.
- Check that an `::error::` line names #91.

Your `/work` stopped earlier because no plan review had approved the plan yet. After the planner fixes this test and a new review approves the plan, autopilot should start the worker without you typing `/work` again.
