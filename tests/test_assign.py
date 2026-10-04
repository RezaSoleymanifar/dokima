import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(path):
    return open(os.path.join(ROOT, path)).read()


def test_worker_prs_are_assigned_and_review_is_asked_again_after_the_build(record_property):
    record_property("proves", "56.1")
    worker = read(".github/workflows/worker.yml")
    assert 'APPROVERS=$(python3 -m dokima.plan approvers)' in worker
    assert '--assignee "$APPROVERS"' in worker
    build = read(".github/workflows/build.yml")
    ready = build.index('gh pr ready "$BRANCH"')
    assert build.index('--add-reviewer "$(python3 -m dokima.plan approvers)"') > ready
