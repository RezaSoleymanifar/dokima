import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card, plan  # noqa: E402

REPO = "o/r"
BODY = ("- [ ] Goal: show a card\n"
        "  - [ ] Done when: first thing works\n"
        "    Verified by: a test that runs the first thing\n"
        "  - [ ] Done when: second thing works\n"
        "    Verified by: another test\n\n"
        "**Not checked:** speed.\n\n"
        "Requested in chat.\n")
ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40", "approved_at": "2026-10-04T10:00:00Z", "changes": []}
PR = {"number": 5, "merged": False, "state": "open"}
WORDS = plan.parse(BODY)
DONE = {"status": "completed", "conclusion": "success", "html_url": "https://github.com/o/r/actions/runs/1"}
BUILDING = {"status": "in_progress", "conclusion": None, "html_url": "https://github.com/o/r/actions/runs/1"}


def run(name, status="completed", conclusion="success", n=7):
    return {"name": name, "status": status, "conclusion": conclusion,
            "html_url": f"https://github.com/o/r/actions/runs/2/job/{n}"}


GREEN = [run("40.1 · first thing works", n=1), run("40.2 · second thing works", n=2), run("all tests", n=3)]


def render(checks=GREEN, worker=DONE, pr=PR, issue=ISSUE, words=WORDS):
    return card.render(REPO, issue, words, pr, checks, worker)


def title(body):
    return body.splitlines()[1]


def icon(name):
    return card.icon(REPO, name)


def test_title_shows_each_stage():
    no_label = dict(ISSUE, approved_at=None)
    assert title(render(checks=[], worker=None, pr=None, issue=no_label)) == "### Plan: add `work` to start"
    assert title(render(checks=[], worker=BUILDING, pr=None)) == "### Building"
    running = GREEN[:1] + [run("40.2 · second thing works", status="in_progress", conclusion=None)] + GREEN[2:]
    assert title(render(checks=running)) == "### Checking"
    failing = GREEN[:1] + [run("40.2 · second thing works", conclusion="failure")] + GREEN[2:]
    assert title(render(checks=failing)) == "### Checks failing"
    assert title(render(pr=dict(PR, merged=True))) == "### Merged"


def test_title_asks_for_approval_when_all_checks_passed(record_property):
    record_property("proves", "58.1")
    assert title(render()) == "### Approve the result to merge"


def test_links_row():
    assert render().splitlines()[2] == ("[PR #5](https://github.com/o/r/pull/5)"
                                        " · [files changed](https://github.com/o/r/pull/5/files)")
    assert render(checks=[], worker=BUILDING, pr=None).splitlines()[2].startswith("[live run](https://github.com/o/r/actions/runs/1)")


def test_criteria_sit_in_an_indented_block_and_only_the_word_criteria_links(record_property):
    record_property("proves", "74.1")
    body = render(checks=GREEN[:1] + [run("40.2 · second thing works", conclusion="failure", n=2)] + GREEN[2:])
    lines = body.splitlines()
    start = lines.index("<dl><dd>")
    end = lines.index("</dd></dl>")
    assert f"{icon('passed')} [Criteria](https://github.com/o/r/actions/runs/2/job/1): first thing works" in lines[start:end]
    assert f"{icon('failed')} [Criteria](https://github.com/o/r/actions/runs/2/job/2): second thing works" in lines[start:end]
    assert "[first thing works]" not in body
    empty = render(checks=[], pr=None)
    assert f"{icon('none')} Criteria: first thing works" in empty
    assert f"{icon('passed')} [Full suite](https://github.com/o/r/actions/runs/2/job/3)" in body
    assert not any(line.startswith("- ") for line in lines)
    for name in ("passed", "failed", "running", "none"):
        svg = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "icons", f"{name}.svg")).read()
        assert svg.startswith("<svg fill=")


def test_verified_by_is_italic_normal_size_right_under_its_criterion(record_property):
    record_property("proves", "74.2")
    lines = render().splitlines()
    i = next(n for n, l in enumerate(lines) if l.endswith("Criteria](https://github.com/o/r/actions/runs/2/job/1): first thing works"))
    assert lines[i + 1] == "*Verified by: a test that runs the first thing*"
    assert "<sub>" not in "\n".join(lines)


def test_no_footer_and_no_gap(record_property):
    record_property("proves", "74.3")
    body = render()
    assert "Built by the card workflow" not in body
    lines = body.splitlines()
    for n, line in enumerate(lines):
        if line.startswith("*Verified by:"):
            assert "Criteria" in lines[n - 1] and not lines[n - 1].endswith("<br>")


def test_card_never_links_to_its_own_page(record_property):
    record_property("proves", "74.4")
    on_issue = render().splitlines()[2]
    on_pr = card.render(REPO, ISSUE, WORDS, PR, GREEN, DONE, page="pr").splitlines()[2]
    assert "[issue #40]" not in on_issue and "[PR #5]" in on_issue
    assert "[PR #5]" not in on_pr and "[issue #40]" in on_pr


def test_card_says_criteria_and_is_read_back_as_the_plan(record_property):
    record_property("proves", "74.5")
    body = render()
    assert "Done when" not in body
    assert plan.parse(card.issue_body(body, WORDS["notes"])) == WORDS
    text = plan.as_text(40, "T", WORDS)
    assert "Criterion 40.1: first thing works" in text and "Done when" not in text


def test_same_card_on_issue_and_pr_and_only_icons_change(record_property):
    record_property("proves", "67.6")
    issue_text = card.issue_body(render(checks=[], pr=None), WORDS["notes"])
    later = card.issue_body(render(), WORDS["notes"])
    assert issue_text != later
    assert plan.parse(issue_text) == plan.parse(later) == WORDS
    assert card.pr_body(render(), "Closes #40.\n\nSome prose.") == render() + "\n\nCloses #40"
    src = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "card.py")).read()
    assert 'f"repos/{repo}/issues/{number}", "-F", "body=@issue.md"' in src
    assert 'f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md"' in src
    yml = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "card.yml")).read()
    assert "types: [opened, edited]" in yml and "github.event.sender.type != 'Bot'" in yml


def test_edits_after_approval_are_listed_on_the_card(record_property):
    record_property("proves", "67.3")
    edited = BODY.replace("second thing works", "second thing works well").replace(
        "**Not checked:**", "  - [ ] Done when: third thing works\n    Verified by: a third test\n\n**Not checked:**")
    found = plan.changes(WORDS, plan.parse(edited))
    assert ("Changed", "second thing works", "second thing works well") in found
    assert ("Added", "third thing works") in found
    body = render(issue=dict(ISSUE, changes=found))
    assert "**Edited after approval, not in use yet.** Re-add `work` to use it:<br>" in body
    assert "&emsp;Changed: “second thing works” → “second thing works well”<br>" in body
    assert "&emsp;Added: “third thing works”<br>" in body
    assert "Edited after approval" not in render()
