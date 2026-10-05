import json
import os
import subprocess
import sys
import textwrap

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKER = os.path.join(ROOT, ".github/workflows/worker.yml")

FAILS = 'def test_{n}(record_property):\n    record_property("proves", "{k}")\n    assert app.f() == 2, "f is not 2"\n'
PASSES = 'def test_{n}(record_property):\n    record_property("proves", "{k}")\n    assert app.f() == 1\n'
CRASHES = 'def test_{n}(record_property):\n    record_property("proves", "{k}")\n    app.missing_function()\n'
HEAD = "import app\n\n\n"


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd, check=True, capture_output=True)


def make_repo(tmp_path, tests, feature_on_branch=False):
    """A repo whose main has app.f() == 1, and a work/issue-81 branch holding the plan's tests."""
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "app.py").write_text("def f():\n    return 1\n")
    (repo / "conftest.py").write_text("")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "main")
    git(repo, "checkout", "-q", "-b", "work/issue-81")
    for name, text in tests.items():
        (repo / "tests" / name).write_text(text)
    if feature_on_branch:
        (repo / "app.py").write_text("def f():\n    return 2\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "plan tests")
    return repo


def run_red(tmp_path, repo):
    """Run `python3 -m dokima.red 81` in the repo with a fake gh; return (exit code, output, comments)."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    log = tmp_path / "gh.log"
    gh = bin_dir / "gh"
    gh.write_text(textwrap.dedent(f"""\
        #!{sys.executable}
        import json, os, sys
        args = sys.argv[1:]
        text = " ".join(args)
        for a in args:
            if os.path.isfile(a):
                text += " " + open(a).read()
        if "--body-file" in args and args[args.index("--body-file") + 1] == "-":
            text += " " + sys.stdin.read()
        open({str(log)!r}, "a").write(json.dumps(text) + "\\n")
        """))
    gh.chmod(0o755)
    env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", PYTHONPATH=ROOT,
               RED_BASE="main", GITHUB_REPOSITORY="o/r", GH_TOKEN="x")
    r = subprocess.run([sys.executable, "-m", "dokima.red", "81"], cwd=repo, env=env,
                       capture_output=True, text=True, timeout=120)
    comments = [json.loads(l) for l in log.read_text().splitlines()] if log.exists() else []
    return r.returncode, r.stdout + r.stderr, comments


def test_tests_that_fail_an_assert_on_main_let_the_worker_start(record_property, tmp_path):
    record_property("proves", "81.1")
    repo = make_repo(tmp_path, {"test_a.py": HEAD + FAILS.format(n="a", k="81.1") + "\n\n" + FAILS.format(n="b", k="81.2")})
    code, out, comments = run_red(tmp_path, repo)
    assert code == 0, f"81.1: all tests fail an assert on main, yet the red check exited {code}: {out}"
    assert comments == [], f"81.1: nothing should be posted when every test is red: {comments}"


def test_the_tests_run_against_main_not_against_the_branch(record_property, tmp_path):
    record_property("proves", "81.1")
    # The branch already holds the feature (a re-run): the tests pass there, but main is what counts.
    repo = make_repo(tmp_path, {"test_a.py": HEAD + FAILS.format(n="a", k="81.1")}, feature_on_branch=True)
    code, out, comments = run_red(tmp_path, repo)
    assert code == 0, f"81.1: the test fails on main, but the check ran it against the branch's code: {out}"
    assert comments == []


def test_only_tests_that_prove_this_issue_are_run(record_property, tmp_path):
    record_property("proves", "81.1")
    repo = make_repo(tmp_path, {"test_a.py": HEAD + FAILS.format(n="a", k="81.1")
                                + "\n\n" + PASSES.format(n="other", k="12.1") + "\n\n" + CRASHES.format(n="other2", k="12.2")})
    code, out, comments = run_red(tmp_path, repo)
    assert code == 0, f"81.1: tests of other issues must not stop the worker: {out}"


def test_a_test_that_already_passes_on_main_is_named_and_stops_the_worker(record_property, tmp_path):
    record_property("proves", "81.2")
    repo = make_repo(tmp_path, {"test_a.py": HEAD + PASSES.format(n="green", k="81.1") + "\n\n" + FAILS.format(n="red", k="81.2")})
    code, out, comments = run_red(tmp_path, repo)
    assert code != 0, "81.2: a test that passes on main did not stop the worker"
    assert len(comments) == 1, f"81.2: expected one comment on the issue, got {comments}"
    text = comments[0]
    assert "tests/test_a.py::test_green" in text, f"81.2: the passing test is not named: {text}"
    assert "proves nothing yet" in text, f"81.2: the comment does not say 'proves nothing yet': {text}"
    assert "test_red" not in text, f"81.2: a test that fails correctly was blamed: {text}"


def test_a_test_that_crashes_is_named_as_broken_and_stops_the_worker(record_property, tmp_path):
    record_property("proves", "81.3")
    repo = make_repo(tmp_path, {"test_a.py": HEAD + CRASHES.format(n="boom", k="81.1") + "\n\n" + FAILS.format(n="red", k="81.2")})
    code, out, comments = run_red(tmp_path, repo)
    assert code != 0, "81.3: a test that crashes on main did not stop the worker"
    assert len(comments) == 1, f"81.3: expected one comment on the issue, got {comments}"
    text = comments[0]
    assert "tests/test_a.py::test_boom" in text, f"81.3: the crashing test is not named: {text}"
    assert "broken" in text, f"81.3: the comment does not say 'broken': {text}"
    assert "proves nothing yet" not in text and "test_red" not in text, f"81.3: wrongly blamed: {text}"


def test_a_test_file_that_cannot_be_imported_is_broken(record_property, tmp_path):
    record_property("proves", "81.3")
    src = "import no_such_module_anywhere\n\n\n" + FAILS.format(n="x", k="81.1").replace("app.f()", "1")
    repo = make_repo(tmp_path, {"test_a.py": src})
    code, out, comments = run_red(tmp_path, repo)
    assert code != 0, "81.3: a test file that cannot be imported did not stop the worker"
    assert comments and "tests/test_a.py::test_x" in comments[0] and "broken" in comments[0], f"81.3: not named as broken: {comments}"


def test_a_crash_in_setup_is_broken(record_property, tmp_path):
    record_property("proves", "81.3")
    src = ("import pytest\nimport app\n\n\n@pytest.fixture\ndef thing():\n    raise RuntimeError('no thing')\n\n\n"
           'def test_s(record_property, thing):\n    record_property("proves", "81.1")\n    assert app.f() == 2\n')
    repo = make_repo(tmp_path, {"test_a.py": src})
    code, out, comments = run_red(tmp_path, repo)
    assert code != 0 and comments and "test_s" in comments[0] and "broken" in comments[0], f"81.3: {code} {comments} {out}"


def test_passing_and_broken_tests_are_both_named_in_one_comment(record_property, tmp_path):
    record_property("proves", "81.2")
    record_property("proves", "81.3")
    repo = make_repo(tmp_path, {"test_a.py": HEAD + PASSES.format(n="green", k="81.1") + "\n\n" + CRASHES.format(n="boom", k="81.2")})
    code, out, comments = run_red(tmp_path, repo)
    assert code != 0
    assert len(comments) == 1, f"81.2/81.3: expected one comment, got {comments}"
    assert "test_green" in comments[0] and "test_boom" in comments[0], f"81.2/81.3: both problems must be named: {comments[0]}"


def test_worker_workflow_runs_the_red_check_before_the_worker(record_property):
    record_property("proves", "81.1")
    text = open(WORKER).read()
    assert "dokima.red" in text, "81.1: worker.yml never runs the red check"
    at = text.index("dokima.red")
    assert at < text.index("Worker (Claude Code)"), "81.1: the red check runs after the worker starts"
    step = text[text.rindex("- name:", 0, at):at]
    assert "steps.who.outputs.ok == 'true'" in step, "81.1: the red check runs even when the label was not a code owner's"
    assert "pip install pytest" in text[:at], "81.1: pytest is installed only after the red check"


def test_worker_workflow_may_comment_on_the_issue(record_property):
    record_property("proves", "81.2")
    text = open(WORKER).read()
    assert "issues: write" in text, "81.2: the worker job cannot comment on the issue (issues: write missing)"
