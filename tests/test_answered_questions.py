"""A question the reviewer answers from the owner's words shows plainly (#238, story 5 of #230).

When the plan reviewer accepts a planner question's assumption on the owner's own words, the run comment shows the
question, the answer below it (the plan's assumption for that question) and the evidence (the owner's matched words,
linked to where they said them). Today render() packs all of that into one line under "The plan's assumptions:" and
never shows the answer at all.

These tests run the workflow's own record step, `python3 -m dokima.agent record reviewer plan OUT check.txt true LOGS`,
with the reviewed plan in `$PACK/plan.json` (the job-wide PACK of agent.yml, where the plan reviewer's plan lives), and
read the comment it writes to OUT/comment.md. The answer of a question is the "assumption" the plan gave it.

What the comment must hold, pinned here:
    the section     a heading line holding the words "Answered from your words", then the list under it: every line
                    after the heading up to the first non-empty line that is neither a list item ("- " or "1. ") nor
                    indented under one
    each answer     inside the section, the question on one line, the answer on a later line and the evidence on a
                    later line still; the evidence is a markdown link whose text holds the matched words and whose
                    target is the source: the issue or comment link as given, or for "AGENTS.md" the file on the
                    repo's main branch, https://github.com/o/r/blob/main/AGENTS.md
    no blank heading  a line that is only a bold heading ending in a colon (an icon may lead it) is always followed,
                    past blank lines, by a list item
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
REPO = "o/r"
ISSUE = "https://github.com/o/r/issues/238"
COMMENT = ISSUE + "#issuecomment-555"
AGENTS = "https://github.com/o/r/blob/main/AGENTS.md"
HEADING = "Answered from your words"

Q1 = "Should a failed run move its card to Needs you?"
A1 = "The plan assumes it does, so the owner sees it without looking."
M1 = "a failed run lands in Needs you"
Q2 = "Should the board column change on a cancelled run?"
A2 = "The plan assumes the column stays where it was."
M2 = "Fail closed."
Q3 = "Should the answer show the owner's name?"
A3 = "The plan assumes it does not, so the card stays short."
Q4 = "Should a story with no tests be shown?"
A4 = "The plan assumes it is shown greyed out."


def plan(*questions):
    """A small approved-shape plan carrying the given (question, assumption) pairs."""
    return {"kind": "user_story", "summary": "Cards.", "user_story": "Cards show what matters.",
            "acceptance_criteria": [{"text": "A card shows the stage.", "source": ISSUE}],
            "non_functional": [], "scope": ["dokima/agent.py"], "out_of_scope": [],
            "tests": {"238.1": ["tests/test_x.py::test_a"]}, "test_changes": {},
            "questions": [{"question": q, "assumption": a} for q, a in questions]}


def accepted(q, matched, source):
    """A plan review's judgement accepting a question's assumption on the owner's words."""
    return {"question": q, "accepted": True, "changes": False, "matched": matched, "source": source}


def refused(q):
    """A plan review's judgement not accepting a question's assumption."""
    return {"question": q, "accepted": False, "changes": True, "why": "It changes how the board works."}


def comment(tmp_path, the_plan, assumptions):
    """Run the workflow's record step on a passed plan review; return the comment it wrote."""
    out, pack, logs = tmp_path / "out", tmp_path / "pack", tmp_path / "logs"
    for d in (out, pack, logs):
        d.mkdir(parents=True)
    (pack / "plan.json").write_text(json.dumps(the_plan))
    review = {"verdict": "approve", "summary": "The plan holds.", "blockers": [], "notes": [], "issues_found": [],
              "asks": [], "assumptions": assumptions}
    (out / "review.json").write_text(json.dumps(review))
    (out / "check.txt").write_text("")
    env = {**os.environ, "PYTHONPATH": ROOT, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_REPOSITORY": REPO,
           "GITHUB_RUN_ID": "42", "PACK": str(pack), "STAGE": "plan"}
    env.pop("PYTHONSAFEPATH", None)
    r = subprocess.run([sys.executable, "-m", "dokima.agent", "record", "reviewer", "plan", str(out),
                        str(out / "check.txt"), "true", str(logs)], cwd=ROOT, env=env, capture_output=True, text=True,
                       timeout=30)
    assert r.returncode == 0 and (out / "comment.md").exists(), \
        f"the record step failed on a passed plan review (exit {r.returncode}):\n{r.stderr[-800:]}"
    return (out / "comment.md").read_text()


def visible(text):
    """The part of the comment the owner sees without opening a fold."""
    return text.split("<details", 1)[0]


def section(text):
    """The lines of the answered-question section, or None when the comment has none."""
    lines = visible(text).splitlines()
    at = [i for i, l in enumerate(lines) if HEADING in l]
    if not at:
        return None
    body = []
    for l in lines[at[0] + 1:]:
        if l.strip() and not (re.match(r"\s*(- |\d+\. )", l) or l[:1].isspace()):
            break
        body.append(l)
    return body


def blank_headings(text):
    """Every bold heading line ending in a colon with no list item under it."""
    lines = visible(text).splitlines()
    bad = []
    for i, l in enumerate(lines):
        if re.fullmatch(r"\s*(<img[^>]*>\s*)?\*\*[^*]+:\*\*\s*", l):
            nxt = next((x for x in lines[i + 1:] if x.strip()), "")
            if not re.match(r"\s*(- |\d+\. )", nxt):
                bad.append(l)
    return bad


def line_of(body, needle):
    """The index of the first line in body holding needle, or -1."""
    return next((i for i, l in enumerate(body) if needle in l), -1)


def link(matched, source):
    """A markdown link whose text holds the matched words and whose target is the source."""
    return re.compile(r"\[[^\]]*" + re.escape(matched) + r"[^\]]*\]\(" + re.escape(source) + r"\)")


def check_answered(body, q, a, matched, target, crit):
    """Assert the section shows q, then a, then the matched words linked to target."""
    iq, ia = line_of(body, q), line_of(body, a)
    ie = next((i for i, l in enumerate(body) if link(matched, target).search(l)), -1)
    assert iq >= 0, f"{crit}: the answered section does not show the question \"{q}\":\n" + "\n".join(body)
    assert ia >= 0, f"{crit}: the answered section does not show the answer \"{a}\" (the plan's assumption):\n" + "\n".join(body)
    assert ie >= 0, (f"{crit}: the answered section has no link [..\"{matched}\"..]({target}) giving the owner's "
                     "words and where they said them:\n" + "\n".join(body))
    assert iq < ia < ie, (f"{crit}: the section must show the question, then the answer below it, then the evidence "
                          f"below that; got lines {iq}, {ia}, {ie}:\n" + "\n".join(body))


def test_an_accepted_question_shows_the_question_then_its_answer_then_the_owners_words_linked(record_property, tmp_path):
    """An answered question shows the question, its answer, then the owner's words linked.

    Records a plan review that accepted two questions, one on a comment of the issue and one on AGENTS.md, and checks
    the comment's "Answered from your words" section shows each question, the plan's assumption on a line below it,
    and below that the matched words as a link to the comment, or to AGENTS.md on the repo's main branch.
    Proves 238.1."""
    record_property("proves", "238.1")
    text = comment(tmp_path, plan((Q1, A1), (Q2, A2)),
                   [accepted(Q1, M1, COMMENT), accepted(Q2, M2, "AGENTS.md")])
    body = section(text)
    assert body is not None, (f"238.1: a plan review that accepted two questions on the owner's words shows no "
                              f"\"{HEADING}\" section:\n{visible(text)}")
    check_answered(body, Q1, A1, M1, COMMENT, "238.1")
    check_answered(body, Q2, A2, M2, AGENTS, "238.1")


def test_no_answered_question_means_no_section_and_no_blank_heading(record_property, tmp_path):
    """With no question answered, the comment shows no answered section and no empty heading.

    Records three plan reviews: one of a plan with no questions, one that accepted none of two questions, and one that
    accepted a question. Only the last shows the "Answered from your words" section; the first two show no such
    heading, neither shows a plan's answer, and no comment has a heading with nothing under it. Proves 238.2."""
    record_property("proves", "238.2")
    none = comment(tmp_path / "a", plan(), [])
    refused_all = comment(tmp_path / "b", plan((Q1, A1), (Q2, A2)), [refused(Q1), refused(Q2)])
    one = comment(tmp_path / "c", plan((Q1, A1), (Q2, A2)), [accepted(Q1, M1, COMMENT), refused(Q2)])
    for name, text in (("a plan with no questions", none), ("a review that accepted no question", refused_all)):
        assert HEADING not in visible(text), f"238.2: {name} still shows a \"{HEADING}\" section:\n{visible(text)}"
        for a in (A1, A2):
            assert a not in visible(text), f"238.2: {name} shows the answer \"{a}\" though it answered nothing:\n{visible(text)}"
    for name, text in (("a plan with no questions", none), ("a review that accepted no question", refused_all),
                       ("a review that accepted one question", one)):
        assert not blank_headings(text), f"238.2: {name} shows a heading with nothing under it: {blank_headings(text)}"
    assert section(one) is not None and line_of(section(one), Q1) >= 0, \
        f"238.2: a review that accepted a question shows no \"{HEADING}\" section with it:\n{visible(one)}"


def test_only_an_assumption_accepted_with_the_owners_words_and_source_shows_as_answered(record_property, tmp_path):
    """Only a question accepted with the owner's words and their source shows as answered.

    Records a plan review with four questions: one accepted with words and source, one not accepted, one accepted with
    no matched words and one accepted with no source. Only the first appears in the "Answered from your words"
    section; the other three questions and their answers appear nowhere in it. Proves 238.3."""
    record_property("proves", "238.3")
    text = comment(tmp_path, plan((Q1, A1), (Q2, A2), (Q3, A3), (Q4, A4)),
                   [accepted(Q1, M1, COMMENT), refused(Q2), accepted(Q3, "", COMMENT), accepted(Q4, "the words", "")])
    body = section(text)
    assert body is not None, f"238.3: a review that accepted a question on the owner's words shows no \"{HEADING}\" section:\n{visible(text)}"
    check_answered(body, Q1, A1, M1, COMMENT, "238.3")
    for q, a, why in ((Q2, A2, "was not accepted"), (Q3, A3, "has no matched words"), (Q4, A4, "has no source")):
        assert line_of(body, q) < 0 and line_of(body, a) < 0, \
            f"238.3: the question \"{q}\" {why} but is shown as answered:\n" + "\n".join(body)
