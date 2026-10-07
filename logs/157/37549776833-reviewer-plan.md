# reviewer (plan) for #157

Run: https://github.com/dokima-dev/dokima/actions/runs/37549776833

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 36
> drwxr-xr-x  3 runner runner 4096 Oct  7 00:02 .
> drwxrwxrwt 18 root   root   4096 Oct  7 00:02 ..
> drwxr-xr-x  2 runner runner 4096 Oct  7 00:02 in
> -rw-r--r--  1 runner runner 9333 Oct  7 00:02 issue.md
> -rw-r--r--  1 runner runner    2 Oct  7 00:02 open_blockers.json
> -rw-r--r--  1 runner runner 4819 Oct  7 00:02 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  7 00:02 .
> drwxr-xr-x 3 runner runner 4096 Oct  7 00:02 ..
> -rw-r--r-- 1 runner runner 5442 Oct  7 00:02 01-planner.json
> # Issue #157: The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 4</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** The worker's and the reviewer's hand-backs reach the owner only in the shape their prompts define, every blocker is about one of the plan's criteria, and a rejected run says why on the issue.
> 
> **Context:** dokima/agent.py problems_review and problems_work check a few fields, crash on a string where an object belongs (blockers: ['B1'] raises AttributeError) or a number where a list belongs (notes: 5 raises TypeError), never check work.json gives a line for every plan criterion, and only check that a blocker's criterion is non-empty. `agent check` does not get the plan or the issue number today, so .github/workflows/agent.yml must pass them; agent.yml also 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; cat tests/test_handback_check.py; wc -l dokima/agent.py
```

> commit cd3da95f0daf9b629bcecc082848b3afb401cbd7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Tue Oct 6 23:26:13 2026 +0000
> 
>     planner for #157 (run 37546155879)
> 
>  tests/test_agent.py          |   2 +-
>  tests/test_handback_check.py | 246 +++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 247 insertions(+), 1 deletion(-)
> """The worker's and reviewer's hand-backs are checked against their prompt's shape and the approved plan, from outside.
> 
> Every test runs the real command the workflow runs, `python3 -m dokima.agent check review|work FILE PLAN N`, on files in
> a temp folder, so it proves what a run sees: the exit code, the reasons printed, and never a crash. A plan for issue 9
> with two acceptance criteria and one non-functional requirement (9.1, 9.2, 9.3) stands in for the approved plan.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> 
> STORY = {"kind": "user_story", "user_story": "u",
>          "acceptance_criteria": [{"text": "a", "source": "https://x/9"}, {"text": "b", "source": "https://x/9"}],
>          "non_functional": [{"text": "c", "why": "w", "principle": "Fail closed"}],
>          "scope": ["dokima/x.py"], "out_of_scope": [],
>          "tests": {"9.1": ["tests/test_x.py::test_a"], "9.2": ["tests/test_x.py::test_b"], "9.3": ["tests/test_x.py::test_c"]}}
> SPLIT = {"kind": "feature", "feature": "f", "stories": [
>     {"title": "One"

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat dokima/agent.py; cat .github/workflows/agent.yml
```

> <persisted-output>
> Output too large (39.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/bdcdb66d-115b-462a-ad46-859d30c0b843/tool-results/byfhwpqp8.txt
> 
> Preview (first 2KB):
> """Packs and hand-back checks for running one agent by hand on a fresh machine.
> 
> `pack` builds the agent's starting pack from GitHub's records: the issue as it stands (body and every comment) and the
> JSON hand-backs of earlier runs, downloaded from those runs. `check` is the deterministic check an agent runs on its own
> hand-back before it finishes, and that code runs again after it: a malformed hand-back never reaches the next agent.
> The plan's own check lives in dokima/planner.py; this module adds review.json and work.json.
> """
> import glob
> import json
> import os
> import re
> import shutil
> import subprocess
> import sys
> 
> VERDICTS = {"approve", "block", "escalate"}
> ANSWERS = {"fixed", "disagree"}
> 
> 
> def gh(*args):
>     """Run the GitHub CLI and return its output."""
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> MARK = "<!-- dokima-record -->"
> BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
> HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 
> 
> def linked_prs(repo, number):
>     """Pull requests built for the issue: from its work or try branch."""
>     found = []
>     for head in (f"work/issue-{number}", f"try/issue-{number}"):
>         found += json.loads(gh("pr", "list", "-R", repo, "--head"

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def \|sys.argv\|argv" dokima/agent.py | head -60; sed -n '/def problems_review/,/^def pack/p' dokima/agent.py | head -150
```

> 20:def gh(*args):
> 30:def linked_prs(repo, number):
> 38:def conversation(repo, number):
> 54:def issue_text(d, items):
> 62:def records(items):
> 77:def latest(recs, role, passed=True):
> 85:def approved(recs):
> 95:def is_record(c, role=None, stage=None):
> 103:def open_blockers(recs, stage):
> 111:def problems_round(role, h, pack_dir):
> 122:def story_body(parent, i, story, parent_title):
> 136:def file_split(repo, parent, recs):
> 163:def build_record(role, stage, out, check_text, passed, meta):
> 178:def render(rec):
> 217:def jsonl_files(root):
> 222:def scrub(text, secrets):
> 229:def transcript(log_dir, secrets=()):
> 255:def run_report(path):
> 267:def footnote(rec):
> 286:def models_used(log_dir):
> 300:def pack(repo, number, role, stage, dest):
> 324:def problems_questions(qs):
> 332:def problems_review(r):
> 369:def problems_work(w):
> 389:def check(kind, path):
> 413:def problems_pack(role, stage, dest):
> 460:def command_of(body):
> 466:def issue_of_pr(head, body):
> 472:def route(body, on_pr, number, head="", pr_body=""):
> 486:def main(argv):
> 489:    if argv[1] == "pack":
> 490:        has_plan = pack(os.environ["GITHUB_REPOSITORY"], argv[2], argv[3], argv[4], argv[5])
> 491:        return 0 if has_plan or argv[3] == "planner" else 3
> 492:    if argv[1] == "check":
> 493:        return check(argv[2], argv[3])
> 494:    if argv[1] == "check-pack":
> 495:        bad = problems_pack(argv[2], argv[3], argv[4])
> 499:    if argv[1] == "record":
> 500:        role, stage, out, check_file, passed, log_dir = argv[2:8]
> 510:    if argv[1] =

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/agent.yml; sed -n 100,125p dokima/agent.py; sed -n 160,300p dokima/agent.py
```

> name: agent
> run-name: "${{ inputs.role }}${{ inputs.role == 'reviewer' && format(' ({0})', inputs.stage) || '' }} for #${{ inputs.issue }}"
> # Runs one agent on a fresh GitHub machine. Started by hand here, or by commands.yml when a code owner's comment
> # starts with /plan, /work or /review. Code gathers everything the agent needs: the issue and its PR as one
> # conversation (comments, reviews, line notes) and every earlier agent record. The agent runs its own check before it
> # finishes; code runs it again, then posts this run's record as a comment: a card on top, the full JSON folded below.
> # Those comments are the permanent records the cards are built from. Session logs stay on the run page.
> on:
>   workflow_call:
>     inputs:
>       role: {type: string, required: true}
>       stage: {type: string, default: plan}
>       issue: {type: string, required: true}
>   workflow_dispatch:
>     inputs:
>       role:
>         description: Which agent
>         type: choice
>         options: [planner, reviewer, worker]
>       stage:
>         description: For the reviewer, what it grades
>         type: choice
>         options: [plan, pr]
>         default: plan
>       issue:
>         description: Issue number
>         required: true
> concurrency:
>   group: agent-${{ inputs.issue }}
>   cancel-in-progress: false
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
>   actions: read
> jobs:
>   run:
>     environment: keys
>     runs-on: ubuntu-24.04
>     env:
>       N: ${{ inputs.issue }}
>       ROLE: ${{ inputs.rol

**Agent:** I'm reviewing the plan for #157. Next I'll run the planner's new tests against main to check that each one fails for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_handback_check.py 2>&1 | grep -E "^(FAILED|PASSED|E  )|passed|failed" | head -40; python3 -m pytest -q 2>&1 | tail -3; git show HEAD -- tests/test_agent.py
```

> >       assert code == 1, f"{crit}: the {kind} check passed (exit {code}) a hand-back it should reject: {case}"
> E       AssertionError: 157.1: the review check passed (exit 0) a hand-back it should reject: {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []}, "verdict": "block", "summary": 5, "blockers": [{"id": "B1", "criterion": "9.1",
> E       assert 0 == 1
> E           AssertionError: 157.1: the round check crashed on {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []}, "verdict": "block", "summary": "One proof is missing.", "blockers": ["B1"], "no:
> E             ima/agent.py", line 557, in <module>
> E                 sys.exit(main(sys.argv))
> E                          ^^^^^^^^^^^^^^
> E               File "/home/runner/work/dokima/dokima/dokima/agent.py", line 516, in main
> E                 bad = problems_round(argv[2], h if isinstance(h, dict) else {}, argv[4])
> E                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E               File "/home/runner/work/dokima/dokima/dokima/agent.py", line 116, in problems_round
> E                 carried = set(h.get("resolved", [])) | {b.get("id") for b in h.get("blockers", [])}
> E                                                         ^^^^^
> E             AttributeError: 'str' object has no attribute 'get'
> E             
> E           assert 'Traceback' not in "Traceback (...bute 'get'\n"
> E             
> E             'Traceback' is contained here:
> E    

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -A25 "work.json" dokima/roles/worker.md | head -60; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('check'))"
```

> 12:   today; if one already passes, say so in work.json.
> 13-3. Find the cause, not the symptom. Before editing, write one line for yourself: what is missing or wrong, where, and why
> 14-   the failure follows from it. If you cannot write that line, read more; an edit without a cause is a guess.
> 15-4. Build exactly the behavior each criterion describes, as the owner wrote it, in the repo's existing style. Nothing
> 16-   more: no refactors, renames, new files or dependencies the plan did not ask for. Every extra line is something the
> 17-   reviewer must clear, and changes outside the plan's scope are flagged on the pull request.
> 18-5. Verify by running, not by reasoning. After each change run the narrowest test that exercises it, then all tests. One
> 19-   change at a time when you are still finding your way, so when something breaks you know which change did it.
> 20-6. When stuck, change approach, not effort. If the same failure survives two attempts, stop editing, reread the failure
> 21-   and your cause line, and name the assumption that was wrong. Repeating a failed fix only burns the budget.
> 22-7. The tests are not yours to satisfy by other means. Never edit, rename, skip, mock or weaken a test or anything it
> 23-   imports to fake; never special-case a test's inputs, hard-code its expected output, or swallow the error it expects;
> 24-   never read the workflows or checkers to learn how to pass them. The reviewer looks for each of these and rejects the
> 25:   whole pull request. I

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "github\|workflow" dokima/fence.py | head; git log --oneline -15 --stat | grep -B3 "workflows" | head -30
```

> tests/test_handback_check.py | 246 +++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 247 insertions(+), 1 deletion(-)
> 78fe9eb /work on an approved split files its stories as sub-issues (#153)
>  .github/workflows/commands.yml | 28 +++++++++++++-
> --
>  tests/test_agent.py            | 51 ++++++++++++++++++++++++-
>  4 files changed, 162 insertions(+), 14 deletions(-)
> 4ee37e0 Dokima's own code always runs from main; no numbering of the owner's notes (#150)
>  .github/workflows/agent.yml | 10 ++++++---
> --
>  tests/test_agent.py         | 49 ++++++++++++++++++++++-----------------------
>  6 files changed, 58 insertions(+), 84 deletions(-)
> 056bffa Commands start stages, agent outputs are comments, every round answers everything (#149)
>  .github/workflows/agent.yml    | 112 +++++++++----
>  .github/workflows/commands.yml |  51 ++++++
> --
>  tests/test_plan.py             |   3 +
>  8 files changed, 639 insertions(+), 132 deletions(-)
> 5e8f247 Opus 5.5 everywhere, and permanent records that build every pack (#147)
>  .github/workflows/agent.yml   |  96 ++++++++++++-----------
>  .github/workflows/planner.yml |   2 +-
>  .github/workflows/worker.yml  |   2 +-
> --
>  tests/test_agent.py        | 11 +++++++++++
>  7 files changed, 41 insertions(+), 4 deletions(-)
> cdc6d5c Run any agent by hand on a fresh machine: packs from GitHub's records, self-checks, JSON hand-backs (#145)
>  .github/workflows/agent.yml | 155 ++++++++++++++++++++++++++++++++++++++++++++
> --
>  tests/test_agent.py         |  57 ++++++++++++

`9. Bash`
```
cd /tmp && mkdir -p /tmp/rv/p && echo '[{"id":"B1"}]' > /tmp/rv/p/open_blockers.json && echo '{"summary":"s","criteria":{},"evidence":"e","replies":5}' > /tmp/rv/w.json && cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check-round worker /tmp/rv/w.json /tmp/rv/p 2>&1 | tail -2; echo '{"summary":"s","criteria":{"9.1":"a"},"evidence":"e","outside_scope":[{"file":"b.py"}]}' > /tmp/rv/w2.json; python3 -m dokima.agent check work /tmp/rv/w2.json; echo rc=$?
```

> ^^^^^^^^^^^^^^^^^^^^
> TypeError: 'int' object is not iterable
> rc=0

`10. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote four acceptance criteria from the story and one fail-closed requirement (157.5): every worker and reviewer run checks its hand-back against the plan and the issue number, and a missing or unreadable plan rejects it.",
          "Wrote seven tests in tests/test_handback_check.py that run the real check commands; all seven fail today for the missing feature, and one older test's notes case now uses well-formed notes."],
  "decided": ["Planned for a rejected worker or reviewer hand-back to post its comment on the pull request once one is open, not on the issue."],
  "open": ["Asks the owner whether that comment goes on the pull request or always on the issue; notes that most of 157.4 already shipped in #149."]},
 "verdict": "block",
 "summary": "The plan is sound and its tests fail today for the right reason, but the tests for 157.1 leave some item shapes and the worker's round check unproven, so code that half-checks them would pass.",
 "blockers": [
  {"id": "B1", "criterion": "157.1",
   "test": "tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named",
   "problem": "157.1 promises that an item of the wrong shape is rejected and that the check never crashes, but for most lists the tests only try an item that is a bare string, never an object missing one of its fields. A check that only asks 'is it an object?' for outside_plan, outside_scope and notes passes every case. The round check is proven not to crash for the reviewer only; the worker's round check still crashes and no test catches it.",
   "evidence": "work_cases has ('outside_scope', ['b.py']) but no {'file': 'b.py'} without why; review_cases has ('outside_plan', ['a.py']) but no {'file': 'a.py'} without change, and no note without evidence or blocker whose test is a number. Today `check work` on {\"summary\":\"s\",\"criteria\":{\"9.1\":\"a\"},\"evidence\":\"e\
```

> rc=0

**Agent:** I blocked the plan for #157, with one blocker. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the planner did:** It wrote four acceptance criteria from the story, plus one fail-closed requirement (157.5): every worker and reviewer run checks its hand-back against the plan and the issue number, and a missing or unreadable plan rejects it. Its seven new tests in `tests/test_handback_check.py` all fail on main because the feature is missing, not because of a crash or bad setup. The other 128 tests pass.

**The blocker (B1, criterion 157.1):** 157.1 promises that a list item of the wrong shape is rejected and that the check never crashes. The tests don't fully prove either:
- **Item shape:** most lists are only tested with a bare string as an item. No test has an object that is missing one of its fields, so a check that only asks "is this an object?" would pass. For example, `check work` on main accepts an `outside_scope` item with a file but no `why` and exits 0.
- **No crash:** only the reviewer's round check is tested. The worker's round check (`check-round worker`) still crashes today on `"replies": 5` with `TypeError: 'int' object is not iterable`, and no test catches that.
- **The smallest fix:** add these cases: a note with no evidence, an `outside_plan` item with no `change`, a blocker whose `test` is a number, an `outside_scope` item with no `why`, and a suspect test with no `test`. Also run the worker's round check with `replies` set to `5` and to `["B1"]`.

**Two notes, not blocking:**
- **Pull request or issue:** criterion 4 is planned for a comment on the pull request once one is open, but the owner's story says "the issue gets one comment". The planner asked the owner instead of choosing silently. The owner's answer should settle the wording before `/work`.
- **Issue number:** every test uses issue 9 with a plan whose criteria are 9.x. A check that ignores the issue number would pass them all. One case using a different number would show the number is actually used.
