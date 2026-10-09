# reviewer (plan) for #333

Run: https://github.com/dokima-dev/dokima/actions/runs/37993335619

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (42KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/ed46925e-e510-48a5-a7c9-7c8baf99cf9e/tool-results/bkq13qvb8.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct  9 21:25 .
> drwxrwxrwt 18 root   root    4096 Oct  9 21:25 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 21:25 in
> -rw-r--r--  1 runner runner 37661 Oct  9 21:25 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 21:25 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 21:25 parent.json
> -rw-r--r--  1 runner runner  4504 Oct  9 21:25 plan.json
> 
> in:
> total 44
> drwxr-xr-x 2 runner runner 4096 Oct  9 21:25 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 21:25 ..
> -rw-r--r-- 1 runner runner 4533 Oct  9 21:25 01-planner.json
> -rw-r--r-- 1 runner runner 4946 Oct  9 21:25 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5859 Oct  9 21:25 03-planner.json
> -rw-r--r-- 1 runner runner 3562 Oct  9 21:25 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5149 Oct  9 21:25 05-planner.json
> # Issue #333: A scan of the whole board and every card names anything that does not match its state
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 331, 332, 343, 344, 345, 346, 347 -->
> <!-- dokima-blocking: {"blocked_by": [331, 332, 344, 345, 346, 347], "blocks": [], "loop": []} -->
> One command scans the board and every issue and PR card, naming each one that does not match its state now.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/do

`2. Bash`
```
cd /tmp/pack; cat plan.json; cat parent.json; echo; cat open_blockers.json
```

> {
>  "kind": "user_story",
>  "summary": "One command scans the board and every issue and PR card, naming each one that does not match its state now.",
>  "user_story": "The owner runs one command that proves the board and every card are true, and it names each card that is not.",
>  "acceptance_criteria": [
>   {
>    "text": "`python3 -m dokima.scan` names every closed card outside Done or with a pill, every open card in the wrong column, and every stale card. An open card in no column is in the wrong column. Each line names the card and says what is wrong. A stale card is an issue or PR card that does not show the card Dokima writes when it redraws that issue now. It exits 1 when it names any; otherwise it prints `All N cards on the board match their state.` and exits 0.",
>    "source": "https://github.com/dokima-dev/dokima/issues/333"
>   },
>   {
>    "text": "The PR cards of #246 and #312 pass the scan only when they show Merged with every check passed. While either shows an old card or none, the scan names it and exits 1.",
>    "source": "https://github.com/dokima-dev/dokima/issues/333"
>   },
>   {
>    "text": "(manual) The scan of this repo's board finds nothing, and both PR cards show Merged with every check passed. The owner checks it once after this merges: runs `DOKIMA_BOARD=dokima-dev/N REPO=dokima-dev/dokima python3 -m dokima.scan`, sees `All N cards on the board match their state.`, and opens the PRs of #246 and #312. The automated part proves the scan checks exactly the board and rep

`3. Read`
```
/tmp/pack/issue.md
```

> 1	# Issue #333: A scan of the whole board and every card names anything that does not match its state
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-linked-from: 331, 332, 343, 344, 345, 346, 347 -->
> 5	<!-- dokima-blocking: {"blocked_by": [331, 332, 344, 345, 346, 347], "blocks": [], "loop": []} -->
> 6	One command scans the board and every issue and PR card, naming each one that does not match its state now.
> 7	
> 8	**Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 9	
> 10	[issue #333](https://github.com/dokima-dev/dokima/issues/333)
> 11	
> 12	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #331, #332, #344, #345, #346, #347
> 13	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #330, #135, #183, #343
> 14	
> 15	**User story:** The owner runs one scan that proves the board and the cards are true, and it names every card that is not.
> 16	
> 17	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 18	
> 19	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/doki

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('05-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); print(d.keys())"; cd /home/runner/work/dokima/dokima; git log --oneline -15 main; git diff --stat main..HEAD; git log --oneline main..HEAD
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37992896457",
>  "commit_before": "862eb31f92ab2a3fc69299647c707e3963a6dfb0",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 187340,
>   "turns": 34,
>   "cost_usd": 1.8363254000000002,
>   "tokens_in": 2916270,
>   "tokens_out": 17566
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/333/37992896457-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37992896457",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> 8b12495 AGENTS.md: every issue reference is a link plus a few plain words (#357)
> 5565fa5 Every 15 minutes, any card that does not match its issue's state is redrawn (#356)
> c16b878 One issue's card redraw never cancels another issue's (#352)
> 10d9114 Merging a PR redraws its card and its issue's card (#351)
> 75e92d3 A merged PR's card is written and says Merged with the true Definition of Done (#350)
> 28ccaf3 An approved plan waiting on a blocker stays in Plan; Work means it is being built (#348)
> b06c44b issue.md points to each record's file instead of repeating its JSON (#342)
> 09881bd The board's column and pills are always computed from the issue's state right now (#339)
> 0782805 Tests run in about a minute: skip slow tests for now, all cores at the merge gate, worker runs only its story's tests (#340)
> 0608e4e A spli

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git branch -a; git merge-base HEAD main; git log -1 --format=%cd main; git log -1 --format=%cd HEAD; git show --stat HEAD | head; python3 -c "
import json;d=json.load(open('/tmp/pack/in/05-planner.json'));print(json.dumps(d['handback'],indent=1)[:6000])"
```

> main
> * try/issue-333
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
>   remotes/origin/issue-116-board-sync
>   remotes/origin/issue-121-needs-you
>   remotes/origin/issue-126-keys-from-main
>   remotes/origin/issue-138-prompt
>   remotes/origin/issue-40-app
>   remotes/origin/issue-46-approve
>   remotes/origin/issue-54-plan
>   remotes/origin/issue-60-wrap
>   remotes/origin/issue-63-latest
>   remotes/origin/issue-67-label
>   remotes/origin/issue-74-layout
>   remotes/origin/issue-78-design
>   remotes/origin/issue-80-planner
>   remotes/origin/issue-81-build-on-main
>   remotes/origin/issue-89-planner-prompt
>   remotes/origin/issue-90-assign
>   remotes/origin/issue-93-terms
>   remotes/origin/logs
>   remotes/origin/main
>   remotes/origin/opus-everywhere
>   remotes/origin/owner-questions
>   remotes/origin/replan-base
>   remotes/origin/replan-own-changes
>   remotes/origin/reviewer-role
>   remotes/origin/river
>   remotes/origin/runtime-from-main
>   remotes/origin/split-filing
>   remotes/origin/try/issue-135
>   remotes/origin/try/issue-139
>   remotes/origin/try/issue-154
>   remotes/origin/try/issue-156
>   remotes/origin/try/issue-157
>   remotes/origin/try/issue-166
>   remotes/origin/try/issue-168
>   remotes/origin/try/issue-170
>   remotes/origin/try/issue-176
>   remotes/o

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt main 2>&1|tail -1; cp tests/test_scan.py /tmp/wt/tests/; cd /tmp/wt; timeout 300 python3 -m pytest -q tests/test_scan.py 2>&1 | tail -30; cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_scan.py 2>&1 | tail -5
```

> as on GitHub today: the scan must name both PRs and exit 1. Then both PR bodies get the card Dokima draws now: each
>         says Merged with All tests passed, and the scan says all 4 cards match and exits 0."""
>         record_property("proves", "333.2")
> >       need_scan("333.2")
> 
> tests/test_scan.py:652: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> 
> criterion = '333.2'
> 
>     def need_scan(criterion):
>         """Fail, naming the criterion, while dokima/scan.py does not exist."""
>         if scan is None:
> >           pytest.fail(f"{criterion}: there is no scan yet (dokima/scan.py is missing)")
> E           Failed: 333.2: there is no scan yet (dokima/scan.py is missing)
> 
> tests/test_scan.py:300: Failed
> =========================== short test summary info ============================
> FAILED tests/test_scan.py::test_the_scan_names_every_closed_card_outside_done_or_with_a_pill - Failed: 333.1: there is no scan yet (dokima/scan.py is missing)
> FAILED tests/test_scan.py::test_the_scan_names_every_open_card_in_the_wrong_column - Failed: 333.1: there is no scan yet (dokima/scan.py is missing)
> FAILED tests/test_scan.py::test_the_card_the_scan_expects_is_drawn_from_the_state_now - Failed: 333.1: there is no scan yet (dokima/scan.py is missing)
> FAILED tests/test_scan.py::test_the_scan_names_every_stale_issue_card_and_pr_card - Failed: 333.1: there is no scan yet (dokima/scan.py is missing)
> FAILED tests/test_scan.py::test_the_scan_of_a_true_board_exits_0_sayi

**Agent:** Reviewing the #333 plan: all 11 new tests fail today for the right reason (no scan yet), on the branch and on main. Next I'm reading the tests against main's current code.

`7. Bash`
```
cd /tmp/wt; sed -n 1,330p tests/test_scan.py
```

> """One scan names every card that does not match its issue's state now (#333).
> 
> Story 3 of #330. The owner's test of #330: after it ships, a scan of the whole board finds no closed card outside Done
> or with a pill, no open card in the wrong column, and the PR cards of #246 and #312 show Merged with every check passed.
> This scan is that test, made a command the owner can run any time:
> 
>     DOKIMA_BOARD=org/number REPO=owner/name python3 -m dokima.scan
> 
> It prints one line for each card that does not match its state, naming it ("issue #N" or "PR #N") and saying what is
> wrong, then exits 1; when every card matches, it prints `All N cards on the board match their state.` (N the number of
> issue and pull request cards it checked) and exits 0. It only reads: it never moves a card, sets a pill or edits a body.
> 
> How the tests run it. dokima.scan.main() is called in-process with DOKIMA_BOARD and REPO set; it returns the exit code
> (or raises SystemExit with it). GitHub is faked in one World:
> - dokima.board.Board is replaced by a fake whose cards() lists every issue and pull request card as
>   {kind, number, status, action, closed, autopilot}, as the real Board.cards() does on main (#339). Every write the
>   fake board offers (set, label, add_view, set_view_filter, and item() for something not on the board) is logged.
> - The `gh` helper of every dokima module that has one (dokima.agent, dokima.body, dokima.card, dokima.plan, and
>   dokima.scan if it defines its own) answers from the World: is

`8. Bash`
```
cd /tmp/wt; grep -n "^def \|^    def \|^DONE\|^class " dokima/board.py | head -60; grep -n "^def draw\|^def pr_body\|^def as_items\|changed_only\|^def render\|^def gather" dokima/card.py; grep -n "^def redraw\|^def save" dokima/body.py
```

> 18:DONE = ("Done", None)
> 21:def priority(event, p):
> 29:def gql(query, **variables):
> 36:def api(method, path, **fields):
> 45:class Board:
> 46:    def __init__(self, spec, repo, q=gql, rest=api):
> 55:    def item(self, kind, number):
> 66:    def set(self, iid, field, option):
> 75:    def value(self, iid, field):
> 80:    def labels(self, kind, number):
> 86:    def autopilot(self, kind, number):
> 90:    def dependencies(self, number, side):
> 101:    def blocking(self, number):
> 104:    def blocked_by(self, number):
> 107:    def open_issues(self):
> 117:    def open_pr(self, number):
> 122:    def parent(self, number):
> 127:    def label(self, kind, number, on):
> 135:    def state(self, kind, number):
> 140:    def cards(self):
> 160:    def views(self):
> 163:    def view_nodes(self):
> 168:    def set_view_filter(self, view_id, filter):
> 171:    def add_view(self, name, layout, filter):
> 175:def about(event, p):
> 187:def queue(event, p):
> 197:def reason(e):
> 201:def issue_of(repo, pr, head=None, body=None):
> 213:def where(repo, owners, n, on):
> 229:def rebuild(board, repo, owners, n, prs=()):
> 244:def put(board, kind, n, place):
> 251:def stopped(board, repo, n, column):
> 253:    def mark(kind, m):
> 265:def switch(board, number):
> 285:def fix_view(board):
> 296:def changed(repo):
> 307:def sweep(board, repo, owners, todo=None):
> 330:def label_priority(labels):
> 335:def blockers(event, p):
> 346:def recompute(board, touched):
> 353:    def refused(n, e):
> 379:def sync(event, payload, spec, repo, q=gql, rest=api):
> 390:    def at

`9. Bash`
```
cd /tmp/wt; sed -n 330,700p tests/test_scan.py; sed -n 140,160p dokima/board.py; sed -n 205,330p dokima/board.py
```

> def run(w, capsys):
>     """Run the scan once; (exit code, the lines it printed)."""
>     try:
>         code = scan.main()
>     except SystemExit as e:
>         code = e.code
>     out = capsys.readouterr()
>     lines = [x for x in (out.out + out.err).splitlines() if x.strip()]
>     return (0 if code is None else code), lines
> 
> 
> def named(lines, kind, n):
>     """The lines naming this card: "issue #N" or "PR #N" as a whole word."""
>     label = r"\bissue #" if kind == "issue" else r"\b(?:PR|pull request) #"
>     return [x for x in lines if re.search(label + str(n) + r"\b", x, re.I)]
> 
> 
> OLD_CARD = "<!-- dokima-card -->\n**Review**\n\nAn old card drawn before the state changed.\n<!-- /dokima-card -->"
> 
> 
> # 333.1: the scan names every closed card outside Done or with a pill
> 
> def test_the_scan_names_every_closed_card_outside_done_or_with_a_pill(world, capsys, record_property):
>     """The scan names every closed card outside Done or with a pill, and fails.
> 
>     Proves 333.1.
>     Closed #57 sits in Review; closed #58 sits in Done with Autopilot; merged PR #64 (for closed #65) sits in Done with
>     Needs you; closed PR #66 (for closed #67) sits in Work. Closed #59, #65 and #67 sit in Done with no pill, the way
>     they should. Every card's body is the card Dokima draws now. The scan must name #57 with Review, #58 with Autopilot,
>     PR #64 with Needs you and PR #66 with Work, name none of #59, #65 and #67, and exit 1."""
>     record_property("proves", "333.1")
>     need_scan("333.1")
>     w = world
>  

`10. Bash`
```
cd /tmp/wt; sed -n 425,470p dokima/board.py; sed -n 740,790p dokima/card.py; grep -n "^def shows\|^def issue_pr" -A8 dokima/card.py
```

> def main(argv=()):
>     if list(argv[1:2]) == ["queue"]:
>         with open(os.environ["GITHUB_OUTPUT"], "a") as f:
>             f.write(f"group={queue(os.environ['GITHUB_EVENT_NAME'], json.load(open(os.environ['GITHUB_EVENT_PATH'])))}\n")
>         return 0
>     spec = os.environ.get("DOKIMA_BOARD", "").strip()
>     if not spec:
>         print("No DOKIMA_BOARD set; nothing to sync.")
>         return 0
>     try:
>         placed = sync(os.environ["GITHUB_EVENT_NAME"], json.load(open(os.environ["GITHUB_EVENT_PATH"])), spec, os.environ["GITHUB_REPOSITORY"])
>     except RuntimeError as e:
>         print(f"::error::{e}")
>         return 1
>     for change in placed:
>         print("board:", *change)
>     return 0
> 
> 
> if __name__ == "__main__":
>     sys.exit(main(sys.argv))
>     cache = {}
>     before, now = draw(repo, number, pr_number, cache=cache)
>     if follow(repo, number, before, now, cache):
>         sys.exit(1)
> 
> 
> def draw(repo, number, pr_number, plans=None, noted=None, cache=None, changed_only=False):
>     """Write the card at the top of the issue and its PR.
> 
>     Returns the blocking links and loop its card showed before and shows now. With `changed_only`, a card that
>     already shows what it would be drawn as is not rewritten.
>     `plans` gives the links of a plan approved just now, by issue (see their_links). `noted` adds (True) or removes
>     (False) issues from the index of those whose approved plans link here. The Blocked by and Blocks lines are
>     GitHub's own blocked-by links, read now; 

`11. Bash`
```
cd /tmp/wt; sed -n 379,424p dokima/board.py
```

> def sync(event, payload, spec, repo, q=gql, rest=api):
>     """Put the cards an event is about where their state says, and keep Priority."""
>     if not spec:
>         return []
>     pill, touched = priority(event, payload), blockers(event, payload)
>     on_off = event == "issues" and payload["action"] in ("labeled", "unlabeled") and payload["label"]["name"] == AUTOPILOT \
>         and payload["issue"]["number"]
>     merged = event in ("pull_request", "pull_request_target") and payload["action"] == "closed" and payload["pull_request"].get("merged")
>     board, owners = Board(spec, repo, q, rest), plan.repo_approvers(repo.split("/")[0])
>     placed, failed = [], []
> 
>     def attempt(step):
>         try:
>             return step()
>         except RuntimeError as e:
>             failed.append(str(e))
> 
>     if event == "schedule":
>         attempt(lambda: sweep(board, repo, owners, changed(repo)))
>     for kind, n, head, body in about(event, payload):
>         issue = n if kind == "issue" else attempt(lambda: issue_of(repo, n, head, body))
>         if issue and kind == "pr" and payload.get("action") in ("opened", "reopened") and "pull_request" in payload \
>                 and board.autopilot("issue", issue) and not board.autopilot("pr", n):
>             # A pull request built for an issue on autopilot carries the label too, so the Autopilot view lists it.
>             board.label("pr", n, True)
>         if issue:
>             placed += attempt(lambda: rebuild(board, repo, owners, issue, [n] if kind == 

`12. Bash`
```
mkdir -p /tmp/proto && cat > /tmp/wt/dokima/scan.py <<'EOF'
import os, subprocess, sys
from dokima import agent, board, body, card, plan


def card_now(repo, kind, n):
    if kind == "pr":
        issue_n = board.issue_of(repo, n)
        pr_number = n
    else:
        issue_n, pr_number = n, card.issue_pr(repo, n)
    issue = plan.fetch_issue(repo, issue_n)
    found = card.gather(repo, issue_n, pr_number)
    found["sources"] = sorted(set(card.linked_from(issue["current_body"])))
    cache = {}
    now = card.github_links(repo, int(issue_n), cache)
    found["blocking"] = now
    if now.get("unread"):
        found["unread"] = card.reason(card.blocking(repo, int(issue_n), cache))
    found["linked"] = {"relates_to": card.their_links(repo, issue_n, found["sources"], None)["relates_to"],
                       "blocked_by": now.get("blocked_by") or [], "blocks": now.get("blocks") or []}
    return card.render(repo, issue, found)


def main():
    spec, repo = os.environ["DOKIMA_BOARD"], os.environ["REPO"]
    b = board.Board(spec, repo)
    owners = plan.repo_approvers(repo.split("/")[0])
    cards, bad = b.cards(), []
    for c in cards:
        kind, n = c["kind"], c["number"]
        name = f"issue #{n}" if kind == "issue" else f"PR #{n}"
        try:
            if c["closed"]:
                want = board.DONE
            else:
                issue_n = n if kind == "issue" else board.issue_of(repo, n)
                want = board.where(repo, owners, issue_n, c["autopilot"])
            got = (c["status"], c["action"])
            if c["closed"] and got != want:
                bad.append(f"{name} is closed but shows {got[0]} {got[1] or ''}")
            elif not c["closed"] and got[0] != want[0]:
                bad.append(f"{name} sits in {got[0]} but belongs in {want[0]}")
            top = card_now(repo, kind, n)
            if kind == "issue":
                cur = plan.fetch_issue(repo, n)["current_body"] or ""
                ok = card.shows(cur, top)
 
```

> ...........                                                              [100%]
> 11 passed in 0.09s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** A throwaway scan built on current main passes all 11 tests. Now I'm checking that the tests catch a scan with parts missing.

`13. Bash`
```
cd /tmp/wt; cp dokima/scan.py /tmp/proto/scan.py
mut(){ cp /tmp/proto/scan.py dokima/scan.py; python3 - "$1" "$2" <<'EOF'
import sys;p='dokima/scan.py';s=open(p).read();a,b=sys.argv[1],sys.argv[2];assert a in s,a;open(p,'w').write(s.replace(a,b,1))
EOF
echo "== $3: $(timeout 120 python3 -m pytest -q tests/test_scan.py 2>&1 | tail -1)"; }
mut 'if not ok:' 'if False:' nostale
mut 'got != want' 'got[0] != want[0]' noclosedpill
mut 'elif not c["closed"] and got[0] != want[0]:' 'elif False:' noopencol
mut 'if bad:
        return 1' 'if False:
        return 1' exit0
mut 'ok = card.pr_body(top, cur) == cur' 'ok = True' noprstale
mut 'ok = card.shows(cur, top)' 'ok = "dokima-card" in cur' weakissuestale
mut 'got[0] != want[0]:
                bad' 'got[0] != want[0] and got[0] is not None:
                bad' skipnone
mut 'bad.append(f"{name} could not be read: {getattr(e, '"'stderr'"', '"''"') or e}")' 'pass' swallowunread
mut 'b = board.Board(spec, repo)' 'b = board.Board("o/1", repo)' fixedboard
cp /tmp/proto/scan.py dokima/scan.py
```

> == nostale: 2 failed, 9 passed in 0.13s
> == noclosedpill: 1 failed, 10 passed in 0.12s
> == noopencol: 3 failed, 8 passed in 0.14s
> == exit0: 7 failed, 4 passed in 0.22s
> == noprstale: 2 failed, 9 passed in 0.13s
> == weakissuestale: 1 failed, 10 passed in 0.12s
> == skipnone: 1 failed, 10 passed in 0.12s
> == swallowunread: 1 failed, 10 passed in 0.11s
> == fixedboard: 1 failed, 10 passed in 0.11s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`14. Bash`
```
cd /tmp/wt; grep -n "open or closed" AGENTS.md; rm dokima/scan.py tests/test_scan.py; git status --short; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt; git status --short; ls /tmp/dokima-out 2>&1
```

> 100:Every agent run posts one comment, written by code: one plain sentence on top saying what the run did, the short version the owner needs (the plan, its questions or the split; the worker's own words on what it changed, linking its pull request, or why it stopped; the criteria a review blocks on and its proposed issues), the long parts in folds drawn by the same code as the issue card, the full JSON record in the last fold, and a footnote with the model, time, turns, tokens, API-equivalent cost and a one-click link to the run's whole conversation. Those comments are the permanent records; only comments the bot posted count as records. The card on top of the issue is drawn from them (planned). Its Blocked by and Blocks lines are GitHub's own blocked-by links, read each time the card is drawn, so a link a person adds or removes by hand shows on both issues' cards with no comment; when GitHub cannot list them, the card says GitHub's reason. GitHub announces no event for such a link, so card.yml redraws on every change or comment a person makes on an issue, along with the card of every issue it is linked to whose links changed, and every 15 minutes rewrites the cards whose links changed, and every issue card and PR card that does not show its issue's state now, open or closed, looking only at the issues and pull requests updated since the last 15-minute sweep that succeeded started (an update to either redraws both); when GitHub cannot list earlier sweeps, or none has succeede

`15. Bash`
```
cd /home/runner/work/dokima/dokima; git show main:AGENTS.md | grep -n "sweeps each\|board run sweeps\|Done with no pill\|closed issue or a merged" ; grep -n "open or closed" AGENTS.md | cut -c1-200
```

> 87:- Columns are stages: Backlog, Plan, Work, Review, Done. Every new item lands in Backlog. Each card's column and pill are computed from its issue's state on GitHub now, never from the event that started the board run: every event about an issue or its pull request and the end of every run that did not fail put both cards there, so the next event fixes a dropped or late one, and an issue and its pull requests share one board queue that keeps the newest recompute. An open issue with no record is in Backlog. Otherwise it is in the column of the newest stage started since its newest record, else where the river placed it after that record, but never ahead in a stage not started yet: an approved plan stays in Plan until its worker starts, also while it waits on a blocker, and a built one stays in Work until its code review starts. A worker starts with a code owner's `/work`, the bot's Autopilot line that starts it, or its run card; a code review starts once the bot puts up its run card, even queued, or its record; the same words from anyone else start nothing. An open pull request goes with its issue. A closed issue, and a merged or closed pull request, sits in Done with no pill, whatever its labels. Every 15 minutes a sweep rechecks the issues and pull requests updated since the last sweep that succeeded, each with its pull request or issue, and every card when GitHub cannot say what changed. A card whose state GitHub cannot give keeps its column and pill, and the run fails na

`16. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Replanned against main as it is now: the board change is dropped from scope, since main's board already lists each card's column, and the scan reuses main's column rules and card drawing unchanged.",
   "Rewrote tests/test_scan.py so the expected column follows main's board rules and the expected card is the one main's card code writes on a redraw; all 11 tests fail today because dokima/scan.py does not exist."
  ],
  "decided": [
   "The scan only reads, and a card GitHub will not give is named with GitHub's reason and fails the scan.",
   "An open card's pill, its Priority, items missing from the board and drafts are left out; the live scan of this repo stays the owner's manual check."
  ],
  "open": [
   "The planner flagged a conflict between AGENTS.md and the board code on pills for closed cards."
  ]
 },
 "verdict": "approve",
 "summary": "The replanned scan matches main as it is now: every promise has a test that fails today only because the scan is missing, and the tests catch a scan with any check left out.",
 "blockers": [],
 "notes": [
  {
   "text": "The planner's one concern is out of date. Main's AGENTS.md already says a closed card sits in Done with no pill whatever its labels, and that Autopilot goes only on open items, so no AGENTS.md fix is needed. The planner quoted the older AGENTS.md on this branch, which main has since changed.",
   "evidence": "git show main:AGENTS.md, The board: 'A closed issue, and a merged or closed pull request, sits in Done with no pill, whatever its labels' and 'Autopilot on every other open item on autopilot'; the branch's AGENTS.md still says 'open or closed'."
  },
  {
   "text": "The tests were checked on main, not only on this branch, which still sits on an older main (0608e4e). With tests/test_scan.py copied onto main, all 11 fail with 'there is no scan yet'. A throwaway scan built only from main's board.where, 
```

> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`17. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The replanned scan matches main now: every promise has a test that fails only because the scan is missing, and catches any check left out."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 333 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the replanned #333 plan. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

You asked for the plan to be checked against main as it is now, so I ran the tests on a copy of main, not only on this branch, which still sits on an older main (`0608e4e`).

- **Fails today for the right reason:** all 11 tests in `tests/test_scan.py` fail with "there is no scan yet (dokima/scan.py is missing)", on both main and the branch.
- **Can be built:** I wrote a throwaway scan in that copy of main using only code main already has: its board rules and card drawing, with no changes to either. It passed all 11 tests, so the plan is right to take `dokima/board.py` out of scope.
- **Catches a scan that cuts corners:** I made versions of that scan with one check removed each. Every one failed at least one test. The removed checks were:
  - spotting out-of-date issue cards and PR cards
  - pills on closed cards
  - columns of open cards, including open cards with no column
  - the exit code
  - cards GitHub won't give
  - which board you named

All six things you asked for in the issue map to a criterion. Nothing is missing, and the plan asks you no questions.

The review has three notes, none of them blockers:
1. **The planner's one concern is out of date.** It says AGENTS.md disagrees with the code on pills for closed cards. Main's AGENTS.md already says a closed card sits in Done with no pill and that Autopilot goes only on open items. The planner was reading the older copy on this branch, so AGENTS.md needs no fix.
2. **The test check above** is recorded in the review.
3. **AGENTS.md is in scope, but no criterion asks for a change there.** The worker should keep any edit to one line on how to run the scan, or leave the file alone.

I removed the copy of main and the throwaway scan, and the repo has no changes.
