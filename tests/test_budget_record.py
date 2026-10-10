"""Tests for #426: an agent run's record shows the API budget before and after it.

agent.yml reads the Dokima app's budget into OUT/budget.jsonl (one JSON line per reading, written by
`python3 -m dokima.budget`) before the run and again once the agent has finished, before the record is written.
These run the workflow's own record commands (`python3 -m dokima.agent record` and `not-started`) on such a file and
check the JSON record holds the four numbers and the record shows them: in its Stats fold when an agent ran, and on
its closing No agent ran line when none did.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = "acme/widgets"


def reading(moment, graphql=None, rest=None, error=None):
    """One line of the budget file, as `python3 -m dokima.budget` writes it."""
    e = {"workflow": "agent", "run": "42", "time": "2026-10-10T18:00:00Z", "key": "app", "moment": moment}
    if error:
        e["error"] = error
    else:
        e.update(graphql=graphql, rest=rest)
    return json.dumps(e)


def make_out(tmp_path, lines):
    """A hand-back folder holding a passed plan and the budget readings; returns (out, logs)."""
    out, logs = tmp_path / "out", tmp_path / "logs"
    out.mkdir()
    logs.mkdir()
    (out / "plan.json").write_text(json.dumps({"kind": "user_story", "summary": "A plan.", "user_story": "A story.",
                                               "acceptance_criteria": [], "non_functional": [], "scope": [],
                                               "out_of_scope": [], "tests": {}, "test_changes": {},
                                               "links": {"blocked_by": [], "blocks": [], "relates_to": []}}))
    (out / "check.txt").write_text("")
    (out / "budget.jsonl").write_text("\n".join(lines) + "\n")
    return out, logs


def run_agent(*args):
    """Run one of agent.yml's record commands; fails the test when it fails."""
    env = {**os.environ, "PYTHONPATH": ROOT, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_REPOSITORY": REPO,
           "GITHUB_RUN_ID": "42"}
    env.pop("PYTHONSAFEPATH", None)
    env.pop("PACK", None)
    r = subprocess.run([sys.executable, "-m", "dokima.agent", *args], cwd=ROOT, env=env, capture_output=True,
                       text=True, timeout=60)
    assert r.returncode == 0, f"426.1: `agent {args[0]}` failed (exit {r.returncode}):\n{r.stderr[-800:]}"


def stats(out):
    """The line inside the record's Stats fold, beside the run's model, time and cost."""
    text = (out / "comment.md").read_text()
    m = re.search(r"Stats</b></summary>\s*\n(.*?)\n\s*</details>", text, re.S)
    assert m, f"426.1: the record should have a Stats fold; it is:\n{text[:800]}"
    return m.group(1).strip()


def no_agent_line(out):
    """The closing line of a record whose agent never started: `No agent ran`, in <sub>."""
    lines = [l for l in (out / "comment.md").read_text().splitlines() if l.strip()]
    assert lines and lines[-1].startswith("<sub>") and "No agent ran" in lines[-1], \
        f"426.1: the record of a run whose agent never started should end with its No agent ran line; it ends {lines[-1:]}"
    return lines[-1]


def test_the_record_of_an_agent_run_shows_the_budget_before_and_after(tmp_path, record_property):
    """An agent's record shows both budgets before and after the run, in Stats and JSON.

    Proves 426.1.

    Writes a budget file with GraphQL 4,321 and REST 4,987 left before the run and 4,100 and 4,950 after it, writes
    the planner's record from it, and checks the JSON record holds the four numbers in the right places and the
    Stats fold shows GraphQL 4,321 → 4,100 and REST 4,987 → 4,950."""
    record_property("proves", "426.1")
    out, logs = make_out(tmp_path, [reading("before", 4321, 4987), reading("after", 4100, 4950)])
    run_agent("record", "planner", "", str(out), str(out / "check.txt"), "true", str(logs))
    rec = json.loads((out / "record.json").read_text())
    b = rec.get("budget") or {}
    got = {(m, k): (b.get(m) or {}).get(k) for m in ("before", "after") for k in ("graphql", "rest")}
    want = {("before", "graphql"): 4321, ("before", "rest"): 4987, ("after", "graphql"): 4100, ("after", "rest"): 4950}
    assert got == want, f"426.1: the JSON record should hold budget.before and budget.after with both numbers; got {b}"
    line = stats(out)
    assert "GraphQL 4,321 → 4,100" in line and "REST 4,987 → 4,950" in line, \
        f"426.1: the Stats fold should show GraphQL 4,321 → 4,100 and REST 4,987 → 4,950; it is:\n{line}"


def test_a_run_whose_agent_never_started_still_shows_the_budget(tmp_path, record_property):
    """A run that stopped before its agent started still shows both budgets.

    Proves 426.1.

    Writes the not-started record from a budget file with readings before and after, and checks the four numbers
    are in the JSON record and on the record's closing No agent ran line, since no Stats fold is drawn."""
    record_property("proves", "426.1")
    out, _ = make_out(tmp_path, [reading("before", 3000, 4800), reading("after", 2950, 4790)])
    why = tmp_path / "why.txt"
    why.write_text("Building the starting pack failed.\n")
    run_agent("not-started", "worker", "", str(out), str(why))
    b = json.loads((out / "record.json").read_text()).get("budget") or {}
    got = [(b.get(m) or {}).get(k) for m in ("before", "after") for k in ("graphql", "rest")]
    assert got == [3000, 4800, 2950, 4790], \
        f"426.1: the not-started record should hold the budget before and after; it holds {b}"
    line = no_agent_line(out)
    assert "GraphQL 3,000 → 2,950" in line and "REST 4,800 → 4,790" in line, \
        f"426.1: the not-started record's No agent ran line should show GraphQL 3,000 → 2,950 and REST 4,800 → 4,790; it is:\n{line}"


def test_a_budget_github_would_not_give_is_said_in_the_record(tmp_path, record_property):
    """A budget GitHub would not give is said in the record, with GitHub's reason.

    Proves 426.3.

    The reading before the run carries GitHub's refusal; the reading after holds numbers. The record must be
    written, its JSON must keep the reason, and its Stats fold must say the budget could not be read, with the
    reason, beside the numbers after the run."""
    record_property("proves", "426.3")
    reason = "API rate limit exceeded for installation ID 1 (HTTP 403)"
    out, logs = make_out(tmp_path, [reading("before", error=reason), reading("after", 4100, 4950)])
    run_agent("record", "planner", "", str(out), str(out / "check.txt"), "true", str(logs))
    b = json.loads((out / "record.json").read_text()).get("budget") or {}
    assert reason in str((b.get("before") or {}).get("error", "")), \
        f"426.3: the JSON record should keep GitHub's reason for the budget before; it holds {b}"
    assert ((b.get("after") or {}).get("graphql"), (b.get("after") or {}).get("rest")) == (4100, 4950), \
        f"426.3: the budget after the run should still be recorded; it holds {b}"
    line = stats(out)
    assert "could not be read" in line and reason in line, \
        f"426.3: the Stats fold should say the budget could not be read, with GitHub's reason; it is:\n{line}"
    assert "4,100" in line and "4,950" in line, f"426.3: the Stats fold should still show the budget after; it is:\n{line}"
