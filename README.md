# Dokima

**Agents are capable but unreliable. Dokima makes the system around them trustworthy.**

Dokima is a production-grade runtime for AI agents. It is the management layer around your agentic ecosystem: memory, execution, verification, resources and recovery, whichever models or clients you use.

> "Give me a machine, connect my preferred models, and let me delegate work to an assistant that remembers and follows through."

*Status: private and in active development. Source is not public yet.*

## You check the verification, not the work

Agents like Claude Code are strong, but someone has to check every step. Dokima moves the human from checking the work
to checking the verification, so agents can code unattended for much longer, with outcomes you can verify:

- **A contract per task:** a definition of done with held-out tests the agent never sees.
- **An independent reviewer:** judges the plan against your own request, and the work against the plan.
- **A merge gate:** nothing lands until the full suite passes.
- **An auditor on every run:** reads every step's input, output and handoff, and files what the machinery got wrong.

Your job shrinks to approving direction and promoting findings.

## Who it's for

- **Engineers, first.** Build on the runtime: define workflows, plug in tools, models and clients.
- **Everyone, next.** Install add-ons that engineers build, and customize your assistant without writing code.

## Why it exists

- **Memory across models and devices.** You shouldn't have to rebuild your context every time you change tools.
- **Verifiable execution.** An agent saying it finished is not evidence that it did.
- **Durable workflows.** Work should survive crashes, interruptions and long runs.
- **Controlled orchestration.** You decide what each model can see and do.
- **A common runtime.** All of this should work across models, clients and, eventually, machines.

## Three guarantees

### Isolation
- **Sandboxing.** Each worker runs sealed, with one way out. Network isolation makes verification provable.
- **Orchestration.** Workflows define exactly what each model sees, may do, and which tools it gets.
- **Scheduling.** Resources and conflicts are managed so parallel, interdependent work lands on its own unless it truly collides.

### Continuity
- **Unified memory.** Conversations, decisions, plans, runs and work history live in one index, across models, subscriptions and devices.
- **Brokerage.** One relay is the only door to any model. It routes, logs every call, and keeps many clients in sync.
- **Durability.** Checkpoints and automatic recovery carry work through crashes and restarts. Every step hands off to the next.

### Verification
- **Evidence, not claims.** Work is graded by locked tests the agent can't see or edit. Done means demonstrated.
- **Adaptation.** Dokima scans its memory for statistically significant patterns and proposes evidence-based improvements. You approve.

## Scope

A genuinely useful system doesn't need thousands of machines:

- One machine, with bounded compute and concurrency
- One persistent personal agent, with many specialized workflows
- One memory and task history
- Scheduling, checkpoints and recovery
- Verification and permission boundaries
- An extensible interface for tools, models and clients

## Life OS: the first add-on bundle

Life OS is a personal assistant built on Dokima, and the proof of what it can do: its own always-on computer, one conversation shared across voice, chat and a pocket device, and a gateway to mail, the browser and the owner's other machines.

---

Built by [Reza Soleymanifar](https://github.com/RezaSoleymanifar).
