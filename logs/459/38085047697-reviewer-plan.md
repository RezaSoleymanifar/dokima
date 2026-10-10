# reviewer (plan) for #459

Run: https://github.com/dokima-dev/dokima/actions/runs/38085047697

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #459: The owner is co-author on every commit Dokima makes
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/459
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> I want to be a co-author on every commit Dokima makes, in every repo it runs on, so it shows on my GitHub profile and contribution graph.
> 
> Every commit Dokima makes (planner, worker, updates with main, anything else) ends with:
> 
> Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
> In another repo, the co-author is that repo's owner (the code owner who runs Dokima there), with their GitHub noreply address, read from GitHub, never hard-coded.
> 
> Done when
> - Every commit on a Dokima branch carries the line, and the squashed commit that lands on main keeps it.
> - A commit without it fails a check, so it can't slip through.
> - The owner's name and address come from GitHub for the repo Dokima runs on.
> 
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" al

`2. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def approvers" -A15 dokima/plan.py | head -30; grep -n "update-branch\|def dokima_issue" dokima/uptodate.py; grep -n "squash" dokima/agent.py dokima/manifest.py dokima/audit.py | head; grep -rn "git commit\|commit -" .github/workflows dokima/*.py | head -20; cat .github/CODEOWNERS; grep -n "split\|stories" dokima/agent.py | grep -n "def " | head
```

> 127:def approvers(codeowners, repo_owner):
> 128-    """The people whose approval counts: the owners of `*` in CODEOWNERS, else the repository owner."""
> 129-    for line in (codeowners or "").splitlines():
> 130-        parts = line.split("#")[0].split()
> 131-        if parts and parts[0] == "*" and len(parts) > 1:
> 132-            return {name.lstrip("@") for name in parts[1:]}
> 133-    return {repo_owner}
> 134-
> 135-
> 136-def repo_approvers(repo_owner, root="."):
> 137-    path = os.path.join(root, ".github", "CODEOWNERS")
> 138-    return approvers(open(path).read() if os.path.exists(path) else "", repo_owner)
> 139-
> 140-
> 141-def approved_at(events, approver_names):
> 142-    """When an approver last added the `work` label, if it is still on; else None. Nobody else's label counts."""
> 87:            rest("PUT", f"repos/{repo}/pulls/{n}/update-branch", expected_head_sha=head)
> 142:def dokima_issue(repo, pr):
> dokima/agent.py:1966:        gh("pr", "merge", str(pr), "-R", repo, "--squash", "--match-head-commit", head)
> .github/workflows/wiki.yml:27:            git commit -m "Sync from ${GITHUB_SHA::7}"
> .github/workflows/agent.yml:145:              git add -A && git -c user.name=dokima -c user.email=dokima@users.noreply.github.com commit -q --no-edit
> .github/workflows/agent.yml:337:            git commit -qm "$ROLE for #$N (run ${{ github.run_id }})"
> .github/workflows/agent.yml:361:          git -C "$W" -c user.name="${SLUG}[bot]" -c user.email="${BOT_ID}+${SLUG}[bot]@users.noreply.github.com" comm

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposed a split into 3 stories: Dokima's agent and other commits credit the owner, updates with main and the squash merge keep the line, and a required check fails a Dokima commit without it."],
  "decided": ["The owner is read from GitHub as each person owning `*` in CODEOWNERS, else the repository owner, with their profile name and ID+login noreply address; a team or organization is never credited.", "When GitHub cannot give a person to credit, nothing is committed and the run says why.", "The check judges only commits Dokima's bot made; a commit a person makes by hand never fails it."],
  "open": ["The planner asks whether #110 closes as a duplicate of #459, and whether several code owners each get a co-author line."]},
 "verdict": "approve",
 "summary": "The split gives every ask of the issue to exactly one story, each story has at most four criteria in one part of the code, and the stories depend on each other in order with no loop; the two questions about #110 and several code owners are yours to answer.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "I want to be a co-author on every commit Dokima makes, in every repo it runs on", "source": "https://github.com/dokima-dev/dokima/issues/459", "criterion": "S1.3"},
  {"ask": "Every commit Dokima makes (planner, worker, updates with main, anything else) ends with: Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>", "source": "https://github.com/dokima-dev/dokima/issues/459", "criterion": "S1.1"},
  {"ask": "updates with main", "source": "https://github.com/dokima-dev/dokima/issues/459", "criterion": "S2.1"},
  {"ask": "In another repo, the co-author is that repo's owner (the code owner who runs Dokima there), with their GitHub noreply address, read from GitHub, never hard-coded.", "source": "https://github.com/dokima-dev/dokima/issues/459", "criterion": "S1.2"
```

> Exit code 1
> summary holds 50 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The split gives every ask to exactly one story; the questions about #110 and several code owners wait for you."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 459 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the planner's split for [#459](https://github.com/dokima-dev/dokima/issues/459) (credit the owner as co-author on every commit Dokima makes). The review file is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What I checked:**
- **Every ask is covered.** Each thing the owner asked for in the issue maps to one criterion, and none is marked missing:
  - commits by the planner, the worker and anything else carry the line: S1.1 and S1.3
  - the name and address come from GitHub, never hard-coded: S1.2
  - updates with main keep the line: S2.1
  - the squashed commit on main keeps it, whether autopilot or the owner merges: S2.2 and S2.3
  - a commit without the line fails a check: S3.1 and S3.2
  - the check reads the owner from GitHub too: S3.3
- **The split follows the rules.** There are 3 stories with at most four criteria each. Each story is in its own part of the code, and story 3 depends on story 2, which depends on story 1, with no loop.
- **The planner's facts match the code.** Every place a commit is made shows up where the planner said:
  - `agent.yml`, including the main merge with no co-author line at line 145
  - `planner.yml`, `worker.yml` and `wiki.yml`
  - the GitHub `update-branch` call in `dokima/uptodate.py:87`
  - the squash merge in `dokima/agent.py:1966`, which passes no message
  - `approvers()` in `dokima/plan.py:127`

  CODEOWNERS gives `* @RezaSoleymanifar`.
- **No tests to run yet.** A split plan comes with none; each story's own planner writes them.

**Readings I accepted without a question:**
- **Hand-made commits don't fail the check.** The check only judges commits Dokima's bot made. This fits "every commit Dokima makes" and the "Humans are free" principle in AGENTS.md.
- **No credit means no commit.** When GitHub can't give a person to credit, nothing is committed and the run says why. This follows the "Fail closed" principle.

**Waiting for the owner:** I didn't answer the planner's two questions for the owner, because nothing the owner has written settles either one:
1. Should [#110](https://github.com/dokima-dev/dokima/issues/110) (the older co-author design) close as a duplicate of #459?
2. If CODEOWNERS names several people, should each of them get a co-author line?

Even on autopilot, these stop the river for the owner. With one code owner in this repo, as now, both readings of the second question give the same result.
