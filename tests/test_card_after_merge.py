"""A PR's card shows its true state after merge, however fast the owner merges (#322).

On #246 the owner merged twelve seconds after the tests finished; the card run that followed could no longer find the
PR (GitHub's event names no PR once it is merged, and GitHub lists only open PRs for a squash-merged commit), so the
PR card kept saying All tests was running. These tests read the real `.github/workflows/card.yml`: they work out, for
one GitHub event, whether the card job runs, its concurrency group and the env its "Write the card" step gets, the way
GitHub would, then run the real `dokima/card.py` main() with that env against a fake GitHub.

The fake GitHub (FakeGitHub below) answers `gh` the way GitHub does for these reads:
    gh api repos/o/r/commits/SHA/pulls          open PRs whose head is SHA, plus the merged PR of a commit on main
    gh api repos/o/r/pulls?head=o:BRANCH&state=open|closed|all   (any order of query parameters)
    gh api repos/o/r/pulls?state=...            every PR in that state
    gh api repos/o/r/pulls/N                    one PR
    gh api search/issues?q=...SHA...            the PRs whose head is SHA, open or merged
    gh api graphql ... -F p=N                   the issue PR N closes (closingIssuesReferences)
    gh api -X PATCH repos/o/r/pulls/N -F body=@FILE   writes the PR's description
Anything else fails as a refused call would, and is logged in `refused`. What the card draws from (records, checks,
reviews) is faked at card.gather, so these tests prove which issue and PR get drawn and what the drawn card says.
"""
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import body, card, plan  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
WORKFLOW = os.path.join(ROOT, ".github/workflows/card.yml")
REPO = "o/r"
OWNER = "owner"


# ---------------------------------------------------------------- card.yml, read the way GitHub reads it

def workflow():
    with open(WORKFLOW) as f:
        return f.read()


def top_block(text, key):
    """The lines under top-level `key:` in card.yml, or None when it has none."""
    m = re.search(rf"^{re.escape(key)}:[^\n]*\n((?:[ \t]+[^\n]*\n|[ \t]*\n)*)", text, re.M)
    return m.group(1) if m else None


def triggers():
    """The `on:` block of card.yml."""
    return top_block(workflow(), "on") or ""


def trigger_types(name):
    """The event types card.yml lists for trigger `name`; None without that trigger.

    [] when the trigger lists no types."""
    on = triggers()
    m = re.search(rf"^(\s+){re.escape(name)}:[^\n]*\n((?:\1[ \t]+[^\n]*\n)*)", on, re.M)
    if not m:
        return None
    types = re.search(r"types:\s*\[([^\]]*)\]", m.group(2))
    return [t.strip().strip("'\"") for t in types.group(1).split(",")] if types else []


def lookup(ctx, path):
    """The value at a dotted path like github.event.workflow_run.pull_requests[0].number; None when missing."""
    cur = ctx
    for part in re.findall(r"[A-Za-z_][A-Za-z0-9_-]*|\[\d+\]", path):
        if part.startswith("["):
            i = int(part[1:-1])
            cur = cur[i] if isinstance(cur, list) and i < len(cur) else None
        else:
            cur = cur.get(part) if isinstance(cur, dict) else None
    return cur


PATH = re.compile(r"\b(?:github|inputs|vars|secrets|steps|env|needs)(?:\.[A-Za-z_][A-Za-z0-9_-]*|\[\d+\])+")


def evaluate(expr, ctx):
    """The value of one GitHub expression, worked out the way GitHub does.

    Handles paths, '' strings, ==, !=, !, &&, ||, true/false/null and the common functions."""
    parts = re.split(r"('(?:[^']|'')*')", expr)
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            out.append(repr(p[1:-1].replace("''", "'")))
            continue
        p = PATH.sub(lambda m: f"_L({m.group(0)!r})", p)
        p = p.replace("&&", " and ").replace("||", " or ")
        p = re.sub(r"!(?!=)", " not ", p)
        out.append(p)

    def text(v):
        return "" if v is None else str(v).lower() if isinstance(v, bool) else str(v)

    names = {"_L": lambda path: lookup(ctx, path), "true": True, "false": False, "null": None,
             "format": lambda s, *a: re.sub(r"\{(\d+)\}", lambda m: text(a[int(m.group(1))]), s),
             "contains": lambda a, b: (b in a) if isinstance(a, list) else text(b).lower() in text(a).lower(),
             "startsWith": lambda a, b: text(a).lower().startswith(text(b).lower()),
             "endsWith": lambda a, b: text(a).lower().endswith(text(b).lower()),
             "toJSON": lambda v: __import__("json").dumps(v), "join": lambda a, s=",": s.join(map(text, a or []))}
    return eval("".join(out), {"__builtins__": {}}, names)


def render_value(value, ctx):
    """A workflow value with every ${{ }} rendered as GitHub renders it.

    A null renders as an empty string."""
    def one(m):
        v = evaluate(m.group(1), ctx)
        return "" if v is None else str(v).lower() if isinstance(v, bool) else str(v)
    return re.sub(r"\$\{\{(.*?)\}\}", one, value).strip().strip("'\"")


def job_runs(ctx):
    """Whether the card job's `if:` lets this event through."""
    m = re.search(r"^\s+if:\s*(.+)$", workflow(), re.M)
    if not m:
        return True
    expr = m.group(1).strip()
    inner = re.fullmatch(r"\$\{\{(.*)\}\}", expr)
    return bool(evaluate(inner.group(1) if inner else expr, ctx))


def group(ctx):
    """The card run's concurrency group for this event, and its cancel-in-progress.

    cancel-in-progress says whether a newer run cancels one already going."""
    block = top_block(workflow(), "concurrency") or ""
    m = re.search(r"^\s+group:\s*(.+)$", block, re.M)
    cancel = re.search(r"^\s+cancel-in-progress:\s*(\S+)", block, re.M)
    return (render_value(m.group(1), ctx) if m else None), (cancel.group(1) if cancel else "false")


def step_env(ctx):
    """The env the "Write the card" step gets for this event, as GitHub renders it."""
    text = workflow()
    m = re.search(r"- name: Write the card\n((?:[ \t]+[^\n]*\n?)*)", text)
    assert m, "card.yml has no 'Write the card' step"
    env = re.search(r"^(\s+)env:\n((?:\1[ \t]+[^\n]*\n?)*)", m.group(1), re.M)
    out = {}
    for line in (env.group(2) if env else "").splitlines():
        kv = re.match(r"\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if kv:
            out[kv.group(1)] = render_value(kv.group(2), ctx)
    return out


# ---------------------------------------------------------------- the events

def event(name, action=None, sender="User", **payload):
    ev = dict(payload, action=action, sender={"type": sender, "login": "dokima-runtime[bot]" if sender == "Bot" else OWNER},
              repository={"default_branch": "main", "full_name": REPO})
    inputs = payload.get("inputs") or {}
    return {"github": {"event_name": name, "event": ev, "repository": REPO, "ref": "refs/heads/main",
                       "sha": "m0", "run_id": "777"},
            "inputs": inputs, "vars": {"DOKIMA_APP_ID": "1"}, "secrets": {}, "steps": {"app": {"outputs": {"token": "t"}}}}


def merged_pr(pr, sender="Bot"):
    """GitHub's event when PR `pr` merges: pull_request_target (or pull_request), closed, merged."""
    payload = {"number": pr["number"], "pull_request": dict(pr), "repository": {"full_name": REPO}}
    return event("pull_request_target", "closed", sender, **payload)


def check_finished(head_sha, head_branch, pull_requests, title="full suite"):
    """GitHub's workflow_run event when a check workflow finishes on `head_sha`."""
    return event("workflow_run", "completed", "Bot",
                 workflow_run={"head_sha": head_sha, "head_branch": head_branch, "pull_requests": pull_requests,
                               "display_title": title, "name": "full suite", "id": 99, "event": "pull_request_target"})


def issue_edited(number):
    return event("issues", "edited", "User", issue={"number": number})


def run_by_hand(number):
    """GitHub's event when the owner presses Run workflow on card.yml with issue `number`."""
    ctx = event("workflow_dispatch", None, "User", inputs={"issue": str(number)})
    ctx["inputs"] = {"issue": str(number)}
    return ctx


# ---------------------------------------------------------------- a fake GitHub

def pr(number, issue, state="open", merged=False, sha=None, merge_commit=None):
    return {"number": number, "state": state, "merged": merged, "merged_at": "2026-10-08T21:36:54Z" if merged else None,
            "merged_by": {"login": OWNER} if merged else None, "body": f"Closes #{issue}",
            "html_url": f"https://github.com/{REPO}/pull/{number}", "merge_commit_sha": merge_commit,
            "head": {"ref": f"try/issue-{issue}", "sha": sha or f"head{number}"}, "base": {"ref": "main"}}


class FakeGitHub:
    """GitHub with a few PRs, answering `gh` as described at the top of this file."""

    def __init__(self, prs, closes):
        self.prs, self.closes = prs, closes
        self.refused, self.pr_bodies = [], {}

    def refuse(self, args):
        self.refused.append(args)
        raise subprocess.CalledProcessError(1, ["gh", *args], "", "gh: Not Found (HTTP 404)")

    def __call__(self, *args, **kw):
        import json
        args = [str(a) for a in args]
        if args[:1] != ["api"]:
            return self.refuse(args)
        rest = args[1:]
        method = "GET"
        if "-X" in rest:
            method = rest[rest.index("-X") + 1]
        path = next((a for a in rest if a.startswith("repos/") or a.startswith("search/") or a == "graphql"), None)
        if path == "graphql":
            p = next((a.split("=", 1)[1] for a in rest if a.startswith("p=")), None)
            issue = self.closes.get(int(p)) if p else None
            nodes = [{"number": issue}] if issue else []
            return json.dumps({"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": nodes}}}}})
        if path is None:
            return self.refuse(args)
        base, _, query = path.partition("?")
        q = dict(urllib.parse.parse_qsl(query))
        m = re.fullmatch(rf"repos/{REPO}/pulls/(\d+)", base)
        if m and method == "PATCH":
            f = next(a for a in rest if a.startswith("body="))[5:]
            if f.startswith("@"):
                with open(f[1:]) as fh:
                    f = fh.read()
            self.pr_bodies[int(m.group(1))] = f
            return "{}"
        if method != "GET":
            return self.refuse(args)
        if m:
            found = [p for p in self.prs if p["number"] == int(m.group(1))]
            return json.dumps(found[0]) if found else self.refuse(args)
        m = re.fullmatch(rf"repos/{REPO}/commits/(\w+)/pulls", base)
        if m:
            sha = m.group(1)
            # GitHub lists the merged PR that brought a commit into main, and otherwise only open PRs.
            return json.dumps([p for p in self.prs if (p["state"] == "open" and p["head"]["sha"] == sha)
                               or (p["merged"] and p["merge_commit_sha"] == sha)])
        if base == f"repos/{REPO}/pulls":
            state = q.get("state", "open")
            found = [p for p in self.prs if state == "all" or p["state"] == state]
            if "head" in q:
                found = [p for p in found if f"o:{p['head']['ref']}" == q["head"]]
            return json.dumps(found)
        if base == "search/issues":
            items = [{"number": p["number"], "state": p["state"], "pull_request": {"merged_at": p["merged_at"]}}
                     for p in self.prs if p["head"]["sha"] in q.get("q", "")]
            return json.dumps({"total_count": len(items), "items": items})
        return self.refuse(args)


MERGED = pr(5, 40, state="closed", merged=True, sha="abc", merge_commit="m1")
OPEN = pr(6, 41, sha="def")


def world(monkeypatch, tmp_path, prs=(MERGED, OPEN)):
    """Fake GitHub for card.py, recording every card it draws and writes.

    Returns the fake, the (issue, PR) pairs drawn, and the issue cards saved by number."""
    gh = FakeGitHub(list(prs), {5: 40, 6: 41, 7: 246})
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(card, "gh", gh)
    monkeypatch.setattr(plan, "gh", gh, raising=False)
    drawn, saved = [], {}

    def gather(repo, number, pr_number):
        drawn.append((number, int(pr_number) if pr_number else None))
        the_pr = next((p for p in gh.prs if pr_number and p["number"] == int(pr_number)), None)
        return found_for(number, the_pr)

    monkeypatch.setattr(card, "gather", gather)
    monkeypatch.setattr(card, "their_links", lambda *a, **k: {})
    monkeypatch.setattr(plan, "fetch_issue", lambda repo, n: {
        "number": n, "url": f"https://github.com/{REPO}/issues/{n}", "title": f"issue {n}",
        "current_body": f"{body.MARKER}\n\nThe owner's ask."})

    def save(repo, number, current, top):
        saved[number] = top
        return True

    monkeypatch.setattr(body, "save", save)
    return gh, drawn, saved


def check(name, n):
    return {"name": name, "status": "completed", "conclusion": "success",
            "html_url": f"https://github.com/{REPO}/actions/runs/2/job/{n}"}


def found_for(number, the_pr):
    """What GitHub holds for an issue whose PR merged with everything passed.

    An approved plan, a build, an approving code review, every check green on the PR's head, and a code owner's
    merge."""
    src = f"https://github.com/{REPO}/issues/{number}"
    h = {"kind": "user_story", "summary": "A card.", "user_story": "Owners see a card.",
         "acceptance_criteria": [{"text": "first thing works", "source": src}], "non_functional": [],
         "scope": ["x.py"], "out_of_scope": [], "tests": {f"{number}.1": ["tests/test_a.py::test_one"]}}
    run = f"https://github.com/{REPO}/actions/runs/"
    recs = [{"role": "planner", "stage": None, "handback": h, "check": {"passed": True}, "run": run + "8"},
            {"role": "reviewer", "stage": "plan", "handback": {"verdict": "approve"}, "check": {"passed": True}, "run": run + "9"},
            {"role": "worker", "stage": None, "handback": {}, "check": {"passed": True}, "run": run + "10"},
            {"role": "reviewer", "stage": "pr", "handback": {"verdict": "approve"}, "check": {"passed": True}, "run": run + "11"}]
    checks = [check(f"{number}.1 · first thing works", 1), check(card.ALL_TESTS, 3)] if the_pr else []
    return {"recs": recs, "pr": the_pr, "check_runs": checks, "reviews": [], "owners": {OWNER}, "tests": {},
            "worker": {"status": "completed", "conclusion": "success", "html_url": run + "10"}, "children": []}


def run_card(monkeypatch, ctx):
    """Run the real card.py main() with the env card.yml gives its step for this event."""
    for k in ("ISSUE_NUMBER", "PR_NUMBER", "HEAD_SHA", "RUN_TITLE", "HEAD_BRANCH"):
        monkeypatch.delenv(k, raising=False)
    env = step_env(ctx)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(sys, "argv", ["card.py"])
    card.main()
    return env


def shows_merged_and_done(text):
    """True when a card shows Merged and its whole Definition of Done passed."""
    passed = card.icon(REPO, "passed", alt="passed")
    row = next((l for l in text.splitlines() if l.startswith("**Definition of Done:**")), "")
    return (f"{card.field_icon(REPO, 'merged')} **Merged**" in text and row.count(passed) == 3
            and "not started" not in row and "running" not in row)


# ---------------------------------------------------------------- the tests

def test_a_check_finishing_after_the_merge_still_writes_the_pr_card(record_property, monkeypatch, tmp_path):
    """A check finishing after the merge still writes the merged PR's card and its issue's.

    Proves 322.1.

    Replays #246: the full suite finishes on the PR's head after a squash merge, so GitHub's event names no PR and
    GitHub lists no open PR for that commit. The card run must still draw issue #40 with its merged PR #5 and write the
    PR's description. An open PR's check still draws its own PR, and a commit with no PR draws nothing."""
    record_property("proves", "322.1")
    gh, drawn, saved = world(monkeypatch, tmp_path)
    assert job_runs(check_finished("abc", "try/issue-40", [])), "322.1: the card job is skipped when a check finishes"
    run_card(monkeypatch, check_finished("abc", "try/issue-40", []))
    assert drawn == [(40, 5)], (f"322.1: a check finishing after PR #5 merged drew {drawn or 'nothing'}, "
                                "not issue #40 with its merged PR #5")
    assert 5 in gh.pr_bodies, "322.1: the merged PR #5's card was not written"
    assert shows_merged_and_done(gh.pr_bodies[5]), "322.1: the merged PR's card does not show Merged with every check passed"
    assert 40 in saved, "322.1: the issue's card was not written"

    drawn.clear()
    gh.pr_bodies.clear()
    run_card(monkeypatch, check_finished("def", "try/issue-41", [{"number": 6, "head": {"sha": "def"}}]))
    assert drawn == [(41, 6)], f"322.1: a check on open PR #6 drew {drawn or 'nothing'}, not issue #41 with PR #6"

    drawn.clear()
    gh.pr_bodies.clear()
    run_card(monkeypatch, check_finished("zzz", "main", []))
    assert drawn == [], f"322.1: a check on a commit with no PR drew {drawn}; it should draw nothing"
    assert not gh.pr_bodies, "322.1: a check on a commit with no PR wrote a PR's card"


def test_merging_a_pr_redraws_its_card_and_its_issues_card(record_property, monkeypatch, tmp_path):
    """Merging a PR redraws its card and its issue's as Merged and Done.

    Proves 322.2.

    Sends card.yml GitHub's event for PR #5 merging (by autopilot's bot, then by the owner), checks the card job runs
    for it, then runs card.py with the env card.yml gives: the PR's description and the issue's card both show Merged,
    with All tests, Code review and Owner approval passed."""
    record_property("proves", "322.2")
    types = trigger_types("pull_request_target")
    assert types is not None and "closed" in types, \
        f"322.2: card.yml does not start on a PR closing (pull_request_target types: {types})"
    for sender in ("Bot", "User"):
        gh, drawn, saved = world(monkeypatch, tmp_path)
        ctx = merged_pr(MERGED, sender)
        assert job_runs(ctx), f"322.2: the card job is skipped when a PR is merged by a {sender}"
        run_card(monkeypatch, ctx)
        assert drawn == [(40, 5)], f"322.2: merging PR #5 drew {drawn or 'nothing'}, not issue #40 with PR #5"
        assert 5 in gh.pr_bodies, "322.2: merging PR #5 did not write its card"
        assert shows_merged_and_done(gh.pr_bodies[5]), "322.2: the PR card after merge does not show Merged and Done"
        assert 40 in saved and shows_merged_and_done(saved[40]), \
            "322.2: the issue card after merge does not show Merged and Done"


def test_the_merges_card_run_always_has_the_last_word(record_property, monkeypatch, tmp_path):
    """The merge's card run waits for its PR's earlier runs, and no other issue's drops it.

    Proves 322.3.

    Works out card.yml's concurrency group for four events: the merge of PR #5, a check finishing late on PR #5's
    branch, a check on another issue's PR and an edit of another issue. The merge and the late check share a group,
    so they run one after the other and never overlap; the other two are in other groups, so they can never replace
    the merge's waiting run; and a newer run never cancels one already going."""
    record_property("proves", "322.3")
    merge, _ = group(merged_pr(MERGED))
    late, _ = group(check_finished("abc", "try/issue-40", []))
    other_check, _ = group(check_finished("def", "try/issue-41", [{"number": 6}]))
    other_issue, cancel = group(issue_edited(9))
    assert merge and merge == late, (f"322.3: the merge's card run (group {merge!r}) and a late check's on the same PR "
                                     f"(group {late!r}) can overlap, so an older drawing can land after the merge")
    assert other_check != merge and other_issue != merge, \
        f"322.3: card runs for other issues share the merge's group {merge!r}, so they can drop its waiting run"
    assert cancel.lower() == "false", "322.3: a newer card run cancels one already going"


def test_a_card_run_by_hand_redraws_one_issue_and_its_merged_pr(record_property, monkeypatch, tmp_path):
    """Run workflow redraws one issue and its merged PR, for #246 and #312.

    Proves 322.4.

    Presses Run workflow on card.yml with issue 40, whose PR #5 is merged, and checks the run draws issue #40 with PR #5
    as Merged and Done. This is how #246 and #312 are redrawn once this ships."""
    record_property("proves", "322.4")
    assert trigger_types("workflow_dispatch") is not None, "322.4: card.yml cannot be run by hand (no workflow_dispatch)"
    assert re.search(r"^\s+issue:", triggers(), re.M), "322.4: running card.yml by hand takes no issue number"
    gh, drawn, saved = world(monkeypatch, tmp_path)
    ctx = run_by_hand(40)
    assert job_runs(ctx), "322.4: the card job is skipped when run by hand"
    run_card(monkeypatch, ctx)
    assert drawn == [(40, 5)], f"322.4: running the card by hand for #40 drew {drawn or 'nothing'}, not #40 with PR #5"
    assert 5 in gh.pr_bodies and shows_merged_and_done(gh.pr_bodies[5]), \
        "322.4: the hand run did not write PR #5's card as Merged and Done"
    assert 40 in saved and shows_merged_and_done(saved[40]), "322.4: the hand run did not write issue #40's card"


def test_the_merges_card_run_uses_mains_code(record_property):
    """The card run a merge starts uses main's card code, never the PR's.

    Proves 322.5.

    Reads card.yml: a PR event reaches it only as pull_request_target (which runs main's copy), never as pull_request,
    and its checkout names no PR ref or sha."""
    record_property("proves", "322.5")
    assert trigger_types("pull_request_target") is not None, "322.5: card.yml has no pull_request_target trigger"
    assert trigger_types("pull_request") is None, \
        "322.5: card.yml starts on pull_request, which runs the PR's own copy of the card"
    text = workflow()
    refs = re.findall(r"^\s+ref:\s*(.+)$", text, re.M)
    assert not [r for r in refs if "pull_request" in r or "head" in r], \
        f"322.5: card.yml checks out the PR's code ({refs}), so the work could change how it is reported"
