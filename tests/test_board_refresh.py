"""The board's refresh button, and the Needs you recount on every board update (#135).

These tests run Dokima the way the workflows do (`python3 -m dokima.board`, `python3 -m dokima.agent board|split`)
with a fake `gh` first on PATH. The fake keeps a whole small repo and board in one JSON file: issues with their labels,
pull requests, their comments (the records), and the board's items with their Status and Action. It answers the gh
calls Dokima makes (issue view, pr list, pr view, api, and GraphQL for the board) and saves every board change, so a
test reads the board as it stands afterwards, whatever order the code wrote it in.
"""
import json as _json
import os
import re
import subprocess as _subprocess
import sys
import tempfile as _tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "board.yml")
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
    fields = {"Status": ("S", ["Backlog", "Plan", "Work", "Review", "Done"]), "Action": ("W", ["Needs you", "Autopilot"])}
    by_fid = {fid: name for name, (fid, _) in fields.items()}
    opt_name = {f"{fid}-{o}": o for _, (fid, opts) in fields.items() for o in opts}
    def content(it):
        if it["kind"] == "issue":
            i = s["issues"][str(it["number"])]
            return {"__typename": "Issue", "id": f"C-issue-{it['number']}", "number": it["number"], "state": i["state"],
                    "title": i["title"], "url": f"https://github.com/o/r/issues/{it['number']}",
                    "repository": {"nameWithOwner": "o/r"}, "labels": {"nodes": [{"name": l} for l in i.get("labels", [])]},
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
    if "node(" in q and "fieldValueByName" in q:
        it = next((x for x in b["items"] if x["id"] == v.get("i")), None)
        name = it.get(v.get("f")) if it else None
        out({"data": {"node": {"fieldValueByName": {"name": name} if name else None}}})
    if "node(" in q:
        out({"data": {"node": project()}})
    if "repository" in q:
        if "pullRequests(" in q:
            heads = [{"number": int(n)} for n, p in sorted(s["prs"].items(), key=lambda x: int(x[0]))
                     if p["head"] == v.get("h") and p["state"] == "OPEN"]
            out({"data": {"repository": {"pullRequests": {"nodes": heads[:1]}}}})
        kind = "issue" if re.search(r"\bissue\(", q) else "pullRequest"
        n = v["n"]
        on = [{"id": x["id"], "project": {"id": "P"}} for x in b["items"] if x["kind"] == ("issue" if kind == "issue" else "pr") and x["number"] == n]
        thing = s["issues"].get(str(n), {}) if kind == "issue" else s["prs"].get(str(n), {})
        out({"data": {"repository": {kind: {"id": f"C-{'issue' if kind == 'issue' else 'pr'}-{n}", "projectItems": {"nodes": on},
                                            "labels": {"nodes": [{"name": l} for l in thing.get("labels", [])]}, "parent": None}}}})
    fail("unknown query: " + q[:80])

if args[:2] == ["issue", "view"]:
    i = s["issues"].get(args[2])
    if i is None:
        fail("no issue " + args[2])
    out({"number": int(args[2]), "title": i["title"], "body": i.get("body", ""), "state": i["state"], "comments": i["comments"],
         "labels": [{"name": l} for l in i.get("labels", [])]})
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
if args[:1] == ["api"]:
    path = next((a for i, a in enumerate(args[1:], 1) if not a.startswith("-") and args[i - 1] not in ("-X", "-f", "-F", "-q", "--jq")), "")
    if re.match(r"repos/o/r/pulls/\d+/comments", path):
        out([])
    m = re.fullmatch(r"repos/o/r/issues/(\d+)", path)
    if m and m.group(1) in s["issues"] and "-X" not in args:
        i = s["issues"][m.group(1)]
        out({"number": int(m.group(1)), "id": int(m.group(1)), "state": i["state"].lower(),
             "labels": [{"name": l} for l in i.get("labels", [])]})
fail("unsupported: " + " ".join(args))
'''


def record(role, stage="", handback=None, passed=True, attempt=None):
    """A record built exactly as the workflow builds one, before the bot posts it."""
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
    """A comment carrying a record, as GitHub returns it, posted at that minute."""
    return {"author": {"login": who}, "body": agent.render(rec), "createdAt": f"2026-10-08T10:{minute:02d}:00Z"}


REVIEW = {"previous_step": {"did": [], "decided": [], "open": []}, "round": 1, "summary": "s", "notes": [],
          "outside_plan": [], "resolved": []}
BLOCK = {"id": "B1", "criterion": "9.1", "test": None, "problem": "p", "evidence": "e", "fix": "f"}
PLAN = {"kind": "user_story", "user_story": "s"}
ASKS = {**PLAN, "questions": [{"question": "Which one?", "assumption": "The first."}]}
FEATURE = {"kind": "feature", "feature": "f", "stories": [{"title": "a"}, {"title": "b"}]}


def repo_and_board():
    """A small repo whose board is scrambled: every card has the wrong column and pill.

    Returns (state, expected): expected maps each card to the (column, pill) its real state and latest record give."""
    issues, prs, expect = {}, {}, {}
    def issue(n, comments=(), state="OPEN", labels=()):
        issues[str(n)] = {"title": f"Issue {n}", "body": "", "state": state, "comments": list(comments), "labels": list(labels)}
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
    # On autopilot: a card the river does not stop for shows Autopilot; one it stops for shows Needs you.
    issue(7, [said(record("planner", handback=PLAN), 1)], labels=["autopilot"]); expect[("issue", 7)] = ("Plan", "Autopilot")
    issue(8, [said(record("planner", handback=PLAN), 1), said(record("not-started", attempt="worker"), 2)], labels=["autopilot"])
    expect[("issue", 8)] = ("Work", "Needs you")
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
    """Run Dokima as the workflow does, with the fake gh first on PATH.

    Returns the finished process and the board state afterwards."""
    bin_dir, path = tmp_path / "bin", tmp_path / "state.json"
    bin_dir.mkdir(exist_ok=True)
    path.write_text(_json.dumps(state))
    gh = bin_dir / "gh"
    gh.write_text(f"#!{sys.executable} -S\n" + FAKE_GH.replace("__STATE__", repr(str(path))))
    gh.chmod(0o755)
    (tmp_path / "event.json").write_text(_json.dumps(payload or {}))
    # The machine's own run settings never leak in: a CARD_ID from an agent run would send `agent split` to edit it.
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GITHUB_", "DOKIMA_")) and k not in ("CARD_ID", "ROLE", "STAGE", "N")}
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
    """Every card whose column or pill differs from its real state, in plain words."""
    return [f"{crit}: {k} #{n} is in {after.get((k, n), ('not on the board',))[0]} with pill {after.get((k, n), (None, None))[1]!r}, "
            f"its real state says {col} with pill {pill!r}" for (k, n), (col, pill) in expect.items() if after.get((k, n)) != (col, pill)]


def test_the_button_puts_every_card_back_where_its_real_state_says(record_property, tmp_path):
    """Pressing "Run workflow" puts every card in the column its real state says.

    Scrambles a board of fifteen cards over eight pages, then runs `python3 -m dokima.board` as the button does. Closed or
    merged is Done; an issue with no record is Backlog; an issue with records goes where the river put it after its
    latest record (a question stops in Plan, a plan going to review is Plan, finished work is Review, blocked work is
    Work, a filed split is Work, a run that never started stops in Work); a pull request goes with its issue, and one
    built for no issue is Review. Two issues on autopilot are placed the same way. Proves 135.1."""
    record_property("proves", "135.1")
    state, expect = repo_and_board()
    p, after = run(tmp_path, state, ["-m", "dokima.board"])
    assert p.returncode == 0, f"135.1: the button's run failed: {p.stderr[-2000:]}"
    wrong = [d for d in differences(cards(after), expect, "135.1")]
    assert not wrong, "\n".join(wrong)


def test_the_board_workflow_has_the_button(record_property):
    """The board workflow can be started by hand, so GitHub shows "Run workflow".

    The trigger is workflow_dispatch, the board setting still guards the job, and it runs the board code. Proves 135.1."""
    record_property("proves", "135.1")
    wf = open(WORKFLOW).read()
    on = wf[wf.index("\non:"):wf.index("\npermissions:")]
    assert re.search(r"(?m)^  workflow_dispatch:", on), "135.1: the board workflow has no workflow_dispatch trigger, so there is no button"
    assert "if: vars.DOKIMA_BOARD != ''" in wf, "135.1: the button would run without a board"
    assert "python3 -m dokima.board" in wf, "135.1: the button does not run the board code"


def stale_board():
    """A board with stale pills: #4, #7 and closed #1 wrongly need you; #3 lacks it."""
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
        if (it["kind"], it["number"]) == ("issue", 7):
            it["Action"] = "Needs you"
    return state, expect


def pills(after, expect):
    """Every card whose Needs you pill disagrees with its latest record."""
    return [f"{k} #{n}: pill {after.get((k, n), (None, None))[1]!r}, its latest record says {pill!r}"
            for (k, n), (_, pill) in expect.items() if after.get((k, n), (None, None))[1] != pill]


def test_an_event_update_recomputes_every_cards_needs_you(record_property, tmp_path):
    """A GitHub event recomputes every card's Needs you from its latest record.

    Closes issue #2 through the board's event sync; afterwards #4's stale pill is gone, #3 (which asks the owner) has
    one, closed #1 has none, and every other card keeps the pill its record gives. Proves 135.2."""
    record_property("proves", "135.2")
    state, expect = stale_board()
    state["issues"]["2"]["state"] = "CLOSED"
    expect[("issue", 2)] = ("Done", None)
    p, after = run(tmp_path, state, ["-m", "dokima.board"], event="issues",
                   payload={"action": "closed", "issue": {"number": 2}})
    assert p.returncode == 0, f"135.2: the event sync failed: {p.stderr[-2000:]}"
    wrong = pills(cards(after), expect)
    assert not wrong, "135.2: after an event update some pills disagree with their latest record:\n" + "\n".join(wrong)


def test_an_event_that_moves_no_card_still_recounts_every_pill(record_property, tmp_path):
    """A comment that moves no card still recounts every card's Needs you.

    Sends the board workflow an issue_comment event from a person on #2; afterwards #4's stale pill is gone, #3 has
    one, closed #1 has none, and every other card keeps the pill its record gives. Proves 135.2."""
    record_property("proves", "135.2")
    state, expect = stale_board()
    p, after = run(tmp_path, state, ["-m", "dokima.board"], event="issue_comment",
                   payload={"action": "created", "issue": {"number": 2},
                            "comment": {"user": {"login": "someone", "type": "User"}, "body": "Looks good."}})
    assert p.returncode == 0, f"135.2: the event sync failed: {p.stderr[-2000:]}"
    wrong = pills(cards(after), expect)
    assert not wrong, "135.2: after a comment event some pills disagree with their latest record:\n" + "\n".join(wrong)


def test_a_river_move_recomputes_every_cards_needs_you(record_property, tmp_path):
    """When the river moves one card after a run, every card's Needs you is recomputed.

    Runs `python3 -m dokima.agent board 3 OUT` as the agent workflow does after the planner asked a question on #3;
    #4's stale pill drops off, closed #1 loses its pill, and #3 gets one. Proves 135.2."""
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
    """Filing an approved split recomputes every card's Needs you from its latest record.

    Runs `python3 -m dokima.agent split 10` on an issue whose split is already filed; #4's stale pill drops off and #3
    gets one, alongside the split's own moves. Proves 135.2."""
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
    """A reviewer-approved PR waiting for the owner's merge needs you, on itself and its issue.

    Puts issue #20 and its open PR #21 (latest record: the reviewer approves the work) on the board without a pill and
    presses the button: both get Needs you in Review. Then the PR merges and the issue closes: the next press clears
    both pills and moves them to Done. Proves 135.3."""
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
    """The board's description links to the button once and keeps the owner's words.

    Presses the button on a board described as "Our team board.": afterwards the description still says that and
    holds the link to the board workflow's page, where "Run workflow" is. A second press leaves the link there once. Proves 135.4."""
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
    """A record pasted by a person never sets or clears Needs you.

    Issue #30's real latest record sends the plan to review (no pill); a person then pastes a record that asks the
    owner a question. After the button, #30 has no pill. Issue #31 is the mirror: its real record asks a question and
    a person pastes one that does not; #31 keeps Needs you. Proves 135.5."""
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


def test_the_recount_keeps_autopilot_on_cards_that_do_not_need_you(record_property, tmp_path):
    """After a recount, autopilot cards show Autopilot, or Needs you when the river stopped.

    #7 is on autopilot with a stale Needs you, its plan going on to review: after an event update it shows Autopilot.
    #8 is on autopilot and its worker never started, but shows Autopilot: afterwards it shows Needs you. A plain issue
    whose stale pill drops off (#4) gets no Autopilot. Proves 135.6."""
    record_property("proves", "135.6")
    state, expect = stale_board()
    for it in state["board"]["items"]:
        if (it["kind"], it["number"]) == ("issue", 8):
            it["Action"] = "Autopilot"
    p, after = run(tmp_path, state, ["-m", "dokima.board"], event="issue_comment",
                   payload={"action": "created", "issue": {"number": 2},
                            "comment": {"user": {"login": "someone", "type": "User"}, "body": "Looks good."}})
    assert p.returncode == 0, f"135.6: the event sync failed: {p.stderr[-2000:]}"
    got = cards(after)
    assert got[("issue", 7)][1] == "Autopilot", f"135.6: #7 is on autopilot and needs no one, but shows {got[('issue', 7)][1]!r}"
    assert got[("issue", 8)][1] == "Needs you", f"135.6: #8 is on autopilot and stopped for the owner, but shows {got[('issue', 8)][1]!r}"
    assert got[("issue", 4)][1] is None, f"135.6: #4 is not on autopilot and needs no one, but shows {got[('issue', 4)][1]!r}"
