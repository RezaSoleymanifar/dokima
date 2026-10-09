"""Tests for #375: the manifest declares main's merge queue, and the audit asks for it.

GitHub offers a merge queue on public repos of an organization and on private repos of an organization on Enterprise
Cloud; personal-account repos never have one. The manifest (`dokima/manifest.py`) declares main's queue as optional,
and the drift audit (`dokima/audit.py`) reports on the Setup issue a queue that is missing where GitHub offers one, a
queue on with other settings, or a queue it could not check. Dokima never switches the queue on itself.

The first half hands `audit.compare` and `audit.run` the in-memory GitHub of tests/test_audit.py, whose
merge_queue(repo, branch) answer each test sets. The second half runs `python3 -m dokima.audit acme/widgets` from
outside against the fake `gh` of tests/fake_gh.py (through tests/test_audit_cli.py's Audit), which proves the real
command reads the repo, its organization's plan and main's active rules from GitHub:
    gh api repos/OWNER/REPO                       owner type and visibility
    gh api orgs/OWNER                             the organization's plan (only needed for a private repo)
    gh api repos/OWNER/REPO/rules/branches/main   main's active rules; a merge_queue rule means the queue is on
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import test_audit as ta  # noqa: E402
import test_audit_cli as tc  # noqa: E402
from dokima import manifest  # noqa: E402

REPO = "acme/widgets"
DECLARED = {"merge_method": "SQUASH", "grouping_strategy": "ALLGREEN", "max_entries_to_build": 5,
            "max_entries_to_merge": 5}
# GitHub's rule carries settings Dokima does not declare; they are never compared.
LIVE = dict(DECLARED, min_entries_to_merge=1, min_entries_to_merge_wait_minutes=5, check_response_timeout_minutes=60)
SWITCH_ON = "only the owner can switch it on"


def queue_lines(lines):
    """The lines that speak about a merge queue."""
    return [l for l in lines if "merge queue" in l.lower()]


def with_queue(answer):
    """The in-memory GitHub, matching the manifest, whose main has the given queue answer."""
    g = ta.GitHub()
    g.queues["main"] = answer
    return g


def declared_queues(criterion):
    """The manifest's declared merge queues, or a failure naming the criterion."""
    queues = getattr(manifest, "MERGE_QUEUES", None)
    assert queues is not None, f"{criterion}: dokima/manifest.py declares no MERGE_QUEUES"
    return queues


# 375.1: the manifest declares main's merge queue as optional: squash, all-green groups, up to 5 at a time

def test_the_manifest_declares_mains_merge_queue_as_optional(record_property):
    """The manifest declares main's queue as optional: squash, all-green, up to 5 at once.

    Proves 375.1. Reads manifest.MERGE_QUEUES and checks it declares exactly one queue, main's, marked optional, merging by squash,
    grouping all-green, and building and merging at most 5 pull requests at a time, in GitHub's own rule parameters."""
    record_property("proves", "375.1")
    queues = declared_queues("375.1")
    assert set(queues) == {"main"}, f"375.1: the manifest declares merge queues for {sorted(queues)}, not only main"
    want = dict(DECLARED, optional=True)
    assert queues["main"] == want, f"375.1: main's merge queue is declared as {queues['main']}, not {want}"


# 375.2: where GitHub offers a queue and main has none, the Setup issue says only the owner can switch it on

def test_a_missing_queue_puts_one_line_on_the_setup_issue_marked_needs_you(record_property, tmp_path):
    """A missing queue gets one Setup issue line: only the owner can switch it on.

    Proves 375.2. Every other setting matches the manifest; GitHub offers a queue and main has none. The audit opens the Setup
    issue, marks it Needs you, and the issue has exactly one line about the merge queue, naming main and saying only
    the owner can switch it on."""
    record_property("proves", "375.2")
    g = with_queue({"offered": True, "queue": None})
    n = ta.audit("375.2").run(g, REPO, ta.codeowners(tmp_path, "* @alice\n"))
    assert n is not None and n in g.issues, f"375.2: a missing merge queue opened no Setup issue; writes: {g.writes}"
    issue = g.issues[n]
    assert issue["needs_you"], f"375.2: the Setup issue about the missing merge queue is not marked Needs you"
    lines = queue_lines(ta.body_lines(issue["body"]))
    assert len(lines) == 1, f"375.2: the Setup issue should have one line about the merge queue, it has {lines}"
    assert re.search(r"(?<![\w-])main(?![\w-])", lines[0]), f"375.2: the merge queue line does not name main: {lines[0]!r}"
    assert SWITCH_ON in lines[0].lower(), f"375.2: the merge queue line does not say {SWITCH_ON!r}: {lines[0]!r}"


def test_a_queue_on_as_declared_gets_no_line(record_property):
    """A queue on as declared is read and gets no line.

    Proves 375.2. GitHub offers a queue and main has one with the declared settings, plus settings Dokima does not declare. The
    audit reads main's queue and gives no line at all, so a clean repo still writes nothing."""
    record_property("proves", "375.2")
    g = with_queue({"offered": True, "queue": dict(LIVE)})
    lines = ta.audit("375.2").compare(g, REPO)
    assert (REPO, "main") in g.queue_reads, f"375.2: the audit never read main's merge queue; it read {g.queue_reads}"
    assert lines == [], f"375.2: a merge queue on as declared should give no line, it gave {lines}"


def test_a_queue_on_with_other_settings_gets_one_line_per_difference(record_property):
    """A queue on with other settings gets one line per setting that differs.

    Proves 375.2. Main's queue merges with MERGE instead of SQUASH and groups HEADGREEN instead of ALLGREEN, with the rest as
    declared. The audit gives exactly two merge queue lines: one naming MERGE and SQUASH, one naming HEADGREEN and
    ALLGREEN, each naming main and saying only the owner can change it."""
    record_property("proves", "375.2")
    g = with_queue({"offered": True, "queue": dict(LIVE, merge_method="MERGE", grouping_strategy="HEADGREEN")})
    lines = queue_lines(ta.audit("375.2").compare(g, REPO))
    assert len(lines) == 2, f"375.2: two different settings should give two merge queue lines, got {lines}"
    for words in (("MERGE", "SQUASH"), ("HEADGREEN", "ALLGREEN")):
        line = ta.one_line(lines, "375.2", f"main's queue setting {words[0]}", *words)
        assert re.search(r"(?<![\w-])main(?![\w-])", line), f"375.2: the line does not name main: {line!r}"
        assert "only the owner" in line.lower(), f"375.2: the line does not say only the owner can change it: {line!r}"


def test_the_audit_command_reports_a_missing_queue_on_a_public_org_repo(record_property, tmp_path):
    """The audit command reports main's missing queue on a public organization repo.

    Proves 375.2. Runs `python3 -m dokima.audit acme/widgets` against a fake gh: a public repo of the organization acme, clean in
    every setting, with no merge_queue rule on main. The command opens one Setup issue marked Needs you whose only
    line is about the merge queue, naming main and saying only the owner can switch it on."""
    record_property("proves", "375.2")
    s = tc.clean()
    s["account"] = {"type": "Organization", "visibility": "public", "plan": "free"}
    a = tc.Audit(tmp_path, s)
    a.run("375.2")
    n, issue = tc.created(a, "375.2")
    queue = queue_lines(tc.body_lines(issue["body"]))
    assert len(queue) == 1, f"375.2: the Setup issue should have one merge queue line, it has {queue}\n{a.why()}"
    assert re.search(r"(?<![\w-])main(?![\w-])", queue[0]) and SWITCH_ON in queue[0].lower(), \
        f"375.2: the merge queue line should name main and say {SWITCH_ON!r}: {queue[0]!r}"
    assert not a.state().get("unsupported"), f"375.2: the command made calls the fake gh does not answer\n{a.why()}"
    card = a.state()["items"].get(f"PVTI_I_{n}", {})
    assert card.get("Action") == tc.manifest_option("Action", "Needs you"), \
        f"375.2: the Setup issue's card is not marked Needs you: {card}\n{a.why()}"


def test_the_audit_command_writes_nothing_when_the_queue_is_on_as_declared(record_property, tmp_path):
    """The audit command writes nothing when main's queue is on as declared.

    Proves 375.2. A clean public repo of the organization acme whose main has a merge_queue rule with the declared settings. The
    command reads main's rules, makes no call the fake does not answer, and writes nothing to GitHub."""
    record_property("proves", "375.2")
    s = tc.clean()
    s["account"] = {"type": "Organization", "visibility": "public", "plan": "free"}
    s["queue"] = {"main": dict(LIVE)}
    a = tc.Audit(tmp_path, s)
    p = a.run("375.2")
    after = a.state()
    assert any(f"repos/{REPO}/rules/branches/main" in arg for c in after["calls"] for arg in c), \
        f"375.2: the command never read main's rules: {after['calls']}"
    assert not after.get("unsupported"), f"375.2: the command made calls the fake gh does not answer\n{a.why()}"
    assert after["writes"] == [], f"375.2: a queue on as declared should write nothing, it wrote {after['writes']}"
    assert p.returncode == 0, f"375.2: the command exited {p.returncode}:\n{p.stdout}\n{p.stderr}"


def test_the_audit_command_reports_a_missing_queue_on_an_enterprise_private_repo(record_property, tmp_path):
    """A missing queue on an Enterprise Cloud private repo is reported too.

    Proves 375.2. A clean private repo of the organization acme on the enterprise plan, with no merge_queue rule on main. The
    command opens one Setup issue with one merge queue line saying only the owner can switch it on."""
    record_property("proves", "375.2")
    s = tc.clean()
    s["account"] = {"type": "Organization", "visibility": "private", "plan": "enterprise"}
    a = tc.Audit(tmp_path, s)
    a.run("375.2")
    n, issue = tc.created(a, "375.2")
    queue = queue_lines(tc.body_lines(issue["body"]))
    assert len(queue) == 1 and SWITCH_ON in queue[0].lower(), \
        f"375.2: the Setup issue should have one line saying {SWITCH_ON!r}, it has {queue}\n{a.why()}"


# 375.3: where GitHub offers no queue, the audit says nothing about it and nothing fails

def test_no_queue_offered_gives_no_line_and_no_writes(record_property, tmp_path):
    """Where GitHub offers no queue, the audit says nothing and writes nothing.

    Proves 375.3. Every setting matches the manifest and GitHub offers the repo no merge queue. compare() reads main's queue and
    gives no line; run() returns None and writes nothing to GitHub."""
    record_property("proves", "375.3")
    audit = ta.audit("375.3")
    g = with_queue({"offered": False})
    lines = audit.compare(g, REPO)
    assert (REPO, "main") in g.queue_reads, f"375.3: the audit never asked GitHub about main's merge queue"
    assert lines == [], f"375.3: a repo GitHub offers no queue should get no line, it got {lines}"
    g = with_queue({"offered": False})
    assert audit.run(g, REPO, ta.codeowners(tmp_path, "* @alice\n")) is None, "375.3: run() touched a Setup issue"
    assert g.writes == [], f"375.3: a repo GitHub offers no queue got writes: {g.writes}"


def test_the_audit_command_is_silent_on_repos_github_offers_no_queue(record_property, tmp_path):
    """Personal repos and private repos without Enterprise Cloud get no writes, and exit 0.

    Proves 375.3. Runs the command twice against a fake gh with no merge_queue rule on main: once as a public personal repo, once
    as a private repo of an organization on the team plan. Each run exits 0, makes no call the fake does not answer
    and writes nothing; the second also proves the command asked GitHub, since it read the repo."""
    record_property("proves", "375.3")
    for account in ({"type": "User", "visibility": "public", "plan": None},
                    {"type": "Organization", "visibility": "private", "plan": "team"}):
        case = tmp_path / account["type"]
        case.mkdir()
        s = tc.clean()
        s["account"] = account
        a = tc.Audit(case, s)
        p = a.run("375.3")
        after = a.state()
        assert any(c[:1] == ["api"] and any(arg.strip("/").split("?")[0] == f"repos/{REPO}" for arg in c)
                   for c in after["calls"]), f"375.3: the command never read the repo itself: {after['calls']}"
        assert not after.get("unsupported"), f"375.3: calls the fake gh does not answer ({account})\n{a.why()}"
        assert after["writes"] == [], f"375.3: a repo GitHub offers no queue ({account}) got writes: {after['writes']}"
        assert p.returncode == 0, f"375.3: the command exited {p.returncode} ({account}):\n{p.stdout}\n{p.stderr}"


# 375.4: when GitHub cannot say whether main has a queue, the Setup issue says so with GitHub's reason

def test_an_unreadable_queue_says_could_not_be_verified(record_property, tmp_path):
    """An unreadable queue gets one line saying it could not be verified, with GitHub's reason.

    Proves 375.4. Every setting matches the manifest, but reading main's queue is refused with 403. The audit opens the Setup issue
    with exactly one merge queue line, naming main, saying it could not be verified and giving GitHub's reason."""
    record_property("proves", "375.4")
    g = with_queue({"offered": True, "queue": None})
    g.fail["merge_queue"] = ta.FORBIDDEN
    n = ta.audit("375.4").run(g, REPO, ta.codeowners(tmp_path, "* @alice\n"))
    assert n is not None and n in g.issues, f"375.4: an unreadable merge queue opened no Setup issue: {g.writes}"
    lines = queue_lines(ta.body_lines(g.issues[n]["body"]))
    assert len(lines) == 1, f"375.4: the Setup issue should have one merge queue line, it has {lines}"
    line = lines[0]
    assert re.search(r"(?<![\w-])main(?![\w-])", line), f"375.4: the line does not name main: {line!r}"
    assert "could not be verified" in line.lower(), f"375.4: the line does not say could not be verified: {line!r}"
    assert "Resource not accessible by integration" in line, f"375.4: the line does not give GitHub's reason: {line!r}"


def test_the_audit_command_reports_refused_queue_reads_with_githubs_reason(record_property, tmp_path):
    """Refused reads of main's rules or the repo say could not be verified, with why.

    Proves 375.4. Runs the command against a clean public organization repo with no queue twice: once with main's rules refused
    with 502, once with the repo itself refused with 403. Each run opens a Setup issue whose one merge queue line
    names main, says it could not be verified and gives GitHub's reason, and never claims the queue is missing."""
    record_property("proves", "375.4")
    for what, why in (("rules", tc.BROKEN), ("repo", tc.FORBIDDEN)):
        case = tmp_path / what
        case.mkdir()
        s = tc.clean()
        s["account"] = {"type": "Organization", "visibility": "public", "plan": "free"}
        s["fail"] = {what: why}
        a = tc.Audit(case, s)
        a.run("375.4")
        n, issue = tc.created(a, "375.4")
        lines = queue_lines(tc.body_lines(issue["body"]))
        assert len(lines) == 1, f"375.4: refused {what}: one merge queue line expected, got {lines}\n{a.why()}"
        line = lines[0]
        assert re.search(r"(?<![\w-])main(?![\w-])", line) and "could not be verified" in line.lower(), \
            f"375.4: refused {what}: the line should name main and say could not be verified: {line!r}"
        assert why in line, f"375.4: refused {what}: the line does not give GitHub's reason {why!r}: {line!r}"
        assert SWITCH_ON not in line.lower(), f"375.4: refused {what}: an unread queue was reported missing: {line!r}"


# 375.5: Dokima never turns the merge queue on or changes it, and the app keeps administration: read

def test_dokima_only_reads_the_queue_and_keeps_administration_read(record_property, tmp_path):
    """Dokima only reads the queue, never writes a rule, and keeps administration: read.

    Proves 375.5. Runs the command against a clean public organization repo with no merge queue. It reads main's rules and opens
    the Setup issue, and every write it makes is to an issue or the board: no call is a POST, PUT, PATCH or DELETE
    on a ruleset, a rule or branch protection. The manifest still grants the app administration: read."""
    record_property("proves", "375.5")
    assert manifest.PERMISSIONS.get("administration") == "read", \
        f"375.5: the manifest grants administration: {manifest.PERMISSIONS.get('administration')}, not read"
    s = tc.clean()
    s["account"] = {"type": "Organization", "visibility": "public", "plan": "free"}
    a = tc.Audit(tmp_path, s)
    a.run("375.5")
    tc.created(a, "375.5")
    after = a.state()
    assert any(f"repos/{REPO}/rules/branches/main" in arg for c in after["calls"] for arg in c), \
        f"375.5: the command never read main's rules: {after['calls']}"
    for call in after["calls"]:
        text = " ".join(call)
        assert not re.search(r"rulesets|rules/|/protection", text) or not re.search(
            r"(-X|--method)\s+(POST|PUT|PATCH|DELETE)|\s(-f|-F|--field|--raw-field|--input)\s", text), \
            f"375.5: the command wrote to a rule or branch protection: {call}"
        assert not re.search(r"mergeQueue|Ruleset|BranchProtection", text) or not text.startswith("api graphql") \
            or "mutation" not in text, f"375.5: the command changed a rule through GraphQL: {call}"
    assert not after.get("unsupported"), f"375.5: the command made calls the fake gh does not answer\n{a.why()}"
    assert {w["kind"] for w in after["writes"]} <= {"create", "edit", "comment", "close", "pin", "board"}, \
        f"375.5: the command made writes other than the Setup issue and its card: {after['writes']}"
