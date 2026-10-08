"""Red before work: the plan's tests must fail on main, on an assert, before the worker starts (#81).

A test that already passes before the work exists proves nothing, and a test that crashes burns the worker's whole
budget against something it can never pass. So before the worker starts, code builds main's code in a scratch folder,
lays the plan's test files over it as the issue's branch holds them, and runs the plan's tests, and only those, there.
Every plan test that does not fail an assert is named with why; any named test stops the worker.
"""
import json
import os
import subprocess
import sys
import tempfile

MAIN = "origin/main"

# Loaded into pytest by the run below: keeps only the plan's tests and writes how each one went.
PLUGIN = '''
import json, os, re
import pytest

WANT = json.loads(os.environ["DOKIMA_RED_TESTS"])
OUT = os.environ["DOKIMA_RED_OUT"]
seen = {"files_broken": {}, "phases": {}}


def wanted(nodeid):
    return nodeid in WANT or nodeid.split("[")[0] in WANT


def pytest_collectreport(report):
    if report.failed:
        seen["files_broken"][report.nodeid] = [re.sub(r"^E\s+", "", l.strip()) for l in str(report.longrepr).strip().splitlines()[-1:]]


def pytest_collection_modifyitems(config, items):
    keep = [i for i in items if wanted(i.nodeid)]
    drop = [i for i in items if not wanted(i.nodeid)]
    items[:] = keep
    if drop:
        config.hook.pytest_deselected(items=drop)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    err = ""
    kind = rep.outcome
    if call.excinfo is not None and rep.failed:
        kind = "assert" if call.excinfo.errisinstance(AssertionError) else "error"
        err = f"{call.excinfo.typename}: {str(call.excinfo.value).strip().splitlines()[0] if str(call.excinfo.value).strip() else ''}"
    if hasattr(rep, "wasxfail"):
        kind = "skipped"
    seen["phases"].setdefault(item.nodeid, []).append([call.when, kind, err.strip().rstrip(":")])


def pytest_sessionfinish(session):
    json.dump(seen, open(OUT, "w"))
'''


def plan_tests(plan):
    """Every test the plan names, once each, in the plan's order."""
    out = []
    for ids in (plan.get("tests") or {}).values():
        for t in ids if isinstance(ids, list) else []:
            if t not in out:
                out.append(t)
    return out


def verdict(test, seen, present):
    """Why one plan test does not prove anything yet on main, or None when it fails an assert there as it should."""
    path = test.split("::")[0]
    if path not in present:
        return "cannot be found: its file is not on the issue's branch"
    if path in seen["files_broken"]:
        return f"is broken: its file cannot be imported on main ({' '.join(seen['files_broken'][path])[:160]})"
    runs = [p for n, ps in seen["phases"].items() if n == test or n.split("[")[0] == test for p in ps]
    if not runs:
        return "cannot be found on main, so it never ran"
    errors = [(when, err) for when, kind, err in runs if kind == "error" or (kind == "assert" and when != "call")]
    if errors:
        when, err = errors[0]
        where = "in its setup" if when == "setup" else "in its teardown" if when == "teardown" else "in its body"
        return f"is broken: it crashes {where} ({err[:160]})"
    if any(kind == "assert" for _, kind, _ in runs):
        return None
    if any(kind == "skipped" for _, kind, _ in runs):
        return "is skipped on main, so it never ran and proves nothing yet"
    return "already passes on main, so it proves nothing yet"


def problems(plan_path, repo="."):
    """Why the plan's tests do not all fail an assert on main's code, naming each test that does not; empty when all are red."""
    try:
        tests = plan_tests(json.load(open(plan_path)))
    except (OSError, json.JSONDecodeError, AttributeError) as e:
        return [f"red before work: the plan's tests could not be read ({e})"]
    if not tests:
        return ["red before work: the plan names no tests, so nothing proves it yet"]
    with tempfile.TemporaryDirectory() as tmp:
        tree, tools, out = os.path.join(tmp, "main"), os.path.join(tmp, "tools"), os.path.join(tmp, "seen.json")
        os.makedirs(tree)
        os.makedirs(tools)
        archive = subprocess.run(["git", "-C", repo, "archive", MAIN], capture_output=True)
        if archive.returncode != 0:
            return [f"red before work: main's code could not be read ({archive.stderr.decode(errors='replace').strip()})"]
        subprocess.run(["tar", "-x", "-C", tree], input=archive.stdout, check=True)
        present = set()
        for path in dict.fromkeys(t.split("::")[0] for t in tests):
            body = subprocess.run(["git", "-C", repo, "show", f"HEAD:{path}"], capture_output=True)
            if body.returncode != 0:
                continue
            os.makedirs(os.path.dirname(os.path.join(tree, path)) or tree, exist_ok=True)
            open(os.path.join(tree, path), "wb").write(body.stdout)
            present.add(path)
        open(os.path.join(tools, "dokima_red_plugin.py"), "w").write(PLUGIN)
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONSAFEPATH")}
        env.update({"PYTHONPATH": tools, "DOKIMA_RED_TESTS": json.dumps(tests), "DOKIMA_RED_OUT": out})
        run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "dokima_red_plugin", "-p", "no:cacheprovider",
                              f"--rootdir={tree}", "--continue-on-collection-errors", *sorted(present)],
                             cwd=tree, env=env, capture_output=True, text=True)
        try:
            seen = json.load(open(out))
        except (OSError, json.JSONDecodeError):
            tail = " ".join((run.stdout + run.stderr).strip().splitlines()[-2:])
            return [f"red before work: the plan's tests could not be run on main ({tail[:300]})"]
    named = [(t, verdict(t, seen, present)) for t in tests]
    named = [f"{t} {why}" for t, why in named if why]
    if not named:
        return []
    # One line: the workflow joins the check's lines with alternating separators.
    return ["red before work, every plan test must fail an assert on main's code before the worker starts: " + "; ".join(named)]
