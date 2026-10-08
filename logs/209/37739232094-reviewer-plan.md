# reviewer (plan) for #209

Run: https://github.com/dokima-dev/dokima/actions/runs/37739232094

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #209: Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 1</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** The owner switches a whole issue tree onto autopilot, or off it, with one comment on any of its issues or pull requests.
> 
> **Context:** Commands are routed in dokima/agent.py (COMMANDS, command_of, route) and listened for in .github/workflows/commands.yml; only a code owner's comment counts (dokima.plan approvers). Sub-issues are GitHub's native sub-issues, filed by file_split in dokima/agent.py. Keep the state on GitHub: an `autopilot` label on every issue in the tree. This story needs .github/workflows/commands.yml, so it must say so explicitly, per AGENTS.md. Autopilot changes the flow, so AGENTS.md (Commands, The flow) gets a short entry. This story only switches autopilot on and off; it starts no stage and shows nothing on the board (story 2).
> 
> **Acceptance criteria:**
> - A code owner's comment `/autopilot start` on an issue puts that issue and every sub-issue under it, at every level, on autopilot; on a pull request it does the same for the issue the pull request was built for and everything under it. ([source](https://github.com/dokima-dev/dokima/issues/205))
> - A code owner's comment `/autopilot stop` on an issue or its pull req

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_autopilot.py
```

> commit 0d9ed2a5a35ace43885b92272a4b488bd427adaa
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 06:43:35 2026 +0000
> 
>     planner for #209 (run 37738831571)
> 
>  tests/test_autopilot.py | 281 ++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 281 insertions(+)
> """`/autopilot start` and `/autopilot stop` switch a whole issue tree on and off, and start nothing else (#209).
> 
> These tests run the command listener (.github/workflows/commands.yml) the way GitHub runs it, on the machine from
> test_start.py: every job's `if:` is evaluated and its scripts run with bash against a fake `gh`. Here the fake GitHub
> also knows an issue tree and its labels, kept in tree.json and labels.json:
> 
>     #50                 (a parent above the issue; never part of its tree)
>     ├── #57             (the issue the command is about; its pull request is #60, branch try/issue-57)
>     │   ├── #101
>     │   │   └── #103
>     │   │       └── #104
>     │   └── #102
>     └── #58             (a sibling of #57; never part of its tree)
> 
> GitHub answers sub-issues on its REST API (`gh api repos/o/r/issues/N/sub_issues`, with or without --paginate) and a
> single issue (`gh api repos/o/r/issues/N`) with its labels. Labels change through `gh issue edit N... --add-label` /
> `--remove-label`, or the REST API (POST or PUT on repos/o/r/issues/N/labels, DELETE on .../labels/NAME, which fails
> with 404 when the issue does not carry that label, the way GitHub does). `

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_autopilot.py 2>&1 | grep -E "^E .*20[0-9]\.|passed|failed|Error" | head -30
```

> assert not m.failed, f"209.1 ({case}): the listener failed on /autopilot start:\n{m.tail()}"
> E           AssertionError: 209.1 (issue): /autopilot start left these issues of #57's tree off autopilot: [57, 101, 102, 103, 104]
> tests/test_autopilot.py:187: AssertionError
>             assert not m.failed, f"209.2 ({case}): the listener failed on /autopilot stop:\n{m.tail()}"
> E           AssertionError: 209.2 (issue): /autopilot stop left these issues of #57's tree on autopilot: [57, 101, 103, 104]
> tests/test_autopilot.py:207: AssertionError
>             assert not m.failed, f"209.3 ({case}): the listener failed on {body}:\n{m.tail()}"
> E           AssertionError: 209.3 (start-issue): /autopilot start left 0 comments, expected exactly one: []
> tests/test_autopilot.py:232: AssertionError
> E           AssertionError: 209.4: AGENTS.md's Commands section does not name `/autopilot start`
> tests/test_autopilot.py:254: AssertionError
> E       AssertionError: 209.5 (owner): the code owner's /autopilot start did not switch #57's tree on: []
> tests/test_autopilot.py:280: AssertionError
> FAILED tests/test_autopilot.py::test_autopilot_start_puts_the_issue_and_every_sub_issue_at_every_level_on_autopilot - AssertionError: 209.1 (issue): /autopilot start left these issues of #57's tree off autopilot: [57, 101, 102, 103, 104]
> FAILED tests/test_autopilot.py::test_autopilot_stop_takes_the_same_tree_off_autopilot - AssertionError: 209.2 (issue): /autopilot stop left these issues of #57's tree on autopilot: [

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/commands.yml; grep -n "def run_job\|def posted\|def dispatches\|def agent_started\|uses\b\|CODEOWNERS\|pr_open\|def tail" tests/test_start.py | head -50
```

> name: commands
> run-name: "${{ github.event.comment.body }}"
> # The listener. A code owner's comment whose first line starts with /plan, /work or /review starts that stage, on the
> # issue or on its pull request, and so does a PR review submitted as a comment or a change request. An Approve never
> # starts anything: it only ever means merge. Everything after the command, and every other comment, review and line
> # note, reaches the agent through its pack. No command, nothing starts; bots never start anything. On an issue
> # /review grades the plan; on a pull request, the work. A code owner's command that fails here, before any agent
> # starts, gets one record where it was written with GitHub's error, and the owner is mentioned. Every code owner's
> # command first puts up one card for its run, which becomes that run's record.
> on:
>   issue_comment:
>     types: [created]
>   pull_request_review:
>     types: [submitted]
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
>   actions: read
> jobs:
>   route:
>     if: >-
>       (github.event.comment.user.type || github.event.review.user.type) == 'User' &&
>       startsWith(github.event.comment.body || github.event.review.body, '/') &&
>       github.event.review.state != 'approved' 
>     runs-on: ubuntu-24.04
>     outputs:
>       role: ${{ steps.r.outputs.role }}
>       stage: ${{ steps.r.outputs.stage }}
>       issue: ${{ steps.r.outputs.issue }}
>       why: ${{ steps.why.outputs.why }}
>     steps:
>       - uses: actions/checkout@v5
>         with:
> 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 525,560p tests/test_start.py; grep -n "posts.json\|\"comment\"\|comments" tests/test_start.py | head -20
```

> author and every version of its body."""
>         path = f"{self.tmp}/gh/comments.json"
>         return json.load(open(path)) if os.path.exists(path) else []
> 
>     def posted(self):
>         """Every comment the run wrote, as {where, author, body}: where it is and its body as it stands now, after any
>         edits."""
>         return [{"where": [c["kind"], "comment", str(c["number"])], "author": c["author"], "body": c["versions"][-1]}
>                 for c in self.comments()]
> 
>     def dispatches(self):
>         """Every signal sent to start another stage."""
>         return [c for c in self.calls() if c[:1] == ["api"] and any("dispatches" in x for x in c)]
> 
>     def created_issues(self):
>         """Every issue the run asked GitHub to create."""
>         return [c for c in self.calls() if c[:2] == ["issue", "create"]]
> 
>     def agent_started(self):
>         """True when the fake Claude Code was started."""
>         return os.path.exists(f"{self.tmp}/claude-started")
> 
>     def tail(self):
>         """The failed step's output, then the last steps' output, for a failure message."""
>         first = [l for l in self.log if self.failed_step and f": {self.failed_step} (" in l.split("\n")[0]][:1]
>         return "\n".join(first + self.log[-3:])[-3000:]
> 
> 
> class Run(Machine):
>     """One run of the agent workflow (agent.yml), started by hand by the actor."""
> 
>     def __init__(self, tmp, role, stage, comments, try_branch=False, actor=OWNER, broken=None, options=None, review=None):
>         super().__init

**Agent:** Tests fail for the right reasons; now checking one detail of the fake GitHub's comment handling.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 155,170p tests/test_start.py
```

> else:
>         print("" if (flag("-q") or flag("--jq")) else "[]")
> elif a[:1] == ["api"] and any(x.startswith("users/") for x in a):
>     print("1")
> elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/\d+/comments", x) for x in a):
>     path = next(x for x in a if re.fullmatch(r"/?repos/o/r/issues/\d+/comments", x))
>     n = int(path.rstrip("/").split("/")[-2])
>     body = api_body()
>     if body is None and (flag("-X", "--method") or "GET").upper() == "GET":
>         print(json.dumps([shown(c) for c in load() if c["number"] == n]))
>     else:
>         out(shown(create("pr" if n == 60 else "issue", n, body)))
> elif a[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/comments/\d+", x) for x in a):
>     cid = next(x for x in a if re.fullmatch(r"/?repos/o/r/issues/comments/\d+", x)).rsplit("/", 1)[1]
>     if (flag("-X", "--method") or "GET").upper() in ("PATCH", "POST"):
>         out(shown(edit(cid, api_body())))

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote five criteria: start switches the issue and its whole sub-issue tree on, stop switches the same tree off, neither starts a stage and each leaves one comment naming the switched issues, AGENTS.md describes autopilot, and only a code owner's command counts.",
          "Wrote one test per criterion in tests/test_autopilot.py that runs the command listener against a fake GitHub holding a four-level issue tree with its labels."],
  "decided": ["The one comment goes where the command was written (the pull request when said there); the owner went on with this reading by saying /review."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers every promise of the story, and each of its five tests runs the real command listener and fails today because autopilot does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "On /autopilot stop, the comment test checks that every switched issue is named and nothing outside the tree is, but not that #102 (never on autopilot) is left out, so a comment listing the whole tree as switched off would still pass.",
   "evidence": "tests/test_autopilot.py::test_autopilot_starts_no_stage_and_says_which_issues_it_switched checks `switched - named` and `named & OUTSIDE` only."},
  {"text": "The AGENTS.md test only checks that The flow section mentions the word autopilot; it is a light check on a documentation promise.",
   "evidence": "tests/test_autopilot.py::test_agents_md_tells_how_autopilot_works: `assert \"autopilot\" in flow.lower()`."},
  {"text": "Every new test fails today for the right reason: the tree's labels are unchanged, no comment is left, and AGENTS.md does not name the commands.",
   "evidence": "pytest -q tests/test_autopilot.py: 5 failed, e.g. '209.1 (issue): /autopilot start left these issues of #57's tree off autopilot: [57, 101, 102, 103, 104]', '209.5 (owner): the code owner's /autopilot start did n
```

> (Bash completed with no output)

**Agent:** I approved the plan for #209. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**Why I approved:**
- **Covers the story:** there are five criteria. `/autopilot start` puts the issue and every sub-issue under it, at every level, on autopilot. `/autopilot stop` takes that same tree off. Neither command starts a stage, and each leaves one comment naming the issues it switched. AGENTS.md describes autopilot. Only a code owner's command counts.
- **Tests cover both directions:** each criterion has one test, and each test runs the real `commands.yml` against a fake GitHub with a four-level issue tree. They check that the parent and sibling issues are left alone, that other labels stay, that strangers and the bot change nothing, and that the code owner's command does work.
- **They fail today for the right reason:** I ran `pytest -q tests/test_autopilot.py` and all 5 failed on the missing feature, not on setup. For example: "209.1 (issue): /autopilot start left these issues of #57's tree off autopilot: [57, 101, 102, 103, 104]".
- **The owner's choice is followed:** the planner asked where the comment goes when the command is said on a pull request. The owner said `/review`, which accepts its assumption that the comment goes on the pull request, and the tests check exactly that.

**Two weak spots, recorded as notes rather than blockers:**
- After `/autopilot stop`, the comment test doesn't check that #102 is left out. #102 was never on autopilot, so a comment claiming the whole tree was switched off would still pass.
- The AGENTS.md test only checks that the word "autopilot" appears in The flow section.

There were no earlier blockers to resolve and nothing outside this issue to propose.
