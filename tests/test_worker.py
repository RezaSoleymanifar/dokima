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
