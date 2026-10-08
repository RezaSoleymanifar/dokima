# reviewer (plan) for #229

Run: https://github.com/dokima-dev/dokima/actions/runs/37823075252

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #229: Every card reads like plain English, and the checker catches long text before the reviewer does
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
> Cards are too verbose. Worker and reviewer summaries read like changelogs full of file names and flags, and acceptance criteria run 80+ words (see #212). I want every card to read like what I asked for, in plain English, and still say the same thing.
> 
> What I want:
> - Every agent's role file says how I like to read cards: short, plain words, reads like my ask, no file, function or flag names in card text. Technical detail goes in docstrings. Planner, worker and reviewer each get it in their own role file, not a shared rule.
> - Every card opens with one plain sentence. The worker's summary today is "two sentences, cause and change" with no voice rule; fix that. The reviewer's summary says what was approved in my terms

`2. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "check" .github/workflows/agent.yml | head -40; grep -n "def opening" -A40 dokima/agent.py | head -70
```

> 5:# conversation (comments, reviews, line notes) and every earlier agent record. The agent runs its own check before it
> 62:      - uses: actions/checkout@v5
> 70:        # AGENTS.md comes too: the river checks the owner's words a plan reviewer quotes from it.
> 82:      # The run's card moves through its stages (queued, setting up, agent working, checking, then its record), each
> 84:      # live on this machine while the branch's code, its tests, the agent or the hand-back check run. Every stage
> 136:            git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
> 142:            git checkout -q -B "try/issue-$N" origin/main
> 179:      - name: Code checks the pack has everything this role needs
> 181:          python3 -m dokima.agent check-pack "$ROLE" "$STAGE" "$PACK" > /tmp/pack-check.txt \
> 182:            || { echo "Incomplete pack: $(paste -sd'; ' /tmp/pack-check.txt)" > /tmp/why.txt
> 212:            planner)      GRADE=plan-grade;   FILE=plan.json;   CHECK="python3 -m dokima.planner check $N $OUT" ;;
> 213:            reviewerplan) GRADE=plan-grade;   FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json $PACK/plan.json $N" ;;
> 214:            reviewerpr)   GRADE=result-grade; FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json $PACK/plan.json $N" ;;
> 215:            worker)       GRADE=result-grade; FILE=work.json;   CHECK="python3 -m dokima.agent check work $OUT/work.json $PACK/plan.json $N" ;;
> 217:   

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner split the issue into four stories: the planner's length caps, the worker's and reviewer's summaries and docstrings, dropping concerns and replies, and the role files with the reviewer blocking on verbose text."],
  "decided": ["A text a little over its cap is listed but passes; only a text far over is rejected.", "The worker keeps its replies to blockers; only the planner's go."],
  "open": ["The owner has not set the caps or how far over is too far; the plan assumes 20 words, 12 words and 5 over.", "Where a planner's doubt about the ask goes once concerns are gone."]},
 "verdict": "approve",
 "summary": "The split keeps every ask in the issue, but the caps it assumes are the owner's to set.",
 "blockers": [],
 "notes": [
  {"text": "Story 2's last criterion reads as if the check passes only when a text is over its cap; it should say it passes when each text is at most a little over, and that far over is rejected naming the text, as story 1 says for the planner.", "evidence": "plan.json stories[1].acceptance_criteria[3] versus stories[0].acceptance_criteria[3] and [4]"},
  {"text": "Several story criteria join two behaviors with 'and', which the owner asks the plan not to do; each story's own plan should give each its own criterion.", "evidence": "plan.json S1.2, S1.4, S2.4, S3.2, S4.2"},
  {"text": "Story 1 caps only the docstrings of the planner's new tests; the planner may also write helpers whose docstrings the owner's rule covers.", "evidence": "plan.json S1.2; dokima/roles/planner.md asks for a docstring on every file, class, function and test"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Every agent's role file says how I like to read cards: short, plain words, reads like my ask, no file, function or flag names in card text.", "source": "https://github.com/dokima-dev/dokima/issues/229", "criterion": "S4.1"},
  {"ask": "Technical d
```

> rc=0

**Agent:** I approved the planner's split of #229 with no blockers, but on autopilot it will still stop for you, because I didn't accept two of its four assumptions. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks passed.

**The split:** four stories:
1. Length caps for the planner, where a text a little over its cap is listed but still passes.
2. One-sentence summaries for the worker and reviewer, plus length checks on the worker's docstrings.
3. The planner hands back no concerns or replies, keeps its questions, and has at most five criteria per story.
4. Each role file says how you like to read cards, and the reviewer blocks on wordy text.

**Your asks:** I listed all 15 asks from the issue, and each one maps to a story criterion. None are missing. Each agent already runs the checker inside its own run, so that part of your ask is already true.

**The planner's assumptions:**

| Question | Accepted? | Why |
|---|---|---|
| What caps, and how far over is too far? (it assumed 20 words, 12 words, rejected at more than 5 over) | No, waits for you | The numbers decide which hand-backs get rejected, and you named no number. |
| Name each test's criterion by number? | Yes | AGENTS.md already says tests map to criteria by number. |
| A planner's doubt about your ask becomes a question? | No, waits for you | Today questions are only for asks with two readings. This would widen that rule, and you didn't say where doubts should go. |
| The worker keeps its replies to blockers? | Yes | Your ask drops replies only from the planner's hand-back. |

**Three notes, none blocking:**
- Story 2's last criterion reads as if the check passes only when a text is over its cap. It should match story 1: passes when at most a little over, and a text far over is rejected with the text named.
- Several story criteria join two behaviors with "and", which you asked plans not to do. Each story's own plan should split them.
- Story 1 caps only the docstrings of the planner's new tests, not other docstrings the planner might write.
