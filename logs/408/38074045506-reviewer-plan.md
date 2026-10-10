# reviewer (plan) for #408

Run: https://github.com/dokima-dev/dokima/actions/runs/38074045506

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; cat open_blockers.json; cat plan.json
```

> total 32
> drwxr-xr-x 2 runner runner 4096 Oct 10 18:00 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 18:00 ..
> -rw-r--r-- 1 runner runner 4743 Oct 10 18:00 01-planner.json
> -rw-r--r-- 1 runner runner  370 Oct 10 18:00 02-not-started.json
> -rw-r--r-- 1 runner runner 3891 Oct 10 18:00 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5334 Oct 10 18:00 04-planner.json
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
> **User story:** When GitHub refuses to bring a pull request up to date with main, the owner sees one comment on it that always shows the newest main commit and GitHub's reason, and that same comment says so once the pull request updates cleanly again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD HEAD~1 | head -30; cat tests/test_uptodate_once.py; python -m pytest -q tests/test_uptodate_once.py tests/test_uptodate.py 2>&1 | tail -30
```

> commit 9053f059a42fc5e76f51a47aa5094bc9bcac1f4a
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:00:23 2026 +0000
> 
>     planner for #408 (run 38073687432)
> 
>  tests/test_uptodate_once.py | 69 ++++++++++++++++++++++++++++++++++-----------
>  1 file changed, 53 insertions(+), 16 deletions(-)
> 
> commit 68928554e80c312d65b3012cb00b79f498ed87ad
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 15:08:07 2026 +0000
> 
>     planner for #408 (run 38062103512)
> 
>  tests/test_uptodate.py      |   5 +
>  tests/test_uptodate_once.py | 351 ++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 356 insertions(+)
> """A PR that cannot be updated with main carries one comment, edited in place (#408).
> 
> After every merge to main, `dokima.uptodate.run(repo, base, sha, rest=...)` tries GitHub's Update branch on every open
> PR behind main. Before #408, every refusal posted a new "could not be updated" comment, so PR #287 got 23 identical
> ones in a day. These tests fake GitHub through the same `rest(method, path, **fields)` seam as tests/test_uptodate.py,
> but keep each PR's comments as GitHub would, so several merges in a row can be run against one PR and the comments it
> ends up carrying can be counted. One test runs the real module from outside against a fake `gh` on PATH.
> 
> The fake GitHub answers:
>   - GET .../pulls: the open PRs; GET .../compare/BASE...HEAD: behind by one commit;
>   - PUT .../pul

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_uptodate_once.py tests/test_uptodate.py 2>&1 | grep -E "^(FAILED|E  )" | cut -c1-300; sed -n 1,175p dokima/uptodate.py
```

> E           AssertionError: 408.1: PR 81 got 3 comments posted over three refusals, expected one
> E           assert 3 == 1
> E            +  where 3 = posts(81)
> E            +    where posts = <test_uptodate_once.GitHub object at 0x7fe55235aea0>.posts
> E       AssertionError: 408.2: a new comment was posted on a PR that already had refusal comments
> E       assert 1 == 0
> E        +  where 1 = posts(83)
> E        +    where posts = <test_uptodate_once.GitHub object at 0x7fe5521a9e80>.posts
> E       AssertionError: 408.3: after a clean update the comment still says it could not be updated: 'This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head'
> E       assert 'could not be updated' not in 'This pull r...ase and head'
> E         
> E         'could not be updated' is contained here:
> E           This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head
> E         ?                   ++++++++++++++++++++
> E       AssertionError: 408.4: expected one comment posted and carried, got 2 posted: ['This pull request could not be updated with `main` (a1b2c3d). GitHub said: merge conflict between base and head', 'This pull request could not be updated with `main` (c3d4e5f). GitHub said: refusing to allow a Gi
> E       assert (2 == 1)
> E        +  where 2 = posts(86)
> E        +    where posts = <test_uptodate_once.GitHub object at 0x7fe5521aafc0>.posts
> E       AssertionError: 408.5: expected t

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main -- tests/test_uptodate.py; git diff --stat main
```

> diff --git a/tests/test_uptodate.py b/tests/test_uptodate.py
> index c2d2378..4d18a3a 100644
> --- a/tests/test_uptodate.py
> +++ b/tests/test_uptodate.py
> @@ -11,6 +11,7 @@ The fake GitHub answers:
>    - GET .../pulls (any query or fields; an empty page past the first): the open PRs, drafts included;
>    - GET .../compare/BASE...HEAD, where HEAD is a PR's head sha, its ref or its "owner:ref" label: behind_by, ahead_by;
>    - PUT .../pulls/N/update-branch (expected_head_sha): 202, or GitHub's refusal for that PR, 422 with its message;
> +  - GET .../issues/N/comments: no comments yet (#408 looks for its earlier refusal comment);
>    - POST .../issues/N/comments (body): a comment on PR N.
>  """
>  import json
> @@ -79,6 +80,8 @@ class FakeGitHub:
>                  self.fail(self.refuse[n])
>              return {"message": "Updating pull request branch.", "url": f"https://github.com/{REPO}/pull/{n}"}
>          m = re.fullmatch(rf"repos/{REPO}/issues/(\d+)/comments", bare)
> +        if method == "GET" and m:
> +            return []
>          if method == "POST" and m:
>              return {"id": len(self.calls), "body": fields.get("body", "")}
>          raise AssertionError(f"189: unexpected GitHub call {method} {path} {fields}")
> @@ -175,6 +178,8 @@ if method == "GET" and m:
>              print(json.dumps({{"behind_by": p["_behind"], "ahead_by": p["_ahead"]}})); sys.exit(0)
>  if method == "PUT" and re.fullmatch("repos/" + d["repo"] + r"/pulls/\\d+/update-branch", bare):
>      print(json.dumps({{"message": "

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added a second test for 408.6: PR 91 already carries the bot's refusal comment, GitHub refuses to edit or delete it, PR 92 after it must still update and the run must fail.",
          "Made both 408.6 tests require an '::error::' line naming #91, so the '::warning::' line every refused pull request gets today no longer passes."],
  "decided": ["Kept the four criteria and two non-functional requirements of the first plan unchanged."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask, and each of its seven tests fails today because the pull request still gets a new comment per refusal, not because of a broken test.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Keep one such comment per PR and update it in place with the latest main commit and GitHub's reason.", "source": "https://github.com/dokima-dev/dokima/issues/408", "criterion": "408.1"},
  {"ask": "When the PR updates cleanly again, edit that comment to say so (or remove it), never add a new one.", "source": "https://github.com/dokima-dev/dokima/issues/408", "criterion": "408.3"},
  {"ask": "A PR refused on several merges in a row carries exactly one refusal comment, showing the newest main commit.", "source": "https://github.com/dokima-dev/dokima/issues/408", "criterion": "408.1"},
  {"ask": "A PR that updates cleanly after being refused gets no new comment.", "source": "https://github.com/dokima-dev/dokima/issues/408", "criterion": "408.3"},
  {"ask": "PR #287 got 23 identical comments in a day.", "source": "https://github.com/dokima-dev/dokima/issues/408", "criterion": "408.2"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 408 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

**Agent:** Shortening the review's summary line, then re-running the check.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan keeps every ask, and all seven tests fail today because each refusal still posts a new comment."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 408 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> exit 0

**Agent:** I approved the revised plan for #408 (one refusal comment per pull request), and it's now waiting for you. Both of Dokima's checks accept the review file.

**My earlier blocker on 408.6 is fixed.** That criterion says a run fails with an error naming the pull request when GitHub won't list or change its comments.
- There is now a second test where GitHub refuses to edit the bot's existing refusal comment on PR 91. PR 92 must still be updated, and the run must fail.
- Both tests for 408.6 now need an `::error::` line naming #91. The `::warning::` line every refused pull request already gets no longer counts.
- With PR 91's comments readable, the run must still pass with no error.

**Every ask in the issue maps to a criterion.** "Keep one comment and update it in place" is 408.1, "edit it when it updates cleanly, never add a new one" is 408.3, and the #287 case of 23 comments is 408.2. Where you wrote "edit that comment to say so (or remove it)", the plan chose to edit, which your words allow.

**Test runs on this branch:**
- All 7 new tests fail today for the right reason: each refusal still posts a new comment. In the 408.6 tests the run stops at that post, so PR 92 is never updated.
- The 8 existing tests in `tests/test_uptodate.py` still pass. The planner's only changes there teach the two fake GitHubs to answer a request for comments with an empty list.

I raised nothing. The review is in `/tmp/dokima-out/review.json`.
