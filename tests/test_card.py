import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card  # noqa: E402

LATEST = "abc1234"
RUN = {"url": "https://github.com/o/r/actions/runs/1/job/2", "sha": LATEST}
ISSUE = {"number": 8, "title": "Card"}
BODY = ("- [ ] Goal: show a card\n"
        "  - [ ] Done when: it appears\n"
        "    Verified by: reading it\n"
        "  - [ ] Done when: it is honest\n"
        "    Verified by: these tests\n")


def link(result):
    return f"https://proof/{result['name']}"


def result(status, proves="8.2"):
    return {"file": "tests/t.py", "name": "t", "status": status, "proves": [proves]}


def test_issue_parses_goals_done_whens_and_how_verified():
    goals = card.parse_issue(BODY)
    assert goals[0]["text"] == "Goal: show a card"
    assert [(d["n"], d["text"], d["verified_by"]) for d in goals[0]["done_whens"]] == [
        (1, "it appears", "reading it"), (2, "it is honest", "these tests")]


def test_junit_reads_status_and_which_done_when_it_proves():
    xml = ('<testsuites><testsuite><testcase file="tests/t.py" name="t_ok"><properties>'
           '<property name="proves" value="8.3"/></properties></testcase>'
           '<testcase file="tests/t.py" name="t_bad"><failure/></testcase></testsuite></testsuites>')
    assert [(r["name"], r["status"], r["proves"]) for r in card.parse_junit(xml)] == [
        ("t_ok", "passed", ["8.3"]), ("t_bad", "failed", [])]


def test_recorded_pass_on_latest_commit_shows_check_with_built_proof_link(record_property):
    record_property("proves", "8.3")
    assert card.verdict(8, 2, [result("passed")], RUN, LATEST, link) == ("✅", "[proof](https://proof/t)")


def test_pass_with_no_recorded_run_is_not_a_check(record_property):
    record_property("proves", "8.3")
    icon, text = card.verdict(8, 2, [result("passed")], None, LATEST, link)
    assert icon == "⚠️" and "no recorded run" in text


def test_pass_from_an_older_commit_is_not_a_check(record_property):
    record_property("proves", "8.3")
    icon, text = card.verdict(8, 2, [result("passed")], {"url": RUN["url"], "sha": "old0000"}, LATEST, link)
    assert icon == "⚠️" and "older commit" in text


def test_failure_shows_cross_with_proof(record_property):
    record_property("proves", "8.3")
    assert card.verdict(8, 2, [result("passed"), result("failed")], RUN, LATEST, link)[0] == "❌"


def test_done_when_without_a_test_is_not_a_check(record_property):
    record_property("proves", "8.3")
    icon, text = card.verdict(8, 1, [result("passed")], RUN, LATEST, link)
    assert icon == "⚠️" and "no test verifies" in text


def test_card_shape_pr_goal_done_when_verified_by():
    body = card.render(12, ISSUE, card.parse_issue(BODY), [result("passed")], RUN, LATEST, link)
    assert body.startswith(card.MARKER)
    assert f"### PR #12 · [live run]({RUN['url']})" in body
    assert "**Goal: show a card**" in body
    assert "- ✅ **Done when:** it is honest · [proof](https://proof/t)" in body
    assert "  **Verified by:** these tests" in body
    assert "- ⚠️ **Done when:** it appears" in body


def test_card_without_issue_says_so():
    assert "No linked issue" in card.render(3, None, [], [], RUN, LATEST, link)


def test_proof_link_lands_on_the_pytest_line():
    job = {"html_url": "https://job", "steps": [{"number": 5, "name": "Run pytest -q"}]}
    log = "2026Z ##[group]Run pytest -q\n2026Z x\n2026Z PASSED tests/t.py::t\n"
    links = card.step_line_links(job, log, [result("passed")])
    assert links["tests/t.py::t"] == "https://job#step:5:3"


def test_proof_link_skips_the_step_that_only_installs_pytest():
    job = {"html_url": "https://job", "steps": [{"number": 4, "name": "Run pip install pytest"},
                                                {"number": 5, "name": "Run pytest -q"}]}
    log = "2026Z ##[group]Run pip install pytest\n2026Z ##[group]Run pytest -q\n2026Z PASSED tests/t.py::t\n"
    assert card.step_line_links(job, log, [result("passed")])["tests/t.py::t"] == "https://job#step:5:2"


def test_proof_link_falls_back_to_the_test_step_without_a_log():
    job = {"html_url": "https://job", "steps": [{"number": 5, "name": "Run pytest -q"}]}
    assert card.step_line_links(job, "", [result("passed")])["tests/t.py::t"] == "https://job#step:5"
