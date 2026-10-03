# Dokima design

The living record of how Dokima works and why. Updated through pull requests as the system is built, so it never drifts from the code.

## What Dokima is

An agent runtime that uses GitHub Actions as its orchestrator. A task is a GitHub issue. Isolated AI sessions plan, build and review it, and nothing reaches main until it is proven. GitHub is the whole system: issues hold the work, labels hold the state, pull requests hold the proof.

## Principles

- **Port intent, not code.** Nothing is carried over from earlier systems unless a story needs it.
- **Use GitHub's own features.** Dokima adds nothing GitHub already has: forms, labels, sub-issues, "blocked by" links, branch protection, project boards.
- **One source of truth.** The issue is the record. No mirrors, no caches, no second copy to drift.
- **Rules are enforced in code, not prose.** One definition per rule, read by both the instruction and the check.
- **The human checks the verification, not the work.** Every unit of work is shown as a card (below).
- **Add complexity only on evidence.** A mechanism returns only after the same failure shows up twice.

## Issues

An issue has three fields:

1. **Title:** the outcome, as a sentence you could check.
2. **Goals and checks** (required): a checklist, with each goal's checks nested under it. A goal is done when its checks are done.
3. **Where to look** (optional): file paths, one per line.

```markdown
- [ ] Goal: issues are written the same way every time
  - [ ] the new-issue page shows the form
  - [ ] an issue missing checks is bounced back
```

Blank issues are allowed; nothing runs until an issue has goals and checks. The issue form and the issue check read the same field list, so issues made through the website, the API or Claude are held to the same standard.

**Splits:** a large issue becomes sub-issues, and the parent becomes a placeholder that closes when its children close. A split agreed in chat is created directly; a split the planner proposes waits for the owner's "go."

**The planner as architect:** before planning, it reads related open issues, flags duplicates and conflicts, rejects checks that can't be verified, and proposes rewrites or splits instead of guessing.

## The card

Every unit of work is reported the same way, twice: before it starts and after it ends.

```markdown
Goal: nothing reaches main unless tests pass
- ✅ A failing PR can't merge. Proof: <link to GitHub's record>
- ☐ A passing PR can merge. Verify: <how it will be shown>

Not checked: <what is deliberately out of scope>
```

**Proof** is a link to GitHub's own record (a test run, a blocked merge, a rule as GitHub reports it), so no one has to take the agent's word. Where there is no page, GitHub's exact response is quoted.

**Enforcement:** cards are built by a script from the issue's checks and GitHub's check results, and posted by the workflow. No model writes, skips or rewords them. In chat, Claude relays the same card.

## Pull requests

A branch is a parallel line of commits; a pull request is a proposal to merge it into main, plus the page where checks run, reviews happen and history is kept. AI workers are treated like outside contributors: every change, including the maintainer's own, arrives as a pull request and passes the gate.

## The gate

Main is protected:

- the `tests` check must pass,
- the branch must be up to date with main,
- the rule applies to admins too,
- no force pushes, no deletions.

## Decisions

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-03 | Dokima repo is public | Free unlimited Actions minutes; shareable runtime. Private projects get GitHub Pro when plugged in. |
| 2026-10-03 | Python and pytest for the pipeline's own tests | Simple and readable. |
| 2026-10-03 | No custom run page | GitHub's PR and Actions pages already show the full history. Revisit after real runs. |
| 2026-10-03 | No MCP tool yet | Useful later for fetching cards from any chat; not needed until the pipeline posts them. |
| 2026-10-03 | Docs live in the repo, not the GitHub wiki | The wiki sits outside the gate and drifts from the code. |

## Build log

**Step 1: tests run automatically.** Done 2026-10-03.
- ✅ On every change to main. Proof: run on commit `e3538f4`.
- ✅ On every pull request. Proof: [PR #3](https://github.com/RezaSoleymanifar/dokima/pull/3).

**Step 2: nothing reaches main unless tests pass.** Done 2026-10-03.
- ✅ Rule covers everyone, admins included. Proof: rule as reported by GitHub.
- ✅ A failing PR can't merge, even with admin override. Proof: [PR #4](https://github.com/RezaSoleymanifar/dokima/pull/4), [red run](https://github.com/RezaSoleymanifar/dokima/actions/runs/37142676806/job/111260168556).
- ✅ A passing PR can merge. Proof: [green run](https://github.com/RezaSoleymanifar/dokima/actions/runs/37142710627/job/111260268858).
- ✅ Direct pushes to main are rejected. Proof: GitHub answered *"Required status check "tests" is expected"* (HTTP 409).

**Next:** step 3, connect Claude; step 4, the worker; then issue #1, the smoke test.
