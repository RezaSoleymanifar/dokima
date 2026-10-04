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
    assert title(card.render(REPO, 5, ISSUE, GREEN, DONE)) == "### PR #5 · Approve the result to merge"


def test_approve_link_only_while_waiting(record_property):
    record_property("proves", "29.6")
    assert f"[Approve the plan]({WAITING['html_url']})" in links(card.render(REPO, 5, ISSUE, GREEN, WAITING))
    for worker in (BUILDING, DONE, None):
        assert "Approve the plan" not in card.render(REPO, 5, ISSUE, GREEN, worker)


def test_live_run_points_to_what_is_running_now(record_property):
    record_property("proves", "29.7")
    assert f"[live run]({BUILDING['html_url']})" in links(card.render(REPO, 5, ISSUE, GREEN, BUILDING))
    running = [run("40.1 · first thing works", status="in_progress", conclusion=None, n=9)]
    assert "[live run](https://github.com/o/r/actions/runs/2/job/9)" in links(card.render(REPO, 5, ISSUE, running, DONE))
    assert "live run" not in card.render(REPO, 5, ISSUE, GREEN, DONE)


def test_one_row_of_links(record_property):
    record_property("proves", "29.8")
    row = links(card.render(REPO, 5, ISSUE, GREEN, WAITING))
    assert row == (f"[Approve the plan]({WAITING['html_url']}) · "
                   "[issue #40](https://github.com/o/r/issues/40) · [files changed](https://github.com/o/r/pull/5/files)")


def icon(name):
    return card.icon(REPO, name)


def test_each_done_when_shows_githubs_verdict_from_its_own_check(record_property):
    record_property("proves", "29.9")
    checks = [run("40.1 · first thing works", n=1), run("40.2 · second thing works", conclusion="failure", n=2),
              run("all tests", n=3)]
    body = card.render(REPO, 5, ISSUE, checks, DONE)
    assert f"{icon('passed')} [Done](https://github.com/o/r/actions/runs/2/job/1): first thing works<br>" in body
    assert f"{icon('failed')} [Failing](https://github.com/o/r/actions/runs/2/job/2): second thing works<br>" in body
    assert "[proof]" not in body
    assert "<sub>Verified by: a test</sub>" in body
    assert f"{icon('passed')} [Full suite](https://github.com/o/r/actions/runs/2/job/3)" in body
    assert "**Not checked:** speed." in body


def test_running_or_missing_checks_never_show_a_pass(record_property):
    record_property("proves", "29.9")
    assert card.state(None) == "none"
    assert card.state(run("x", status="in_progress", conclusion=None)) == "running"
    body = card.render(REPO, 5, ISSUE, [run("40.1 · first thing works")], DONE)
    assert f"{icon('none')} Done when: second thing works · no check yet" in body
    running = card.render(REPO, 5, ISSUE, [run("40.1 · first thing works", status="in_progress", conclusion=None, n=9)], DONE)
    assert f"{icon('running')} [Checking](https://github.com/o/r/actions/runs/2/job/9): first thing works" in running
    assert f"{icon('none')} Full suite · no check yet" in body


def test_card_goes_into_the_pr_description_with_only_the_closes_line(record_property):
    record_property("proves", "65.1")
    assert card.description("CARD", "Closes #63.\n\nSome prose.\n") == "CARD\n\nCloses #63"
    assert card.description("CARD", None) == "CARD"
    src = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "card.py")).read()
    assert 'gh("api", "-X", "PATCH", f"repos/{repo}/pulls/{pr}", "-F", "body=@body.md")' in src


def test_verdicts_use_githubs_circle_icons_centered(record_property):
    record_property("proves", "65.2")
    tag = card.icon("o/r", "passed")
    assert tag == ('<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" '
                   'width="16" height="16" align="absmiddle" alt="passed">')
    root = os.path.join(os.path.dirname(__file__), "..", "dokima", "icons")
    for name in ("passed", "failed", "running", "none"):
        assert open(os.path.join(root, f"{name}.svg")).read().startswith("<svg fill=")
    body = card.render(REPO, 5, ISSUE, GREEN, DONE)
    assert "✅" not in body and "❌" not in body and "⚠️" not in body
    assert not any(line.startswith("- ") for line in body.splitlines())


def test_verified_by_sits_under_its_done_when_in_small_text(record_property):
    record_property("proves", "65.3")
    lines = card.render(REPO, 5, ISSUE, GREEN, DONE).splitlines()
    i = next(n for n, l in enumerate(lines) if "first thing works" in l)
    assert lines[i].endswith("<br>") and lines[i + 1] == "<sub>Verified by: a test</sub>"


def test_full_suite_is_the_link(record_property):
    record_property("proves", "65.4")
    body = card.render(REPO, 5, ISSUE, GREEN, DONE)
    assert f"{icon('passed')} [Full suite](https://github.com/o/r/actions/runs/2/job/3)" in body
    assert "**Full suite:**" not in body


def test_card_without_issue_says_so():
    assert "No linked issue" in card.render(REPO, 5, None, [], None)


def test_waiting_card_says_approve_the_plan_and_has_no_live_run(record_property):
    record_property("proves", "54.2")
    row = links(card.render(REPO, 5, ISSUE, [], WAITING))
    assert row.startswith(f"[Approve the plan]({WAITING['html_url']})")
    assert "live run" not in row


def test_title_asks_for_approval_when_all_checks_passed(record_property):
    record_property("proves", "58.1")
    heading = title(card.render(REPO, 5, ISSUE, GREEN, DONE))
    assert heading == "### PR #5 · Approve the result to merge"
    assert "Ready to merge" not in heading
