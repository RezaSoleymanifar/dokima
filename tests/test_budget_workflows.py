"""Tests for #426: every workflow calling GitHub's API reads the budget before and after.

These read the workflow files with the repo's own YAML reader (tests/test_start.py's load_yaml, no YAML library).
A job calls GitHub's API when any of its steps is given GH_TOKEN. Each such job must run
`python3 -m dokima.budget before KEY FILE` before its first call and `python3 -m dokima.budget after KEY FILE` after
its last, even when a step failed, and keep FILE with the run as an artifact. KEY is `app` when the job holds the
Dokima app's key and `github-token` when it only holds the repo's own GITHUB_TOKEN, which has a budget of its own.
The command itself, and what it writes, is proven in tests/test_budget.py.
"""
import os
import re
import shlex
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import test_start as ts  # noqa: E402

WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
NAMED = ["agent.yml", "assign.yml", "audit.yml", "autopilot.yml", "board.yml", "card.yml", "commands.yml",
         "done-whens.yml", "planner.yml", "worker.yml", "uptodate.yml"]
BUDGET = re.compile(r"python3\s+(?:-m\s+dokima\.budget|\S*dokima/budget\.py)\s+(.*)")
APP_TOKEN = re.compile(r"^\$\{\{\s*steps\.([\w-]+)\.outputs\.token\s*\}\}$")


def load(name):
    """One workflow file, read."""
    return ts.load_yaml(open(os.path.join(WORKFLOWS, name)).read())


def token(step):
    """The GH_TOKEN a step is given, or None."""
    t = (step.get("env") or {}).get("GH_TOKEN")
    return str(t).strip() if t else None


def budget_call(step):
    """(moment, key, file) when the step reads the budget, else None."""
    m = BUDGET.search(str(step.get("run") or ""))
    if not m:
        return None
    words = shlex.split(m.group(1).split("\n")[0])
    return tuple(words[:3]) if len(words) >= 3 else ("?", "?", "?")


def api_jobs(wf):
    """Every (job name, job) whose steps are given GH_TOKEN, so it calls GitHub's API."""
    return [(n, j) for n, j in (wf.get("jobs") or {}).items()
            if any(token(s) for s in j.get("steps") or [])]


def expand(text, env):
    """A path with $X, ${X} and ${{ env.X }} filled in from its env."""
    text = re.sub(r"\$\{\{\s*env\.(\w+)\s*\}\}", lambda m: str(env.get(m.group(1), m.group(0))), str(text))
    return re.sub(r"\$\{?(\w+)\}?", lambda m: str(env.get(m.group(1), m.group(0))), text)


def is_key_step(step):
    """Whether the step mints the Dokima app's key."""
    return "create-github-app-token" in str(step.get("uses") or "")


def always(step):
    """Whether the step runs even after an earlier step failed."""
    return "always()" in str(step.get("if") or "")


def uploads(wf):
    """Every upload-artifact step of the workflow, with its job's name."""
    return [(n, i, s) for n, j in (wf.get("jobs") or {}).items() for i, s in enumerate(j.get("steps") or [])
            if "upload-artifact" in str(s.get("uses") or "")]


def check_job(wf_name, wf, job_name, job):
    """Every problem with how one API-calling job reads and keeps its budget, in plain words."""
    where = f"{wf_name} job {job_name}"
    steps = job.get("steps") or []
    env = {**(wf.get("env") or {}), **(job.get("env") or {})}
    calls = [(i, s, budget_call(s)) for i, s in enumerate(steps) if budget_call(s)]
    api = [i for i, s in enumerate(steps) if token(s) and not budget_call(s)]
    holds_app = any(APP_TOKEN.match(token(s) or "") for s in steps)
    want_key = "app" if holds_app else "github-token"
    befores = [(i, s, c) for i, s, c in calls if c[0] == "before"]
    afters = [(i, s, c) for i, s, c in calls if c[0] == "after"]
    bad = []
    if len(befores) != 1:
        return [f"{where}: should read the budget before its run in exactly one step "
                f"(`python3 -m dokima.budget before {want_key} FILE`), found {len(befores)}"]
    if not afters:
        return [f"{where}: never reads the budget after its run (`python3 -m dokima.budget after {want_key} FILE`)"]
    b_i, b_step, (_, b_key, b_file) = befores[0]
    b_path = expand(b_file, {**env, **(b_step.get("env") or {})})
    if api and b_i > min(api):
        bad.append(f"{where}: reads the budget before its run at step {b_i}, after its first API call at step {min(api)}")
    last_after = max(i for i, _, _ in afters)
    if api and last_after < max(api):
        bad.append(f"{where}: its last budget reading (step {last_after}) comes before its last API call "
                   f"(step {max(api)}), so it is not after the run")
    for i, s, (moment, key, file) in calls:
        if moment not in ("before", "after"):
            bad.append(f"{where}: step {i} reads the budget at {moment!r}, not before or after")
        if key != want_key:
            bad.append(f"{where}: step {i} labels the budget {key!r}; this job's key is {want_key!r}")
        if expand(file, {**env, **(s.get("env") or {})}) != b_path:
            bad.append(f"{where}: step {i} writes its reading to {file}, not to the same file as the reading before "
                       f"({b_file})")
        if str(s.get("continue-on-error") or "").strip() != "true":
            bad.append(f"{where}: step {i} reads the budget without continue-on-error: true, so a reading that fails "
                       f"could fail the run's work")
        if moment == "after" and not always(s):
            bad.append(f"{where}: step {i} reads the budget after the run only when every step passed; its if: "
                       f"needs always()")
        t = token(s) or ""
        if want_key == "app":
            m = APP_TOKEN.match(t)
            minted = [j for j, k in enumerate(steps[:i]) if m and k.get("id") == m.group(1) and is_key_step(k)]
            if not minted:
                bad.append(f"{where}: step {i} reads the app's budget, so its GH_TOKEN should be an app key minted "
                           f"earlier in the job; it is {t!r}")
            elif all(budget_call(x) for x in steps if APP_TOKEN.match(token(x) or "")
                     and APP_TOKEN.match(token(x)).group(1) == m.group(1)) \
                    and str(steps[minted[0]].get("continue-on-error") or "").strip() != "true":
                bad.append(f"{where}: the key minted at step {minted[0]} only reads the budget, so it needs "
                           f"continue-on-error: true; a key that cannot be minted must not stop the run")
        elif not re.fullmatch(r"\$\{\{\s*(github\.token|secrets\.GITHUB_TOKEN)\s*\}\}", t):
            bad.append(f"{where}: step {i} reads the GITHUB_TOKEN's budget, so its GH_TOKEN should be "
                       f"${{{{ github.token }}}}; it is {t!r}")
    pythonpath = str(env.get("PYTHONPATH") or "")
    if pythonpath:
        if not any(pythonpath in str(s.get("run") or "") for s in steps[:b_i]):
            bad.append(f"{where}: Dokima's code is on {pythonpath}, but nothing puts it there before the budget is "
                       f"read at step {b_i}")
    elif not any("actions/checkout" in str(s.get("uses") or "") for s in steps[:b_i]):
        bad.append(f"{where}: nothing checks out Dokima's code before the budget is read at step {b_i}")
    kept = []
    for i, s in enumerate(steps):
        if "upload-artifact" not in str(s.get("uses") or "") or i <= last_after or not always(s):
            continue
        paths = [expand(p.strip(), {**env, **(s.get("env") or {})})
                 for p in str((s.get("with") or {}).get("path") or "").splitlines() if p.strip()]
        if any(b_path == p.rstrip("/") or b_path.startswith(p.rstrip("/") + "/") for p in paths):
            kept.append(i)
    if not kept:
        bad.append(f"{where}: the budget file {b_file} is not kept with the run: no upload-artifact step with "
                   f"if: always() after the last reading uploads it")
    return bad


def artifact_name(job_name, step):
    """An upload step's artifact name, with ${{ github.job }} filled in as GitHub does."""
    name = str((step.get("with") or {}).get("name") or "artifact")
    return re.sub(r"\$\{\{\s*github\.job\s*\}\}", job_name, name)


def same_names(wf_name, wf):
    """Every artifact name the run uploads twice, counting the workflows it calls."""
    names = [artifact_name(n, s) for n, _, s in uploads(wf)]
    for job in (wf.get("jobs") or {}).values():
        called = str(job.get("uses") or "")
        if called.startswith("./.github/workflows/"):
            names += [artifact_name(n, s) for n, _, s in uploads(load(os.path.basename(called)))]
    return [f"{wf_name}: uploads more than one artifact named {n}, so one would be lost"
            for n in sorted({n for n in names if names.count(n) > 1})]


@pytest.mark.parametrize("name", NAMED)
def test_every_workflow_that_calls_github_records_the_budget_before_and_after(name, record_property):
    """Every workflow calling GitHub's API reads both budgets before and after, and keeps them.

    Proves 426.2.

    Reads the workflow, finds every job given GH_TOKEN, and checks each reads the budget before its first API call
    and after its last (even after a failure), under the key it holds, into one file it uploads with the run under
    an artifact name no other job of the run uses, so no budget file is lost."""
    record_property("proves", "426.2")
    wf = load(name)
    jobs = api_jobs(wf)
    assert jobs, f"426.2: {name} should call GitHub's API in at least one job; found none"
    bad = [p for n, j in jobs for p in check_job(name, wf, n, j)] + same_names(name, wf)
    assert not bad, "426.2: " + "\n426.2: ".join(bad)


def test_an_agent_run_reads_the_budget_after_the_agent_and_before_its_record(record_property):
    """An agent's record is written from readings before the run and after the agent finished.

    Proves 426.1.

    Checks agent.yml reads the app's budget into $OUT/budget.jsonl, the file the record reads, and that a reading
    after the run comes after the agent and before the step that writes the record, even when the agent failed."""
    record_property("proves", "426.1")
    wf = load("agent.yml")
    job = wf["jobs"]["run"]
    steps = job["steps"]
    env = {**(wf.get("env") or {}), **(job.get("env") or {})}
    agent = [i for i, s in enumerate(steps) if "claude -p" in str(s.get("run") or "")]
    record = [i for i, s in enumerate(steps) if "dokima.agent record" in str(s.get("run") or "")]
    assert agent and record, "426.1: agent.yml should run the agent and then write the record"
    calls = [(i, s, budget_call(s)) for i, s in enumerate(steps) if budget_call(s)]
    want = os.path.join(str(env.get("OUT")), "budget.jsonl")
    files = {expand(c[2], {**env, **(s.get("env") or {})}) for _, s, c in calls}
    assert files == {want}, f"426.1: agent.yml should read the budget into $OUT/budget.jsonl ({want}); it uses {files}"
    assert any(c[0] == "before" and c[1] == "app" for _, _, c in calls), \
        "426.1: agent.yml should read the app's budget before the run"
    between = [i for i, s, c in calls if c[0] == "after" and c[1] == "app" and agent[0] < i < record[0] and always(s)]
    assert between, (f"426.1: agent.yml should read the app's budget after the agent (step {agent[0]}) and before "
                     f"the record is written (step {record[0]}), with if: always()")
