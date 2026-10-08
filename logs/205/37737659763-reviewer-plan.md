# reviewer (plan) for #205

Run: https://github.com/dokima-dev/dokima/actions/runs/37737659763

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (54.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5f3fb30f-5650-4592-a1e2-6cf264cfef3e/tool-results/bd29drz4w.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-planner.json
> # Issue #205: Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: the owner can hand a whole issue tree to Dokima and get it back done, stopped only where the owner must decide**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: `/autopilot start` on a parent issue puts its whole tree on autopilot, and `/autopilot stop` ends it; both work on issues and PRs
> *Verified by: tests that each command sets and clears autopilot for the parent and its children*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: an issue on autopilot shows an Autopilot pill on the board while it runs
> *Verified by: a test that start sets the pill and stop clears it*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: on autopilot the river goes on by i

`2. Bash`
```
cd /tmp/pack; sed -n '/<!-- dokima-card/,$p' issue.md | grep -v 'icons/' | head -300
```

> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: the owner can hand a whole issue tree to Dokima and get it back done, stopped only where the owner must decide**
> 
> <dl><dd>
> 
> *Verified by: tests that each command sets and clears autopilot for the parent and its children*
> 
> *Verified by: a test that start sets the pill and stop clears it*
> 
> *Verified by: tests for each of the three hand-offs on an autopilot issue, and that none happens without autopilot*
> 
> *Verified by: a test for each stop on an autopilot issue*
> 
> *Verified by: a test that the last child merging closes the parent and clears autopilot*
> 
> </dd></dl>
> 
> 
> <!-- /dokima-card -->
> 
> Requested by Reza in chat, 2026-10-08.
> 
> <details><summary><b>Context</b></summary>
> 
> On 2026-10-07 Claude cleared issues for Reza from chat on a 3 minute timer: /work on approved plans, merges of approved PRs, /plan on children whose blockers merged. Almost all of that is mechanical, so it belongs in the river, triggered by events, not in a chat session that runs 24/7. Questions stay with the owner. The "start children when blockers merge" part overlaps #86. First practical slice of the idea in #199.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #205 (2026-10-08T06:17:49Z)
> 
> /plan
> 
> ### dokima-runtime on issue #205 (2026-10-08T06:18:10Z)
> 
> <!-- dokima-record -->
> 
> Proposes a split: The owner hands a whole issue tree to Dokima with `/autopilot start` and gets it back done, stopped only where the owner must decide. Split by R2 a

`3. Bash`
```
cd /tmp/pack; awk '/2026-10-08T06:24:52Z/{f=1} f' issue.md | sed -n '/<\/details>/,$p' | head -100; echo ----; cat open_blockers.json; ls in; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))" | head -400
```

> </details>
> 
> <sub>Opus 5.5 · 1.4 min · 5 turns · 176,260 tokens in, 9,516 out · $0.37 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/205/37737442907-planner.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37737442907)</sub>
> 
> **Next:** The reviewer starts now.
> 
> 
> ### RezaSoleymanifar on issue #205 (2026-10-08T06:25:19Z)
> 
> Correction to my last comment. No separate Autopilot needs you pill, use the Needs you pill we have. Autopilot and Needs you never show on the same card, when autopilot stops for me the card shows Needs you instead. The autopilot view is a table list like the Needs you view. Drop the On autopilot from #N line on the issue.
> 
> ### dokima-runtime on issue #205 (2026-10-08T06:26:57Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> **Reviewer (plan)** · getting ready
> 
> The machine is getting ready. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37737659763)</sub>
> 
> ----
> []01-planner.json
> 02-planner.json
> {
>  "kind": "feature",
>  "feature": "The owner hands a whole issue tree to Dokima with `/autopilot start` and gets it back done, stopped only where the owner must decide, and sees on the board and on every card what is on autopilot. Split by R2 and R3: the ask holds far more than five criteria (two commands, the pi

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn -i "needs you" dokima/board.py | head; grep -rn -i "view" dokima/board.py AGENTS.md | head
```

> dokima/board.py:1:"""Keep the project board's Status, Action ("Needs you") and Priority current, from GitHub events.
> dokima/board.py:106:        board.set(iid, "Action", "Needs you" if needs_you else None)
> AGENTS.md:14:Dokima is Jira for agent teams. You are the project manager: you define the work, define what "done" means, and set priorities. Your team is remote engineers: agents that each take one narrow task, do it on their own machine, and hand back work you can check. They plan, build and review in the open on GitHub, the way people already work. You approve the plan before work starts and the result before it merges.
> AGENTS.md:16:GitHub is the office: issues are the tasks, pull requests are the work, comments and reviews are the conversation, checks are the proof, and the project board is the overview. Nothing new to learn.
> AGENTS.md:24:- The reviewer owns nothing; it judges and proposes.
> AGENTS.md:31:- **Use what GitHub already has.** Comments, reviews, checks, branch protection, CODEOWNERS, project boards, merge queue. Build only the thin glue GitHub lacks.
> AGENTS.md:33:- **Everything lives on GitHub.** One permanent history per issue, across every agent and device: plans, attempts, failures, reviews.
> AGENTS.md:34:- **Fail closed.** Missing proof, a missing reviewer or a broken check blocks; nothing is waved through, and a failure always says why on the issue.
> AGENTS.md:43:- **Reviewer:** checks the plan, then the result (a real PR review). It blocks only on a promis

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned after the owner confirmed the three assumptions and asked for an Autopilot pill on every card, an Autopilot needs you pill, a board view and an On autopilot from #N line.",
          "It proposes a split into five stories: switch on and off, show it on the board and card, an approved plan starts the worker, an approved pull request merges, and children start and the tree ends by itself."],
  "decided": ["Autopilot is kept as an `autopilot` label on every issue in the tree; the board pill follows that label."],
  "open": ["The plan was written before the owner's correction at 06:25 and still holds the Autopilot needs you pill and the On autopilot from #N line the owner dropped."]},
 "verdict": "block",
 "summary": "The split misses the owner's correction of 06:25: it still promises an Autopilot needs you pill and an On autopilot from #N line the owner dropped, never says Autopilot and Needs you never show together, and does not make the autopilot view a table list like the Needs you view.",
 "blockers": [
  {"id": "B1", "criterion": "2.2", "test": null,
   "problem": "Story 2 promises a separate 'Autopilot needs you' pill. The owner dropped it: the existing Needs you pill is used, and Autopilot and Needs you never show on the same card. No criterion says the Autopilot pill is hidden while Needs you shows.",
   "evidence": "Owner comment 2026-10-08T06:25:19Z: 'No separate Autopilot needs you pill, use the Needs you pill we have. Autopilot and Needs you never show on the same card, when autopilot stops for me the card shows Needs you instead.' plan.json story 2, criterion 2 and user_story; feature text lists 'the Autopilot needs you pill'.",
   "fix": "Replace story 2 criterion 2 with: when the river stops for the owner on an issue on autopilot, the card shows Needs you and no Autopilot pill, and shows Autopilot again (and no Needs you) once the riv
```

> Exit code 1
> blocker B1 names 2.2, which is not a criterion of the plan (S1.1, S1.2, S1.3, S1.4, S2.1, S2.2, S2.3, S2.4, S2.5, S3.1, S3.2, S3.3, S3.4, S3.5, S4.1, S4.2, S4.3, S4.4, S4.5, S5.1, S5.2, S5.3, S5.4, S5.5)
> blocker B2 names 2.4, which is not a criterion of the plan (S1.1, S1.2, S1.3, S1.4, S2.1, S2.2, S2.3, S2.4, S2.5, S3.1, S3.2, S3.3, S3.4, S3.5, S4.1, S4.2, S4.3, S4.4, S4.5, S5.1, S5.2, S5.3, S5.4, S5.5)
> blocker B3 names 2.3, which is not a criterion of the plan (S1.1, S1.2, S1.3, S1.4, S2.1, S2.2, S2.3, S2.4, S2.5, S3.1, S3.2, S3.3, S3.4, S3.5, S4.1, S4.2, S4.3, S4.4, S4.5, S5.1, S5.2, S5.3, S5.4, S5.5)

**Agent:** I'm writing up the plan review with three blockers, and I'm fixing the criterion IDs so the checker accepts them.

`6. Bash`
```
sed -i 's/"criterion": "2\.\([234]\)"/"criterion": "S2.\1"/' /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 205 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #205. The planner wrote it at 06:24, and Reza posted a correction at 06:25 that it never picked up. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks. All three blockers sit in story 2, the one that shows autopilot on the board and the card:

- **S2.2:** The plan still promises a separate "Autopilot needs you" pill. Reza dropped it and asked for the Needs you pill we already have, with Autopilot and Needs you never showing on the same card. No criterion says that yet.
- **S2.4:** The plan still promises an "On autopilot from #N" line on the issue card, which Reza also dropped. Removing it also removes the start-point record in story 1 and puts `dokima/card.py` back out of scope.
- **S2.3:** The board view criterion only asks for "a view that lists" everything on autopilot. Reza said it should be a table list like the Needs you view, so a view of any other shape would still pass as written.

Each blocker goes back to the planner with Reza's 06:25 comment as evidence and a suggested rewrite. I added one note, not a blocker: story 5 combines two goals (children starting once their blockers merge, and the tree switching itself off), and the plan could say why it keeps them together.

Apart from these, the plan already follows Reza's 06:24 answers (it confirms all three of the planner's first-round assumptions). It's a split, so there are no new tests to run at this stage.
