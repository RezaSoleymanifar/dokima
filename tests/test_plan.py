import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import plan  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OWNER = "the-approver"
APPROVERS = {OWNER}


def read(path):
    return open(os.path.join(ROOT, path)).read()


def label(event, by, at, name="work"):
    return {"event": event, "label": {"name": name}, "actor": {"login": by}, "created_at": at}


def test_a_code_owners_work_label_approves_and_starts_the_worker(record_property):
    record_property("proves", "67.1")
    text = read(".github/workflows/worker.yml")
    assert "types: [labeled, unlabeled]" in text
    assert "if: github.event.action == 'labeled' && github.event.label.name == 'work'" in text
    assert 'python3 -m dokima.plan approvers | tr \',\' \'\\n\' | grep -qx "$SENDER"' in text
    assert "SENDER: ${{ github.event.sender.login }}" in text
    assert "claude -p" in text and "gh pr create" in text
    assert plan.approvers("# owners\n* @alice @bob  # both\n/docs/ @carol\n", "repo-owner") == {"alice", "bob"}
    assert plan.approvers("", "repo-owner") == {"repo-owner"}
    events = [label("labeled", "some-app[bot]", "2026-10-04T10:00:00Z")]
    assert plan.approved_at(events, APPROVERS) is None


EDITS = [  # GitHub lists each version's full text; the oldest is the original.
    {"editedAt": "2026-10-04T13:00:00Z", "diff": "v3: edited while labeled"},
    {"editedAt": "2026-10-04T11:00:00Z", "diff": "v2: the approved plan"},
    {"editedAt": "2026-10-04T10:00:00Z", "diff": "v1: first draft"},
]


def test_the_plan_is_frozen_when_the_label_is_added(record_property):
    record_property("proves", "67.2")
    first = [label("labeled", OWNER, "2026-10-04T12:00:00Z")]
    at = plan.approved_at(first, APPROVERS)
    assert at == "2026-10-04T12:00:00Z"
    assert plan.approved_version("v3: edited while labeled", EDITS, at) == "v2: the approved plan"
    removed = first + [label("unlabeled", OWNER, "2026-10-04T13:30:00Z")]
    assert plan.approved_at(removed, APPROVERS) is None
    again = removed + [label("labeled", OWNER, "2026-10-04T14:00:00Z")]
    assert plan.approved_version("v3: edited while labeled", EDITS, plan.approved_at(again, APPROVERS)) == "v3: edited while labeled"
    worker = read(".github/workflows/worker.yml")
    assert 'git ls-remote --exit-code --heads origin "work/issue-$N"' in worker
    assert 'git checkout -q -B "work/issue-$N" FETCH_HEAD' in worker


def test_removing_work_stops_a_running_build(record_property):
    record_property("proves", "67.4")
    text = read(".github/workflows/worker.yml")
    assert "group: work-${{ github.event.issue.number }}-${{ github.event.label.name }}" in text
    assert "cancel-in-progress: true" in text


def test_approve_only_means_merge(record_property):
    record_property("proves", "67.5")
    workflows = os.path.join(ROOT, ".github", "workflows")
    assert not os.path.exists(os.path.join(workflows, "build.yml"))
    import test_review_relay as trr
    relays = trr.review_relays()
    for name in os.listdir(workflows):
        if name == "board.yml":  # only moves board cards on a review; it never starts a build
            continue
        if name in relays:  # only tells board.yml a review came (#396); it starts nothing
            text = read(f".github/workflows/{name}")
            assert "uses: ./" not in text and "workflow run" not in text and "workflow_dispatch" not in text
            continue
        if name == "commands.yml":  # a review's command starts a stage, but never an Approve
            assert "github.event.review.state != 'approved'" in read(f".github/workflows/{name}")
            continue
        assert "pull_request_review" not in read(f".github/workflows/{name}")
    assert ".dokima/plans" not in read(".github/workflows/worker.yml")
    assert "Approve the plan" not in read("dokima/card.py")
    assert not hasattr(plan, "starts_build")


def test_card_and_checkbox_formats_read_the_same_plan(record_property):
    record_property("proves", "67.8")
    body = ("- [ ] Goal: g\n  - [ ] Done when: c one\n    Verified by: v one\n"
            "  - [ ] Criterion: c two\n    Verified by: v two\n\n**Not checked:** n\n\nA note.\n")
    words = plan.parse(body)
    assert [c["text"] for c in words["goals"][0]["criteria"]] == ["c one", "c two"]
    assert words["goals"][0]["text"] == "g" and words["not_checked"] == "n" and words["notes"] == "A note."
