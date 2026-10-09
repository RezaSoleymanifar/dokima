"""No test caps how many lines dokima/agent.py or dokima/board.py may have (#344).

#331 added tests/test_board_state.py::test_the_board_code_is_shorter_than_before, which failed whenever board.py, or
board.py and agent.py together, grew past their line counts of that day. The owner asked for it to go: a size limit is
not a behavior, and it blocked work that had to add lines. These tests hold the repo to that: no test anywhere counts
the lines of either file, the board's tests pass with both files much longer, and every other board test is kept.
"""
import ast
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAPPED = ("dokima/agent.py", "dokima/board.py")
# Every test tests/test_board_state.py held when #344 was planned, except the size cap the owner asked to remove.
KEPT = ["test_any_event_puts_both_cards_where_the_issues_state_says",
        "test_the_next_event_fixes_what_a_dropped_or_late_event_left_wrong",
        "test_the_end_of_a_run_places_the_cards_from_state_not_from_the_run",
        "test_needs_you_and_autopilot_follow_the_history_whichever_event_comes",
        "test_the_board_runs_on_every_event_about_an_issue_or_its_pull_request",
        "test_the_15_minute_sweep_rechecks_only_what_changed_since_the_last_sweep",
        "test_with_no_sweep_to_count_from_the_sweep_rechecks_every_card",
        "test_the_15_minute_sweep_puts_every_card_where_its_state_says",
        "test_the_real_board_reads_each_cards_column_for_the_sweep",
        "test_closed_items_sit_in_done_with_no_pill_whatever_their_labels",
        "test_the_sweep_puts_closed_items_in_done_with_no_pill",
        "test_agents_md_says_a_closed_item_shows_no_pill_whatever_its_labels",
        "test_an_issue_and_its_pull_request_share_one_board_queue",
        "test_the_board_workflow_joins_that_queue_and_never_cancels_a_running_recompute",
        "test_the_per_event_board_rules_are_removed",
        "test_an_unreadable_card_keeps_its_place_and_the_run_fails_naming_it",
        "test_the_sweep_fixes_the_rest_and_fails_naming_the_unreadable_card",
        "test_a_failed_run_shows_needs_you_at_once_even_when_github_cannot_be_read"]


def counts_lines(fn):
    """True when a function counts lines with len() of splitlines() or readlines()."""
    return any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == "len" and c.args
               and isinstance(c.args[0], ast.Call) and isinstance(c.args[0].func, ast.Attribute)
               and c.args[0].func.attr in ("splitlines", "readlines") for c in ast.walk(fn))


def line_caps():
    """Every test in tests/ that names dokima/agent.py or dokima/board.py and counts lines, as path::name."""
    found = []
    for path in sorted(glob.glob(os.path.join(ROOT, "tests", "*.py"))):
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        for fn in ast.walk(ast.parse(open(path).read())):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and fn.name.startswith("test"):
                texts = {c.value for c in ast.walk(fn) if isinstance(c, ast.Constant) and isinstance(c.value, str)}
                if any(t.endswith(CAPPED) for t in texts) and counts_lines(fn):
                    found.append(f"tests/{os.path.basename(path)}::{fn.name}")
    return found


def test_no_test_caps_the_line_count_of_agent_py_or_board_py(record_property):
    """No test counts agent.py or board.py lines, and every other board test stays.

    Reads every test in tests/ and fails naming each one that names dokima/agent.py or dokima/board.py and counts lines
    with len(...splitlines()) or len(...readlines()), the way the removed size cap did. Then reads
    tests/test_board_state.py and fails naming any other test it held when this was planned that is gone, so removing
    the whole file or more than the cap does not count. Proves 344.3."""
    record_property("proves", "344.3")
    left = line_caps()
    assert not left, f"344.3: these tests still cap the line count of agent.py or board.py: {', '.join(left)}"
    tree = ast.parse(open(os.path.join(ROOT, "tests", "test_board_state.py")).read())
    there = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    gone = [t for t in KEPT if t not in there]
    assert not gone, f"344.3: removing the size cap also removed these board tests: {', '.join(gone)}"


def test_the_board_tests_pass_with_agent_py_and_board_py_far_longer(record_property, tmp_path):
    """The board's tests still pass when agent.py and board.py grow by 3000 lines each.

    Copies dokima/ and tests/ into a temp folder, adds 3000 comment lines to the end of dokima/agent.py and
    dokima/board.py, and runs tests/test_board_state.py there: it must pass, so no size limit is left in it. Proves
    344.3."""
    record_property("proves", "344.3")
    for d in ("dokima", "tests"):
        shutil.copytree(os.path.join(ROOT, d), tmp_path / d, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(os.path.join(ROOT, "AGENTS.md"), tmp_path / "AGENTS.md")
    if os.path.isdir(os.path.join(ROOT, ".github")):
        shutil.copytree(os.path.join(ROOT, ".github"), tmp_path / ".github")
    for p in CAPPED:
        with open(tmp_path / p, "a") as f:
            f.write("".join(f"# padding line {k}\n" for k in range(3000)))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_board_state.py"],
                       cwd=tmp_path, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, ("344.3: with agent.py and board.py 3000 lines longer, tests/test_board_state.py fails:\n"
                               + r.stdout[-2000:] + r.stderr[-1000:])
