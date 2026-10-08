# reviewer (plan) for #164

Run: https://github.com/dokima-dev/dokima/actions/runs/37728476138

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  8 04:38 .
> drwxrwxrwt 18 root   root    4096 Oct  8 04:39 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 04:38 in
> -rw-r--r--  1 runner runner 12842 Oct  8 04:38 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 04:38 open_blockers.json
> -rw-r--r--  1 runner runner  9364 Oct  8 04:38 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner  4096 Oct  8 04:38 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 04:38 ..
> -rw-r--r-- 1 runner runner 10041 Oct  8 04:38 01-planner.json
> # Issue #164: Visibility: one live card per run, from queued to done
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> Every agent run gets one card on the issue or PR that updates in place, so I always see where the work is.
> 
> - Within seconds of my command it says queued.
> - When the machine starts it says working, with the start time.
> - While it works it shows the minutes and the step it is on, like reading the issue, writing tests or checking its output.
> - At the end the same card becomes the result, done, failed with why, or cancelled.
> - When a run waits behind another run on the same issue, the card says so.
> - The same card for every stage, every hand off in the river, and filing a split.
> - A run that fails before its 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn -i "reaction\|emoji" .github/workflows dokima | head -20; git log --oneline -8 -- .github/workflows; grep -n "R2\|def check_split\|split" dokima/agent.py | head -40
```

> 0c5a1ad Plan review fails silently on a split: it needs a try branch splits never create (#177)
> ad1f759 Plan checker: kinds, sources and named tests (#174)
> e28c83c Merge check reads the criteria from the approved plan, not the issue text (#171)
> 6672bda A re-plan is judged only on what the planner changed in its own run (#167)
> 860b40d The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue (#161)
> 77c5b21 The river: each stage starts the next until it needs the owner (#162)
> a6ac00c A re-plan checks its tests against where the branch left main (#159)
> 78fe9eb /work on an approved split files its stories as sub-issues (#153)
> 164:def file_split(repo, parent, recs):
> 165:    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links.
> 167:    Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
> 168:    done = latest(recs, "split", passed=True)
> 176:        number = int(url.rstrip("/").split("/")[-1])
> 188:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> 199:           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()] if not passed else []}}
> 202:        rec["dropped_by_fence"] = [l for l in open(dropped).read().splitlines() if l.strip()]
> 208:    lines = [l.strip() for l in why.splitlines() if l.strip()] or ["A step before the 

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Proposed splitting the live run card into four stories: working-to-result, queued/waiting/every hand-off, minutes and step, and cancelled runs with who gets pinged."],
  "decided": ["Every bullet of the issue goes to exactly one story; the done and failed half of the result bullet goes to story 1, the cancelled half to story 4.",
              "Stories 2, 3 and 4 wait for story 1, which brings the card itself.",
              "Treats the issue as asking for changes to the workflow files, since a card within seconds of a command can only come from them."],
  "open": []},
 "verdict": "approve",
 "summary": "The split gives each of the nine asks in the issue to exactly one of four stories, with nothing dropped or added; it is ready for the owner's /work.",
 "blockers": [],
 "notes": [
  {"text": "Story 1, criterion 3 says a run that fails before its agent starts 'updates that card', but in story 1 alone the card first appears when the machine is ready, so there is no card yet at that point; the queued card only arrives with story 2. The child's planner should say the run posts the card in that case.",
   "evidence": "plan.json stories[0].acceptance_criteria[0] and [2]; stories[1] (queued card) depends_on story 1"},
  {"text": "Story 4, criterion 2 (a rejected hand-back mentions the owner) already happens today through next_step, so the child's test must show it on the new card, or it will pass before any work.",
   "evidence": "plan.json stories[3].context: 'next_step() in dokima/agent.py stops on any hand-back code rejected and mentions the owner'"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 164 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the planner's proposed split of issue #164 into four stories, with no blockers. The review is in `/tmp/dokima-out/review.json` and passes both required checks.

**How the nine asks are shared out:**

| Story | What it covers | Issue bullets |
|---|---|---|
| 1 | One card per run that goes from working to its result | 2, the done and failed half of 4, 7, 9 |
| 2 | Queued, waiting behind another run, the same card at every hand-off and split | 1, 5, 6 |
| 3 | Minutes and the current step while the agent works | 3 |
| 4 | Cancelled runs, and who gets pinged | 8, the cancelled half of 4 |

- **Coverage:** each ask goes to exactly one story, and nothing is dropped or added.
- **Rules for a split:** four stories, one level deep. Stories 2–4 depend on story 1 and nothing loops back.
- **Changing the workflow files:** the planner flags that every story has to change the workflow files, which are normally off limits unless the issue asks. That's a fair reading: a card "within seconds of my command" can only come from them, and earlier issues (#162, #169, #177) changed them the same way.
- **Tests:** a split has none of its own; each story's planner writes them.

**Two notes for the story planners (not blockers):**
- **Story 1, criterion 3:** it says a run that fails before its agent starts "updates that card". In story 1 alone there is no card yet at that point; the queued card only arrives with story 2. That story's planner should say the run posts the card instead.
- **Story 4, criterion 2:** "a rejected hand-back mentions the owner" already happens today. Its test has to check the mention on the new card, or it will pass before any work is done.

Next, it's your call: `/work` files the four stories as sub-issues.
