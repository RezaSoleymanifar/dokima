"""Turn an issue's criteria into GitHub checks, and annotate the tests they ran.

    python3 -m dokima.checks matrix          # print the check list for this PR
    python3 -m dokima.checks annotate r.xml  # print one annotation per test in a JUnit report

A test proves a criterion by calling record_property("proves", "<issue>.<n>"),
where n counts the issue's criteria from 1, top to bottom.
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from dokima import plan

PROVES = re.compile(r"""record_property\(\s*["']proves["']\s*,\s*["']([\d.]+)["']\s*\)""")
TEST_DEF = re.compile(r"^def (test_\w+)\(")


def find_tests(paths):
    """Map each criterion key like '29.1' to the tests that prove it, as 'path::test'."""
    found = {}
    for path in sorted(paths):
        current = None
        with open(path) as f:
            for line in f:
                name = TEST_DEF.match(line)
                if name:
                    current = name.group(1)
                for key in PROVES.findall(line):
                    if current:
                        found.setdefault(key, []).append(f"{path}::{current}")
    return found


def check_name(key, text, limit=60):
    """The check's name on GitHub: '29.1 · <criterion, shortened>'."""
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return f"{key} · {text}"


def build_matrix(number, words, tests):
    """One check per criterion in the plan; empty when there is no issue or no criteria."""
    rows = []
    if not number:
        return rows
    for goal in words["goals"]:
        for c in goal["criteria"]:
            key = f"{number}.{c['n']}"
            rows.append({"id": key, "name": check_name(key, c["text"]), "tests": " ".join(tests.get(key, []))})
    return rows


def annotations(junit_xml, repo, sha, done_when):
    """One annotation per test that ran, with a permanent link to the test's first line at this commit."""
    lines = []
    for tc in ET.fromstring(junit_xml).iter("testcase"):
        failed = any(child.tag in ("failure", "error") for child in tc)
        kind, verdict = ("error", "failed") if failed else ("notice", "passed")
        path, line = tc.get("file"), int(tc.get("line")) + 1
        link = f"https://github.com/{repo}/blob/{sha}/{path}#L{line}"
        lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"
                     f"{tc.get('name')} {verdict} · {path} line {line} · view the test: {link}")
    return lines


def main(argv):
    repo = os.environ["GITHUB_REPOSITORY"]
    if argv[1] == "matrix":
        pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]["number"]
        number = plan.pr_issue_number(repo, pr)
        # The plan as approved; edits made after the `work` label are not used.
        words = plan.fetch_issue(repo, number)["plan"] if number else {"goals": []}
        print("matrix=" + json.dumps(build_matrix(number, words, find_tests(glob.glob("tests/test_*.py")))))
    elif argv[1] == "annotate":
        for line in annotations(open(argv[2]).read(), repo, os.environ["HEAD_SHA"], os.environ["ID"]):
            print(line)


if __name__ == "__main__":
    main(sys.argv)
