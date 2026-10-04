import os

WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github/workflows/worker.yml")


def run_name():
    return next(line for line in open(WORKFLOW) if line.startswith("run-name:"))[len("run-name:"):].strip()


def test_run_name_is_a_quoted_string_without_bare_colons(record_property):
    record_property("proves", "34.1")
    value = run_name()
    assert value.startswith('"') and value.endswith('"')
    inner = value[1:-1]
    assert '"' not in inner
    assert ": " not in inner


def test_work_label_runs_are_named_worker_for_issue(record_property):
    record_property("proves", "34.2")
    value = run_name()[1:-1]
    assert value.startswith("worker for #${{ github.event.issue.number }}")
    suffix = value[len("worker for #${{ github.event.issue.number }}"):]
    assert suffix.startswith("${{ github.event.label.name != 'work' && ")
    assert suffix.endswith("|| '' }}")


def test_first_commit_is_the_plan_file(record_property):
    record_property("proves", "54.1")
    text = open(WORKFLOW).read()
    assert "BODY: ${{ github.event.issue.body }}" in text
    assert '.dokima/plans/$N.md"' in text
    assert 'git add ".dokima/plans/$N.md"' in text
    assert "--allow-empty" not in text


def test_plan_file_lines_are_wrapped_for_phones(record_property):
    record_property("proves", "60.1")
    import re
    import subprocess
    text = open(WORKFLOW).read()
    line = next(l for l in text.splitlines() if '.dokima/plans/$N.md"' in l and "printf" in l)
    assert "| fold -s -w 60 >" in line
    script = re.sub(r'> ".dokima/plans/\$N.md"', "", line.strip())
    body = "- [ ] Done when: " + "word " * 40
    out = subprocess.run(["sh", "-c", script], env={"N": "7", "TITLE": "T", "BODY": body, "PATH": "/usr/bin:/bin"},
                         capture_output=True, text=True, check=True).stdout
    assert out.count("\n") > 3
    assert all(len(l) <= 60 for l in out.splitlines())
    assert " ".join(out.split()) == " ".join(("# #7: T " + body).split())
