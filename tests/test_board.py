"""Tests for the project board: stage moves from GitHub events, the refresh button, and the Needs you pill.

The board is never real here: either a fake GraphQL function or a fake `gh` on PATH stands in for GitHub."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import board  # noqa: E402

WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "board.yml")
BOT, YOU = {"type": "Bot"}, {"type": "User"}


def pr(action, number=7, body="Closes #5", merged=False):
    return {"action": action, "pull_request": {"number": number, "body": body, "merged": merged}}


# 116.1: every stage moment sets the stage and whose turn it is

def test_issue_stage_moments(record_property):
    record_property("proves", "116.1")
    issue = {"number": 5}
    assert board.decide("issues", {"action": "labeled", "label": {"name": "plan"}, "issue": issue}) == [("issue", 5, "Plan", False)]
    assert board.decide("issues", {"action": "labeled", "label": {"name": "work"}, "issue": issue}) == [("issue", 5, "Work", False)]
    assert board.decide("issues", {"action": "closed", "issue": issue}) == [("issue", 5, "Done", False)]
    assert board.decide("issues", {"action": "labeled", "label": {"name": "bug"}, "issue": issue}) == []


def test_plan_ready_question_or_rejection_is_your_turn(record_property):
    record_property("proves", "116.1")
    for body in ("Plan written above, tests on `work/issue-5`.", "**Planner question**\n\nWhich?", "**Plan rejected:** no tests"):
        assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": body}}) == [("issue", 5, "Plan", True)]
    assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": YOU, "body": "Plan written above"}}) == [], "116.1: a person's comment moved the board"


def test_pr_moments(record_property):
    record_property("proves", "116.1")
    assert board.decide("pull_request", pr("opened")) == [("pr", 7, "Review", False), ("issue", 5, "Review", False)]
    run = {"action": "completed", "workflow_run": {"pull_requests": [{"number": 7}]}}
    assert board.decide("workflow_run", run) == [("pr", 7, "Review", True)]
    review = {"action": "submitted", "review": {"state": "changes_requested"}, "pull_request": {"number": 7, "body": "Closes #5"}}
    assert board.decide("pull_request_review", review) == [("pr", 7, "Work", False), ("issue", 5, "Work", False)]
    assert board.decide("pull_request", pr("closed", merged=True)) == [("pr", 7, "Done", False), ("issue", 5, "Done", False)]
    assert board.decide("pull_request", pr("closed", merged=False)) == [("pr", 7, "Done", False)], "116.1: an unmerged close finished the issue"


# 116.2: PR and issue move together; new items land on top

class FakeGitHub:
    def __init__(self, on_board=False):
        self.calls, self.on_board = [], on_board

    def __call__(self, query, **v):
        self.calls.append((query.split("(")[0].split("{")[0].strip(), v))
        if "organization" in query:
            return {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
                {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Plan", "Work", "Review", "Done")]},
                {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": "Needs you"}]}]}}}}
        if query.startswith("query") and "repository" in query:
            kind = "issue" if "issue(" in query else "pullRequest"
            items = [{"id": "ITEM", "project": {"id": "P"}}] if self.on_board else []
            return {"repository": {kind: {"id": "C", "projectItems": {"nodes": items}}}}
        if "addProjectV2ItemById" in query:
            return {"addProjectV2ItemById": {"item": {"id": "NEW"}}}
        return {}


def test_pr_and_issue_move_together(record_property):
    record_property("proves", "116.2")
    gh = FakeGitHub(on_board=True)
    changed = board.sync("pull_request", pr("opened"), "dokima-dev/1", "dokima-dev/dokima", q=gh)
    assert [(k, n) for k, n, *_ in changed] == [("pr", 7), ("issue", 5)]
    sets = [v for name, v in gh.calls if name == "mutation" and "o" in v]
    assert {s["o"] for s in sets} == {"s-Review"}, f"116.2: got {sets}"
    clears = [v for name, v in gh.calls if name == "mutation" and v.get("f") == "W" and "o" not in v]
    assert len(clears) == 2, "116.2: Action was not cleared on both items while Dokima works"


def test_new_item_is_added_at_the_top(record_property):
    record_property("proves", "116.2")
    gh = FakeGitHub(on_board=False)
    board.sync("issues", {"action": "labeled", "label": {"name": "work"}, "issue": {"number": 5}}, "dokima-dev/1", "dokima-dev/dokima", q=gh)
    positions = [v for _, v in gh.calls if v.get("i") == "NEW" and set(v) == {"p", "i"}]
    assert positions, "116.2: new item was not placed"
    assert all("a" not in v for v in positions), "116.2: new item was placed after another item, not on top"


# 116.3: without a board, nothing happens and nothing fails

def test_no_board_means_no_calls(record_property):
    record_property("proves", "116.3")
    def explode(*a, **k):
        raise AssertionError("116.3: GitHub was called without a board")
    assert board.sync("issues", {"action": "closed", "issue": {"number": 5}}, "", "o/r", q=explode) == []


def test_workflow_skips_without_the_board_setting(record_property):
    record_property("proves", "116.3")
    assert "if: vars.DOKIMA_BOARD != ''" in open(WORKFLOW).read()


def test_lanes_are_needs_you_or_nothing(record_property):
    """Items that need the owner get Action = "Needs you"; everything else has no Action."""
    record_property("proves", "130.1")
    gh = FakeGitHub(on_board=True)
    board.sync("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": "**Planner question**"}}, "dokima-dev/1", "o/r", q=gh)
    assert any(v.get("o") == "w-you" for _, v in gh.calls), "130.1: a question for the owner did not land in Needs you"


# 135: the board's own button puts every card back where its records say, and every board update
# recomputes each card's Needs you from its latest record.
#
# These tests run Dokima the way the workflows do (`python3 -m dokima.board`, `python3 -m dokima.agent board|split`)
# with a fake `gh` first on PATH. The fake keeps a whole small repo and board in one JSON file: issues, pull requests,
# their comments (the records), and the board's items with their Status and Action. It answers the gh calls Dokima
# makes today (issue view, pr list, pr view, api, and GraphQL for the board) and saves every board change, so a test
# reads the board as it stands afterwards, whatever order the code wrote it in.

import json as _json
import subprocess as _subprocess
import tempfile as _tempfile

from dokima import agent  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
BUTTON = "https://github.com/o/r/actions/workflows/board.yml"

FAKE_GH = r'''
import json, re, sys
STATE = __STATE__
s = json.load(open(STATE))
args = sys.argv[1:]
s.setdefault("calls", []).append(args)

def save():
    json.dump(s, open(STATE, "w"))

def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default

def out(v):
    save()
    print(v if isinstance(v, str) else json.dumps(v))
    sys.exit(0)

def fail(why):
    save()
    sys.stderr.write("fake gh: " + why + "\n")
    sys.exit(1)

if args[:2] == ["api", "graphql"]:
    q, v = "", {}
    for i, a in enumerate(args):
        if a in ("-f", "-F", "--raw-field", "--field"):
            k, _, val = args[i + 1].partition("=")
            if k == "query":
                q = val
            else:
                v[k] = int(val) if a in ("-F", "--field") and val.lstrip("-").isdigit() else val
    b = s["board"]
    fields = {"Status": ("S", ["Backlog", "Plan", "Work", "Review", "Done"]), "Action": ("W", ["Needs you"])}
    by_fid = {fid: name for name, (fid, _) in fields.items()}
    opt_name = {f"{fid}-{o}": o for _, (fid, opts) in fields.items() for o in opts}
    def content(it):
        if it["kind"] == "issue":
            i = s["issues"][str(it["number"])]
            return {"__typename": "Issue", "id": f"C-issue-{it['number']}", "number": it["number"], "state": i["state"],
                    "title": i["title"], "url": f"https://github.com/o/r/issues/{it['number']}",
                    "repository": {"nameWithOwner": "o/r"}, "labels": {"nodes": []},
                    "closedByPullRequestsReferences": {"nodes": []}}
        p = s["prs"][str(it["number"])]
        return {"__typename": "PullRequest", "id": f"C-pr-{it['number']}", "number": it["number"], "state": p["state"],
                "merged": p["state"] == "MERGED", "closed": p["state"] != "OPEN", "headRefName": p["head"], "body": p["body"],
                "title": p.get("title", ""), "url": f"https://github.com/o/r/pull/{it['number']}", "repository": {"nameWithOwner": "o/r"}}
    def item(it):
        values = [{"name": it[f], "optionId": f"{fields[f][0]}-{it[f]}", "field": {"id": fields[f][0], "name": f}}
                  for f in fields if it.get(f)]
        return {"id": it["id"], "type": "ISSUE" if it["kind"] == "issue" else "PULL_REQUEST", "isArchived": False,
                "content": content(it), "fieldValues": {"nodes": values}}
    def project():
        p = {"id": "P", "title": "Board", "number": 1, "url": "https://github.com/orgs/o/projects/1",
             "shortDescription": b["description"], "readme": b.get("readme", ""),
             "fields": {"nodes": [{"id": fid, "name": name, "options": [{"id": f"{fid}-{o}", "name": o} for o in opts]}
                                  for name, (fid, opts) in fields.items()]}}
        if "items(" in q:
            # Two items a page, so code that reads only the first page misses cards.
            start = int(v.get("after") or 0) if str(v.get("after") or "0").isdigit() else 0
            page = b["items"][start:start + 2]
            more = start + 2 < len(b["items"])
            p["items"] = {"totalCount": len(b["items"]), "nodes": [item(it) for it in page],
                          "pageInfo": {"hasNextPage": more, "endCursor": str(start + 2) if more else None}}
        return p
    if q.lstrip().startswith("mutation"):
        if "updateProjectV2ItemFieldValue" in q:
            it = next(x for x in b["items"] if x["id"] == v["i"])
            it[by_fid[v["f"]]] = opt_name[v["o"]]
            out({"data": {"updateProjectV2ItemFieldValue": {"projectV2Item": {"id": v["i"]}}}})
        if "clearProjectV2ItemFieldValue" in q:
            it = next(x for x in b["items"] if x["id"] == v["i"])
            it[by_fid[v["f"]]] = None
            out({"data": {"clearProjectV2ItemFieldValue": {"projectV2Item": {"id": v["i"]}}}})
        if "addProjectV2ItemById" in q:
            kind, n = v["c"].split("-")[1:]
            new = {"id": f"ITEM-{kind}-{n}", "kind": kind, "number": int(n), "Status": None, "Action": None}
            b["items"].insert(0, new)
            out({"data": {"addProjectV2ItemById": {"item": {"id": new["id"]}}}})
        if "updateProjectV2ItemPosition" in q:
            out({"data": {"updateProjectV2ItemPosition": {"clientMutationId": None}}})
        if "updateProjectV2(" in q or "updateProjectV2 (" in q:
            if "shortDescription" in q:
                texts = [x for k, x in v.items() if isinstance(x, str) and x != "P"]
                m = re.search(r'shortDescription\s*:\s*"((?:[^"\\]|\\.)*)"', q)
                b["description"] = texts[0] if texts else json.loads('"' + m.group(1) + '"')
            if "readme" in q:
                b["readme"] = b.get("readme", "")
            out({"data": {"updateProjectV2": {"projectV2": {"id": "P"}}}})
        fail("unknown mutation: " + q[:80])
    if "organization" in q:
        out({"data": {"organization": {"projectV2": project()}}})
    if "node(" in q:
        out({"data": {"node": project()}})
    if "repository" in q:
        kind = "issue" if re.search(r"\bissue\(", q) else "pullRequest"
        n = v["n"]
        on = [{"id": x["id"], "project": {"id": "P"}} for x in b["items"] if x["kind"] == ("issue" if kind == "issue" else "pr") and x["number"] == n]
        out({"data": {"repository": {kind: {"id": f"C-{'issue' if kind == 'issue' else 'pr'}-{n}", "projectItems": {"nodes": on}}}}})
    fail("unknown query: " + q[:80])

if args[:2] == ["issue", "view"]:
    i = s["issues"].get(args[2])
    if i is None:
        fail("no issue " + args[2])
    out({"number": int(args[2]), "title": i["title"], "body": i.get("body", ""), "state": i["state"], "comments": i["comments"]})
if args[:2] == ["pr", "list"]:
    head, state = opt("--head"), (opt("--state") or "open").upper()
    found = [{"number": int(n), "headRefName": p["head"], "state": p["state"]} for n, p in sorted(s["prs"].items(), key=lambda x: int(x[0]))
             if (head is None or p["head"] == head) and (state == "ALL" or p["state"] == state)]
    jq = opt("-q") or opt("--jq")
    if jq:
        out(str(found[0]["number"]) if found and jq.strip() == ".[0].number" else "")
    out([{"number": f["number"]} for f in found])
if args[:2] == ["pr", "view"]:
    p = s["prs"][args[2]]
    out({"number": int(args[2]), "state": p["state"], "headRefName": p["head"], "body": p["body"],
         "comments": p["comments"], "reviews": p.get("reviews", [])})
if args[:1] == ["api"] and re.match(r"repos/o/r/pulls/\d+/comments", args[1]):
    out([])
fail("unsupported: " + " ".join(args))
'''


def record(role, stage="", handback=None, passed=True, attempt=None):
    """A record exactly as the workflow builds and posts one, rendered into the comment text the bot posts."""
    if role == "not-started":
        return agent.not_started(attempt, stage, "A step failed.", {"run_id": "1", "run": "https://x/run/1"})
    if role == "split":
        return {"role": "split", "stage": None, "handback": {"stories": [{"story": 1, "issue": 98, "title": "a", "id": "N1", "blocked_by": []},
                                                                         {"story": 2, "issue": 99, "title": "b", "id": "N2", "blocked_by": [1]}]},
                "check": {"passed": True, "problems": []}, "run": "https://x/run/1"}
    out = _tempfile.mkdtemp()
    _json.dump(handback or {}, open(os.path.join(out, agent.HANDBACK[role]), "w"))
    return agent.build_record(role, stage, out, "", passed, {"run_id": "1", "run": "https://x/run/1"})


def said(rec, minute, who="dokima-runtime"):
    """A comment carrying a record, as GitHub returns it, posted at that minute of the day."""
    return {"author": {"login": who}, "body": agent.render(rec), "createdAt": f"2026-10-08T10:{minute:02d}:00Z"}


REVIEW = {"previous_step": {"did": [], "decided": [], "open": []}, "round": 1, "summary": "s", "notes": [],
          "outside_plan": [], "resolved": []}
BLOCK = {"id": "B1", "criterion": "9.1", "test": None, "problem": "p", "evidence": "e", "fix": "f"}
PLAN = {"kind": "user_story", "user_story": "s"}
ASKS = {**PLAN, "questions": [{"question": "Which one?", "assumption": "The first."}]}
FEATURE = {"kind": "feature", "feature": "f", "stories": [{"title": "a"}, {"title": "b"}]}


def repo_and_board():
    """A small repo whose board is scrambled: every card sits in the wrong column with the wrong Needs you pill.

    Returns (state, expected): expected maps each card to the (column, pill) its real state and latest record give."""
    issues, prs, expect = {}, {}, {}
    def issue(n, comments=(), state="OPEN"):
        issues[str(n)] = {"title": f"Issue {n}", "body": "", "state": state, "comments": list(comments)}
    def pr(n, head, state="OPEN", comments=(), body=""):
        prs[str(n)] = {"head": head, "state": state, "body": body, "comments": list(comments), "reviews": []}
    issue(1, [said(record("planner", handback=ASKS), 1)], state="CLOSED"); expect[("issue", 1)] = ("Done", None)
    issue(2); expect[("issue", 2)] = ("Backlog", None)
    issue(3, [said(record("planner", handback=ASKS), 1)]); expect[("issue", 3)] = ("Plan", "Needs you")
    issue(4, [said(record("planner", handback=ASKS), 1), said(record("planner", handback=PLAN), 2)])
    expect[("issue", 4)] = ("Plan", None)
    issue(5, [said(record("planner", handback=PLAN), 1)])
    pr(50, "try/issue-5", comments=[said(record("worker", handback={"summary": "s"}), 3)])
    expect[("issue", 5)] = expect[("pr", 50)] = ("Review", None)
    issue(6, [said(record("planner", handback=PLAN), 1)])
    pr(60, "try/issue-6", comments=[said(record("reviewer", "pr", {**REVIEW, "stage": "pr", "verdict": "block",
                                                                  "blockers": [{**BLOCK, "fixer": "worker"}]}), 4)])
    expect[("issue", 6)] = expect[("pr", 60)] = ("Work", None)
    issue(10, [said(record("planner", handback=FEATURE), 1),
               said(record("reviewer", "plan", {**REVIEW, "stage": "plan", "verdict": "approve", "blockers": []}), 2),
               said(record("split"), 3)])
    expect[("issue", 10)] = ("Work", None)
    issue(11, [said(record("planner", handback=PLAN), 1), said(record("not-started", attempt="worker"), 2)])
    expect[("issue", 11)] = ("Work", "Needs you")
    issue(12, [said(record("worker", handback={"summary": "s"}), 3)], state="CLOSED")
    pr(120, "try/issue-12", state="MERGED"); expect[("issue", 12)] = expect[("pr", 120)] = ("Done", None)
    pr(130, "feature-x"); expect[("pr", 130)] = ("Review", None)
    wrong = {"Backlog": ("Done", "Needs you"), "Plan": ("Work", "Needs you"), "Work": ("Backlog", "Needs you"),
             "Review": ("Plan", "Needs you"), "Done": ("Review", "Needs you")}
    items = []
    for (kind, n), (col, pill) in expect.items():
        status, _ = wrong[col]
        items.append({"id": f"ITEM-{kind}-{n}", "kind": kind, "number": n, "Status": status,
                      "Action": None if pill else "Needs you"})
    state = {"issues": issues, "prs": prs, "board": {"description": "Our team board.", "items": items}}
    return state, expect


def run(tmp_path, state, args, event="workflow_dispatch", payload=None, extra=None):
    """Run Dokima as the workflow does, with the fake gh first on PATH; returns (process, board state afterwards)."""
    bin_dir, path = tmp_path / "bin", tmp_path / "state.json"
    bin_dir.mkdir(exist_ok=True)
    path.write_text(_json.dumps(state))
    gh = bin_dir / "gh"
    gh.write_text(f"#!{sys.executable} -S\n" + FAKE_GH.replace("__STATE__", repr(str(path))))
    gh.chmod(0o755)
    (tmp_path / "event.json").write_text(_json.dumps(payload or {}))
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GITHUB_", "DOKIMA_"))}
    env.update({"PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}", "DOKIMA_BOARD": "o/1", "GITHUB_REPOSITORY": "o/r",
                "GITHUB_REPOSITORY_OWNER": "o", "GITHUB_EVENT_NAME": event, "GITHUB_EVENT_PATH": str(tmp_path / "event.json"),
                "GITHUB_SERVER_URL": "https://github.com", "GITHUB_RUN_ID": "1", "OWNERS": "owner", "GH_TOKEN": "x",
                "PYTHONPATH": ROOT, **(extra or {})})
    p = _subprocess.run([sys.executable, *args], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
    return p, _json.loads(path.read_text())


def cards(state):
    """The board as it stands: {(kind, number): (column, pill)}."""
    return {(it["kind"], it["number"]): (it.get("Status"), it.get("Action")) for it in state["board"]["items"]}


def differences(after, expect, crit):
    """Every card whose column or pill is not what its real state says, in plain words."""
    return [f"{crit}: {k} #{n} is in {after.get((k, n), ('not on the board',))[0]} with pill {after.get((k, n), (None, None))[1]!r}, "
            f"its real state says {col} with pill {pill!r}" for (k, n), (col, pill) in expect.items() if after.get((k, n)) != (col, pill)]


def test_the_button_puts_every_card_back_where_its_real_state_says(record_property, tmp_path):
    """Pressing "Run workflow" on the board workflow puts every card in the column its real state says.

    Scrambles a board of eleven cards over six pages, then runs `python3 -m dokima.board` as the button does. Closed or
    merged is Done; an issue with no record is Backlog; an issue with records goes where the river put it after its
    latest record (a question stops in Plan, a plan going to review is Plan, finished work is Review, blocked work is
    Work, a filed split is Work, a run that never started stops in Work); a pull request goes with its issue, and one
    built for no issue is Review."""
    record_property("proves", "135.1")
    state, expect = repo_and_board()
    p, after = run(tmp_path, state, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.1: the button's run failed: {p.stderr[-2000:]}"
    wrong = [d for d in differences(cards(after), expect, "135.1")]
    assert not wrong, "\n".join(wrong)


def test_the_board_workflow_has_the_button(record_property):
    """The board workflow can be started by hand, so GitHub shows its "Run workflow" button, and the board setting still guards it."""
    record_property("proves", "135.1")
    wf = open(WORKFLOW).read()
    on = wf[wf.index("\non:"):wf.index("\npermissions:")]
    assert re.search(r"(?m)^  workflow_dispatch:", on), "135.1: the board workflow has no workflow_dispatch trigger, so there is no button"
    assert "if: vars.DOKIMA_BOARD != ''" in wf, "135.1: the button would run without a board"
    assert "python3 -m dokima.board" in wf, "135.1: the button does not run the board code"


def stale_board():
    """A board where #4 carries a stale Needs you (its plan went on to review) and #3 lacks one (it asks the owner)."""
    state, expect = repo_and_board()
    for it in state["board"]["items"]:
        col, pill = expect[(it["kind"], it["number"])]
        it["Status"], it["Action"] = col, pill
    for it in state["board"]["items"]:
        if (it["kind"], it["number"]) == ("issue", 4):
            it["Action"] = "Needs you"
        if (it["kind"], it["number"]) == ("issue", 3):
            it["Action"] = None
        if (it["kind"], it["number"]) == ("issue", 1):
            it["Action"] = "Needs you"
    return state, expect


def pills(after, expect):
    """Every card whose Needs you pill disagrees with its latest record."""
    return [f"{k} #{n}: pill {after.get((k, n), (None, None))[1]!r}, its latest record says {pill!r}"
            for (k, n), (_, pill) in expect.items() if after.get((k, n), (None, None))[1] != pill]


def test_an_event_update_recomputes_every_cards_needs_you(record_property, tmp_path):
    """When a GitHub event updates the board, every card's Needs you is recomputed from its latest record.

    Closes issue #2 through the board's event sync; afterwards #4's stale pill is gone, #3 (which asks the owner) has
    one, closed #1 has none, and every other card keeps the pill its record gives."""
    record_property("proves", "135.2")
    state, expect = stale_board()
    state["issues"]["2"]["state"] = "CLOSED"
    expect[("issue", 2)] = ("Done", None)
    p, after = run(tmp_path, state, ["-m", "dokima.board"], event="issues",
                   payload={"action": "closed", "issue": {"number": 2}})
    assert p.returncode == 0, f"135.2: the event sync failed: {p.stderr[-2000:]}"
    wrong = pills(cards(after), expect)
    assert not wrong, "135.2: after an event update some pills disagree with their latest record:\n" + "\n".join(wrong)


def test_a_river_move_recomputes_every_cards_needs_you(record_property, tmp_path):
    """When the river moves one card after a run, every other card's Needs you is recomputed from its latest record too.

    Runs `python3 -m dokima.agent board 3 OUT` as the agent workflow does after the planner asked a question on #3;
    #4's stale pill drops off, closed #1 loses its pill, and #3 gets one."""
    record_property("proves", "135.2")
    state, expect = stale_board()
    out = tmp_path / "out"
    out.mkdir()
    (out / "board.txt").write_text("Plan needs\n")
    p, after = run(tmp_path, state, ["-m", "dokima.agent", "board", "3", str(out)])
    assert p.returncode == 0, f"135.2: the river's board move failed: {p.stderr[-2000:]}"
    wrong = pills(cards(after), expect)
    assert not wrong, "135.2: after a river move some pills disagree with their latest record:\n" + "\n".join(wrong)


def test_filing_a_split_recomputes_every_cards_needs_you(record_property, tmp_path):
    """When an approved split is filed and the board updated, every card's Needs you is recomputed from its latest record.

    Runs `python3 -m dokima.agent split 10` on an issue whose split is already filed; #4's stale pill drops off and #3
    gets one, alongside the split's own moves."""
    record_property("proves", "135.2")
    state, expect = stale_board()
    for n in (98, 99):
        state["issues"][str(n)] = {"title": f"Story {n}", "body": "", "state": "OPEN", "comments": []}
        expect[("issue", n)] = ("Backlog", None)
    p, after = run(tmp_path, state, ["-m", "dokima.agent", "split", "10"])
    assert p.returncode == 0, f"135.2: filing the split failed: {p.stderr[-2000:]}"
    wrong = pills(cards(after), expect)
    assert not wrong, "135.2: after filing a split some pills disagree with their latest record:\n" + "\n".join(wrong)


def test_an_approved_pr_waiting_for_merge_needs_you(record_property, tmp_path):
    """A pull request the reviewer approved, waiting for the owner's merge, shows Needs you on the PR and its issue.

    Puts issue #20 and its open PR #21 (latest record: the reviewer approves the work) on the board without a pill and
    presses the button: both get Needs you in Review. Then the PR merges and the issue closes: the next press clears
    both pills and moves them to Done."""
    record_property("proves", "135.3")
    state, expect = repo_and_board()
    state["issues"]["20"] = {"title": "Issue 20", "body": "", "state": "OPEN",
                             "comments": [said(record("planner", handback=PLAN), 1)]}
    state["prs"]["21"] = {"head": "try/issue-20", "state": "OPEN", "body": "", "reviews": [], "comments": [
        said(record("worker", handback={"summary": "s"}), 3),
        said(record("reviewer", "pr", {**REVIEW, "stage": "pr", "verdict": "approve", "blockers": []}), 4)]}
    state["board"]["items"] += [{"id": "ITEM-issue-20", "kind": "issue", "number": 20, "Status": "Review", "Action": None},
                                {"id": "ITEM-pr-21", "kind": "pr", "number": 21, "Status": "Review", "Action": None}]
    p, after = run(tmp_path, state, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.3: the button's run failed: {p.stderr[-2000:]}"
    got = cards(after)
    assert got[("issue", 20)] == ("Review", "Needs you"), f"135.3: the issue of an approved PR waiting for merge shows {got[('issue', 20)]}"
    assert got[("pr", 21)] == ("Review", "Needs you"), f"135.3: an approved PR waiting for merge shows {got[('pr', 21)]}"
    after["prs"]["21"]["state"], after["issues"]["20"]["state"] = "MERGED", "CLOSED"
    p, again = run(tmp_path, after, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.3: the second run failed: {p.stderr[-2000:]}"
    got = cards(again)
    assert got[("pr", 21)] == ("Done", None) and got[("issue", 20)] == ("Done", None), \
        f"135.3: once merged, the PR and issue still show {got[('pr', 21)]} and {got[('issue', 20)]}"


def test_the_boards_description_links_to_the_button(record_property, tmp_path):
    """The board's description links to the button, keeps what the owner wrote there, and never repeats the link.

    Presses the button on a board described as "Our team board.": afterwards the description still says that and
    holds the link to the board workflow's page, where "Run workflow" is. A second press leaves the link there once."""
    record_property("proves", "135.4")
    state, _ = repo_and_board()
    p, after = run(tmp_path, state, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.4: the button's run failed: {p.stderr[-2000:]}"
    text = after["board"]["description"]
    assert BUTTON in text, f"135.4: the board's description does not link to the button: {text!r}"
    assert "Our team board." in text, f"135.4: the owner's description was overwritten: {text!r}"
    p, again = run(tmp_path, after, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.4: the second run failed: {p.stderr[-2000:]}"
    assert again["board"]["description"].count(BUTTON) == 1, f"135.4: the link repeats: {again['board']['description']!r}"


def test_only_the_bots_records_set_needs_you(record_property, tmp_path):
    """A record pasted by a person never sets or clears Needs you; only the records Dokima's bot posted count.

    Issue #30's real latest record sends the plan to review (no pill); a person then pastes a record that asks the
    owner a question. After the button, #30 has no pill. Issue #31 is the mirror: its real record asks a question and
    a person pastes one that does not; #31 keeps Needs you."""
    record_property("proves", "135.5")
    state, _ = repo_and_board()
    state["issues"]["30"] = {"title": "Issue 30", "body": "", "state": "OPEN", "comments": [
        said(record("planner", handback=PLAN), 1), said(record("planner", handback=ASKS), 2, who="someone")]}
    state["issues"]["31"] = {"title": "Issue 31", "body": "", "state": "OPEN", "comments": [
        said(record("planner", handback=ASKS), 1), said(record("planner", handback=PLAN), 2, who="someone")]}
    state["board"]["items"] += [{"id": "ITEM-issue-30", "kind": "issue", "number": 30, "Status": "Plan", "Action": None},
                                {"id": "ITEM-issue-31", "kind": "issue", "number": 31, "Status": "Plan", "Action": None}]
    p, after = run(tmp_path, state, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.5: the button's run failed: {p.stderr[-2000:]}"
    got = cards(after)
    assert got[("issue", 30)] == ("Plan", None), f"135.5: a record pasted by a person set Needs you: {got[('issue', 30)]}"
    assert got[("issue", 31)] == ("Plan", "Needs you"), f"135.5: a record pasted by a person cleared Needs you: {got[('issue', 31)]}"
