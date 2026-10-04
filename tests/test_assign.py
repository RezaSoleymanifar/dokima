import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(path):
    return open(os.path.join(ROOT, path)).read()


def test_new_issues_are_assigned_to_the_approvers(record_property):
    record_property("proves", "56.1")
    text = read(".github/workflows/assign.yml")
    assert "issues:" in text and "types: [opened]" in text
    assert '--add-assignee "$(python3 -m dokima.plan approvers)"' in text
    out = subprocess.run([sys.executable, "-m", "dokima.plan", "approvers"], cwd=ROOT, capture_output=True, text=True,
                         check=True, env={**os.environ, "GITHUB_REPOSITORY_OWNER": "fallback-owner"}).stdout.strip()
    assert out and "fallback-owner" not in out.split(",")  # this repo has CODEOWNERS, so it wins


def test_worker_prs_are_assigned_and_review_is_asked_again_after_the_build(record_property):
    record_property("proves", "56.2")
    worker = read(".github/workflows/worker.yml")
    assert 'APPROVERS=$(python3 -m dokima.plan approvers)' in worker
    assert '--assignee "$APPROVERS"' in worker
    build = read(".github/workflows/build.yml")
    ready = build.index('gh pr ready "$BRANCH"')
    assert build.index('--add-reviewer "$(python3 -m dokima.plan approvers)"') > ready
