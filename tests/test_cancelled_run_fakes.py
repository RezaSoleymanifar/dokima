"""The fake plan review the cancelled-run tests feed is one code's check accepts, so they test what they say (#215).

tests/test_cancelled_run.py feeds a blocking plan review (BLOCK) to runs on a one-story plan for issue 57, whose only
criterion is 57.1. BLOCK was built from test_start.APPROVE, whose ask names S1.1, a criterion only a split has; once
#158's asks check landed, code rejected that hand-back, so the "blocked" run no longer sent the plan back to the
planner and main went red. These tests run the real check the workflow runs on a plan review
(`python3 -m dokima.agent check review FILE PLAN N`, with STAGE=plan) against the fake plan those runs use.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

import test_cancelled_run as tcr  # noqa: E402
from test_start import N, STORY  # noqa: E402

from dokima import agent  # noqa: E402


def check_review(tmp_path, review, name):
    """Run code's plan-review check on a review against the cancelled-run tests' fake plan; (exit code, output)."""
    path, plan = tmp_path / f"{name}.json", tmp_path / "plan.json"
    path.write_text(json.dumps(review))
    plan.write_text(json.dumps(STORY))
    r = subprocess.run([sys.executable, "-m", "dokima.agent", "check", "review", str(path), str(plan), N],
                       cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, STAGE="plan"), timeout=60)
    return r.returncode, r.stdout + r.stderr


def test_the_fake_blocking_review_matches_its_asks_to_the_fake_plan(record_property, tmp_path):
    """The fake blocking plan review matches every ask to a criterion the fake plan has, and code's check accepts it.

    Reads BLOCK from tests/test_cancelled_run.py: it must still block, on 57.1, and every ask it lists must name one of
    the fake plan's own criteria (57.1), not "missing" and not a split's S1.1. Then runs code's real plan-review check
    on it against that plan: it must pass with no problems. Beside it, the same review with its ask moved to S1.1 must
    still be rejected for naming a criterion the plan does not have, so the fix is in the fake, not a looser check."""
    record_property("proves", "215.2")
    ids = agent.plan_criteria(STORY, N)
    assert ids == ["57.1"], f"215.2: setup: the fake plan's criteria are {ids}, expected ['57.1']"
    block = tcr.BLOCK
    assert block.get("verdict") == "block" and [b.get("criterion") for b in block.get("blockers", [])] == ["57.1"], \
        f"215.2: the fake review is no longer a block on 57.1, so the river test no longer tests a blocking review: {block}"
    asks = block.get("asks")
    assert isinstance(asks, list) and asks, f"215.2: the fake blocking review lists no asks: {asks!r}"
    wrong = [a for a in asks if not isinstance(a, dict) or a.get("criterion") not in ids]
    assert not wrong, (f"215.2: the fake blocking review matches asks to criteria the fake plan does not have "
                       f"(it has {ids}): {wrong}")
    code, out = check_review(tmp_path, block, "block")
    assert code == 0, f"215.2: code's check rejects the fake blocking review (exit {code}):\n{out}"
    bad = dict(block, asks=[dict(a, criterion="S1.1") for a in asks])
    code, out = check_review(tmp_path, bad, "bad")
    assert code == 1 and "is matched to S1.1, which is not a criterion of the plan" in out, \
        f"215.2: code's check no longer rejects an ask matched to S1.1 on a one-story plan (exit {code}):\n{out}"
