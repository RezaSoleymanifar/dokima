import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card  # noqa: E402

REPO = "o/r"
ISSUE = {"number": 40, "title": "T", "url": "https://github.com/o/r/issues/40",
         "body": ("- [ ] Goal: show a card\n"
                  "  - [ ] Done when: first thing works\n"
                  "    Verified by: a test\n"
                  "  - [ ] Done when: second thing works\n"
                  "    Verified by: another test\n\n"
                  "**Not checked:** speed.\n")}
WAITING = {"status": "waiting", "html_url": "https://github.com/o/r/actions/runs/1"}
BUILDING = {"status": "in_progress", "html_url": "https://github.com/o/r/actions/runs/1"}
DONE = {"status": "completed", "html_url": "https://github.com/o/r/actions/runs/1"}


def run(name, status="completed", conclusion="success", n=7):
    return {"name": name, "status": status, "conclusion": conclusion,
            "html_url": f"https://github.com/o/r/actions/runs/2/job/{n}"}


GREEN = [run("40.1 · first thing works", n=1), run("40.2 · second thing works", n=2), run("all tests", n=3)]


def title(body):
    return body.splitlines()[1]


def links(body):
    return body.splitlines()[2]


def test_title_shows_pr_and_each_stage(record_property):
    record_property("proves", "29.5")
    assert title(card.render(REPO, 5, ISSUE, GREEN, WAITING)) == "### PR #5 · Waiting for your approval"
    assert title(card.render(REPO, 5, ISSUE, GREEN, BUILDING)) == "### PR #5 · Building"
    running = GREEN[:1] + [run("40.2 · second thing works", status="in_progress", conclusion=None)] + GREEN[2:]
    assert title(card.render(REPO, 5, ISSUE, running, DONE)) == "### PR #5 · Checking"
    failing = GREEN[:1] + [run("40.2 · second thing works", conclusion="failure")] + GREEN[2:]
    assert title(card.render(REPO, 5, ISSUE, failing, DONE)) == "### PR #5 · Checks failing"
    assert title(card.render(REPO, 5, ISSUE, GREEN, DONE)) == "### PR #5 · Ready to merge"


def test_approve_link_only_while_waiting(record_property):
    record_property("proves", "29.6")
    assert f"[Approve]({WAITING['html_url']})" in links(card.render(REPO, 5, ISSUE, GREEN, WAITING))
    for worker in (BUILDING, DONE, None):
        assert "Approve" not in card.render(REPO, 5, ISSUE, GREEN, worker)


def test_live_run_points_to_what_is_running_now(record_property):
    record_property("proves", "29.7")
    assert f"[live run]({BUILDING['html_url']})" in links(card.render(REPO, 5, ISSUE, GREEN, BUILDING))
    running = [run("40.1 · first thing works", status="in_progress", conclusion=None, n=9)]
    assert "[live run](https://github.com/o/r/actions/runs/2/job/9)" in links(card.render(REPO, 5, ISSUE, running, DONE))
    assert "live run" not in card.render(REPO, 5, ISSUE, GREEN, DONE)


def test_one_row_of_links(record_property):
    record_property("proves", "29.8")
    row = links(card.render(REPO, 5, ISSUE, GREEN, WAITING))
    assert row == (f"[Approve]({WAITING['html_url']}) · [live run]({WAITING['html_url']}) · "
                   "[issue #40](https://github.com/o/r/issues/40) · [files changed](https://github.com/o/r/pull/5/files)")


def test_each_done_when_shows_githubs_verdict_from_its_own_check(record_property):
    record_property("proves", "29.9")
    checks = [run("40.1 · first thing works", n=1), run("40.2 · second thing works", conclusion="failure", n=2),
              run("all tests", n=3)]
    body = card.render(REPO, 5, ISSUE, checks, DONE)
    assert "- ✅ **Done when:** first thing works · [proof](https://github.com/o/r/actions/runs/2/job/1)" in body
    assert "- ❌ **Done when:** second thing works · [proof](https://github.com/o/r/actions/runs/2/job/2)" in body
    assert "  **Verified by:** a test" in body
    assert "**Full suite:** ✅ [proof](https://github.com/o/r/actions/runs/2/job/3)" in body
    assert "**Not checked:** speed." in body


def test_running_or_missing_checks_never_show_a_pass(record_property):
    record_property("proves", "29.9")
    assert card.verdict(None) == ("⚠️", "no check yet")
    assert card.verdict(run("x", status="in_progress", conclusion=None))[0] == "⏳"
    body = card.render(REPO, 5, ISSUE, [run("40.1 · first thing works")], DONE)
    assert "- ⚠️ **Done when:** second thing works · no check yet" in body
    assert "**Full suite:** ⚠️ no check yet" in body


def test_card_without_issue_says_so():
    assert "No linked issue" in card.render(REPO, 5, None, [], None)
