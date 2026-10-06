"""Red before work: the tests that prove an issue's criteria must fail an assert on main.

    python3 -m dokima.red 81   # exit non-zero, and comment on the issue, if any is green or broken

The tests run against main's code (RED_BASE, default origin/main) with the branch's
test files laid over it, so a work branch that already holds the feature still counts
as red. A test that passes proves nothing yet; one that crashes is broken.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from dokima import checks


def tests_for(number, paths):
    """The 'path::test' ids of every test that proves one of this issue's criteria."""
    ids = []
    for key, found in checks.find_tests(paths).items():
        if key.startswith(f"{number}."):
            ids += found
    return sorted(set(ids))


def is_assert(element):
    message = element.get("message") or ""
    return message.startswith(("assert", "AssertionError"))


def classify(ids, junit_xml):
    """Split test ids into (passing, broken); a test that fails an assert is correctly red."""
    verdict = {}
    for tc in ET.fromstring(junit_xml).iter("testcase"):
        name = tc.get("name")
        failure, error, skipped = tc.find("failure"), tc.find("error"), tc.find("skipped")
        if error is not None or skipped is not None:
            verdict[name] = "broken"
        elif failure is not None:
            verdict[name] = "red" if is_assert(failure) else "broken"
        else:
            verdict[name] = "passing"
    passing, broken = [], []
    for test_id in ids:
        got = verdict.get(test_id.split("::")[-1], "broken")
        if got == "passing":
            passing.append(test_id)
        elif got == "broken":
            broken.append(test_id)
    return passing, broken


def message(number, passing, broken):
    lines = [f"The tests for #{number} are not ready: the worker did not start.", ""]
    if passing:
        lines.append("These pass on main already, so each one proves nothing yet:")
        lines += [f"- `{t}`" for t in passing]
        lines.append("")
    if broken:
        lines.append("These are broken (they crash on main instead of failing an assert):")
        lines += [f"- `{t}`" for t in broken]
        lines.append("")
    lines.append("Amend the plan with `/plan` so each test fails an assert on main, then add `work` again.")
    return "\n".join(lines)


def run(number):
    ids = tests_for(number, glob.glob("tests/**/*.py", recursive=True))
    if not ids:
        return 0, None
    base = os.environ.get("RED_BASE", "origin/main")
    tmp = tempfile.mkdtemp()
    tree = os.path.join(tmp, "main")
    try:
        subprocess.run(["git", "worktree", "add", "-q", "--detach", tree, base], check=True)
        shutil.copytree("tests", os.path.join(tree, "tests"), dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
        report = os.path.join(tmp, "red.xml")
        subprocess.run([sys.executable, "-m", "pytest", "-q", "--continue-on-collection-errors",
                        "-p", "no:cacheprovider", f"--junitxml={report}", *ids],
                       cwd=tree, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH=tree))
        junit = open(report).read() if os.path.exists(report) else "<testsuites/>"
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", tree], capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)
    passing, broken = classify(ids, junit)
    if not passing and not broken:
        return 0, None
    return 1, message(number, passing, broken)


def main(argv):
    number = argv[0]
    code, text = run(number)
    if text:
        print(text)
        subprocess.run(["gh", "issue", "comment", number, "--repo", os.environ["GITHUB_REPOSITORY"],
                        "--body-file", "-"], input=text, text=True, check=True)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
