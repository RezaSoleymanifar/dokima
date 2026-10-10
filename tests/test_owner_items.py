"""Each question for the owner is one item with the reviewer's take (#485).

Next only says what to do.

The owner asked (#470, story 4) that a review show every raise for the owner as one item, with its icon: a few words
naming it, then "; " and the reviewer's take, in the order the raises came; that the reviewer give its take on every
question the planner asked the owner; and that Next be one sentence saying what to do and how, never quoting a raise.

What the code these tests run must do, as the plan pins it:
- In a review's run comment (`agent.render(rec, earlier=...)`), each raise for the owner is one list item whose first
  line is exactly `- <icon> **<name>**; <take>`, where <icon> is `card.field_icon(repo, "question")` or
  `card.field_icon(repo, "blocker")` by the raise's kind, <name> is the raise's label (its kind, "Question" or
  "Blocker", when it has none) and <take> is the review's why for a plan's question it answered, or the text of the
  review's own raise for the owner. Nothing else sits on that line: not the planner's full question, not Done or
  Disagree, not "for you". The only line allowed under it is the "Your words" line of an answer given on the owner's
  words.
- The plan's questions show in the order the plan raised them, whatever order the review answered them in; the
  review's own raises for the owner show in the order it raised them.
- `agent.problems_round("reviewer", handback, pack_dir)` (the `check-round reviewer` step) names, by ID, every
  question for the owner that the newest passed planner record raised and the review leaves unanswered; done or
  disagree with a why both count as a take.
- `agent.next_step(...)`: when the river stops for the owner over a raise, its words are one sentence that says what to
  answer and with which commands, and quote no raise.

Tests draw comments outside the Full record fold, the way the owner reads them.
"""
import json
import os
import re
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, card  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
REPO = "o/r"
N = 485
ISSUE = f"https://github.com/o/r/issues/{N}"
SAID = ISSUE + "#issuecomment-900"
OWNER = "boss"
FULL = re.compile(r"<details><summary>Full record</summary>.*?</details>", re.S)
META = {"run_id": "7", "run": "https://github.com/o/r/actions/runs/7", "log": "https://x/log", "models": ["claude-opus-5-5"],
        "report": {"duration_ms": 1000, "turns": 2, "cost_usd": 0.1, "tokens_in": 10, "tokens_out": 5}}

PLAN = {"kind": "user_story", "summary": "Slow calls hand back a job id.", "user_story": "Owners get a job id.",
        "acceptance_criteria": [{"text": "A slow call returns a job id.", "source": ISSUE}], "non_functional": [],
        "scope": ["dokima/agent.py"], "out_of_scope": [], "tests": {f"{N}.1": ["tests/test_a.py::test_one"]},
        "test_changes": {}, "links": {"blocked_by": [], "blocks": [], "relates_to": []}}

# The plan's questions for the owner, as code stamps them; every label, text and why is unique so a test can find it.
Q1 = {"kind": "question", "to": "owner", "label": "Board column",
      "text": "Should a cancelled run keep its column zqone? The plan assumes it does.", "evidence": "dokima/board.py",
      "raised_by": "planner", "id": "P1"}
Q2 = {"kind": "question", "to": "owner", "label": "Retry rule",
      "text": "Should a failed call retry once zqtwo? The plan assumes it does not.", "evidence": "dokima/agent.py",
      "raised_by": "planner", "id": "P2"}
Q3 = {"kind": "question", "to": "owner",
      "text": "Should the job page show its age zqthree? The plan assumes it does.", "raised_by": "planner", "id": "P3"}
A1 = {"raise": "P1", "answer": "done", "why": "Right, and you already said so, so you need not answer.",
      "words": "a cancelled run stays in its column", "source": SAID, "changes": False}
A2 = {"raise": "P2", "answer": "disagree", "why": "Likely right, but only you can say if a retry is worth its cost."}
A3 = {"raise": "P3", "answer": "disagree", "why": "Probably wrong: the issue never asks for an age, so you decide."}

# The review's own raises for the owner, and one for the planner that keeps today's line.
R1 = {"kind": "question", "to": "owner", "label": "Timeout", "text": "Is twenty seconds the right timeout zqfour?",
      "evidence": "tests/test_a.py", "raised_by": "reviewer", "id": "R4"}
R2 = {"kind": "blocker", "to": "owner", "label": "Secret key", "text": "Only you can add the key the test needs zqfive.",
      "evidence": "the run log", "raised_by": "reviewer", "id": "R5"}
R3 = {"kind": "question", "to": "owner", "text": "Should the old endpoint stay a week zqsix?", "raised_by": "reviewer",
      "id": "R6"}
R_PLANNER = {"kind": "blocker", "to": "planner", "label": "Weak test", "text": "The test passes against a stub zqseven.",
             "evidence": "tests/test_a.py", "raised_by": "reviewer", "id": "R7"}


def rec(role, stage=None, **handback):
    """One passed record as the record step builds it."""
    return {"role": role, "stage": stage, **META, "handback": handback, "check": {"passed": True, "problems": []}}


PLANNER = rec("planner", **dict(PLAN, raises=[Q1, Q2, Q3], answers=[]))


def review(answers=(), raises=(), verdict="approve", stage="plan"):
    """A review record with these answers and raises."""
    return rec("reviewer", stage, verdict=verdict, summary="Judged.", asks=[], raises=list(raises), answers=list(answers))


@pytest.fixture
def env(monkeypatch):
    """The repo the icons are served from, as the workflow sets it."""
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")


def shown(record, earlier):
    """The review's comment as the owner reads it: everything but the Full record fold."""
    return FULL.sub("", agent.render(record, earlier=earlier))


def item(text, name):
    """The one list item naming `name` in bold, as its lines.

    Fails when there is not exactly one."""
    lines = text.splitlines()
    at = [i for i, l in enumerate(lines) if l.startswith("- ") and f"**{name}**" in l]
    assert len(at) == 1, f"expected one item named **{name}**, found {len(at)}:\n{text}"
    out = [lines[at[0]]]
    for l in lines[at[0] + 1:]:
        if not (l[:1].isspace() and l.strip()):
            break
        out.append(l)
    return out


def expected(kind, name, take):
    """The exact first line of an item for the owner."""
    return f"- {card.field_icon(REPO, kind)} **{name}**; {take}"


# 485.1 and 485.2: one item per raise for the owner, with its icon, its name, then the reviewer's take.

def test_each_plan_question_shows_as_one_item_with_its_icon(record_property, env):
    """A review shows each plan question for you as one item with its icon.

    Draws a plan review that answered the plan's three questions, and checks each shows as exactly one list item
    opening with the question icon, with nothing under it but, for the one answered on your words, the line quoting
    them.

    Proves 485.1."""
    record_property("proves", "485.1")
    body = shown(review([A1, A2, A3]), [PLANNER])
    for q, name in ((Q1, "Board column"), (Q2, "Retry rule"), (Q3, "Question")):
        lines = item(body, name)
        assert lines[0].startswith("- " + card.field_icon(REPO, "question") + " "), \
            f"485.1: the item for {name!r} does not open with the question icon:\n{lines[0]}"
        under = lines[1:]
        if q is Q1:
            assert len(under) == 1 and "Your words" in under[0] and A1["words"] in under[0], \
                f"485.1: the item answered on your words must hold only the line quoting them under it:\n" + "\n".join(lines)
        else:
            assert not under, f"485.1: the item for {name!r} is more than one line:\n" + "\n".join(lines)


def test_the_reviews_own_raises_for_you_show_as_one_item_each(record_property, env):
    """A review's own raises for you show as one item each, with their icon.

    Draws a code review that raised a question, a blocker and an unlabelled question for you, and one blocker for the
    planner; checks each raise for you is one single-line item opening with its kind's icon, and the planner's blocker
    still shows as today, saying it is for the planner.

    Proves 485.1."""
    record_property("proves", "485.1")
    body = shown(review([], [R1, R2, R3, R_PLANNER], verdict="block", stage="pr"), [PLANNER])
    for r, name, kind in ((R1, "Timeout", "question"), (R2, "Secret key", "blocker"), (R3, "Question", "question")):
        lines = item(body, name)
        assert len(lines) == 1, f"485.1: the item for {name!r} is more than one line:\n" + "\n".join(lines)
        assert lines[0].startswith("- " + card.field_icon(REPO, kind) + " "), \
            f"485.1: the item for {name!r} does not open with the {kind} icon:\n{lines[0]}"
    other = [l for l in body.splitlines() if R_PLANNER["text"] in l]
    assert len(other) == 1 and "for the planner" in other[0], \
        f"485.1: a raise for the planner no longer shows as before:\n{body}"


def test_each_item_reads_its_name_then_the_reviewers_take(record_property, env):
    """Each item reads a few words naming it, then a semicolon and the reviewer's take.

    Draws a plan review that answered the plan's three questions (two labelled, one not) and checks each item's line is
    exactly the icon, the label in bold (Question when it has none), "; " and the review's why, with neither the
    planner's full question, nor Done or Disagree, nor "for you".

    Proves 485.2."""
    record_property("proves", "485.2")
    body = shown(review([A1, A2, A3]), [PLANNER])
    for q, a, name in ((Q1, A1, "Board column"), (Q2, A2, "Retry rule"), (Q3, A3, "Question")):
        first = item(body, name)[0]
        assert first == expected("question", name, a["why"]), \
            f"485.2: the item must read {expected('question', name, a['why'])!r}, it reads:\n{first}"
        assert q["text"] not in body, f"485.2: the review still shows the planner's full question {q['text']!r}:\n{body}"
        for word in ("Done", "Disagree", "for you"):
            assert word not in first, f"485.2: the item for {name!r} still says {word!r}:\n{first}"


def test_the_reviews_own_raise_reads_its_name_then_its_words(record_property, env):
    """The review's own raise for you reads its name, then what it says.

    Draws a code review that raised a question, a blocker and an unlabelled question for you, and checks each line is
    exactly the icon, the label in bold (Question when it has none), "; " and the raise's own words, with no "for you"
    and no evidence shown.

    Proves 485.2."""
    record_property("proves", "485.2")
    body = shown(review([], [R1, R2, R3], verdict="block", stage="pr"), [PLANNER])
    for r, name, kind in ((R1, "Timeout", "question"), (R2, "Secret key", "blocker"), (R3, "Question", "question")):
        first = item(body, name)[0]
        assert first == expected(kind, name, r["text"]), \
            f"485.2: the item must read {expected(kind, name, r['text'])!r}, it reads:\n{first}"
    for ev in (R1["evidence"], R2["evidence"]):
        assert ev not in body, f"485.2: an item for you still shows its evidence {ev!r}:\n{body}"


# 485.3: the reviewer gives its take on every question the plan asked the owner.

def pack(tmp_path, records):
    """A starting pack for issue #485 holding these earlier records, oldest first."""
    p = tmp_path / "pack"
    (p / "in").mkdir(parents=True)
    for i, r in enumerate(records, 1):
        (p / "in" / f"{i:02d}-{r['role']}{'-' + r['stage'] if r.get('stage') else ''}.json").write_text(json.dumps(r))
    (p / "issue.md").write_text(f"# Issue #{N}: Slow calls\n\nThe owner's ask.\n")
    (p / "open_blockers.json").write_text("[]")
    (p / "parent.json").write_text(json.dumps({"number": None}))
    return str(p)


def test_a_review_that_skips_a_plan_question_is_rejected_naming_it(record_property, tmp_path):
    """A review with no take on a plan question for you is rejected, naming it.

    Checks a plan review of a plan with three questions for you: answering only two is rejected with a problem naming
    the third by its ID; answering none names all three; answering all three, with done or disagree, passes.

    Proves 485.3."""
    record_property("proves", "485.3")
    p = pack(tmp_path, [PLANNER])
    some = agent.problems_round("reviewer", review([A2, A3])["handback"], p)
    assert some and any("P1" in s for s in some), f"485.3: a review with no take on P1 passed the round check: {some}"
    assert not any("P2" in s or "P3" in s for s in some), f"485.3: the check names questions the review answered: {some}"
    none = " ".join(agent.problems_round("reviewer", review([])["handback"], p))
    for rid in ("P1", "P2", "P3"):
        assert rid in none, f"485.3: a review with no take on any question does not name {rid}: {none}"
    every = agent.problems_round("reviewer", review([dict(A1, answer="disagree"), A2, A3])["handback"], p)
    assert every == [], f"485.3: a review with a take on every question was rejected: {every}"


def test_only_the_newest_plans_questions_need_a_take(record_property, tmp_path):
    """Only the questions of the plan under review need the reviewer's take.

    Checks a plan review after a re-plan: the old plan asked one question, the new plan two; answering the new two
    passes, and leaving one of them out is rejected naming it, never the old one.

    Proves 485.3."""
    record_property("proves", "485.3")
    old = rec("planner", **dict(PLAN, raises=[Q1], answers=[]))
    new = rec("planner", **dict(PLAN, raises=[Q2, Q3], answers=[]))
    p = pack(tmp_path, [old, review([], [R_PLANNER], verdict="block"), new])
    ok = agent.problems_round("reviewer", review([A2, A3])["handback"], p)
    assert ok == [], f"485.3: a review was asked for a take on an older plan's question: {ok}"
    left = agent.problems_round("reviewer", review([A2])["handback"], p)
    assert any("P3" in s for s in left) and not any("P1" in s for s in left), \
        f"485.3: leaving the new plan's P3 out must name P3 and only it: {left}"


def test_the_round_check_step_rejects_a_review_with_no_take(record_property, tmp_path):
    """The review's round check exits 1, naming the question left without a take.

    Runs `python3 -m dokima.agent check-round reviewer FILE PACK` as the workflow does, on a review that answers two of
    the plan's three questions, and checks it exits 1 naming the third; then on one that answers all three, exit 0.

    Proves 485.3."""
    record_property("proves", "485.3")
    p = pack(tmp_path, [PLANNER])
    env = {**os.environ, "PYTHONPATH": os.path.abspath(ROOT)}
    env.pop("PYTHONSAFEPATH", None)
    for answers, code, named in (([A2, A3], 1, "P1"), ([dict(A1, answer="disagree"), A2, A3], 0, None)):
        f = tmp_path / "review.json"
        f.write_text(json.dumps(review(answers)["handback"]))
        r = subprocess.run([sys.executable, "-m", "dokima.agent", "check-round", "reviewer", str(f), p], cwd=ROOT,
                           env=env, capture_output=True, text=True, timeout=30)
        assert r.returncode == code, f"485.3: check-round exited {r.returncode}, not {code}:\n{r.stdout}{r.stderr[-400:]}"
        if named:
            assert named in r.stdout, f"485.3: check-round does not name {named}:\n{r.stdout}"


# 485.4: items follow the order of the raises.

def positions(body, names):
    """Where each named item's line sits in the body."""
    lines = body.splitlines()
    at = [[i for i, l in enumerate(lines) if l.startswith("- ") and f"**{n}**" in l] for n in names]
    missing = [n for n, a in zip(names, at) if len(a) != 1]
    assert not missing, f"485.4: no single item named {missing} in bold, so their order cannot be read:\n{body}"
    return [a[0] for a in at]


def test_the_plans_questions_show_in_the_order_the_plan_raised_them(record_property, env):
    """The plan's questions show in the order the plan raised them.

    Draws the same plan review with its answers given in two different orders, and checks both times the items read
    Board column, Retry rule, then Question, as the plan raised them.

    Proves 485.4."""
    record_property("proves", "485.4")
    for answers in ([A3, A1, A2], [A2, A3, A1]):
        at = positions(shown(review(answers), [PLANNER]), ["Board column", "Retry rule", "Question"])
        assert at == sorted(at), f"485.4: answered in the order {[a['raise'] for a in answers]}, the items " \
                                 f"are not in the plan's order (lines {at})"


def test_the_reviews_own_raises_for_you_keep_the_order_it_raised_them(record_property, env):
    """The review's own raises for you show in the order it raised them.

    A blocker raised after a question stays after it.

    Draws a code review that raised for you a question, then a blocker, then another question, and checks the items
    read in that order; then the same raises the other way round, and checks they follow.

    Proves 485.4."""
    record_property("proves", "485.4")
    for raised, names in (([R1, R2, R3], ["Timeout", "Secret key", "Question"]),
                          ([R3, R2, R1], ["Question", "Secret key", "Timeout"])):
        at = positions(shown(review([], raised, verdict="block", stage="pr"), [PLANNER]), names)
        assert at == sorted(at), f"485.4: raised as {names}, the items show out of that order (lines {at})"


# 485.5: Next is one sentence saying what to do and how, quoting no raise.

def comment(record, at):
    """The bot's comment carrying a record, as GitHub lists it."""
    return {"author": {"login": agent.BOT}, "body": agent.render(record), "createdAt": at, "url": f"{ISSUE}#c-{at}"}


def one_sentence(why):
    """True when the words are one sentence ending in a full stop.

    Commands in backticks are set aside first, so `/plan` is no sentence end."""
    plain = re.sub(r"`[^`]*`", "CMD", why).strip()
    return plain.endswith(".") and len(re.findall(r"[.!?](?=\s|$)", plain)) == 1


def check_next(why, raised, commands, case):
    """Assert the river's words are one plain sentence naming each command."""
    assert one_sentence(why), f"485.5: {case}: Next is not one sentence: {why!r}"
    assert '"' not in why, f"485.5: {case}: Next quotes something: {why!r}"
    for r in raised:
        assert r["text"] not in why and r["text"].split("?")[0] not in why, f"485.5: {case}: Next quotes a raise: {why!r}"
    assert "answer" in why.lower(), f"485.5: {case}: Next does not say what to do (answer): {why!r}"
    for c in commands:
        assert f"`{c}`" in why, f"485.5: {case}: Next does not say how, with `{c}`: {why!r}"


def test_next_after_a_plan_with_questions_or_a_blocker_for_you_is_one_plain_sentence(record_property):
    """After a plan asks you something, Next is one plain sentence.

    Runs the river on a plan with questions for you (off autopilot) and on a plan with a blocker for you, and checks
    each stops for you with one sentence that says to answer, names the commands, and quotes no raise.

    Proves 485.5."""
    record_property("proves", "485.5")
    blocker = {"kind": "blocker", "to": "owner", "label": "Key", "text": "Only you can add the key zqeight.",
               "raised_by": "planner", "id": "P4"}
    for raised, commands, case in (([Q1, Q2], ["/plan", "/review"], "a plan with questions"),
                                   ([blocker], ["/plan"], "a plan with a blocker for you")):
        planner = rec("planner", **dict(PLAN, raises=raised, answers=[]))
        step = agent.next_step([], planner, {OWNER}, autopilot=lambda: False, body="", number=str(N))
        assert step[0] == "stop", f"485.5: {case} did not stop for you: {step}"
        check_next(step[1], raised, commands, case)


def test_next_after_a_review_that_asks_you_is_one_plain_sentence(record_property):
    """After a review asks you something, Next is one plain sentence.

    Runs the river on a code review that raised a question and a blocker for you, and on an approving plan review on
    autopilot that left the plan's questions to you; checks each stops with one sentence that says to answer, names
    the commands, and quotes no raise.

    Proves 485.5."""
    record_property("proves", "485.5")
    step = agent.next_step([comment(PLANNER, "2026-10-10T10:00:00Z")], review([], [R1, R2], verdict="block", stage="pr"),
                           {OWNER}, autopilot=lambda: False, body="", number=str(N))
    assert step[0] == "stop", f"485.5: a review with raises for you did not stop: {step}"
    check_next(step[1], [R1, R2], ["/plan", "/work", "/review"], "a review that raised for you")
    step = agent.next_step([comment(PLANNER, "2026-10-10T10:00:00Z")], review([A2, A3]), {OWNER},
                           autopilot=lambda: True, body="", number=str(N))
    assert step[0] == "stop", f"485.5: a plan review that left questions to you did not stop: {step}"
    check_next(step[1], [Q1, Q2, Q3], ["/plan", "/work"], "a plan review that left questions to you")
