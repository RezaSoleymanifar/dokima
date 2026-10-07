# Dokima

*The one place for how Dokima works, for people and for every agent (Claude, Codex and others read this file; their own files just point here). Decisions land here once they're made; the issues hold how we got there. Items marked (planned) are decided but not built yet.*

## Working in this repo

- Python 3.12. Run the tests with `pytest -q`; tests live in `tests/`.
- Never change `.github/workflows/`, `dokima/card.py` or `dokima/roles/` unless the issue explicitly asks.
- Keep changes small. Add no dependencies unless the issue asks.
- Read this whole file before changing how Dokima works.

## The picture

Dokima is Jira for agent teams. You are the project manager: you define the work, define what "done" means, and set priorities. Your team is remote engineers: agents that each take one narrow task, do it on their own machine, and hand back work you can check. They plan, build and review in the open on GitHub, the way people already work. You approve the plan before work starts and the result before it merges.

GitHub is the office: issues are the tasks, pull requests are the work, comments and reviews are the conversation, checks are the proof, and the project board is the overview. Nothing new to learn.

## The core rule

**A stage never edits what another stage owns. It proposes, and the owner routes it with a command.**

- The plan (criteria and their tests) belongs to the planner, approved by the owner.
- The code belongs to the worker.
- The reviewer owns nothing; it judges and proposes.
- A command depends only on the stage it starts, never on the stage it comes from: every run rebuilds its starting pack from the issue's full history, so any stage can be re-entered at any time.

## Principles

- **Nothing merges until it's proven.** Every promise in a plan has its own check, and GitHub's verdict on that check is the proof. No model's say-so counts.
- **Code owns the structure; models fill in content.** Everything that must be exact (freezing plans, posting stage comments, building starting packs, drawing cards, setting labels and board fields) is done by code. Models write only the plan, the code and their findings.
- **Use what GitHub already has.** Comments, reviews, checks, branch protection, CODEOWNERS, project boards, merge queue. Build only the thin glue GitHub lacks.
- **Humans are free; bots are compliant.** People can do anything, on the record. Agents work inside fixed rules: they can't approve, can't change the workflows that judge them, and can't widen their own scope.
- **Everything lives on GitHub.** One permanent history per issue, across every agent and device: plans, attempts, failures, reviews.
- **Fail closed.** Missing proof, a missing reviewer or a broken check blocks; nothing is waved through, and a failure always says why on the issue.
- **Agent-neutral and language-neutral.** No hard-coded people, vendors or languages. Approvers come from CODEOWNERS; each agent plugs in through a small adapter; instructions (including how many sub-agents to use) live in prompts, not code.
- **Small and lean.** One issue, one PR. Fold related things together. Extras (the board, merge queue) are optional and never required.

## Roles

- **Owner:** decides. Approves plans and results, routes proposals. Only a code owner's commands count.
- **Planner:** turns a rough issue into a plan: an objective, acceptance criteria, scope, and a test for every criterion written before any code. It judges the ask first and raises a concern only with evidence. It may change or delete an older test when the plan makes it wrong, with a reason the owner sees. It proposes splits; it never writes code.
- **Worker:** builds what the approved plan says, on a fresh machine, within scope, until its tests pass. It never changes the plan's tests.
- **Reviewer:** checks the plan, then the result (a real PR review). It blocks only on a promise with no proof or a proof that proves nothing, and ends with a list of proposed issues.
- **Code:** everything that must be exact (see the principles).

## The flow (the river)

1. **Issue.** The owner writes what they want, in plain words, rough or detailed.
2. **`/plan`.** The planner always plans, on its best reading, and lists any questions with the reading it planned for. Too big: it proposes a split. If the plan has questions, the river stops and mentions the owner, who answers with `/plan` and their words, or says `/review` to go on with the planner's assumptions. Otherwise the reviewer starts by itself.
3. **Plan review.** A block sends it back to the planner by itself. An approval stops for the owner.
4. **`/work`.** The owner's approval. An approved split files its stories as sub-issues with blocked-by links; each story then goes through the flow on its own. Otherwise the worker builds on a fresh machine and opens the PR.
5. **Code review.** The reviewer starts by itself when the worker finishes. A block sends it back to the worker by itself. An approval stops for the owner.
6. **Merge.** The owner approves and merges.

Agents work things out between themselves. The river stops and mentions the owner only on questions, approvals, an escalation, a hand-back code rejected, or three blocking reviews in a row at one stage since the owner last spoke. Every card ends with a **Next** line saying what happens next or what is the owner's to do.

## Commands

A command is the first word of an owner's comment on the issue or its PR, or of a PR review's summary submitted as a comment or a change request. Everything after it, and every other comment, review and line note, reaches the agent.

- `/plan`: the planner (re)plans. `/work`: the worker builds, or an approved split is filed. `/review`: the reviewer looks again; on an issue it grades the plan, on a PR the work.
- `/issue`: file the reviewer's proposed issues (planned).
- No command, nothing starts. Bots never start anything. An Approve never starts anything: it only ever means merge.
- Reviewers never start on the owner's command alone except `/review`; otherwise the river starts them.

## Questions

Only the planner asks the owner, as a plain list inside its plan, and only where the owner's words allow two readings and no principle or earlier decision settles it. Each question says which reading it planned for, so the owner may skip answering. The worker and the reviewer never ask: the plan is the contract, and disagreements reach the owner by escalation.

## The board

- Columns are stages: Backlog, Plan, Work, Review, Done. Every new item lands in Backlog.
- "Needs you" is a pill on the card, sorted to the top of each column, set exactly when the river stops for the owner and cleared otherwise. No swimlanes.
- The river moves each card to the stage now running. Priority (Blocker) is a field, not a label.

## The issue body

The body has two parts split by a fixed marker. Above it, the current-state card, redrawn by code every round. Below it, the owner's original ask, folded, exactly as written. Code only writes above the marker and checks the owner's part is unchanged before saving, or refuses and says why (planned).

## Agent records and cards

Every agent run posts one comment, written by code: a readable card on top in plain product words, the full JSON record folded below, and a footnote with the model, time, turns, tokens, API-equivalent cost and a one-click link to the run's whole conversation. Those comments are the permanent records; only comments the bot posted count as records. The card on top of the issue is drawn from them (planned). Each run also gets one live card from queued to done (planned, #164).

## Splitting and the graph

- Split when an issue has more than one independent objective, more than five criteria, or work in unrelated parts of the code. Don't split parts that can't land separately.
- 2 to 5 children, one level; every promise owned by exactly one child; children may depend on siblings, with no cycles.
- The planner proposes; code checks the rules and files real GitHub sub-issues. `/work` on the parent approves the split and every child's plan.
- When a child merges, every sibling whose needs have landed starts; independent children run in parallel. GitHub is the state.

## Changing scope

Never change the scope of an issue silently. Every change of scope is a comment or a native GitHub link.

- **Splitting** uses native sub-issues, each linking back to the parent. This is how `/work` files a split.
- **Merging or replacing** closes the old issue as a duplicate of the new one. GitHub links both ways.
- **Moving scope between issues** gets one short comment on each side ("moved X to #Y"). GitHub cross-links them, so the trail is two clicks either way.
- **A big reshuffle** of several issues closes the old ones as replaced by new ones that link back, instead of rewriting them.

## Identity and safety

- Agents act as the repo's own GitHub App (bot), never as a person. The bot can't approve, can't push workflow changes, and can't change settings.
- A build that changes a workflow file pauses until the owner approves it on GitHub; only then does a key held behind that approval push it (planned).
- Every run happens on a fresh, isolated machine with no access to the owner's computer. Agents hold no GitHub key while they work; code checks their output, then posts it.
- A chat agent may act as the owner's proxy with the owner's token, logged; the bot's own comments never start anything.
- Agent commits credit the owner as co-author (planned).

## Decisions log

- No hidden tests: in a public repo nothing stays hidden; the planner writing the tests covers most of the need.
- Approve on a PR only means "approve the result to merge".
- Tests map to criteria by the criterion number inside each test; criterion numbers are never reused.
- One PR per issue; replaced issues close as duplicates of what replaces them.
- Real GitHub reviews for code; comments for plans.
- Each repo declares its own setup and test command; Dokima never needs to understand a language (planned).
- Dokima lives in the `dokima-dev` organization so its bot can keep the project board and use the merge queue; on personal repos those extras fall back or are skipped.
- Onboarding is a few minutes from one link, never overwrites existing labels or files, and Dokima onboards itself first (planned).
