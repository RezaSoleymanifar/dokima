"""Every text the owner reads is capped whole; a criterion at 12 words.

Issue #482 (story 1 of #470). Before it, only a criterion's first sentence, the summary and a docstring's first line
were capped, each with 20% slack, so criteria ran 33 to 70 words. Now every field the owner reads is held to a cap on
its whole text, and a text one word over its cap is rejected, with no slack. The summary and docstring caps keep their
rules from #239 and #240.

The caps live as named numbers in dokima/words.py, so the shared style file (#484) can quote them:

    CRITERION_CAP 12      each acceptance criterion and each non-functional requirement's text
    USER_STORY_CAP 20     the user story, a split's feature and each story's user story
    TITLE_CAP 10          each story's title
    WHY_CAP 15            each non-functional requirement's why
    OUT_OF_SCOPE_CAP 15   each out of scope line
    TEST_CHANGE_CAP 20    each reason in test_changes
    LABEL_CAP 5           each raise's label
    RAISE_TEXT_CAP 30     each raise's text
    EVIDENCE_CAP 30       each raise's evidence
    ANSWER_CAP 25         each answer's why
    PREVIOUS_STEP_CAP 15  each did, decided and open line of a review's previous_step
    BUILT_CAP 15          each line of a work hand-back's criteria
    TEST_RUN_CAP 20       a work hand-back's evidence (its own test run)

A rejection names the field the way FIELDS below writes it, then "N words" and "cap of C". The fields of a split's
story carry the prefix "story S: ". words.handback_caps(handback) returns (listed, rejected): the word-cap messages of
one hand-back and nothing else, so story 5 (#486) can send them back apart from every other check failure.

The planner's tests run `python3 -m dokima.planner check 9 OUT` through the `check` fixture of tests/test_plan_check.py;
the worker's and reviewer's run `python3 -m dokima.agent check work|review` through the `repo` fixture of
tests/test_summary_caps.py.
"""
import copy
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import words as caps  # noqa: E402
from tests.test_handback_check import REVIEW, WORK  # noqa: E402
from tests.test_plan_check import FEATURE, STORY, check  # noqa: E402,F401
from tests.test_summary_caps import repo  # noqa: E402,F401
from tests.test_word_caps import jobs, run as run_planner  # noqa: E402

CAPS = {"CRITERION_CAP": 12, "USER_STORY_CAP": 20, "TITLE_CAP": 10, "WHY_CAP": 15, "OUT_OF_SCOPE_CAP": 15,
        "TEST_CHANGE_CAP": 20, "LABEL_CAP": 5, "RAISE_TEXT_CAP": 30, "EVIDENCE_CAP": 30, "ANSWER_CAP": 25,
        "PREVIOUS_STEP_CAP": 15, "BUILT_CAP": 15, "TEST_RUN_CAP": 20}
OLD_TEST = "tests/test_old.py::test_old"


def text(n):
    """A text of exactly n words whose first sentence holds only two.

    So a cap on the first sentence alone would never catch it.
    """
    return "Two words. " + " ".join(f"w{i}" for i in range(1, n - 1)) + "." if n > 2 else " ".join(["w"] * n)


def story(n):
    """A planner story whose every owner-read field holds its cap plus n words.

    With n = 0 every field sits exactly at its cap.
    """
    c = lambda name: text(CAPS[name] + n)
    s = copy.deepcopy(STORY)
    s["user_story"] = c("USER_STORY_CAP")
    s["acceptance_criteria"][0]["text"] = c("CRITERION_CAP")
    s["non_functional"][0]["text"] = c("CRITERION_CAP")
    s["non_functional"][0]["why"] = c("WHY_CAP")
    s["out_of_scope"] = [c("OUT_OF_SCOPE_CAP")]
    s["test_changes"] = {OLD_TEST: c("TEST_CHANGE_CAP")}
    s["raises"] = [{"kind": "question", "to": "owner", "label": c("LABEL_CAP"), "text": c("RAISE_TEXT_CAP"),
                    "evidence": c("EVIDENCE_CAP")}]
    s["answers"] = [{"raise": "R1", "answer": "done", "why": c("ANSWER_CAP")}]
    return s


STORY_FIELDS = [("user story", "USER_STORY_CAP"), ("acceptance criterion 1", "CRITERION_CAP"),
                ("non-functional requirement 1", "CRITERION_CAP"), ("non-functional requirement 1 why", "WHY_CAP"),
                ("out of scope 1", "OUT_OF_SCOPE_CAP"), (f"test change {OLD_TEST}", "TEST_CHANGE_CAP"),
                ("raise 1 label", "LABEL_CAP"), ("raise 1 text", "RAISE_TEXT_CAP"),
                ("raise 1 evidence", "EVIDENCE_CAP"), ("answer 1 why", "ANSWER_CAP")]


def feature(n):
    """A planner split whose every owner-read field holds its cap plus n words."""
    c = lambda name: text(CAPS[name] + n)
    f = copy.deepcopy(FEATURE)
    f["feature"] = c("USER_STORY_CAP")
    st = f["stories"][0]
    st["title"] = c("TITLE_CAP")
    st["user_story"] = c("USER_STORY_CAP")
    st["acceptance_criteria"][0]["text"] = c("CRITERION_CAP")
    st["non_functional"] = [{"text": c("CRITERION_CAP"), "why": c("WHY_CAP"), "principle": "fail closed"}]
    return f


FEATURE_FIELDS = [("feature", "USER_STORY_CAP"), ("story 1: title", "TITLE_CAP"),
                  ("story 1: user story", "USER_STORY_CAP"), ("story 1: acceptance criterion 1", "CRITERION_CAP"),
                  ("story 1: non-functional requirement 1", "CRITERION_CAP"),
                  ("story 1: non-functional requirement 1 why", "WHY_CAP")]


def work(n):
    """A work hand-back whose owner-read fields, but its summary, hold their cap plus n words."""
    c = lambda name: text(CAPS[name] + n)
    w = copy.deepcopy(WORK)
    w["criteria"]["9.2"] = c("BUILT_CAP")
    w["evidence"] = c("TEST_RUN_CAP")
    w["raises"] = [{"kind": "blocker", "to": "planner", "label": c("LABEL_CAP"), "text": c("RAISE_TEXT_CAP"),
                    "evidence": c("EVIDENCE_CAP")}]
    w["answers"][0]["why"] = c("ANSWER_CAP")
    return w


WORK_FIELDS = [("criteria line for 9.2", "BUILT_CAP"), ("evidence", "TEST_RUN_CAP"), ("raise 1 label", "LABEL_CAP"),
               ("raise 1 text", "RAISE_TEXT_CAP"), ("raise 1 evidence", "EVIDENCE_CAP"), ("answer 1 why", "ANSWER_CAP")]


def review(n):
    """A review whose owner-read fields, but its summary, hold their cap plus n words."""
    c = lambda name: text(CAPS[name] + n)
    r = copy.deepcopy(REVIEW)
    r["previous_step"] = {"did": [c("PREVIOUS_STEP_CAP")], "decided": [c("PREVIOUS_STEP_CAP")],
                          "open": [c("PREVIOUS_STEP_CAP")]}
    r["raises"][0].update(label=c("LABEL_CAP"), text=c("RAISE_TEXT_CAP"), evidence=c("EVIDENCE_CAP"))
    r["answers"][0]["why"] = c("ANSWER_CAP")
    return r


REVIEW_FIELDS = [("did line 1", "PREVIOUS_STEP_CAP"), ("decided line 1", "PREVIOUS_STEP_CAP"),
                 ("open line 1", "PREVIOUS_STEP_CAP"), ("raise 1 label", "LABEL_CAP"),
                 ("raise 1 text", "RAISE_TEXT_CAP"), ("raise 1 evidence", "EVIDENCE_CAP"),
                 ("answer 1 why", "ANSWER_CAP")]


def names(said, where, n, cap):
    """True when one part of a check's output names `where`, its n words and cap.

    Parts are its lines, each split again at '; ', the way the planner joins its reasons.
    """
    parts = [p for line in said.splitlines() for p in line.split("; ")]
    return any(p.startswith(where + " ") and f"{n} words" in p and f"cap of {cap}" in p for p in parts)


def assert_names_every(said, fields, n, crit):
    """Fail unless the check named every field with its cap plus n words."""
    for where, cap in fields:
        assert names(said, where, CAPS[cap] + n, CAPS[cap]), \
            (f"{crit}: the rejection does not name {where!r} with its {CAPS[cap] + n} words and its cap of "
             f"{CAPS[cap]}:\n{said}")


def test_a_criterion_over_12_words_is_rejected_with_no_slack(record_property, check, capsys):
    """A criterion of 13 words is rejected; one of 12 passes.

    Proves 482.1. Acceptance criteria and non-functional requirements of exactly 12 words pass unlisted, in a story
    and a split. A 13-word criterion is rejected naming it, its 13 words and its cap of 12, whether it is one sentence
    or opens with a two-word sentence; so is a 13-word non-functional requirement and a split story's criterion.
    The old 20% slack (14 words for 12) is gone.
    """
    record_property("proves", "482.1")
    cap = getattr(caps, "CRITERION_CAP", None)
    assert cap == 12, f"482.1: dokima/words.py names no criterion cap of 12 (CRITERION_CAP is {cap})"
    plan = copy.deepcopy(STORY)
    plan["acceptance_criteria"][0]["text"] = text(12)
    plan["acceptance_criteria"][1]["text"] = " ".join(["w"] * 12)
    plan["non_functional"][0]["text"] = text(12)
    split = copy.deepcopy(FEATURE)
    split["stories"][1]["acceptance_criteria"][0]["text"] = text(12)
    for good in (plan, split):
        rc, why, printed = run_planner(check, capsys, good, jobs(), "482.1")
        assert rc == 0 and not why, f"482.1: a {good['kind']} with 12-word criteria was rejected: {why!r}"
        assert "criterion" not in printed and "requirement" not in printed, \
            f"482.1: a 12-word criterion was listed as over its cap: {printed!r}"
    plan["acceptance_criteria"][0]["text"] = " ".join(["w"] * 13)
    plan["acceptance_criteria"][1]["text"] = text(13)
    plan["non_functional"][0]["text"] = text(13)
    rc, why, _ = run_planner(check, capsys, plan, jobs(), "482.1")
    assert rc == 1, "482.1: a plan with 13-word criteria was accepted; the cap is 12 with no slack"
    for where in ("acceptance criterion 1", "acceptance criterion 2", "non-functional requirement 1"):
        assert names(why, where, 13, 12), f"482.1: the rejection does not name {where}, its 13 words and cap of 12: {why!r}"
    split["stories"][1]["acceptance_criteria"][0]["text"] = text(13)
    rc, why, _ = run_planner(check, capsys, split, jobs(), "482.1")
    assert rc == 1 and names(why, "story 2: acceptance criterion 1", 13, 12), \
        f"482.1: a split story's 13-word criterion was not rejected naming it: rc {rc}, {why!r}"


def test_every_field_of_a_plan_is_capped_on_its_whole_text(record_property, check, capsys):
    """Each plan field the owner reads, one word over its cap, is rejected by name.

    Proves 482.2. Every cap is the named number in dokima/words.py listed above. A story and a split each get every
    owner-read field one word over its cap, each text opening with a two-word sentence so a first-sentence cap would
    miss it; the planner's check rejects naming every one of those fields.
    """
    record_property("proves", "482.2")
    for name, value in CAPS.items():
        assert getattr(caps, name, None) == value, f"482.2: dokima/words.py has {name} = {getattr(caps, name, None)}, not {value}"
    rc, why, _ = run_planner(check, capsys, story(1), jobs(), "482.2")
    assert rc == 1, "482.2: a story with every owner-read field over its cap was accepted"
    assert_names_every(why, STORY_FIELDS, 1, "482.2")
    rc, why, _ = run_planner(check, capsys, feature(1), jobs(), "482.2")
    assert rc == 1, "482.2: a split with every owner-read field over its cap was accepted"
    assert_names_every(why, FEATURE_FIELDS, 1, "482.2")


def test_every_field_of_a_work_or_review_is_capped_on_its_whole_text(record_property, repo):
    """Each work or review field, one word over its cap, is rejected by name.

    Proves 482.2. A work hand-back and a review each get every owner-read field one word over its cap, each text
    opening with a two-word sentence; the worker's and reviewer's checks reject naming every one of those fields.
    """
    record_property("proves", "482.2")
    rc, out = repo("work", work(1))
    assert rc == 1, f"482.2: a work hand-back with every owner-read field over its cap was accepted:\n{out}"
    assert_names_every(out, WORK_FIELDS, 1, "482.2")
    rc, out = repo("review", review(1))
    assert rc == 1, f"482.2: a review with every owner-read field over its cap was accepted:\n{out}"
    assert_names_every(out, REVIEW_FIELDS, 1, "482.2")


def test_the_planners_check_rejects_one_long_text(record_property, check, capsys):
    """The planner's check rejects a plan whose only fault is one long raise.

    Proves 482.3. The plan passes with its raise at 30 words; at 31 words the check exits 1 and its saved reason
    names the raise's text.
    """
    record_property("proves", "482.3")
    plan = copy.deepcopy(STORY)
    plan["raises"] = [{"kind": "question", "to": "owner", "text": text(30)}]
    rc, why, _ = run_planner(check, capsys, plan, jobs(), "482.3")
    assert rc == 0 and not why, f"482.3: the planner's check rejected a 30-word raise, at its cap: {why!r}"
    plan["raises"][0]["text"] = text(31)
    rc, why, _ = run_planner(check, capsys, plan, jobs(), "482.3")
    assert rc == 1 and names(why, "raise 1 text", 31, 30), \
        f"482.3: the planner's check did not reject a 31-word raise naming it: rc {rc}, {why!r}"


def test_the_worker_and_reviewer_checks_reject_one_long_text(record_property, repo):
    """The worker's and reviewer's checks reject a hand-back whose only fault is one long raise.

    Proves 482.3. Each hand-back passes with its raise at 30 words; at 31 words each check exits 1 naming the raise's
    text.
    """
    record_property("proves", "482.3")
    w, r = copy.deepcopy(WORK), copy.deepcopy(REVIEW)
    for n in (30, 31):
        w["raises"] = [{"kind": "blocker", "to": "planner", "text": text(n)}]
        r["raises"][0]["text"] = text(n)
        for kind, h in (("work", w), ("review", r)):
            rc, out = repo(kind, h)
            if n == 30:
                assert rc == 0, f"482.3: the {kind} check rejected a 30-word raise, at its cap:\n{out}"
            else:
                assert rc == 1 and names(out, "raise 1 text", 31, 30), \
                    f"482.3: the {kind} check did not reject a 31-word raise naming it (exit {rc}):\n{out}"


def test_a_plan_rejection_names_the_field_its_word_count_and_its_cap(record_property, check, capsys):
    """A plan's rejection says which field, how many words it holds and its cap.

    Proves 482.4. A 22-word user story, then a 40-word one, are each named with their own count and the cap of 20.
    """
    record_property("proves", "482.4")
    for n in (22, 40):
        rc, why, _ = run_planner(check, capsys, dict(STORY, user_story=text(n)), jobs(), "482.4")
        assert rc == 1 and names(why, "user story", n, 20), \
            f"482.4: the rejection of a {n}-word user story does not say 'user story', '{n} words' and 'cap of 20': {why!r}"


def test_a_work_or_review_rejection_names_the_field_its_word_count_and_its_cap(record_property, repo):
    """A work or review rejection names the field, its word count and its cap.

    Proves 482.4. A worker's 26-word and 41-word answer why are named with their count and the cap of 25; a review's
    16-word did line with its count and the cap of 15.
    """
    record_property("proves", "482.4")
    for n in (26, 41):
        w = copy.deepcopy(WORK)
        w["answers"][0]["why"] = text(n)
        rc, out = repo("work", w)
        assert rc == 1 and names(out, "answer 1 why", n, 25), \
            f"482.4: the rejection of a {n}-word answer does not say 'answer 1 why', '{n} words' and 'cap of 25':\n{out}"
    r = copy.deepcopy(REVIEW)
    r["previous_step"]["did"] = [text(16)]
    rc, out = repo("review", r)
    assert rc == 1 and names(out, "did line 1", 16, 15), \
        f"482.4: the rejection of a 16-word did line does not say 'did line 1', '16 words' and 'cap of 15':\n{out}"


def test_a_plan_with_every_text_at_its_cap_still_passes(record_property, check, capsys):
    """A story and a split with every text exactly at its cap pass unlisted.

    Proves 482.5. The planner's check exits 0 on both, saves no reason and names no field as over its cap; beside
    them, the same story with its user story one word longer is rejected, so the pass is the cap's and not a check
    that caps nothing.
    """
    record_property("proves", "482.5")
    for plan in (story(0), feature(0)):
        rc, why, printed = run_planner(check, capsys, plan, jobs(), "482.5")
        assert rc == 0 and not why, f"482.5: a {plan['kind']} with every text at its cap was rejected: {why!r}"
        assert "cap of" not in printed, f"482.5: a text at its cap was listed as over it: {printed!r}"
    rc, why, _ = run_planner(check, capsys, dict(story(0), user_story=text(21)), jobs(), "482.5")
    assert rc == 1, "482.5: a story whose user story is one word over its cap of 20 passed, so the check caps nothing"


def test_a_work_or_review_with_every_text_at_its_cap_still_passes(record_property, repo):
    """A work hand-back and a review with every text at its cap pass unlisted.

    Proves 482.5. The worker's and reviewer's checks exit 0 and name no field as over its cap; beside them, each
    with its answer's why one word longer is rejected, so the pass is the cap's and not a check that caps nothing.
    """
    record_property("proves", "482.5")
    for kind, h in (("work", work(0)), ("review", review(0))):
        rc, out = repo(kind, h)
        assert rc == 0, f"482.5: a {kind} hand-back with every text at its cap was rejected:\n{out}"
        assert "cap of" not in out, f"482.5: a {kind} text at its cap was named as over it:\n{out}"
        h["answers"][0]["why"] = text(26)
        rc, out = repo(kind, h)
        assert rc == 1, f"482.5: a {kind} answer one word over its cap of 25 passed, so the check caps nothing:\n{out}"


def test_the_planners_check_never_rewrites_the_plan(record_property, check, capsys, tmp_path):
    """The planner's check leaves plan.json exactly as the planner wrote it, passing or not.

    Proves 482.6. After the check rejects a plan with every field over its cap, and after it passes one at its caps,
    plan.json is byte for byte what was handed in.
    """
    record_property("proves", "482.6")
    for plan, rejected in ((story(1), True), (story(0), False)):
        rc, why, _ = run_planner(check, capsys, plan, jobs(), "482.6")
        assert rc == int(rejected), f"482.6: the planner's check exited {rc} on a plan {'over' if rejected else 'at'} its caps: {why!r}"
        assert (tmp_path / "out" / "plan.json").read_text() == json.dumps(plan), \
            "482.6: the planner's check changed plan.json"


def test_the_worker_and_reviewer_checks_never_rewrite_the_handback(record_property, repo, tmp_path):
    """The worker's and reviewer's checks, and handback_caps, leave every hand-back as written.

    Proves 482.6. work.json and review.json are byte for byte what was handed in after their checks reject or pass
    them, and handback_caps leaves every hand-back it reads unchanged.
    """
    record_property("proves", "482.6")
    for kind, h, rejected in (("work", work(1), True), ("review", review(1), True), ("work", work(0), False),
                              ("review", review(0), False)):
        rc, out = repo(kind, h)
        assert rc == int(rejected), f"482.6: the {kind} check exited {rc} on a hand-back {'over' if rejected else 'at'} its caps:\n{out}"
        assert (tmp_path / f"{kind}.json").read_text() == json.dumps(h), f"482.6: the {kind} check changed {kind}.json"
    assert callable(getattr(caps, "handback_caps", None)), "482.6: dokima/words.py has no handback_caps to read hand-backs"
    for h in (story(1), feature(1), work(1), review(1)):
        before = copy.deepcopy(h)
        caps.handback_caps(h)
        assert h == before, "482.6: handback_caps changed the hand-back it checked"


def test_word_cap_failures_are_reported_apart_from_every_other_failure(record_property):
    """The word-cap failures of a hand-back come back on their own, without its other faults.

    Proves 482.7. handback_caps on a work hand-back with no evidence or criteria, and on a review with a bad verdict,
    returns no failure while every text is within its cap; with one raise text over its cap, it returns exactly that
    one failure, and with every field over, one failure per field and nothing else.
    """
    record_property("proves", "482.7")
    assert callable(getattr(caps, "handback_caps", None)), \
        "482.7: dokima/words.py has no handback_caps returning a hand-back's word-cap failures on their own"
    broken = [dict(work(0), criteria={}, evidence=""), dict(review(0), verdict="maybe")]
    for h in broken:
        listed, rejected = caps.handback_caps(h)
        assert rejected == [] and listed == [], \
            f"482.7: handback_caps reported other faults as word-cap failures: {listed + rejected}"
    for h in broken:
        h["raises"][0]["text"] = text(31)
        _, rejected = caps.handback_caps(h)
        assert len(rejected) == 1 and names(rejected[0], "raise 1 text", 31, 30), \
            f"482.7: handback_caps did not return exactly the one long raise: {rejected}"
    for h, fields in ((story(1), STORY_FIELDS), (feature(1), FEATURE_FIELDS), (work(1), WORK_FIELDS),
                      (review(1), REVIEW_FIELDS)):
        _, rejected = caps.handback_caps(h)
        assert len(rejected) == len(fields), \
            f"482.7: handback_caps returned {len(rejected)} failures for {len(fields)} long fields: {rejected}"
        assert_names_every("\n".join(rejected), fields, 1, "482.7")
