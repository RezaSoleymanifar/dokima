"""An agent's hand-back is checked by code before anyone else sees it: well formed passes, every malformation is named."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, fence  # noqa: E402

GOOD_REVIEW = {"previous_step": {"did": ["Split the issue into four stories."], "decided": [], "open": ["Three questions."]},
               "stage": "plan", "round": 1, "verdict": "block", "summary": "One test is missing.",
               "blockers": [{"id": "B1", "criterion": "9.1", "test": None, "problem": "No good-case test.",
                             "evidence": "18 passed against a stub.", "fix": "Add one."}],
               "notes": [], "outside_plan": [], "resolved": []}
GOOD_WORK = {"summary": "Cause and change.", "criteria": {"9.1": "dokima/x.py, parse()"},
             "evidence": "pytest -q: 12 passed", "replies": [{"blocker": "B1", "answer": "fixed", "why": "Added it."}]}


def test_a_good_review_passes_and_each_malformation_is_named(record_property):
    """A well-formed review has no problems; an approve with blockers, a block without, a bad stage and a bare blocker are each named."""
    record_property("proves", "agent.1")
    assert agent.problems_review(GOOD_REVIEW) == []
    assert agent.problems_review({**GOOD_REVIEW, "verdict": "approve"}) == ["an approve has no blockers"]
    assert agent.problems_review({**GOOD_REVIEW, "blockers": []}) == ["a block needs at least one blocker"]
    assert "stage must be" in agent.problems_review({**GOOD_REVIEW, "stage": "x"})[0]
    bare = agent.problems_review({**GOOD_REVIEW, "blockers": [{"id": "B1"}]})
    assert {"blocker B1 has no criterion", "blocker B1 has no evidence", "blocker B1 has no fix"} <= set(bare)
    assert agent.problems_review({**GOOD_REVIEW, "notes": [{}] * 4}) == ["at most three notes"]


def test_a_good_work_passes_and_each_malformation_is_named(record_property):
    """A well-formed work.json has no problems; missing criteria, missing evidence and a reply without a reason are each named."""
    record_property("proves", "agent.2")
    assert agent.problems_work(GOOD_WORK) == []
    assert agent.problems_work({**GOOD_WORK, "criteria": {}}) == ["criteria must give one line per criterion"]
    assert "evidence is empty" in agent.problems_work({**GOOD_WORK, "evidence": " "})[0]
    assert "reply to B1" in agent.problems_work({**GOOD_WORK, "replies": [{"blocker": "B1", "answer": "maybe"}]})[0]


def test_check_fails_closed_on_missing_or_broken_files(record_property, tmp_path, capsys):
    """A missing file or invalid JSON is a failure with its reason, never a pass; a good file passes."""
    record_property("proves", "agent.3")
    assert agent.check("review", str(tmp_path / "none.json")) == 1
    (tmp_path / "bad.json").write_text("{not json")
    assert agent.check("work", str(tmp_path / "bad.json")) == 1
    (tmp_path / "ok.json").write_text(json.dumps(GOOD_REVIEW))
    assert agent.check("review", str(tmp_path / "ok.json")) == 0
    assert "missing" in capsys.readouterr().out


def test_the_fence_reads_scope_from_plan_json(record_property, tmp_path, monkeypatch):
    """Given plan.json, the fence uses its scope list exactly."""
    record_property("proves", "agent.4")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"scope": ["app.py"]}))
    seen = {}
    monkeypatch.setattr(fence, "fence", lambda base, scope: seen.setdefault("scope", scope) and [])
    fence.main(["fence", "BASE", str(plan)])
    assert seen["scope"] == ["app.py"]


def test_only_the_planner_asks_and_its_questions_are_checked(record_property):
    """Plain questions pass; anything that is not a plain question is named; review and work may not ask."""
    record_property("proves", "agent.5")
    q = "Should a failed run move its card to Needs you? I planned for yes."
    assert agent.problems_questions([q, "Which board view?"]) == []
    assert agent.problems_questions(["Split it."]) == ["question 1 must be a plain question with a '?'"]
    assert agent.problems_questions([{"question": "Split it?"}]) == ["question 1 must be a plain question with a '?'"]
    assert agent.problems_review({**GOOD_REVIEW, "questions": [q]}) == ["the reviewer never asks the owner; escalate on round three instead"]
    assert agent.problems_work({**GOOD_WORK, "questions": [q]}) == ["the worker never asks the owner; the plan is the contract"]


def comment(rec, who="dokima-runtime", t="2026-10-06T10:00:00Z"):
    """A comment as GitHub returns it, carrying a record rendered by code."""
    return {"author": {"login": who}, "body": agent.render(rec), "createdAt": t, "where": "issue #7"}


def rec(role, stage="", handback=None, passed=True, problems=""):
    """A record built the way the workflow builds one, from a temp hand-back folder."""
    import tempfile
    out = tempfile.mkdtemp()
    json.dump(handback or {}, open(os.path.join(out, agent.HANDBACK[role]), "w"))
    return agent.build_record(role, stage, out, problems, passed, {"run_id": "1", "run": "https://x/run/1"})


def test_a_record_survives_its_comment_and_only_the_bot_counts(record_property):
    """A record rendered into a comment reads back exactly; the same text posted by anyone else, or broken JSON, is not a record."""
    record_property("proves", "agent.6")
    r = rec("planner", handback={"kind": "user_story", "user_story": "first", "questions": ["Split it?"]})
    assert agent.records([comment(r)]) == [r]
    assert agent.records([comment(r, who="someone")]) == [], "a pasted record from a person was trusted"
    broken = comment(r)
    broken["body"] = broken["body"].replace('"role"', '"role', 1)
    assert agent.records([broken]) == []
    body = agent.render(r)
    assert body.startswith(agent.MARK) and "first" in body and "Split it?" in body and "<details>" in body


def test_only_passed_plans_count_and_rejections_are_kept(record_property):
    """A rejected plan stays in the trail with its problems but is never the plan; a passed record lists no problems."""
    record_property("proves", "agent.7")
    ok = rec("planner", handback={"kind": "user_story", "user_story": "first"}, problems="feature\n")
    bad = rec("planner", handback={"kind": "user_story", "user_story": "second"}, passed=False, problems="criterion 7.2 has no test\n")
    recs = agent.records([comment(ok), comment(bad)])
    assert ok["check"]["problems"] == [], "a passed record listed the checker's normal output as a problem"
    assert agent.latest(recs, "planner")["handback"]["user_story"] == "first"
    assert agent.latest(recs, "planner", passed=False)["check"]["problems"] == ["criterion 7.2 has no test"]
    assert "hand-back rejected by code" in agent.render(bad)


def test_a_missing_hand_back_is_recorded_as_missing(record_property, tmp_path):
    """A run that handed back nothing still leaves a record saying so, never an empty or invented hand-back."""
    record_property("proves", "agent.8")
    r = agent.build_record("worker", "", str(tmp_path), "work.json is missing\n", False, {})
    assert "work.json" in r["handback"]["missing"] and r["check"] == {"passed": False, "problems": ["work.json is missing"]}


def test_the_models_used_come_from_the_session_log(record_property, tmp_path):
    """The record names every model that appears in the run's session log, so a wrong model is visible and can fail the run."""
    record_property("proves", "agent.9")
    log = tmp_path / "logs" / ".claude" / "proj"
    log.mkdir(parents=True)
    (log / "s.jsonl").write_text("\n".join(json.dumps(x) for x in [
        {"message": {"model": "claude-opus-5-5"}}, {"type": "user"}, {"message": {"model": "claude-sonnet-5-5"}}]) + "\nnot json\n")
    assert agent.models_used(str(tmp_path / "logs")) == ["claude-opus-5-5", "claude-sonnet-5-5"]
    assert agent.models_used(str(tmp_path / "none")) == []


def test_the_worker_starts_only_on_a_plan_the_reviewer_approved(record_property):
    """No review, a blocking review, or an approval of an older plan keeps the worker out; an approval of the newest plan lets it in."""
    record_property("proves", "agent.10")
    plan = rec("planner", handback={"kind": "user_story"})
    block = rec("reviewer", "plan", GOOD_REVIEW)
    ok = rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})
    assert not agent.approved([plan])
    assert not agent.approved([plan, block])
    assert agent.approved([plan, block, ok])
    assert not agent.approved([plan, ok, plan]), "an approval of an older plan let the worker in on a newer one"


def test_a_pack_missing_anything_its_role_needs_is_refused(record_property, tmp_path):
    """A complete pack passes for each role; a missing plan, an empty issue, no comments section, a broken record or a PR pack without the worker's log is named."""
    record_property("proves", "agent.11")
    d = tmp_path / "pack"
    (d / "in").mkdir(parents=True)
    (d / "issue.md").write_text("# Issue #9: t\n\nbody\n\n## Comments\n")
    assert agent.problems_pack("planner", "", str(d)) == []
    assert agent.problems_pack("worker", "", str(d)) == ["plan.json is missing"]
    (d / "plan.json").write_text(json.dumps({"kind": "user_story"}))
    assert agent.problems_pack("reviewer", "plan", str(d)) == []
    assert agent.problems_pack("worker", "", str(d)) == []
    (d / "diff.patch").write_text("+x\n")
    (d / "tests.txt").write_text("1 passed\n")
    (d / "tests.xml").write_text("<testsuite/>\n")
    assert agent.problems_pack("reviewer", "pr", str(d)) == ["worker-run is missing"]
    (d / "worker-run" / "p").mkdir(parents=True)
    assert agent.problems_pack("reviewer", "pr", str(d)) == ["worker-run holds no session log"]
    (d / "worker-run" / "home" / ".claude" / "p").mkdir(parents=True)
    (d / "worker-run" / "home" / ".claude" / "p" / "s.jsonl").write_text("{}\n")
    assert agent.problems_pack("reviewer", "pr", str(d)) == []
    (d / "in" / "01-planner.json").write_text("{not json")
    assert agent.problems_pack("planner", "", str(d)) == ["record 01-planner.json is not valid JSON"]
    (d / "in" / "01-planner.json").write_text(json.dumps({"role": "planner"}))
    assert agent.problems_pack("planner", "", str(d)) == ["record 01-planner.json lacks role, handback or check"]
    (d / "in" / "01-planner.json").unlink()
    (d / "issue.md").write_text("   \n")
    assert agent.problems_pack("planner", "", str(d)) == ["issue.md is empty", "issue.md has no comments section"]


def test_the_pack_reads_the_issue_and_its_pr_as_one_conversation(record_property, tmp_path, monkeypatch):
    """Comments from the issue, its PR, PR reviews and line notes on the code arrive in time order, each labeled with where it was written; records come from both."""
    record_property("proves", "agent.12")
    plan = rec("planner", handback={"kind": "user_story", "user_story": "s"})
    def fake_gh(*args):
        if args[:2] == ("issue", "view"):
            return json.dumps({"number": 7, "title": "T", "body": "B", "comments": [
                {"author": {"login": "owner"}, "body": "/plan first", "createdAt": "2026-01-01T00:00:01Z"},
                {"author": {"login": "dokima-runtime"}, "body": agent.render(plan), "createdAt": "2026-01-01T00:00:03Z"}]})
        if args[:2] == ("pr", "list"):
            return json.dumps([{"number": 9}] if "try/issue-7" in args else [])
        if args[:2] == ("pr", "view"):
            return json.dumps({"comments": [{"author": {"login": "owner"}, "body": "/work change it", "createdAt": "2026-01-01T00:00:04Z"}],
                               "reviews": [{"author": {"login": "owner"}, "body": "line note", "submittedAt": "2026-01-01T00:00:02Z", "state": "COMMENTED"}]})
        if args[0] == "api" and args[1].endswith("/pulls/9/comments"):
            return json.dumps([{"user": {"login": "owner"}, "body": "rename this", "created_at": "2026-01-01T00:00:05Z", "path": "x.py", "line": 3}])
        raise AssertionError(args)
    monkeypatch.setattr(agent, "gh", fake_gh)
    assert agent.pack("o/r", 7, "reviewer", "plan", str(tmp_path / "p"))
    text = (tmp_path / "p" / "issue.md").read_text()
    order = [text.index(x) for x in ("/plan first", "line note", "dokima-record", "/work change it", "rename this")]
    assert order == sorted(order), "the conversation is not in time order"
    assert "on PR #9 review (commented)" in text and "on issue #7" in text and "on PR #9 line note on x.py:3" in text
    assert json.load(open(tmp_path / "p" / "plan.json")) == {"kind": "user_story", "user_story": "s"}
    assert (tmp_path / "p" / "in" / "01-planner.json").exists()


def test_a_command_starts_its_stage_and_anything_else_starts_nothing(record_property):
    """/plan, /work and /review on the first line route to their stage with the right issue; prose, a later-line command or an unlinked PR start nothing."""
    record_property("proves", "agent.13")
    assert agent.route("/plan tighten story 2\nmore words", False, 139) == {"role": "planner", "stage": "", "issue": "139"}
    assert agent.route("/review", False, 139) == {"role": "reviewer", "stage": "plan", "issue": "139"}
    assert agent.route("/review look at x.py", True, 150, "try/issue-139") == {"role": "reviewer", "stage": "pr", "issue": "139"}
    assert agent.route("/WORK fix the line notes", True, 150, "feature-x", "Closes #42") == {"role": "worker", "stage": "", "issue": "42"}
    assert agent.route("looks good to me", False, 139) is None
    assert agent.route("thoughts first\n/plan later", False, 139) is None, "a command not on the first line started a stage"
    assert agent.route("/planner", False, 139) is None
    assert agent.route("/work", True, 150, "feature-x", "no link here") is None, "a PR with no issue started a stage"
    assert agent.route("", False, 139) is None


def test_each_round_answers_every_open_blocker(record_property, tmp_path):
    """Planner and worker must answer every open blocker by id; the reviewer must resolve or keep each earlier one."""
    record_property("proves", "agent.14")
    (tmp_path / "open_blockers.json").write_text(json.dumps([{"id": "B1"}, {"id": "B2"}]))
    assert agent.problems_round("worker", {"replies": [{"blocker": "B1"}, {"blocker": "B2"}]}, str(tmp_path)) == []
    assert agent.problems_round("planner", {"replies": [{"blocker": "B1"}]}, str(tmp_path)) == ["blocker B2 is not answered"]
    assert agent.problems_round("reviewer", {"resolved": ["B1"], "blockers": [{"id": "B2"}]}, str(tmp_path)) == []
    assert agent.problems_round("reviewer", {"resolved": ["B1"], "blockers": []}, str(tmp_path)) == ["earlier blocker B2 is neither resolved nor still listed"]
    assert agent.problems_round("worker", {}, str(tmp_path / "none")) == []


def test_open_blockers_come_from_the_newest_review_at_that_stage(record_property):
    """A blocking review leaves its blockers open; a later approval clears them; another stage's review never counts."""
    record_property("proves", "agent.15")
    plan = rec("planner", handback={"kind": "user_story"})
    block = rec("reviewer", "plan", GOOD_REVIEW)
    ok = rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})
    assert [b["id"] for b in agent.open_blockers([plan, block], "plan")] == ["B1"]
    assert agent.open_blockers([plan, block, ok], "plan") == []
    assert agent.open_blockers([plan, block], "pr") == []


def test_dokimas_own_code_always_runs_from_main(record_property):
    """The runtime is copied from main before any branch is checked out, every Dokima step runs from that copy, and only tests use the branch's code."""
    record_property("proves", "agent.19")
    wf = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "agent.yml")).read()
    assert wf.index("cp -r dokima /tmp/runtime/dokima") < wf.index("name: Starting branch")
    assert "PYTHONPATH: /tmp/runtime" in wf and 'PYTHONSAFEPATH: "1"' in wf
    assert "cat /tmp/runtime/dokima/roles/" in wf and "cat dokima/roles/" not in wf
    for line in wf.splitlines():
        if "python3 -m pytest" in line:
            assert "PYTHONPATH= PYTHONSAFEPATH=" in line, f"tests would run Dokima from main instead of the branch: {line.strip()}"


def test_the_review_sums_up_the_previous_step_in_at_most_five_lines(record_property):
    """A review without a summary of what the planner or worker did, or with more than five lines of it, is named."""
    record_property("proves", "agent.16")
    assert agent.problems_review({**GOOD_REVIEW, "previous_step": {}}) == ["previous_step must sum up what the planner or worker did, decided and left open"]
    long = {"did": ["a", "b", "c"], "decided": ["d", "e"], "open": ["f"]}
    assert agent.problems_review({**GOOD_REVIEW, "previous_step": long}) == ["previous_step holds at most five lines"]
    body = agent.render(rec("reviewer", "plan", GOOD_REVIEW))
    assert "What the previous step did" in body and "Split the issue into four stories." in body


def test_the_conversation_is_saved_readable_and_without_secrets(record_property, tmp_path):
    """The transcript shows what the agent said, the tools it used and their results, and every secret value is removed."""
    record_property("proves", "agent.17")
    log = tmp_path / ".claude" / "p"
    log.mkdir(parents=True)
    secret = "sk-ant-oat01-SECRETSECRET"
    lines = [{"message": {"role": "assistant", "content": [{"type": "text", "text": "Reading the issue."},
                                                         {"type": "tool_use", "name": "Bash", "input": {"command": f"echo {secret}"}}]}},
             {"message": {"role": "user", "content": [{"type": "tool_result", "content": f"token {secret}"}]}}]
    (log / "s.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n")
    t = agent.transcript(str(tmp_path), [secret])
    assert "**Agent:** Reading the issue." in t and "1. Bash" in t and "> token" in t
    assert secret not in t and "[secret removed]" in t
    assert agent.scrub("abc", ["short"]) == "abc"


def test_the_footnote_reports_claudes_own_numbers_and_links_the_conversation(record_property, tmp_path):
    """Time, turns, tokens and cost come from Claude's end-of-run report; a missing report shows none of them, never a guess."""
    record_property("proves", "agent.18")
    (tmp_path / "claude.json").write_text(json.dumps({"duration_ms": 240000, "num_turns": 23, "total_cost_usd": 3.2,
                                                       "usage": {"input_tokens": 1000, "cache_read_input_tokens": 400000, "output_tokens": 18000}}))
    r = {"models": ["claude-opus-5-5"], "report": agent.run_report(str(tmp_path / "claude.json")), "log": "https://g/log.md", "run": "https://g/run"}
    f = agent.footnote(r)
    assert all(x in f for x in ("Opus 5.5", "4.0 min", "23 turns", "401,000 tokens in, 18,000 out", "$3.20 at API prices", "[conversation](https://g/log.md)"))
    bare = agent.footnote({"models": ["claude-opus-5-5"], "report": agent.run_report(str(tmp_path / "none.json"))})
    assert "min" not in bare and "$" not in bare and "tokens" not in bare
