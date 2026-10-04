import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import checks, plan  # noqa: E402

ISSUE = {"number": 40, "body": ("- [ ] Goal: g\n"
                                "  - [ ] Done when: first thing works\n"
                                "    Verified by: a test\n"
                                "  - [ ] Done when: second thing works\n"
                                "    Verified by: another test\n")}


def write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return str(p)


def test_each_done_when_becomes_a_named_check_running_only_its_tests(record_property, tmp_path):
    record_property("proves", "29.1")
    path = write(tmp_path, "test_x.py",
                 'def test_a(record_property):\n    record_property("proves", "40.1")\n\n'
                 'def test_b(record_property):\n    record_property("proves", "40.2")\n\n'
                 'def test_c(record_property):\n    record_property("proves", "40.2")\n')
    rows = checks.build_matrix(40, plan.parse(ISSUE["body"]), checks.find_tests([path]))
    assert [r["name"] for r in rows] == ["40.1 · first thing works", "40.2 · second thing works"]
    assert rows[0]["tests"] == f"{path}::test_a"
    assert rows[1]["tests"] == f"{path}::test_b {path}::test_c"


def test_long_done_whens_get_short_check_names(record_property):
    record_property("proves", "29.1")
    assert checks.check_name("40.1", "x" * 100) == "40.1 · " + "x" * 57 + "..."


def test_annotation_links_permanently_to_the_tests_first_line(record_property):
    record_property("proves", "29.2")
    xml = ('<testsuites><testsuite>'
           '<testcase file="tests/t.py" line="4" name="test_ok"/>'
           '<testcase file="tests/t.py" line="9" name="test_bad"><failure/></testcase>'
           '</testsuite></testsuites>')
    ok, bad = checks.annotations(xml, "o/r", "abc123", "40.1")
    assert ok.startswith("::notice file=tests/t.py,line=5,title=40.1 passed::")
    assert ok.endswith("view the test: https://github.com/o/r/blob/abc123/tests/t.py#L5")
    assert bad.startswith("::error file=tests/t.py,line=10,title=40.1 failed::")


def test_done_when_without_tests_gets_a_check_that_must_fail(record_property, tmp_path):
    record_property("proves", "29.3")
    rows = checks.build_matrix(40, plan.parse(ISSUE["body"]), {})
    assert [r["tests"] for r in rows] == ["", ""]
    workflow = open(os.path.join(os.path.dirname(__file__), "..", ".github/workflows/done-whens.yml")).read()
    assert 'if [ -z "$TESTS" ]' in workflow and "exit 1" in workflow


def test_pull_request_without_done_whens_cannot_pass(record_property):
    record_property("proves", "29.3")
    assert checks.build_matrix(None, {"goals": []}, {}) == []
    assert checks.build_matrix(40, plan.parse("no checklist"), {}) == []
    workflow = open(os.path.join(os.path.dirname(__file__), "..", ".github/workflows/done-whens.yml")).read()
    assert '[ "$MATRIX" = "[]" ]' in workflow and "No done-whens" in workflow


def test_full_suite_runs_every_test_on_every_pull_request(record_property):
    record_property("proves", "29.4")
    path = os.path.join(os.path.dirname(__file__), "..", ".github/workflows/full-suite.yml")
    lines = [line.strip() for line in open(path)]
    assert "name: full suite" in lines
    assert "pull_request:" in lines
    assert "name: all tests" in lines
    assert any(line.startswith("- run: pytest") and line.endswith(" tests") for line in lines)
