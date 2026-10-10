# reviewer (plan) for #412

Run: https://github.com/dokima-dev/dokima/actions/runs/38073552865

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-not-started.json
> # Issue #412: Autopilot says it merged a PR that only queued or is waiting for my approval
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Autopilot says it merged a pull request only once GitHub reports it merged, and otherwise says it queued or waits for your approval.
> 
> **Work** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Fix why nothing ran
> 
> https://github.com/dokima-dev/dokima/issues/412
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Overlap with #378:** #378 (merge queue story 4 of #111) already promises `Autopilot: PR #N joined the merge queue` in place of the false merged line. This plan fixes that bug here, uses #378's exact wording, and leaves #378 the line when the queue lands it and the dequeue reason. Should the queued case stay here, or move wholly to #378 so this issue covers only the wait for your approval? The plan assumes it stays here. · for you
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #378, #379, #413
> 
> **User story:** The owner can trust autopilot's line

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/parent.json | head -50; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; git show --stat HEAD; wc -l tests/test_automerge_confirmed.py
```

> {"number": null}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38062105348",
>  "commit_before": "e02bcb264bf540a81ee342e4d6eb36435fcaa4fa",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 532899,
>   "turns": 37,
>   "cost_usd": 2.1426691999999994,
>   "tokens_in": 2904741,
>   "tokens_out": 34828
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/412/38062105348-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38062105348",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> commit 69e33dffd08dc2215efab50b18536da274eb91a7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 15:13:46 2026 +0000
> 
>     planner for #412 (run 38062105348)
> 
>  tests/test_automerge_confirmed.py | 291 ++++++++++++++++++++++++++++++++++++++
>  1 file changed, 291 insertions(+)
> 291 tests/test_automerge_confirmed.py

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_automerge_confirmed.py
```

> """Autopilot says it merged a pull request only once GitHub reports it merged (#412).
> 
> With a merge queue, or branch protection that waits on the owner's approval, `gh pr merge --squash` only puts the pull
> request in the queue, or turns on auto-merge, and exits 0 with nothing merged. Autopilot used to post
> `Autopilot: merged PR #N` on that exit code alone, so the issue said merged while its card said Needs you.
> 
> These tests run the code review (agent.yml) and `/autopilot start` (commands.yml) the way test_automerge.py does, on its
> fake GitHub, taught three more ways a merge can go. A pull request in prs.json may carry "accepts":
>   - "queue": `gh pr merge` with a method exits 0 saying the pull request was added to the merge queue; it stays open,
>     and GitHub then reports isInMergeQueue true, autoMergeRequest set and reviewDecision APPROVED (`gh pr view --json`),
>     and auto_merge set with merged false (`gh api repos/o/r/pulls/N`);
>   - "approval": `gh pr merge` exits 0 saying it will be merged when all requirements are met; it stays open, out of the
>     queue, with autoMergeRequest set and reviewDecision REVIEW_REQUIRED;
>   - "silent": `gh pr merge` exits 0 and nothing changes: open, out of the queue, no auto-merge, no review required.
> Asked through `gh api -X PUT repos/o/r/pulls/N/merge`, such a pull request is refused as GitHub refuses it (405). With
> "unreadable" set too, once a merge was asked GitHub fails every read of that pull request (`gh pr view`,
> `gh api repos/o/r/pu

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_automerge_confirmed.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | head -60
```

> E       AssertionError: 412.1 (review-queue): GitHub never reported #60 merged, yet a comment says it merged: ['Autopilot: merged PR #60', 'g" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-pr.md) · [run](https://github.com/o/r/actions/runs/42)</sub>\n\n**Next:** Autopilot merged PR #60; what it unblocks starts when the issue closes.\n']
> E       assert not ['Autopilot: merged PR #60', '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icon...com/o/r/actions/runs/42)</sub>\n\n**Next:** Autopilot merged PR #60; what it unblocks starts when the issue closes.\n']
> E           AssertionError: 412.2 (review-queue): #57 did not get exactly one Autopilot line reading 'Autopilot: PR #60 joined the merge queue': ['Autopilot: merged PR #60']
> E             ## run: Decide what follows, merge on autopilot, and say it on the card (exit 0)
> E             stop
> E             
> E             ## run: Post the record as a comment, on the PR once there is one (exit 0)
> E             \n\n- **Did:** Built the fix.\n\n</details>\n\n<details><summary>Full record</summary>\n\n```json\n{\n \"role\": \"reviewer\",\n \"stage\": \"pr\",\n \"run_id\": \"42\",\n \"commit_before\": \"3cd41e1980a24da90e043c06d28823bd0efdb713\",\n \"started_by\": \"owner-person\",\n \"models\": [\n  \"claude-opus-5-5\"\n ],\n \"report\": {\n  \"duration_ms\": 1000,\n  \"turns\": 1,\n  \"cost_us

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "card.py" .github/workflows dokima/*.py | head; grep -n "merged PR\|def automerge\|def try_merge" dokima/*.py | head -20
```

> .github/workflows/card.yml:9:# always use the default branch's copy of this file and of dokima/card.py, so
> .github/workflows/card.yml:98:        run: python3 dokima/card.py
> dokima/agent.py:1605:def try_merge(repo, pr):
> dokima/agent.py:1635:def automerge(repo, number):
> dokima/agent.py:1646:        gh("issue", "comment", str(number), "-R", repo, "--body", f"Autopilot: merged PR #{pr}")
> dokima/agent.py:2073:                step = ("merged", f"Autopilot merged PR #{pr}; what it unblocks starts when the issue closes.") if merged else \

**Agent:** Tests all fail today for the right reason (autopilot posts "merged" though nothing merged). Checking the merge code paths before writing the verdict.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1600,1660p dokima/agent.py; grep -n "automerge(\|try_merge(" dokima/*.py
```

> if running:
>         return f"a check is still running on its head commit {sha[:7]}: {', '.join(running)}"
>     return None
> 
> 
> def try_merge(repo, pr):
>     """Merge the pull request at the head whose checks were read, only when it changes no workflow file and every
>     check on that head has passed. Returns (True, the merged head) or (False, why not, in GitHub's words when GitHub
>     refused)."""
>     try:
>         files = [f["filename"] for p in pages(gh("api", f"repos/{repo}/pulls/{pr}/files?per_page=100", "--paginate")) for f in p]
>         flows = [f for f in files if f.startswith(WORKFLOWS)]
>         if flows:
>             return False, f"it changes a workflow file ({', '.join(flows)}), and only the owner merges those"
>         head = gh("pr", "view", str(pr), "-R", repo, "--json", "headRefOid", "-q", ".headRefOid").strip()
>         if not head:
>             return False, "GitHub did not say which commit is its head"
>         why = unproven(repo, head)
>         if why:
>             return False, why
>         # Pinned to the head whose checks passed: a commit pushed since makes GitHub refuse.
>         gh("pr", "merge", str(pr), "-R", repo, "--squash", "--match-head-commit", head)
>         return True, head
>     except subprocess.CalledProcessError as e:
>         return False, " ".join((e.stderr or str(e)).split())
>     except (json.JSONDecodeError, AttributeError, KeyError, TypeError) as e:
>         return False, f"GitHub's answer could not be read: {e}"
> 
> 
> def open_pr(repo, number):
>     """Th

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three criteria and one non-functional requirement for autopilot's merge line, each with its own test in tests/test_automerge_confirmed.py."],
  "decided": ["The queued case uses #378's wording, `Autopilot: PR #N joined the merge queue`; a merge waiting on the owner says `Autopilot: PR #N waits for your approval before it merges`.",
              "A merge GitHub cannot confirm posts no Autopilot line and says why on the pull request, mentioning the owner."],
  "open": ["Whether the queued case stays here or moves wholly to #378; the plan keeps it here."]},
 "verdict": "approve",
 "summary": "The plan covers every ask in the issue, each criterion has a test that runs the real code review and /autopilot start, and all four tests fail today because autopilot posts `Autopilot: merged PR #60` though nothing merged.",
 "raises": [],
 "answers": [
  {"raise": "P1", "answer": "done",
   "why": "The owner's own Done-when line asks this issue to cover the queued case as well as the wait for approval, so the queued case stays here as the plan assumes; #378 keeps the line when the queue lands the PR and the dequeue reason. Either way autopilot behaves the same; only which issue delivers it differs.",
   "words": "When the merge only queued or waits on owner approval, the issue says that instead, in one line, and the card and that line agree.",
   "source": "https://github.com/dokima-dev/dokima/issues/412",
   "changes": false}
 ],
 "asks": [
  {"ask": "The \"merged\" line is posted only after GitHub reports the PR merged.", "source": "https://github.com/dokima-dev/dokima/issues/412", "criterion": "412.1"},
  {"ask": "When the merge only queued ... the issue says that instead, in one line, and the card and that line agree.", "source": "https://github.com/dokima-dev/dokima/issues/412", "criterion": "412.2"},
  {"ask": "When the merge ... waits on owner approval, the
```

> Exit code 1
> summary holds 38 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every ask has a criterion and a test that runs the real merge, and all four fail today because autopilot claims a merge that never happened."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 412 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> 0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every ask has a criterion and a test that runs the real merge; all four fail today because autopilot claims merges that never happened."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 412 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for [#412](https://github.com/dokima-dev/dokima/issues/412) (autopilot says it merged a PR that only queued or is waiting for your approval). The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass with nothing reported.

- **Every ask is covered.** The owner asked for three things, and each has its own criterion:
  - the "merged" line is posted only once GitHub reports the PR merged (412.1);
  - a merge that only joined the queue says so in one line, and the card agrees (412.2);
  - a merge waiting on the owner's approval says so in one line, and the card agrees (412.3).
- **The tests would catch a wrong fix.** They run the real code review and `/autopilot start` against a fake GitHub that can queue a merge, wait on approval, do nothing, or fail to answer afterwards. Each test pairs the bad case with a good one: a real merge must still post the line exactly once, and the card must still say "Ready for approval" when there is no queue line. That stops a fix that just blocks everything from passing.
- **All four tests fail today for the right reason.** In every case autopilot posts `Autopilot: merged PR #60` even though nothing merged. None of them fail from a crash or a setup problem.
- **I answered the planner's question for the owner, P1** (does the queued case stay here or move to [#378](https://github.com/dokima-dev/dokima/issues/378), the merge queue story that already promises the queued line?). It stays here. Autopilot is on for this issue, and the owner's own words in the issue settle it: "When the merge only queued or waits on owner approval, the issue says that instead, in one line, and the card and that line agree." I marked it as not changing how the system works or what it costs; only which issue delivers the change differs.

I raised no blockers and no new issues. The work also changes `dokima/card.py`, which normally stays untouched unless the issue asks. I accepted it because the owner asks for the card to agree with the line. Two small points I didn't block on: the "GitHub can't confirm the merge" case is only tested through the code review, not through `/autopilot start`, and the `AGENTS.md` update has no test.
