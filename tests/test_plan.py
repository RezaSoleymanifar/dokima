import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card, plan  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OWNER = "the-approver"
APPROVERS = {OWNER}


def read(path):
    return open(os.path.join(ROOT, path)).read()


def test_only_an_approvers_approval_on_a_fresh_worker_pr_starts_the_build(record_property):
    record_property("proves", "46.1")
    assert plan.starts_build("approved", OWNER, APPROVERS, "work/issue-44", 1)
    assert not plan.starts_build("approved", "some-app[bot]", APPROVERS, "work/issue-44", 1)
    assert not plan.starts_build("approved", "someone-else", APPROVERS, "work/issue-44", 1)
    assert not plan.starts_build("commented", OWNER, APPROVERS, "work/issue-44", 1)
    assert not plan.starts_build("changes_requested", OWNER, APPROVERS, "work/issue-44", 1)
    # Once work exists, an approval is for merging and starts nothing.
    assert not plan.starts_build("approved", OWNER, APPROVERS, "work/issue-44", 2)
    assert not plan.starts_build("approved", OWNER, APPROVERS, "some-branch", 1)


def test_approvers_are_the_code_owners_else_the_repo_owner(record_property):
    record_property("proves", "46.1")
    assert plan.approvers("# owners\n* @alice @bob  # both\n/docs/ @carol\n", "repo-owner") == {"alice", "bob"}
    assert plan.approvers("", "repo-owner") == {"repo-owner"}
    assert plan.approvers("/docs/ @carol\n", "repo-owner") == {"repo-owner"}


def test_build_runs_on_his_review_and_decides_with_mains_code(record_property):
    record_property("proves", "46.1")
    text = read(".github/workflows/build.yml")
    assert "pull_request_review:" in text and "types: [submitted]" in text
    assert "python3 -m dokima.plan starts" in text
    assert "ref: main" in text
    assert "steps.decide.outputs.start == 'true'" in text


def test_only_an_approvers_approval_marks_the_plan_approved(record_property):
    record_property("proves", "46.1")
    reviews = [
        {"user": {"login": "some-app[bot]"}, "state": "APPROVED", "submitted_at": "2026-10-03T10:00:00Z"},
        {"user": {"login": OWNER}, "state": "COMMENTED", "submitted_at": "2026-10-03T11:00:00Z"},
        {"user": {"login": OWNER}, "state": "DISMISSED", "submitted_at": "2026-10-03T12:00:00Z"},
        {"user": {"login": OWNER}, "state": "APPROVED", "submitted_at": "2026-10-03T15:00:00Z"},
    ]
    assert plan.approved_at(reviews, APPROVERS) == "2026-10-03T15:00:00Z"
    assert plan.approved_at(reviews[:2], APPROVERS) is None


EDITS = [  # GitHub lists each version's full text; the oldest is the original.
    {"editedAt": "2026-10-03T13:00:00Z", "diff": "v3: moved a done-when to Not checked", "editor": {"login": "some-app[bot]"}},
    {"editedAt": "2026-10-03T11:00:00Z", "diff": "v2: the approved plan", "editor": {"login": OWNER}},
    {"editedAt": "2026-10-03T10:00:00Z", "diff": "v1: first draft", "editor": {"login": OWNER}},
]


def test_the_plan_is_read_as_it_was_when_approved(record_property):
    record_property("proves", "46.2")
    at = "2026-10-03T12:00:00Z"
    assert plan.approved_version("v3: moved a done-when to Not checked", EDITS, at) == "v2: the approved plan"
    assert plan.approved_version("current", [], at) == "current"
    assert plan.approved_version("current", EDITS, None) == "current"
    assert plan.edits_after(EDITS, at) == [{"at": "2026-10-03T13:00:00Z", "by": "some-app[bot]"}]
    assert plan.edits_after(EDITS, None) == []


def test_the_card_lists_ignored_edits_and_the_gate_reads_the_approved_plan(record_property):
    record_property("proves", "46.2")
    issue = {"number": 44, "title": "T", "url": "https://github.com/o/r/issues/44",
             "body": "- [ ] Goal: g\n  - [ ] Done when: d\n    Verified by: v\n",
             "edited_after": [{"at": "2026-10-03T13:00:00Z", "by": "some-app[bot]"}]}
    body = card.render("o/r", 45, issue, [], None)
    assert "**Edited after approval (ignored):** 2026-10-03 13:00 UTC by some-app[bot]" in body
    assert "plan.approved_issue(repo, pr)" in read("dokima/checks.py")
    assert "/tmp/issue.md" in read(".github/workflows/build.yml")


def test_the_card_waits_for_an_approve_on_the_pr_page(record_property):
    record_property("proves", "46.2")
    files = "https://github.com/o/r/pull/45/files"
    waiting = card.pipeline_state("o/r", 45, "work/issue-44", None, None, False, 1)
    assert waiting == {"status": "waiting", "html_url": files}
    assert card.pipeline_state("o/r", 45, "work/issue-44", None, None, True, 1) is None
    assert card.pipeline_state("o/r", 45, "issue-40-app", None, None, False, 1) is None
    building = {"status": "in_progress", "html_url": "https://github.com/o/r/actions/runs/9"}
    assert card.pipeline_state("o/r", 45, "work/issue-44", None, building, True, 1) == building


def test_the_old_run_page_approval_is_gone(record_property):
    record_property("proves", "46.3")
    for name in ("worker.yml", "build.yml"):
        text = read(f".github/workflows/{name}")
        assert "environment:" not in text
    assert "approve:" not in read(".github/workflows/worker.yml")


def test_build_is_one_job_whose_first_step_decides(record_property):
    record_property("proves", "65.6")
    text = read(".github/workflows/build.yml")
    jobs = text[text.index("jobs:"):]
    assert jobs.count("\n  build:") == 1 and "\n  decide:" not in jobs
    steps = jobs.split("\n      - ")
    assert "ref: main" in steps[1] and "id: decide" in steps[2]
    assert "rm -rf _main" in steps[2]
    assert all("if: steps.decide.outputs.start == 'true'" in step for step in steps[3:])
def test_a_later_approval_adopts_the_newer_plan(record_property):
    record_property("proves", "63.1")
    first = [{"user": {"login": OWNER}, "state": "DISMISSED", "submitted_at": "2026-10-03T12:00:00Z"}]
    again = first + [{"user": {"login": OWNER}, "state": "APPROVED", "submitted_at": "2026-10-03T14:00:00Z"}]
    at = plan.approved_at(first, APPROVERS)
    assert plan.approved_version("v3", EDITS, at) == "v2: the approved plan"
    assert plan.edits_after(EDITS, at) == [{"at": "2026-10-03T13:00:00Z", "by": "some-app[bot]"}]
    at = plan.approved_at(again, APPROVERS)
    assert plan.approved_version("v3", EDITS, at) == "v3: moved a done-when to Not checked"
    assert plan.edits_after(EDITS, at) == []


def test_done_whens_are_rechecked_after_a_review(record_property):
    record_property("proves", "63.2")
    text = read(".github/workflows/done-whens.yml")
    assert "pull_request_review:" in text and "types: [submitted]" in text
