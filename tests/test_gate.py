import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import gate  # noqa: E402

WORKER = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "worker.yml")).read()


def job(name):
    start = WORKER.index(f"\n  {name}:")
    rest = WORKER[start + 1:]
    nxt = [i for i in (rest.find("\n  push-workflow-changes:"), rest.find("\n  workflow-change-stopped:"), rest.find("\n  work:")) if i > 0]
    return rest[:min(nxt)] if nxt else rest


# 113.1: a build that touches workflows pauses for the owner's approval and says so

def test_only_workflow_files_count(record_property):
    record_property("proves", "113.1")
    assert gate.workflow_files(["dokima/x.py", ".github/workflows/worker.yml", "tests/t.py", ".github/CODEOWNERS"]) == [".github/workflows/worker.yml"]
    assert gate.workflow_files(["dokima/x.py"]) == []


def test_changed_files_are_read_from_git(record_property, tmp_path, monkeypatch):
    record_property("proves", "113.1")
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout
    git("init", "-q"); git("config", "user.name", "t"); git("config", "user.email", "t@t")
    (tmp_path / "a.py").write_text("x"); git("add", "-A"); git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD").strip()
    (tmp_path / ".github/workflows").mkdir(parents=True); (tmp_path / ".github/workflows/w.yml").write_text("on: push")
    (tmp_path / "b.py").write_text("y"); git("add", "-A"); git("commit", "-qm", "build")
    monkeypatch.chdir(tmp_path)
    assert gate.workflow_files(gate.changed_since(base)) == [".github/workflows/w.yml"]


def test_the_issue_is_told_what_waits_and_where_to_approve(record_property):
    record_property("proves", "113.1")
    body = gate.waiting([".github/workflows/worker.yml"], "https://github.com/o/r/actions/runs/1")
    assert body.startswith("**Waiting for your approval:**") and "`.github/workflows/worker.yml`" in body
    assert "https://github.com/o/r/actions/runs/1" in body and "Nothing is pushed until you do" in body


def test_the_push_job_waits_behind_the_owners_approval(record_property):
    record_property("proves", "113.1")
    push = job("push-workflow-changes")
    assert "environment: workflow-changes" in push, "113.1: the workflow push is not behind an approval"
    assert "if: needs.work.outputs.workflows == 'true'" in push


# 113.2: the key that can push workflows lives only behind the approval; normal builds don't pause

def test_the_workflow_key_is_used_only_in_the_approved_job(record_property):
    record_property("proves", "113.2")
    assert WORKER.count("DOKIMA_WORKFLOW_TOKEN") == 1 and "DOKIMA_WORKFLOW_TOKEN" in job("push-workflow-changes")
    assert "DOKIMA_WORKFLOW_TOKEN" not in job("work"), "113.2: the build job can reach the workflow key"


def test_a_build_without_workflow_changes_pushes_as_before(record_property):
    record_property("proves", "113.2")
    work = job("work")
    normal = work[work.index("- name: Push and open the pull request"):]
    assert "steps.gate.outputs.workflows == 'false'" in normal.split("\n")[1], "113.2: the normal push is gated on the wrong condition"
    hand = work[work.index("- name: Hand the build to the approval step"):]
    assert "git push" not in hand.split("- name:")[1], "113.2: the bot pushes a workflow change"


# 113.3: rejected or expired approval pushes nothing and says so

def test_a_rejection_posts_that_nothing_was_pushed(record_property):
    record_property("proves", "113.3")
    stop = job("workflow-change-stopped")
    assert "needs.push-workflow-changes.result != 'success'" in stop and "always()" in stop
    assert "dokima.gate stopped" in stop and "git push" not in stop
    assert gate.stopped("https://r").startswith("**Workflow change not pushed:**")
