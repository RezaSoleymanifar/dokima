# Dokima

**Agents are capable but unreliable. Dokima makes the system around them trustworthy.**

Dokima is an agent runtime that uses GitHub Actions as its orchestrator. You describe a task in a GitHub issue. Isolated AI sessions plan it, build it and review it, and nothing reaches your main branch until it is proven.

There are no servers to run and no database. Your repository, its issues and its pull requests are the whole system.

> **Status:** in active development. Pages describe the design; features marked *planned* are not built yet.

## You check the verification, not the work

Coding agents are strong, but someone still has to watch every step. Dokima moves you from checking the work to checking the verification. You approve the plan, you accept the result, and the runtime guarantees everything in between.

## How it works

```
issue ──► Planner ──► you approve ──► Worker ──► Reviewer ──► Gate ──► main
```

1. **You open an issue** saying what you want and how to tell it's done. See [Writing issues](Writing-issues).
2. **The planner** turns it into a plan and the tests that will prove it, then waits for your go. You approve the plan by adding the `work` label to the issue. *Planned.*
3. **The worker** writes code to make those tests pass. It cannot change them.
4. **The reviewer**, a fresh session that never talked to the worker, checks the change against the plan. *Planned.*
5. **The gate** merges only when the full test suite passes against the latest main.

Each role runs as its own GitHub Actions job on its own clean machine. Labels on the issue say whose turn it is. At every step you see a [card](The-card): what was promised, and the proof it was delivered.

## Production-grade by design

- **Separation of duties.** Planner, worker and reviewer run as separate sessions on separate machines. None can see, steer or vouch for another.
- **Tamper-proof grading.** Tests are written before the work and locked during it. A change that edits them fails, even if everything passes.
- **Independent review.** A read-only reviewer blocks gamed tests and changes outside the task's scope.
- **A merge gate.** Main never breaks. Nothing lands until it is green against the latest main, and the rule applies to everyone, admins included.
- **Durable execution.** Work is committed after every step, so a crash or timeout resumes instead of starting over.
- **Fast verification.** Large test suites split across many machines at once.
- **Full audit trail.** Every plan, step, review and decision is a commit, comment or log on GitHub.
- **Least privilege.** Each role gets only the permissions its job needs. Secrets stay in GitHub's encrypted store.

## Pages

- [Writing issues](Writing-issues): how to describe a task so it can be verified
- [The card](The-card): how Dokima shows you what it did and proves it
- [FAQ](FAQ): why GitHub, why pull requests, and other design choices
