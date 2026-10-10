"""Tests for #426: every run records the GitHub API budget left before and after it.

These run `python3 -m dokima.budget before|after KEY FILE` the way a workflow step runs it, against a fake `gh` put
first on PATH. The fake answers `gh api rate_limit` with GitHub's own shape (resources.graphql and resources.core),
or refuses the way gh does (GitHub's reason on stderr, exit 1), and logs every call it gets so a test can see the
command spent nothing but the free rate-limit read. Each reading goes to the step's log (stdout) and, as one JSON
line, to FILE, the small file the workflow keeps with the run.
"""
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FAKE_GH = """#!{python}
import json, os, sys
with open(os.environ["FAKE_GH_LOG"], "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")
if os.environ.get("FAKE_GH_FAIL"):
    print(os.environ["FAKE_GH_FAIL"], file=sys.stderr)
    sys.exit(1)
sys.stdout.write(os.environ["FAKE_GH_ANSWER"])
"""


def rate_limit(graphql, rest):
    """GitHub's answer to GET /rate_limit, with these two budgets left of 5,000 each."""
    def one(left):
        return {"limit": 5000, "used": 5000 - left, "remaining": left, "reset": 1791655200}
    return json.dumps({"resources": {"core": one(rest), "graphql": one(graphql), "search": one(30)},
                       "rate": one(rest)})


def run_budget(tmp_path, moment, key, answer="", fail=""):
    """Run the budget command once against the fake gh; return its exit, log, entries and calls."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    gh = bin_dir / "gh"
    gh.write_text(FAKE_GH.format(python=sys.executable))
    gh.chmod(0o755)
    log = tmp_path / "gh-calls.jsonl"
    file = tmp_path / "budget.jsonl"
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}", "PYTHONPATH": ROOT,
           "FAKE_GH_LOG": str(log), "FAKE_GH_ANSWER": answer, "FAKE_GH_FAIL": fail, "GH_TOKEN": "fake-token",
           "GITHUB_WORKFLOW": "card", "GITHUB_RUN_ID": "4242", "GITHUB_REPOSITORY": "acme/widgets"}
    env.pop("PYTHONSAFEPATH", None)
    if not fail:
        env.pop("FAKE_GH_FAIL")
    r = subprocess.run([sys.executable, "-m", "dokima.budget", moment, key, str(file)], cwd=str(tmp_path), env=env,
                       capture_output=True, text=True, timeout=30)
    entries = [json.loads(l) for l in file.read_text().splitlines() if l.strip()] if file.exists() else []
    calls = [json.loads(l) for l in log.read_text().splitlines() if l.strip()] if log.exists() else []
    return r.returncode, r.stdout + r.stderr, entries, calls


def number(n):
    """A number as the log may write it: 4321 or 4,321."""
    s = str(n)
    return rf"{s[:-3]},?{s[-3:]}" if len(s) > 3 else s


def test_a_reading_before_the_run_goes_to_the_log_and_the_file(tmp_path, record_property):
    """A run's budget before it starts shows in its log and its kept file.

    Proves 426.2.

    Runs the budget command for `before` with the Dokima app's key against a fake GitHub that has 4,321 GraphQL and
    4,987 REST left, and checks the log names both budgets with their numbers, and that the file holds one JSON
    line naming the workflow, the run, the time, the key and the moment, with the two numbers."""
    record_property("proves", "426.2")
    code, log, entries, _ = run_budget(tmp_path, "before", "app", answer=rate_limit(4321, 4987))
    assert code == 0, f"426.2: the budget command failed (exit {code}):\n{log[-800:]}"
    assert re.search(r"GraphQL\D*" + number(4321), log) and re.search(r"REST\D*" + number(4987), log), \
        f"426.2: the log should name GraphQL 4,321 and REST 4,987 left; it says:\n{log}"
    assert "before" in log and "app" in log, f"426.2: the log should say this is the app key's budget before the run:\n{log}"
    assert len(entries) == 1, f"426.2: the file should hold exactly one reading, it holds {len(entries)}: {entries}"
    e = entries[0]
    assert (e.get("workflow"), str(e.get("run")), e.get("key"), e.get("moment")) == ("card", "4242", "app", "before"), \
        f"426.2: the reading should name workflow card, run 4242, key app and moment before; it is {e}"
    assert (e.get("graphql"), e.get("rest")) == (4321, 4987), \
        f"426.2: the reading should hold GraphQL 4321 and REST 4987 left; it is {e}"
    assert "error" not in e, f"426.2: a reading GitHub gave should carry no error: {e}"
    when = datetime.datetime.strptime(e.get("time", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    assert abs((datetime.datetime.now(datetime.timezone.utc) - when).total_seconds()) < 120, \
        f"426.2: the reading's time should be now, in UTC; it is {e.get('time')}"


def test_a_reading_after_the_run_is_added_to_the_same_file(tmp_path, record_property):
    """The budget after a run is added beside the reading before it, never over it.

    Proves 426.2.

    Reads before (4,321 GraphQL, 4,987 REST) and after (4,100 GraphQL, 4,950 REST) into one file, with the repo's own
    GITHUB_TOKEN named as the key, and checks both readings are there in order, each with its own numbers."""
    record_property("proves", "426.2")
    run_budget(tmp_path, "before", "github-token", answer=rate_limit(4321, 4987))
    code, log, entries, _ = run_budget(tmp_path, "after", "github-token", answer=rate_limit(4100, 4950))
    assert code == 0, f"426.2: the budget command failed after the run (exit {code}):\n{log[-800:]}"
    assert re.search(r"GraphQL\D*" + number(4100), log) and re.search(r"REST\D*" + number(4950), log), \
        f"426.2: the log should name GraphQL 4,100 and REST 4,950 left after the run; it says:\n{log}"
    assert "after" in log and "github-token" in log, \
        f"426.2: the log should say this is the GITHUB_TOKEN's budget after the run:\n{log}"
    got = [(e.get("moment"), e.get("key"), e.get("graphql"), e.get("rest")) for e in entries]
    assert got == [("before", "github-token", 4321, 4987), ("after", "github-token", 4100, 4950)], \
        f"426.2: the file should hold the reading before, then the one after; it holds {got}"


def test_a_refused_reading_never_stops_the_run_and_says_githubs_reason(tmp_path, record_property):
    """When GitHub refuses the budget, the run goes on and its log and file say why.

    Proves 426.3.

    The fake gh refuses with GitHub's reason, as gh does. The command must still exit 0, so the run does its work,
    and both the log and the file's reading must say the budget could not be read, with that reason."""
    record_property("proves", "426.3")
    reason = "gh: API rate limit exceeded for installation ID 1 (HTTP 403)"
    code, log, entries, _ = run_budget(tmp_path, "before", "app", fail=reason)
    assert code == 0, f"426.3: a budget GitHub would not give must not fail the run, but the command exited {code}:\n{log}"
    assert "could not be read" in log and "API rate limit exceeded for installation ID 1 (HTTP 403)" in log, \
        f"426.3: the log should say the budget could not be read, with GitHub's reason; it says:\n{log}"
    assert len(entries) == 1, f"426.3: the file should still get one reading, it holds {entries}"
    e = entries[0]
    assert "API rate limit exceeded for installation ID 1 (HTTP 403)" in str(e.get("error", "")), \
        f"426.3: the reading should carry GitHub's reason under error; it is {e}"
    assert e.get("graphql") is None and e.get("rest") is None, f"426.3: a refused reading should hold no numbers: {e}"
    assert (e.get("workflow"), e.get("key"), e.get("moment")) == ("card", "app", "before"), \
        f"426.3: a refused reading still names the workflow, the key and the moment: {e}"


def test_an_answer_that_is_not_a_budget_never_stops_the_run(tmp_path, record_property):
    """An answer holding no budget is said plainly, and the run goes on.

    Proves 426.3.

    The fake gh answers with something that is not GitHub's rate-limit shape. The command must exit 0, and its
    log and file must say the budget could not be read, with a reason, instead of writing made-up numbers."""
    record_property("proves", "426.3")
    code, log, entries, _ = run_budget(tmp_path, "after", "app", answer="<html>Service unavailable</html>")
    assert code == 0, f"426.3: an unreadable answer must not fail the run, but the command exited {code}:\n{log}"
    assert "could not be read" in log, f"426.3: the log should say the budget could not be read; it says:\n{log}"
    assert len(entries) == 1 and str(entries[0].get("error") or "").strip(), \
        f"426.3: the file should hold one reading with a reason under error; it holds {entries}"
    assert entries[0].get("graphql") is None and entries[0].get("rest") is None, \
        f"426.3: an unreadable answer should leave no numbers: {entries[0]}"


def test_reading_the_budget_only_asks_the_free_rate_limit_endpoint(tmp_path, record_property):
    """Measuring the budget spends none of it: the only call is GitHub's free rate-limit read.

    Proves 426.4.

    Runs a reading and checks the fake gh got exactly one call, `gh api rate_limit`, and no GraphQL query or
    other API call that would count against either budget."""
    record_property("proves", "426.4")
    code, log, _, calls = run_budget(tmp_path, "before", "app", answer=rate_limit(4321, 4987))
    assert code == 0, f"426.4: the budget command failed (exit {code}):\n{log[-800:]}"
    assert calls in ([["api", "rate_limit"]], [["api", "/rate_limit"]]), \
        f"426.4: the only call should be `gh api rate_limit`, which costs nothing; the calls were {calls}"
