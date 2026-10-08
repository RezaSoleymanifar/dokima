"""Red before work: the plan's tests must fail on main, on an assert, before the worker starts (#81).

A test that already passes before the work exists proves nothing, and a test that crashes burns the worker's whole
budget against something it can never pass. So when the owner says `/work`, code runs the plan's tests against main's
code first, and names every test that passes or crashes there instead of starting the worker.

These tests run the whole agent workflow (.github/workflows/agent.yml) for the worker, with the machinery of
tests/test_start.py: a temp repo with a local origin, a fake GitHub and a fake Claude Code. Main holds a small module,
`calc.py`, whose `double()` is wrong; the issue's try branch holds the plan's tests and, as on a re-run after the worker
already built, the fix. The plan names which of the branch's tests prove the issue, so each test can say exactly which
tests are the plan's and how each one behaves on main: fails an assert, passes, crashes, or cannot be found.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from test_start import (APPROVE, N, OWNER, Machine, Ctx, agent, owner_comment, planner_record,  # noqa: E402
                        record_comment, review_record, sh, workflow)

# main's code: double() is wrong, so a test of it fails on an assert there.
MAIN_CALC = "def double(x):\n    return x\n"
# The branch already holds the fix, the way it does when the worker runs again after a review.
FIXED_CALC = "def double(x):\n    return 2 * x\n"
# Every test file puts its repo's root first on the path, so it imports calc.py from wherever it is run.
HEAD = ("import os, sys\nsys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
        "import pytest\nfrom calc import double\n\n\n")
CALC_TESTS = HEAD + '''@pytest.fixture
def broken_setup():
    raise RuntimeError("setup blew up")


def test_red():
    assert double(2) == 4


def test_red_too():
    assert double(3) == 6


def test_green():
    assert double(0) == 0


def test_crash():
    return {}["missing"]


def test_setup_crash(broken_setup):
    assert double(2) == 4


def test_skipped():
    pytest.skip("not today")


def test_unlisted_green():
    assert double(0) == 0


def test_unlisted_crash():
    raise RuntimeError("not the plan's")
'''
MORE_TESTS = HEAD + "def test_also_green():\n    assert double(1) == double(1)\n"
GONE_TESTS = "import nowhere_module_81\n\n\ndef test_x():\n    assert nowhere_module_81.x == 1\n"
OTHER_TESTS = "def test_other_crash():\n    raise RuntimeError('an older test outside this plan')\n"

RED = "tests/test_calc.py::test_red"
RED_TOO = "tests/test_calc.py::test_red_too"
GREEN = "tests/test_calc.py::test_green"
ALSO_GREEN = "tests/test_more.py::test_also_green"
CRASH = "tests/test_calc.py::test_crash"
SETUP_CRASH = "tests/test_calc.py::test_setup_crash"
GONE = "tests/test_gone.py::test_x"
SKIPPED = "tests/test_calc.py::test_skipped"
MISSING = "tests/test_calc.py::test_not_written"
UNLISTED = ["tests/test_calc.py::test_unlisted_green", "tests/test_calc.py::test_unlisted_crash",
            "tests/test_other.py::test_other_crash"]


def plan_with(tests):
    """An approved-shape story plan whose criterion 57.1 is proved by the given tests."""
    return {"kind": "user_story", "user_story": "Doubling works.",
            "acceptance_criteria": [{"text": "double(x) is 2x", "source": "https://github.com/o/r/issues/57"}],
            "non_functional": [], "scope": ["calc.py"], "out_of_scope": [], "tests": {"57.1": list(tests)}}


class WorkerRun(Machine):
    """One run of the agent workflow for the worker, after the owner's `/work` on an approved plan naming `tests`."""

    def __init__(self, tmp, tests):
        comments = [owner_comment("/plan", "2026-10-07T10:00:00Z"),
                    record_comment(planner_record(plan_with(tests)), "2026-10-07T10:10:00Z"),
                    record_comment(review_record(APPROVE), "2026-10-07T10:20:00Z"),
                    owner_comment("/work", "2026-10-07T10:30:00Z")]
        super().__init__(tmp, comments)
        t, src = self.tmp, f"{self.tmp}/src"
        # main: the wrong calc.py and an older crashing test that no plan names.
        os.makedirs(f"{src}/tests")
        open(f"{src}/calc.py", "w").write(MAIN_CALC)
        open(f"{src}/tests/test_other.py", "w").write(OTHER_TESTS)
        sh(src, "git", "add", "-A")
        sh(src, "git", "commit", "-qm", "calc")
        sh(src, "git", "push", "-q", "origin", "main")
        # try/issue-57: the planner's tests, then the worker's fix from an earlier round.
        sh(src, "git", "checkout", "-q", "-b", f"try/issue-{N}")
        for name, body in (("test_calc.py", CALC_TESTS), ("test_more.py", MORE_TESTS), ("test_gone.py", GONE_TESTS)):
            open(f"{src}/tests/{name}", "w").write(body)
        sh(src, "git", "add", "-A")
        sh(src, "git", "commit", "-qm", "planner's tests")
        open(f"{src}/calc.py", "w").write(FIXED_CALC)
        sh(src, "git", "commit", "-qam", "worker's fix")
        sh(src, "git", "push", "-q", "origin", f"try/issue-{N}")
        open(f"{t}/event.json", "w").write(json.dumps({"inputs": {"role": "worker", "stage": "", "issue": N}}))
        ctx = {"inputs": Ctx(role="worker", stage="", issue=N),
               "github": Ctx(event_name="workflow_dispatch", actor=OWNER, event=Ctx(), run_id="42", run_attempt="1",
                             server_url="https://github.com", repository="o/r", token="fake-github-token"),
               "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
               "vars": Ctx(DOKIMA_APP_ID="1"), "needs": Ctx()}
        wf = workflow("agent.yml")
        self.result, _ = self.run_job("run", wf["jobs"]["run"], ctx, "workflow_dispatch",
                                      [("/tmp/", f"{t}/"), ("/home/runner/", f"{t}/home/")], wf.get("defaults"))
        self.failed = self.result == "failure"

    def stopped_records(self):
        """Every posted record saying the run stopped before its agent started, with where it was posted."""
        out = []
        for p in self.posted():
            for r in agent.records([{"author": {"login": agent.BOT}, "body": p["body"]}]):
                if r.get("role") == "not-started":
                    out.append((p["where"], p["body"], r))
        return out


def says(body, test):
    """What the comment says about one test: the words after each place it is named, up to the next test or line end.

    Only the readable part of the comment counts, not the full record folded below it. The workflow may join several
    reasons on one line, so a test's words end where the next test's name (path::test) begins."""
    readable = body.split("<details>")[0]
    said = []
    for line in readable.splitlines():
        at = line.find(test)
        while at >= 0:
            rest = line[at + len(test):]
            nxt = rest.find(".py::")
            if nxt >= 0:
                cut = max(rest.rfind(c, 0, nxt) for c in " ;,")
                rest = rest[:cut if cut >= 0 else nxt]
            said.append(rest)
            at = line.find(test, at + 1)
    return " ".join(said)


def one_stop_on_the_issue(r, crit):
    """The run's single stop record, posted on the issue, after checking the worker never started."""
    assert not r.agent_started(), f"{crit}: the worker started though a plan test does not fail an assert on main:\n{r.tail()}"
    stops = r.stopped_records()
    assert len(stops) == 1, f"{crit}: expected one comment saying why the worker did not start, got {len(stops)}:\n{r.tail()}"
    where, body, _ = stops[0]
    assert where[:3] == ["issue", "comment", N], f"{crit}: the reason was posted at {where}, not on issue #{N}"
    assert r.failed, f"{crit}: the run that stopped the worker ended as a success"
    return body


def test_tests_that_fail_an_assert_on_main_let_the_worker_start(record_property, tmp_path):
    """When every plan test fails an assert on main, the worker starts; any plan test that passes there stops it first.

    Runs the worker twice on an issue whose branch already holds the fix. First the plan names two tests that fail an
    assert on main's code (and would pass on the branch); beside them sit tests the plan does not name, one that passes
    and two that crash, one of them an older test on main. The worker must start and no comment may name any test, so
    the check runs only the plan's tests and runs them on main, not on the branch. Then the plan also names a test that
    passes on main: the worker must not start, so the plan's tests really are run before the worker."""
    record_property("proves", "81.1")
    r = WorkerRun(tmp_path / "red", [RED, RED_TOO])
    assert r.agent_started(), (f"81.1: the worker did not start though every plan test fails an assert on main; it stopped "
                               f"at '{r.failed_step}':\n{r.tail()}")
    stops = r.stopped_records()
    assert stops == [], f"81.1: a stop was posted though every plan test is red on main:\n{stops[0][1][:800]}"
    for p in r.posted():
        for test in [RED, RED_TOO] + UNLISTED:
            assert test not in p["body"], f"81.1: a comment names {test}, which needs no word from the check:\n{p['body'][:800]}"

    r = WorkerRun(tmp_path / "green", [RED, GREEN])
    assert not r.agent_started(), ("81.1: the worker started though a plan test already passes on main: the plan's tests "
                                   "were not run on main before the worker")


def test_a_test_that_already_passes_on_main_is_named_and_stops_the_worker(record_property, tmp_path):
    """A plan test that already passes on main is named on the issue as "proves nothing yet", and the worker does not start.

    The plan names one test that fails an assert on main and two, in two files, that already pass there. The worker
    must not start, one comment on the issue must name each passing test as path::test with the words "proves nothing
    yet" (and not call it broken), the test that fails correctly must not be named, and the run must end failed."""
    record_property("proves", "81.2")
    r = WorkerRun(tmp_path / "green", [RED, GREEN, ALSO_GREEN])
    body = one_stop_on_the_issue(r, "81.2")
    for test in (GREEN, ALSO_GREEN):
        said = says(body, test)
        assert "proves nothing yet" in said, f"81.2: {test} passes on main but is not named as \"proves nothing yet\":\n{body[:1200]}"
        assert "broken" not in said.lower(), f"81.2: {test} passes on main but is called broken: {said}"
    assert RED not in body.split("<details>")[0], f"81.2: {RED} fails correctly on main but is named:\n{body[:1200]}"


def test_a_test_that_crashes_on_main_is_named_as_broken_and_stops_the_worker(record_property, tmp_path):
    """A plan test that crashes on main, in its body, its setup or its file's import, is named on the issue as broken.

    The plan names a test that fails an assert, one that raises a KeyError in its body, one whose fixture raises, one
    in a file that cannot be imported, and one that already passes. The worker must not start, and one comment on the
    issue must name each crashing test as path::test with the word "broken" (never "proves nothing yet"), name the
    passing test as "proves nothing yet" beside them, leave the correctly failing test unnamed, and end the run failed."""
    record_property("proves", "81.3")
    r = WorkerRun(tmp_path / "crash", [RED, CRASH, SETUP_CRASH, GONE, GREEN])
    body = one_stop_on_the_issue(r, "81.3")
    for test in (CRASH, SETUP_CRASH, GONE):
        said = says(body, test)
        assert "broken" in said.lower(), f"81.3: {test} crashes on main but is not named as broken:\n{body[:1200]}"
        assert "proves nothing yet" not in said, f"81.3: {test} crashes on main but is called a passing test: {said}"
    said = says(body, GREEN)
    assert "proves nothing yet" in said and "broken" not in said.lower(), \
        f"81.3: the passing test is not named as \"proves nothing yet\" beside the broken ones: {said!r}"
    assert RED not in body.split("<details>")[0], f"81.3: {RED} fails correctly on main but is named:\n{body[:1200]}"


def test_a_plan_test_that_does_not_run_on_main_is_named_not_waved_through(record_property, tmp_path):
    """A plan test that cannot be found, or is skipped, on main is named on the issue and the worker does not start.

    The plan names a test that fails an assert, one that does not exist in its file, and one that skips itself. Neither
    failed an assert, so neither proves anything: one comment on the issue must name both, the correctly failing test
    must stay unnamed, the worker must not start and the run must end failed."""
    record_property("proves", "81.4")
    r = WorkerRun(tmp_path / "gone", [RED, MISSING, SKIPPED])
    body = one_stop_on_the_issue(r, "81.4")
    for test in (MISSING, SKIPPED):
        assert says(body, test), f"81.4: {test} did not fail an assert on main but is not named:\n{body[:1200]}"
    assert RED not in body.split("<details>")[0], f"81.4: {RED} fails correctly on main but is named:\n{body[:1200]}"
