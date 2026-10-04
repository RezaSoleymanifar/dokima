# Dokima design

*The one place for Dokima's design. Decisions land here once they're made; the issues hold how we got there.*

## The picture

You are a senior engineer. Your team is remote engineers: agents that each take one narrow, well-defined task, do it on their own machine, and hand back work you can check. They plan, build and review each other's work in the open, on GitHub, the way people already work. You don't sit in every conversation. You approve the plan before work starts, you approve the result before it merges, and you step in when they can't agree.

GitHub is the office: issues are the tasks, pull requests are the work, reviews and comments are the conversation, and checks are the proof. Nothing new to learn.

## Principles

- **Nothing merges until it's proven.** Every promise in a plan has its own check, and GitHub's own verdict on that check is the proof. No model's say-so counts as proof.
- **Use what GitHub already has.** Labels, sub-issues, reviews, comments, checks, branch protection, CODEOWNERS. Build only the thin glue GitHub lacks.
- **Humans are free; bots are compliant.** People can do anything, and their choices stay on the record. Agents work inside fixed rules they cannot change: they can't approve, can't edit the workflows that judge them, and can't widen their own scope.
- **Everything lives on GitHub.** The issue holds the decisions, the PR holds the work, and the history stays recoverable in both directions. No side channels that lose the trail.
- **Fail closed.** Missing proof, a missing reviewer or a broken check blocks; it never waves work through.
- **No hard-coded people or agents.** Approvers come from CODEOWNERS; each agent plugs in through a small adapter; nothing assumes one person or one vendor.
- **Small and lean.** One issue, one PR. Fold related things together; avoid machinery for problems that are cheap to recover from.

## Roles

- **Owner (you):** approves plans and results. Only a code owner's actions count.
- **Planner:** turns a rough issue into a plan: goals, criteria, and how each is verified. It judges the ask first and raises a concern only with evidence. It proposes splits; it never writes code.
- **Reviewer:** checks the plan right after the planner (comments on the issue), and the work right after the worker (a real PR review, with line notes, "request changes" or approve). It blocks only on a promise with no proof, or a proof that proves nothing.
- **Worker:** builds what the approved plan says, on a fresh machine, and nothing outside its scope.
- **Code (workflows):** does everything that must be exact: freezing the plan, filing sub-issues, starting work in order, running checks, drawing the card.

## The flow

1. **Issue.** Someone writes what they want, in plain words.
2. **Plan.** The planner writes goals, criteria and "Verified by" lines into the issue; the reviewer checks it. Too big: the planner proposes a split instead. Wrong ask: the planner says why, with evidence, and offers options.
3. **Approve the plan.** The owner adds the `work` label. The plan is frozen at that moment; edits after it are listed on the card but not used until `work` is added again.
4. **Build.** The worker builds on a fresh machine and opens the PR.
5. **Prove.** Each criterion runs as its own GitHub check; the full test suite runs too.
6. **Review.** The reviewer leaves a PR review; worker and reviewer iterate.
7. **Approve the result.** The owner approves and merges. Nothing merges without every check passing and the owner's approval.

## The card

The same card sits at the top of the issue and its PR. It shows the stage, links (never to the page it's on), each goal with its criteria indented beneath, a circle for GitHub's verdict on each, "Criteria" as the link to its proof, "Verified by" underneath, and the full suite. Code draws it from GitHub's records; no AI writes it.

## Splitting and the graph

- Split when an issue has more than one independent goal, more than five criteria, or work in unrelated parts of the code. Don't split when the parts can't land separately.
- 2 to 5 children, one level only; every promise owned by exactly one child; children may need siblings, with no cycles.
- The planner proposes; code checks the rules and files real GitHub sub-issues. `work` on the parent approves the split and every child's plan.
- The graph runs itself: when a child merges, every sibling whose needs have landed starts; independent children run in parallel; a failed child holds back what depends on it. GitHub is the state.

## Conversation

- Agents and people talk in comments and reviews, on the issue or PR the work belongs to. A code owner can address the pipeline with "@dokima ...".
- An agent that needs the owner asks in a comment and waits; the reply goes back into the same run.
- Sensitive work belongs in a private repo (or a private companion repo); secrets are used by fixed steps the agent can't read.

## Identity and safety

- Agents act as the repo's own GitHub App (bot), never as a person. The bot can't approve, can't edit workflows, and can't change settings.
- The owner's token is used only for what the bot is barred from, and every use is logged.
- Only a code owner's `work` label starts work; strangers can't spend your agents.

## Decisions log

- No hidden tests: in a public repo nothing stays hidden, and the planner writing the tests (not the worker) covers most of the need.
- Plans are approved with the `work` label, not the Approve button; Approve only means "approve the result to merge".
- The same card on the issue and the PR, written by code.
- Criteria are matched to tests by number inside each test; changing a plan means re-adding `work`, and the worker retags.
- One PR per issue; parents do nothing on `work` except approve a proposed split.
- Replaced issues close as duplicates of what replaces them.
- Real GitHub reviews for code; comments for plans.
- Onboarding creates the repo's Dokima labels and writes a fenced "Dokima settings" section into AGENTS.md; versioned releases (v0.1.0) start with the first outside install.
