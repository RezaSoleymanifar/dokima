"""The planner hand-back checker (#139): it reads only plan.json and says exactly why a plan is rejected.

Each test builds a throwaway git repo holding the "older" tests, adds the planner's new tests and a plan.json,
then runs `planner.main(["planner", "check", "139", out])` the way the workflow does. A rejection is the
return code 1 plus the reasons written to rejected.txt, which is what the owner sees on the issue.
"""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import planner  # noqa: E402

SRC = "https://github.com/o/r/issues/139"
NEW = "tests/test_new.py::test_new"
GOOD_TEST = ('def test_new(record_property):\n    """The feature works.\n\n    Fails until the feature exists."""\n'
             '    record_property("proves", "139.1")\n    assert False, "139.1: feature missing"\n')
OLD_TEST = ('def test_old(record_property):\n    """An older test that passes."""\n'
            '    record_property("proves", "80.1")\n    assert True\n')
STORY = {"kind": "user_story", "user_story": "The owner sees it.",
         "acceptance_criteria": [{"text": "It shows.", "source": SRC}], "non_functional": [],
         "scope": ["dokima/x.py"], "out_of_scope": ["Nothing else."], "tests": {"139.1": [NEW]}}
FEATURE_STORY = {"title": "t", "user_story": "u", "acceptance_criteria": [], "non_functional": [], "depends_on": []}


def check(tmp_path, monkeypatch, plan, new_files=None, older=None):
    """Run the checker in a temp repo; returns (exit code, rejected.txt text)."""
    repo, out = tmp_path / "repo", tmp_path / "out"
    (repo / "tests").mkdir(parents=True)
    out.mkdir()
    (repo / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n*.pyc\n")
    for name, text in (older or {"tests/test_base.py": OLD_TEST}).items():
        (repo / name).write_text(text)
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True, text=True).stdout.strip()
    git("init", "-q")
    git("config", "user.name", "t")
    git("config", "user.email", "t@example.com")
    git("add", "-A")
    git("commit", "-qm", "base")
    for name, text in (new_files if new_files is not None else {"tests/test_new.py": GOOD_TEST}).items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        if text is None:
            (repo / name).unlink()
        else:
            (repo / name).write_text(text)
    (out / "plan.json").write_text(json.dumps(plan))
    monkeypatch.chdir(repo)
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("PLANNER_BASE", git("rev-parse", "HEAD"))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    rc = planner.main(["planner", "check", "139", str(out)])
    rejected = out / "rejected.txt"
    return rc, rejected.read_text() if rejected.exists() else ""


def story(**change):
    """A copy of the good story with some fields replaced."""
    return {**json.loads(json.dumps(STORY)), **change}


@pytest.mark.parametrize("source", [
    "https://github.com/o/r/issues/138", "https://github.com/o/r/issues/1390", "https://github.com/x/y/issues/139",
    "https://github.com/o/r/pull/139", "see the issue", "https://github.com/o/r/issues/139#discussion-5",
])
def test_a_source_must_point_at_this_issue(record_property, tmp_path, monkeypatch, source):
    """A criterion whose source points at another issue, repo or page is rejected, naming the source.

    Tries six wrong sources and checks each is named in the reason."""
    record_property("proves", "139.1")
    rc, why = check(tmp_path, monkeypatch, story(acceptance_criteria=[{"text": "It shows.", "source": source}]))
    assert rc == 1 and "source" in why and source in why, f"139.1: source {source!r} was not rejected with its reason: {why!r}"


def test_the_issue_and_its_comments_are_valid_sources(record_property, tmp_path, monkeypatch):
    """A source that is the issue or one of its comments is accepted, but only when the rest is wrong in no way.

    Uses a comment link and a broken plan elsewhere, so the only thing under test is that the source is not blamed."""
    record_property("proves", "139.1")
    ok = story(acceptance_criteria=[{"text": "It shows.", "source": SRC + "#issuecomment-4242"}], tests={"139.1": ["tests/test_new.py::test_nope"]})
    rc, why = check(tmp_path, monkeypatch, ok)
    assert rc == 1 and "test_nope" in why, "139.1: the plan's other problem was not reported"
    assert "source" not in why, f"139.1: a comment link was rejected as a source: {why!r}"


def test_every_named_test_must_exist_and_prove_a_criterion_of_this_plan(record_property, tmp_path, monkeypatch):
    """A plan naming a test that is not in the repo, or filing it under a criterion this plan does not have, is rejected.

    Names a missing function, a missing file, a criterion past the last one and another issue's number, and checks each is reported."""
    record_property("proves", "139.2")
    cases = [
        ({"139.1": ["tests/test_new.py::test_nope"]}, "tests/test_new.py::test_nope"),
        ({"139.1": ["tests/test_ghost.py::test_new"]}, "tests/test_ghost.py::test_new"),
        ({"139.1": [NEW], "139.7": [NEW]}, "139.7"),
        ({"139.1": [NEW], "140.1": [NEW]}, "140.1"),
    ]
    for tests, mention in cases:
        rc, why = check(tmp_path / mention.replace("/", "_").replace(":", "_"), monkeypatch, story(tests=tests))
        assert rc == 1 and mention in why, f"139.2: {mention} was not rejected: {why!r}"
    assert "does not exist" in check(tmp_path / "again", monkeypatch, story(tests={"139.1": ["tests/test_new.py::test_nope"]}))[1], \
        "139.2: the reason does not say the test does not exist"


@pytest.mark.parametrize("docstring", ['', '"""no full stop"""', '"""Two lines\n    run on.\n\n    Then more."""', '"""One sentence. And another on the same line."""'])
def test_a_new_test_needs_a_one_sentence_docstring(record_property, tmp_path, monkeypatch, docstring):
    """A new test with no docstring, or a first line that is not one plain sentence, is rejected, naming the test.

    Tries a missing docstring, a first line with no full stop, a sentence that runs onto a second line and a first line with two sentences."""
    record_property("proves", "139.3")
    text = GOOD_TEST.split('"""')[0] + (docstring + "\n    " if docstring else "") + 'record_property("proves", "139.1")\n    assert False\n'
    rc, why = check(tmp_path, monkeypatch, story(), {"tests/test_new.py": text})
    assert rc == 1 and NEW in why and "docstring" in why, f"139.3: bad docstring {docstring!r} not rejected with its reason: {why!r}"


def test_a_new_test_must_fail_on_todays_code(record_property, tmp_path, monkeypatch):
    """A new test that passes today, or cannot even run, is rejected, naming the test and saying which.

    Runs the checker on a test that passes and on a test with an import error; the passing one must say it passes today."""
    record_property("proves", "139.4")
    passing = GOOD_TEST.replace('assert False, "139.1: feature missing"', "assert True")
    rc, why = check(tmp_path / "a", monkeypatch, story(), {"tests/test_new.py": passing})
    assert rc == 1 and NEW in why and "passes today" in why, f"139.4: a passing new test was not rejected: {why!r}"
    broken = "import no_such_module_139\n\n" + GOOD_TEST
    rc, why = check(tmp_path / "b", monkeypatch, story(), {"tests/test_new.py": broken})
    assert rc == 1 and NEW in why and "does not run" in why, f"139.4: a test that cannot run was not rejected: {why!r}"


def test_a_rename_is_a_change_not_a_new_test(record_property, tmp_path, monkeypatch):
    """A renamed older test is held to the rules for changes (it needs a reason) and not the rules for new tests.

    Renames a passing older test with no docstring change alongside one new passing test; only the new test may be blamed, and a rename with no reason is rejected."""
    record_property("proves", "139.5")
    older = {"tests/test_base.py": OLD_TEST, "tests/test_other.py": OLD_TEST.replace("test_old", "test_older")}
    renamed = {"tests/test_other.py": OLD_TEST.replace("test_old", "test_older_renamed"), "tests/test_new.py": GOOD_TEST,
               "tests/test_extra.py": GOOD_TEST.replace("test_new", "test_extra").replace("assert False", "assert True")}
    plan = story(tests={"139.1": [NEW]}, test_changes={"tests/test_other.py::test_older": "renamed to say what it checks"})
    rc, why = check(tmp_path / "a", monkeypatch, plan, renamed, older)
    assert rc == 1 and "test_extra" in why, f"139.5: the new passing test was not caught: {why!r}"
    assert "test_older_renamed" not in why, f"139.5: the renamed test was judged as a new test: {why!r}"
    rc, why = check(tmp_path / "b", monkeypatch, story(), {"tests/test_other.py": renamed["tests/test_other.py"], "tests/test_new.py": GOOD_TEST}, older)
    assert rc == 1 and "test_older" in why and "test_changes" in why, f"139.5: a rename with no reason passed: {why!r}"


def test_a_feature_needs_valid_stories_and_depends_on(record_property, tmp_path, monkeypatch):
    """A feature whose stories depend on themselves, on stories that don't exist, or on each other in a loop is rejected.

    Tries a self-dependency, an index past the last story, a three-story loop and a story missing its title, then a valid chain."""
    record_property("proves", "139.6")
    def feature(*deps):
        return {"kind": "feature", "feature": "f", "stories": [{**FEATURE_STORY, "depends_on": d} for d in deps]}
    bad = {"self": feature([0], []), "range": feature([5], []), "loop": feature([1], [2], [0]), "negative": feature([-1], [])}
    for name, plan in bad.items():
        rc, why = check(tmp_path / name, monkeypatch, plan, {})
        assert rc == 1 and "depends_on" in why, f"139.6: {name} dependency was not rejected: {why!r}"
    rc, why = check(tmp_path / "titleless", monkeypatch, {**feature([], []), "stories": [{**FEATURE_STORY, "title": " "}, FEATURE_STORY]}, {})
    assert rc == 1 and "title" in why, f"139.6: a story with no title was accepted: {why!r}"
    rc, why = check(tmp_path / "ok", monkeypatch, feature([], [0], [0, 1]), {})
    assert (rc, why) == (0, ""), f"139.6: a valid chain of stories was rejected: {why!r}"


def test_a_question_needs_options_and_a_recommendation(record_property, tmp_path, monkeypatch):
    """A question with no options or no recommendation is rejected, saying which is missing; a full question passes.

    Hands back four questions: complete, no recommendation, no options, and no question mark."""
    record_property("proves", "139.7")
    q = {"kind": "question", "question": "Split it?", "options": ["Yes", "No"], "recommendation": "Yes"}
    assert check(tmp_path / "ok", monkeypatch, q, {}) == (0, ""), "139.7: a complete question was rejected"
    for name, plan, word in [("rec", {**q, "recommendation": " "}, "recommendation"), ("rec2", {k: v for k, v in q.items() if k != "recommendation"}, "recommendation"),
                             ("opts", {**q, "options": []}, "options"), ("mark", {**q, "question": "Split it."}, "?")]:
        rc, why = check(tmp_path / name, monkeypatch, plan, {})
        assert rc == 1 and word in why, f"139.7: question without {word} was not rejected: {why!r}"


def test_every_problem_is_listed_together(record_property, tmp_path, monkeypatch):
    """A plan with several problems is rejected once, with every problem in the reason.

    Gives a wrong source, a named test that does not exist and a new test with no docstring, and checks all three are named."""
    record_property("proves", "139.8")
    nodoc = 'def test_new(record_property):\n    record_property("proves", "139.1")\n    assert False\n'
    plan = story(acceptance_criteria=[{"text": "It shows.", "source": "https://github.com/o/r/issues/7"}],
                 tests={"139.1": [NEW, "tests/test_new.py::test_nope"]})
    rc, why = check(tmp_path, monkeypatch, plan, {"tests/test_new.py": nodoc})
    assert rc == 1, "139.8: the plan was accepted"
    for part in ["source", "test_nope", "docstring"]:
        assert part in why, f"139.8: the rejection does not mention {part!r}: {why!r}"


def test_an_unreadable_test_file_is_rejected_not_a_crash(record_property, tmp_path, monkeypatch):
    """A new test file with a syntax error is rejected with a reason naming the file; the checker itself never crashes.

    Hands back a plan whose new test file cannot be parsed and expects exit code 1 and the file's name in the reason."""
    record_property("proves", "139.9")
    rc, why = check(tmp_path, monkeypatch, story(), {"tests/test_new.py": GOOD_TEST + "\ndef broken(:\n"})
    assert rc == 1 and "tests/test_new.py" in why, f"139.9: an unparseable test file was not rejected with its name: {why!r}"
