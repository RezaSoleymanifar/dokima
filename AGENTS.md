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

## The flow

1. **Issue.** The owner writes what they want, in plain words.
2. **`/plan`.** The planner writes the plan and its tests into the issue; the reviewer checks it. Too big: it proposes a split. Wrong ask: it says why, with evidence, and offers options, ending with one question.
3. **`/work`.** The owner's approval. The plan freezes at that moment; edits after it are listed on the card but used only after the next `/work`.
4. **Build.** The worker builds on a fresh machine and opens the PR.
5. **Prove.** Each criterion runs as its own check; all tests run too.
6. **Review.** The reviewer leaves a PR review and a list of proposed issues.
7. **Merge.** The owner approves. Auto-merge and the merge queue merge it once every check passes (planned).

Commands count only as the first line of an owner's comment: `/plan`, `/work`, `/review` followed by prose in the same comment (re-runs the reviewer with your words, for example changes to its proposed issues) and `/issue` (create every issue on the latest proposed list, each linking back). Amending the current issue goes through `/plan`. (Commands are planned; today `plan` and `work` labels start the stages.)

## Labels and the board

- Labels show the stage only: `plan`, `work`, `review`, set by code, never by people (planned).
- The org's project board shows every issue and PR: Waiting on me, Done, By stage, Priority. Priority and "waiting on" are board fields, not labels, so Dokima adds as few labels as possible. Newest items sit at the top.

## The card

The same card sits on the issue and its PR, drawn by code from GitHub's records. It shows the stage, links, each objective with its criteria, GitHub's verdict on each, and all tests. "Acceptance criteria" links to the check run; "Verified by" is one plain sentence that links to the test itself (planned). The issue's journey (plan, each try, each review, merge) sits in a fold as a small diagram (planned).

## Comments

Every stage change posts one comment from a fixed template written by code: plan started, plan ready, question asked, plan rejected, build started, build failed, PR opened, merged (planned). A model's words appear only in a template's slot: the plan, the question, the proposed issues. Running progress lives on the card and in the run log, not in comments.

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
