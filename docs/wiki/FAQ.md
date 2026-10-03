# FAQ

### Why GitHub Actions instead of a custom orchestrator?

GitHub already provides what a runtime needs: clean machines for every job, a place to store tasks and state, permissions, secrets, logs, and a merge gate. Dokima adds only the rules on top. That means nothing to host, nothing to keep running, and nothing that can drift out of sync with your repository.

### Why does every change go through a pull request?

A pull request is a proposal to merge, plus the page where tests run, reviews happen and history is kept. Dokima treats AI workers like outside contributors to an open-source project: trusted to propose, never to merge on their own say-so. Every change, including the repository owner's, passes the same gate.

### What stops an agent from cheating?

Several independent layers:

- the tests are written before the work and locked during it,
- the worker never sees the reviewer, and the reviewer never talks to the worker,
- the reviewer is told to block changes that game the tests,
- the gate is a GitHub setting, enforced by GitHub, not by the agent.

### Does it work on private repositories?

Yes. On GitHub's free plan the merge gate is only enforced on public repositories; for private ones you need GitHub Pro.

### What does it cost to run?

The Actions minutes come from your GitHub plan; public repositories get unlimited free minutes. The AI sessions use your Claude subscription or API key.

### Where is the state kept? What if a job crashes?

In GitHub: labels say whose turn it is, the issue holds the task, and the branch holds the work. Workers commit after every step, so a crashed or timed-out job resumes from the last commit. *Planned.*

### Why isn't there a dashboard?

GitHub's pull request and Actions pages already show the full history of every task, step by step. A separate dashboard would be a second copy to keep in sync.

### Can it do work other than code?

The same flow fits any task with checkable results, such as a research brief or a job application: the reviewer checks facts and fit, and anything that leaves your hands, like sending or submitting, waits for your approval. *Planned.*

### Where do these docs come from?

They live in the repository under `docs/wiki/` and are copied to this wiki automatically whenever they change. Like code, every edit goes through a pull request.
