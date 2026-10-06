"""Workflow changes merge like any other change, and keys open only from main (#126).

GitHub runs a PR's own copy of the workflow files before anyone reviews it. These tests
prove that every job holding a key takes it from the "keys" environment (which only main
can open), that nothing else names a key, and that the old approval gate is gone.
"""
import glob
import json
import os
import sys

import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
WORKFLOWS = {os.path.basename(p): yaml.safe_load(open(p)) for p in glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml"))}


def jobs():
    for name, wf in WORKFLOWS.items():
        for job_name, job in (wf.get("jobs") or {}).items():
            yield name, job_name, job


def test_agents_may_push_workflow_files_and_no_extra_approval_exists(record_property):
    """The bot can push workflow files, and no approval step or pending-build handoff remains."""
    record_property("proves", "126.1")
    perms = json.load(open(os.path.join(ROOT, "dokima", "app.json")))["default_permissions"]
    assert perms.get("workflows") == "write", "126.1: the bot can't push workflow changes"
    text = "".join(open(p).read() for p in glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")))
    for gone in ("workflow-changes", "DOKIMA_WORKFLOW_TOKEN", "dokima.gate", "push-workflow-changes"):
        assert gone not in text, f"126.1: the old approval gate is still there ({gone})"
    assert not os.path.exists(os.path.join(ROOT, "dokima", "gate.py"))


def test_every_job_that_uses_a_key_takes_it_from_the_main_only_safe(record_property):
    """Any job that mentions a secret declares the "keys" environment; no other job does."""
    record_property("proves", "126.2")
    for name, job_name, job in jobs():
        uses_key = "secrets." in yaml.safe_dump(job)
        if uses_key:
            assert job.get("environment") == "keys", f"126.2: {name}:{job_name} reads a key outside the safe"


def test_pr_triggered_workflows_hold_no_keys(record_property):
    """Workflows that run on a PR's own copy (pull_request, push to branches) never name a key."""
    record_property("proves", "126.2")
    for name, wf in WORKFLOWS.items():
        on = wf.get(True) or wf.get("on") or {}
        if isinstance(on, dict) and "pull_request" in on:
            assert "secrets." not in open(os.path.join(ROOT, ".github", "workflows", name)).read(), f"126.2: {name} runs on PRs and names a key"


def test_a_build_starts_from_todays_main(record_property):
    """An issue branch made before main changed is brought up to date before the build.

    Without this, a branch the planner created earlier runs old code, so newer
    steps are missing and the build fails.
    """
    record_property("proves", "123.1")
    start = next(s for s in WORKFLOWS["worker.yml"]["jobs"]["work"]["steps"] if s.get("name", "").startswith("Start from the issue's branch"))
    assert "merge -q --no-edit origin/main" in start["run"]
