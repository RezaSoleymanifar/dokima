# reviewer (plan) for #294

Run: https://github.com/dokima-dev/dokima/actions/runs/37885609339

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (53.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/80ec427c-7524-40c9-946e-027ef770923c/tool-results/bmnm8bb5s.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:49 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:49 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:49 in
> -rw-r--r--  1 runner runner 48335 Oct  9 04:49 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 04:49 open_blockers.json
> -rw-r--r--  1 runner runner  5739 Oct  9 04:49 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:49 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:49 ..
> -rw-r--r-- 1 runner runner 7017 Oct  9 04:49 01-planner.json
> -rw-r--r-- 1 runner runner 3955 Oct  9 04:49 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6392 Oct  9 04:49 03-planner.json
> # Issue #294: The Blocker pill is computed from blocked-by links, not set by hand
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 253, 254, 282 -->
> The Blocker pill on the board follows GitHub's blocked-by links instead of a label someone sets by hand.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #294](https://github.com/dokima-dev/dokima/issues/294)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" he

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; sed -n '/dokima-card-end\|<!-- dokima-body -->/,$p' issue.md | head -50; grep -n "^## \|^### \|^---" issue.md | head -50
```

> {
>  "kind": "user_story",
>  "summary": "The Blocker pill on the board follows GitHub's blocked-by links instead of a label someone sets by hand.",
>  "user_story": "The owner sees Blocker on exactly the open issues that hold up another open issue, kept current by code from GitHub's blocked-by links, with nothing to set or clear by hand.",
>  "acceptance_criteria": [
>   {
>    "text": "An open issue that blocks at least one other open issue shows Blocker as its Priority pill on the board, computed from GitHub's blocked-by links. One that blocks nothing, or only closed issues, shows no Blocker: its pill follows its high or parked label, or stays empty. Blocker wins over a high label. Code writes a card's Priority only when the pill changes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/294"
>   },
>   {
>    "text": "When the last open issue it blocks closes, an issue loses its Blocker pill in that same board run. It keeps the pill while it still blocks another open issue. An issue that closes loses its own Blocker pill. When a blocked issue reopens, the issues blocking it show Blocker again.",
>    "source": "https://github.com/dokima-dev/dokima/issues/294"
>   },
>   {
>    "text": "A blocked-by link added or removed, by hand or by code, reaches the pill within 15 minutes. The board workflow runs every 15 minutes and recomputes every open issue's pill. A repo with no board, or a board with no Priority field, is left alone.",
>    "source": "https://github.com/dokima-dev/dokima/issues/29

`3. Bash`
```
cd /tmp/pack; sed -n 40,100p issue.md; sed -n 430,445p issue.md; sed -n 635,700p issue.md
```

> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Non-functional requirement:** When GitHub cannot list an issue's blocked-by links, that issue's pill is left as it is. The other issues are still updated, and the board run fails with exit code 1 and an error naming the issue and GitHub's answer.
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-294/tests/test_blocker_pill.py#L345"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: Unread links leave the pill as it is, and the run fails naming the issue.*
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-294/tests/test_blocker_pill.py#L368"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: The scheduled board run with unread links exits 1 with an error saying why.*
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-294/tests/test_blocker_pill.py#L448"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: When GitHub refuses the links, the board's read fails instead of answering none.*
> 
> </details>
> 
> **Scope:**
> 
> - dokima/

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['02-reviewer-plan.json','03-planner.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:5000])
"; cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -20
```

> 02-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37884447330",
>  "commit_before": "27a1d7093fe94f7885adcaa538f93746cdfcdcda",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 3621,
>   "turns": 2,
>   "cost_usd": 0.5373696,
>   "tokens_in": 109517,
>   "tokens_out": 236
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/294/37884447330-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37884447330",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner wrote four criteria and one fail-closed requirement for a Blocker pill that follows GitHub's blocked-by links, with 16 new tests and 7 changed ones."
>    ],
>    "decided": [
>     "The board run recomputes every open issue's pill on close, on reopen and on a schedule every 15 minutes; the blocker label stops counting and leaves the manifest.",
>     "When GitHub cannot list an issue's links, that issue's pill stays as it is and the run fails with exit code 1 naming the issue."
>    ],
>    "open": [
>     "Whether a 15-minute delay is acceptable for a link changed by hand.",
>     "Whether Dokima stops declaring the blocker label altogether."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The plan covers your three asks with tests that fail today for the right reason; both questions change how the board works, so you decide.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "The work adds a reopened trigger and a 15-m

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_blocker_pill.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -30; python -m pytest -q tests/test_board.py tests/test_manifest.py 2>&1 | tail -5; cat tests/test_blocker_pill.py
```

> FAILED tests/test_blocker_pill.py::test_an_issue_blocking_an_open_issue_gets_the_blocker_pill - AssertionError: 294.1: after the scheduled sync the pills are {10: None, 12: None, 14: None, 15: None, 16: None}; only open issues blocking an open issue show Blocker, and the rest follow their high or parked label
> FAILED tests/test_blocker_pill.py::test_the_scheduled_sync_writes_only_pills_that_change - AssertionError: 294.1: with only #22 wrong, the scheduled sync wrote [], not Blocker on #22 alone
> FAILED tests/test_blocker_pill.py::test_closing_the_last_blocked_issue_clears_the_pill - AssertionError: 294.2: after #31 closed the pills are {30: 'Blocker', 32: 'Blocker', 34: 'Blocker'}; #30 should lose Blocker, #32 keep it and #34 fall back to Parked
> FAILED tests/test_blocker_pill.py::test_a_closed_issue_loses_its_own_blocker_pill - AssertionError: 294.2: the closed issue #40 still shows Blocker
> FAILED tests/test_blocker_pill.py::test_reopening_an_issue_brings_the_pill_back - AssertionError: 294.2: after #51 reopened the pills are {50: None, 51: None}, not Blocker on both
> FAILED tests/test_blocker_pill.py::test_the_workflow_runs_on_close_and_reopen - AssertionError: 294.2: the board workflow's issue triggers are ['labeled', 'unlabeled', 'closed']; a close or reopen never reaches the pill
> FAILED tests/test_blocker_pill.py::test_a_link_added_or_removed_reaches_the_pill_on_the_next_scheduled_run - AssertionError: 294.3: after the link was added, #60 shows None, not Blocker
> FAILED test

**Agent:** I'm reviewing the plan: the 16 new tests fail today for the right reason. Next I'm checking that the faked GitHub matches the real Board's interface, then writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def \|class \|rest(\|PRIORITY" dokima/board.py | head -60; cat .github/workflows/board.yml | head -30; grep -n "dependencies" dokima/agent.py | head
```

> 17:PRIORITY = {"blocker": "Blocker", "high": "High", "parked": "Parked"}  # highest first
> 21:def linked(body):
> 25:def decide(event, p):
> 56:def priority(event, p):
> 58:    if event != "issues" or p["action"] not in ("labeled", "unlabeled") or p["label"]["name"] not in PRIORITY:
> 61:    return p["issue"]["number"], next((option for label, option in PRIORITY.items() if label in names), None)
> 64:def gql(query, **variables):
> 71:def api(method, path, **fields):
> 80:class Board:
> 81:    def __init__(self, spec, repo, q=gql, rest=api):
> 90:    def item(self, kind, number):
> 101:    def set(self, iid, field, option):
> 110:    def value(self, iid, field):
> 115:    def autopilot(self, kind, number):
> 121:    def open_pr(self, number):
> 126:    def parent(self, number):
> 131:    def label(self, kind, number, on):
> 135:            self.rest("POST", path, **{"labels[]": AUTOPILOT})
> 137:            self.rest("DELETE", f"{path}/{AUTOPILOT}")
> 139:    def views(self):
> 142:    def view_nodes(self):
> 147:    def set_view_filter(self, view_id, filter):
> 150:    def add_view(self, name, layout, filter):
> 151:        self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)
> 154:def action(board, kind, number, needs_you):
> 159:def switched(event, p):
> 166:def opened(event, p):
> 173:def switch(board, number):
> 199:def fix_view(board):
> 210:def sync(event, payload, spec, repo, q=gql, rest=api):
> 234:def main():
> name: board
> # Keeps the project board's Status and "Waitin

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner replanned after the owner's answers: four criteria and one fail-closed requirement, proved by 16 new tests and 7 changed ones, with no questions left."],
  "decided": ["A link changed by hand reaches the pill within 15 minutes, because the board workflow runs every 15 minutes and recomputes every open issue's pill.",
              "Dokima stops declaring the blocker label and the label no longer moves the pill; repos that already have it keep it, and it stops counting.",
              "When GitHub cannot list an issue's links, that issue's pill stays as it is and the run fails with exit code 1 naming the issue."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now follows both of your answers (a delay of up to 15 minutes, and no blocker label) and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Every new test fails today on the missing feature, each naming its criterion; of the changed old tests, the two that depend on the blocker label fail and the rest pass.",
   "evidence": "pytest -q tests/test_blocker_pill.py: 16 failed (e.g. '294.3: the board workflow has no schedule trigger'); pytest -q tests/test_board.py tests/test_manifest.py: 2 failed, 73 passed."},
  {"text": "The work changes .github/workflows/board.yml (adds a reopened trigger and a 15-minute schedule). Your answer allows the 15-minute runs, and a change to a workflow file stops for you at merge.",
   "evidence": ".github/workflows/board.yml:7 has types [labeled, unlabeled, closed] and no schedule; tests/test_blocker_pill.py::test_the_workflow_runs_every_15_minutes and ::test_the_workflow_runs_on_close_and_reopen require both."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "An open issue that blocks at least one other open issue shows the Blocker pill on the board, computed by code from its links.", "source": 
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan follows both your answers, a delay of up to 15 minutes and no blocker label, and every new test fails today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 294 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> 0

`9. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan follows both your answers, up to 15 minutes of delay and no blocker label, and every new test fails today as it should."
d["summary"]="The plan follows both your answers (15-minute delay, no blocker label), and every new test fails today because the feature is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 294 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for issue #294, and the review is saved at `/tmp/dokima-out/review.json`. Both hand-back checks pass on it.

**What changed since last round:** your two answers are now in the plan, and it has no questions left. Nothing else changed. The tests are the same commit the last review approved.
- **Delay:** a blocked-by link you add or remove by hand reaches the pill within 15 minutes, because the board workflow will run every 15 minutes and recompute every open issue's pill (criterion 294.3).
- **Label:** Dokima stops declaring the `blocker` label, and the label no longer moves the pill; only links do (294.4). Repos that already have the label keep it, since onboarding never deletes labels, but it stops counting.

**Your asks:** all five (three from the issue, two from your answers) map to a criterion. None is missing.

**Tests:** I ran them myself.
- All 16 new tests fail today because the feature is missing, not because of a crash. Each failure names its criterion.
- Of the 7 changed existing tests, the 2 that depend on the `blocker` label fail today; the other 5 pass.
- The fake GitHub calls the same blocked-by links API (GitHub's issue dependencies endpoints) that `dokima/agent.py` already uses.

**This will stop for you at merge:** the work changes `.github/workflows/board.yml`. It adds the 15-minute schedule and a trigger for when an issue reopens. Your answer allows the 15-minute runs, but a pull request that changes a workflow file still waits for your approval before it merges, even on autopilot.

There are no blockers, no earlier blockers to clear, and no issues to file from outside this one.
