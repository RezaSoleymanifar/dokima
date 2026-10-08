"""The planner hands back no concerns or replies, and five criteria per story at most.

The owner asked (story 3 of #229) that a doubt about the ask go in as a question, not a concern; that the planner stop
answering blockers with replies, since the reviewer already resolves or keeps each one itself; that questions keep
reaching the owner; and that a story with more than five criteria be split. Every check here runs the way the planner
workflow runs it: `planner check` through planner.main inside a temp git repo (the `check` fixture of
tests/test_plan_check.py), then `python3 -m dokima.agent check-round planner FILE PACK` on a starting pack built in a
temp folder. The card is drawn with agent.render, the code that writes every record comment.
"""
import copy
import json
import os
import re
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent  # noqa: E402
from tests.test_plan_check import FEATURE, ISSUE, STORY, check  # noqa: E402,F401
from tests.test_run_cards import rec, top  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
QUESTIONS = [{"question": "Should job ids be numbers?", "assumption": "The plan assumes they are strings."},
             {"question": "Should a failed run move to Needs you?", "assumption": "The plan assumes it does."}]
BLOCKERS = [{"id": "B1", "criterion": "9.1", "test": None, "problem": "p", "evidence": "e", "fix": "f", "fixer": "planner"},
            {"id": "B2", "criterion": "9.2", "test": None, "problem": "p", "evidence": "e", "fix": "f", "fixer": "planner"}]
# Every plan names the open issues it is blocked by, blocks and relates to (#256); these plans link none.
NO_LINKS = {"blocked_by": [], "blocks": [], "relates_to": []}


def round_check(tmp_path, role, handback, blockers=BLOCKERS):
    """Run a role's round check on a pack where `blockers` are still open.

    The check runs as `agent check-round ROLE FILE PACK` from the repo root.

    The pack is built the way the planner's real pack is: issue #9 with no open issues to link (open_issues.json is
    an empty list, #256). PYTHONPATH points at the repo so the check that runs is this repo's code, never another copy
    of dokima."""
    pack = tmp_path / f"pack-{role}"
    pack.mkdir(exist_ok=True)
    (pack / "open_blockers.json").write_text(json.dumps(blockers))
    (pack / "issue.md").write_text("# Issue #9: T\n\n## Comments\n")
    (pack / "open_issues.json").write_text("[]")
    f = tmp_path / f"{role}-handback.json"
    f.write_text(json.dumps(handback))
    r = subprocess.run([sys.executable, "-m", "dokima.agent", "check-round", role, str(f), str(pack)],
                       cwd=ROOT, capture_output=True, text=True, timeout=60, env=dict(os.environ, PYTHONPATH=ROOT))
    assert "Traceback" not in r.stderr, f"the round check crashed: {r.stderr}"
    return r.returncode, r.stdout + r.stderr


def both_checks(check, tmp_path, plan, crit, blockers=BLOCKERS):
    """Run the planner check, then its round check: (passed, every reason given).

    A plan with no links gets three empty lists, as every real hand-back carries them, so only this issue's rules decide."""
    plan = plan if "links" in plan else with_(plan, links=NO_LINKS)
    rc, why = check({"plan.json": plan}, crit)
    rc2, why2 = round_check(tmp_path, "planner", plan, blockers)
    return rc == 0 and rc2 == 0, (why + "\n" + why2).strip()


def with_(base, **fields):
    """A copy of the good story or feature with the given fields set."""
    p = copy.deepcopy(base)
    p.update(fields)
    return p


def sized(base, n, story=1):
    """A copy of the good plan with one story holding n criteria in all.

    The story keeps its one non-functional requirement and gets n - 1 acceptance criteria. A user story files 9.1 under
    test_id, 9.2 and 9.3 under test_unique (whose docstrings name exactly those), and 9.4 and up under the older test
    tests/test_old.py::test_old, which counts as proof and needs no docstring naming them; so nothing but the count
    can be wrong."""
    p = copy.deepcopy(base)
    target = p if p["kind"] == "user_story" else p["stories"][story - 1]
    nfr = [{"text": "A failed call says why.", "why": "the owner is never left guessing", "principle": "fail closed"}]
    target["acceptance_criteria"] = [{"text": f"Outcome {k} is shown.", "source": ISSUE} for k in range(1, n)]
    target["non_functional"] = nfr
    if p["kind"] == "user_story":
        name = {1: "tests/test_jobs.py::test_id", 2: "tests/test_jobs.py::test_unique", 3: "tests/test_jobs.py::test_unique"}
        p["tests"] = {f"9.{k}": [name.get(k, "tests/test_old.py::test_old")] for k in range(1, n + 1)}
    return p


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
def test_a_plan_with_concerns_is_rejected_saying_a_doubt_goes_in_as_a_question(record_property, check, tmp_path, base):
    """A plan with concerns is rejected: a doubt goes in as a question.

    Proves 241.1, for a user story and a split.

    On a first round, first checks the good plan with no concerns field passes both checks. Then hands it back with one concern, and with
    an empty concerns list, and checks each is rejected with a reason naming concerns and saying "a doubt about the
    ask goes in as a question"."""
    record_property("proves", "241.1")
    ok, why = both_checks(check, tmp_path, copy.deepcopy(base), "241.1", [])
    assert ok, f"241.1: a good {base['kind']} with no concerns was rejected: {why!r}"
    for concerns in ([{"text": "This overlaps #12.", "evidence": "dokima/board.py"}], []):
        ok, why = both_checks(check, tmp_path, with_(base, concerns=concerns), "241.1", [])
        assert not ok, f"241.1: a {base['kind']} with concerns {concerns} passed the check"
        assert "concerns" in why and "a doubt about the ask goes in as a question" in why, \
            f"241.1: the rejection of concerns does not say a doubt about the ask goes in as a question: {why!r}"


def test_the_prompt_and_agents_md_no_longer_offer_concerns(record_property):
    """The planner's prompt and AGENTS.md say a doubt goes in as a question.

    Proves 241.1.

    Reads dokima/roles/planner.md: it never shows a "concerns" field, no example line starts with "- Concern:", and
    some line says a doubt goes in as a question. Reads the Planner line of AGENTS.md's Roles: it no longer says the
    planner raises a concern, and it says a doubt about the ask goes in as a question."""
    record_property("proves", "241.1")
    prompt = open(os.path.join(ROOT, "dokima", "roles", "planner.md")).read()
    assert '"concerns"' not in prompt, "241.1: the planner's prompt still offers a \"concerns\" field"
    assert not [l for l in prompt.splitlines() if l.lstrip().startswith("- Concern:")], \
        "241.1: the planner's prompt still shows a concern example"
    assert [l for l in prompt.splitlines() if re.search(r"\bdoubt", l, re.I) and re.search(r"\bquestion", l, re.I)], \
        "241.1: the planner's prompt never says a doubt about the ask goes in as a question"
    agents = open(os.path.join(ROOT, "AGENTS.md")).read()
    line = next((l for l in agents.splitlines() if l.startswith("- **Planner:**")), "")
    assert line, "241.1: AGENTS.md lost its Planner line in Roles"
    assert "concern" not in line.lower(), f"241.1: AGENTS.md's Planner line still raises a concern: {line!r}"
    assert re.search(r"doubt.*question", line, re.I), \
        f"241.1: AGENTS.md's Planner line does not say a doubt about the ask goes in as a question: {line!r}"


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
def test_a_plan_with_replies_is_rejected_saying_replies_are_no_longer_part_of_a_plan(record_property, check, tmp_path, base):
    """A plan carrying replies is rejected, saying replies are no longer part of a plan.

    Proves 241.2, for a user story and a split.

    Hands back the good plan with a reply answering each open blocker, and with an empty replies list, and checks
    each is rejected with a reason naming replies and saying "replies are no longer part of a plan"."""
    record_property("proves", "241.2")
    full = [{"blocker": b, "answer": "fixed", "why": "Fixed it."} for b in ("B1", "B2")]
    for replies in (full, []):
        ok, why = both_checks(check, tmp_path, with_(base, replies=replies), "241.2")
        assert not ok, f"241.2: a {base['kind']} with replies {replies} passed the check"
        assert "replies are no longer part of a plan" in why, \
            f"241.2: the rejection of replies does not say replies are no longer part of a plan: {why!r}"


def test_the_prompt_no_longer_asks_the_planner_for_replies(record_property):
    """The planner's prompt no longer asks for replies.

    Proves 241.2.

    Reads dokima/roles/planner.md and checks the word "replies" appears nowhere in it, neither the field nor the
    instruction to answer every open blocker in replies."""
    record_property("proves", "241.2")
    prompt = open(os.path.join(ROOT, "dokima", "roles", "planner.md")).read()
    found = [l for l in prompt.splitlines() if re.search(r"\breplies\b", l, re.I)]
    assert not found, f"241.2: the planner's prompt still asks for replies: {found}"


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
def test_a_later_round_plan_with_no_replies_passes_and_the_reviewer_still_carries_each_blocker(record_property, check, tmp_path, base):
    """A later-round plan with no replies passes; the reviewer still resolves or keeps each blocker.

    Proves 241.3.

    With B1 and B2 open from the newest review, hands back the good plan with no replies and checks both the planner
    check and the planner's round check pass. Then runs the reviewer's round check: a review that resolves B1 and
    keeps B2 passes, while one that drops B2 is rejected naming B2."""
    record_property("proves", "241.3")
    ok, why = both_checks(check, tmp_path, copy.deepcopy(base), "241.3")
    assert ok, f"241.3: a later-round {base['kind']} with no replies was rejected: {why!r}"
    kept = {"resolved": ["B1"], "blockers": [BLOCKERS[1]]}
    rc, why = round_check(tmp_path, "reviewer", kept)
    assert rc == 0, f"241.3: a review resolving B1 and keeping B2 was rejected: {why!r}"
    rc, why = round_check(tmp_path, "reviewer", {"resolved": ["B1"], "blockers": []})
    assert rc != 0 and "B2" in why, f"241.3: a review that drops the open blocker B2 passed, or did not name it: {why!r}"


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
def test_questions_still_pass_and_reach_the_owner_on_a_later_round(record_property, check, tmp_path, base):
    """A plan's questions still pass on a later round and still show on its card.

    Proves 241.4.

    With B1 and B2 open, hands back the good plan carrying two questions and no replies, and checks both checks pass.
    Then draws the planner's run comment and checks each question and its assumption show above the folds."""
    record_property("proves", "241.4")
    plan = with_(base, questions=QUESTIONS)
    ok, why = both_checks(check, tmp_path, plan, "241.4")
    assert ok, f"241.4: a later-round {base['kind']} with questions and no replies was rejected: {why!r}"
    short = top(agent.render(rec("planner", handback=plan)))
    for q in QUESTIONS:
        assert q["question"] in short and q["assumption"] in short, \
            f"241.4: the card does not show the question {q['question']!r} with its assumption above the folds:\n{short}"


@pytest.mark.parametrize("base,story", [(STORY, 1), (FEATURE, 1), (FEATURE, 2)], ids=["story", "split-story-1", "split-story-2"])
def test_a_story_with_more_than_five_criteria_is_rejected_saying_split_it(record_property, check, tmp_path, base, story):
    """A story with more than five criteria is rejected, saying it should be split.

    Proves 241.5; non-functional requirements count too.

    On a first round, hands back a story (or a split whose first or second story is resized) with exactly five criteria, four acceptance
    and one non-functional, and checks it passes. Then with six, and with seven, and checks each is rejected with a
    reason saying "more than five criteria" and "split", naming the story for a split."""
    record_property("proves", "241.5")
    ok, why = both_checks(check, tmp_path, sized(base, 5, story), "241.5", [])
    assert ok, f"241.5: a {base['kind']} with exactly five criteria was rejected: {why!r}"
    for n in (6, 7):
        ok, why = both_checks(check, tmp_path, sized(base, n, story), "241.5", [])
        assert not ok, f"241.5: a {base['kind']} with {n} criteria (story {story}) passed the check"
        assert "more than five criteria" in why and "split" in why, \
            f"241.5: the rejection of {n} criteria does not say more than five criteria means a split: {why!r}"
        if base["kind"] == "feature":
            assert f"story {story}" in why, f"241.5: the rejection does not name story {story}: {why!r}"
