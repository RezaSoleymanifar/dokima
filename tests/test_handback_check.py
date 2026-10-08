"""The worker's and reviewer's hand-backs are checked against their prompt's shape and the approved plan, from outside.

Every test runs the real command the workflow runs, `python3 -m dokima.agent check review|work FILE PLAN N`, on files in
a temp folder, so it proves what a run sees: the exit code, the reasons printed, and never a crash. A plan for issue 9
with two acceptance criteria and one non-functional requirement (9.1, 9.2, 9.3) stands in for the approved plan.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

STORY = {"kind": "user_story", "user_story": "u",
         "acceptance_criteria": [{"text": "a", "source": "https://x/9"}, {"text": "b", "source": "https://x/9"}],
         "non_functional": [{"text": "c", "why": "w", "principle": "Fail closed"}],
         "scope": ["dokima/x.py"], "out_of_scope": [],
         "tests": {"9.1": ["tests/test_x.py::test_a"], "9.2": ["tests/test_x.py::test_b"], "9.3": ["tests/test_x.py::test_c"]}}
SPLIT = {"kind": "feature", "feature": "f", "stories": [
    {"title": "One", "user_story": "u1", "acceptance_criteria": [{"text": "a", "source": "https://x/9"}],
     "non_functional": [{"text": "n", "why": "w"}], "depends_on": []},
    {"title": "Two", "user_story": "u2", "acceptance_criteria": [{"text": "b", "source": "https://x/9"}],
     "non_functional": [], "depends_on": [0]}]}

# Every ask a plan review lists, matched to the story's 9.1 or a split's S1.1: a plan review must list them, a code
# review may, so the well-formed samples pass code's check on whatever stage the machine runs (#244).
ASKS = [{"ask": "Paint the door blue", "source": "https://github.com/o/r/issues/9", "criterion": "9.1"}]
SPLIT_ASKS = [dict(ASKS[0], criterion="S1.1")]
STAGES = ("", "plan", "pr")  # the stage a machine may run on: none (CI), a plan review's or a code review's

REVIEW = {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []},
          "verdict": "block", "summary": "One proof is missing.",
          "blockers": [{"id": "B1", "criterion": "9.1", "test": None, "problem": "No test.", "evidence": "plan.json", "fix": "Add one.",
                        "fixer": "worker"}],
          "notes": [{"text": "A note.", "evidence": "x.py:1"}], "outside_plan": [{"file": "a.py", "change": "c"}],
          "resolved": ["B0"], "issues_found": [{"title": "t", "why": "w", "evidence": "e"}], "asks": ASKS}
WORK = {"summary": "Cause and change.", "criteria": {"9.1": "x.py, a()", "9.2": "x.py, b()", "9.3": "x.py, c()"},
        "evidence": "pytest -q: 3 passed", "outside_scope": [{"file": "b.py", "why": "w"}],
        "suspect_tests": [{"test": "tests/test_x.py::test_a", "evidence": "e"}],
        "replies": [{"blocker": "B1", "answer": "fixed", "why": "Added it."}]}


def on_stage(monkeypatch, stage):
    """Make this machine run on `stage`, the way the workflow sets STAGE for a reviewer: none, plan or pr."""
    if stage:
        monkeypatch.setenv("STAGE", stage)
    else:
        monkeypatch.delenv("STAGE", raising=False)


def run(tmp_path, *args):
    """Run Dokima's agent command from the repo root, the way the workflow does; return (exit code, stdout, stderr)."""
    env = {**os.environ, "PYTHONPATH": ROOT}
    env.pop("PYTHONSAFEPATH", None)
    p = subprocess.run([sys.executable, "-m", "dokima.agent", *args], cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout, p.stderr


def check(tmp_path, kind, handback, plan=STORY, number="9"):
    """Write the hand-back and the plan into a temp folder and run `agent check KIND FILE PLAN N` on them."""
    f = tmp_path / f"{kind}.json"
    f.write_text(json.dumps(handback))
    p = tmp_path / "plan.json"
    p.write_text(json.dumps(plan))
    return run(tmp_path, "check", kind, str(f), str(p), number)


def assert_rejected_naming(tmp_path, kind, handback, name, crit, plan=STORY):
    """The check exits 1 without a crash and one printed reason names `name`; fails with the criterion and the case."""
    code, out, err = check(tmp_path, kind, handback, plan)
    case = json.dumps(handback)[:160]
    assert "Traceback" not in err and "Traceback" not in out, f"{crit}: the {kind} check crashed on {case}:\n{err[-600:]}"
    assert code == 1, f"{crit}: the {kind} check passed (exit {code}) a hand-back it should reject: {case}"
    assert any(name in line for line in out.splitlines()), f"{crit}: no reason names {name!r} for {case}; reasons were:\n{out}"
    return out


def test_well_formed_hand_backs_pass_and_every_malformed_field_is_named(record_property, tmp_path, monkeypatch):
    """A malformed review.json or work.json is rejected with a reason naming the field, and never crashes the check.

    A full, well-formed review and work pass first (exit 0, nothing printed), and with every optional list left out too.
    Then each required field is removed, and each field is given a value of the wrong type or an item of the wrong
    shape: a bare string where an object belongs, and an object missing any one of its fields (a note without text or
    evidence, an outside_plan or outside_scope item without its change or why, a suspect test without its test or
    evidence, a reply without why, a blocker whose test is a number). Each is rejected, the reason names the field,
    and there is no traceback.

    The good cases pass on every stage a machine may run on (STAGE unset, plan or pr), since the sample review lists
    the owner's asks as a plan review must (#244). The rule stays as strong: on a plan review, the same review with
    its asks left out is rejected naming asks, while a code review or a machine with no stage still passes it."""
    record_property("proves", "157.1")
    record_property("proves", "244.1")
    record_property("proves", "244.2")
    # A plan review must list its asks, so on that stage the bare review keeps them; every other list is optional.
    bare_review = {k: REVIEW[k] for k in ("previous_step", "verdict", "summary", "blockers", "asks")}
    bare_work = {k: WORK[k] for k in ("summary", "criteria", "evidence")}
    no_asks = {k: v for k, v in REVIEW.items() if k != "asks"}
    for stage in STAGES:
        on_stage(monkeypatch, stage)
        on = f"with STAGE={stage or 'unset'}"
        for kind, good in (("review", REVIEW), ("work", WORK)):
            code, out, err = check(tmp_path, kind, good)
            assert (code, out.strip()) == (0, ""), \
                f"157.1, 244.1: a well-formed {kind}.json was rejected {on}: {out}{err[-400:]}"
        for kind, good in (("review", bare_review), ("work", bare_work)):
            code, out, err = check(tmp_path, kind, good)
            assert (code, out.strip()) == (0, ""), \
                f"157.1, 244.1: a {kind}.json with its optional lists left out was rejected {on}: {out}{err[-400:]}"
        if stage == "plan":
            assert_rejected_naming(tmp_path, "review", no_asks, "asks", "244.2: a plan review that lists no asks")
        else:
            code, out, err = check(tmp_path, "review", no_asks)
            assert (code, out.strip()) == (0, ""), \
                f"244.2: a review with no asks was rejected {on}, where only a plan review must list them: {out}{err[-400:]}"
    on_stage(monkeypatch, "")

    for field in ("previous_step", "verdict", "summary"):
        assert_rejected_naming(tmp_path, "review", {k: v for k, v in REVIEW.items() if k != field}, field, "157.1")
    for field in ("summary", "criteria", "evidence"):
        assert_rejected_naming(tmp_path, "work", {k: v for k, v in WORK.items() if k != field}, field, "157.1")

    review_cases = [("previous_step", "did it"), ("previous_step", {"did": "one line", "decided": [], "open": []}),
                    ("verdict", 5), ("summary", 5), ("blockers", ["B1"]), ("blockers", "B1"),
                    ("blockers", [{**REVIEW["blockers"][0], "test": 5}]),
                    ("blockers", [{k: v for k, v in REVIEW["blockers"][0].items() if k != "problem"}]),
                    ("notes", 5), ("notes", ["a note"]), ("notes", [{"evidence": "x.py:1"}]), ("notes", [{"text": "n"}]),
                    ("outside_plan", 5), ("outside_plan", ["a.py"]), ("outside_plan", [{"file": "a.py"}]),
                    ("outside_plan", [{"change": "c"}]), ("resolved", 5), ("resolved", [5]),
                    ("issues_found", 5), ("issues_found", ["t"]), ("issues_found", [{"title": "t", "why": "w"}])]
    for field, value in review_cases:
        assert_rejected_naming(tmp_path, "review", {**REVIEW, field: value}, field, "157.1")
    work_cases = [("summary", 5), ("criteria", ["9.1", "9.2", "9.3"]), ("criteria", {"9.1": 5, "9.2": "b", "9.3": "c"}),
                  ("evidence", 5), ("outside_scope", 5), ("outside_scope", ["b.py"]), ("outside_scope", [{"file": "b.py"}]),
                  ("outside_scope", [{"why": "w"}]), ("suspect_tests", "x"),
                  ("suspect_tests", [{"test": "tests/test_x.py::test_a"}]), ("suspect_tests", [{"evidence": "e"}]),
                  ("replies", 5), ("replies", ["B1"]), ("replies", [{"blocker": "B1", "answer": "fixed"}])]
    for field, value in work_cases:
        assert_rejected_naming(tmp_path, "work", {**WORK, field: value}, field, "157.1")


def test_the_round_check_never_crashes_on_a_malformed_review(record_property, tmp_path):
    """The round check a run also does never crashes on a review or work.json whose lists have the wrong shape.

    Runs `agent check-round reviewer FILE PACK` with one open blocker on a review whose blockers are bare strings, and
    on one whose resolved is a number; then `agent check-round worker FILE PACK` on a work.json whose replies is a
    number, and on one whose replies are bare strings. Each exits 1 with a reason, never a traceback."""
    record_property("proves", "157.1")
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "open_blockers.json").write_text(json.dumps([REVIEW["blockers"][0]]))
    cases = [("reviewer", "review", {**REVIEW, "blockers": ["B1"]}), ("reviewer", "review", {**REVIEW, "resolved": 5}),
             ("worker", "work", {**WORK, "replies": 5}), ("worker", "work", {**WORK, "replies": ["B1"]})]
    for role, kind, bad in cases:
        f = tmp_path / f"{kind}.json"
        f.write_text(json.dumps(bad))
        code, out, err = run(tmp_path, "check-round", role, str(f), str(pack))
        assert "Traceback" not in err, f"157.1: the round check crashed on {json.dumps(bad)[:160]}:\n{err[-600:]}"
        assert code == 1 and out.strip(), f"157.1: the round check gave no reason for {json.dumps(bad)[:160]}"


def test_work_gives_a_line_for_exactly_the_plans_criteria(record_property, tmp_path):
    """A work.json missing a line for one of the plan's criteria, or giving one for a criterion the plan lacks, is rejected naming it.

    The plan has 9.1 to 9.3 (two acceptance criteria, then one non-functional). One line each passes. Leaving out 9.2,
    leaving out the non-functional 9.3, leaving out two at once, and adding 9.4 or 8.1 are each rejected, and every
    criterion at fault is named in its own reason while the criteria that are fine are not. Checked as issue 8, the
    plan's criteria are 8.1 to 8.3, so the same lines for 9.1 to 9.3 are rejected naming both 8.1 and 9.1."""
    record_property("proves", "157.2")
    code, out, err = check(tmp_path, "work", WORK)
    assert (code, out.strip()) == (0, ""), f"157.2: a line for every criterion was rejected: {out}{err[-400:]}"
    lines = WORK["criteria"]
    for missing in (["9.2"], ["9.3"], ["9.1", "9.3"]):
        crit = {k: v for k, v in lines.items() if k not in missing}
        out = assert_rejected_naming(tmp_path, "work", {**WORK, "criteria": crit}, missing[0], "157.2")
        for m in missing:
            assert m in out, f"157.2: no line for {m}, and no reason names it:\n{out}"
        for ok in set(lines) - set(missing):
            assert ok not in out, f"157.2: {ok} has its line but a reason names it:\n{out}"
    for extra in ("9.4", "8.1"):
        assert_rejected_naming(tmp_path, "work", {**WORK, "criteria": {**lines, extra: "x.py, d()"}}, extra, "157.2")
    code, out, err = check(tmp_path, "work", WORK, number="8")
    assert "Traceback" not in err, f"157.2: the work check crashed when checked as issue 8:\n{err[-600:]}"
    assert code == 1 and "9.1" in out and "8.1" in out, \
        f"157.2: checked as issue 8, a work.json with lines for 9.1 to 9.3 was not rejected naming 8.1 and 9.1:\n{out}"


def blocker(id_, criterion, test=None):
    """One well-formed blocker naming a criterion and a test."""
    return {"id": id_, "criterion": criterion, "test": test, "problem": "p", "evidence": "e", "fix": "f", "fixer": "worker"}


def test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests(record_property, tmp_path, monkeypatch):
    """A blocker naming no criterion, a criterion the plan lacks, or a test that is not the plan's for it, is rejected naming the blocker.

    Against a story plan (9.1 to 9.3): a blocker on 9.1 with no test, an empty test or 9.1's own test passes; one on
    9.3 (non-functional) passes. A blocker with no criterion, on 9.4, on S1.1, with 9.2's test or an unknown test
    for 9.1, or on 9.3 with 9.1's test is rejected, the reason names that blocker, and a good blocker beside it is not named. Against a split of
    two stories (S1.1, S1.2, S2.1): those pass with no test; S2.2, S3.1, 9.1, or S1.1 with any test are rejected.
    The good blockers pass on every stage a machine may run on (STAGE unset, plan or pr), since the sample review lists
    the owner's asks matched to the plan's own criteria (#244)."""
    record_property("proves", "157.3")
    record_property("proves", "244.1")
    good = [blocker("B1", "9.1"), blocker("B1", "9.1", ""), blocker("B1", "9.1", "tests/test_x.py::test_a"),
            blocker("B1", "9.3", "tests/test_x.py::test_c")]
    for stage in STAGES:
        on_stage(monkeypatch, stage)
        on = f"with STAGE={stage or 'unset'}"
        for b in good:
            code, out, err = check(tmp_path, "review", {**REVIEW, "blockers": [b]})
            assert (code, out.strip()) == (0, ""), \
                f"157.3, 244.1: a blocker on the plan's own criterion and test was rejected {on}: {b}\n{out}{err[-400:]}"
        for c in ("S1.1", "S1.2", "S2.1"):
            code, out, err = check(tmp_path, "review", {**REVIEW, "asks": SPLIT_ASKS, "blockers": [blocker("B1", c)]}, plan=SPLIT)
            assert (code, out.strip()) == (0, ""), \
                f"157.3, 244.1: a blocker on {c} of a two-story split was rejected {on}:\n{out}{err[-400:]}"
    on_stage(monkeypatch, "")
    bad = [blocker("B1", ""), blocker("B1", "9.4"), blocker("B1", "S1.1"),
           blocker("B1", "9.1", "tests/test_x.py::test_b"), blocker("B1", "9.1", "tests/test_x.py::test_zzz"),
           blocker("B1", "9.3", "tests/test_x.py::test_a")]
    for b in bad:
        out = assert_rejected_naming(tmp_path, "review", {**REVIEW, "blockers": [b, blocker("B2", "9.2")]}, "B1", "157.3")
        assert "B2" not in out, f"157.3: blocker B2 is on 9.2 with no test, yet a reason names it:\n{out}"

    for b in (blocker("B1", "S2.2"), blocker("B1", "S3.1"), blocker("B1", "9.1"), blocker("B1", "S1.1", "tests/test_x.py::test_a")):
        assert_rejected_naming(tmp_path, "review", {**REVIEW, "blockers": [b]}, "B1", "157.3", plan=SPLIT)


def rejected_comment(tmp_path, role, kind, handback):
    """Run the workflow's check and record steps on a bad hand-back; return the reasons printed and the comment written."""
    out_dir = tmp_path / role
    out_dir.mkdir()
    (out_dir / f"{kind}.json").write_text(json.dumps(handback))
    (tmp_path / "plan.json").write_text(json.dumps(STORY))
    code, reasons, err = run(tmp_path, "check", kind, str(out_dir / f"{kind}.json"), str(tmp_path / "plan.json"), "9")
    assert code == 1 and "Traceback" not in err, f"157.4: the {kind} check did not reject cleanly (exit {code}):\n{err[-400:]}"
    (out_dir / "check.txt").write_text(reasons)
    logs = tmp_path / "logs"
    logs.mkdir(exist_ok=True)
    env = {**os.environ, "PYTHONPATH": ROOT, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_REPOSITORY": "o/r", "GITHUB_RUN_ID": "42"}
    env.pop("PYTHONSAFEPATH", None)
    stage = "pr" if role == "reviewer" else ""
    subprocess.run([sys.executable, "-m", "dokima.agent", "record", role, stage, str(out_dir), str(out_dir / "check.txt"),
                    "false", str(logs)], cwd=ROOT, env=env, check=True, capture_output=True, text=True, timeout=30)
    return [l for l in reasons.splitlines() if l.strip()], (out_dir / "comment.md").read_text()


def test_a_rejected_hand_back_posts_one_comment_with_every_reason_and_the_run(record_property, tmp_path):
    """A rejected worker or reviewer hand-back leaves one comment listing every reason, with a link to the run.

    Runs the workflow's own check and record steps on a work.json missing 9.2 with a reply that has no why, and on a
    review.json with a blocker on 9.4 and notes that are a number. The comment written is one record with no traceback,
    says the hand-back was rejected, lists each reason the check printed (including the plan-aware ones), and links the run. The workflow
    posts that comment on every run, pass or fail, from exactly one step."""
    record_property("proves", "157.4")
    work = {**WORK, "criteria": {"9.1": "a", "9.3": "c"}, "replies": [{"blocker": "B1", "answer": "fixed"}]}
    review = {**REVIEW, "blockers": [blocker("B1", "9.4")], "notes": 5}
    for role, kind, bad, must in (("worker", "work", work, ("9.2", "replies")), ("reviewer", "review", review, ("B1", "notes"))):
        reasons, body = rejected_comment(tmp_path, role, kind, bad)
        for m in must:
            assert any(m in r for r in reasons), f"157.4: the {kind} check gave no reason naming {m}:\n" + "\n".join(reasons)
        assert body.count("<!-- dokima-record -->") == 1, f"157.4: the {role} comment does not hold exactly one record"
        assert "Traceback" not in body, f"157.4: the {role} comment shows a crash instead of the reasons:\n{body[:600]}"
        assert "hand-back rejected by code" in body, f"157.4: the {role} comment does not say the hand-back was rejected"
        for r in reasons:
            assert f"- {r}" in body, f"157.4: the {role} comment does not list the reason {r!r}"
        assert "](https://github.com/o/r/actions/runs/42)" in body, f"157.4: the {role} comment has no link to the run"
    wf = open(os.path.join(ROOT, ".github", "workflows", "agent.yml")).read()
    steps = re.split(r"\n      - ", wf)
    posting = [s for s in steps if re.search(r"gh (issue|pr) comment[^\n]*comment\.md", s)]
    assert len(posting) == 1, f"157.4: {len(posting)} workflow steps post the record comment; expected one"
    assert "if: always()" in posting[0], "157.4: the record comment is not posted when the hand-back is rejected"


def test_a_check_without_a_readable_plan_rejects_the_hand_back(record_property, tmp_path):
    """A check given a plan that is missing, not JSON or not an object rejects even a good hand-back, and says so.

    Runs `agent check work|review FILE PLAN N` with a well-formed hand-back but a plan.json that does not exist, holds
    broken JSON, or holds a list: each exits 1 with a reason naming plan.json, never a pass and never a traceback.
    Given no plan and no issue number at all, the old way of calling it, the check also exits 1 with a reason."""
    record_property("proves", "157.5")
    for kind, good in (("work", WORK), ("review", REVIEW)):
        f = tmp_path / f"{kind}.json"
        f.write_text(json.dumps(good))
        for content in (None, "{not json", "[]"):
            p = tmp_path / "plan.json"
            if p.exists():
                p.unlink()
            if content is not None:
                p.write_text(content)
            code, out, err = run(tmp_path, "check", kind, str(f), str(p), "9")
            assert "Traceback" not in err, f"157.5: the {kind} check crashed on plan.json {content!r}:\n{err[-600:]}"
            assert code == 1, f"157.5: the {kind} check passed with plan.json {'missing' if content is None else repr(content)}"
            assert "plan.json" in out, f"157.5: the reason does not name plan.json:\n{out}"
        code, out, err = run(tmp_path, "check", kind, str(f))
        assert "Traceback" not in err, f"157.5: the {kind} check crashed when given no plan at all:\n{err[-600:]}"
        assert code == 1 and out.strip(), f"157.5: the {kind} check passed (exit {code}) when given no plan at all"


def test_every_worker_and_reviewer_run_checks_against_the_plan_and_issue(record_property):
    """Every worker and reviewer run checks its hand-back against the plan in its pack and the issue's number.

    Reads the check command agent.yml gives the plan review, the pull request review and the worker, the same command
    the agent runs on itself and code runs again: each passes $PACK/plan.json and $N after the hand-back file."""
    record_property("proves", "157.5")
    wf = open(os.path.join(ROOT, ".github", "workflows", "agent.yml")).read()
    for key, kind, file in (("reviewerplan)", "review", "review.json"), ("reviewerpr)", "review", "review.json"), ("worker)", "work", "work.json")):
        line = next((l for l in wf.splitlines() if l.strip().startswith(key)), "")
        want = rf"dokima\.agent check {kind} \$OUT/{re.escape(file)} \$PACK/plan\.json \$N\b"
        assert re.search(want, line), f"157.5: the {key[:-1]} run does not check against the plan and issue number: {line.strip()}"
