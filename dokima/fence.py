"""The fence: after the worker stops, only in-scope changes survive and the planner's tests are exactly as committed.

The judges (all tests, each criterion's check) run on fresh machines from what gets pushed, so nothing the worker does to
its own machine reaches them. What gets pushed is decided here, by code: every test file and test setup file is put back
to the build's starting commit, and every other change outside the plan's scope is undone. The dropped paths are listed
so the owner sees them.
"""
import os
import re
import subprocess
import sys

TEST_SETUP = {"conftest.py", "pytest.ini", "tox.ini", "setup.cfg", "pyproject.toml"}


def scope_of(issue_text):
    """Return the file paths listed under the plan's Scope heading."""
    paths, inside = [], False
    for line in issue_text.splitlines():
        if re.match(r"\s*\*\*Scope:\*\*", line):
            inside = True
            continue
        if inside:
            m = re.match(r"\s*-\s*`([^`]+)`", line)
            if m:
                paths.append(m.group(1))
            elif line.strip():
                break
    return paths


def is_test(path):
    """Say whether a path is a test or test setup file, which the worker may never change."""
    name = os.path.basename(path)
    return path.startswith("tests/") or "/tests/" in path or name.startswith("test_") or name in TEST_SETUP


def git(*args):
    """Run git in the current repo and return its output."""
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def fence(base, scope):
    """Undo every change since base that is a test file or outside scope; return the dropped paths, sorted."""
    changed = set(git("diff", "--name-only", base).split()) | set(git("ls-files", "--others", "--exclude-standard").split())
    dropped = sorted(p for p in changed if (is_test(p) and p not in TEST_SETUP & set(scope)) or p not in scope)
    for p in dropped:
        if subprocess.run(["git", "cat-file", "-e", f"{base}:{p}"], capture_output=True).returncode == 0:
            git("checkout", base, "--", p)
        elif os.path.exists(p):
            os.remove(p)
    return dropped


def main(argv):
    """fence BASE ISSUE_FILE: apply the fence and print each dropped path."""
    dropped = fence(argv[1], scope_of(open(argv[2]).read()))
    for p in dropped:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
