"""Workflow changes wait for the owner's approval (#113)."""
import os
import re
import stat
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
KEY = "DOKIMA_WORKFLOWS_KEY"
ENV = "workflows"


def git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def make_repo(tmp_path, files):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "user.email", "t@example.com")
    (repo / "README.md").write_text("hi\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")
    base = git(repo, "rev-parse", "HEAD")
    for path, text in files.items():
        p = repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "work", "--allow-empty")
    return repo, base


def run_gate(tmp_path, repo, *args, extra_env=None):
    out, summary = tmp_path / "out.txt", tmp_path / "summary.md"
    out.write_text("")
    summary.write_text("")
    env = dict(os.environ, GITHUB_OUTPUT=str(out), GITHUB_STEP_SUMMARY=str(summary),
               PYTHONPATH=os.path.abspath(ROOT), GITHUB_REPOSITORY="o/r", **(extra_env or {}))
    r = subprocess.run([sys.executable, "-m", "dokima.gate", *args], cwd=repo, env=env,
                       capture_output=True, text=True)
    return r, out.read_text(), summary.read_text()


def test_workflow_change_is_flagged_and_shown(tmp_path, record_property):
    record_property("proves", "113.1")
    repo, base = make_repo(tmp_path, {".github/workflows/x.yml": "name: brand-new-flow\n", "a.py": "x=1\n"})
    r, out, summary = run_gate(tmp_path, repo, "check", base)
    assert r.returncode == 0, f"113.1: gate check crashed: {r.stderr[-300:]}"
    assert "workflows=true" in out.split(), f"113.1: workflow change not flagged in GITHUB_OUTPUT: {out!r}"
    assert "x.yml" in summary and "brand-new-flow" in summary, \
        "113.1: the run summary does not show the workflow file and its change"


def test_workflow_deletion_and_edit_are_flagged(tmp_path, record_property):
    record_property("proves", "113.1")
    repo, base = make_repo(tmp_path, {".github/workflows/y.yml": "a: 1\n"})
    base2 = git(repo, "rev-parse", "HEAD")
    (repo / ".github/workflows/y.yml").write_text("a: 2\n")
    git(repo, "commit", "-qam", "edit")
    r, out, _ = run_gate(tmp_path, repo, "check", base2)
    assert "workflows=true" in out.split(), "113.1: an edit of an existing workflow was not flagged"


def test_no_workflow_change_means_no_pause(tmp_path, record_property):
    record_property("proves", "113.2")
    repo, base = make_repo(tmp_path, {"a.py": "x=1\n", "docs/github/workflows/z.yml": "n: 1\n"})
    r, out, summary = run_gate(tmp_path, repo, "check", base)
    assert r.returncode == 0, f"113.2: gate check crashed: {r.stderr[-300:]}"
    assert "workflows=false" in out.split(), f"113.2: expected workflows=false, got {out!r}"
    assert summary.strip() == "", "113.2: summary should be empty when no workflow changed"


def jobs(path):
    """Split a workflow file into {job name: text} by its 2-space-indented keys under `jobs:`."""
    text = open(os.path.join(ROOT, ".github/workflows", path)).read()
    body = text.split("\njobs:\n", 1)[1]
    parts = re.split(r"(?m)^  ([A-Za-z0-9_-]+):\s*$", body)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def check_gated(path):
    js = jobs(path)
    gated = {n: t for n, t in js.items() if re.search(rf"(?m)^    environment:\s*{ENV}\s*$", t)}
    assert len(gated) == 1, f"{path}: expected exactly one job with `environment: {ENV}`, found {list(gated)}"
    return js, next(iter(gated))


def test_key_lives_only_in_the_approval_environment_job(record_property):
    record_property("proves", "113.2")
    for path in ("worker.yml", "planner.yml"):
        js, name = check_gated(path)
        for n, t in js.items():
            if n != name:
                assert f"secrets.{KEY}" not in t, f"113.2: {path}: job {n} uses {KEY} outside the environment"
        assert f"secrets.{KEY}" in js[name], f"113.2: {path}: the gated job never uses {KEY}"
        assert re.search(r"(?m)^    needs:", js[name]), f"113.2: {path}: gated job does not wait for the build job"
        assert "workflows == 'true'" in js[name] or 'workflows == "true"' in js[name], \
            f"113.2: {path}: gated job is not limited to runs that changed workflows"
        assert "git push" in js[name], f"113.2: {path}: the gated job does not push"


def test_ordinary_push_is_not_gated(record_property):
    record_property("proves", "113.2")
    for path in ("worker.yml", "planner.yml"):
        js, name = check_gated(path)
        plain = [n for n, t in js.items() if n != name and "git push" in t]
        assert plain, f"113.2: {path}: no ungated job pushes runs without workflow changes"
        for n in plain:
            assert "workflows == 'false'" in js[n] or 'workflows == "false"' in js[n] \
                or "workflows != 'true'" in js[n], f"113.2: {path}: job {n} is not limited to runs with no workflow change"
            assert "environment" not in js[n], f"113.2: {path}: ordinary push job {n} is gated"
        assert "dokima.gate check" in "".join(js.values()), f"113.2: {path}: the build never runs the gate check"


def test_declined_posts_a_comment_and_pushes_nothing(tmp_path, record_property):
    record_property("proves", "113.3")
    repo, _ = make_repo(tmp_path, {})
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "gh.log"
    gh = bindir / "gh"
    gh.write_text(f'#!/bin/sh\necho "$@" >> {log}\ncat >/dev/null 2>&1 </dev/null\n')
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    pushlog = tmp_path / "git.log"
    git_shim = bindir / "git"
    real = subprocess.run(["which", "git"], capture_output=True, text=True).stdout.strip()
    git_shim.write_text(f'#!/bin/sh\necho "$@" >> {pushlog}\nexec {real} "$@"\n')
    git_shim.chmod(git_shim.stat().st_mode | stat.S_IEXEC)
    env = {"PATH": f"{bindir}:{os.environ['PATH']}", "GH_TOKEN": "x"}
    r, _, _ = run_gate(tmp_path, repo, "declined", "113", extra_env=env)
    assert r.returncode == 0, f"113.3: gate declined crashed: {r.stderr[-300:]}"
    calls = log.read_text() if log.exists() else ""
    assert "issue comment 113" in calls, f"113.3: no comment posted on the issue; gh calls: {calls!r}"
    assert "workflow" in calls.lower() and ("not pushed" in calls.lower() or "nothing was pushed" in calls.lower()), \
        f"113.3: the comment does not say the workflow change was not pushed: {calls!r}"
    assert "push" not in (pushlog.read_text() if pushlog.exists() else "").split(), "113.3: declined must not push"


def test_workflows_post_a_comment_when_approval_is_not_given(record_property):
    record_property("proves", "113.3")
    for path in ("worker.yml", "planner.yml"):
        js, name = check_gated(path)
        decliners = [t for n, t in js.items() if "dokima.gate declined" in t]
        assert decliners, f"113.3: {path}: nothing posts the comment when approval is rejected or expires"
        for t in decliners:
            assert f"needs.{name}.result" in t, f"113.3: {path}: the comment is not tied to the approval's result"
            assert "always()" in t, f"113.3: {path}: the comment job would be skipped when approval fails"
            assert "git push" not in t and "secrets." + KEY not in t, f"113.3: {path}: comment job must not push"
