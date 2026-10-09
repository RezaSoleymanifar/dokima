"""Tests for #284: the audit fixes declared labels, options and views, and only reports the rest.

The audit (`dokima/audit.py`, from #283) compares the manifest with the live repo and reports on one Setup issue. These
tests run `audit.run` against the in-memory faked GitHub of tests/test_audit.py, whose docstring lists every read and
write the audit is expected to use: since #284 it may create and update labels, replace a board field's options and
create and update views. It has no write for branch rules or app permissions at all.

How the Setup issue is expected to read: first what is still off, one line each; then one line holding the word
"fixed" (nothing before it says fixed); then each setting this run fixed, on its own line, worded exactly as the
audit's compare() line for it. parts() below splits a body that way. When everything off was fixed, the Setup issue
still lists the fixes, is not marked Needs you, and is closed with the one line saying nothing is off.
"""
import copy
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dokima import manifest  # noqa: E402
from test_audit import (BOARD, FORBIDDEN, BROKEN, REPO, GitHub, audit, body_lines, codeowners,  # noqa: E402
                        one_line, open_setup)

ISSUE_WRITES = {"create_issue", "edit_issue", "comment", "close_issue", "pin_issue", "needs_you"}
FIX_WRITES = {"create_label", "update_label", "set_options", "create_view", "update_view"}


def parts(body):
    """(still off, fixed): the body's lines before and after its first "fixed" line."""
    lines = [l for l in body_lines(body) if l]
    for k, line in enumerate(lines):
        if re.search(r"\bfixed\b", line, re.I):
            return lines[:k], lines[k + 1:]
    return lines, []


def setup(g, criterion):
    """The one Setup issue the run left, or a failure naming the criterion."""
    assert len(g.issues) == 1, f"{criterion}: the run should leave exactly one Setup issue, there are {sorted(g.issues)}"
    n = next(iter(g.issues))
    return n, g.issues[n]


def listed_fixed(g, line, criterion, what):
    """Fail unless the line is listed as fixed, not as still off."""
    _, issue = setup(g, criterion)
    off, fixed = parts(issue["body"])
    assert line in fixed, f"{criterion}: {what} should be listed as fixed, as {line!r}; fixed part: {fixed}"
    assert line not in off, f"{criterion}: {what} was fixed but is still listed as off: {off}"


def listed_off(g, line, criterion, what):
    """Fail unless the line is listed as still off, not as fixed."""
    _, issue = setup(g, criterion)
    off, fixed = parts(issue["body"])
    assert line in off, f"{criterion}: {what} should be listed as still off, as {line!r}; still off: {off}"
    assert line not in fixed, f"{criterion}: {what} is listed as fixed, but it must only be reported: {fixed}"


def options(g):
    """Every board option as {field: {option: (id, color, description)}}."""
    return {f: {o: (v.get("id"), v["color"], v["description"]) for o, v in opts.items()}
            for f, opts in g.field_map.items()}


# 284.1: a declared label, board option or view that is missing or differs is set, and listed as fixed

def test_a_missing_or_changed_label_is_set_and_listed_as_fixed(record_property, tmp_path):
    """Missing or wrong labels are set to the manifest's and listed as fixed.

    Proves 284.1. The faked repo has no plan label, a black work label, and a high label described "Old words"; the app's issues
    permission is also read, so the Setup issue stays open. After one run all three labels have exactly the manifest's
    color and description, and the Setup issue lists each of the three label lines as fixed, not as still off."""
    record_property("proves", "284.1")
    a = audit("284.1")
    g = GitHub()
    del g.label_list["plan"]
    g.label_list["work"]["color"] = "000000"
    g.label_list["high"]["description"] = "Old words"
    g.perms["issues"] = "read"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    for name in ("plan", "work", "high"):
        assert g.label_list.get(name) == manifest.LABELS[name], \
            f"284.1: the {name} label is {g.label_list.get(name)}, not the manifest's {manifest.LABELS[name]}"
    listed_fixed(g, one_line(lines, "284.1", "the missing plan label", "plan", "1d76db"), "284.1", "the plan label")
    listed_fixed(g, one_line(lines, "284.1", "the work label's color", "work", "000000"), "284.1", "the work label")
    listed_fixed(g, one_line(lines, "284.1", "the high label's description", "high", "Old words"), "284.1",
                 "the high label")


def test_a_missing_or_changed_board_option_is_set_and_listed_as_fixed(record_property, tmp_path):
    """Missing or wrong board options are set to the manifest's and listed as fixed.

    Proves 284.1. The faked board's Action field has no Autopilot option, the High priority option is RED and the Plan status option
    is described "Old words"; the app's issues permission is also read. After one run each of the three options has
    exactly the manifest's color and description, and the Setup issue lists each option line as fixed."""
    record_property("proves", "284.1")
    a = audit("284.1")
    g = GitHub()
    del g.field_map["Action"]["Autopilot"]
    g.field_map["Priority"]["High"]["color"] = "RED"
    g.field_map["Status"]["Plan"]["description"] = "Old words"
    g.perms["issues"] = "read"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    for field, option in (("Action", "Autopilot"), ("Priority", "High"), ("Status", "Plan")):
        have = g.field_map[field].get(option)
        want = manifest.FIELDS[field][option]
        assert have and (have["color"], have["description"]) == (want["color"], want["description"]), \
            f"284.1: the {option} option of {field} is {have}, not the manifest's {want}"
    for what, words in (("the Autopilot option", ("Action", "Autopilot", "PURPLE")),
                        ("the High option", ("High", "RED", "ORANGE")),
                        ("the Plan option", ("Plan", "Old words"))):
        listed_fixed(g, one_line(lines, "284.1", what, *words), "284.1", what)


def test_a_missing_or_changed_view_is_set_and_listed_as_fixed(record_property, tmp_path):
    """A missing or wrong Autopilot view is set to the manifest's and listed as fixed.

    Proves 284.1. First the faked board has no Autopilot view: after one run it has one, a table filtered to
    `label:autopilot is:open`, listed as fixed. Then a board whose Autopilot view is a board layout filtered to
    `label:autopilot`: after one run the view is a table with the manifest's filter, and both lines are listed as
    fixed. The app's issues permission is read in both, so the Setup issue stays open."""
    record_property("proves", "284.1")
    a = audit("284.1")
    g = GitHub()
    del g.view_map["Autopilot"]
    g.perms["issues"] = "read"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path / "one", "* @alice\n"))
    assert g.view_map.get("Autopilot") == manifest.VIEWS["Autopilot"], \
        f"284.1: the missing Autopilot view was not added as the manifest has it: {g.view_map.get('Autopilot')}"
    listed_fixed(g, one_line(lines, "284.1", "the missing view", "Autopilot", "table"), "284.1", "the missing view")
    g = GitHub()
    g.view_map["Autopilot"] = {"layout": "board", "filter": "label:autopilot"}
    g.perms["issues"] = "read"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path / "two", "* @alice\n"))
    assert g.view_map.get("Autopilot") == manifest.VIEWS["Autopilot"], \
        f"284.1: the Autopilot view was not set to the manifest's layout and filter: {g.view_map.get('Autopilot')}"
    listed_fixed(g, one_line(lines, "284.1", "the view's layout", "Autopilot", "board"), "284.1", "the view's layout")
    listed_fixed(g, one_line(lines, "284.1", "the view's filter", "label:autopilot is:open"), "284.1",
                 "the view's filter")


def test_a_run_that_fixes_everything_lists_the_fixes_and_closes_the_setup_issue(record_property, tmp_path):
    """With everything fixed, the Setup issue lists the fixes and closes, never Needs you.

    Proves 284.1. With no Setup issue open and only the plan label missing, the run opens one Setup issue listing the plan label as
    fixed, closes it with one comment saying nothing is off, and never marks it Needs you. With Setup issue #7 open
    from an earlier run, the same happens on #7 and no other issue opens."""
    record_property("proves", "284.1")
    a = audit("284.1")
    for issues in ({}, open_setup()):
        g = GitHub(issues=issues)
        del g.label_list["plan"]
        line = one_line(a.compare(copy.deepcopy(g), REPO), "284.1", "the missing plan label", "plan")
        a.run(g, REPO, codeowners(tmp_path / str(len(issues)), "* @alice\n"))
        assert g.label_list.get("plan") == manifest.LABELS["plan"], "284.1: the missing plan label was not created"
        n, issue = setup(g, "284.1")
        if issues:
            assert n == 7, f"284.1: the open Setup issue #7 was not the one used: {g.writes}"
        listed_fixed(g, line, "284.1", "the plan label")
        assert issue["state"] == "closed", "284.1: a run that fixed everything left the Setup issue open"
        assert len(issue["comments"]) == 1 and "nothing is off" in issue["comments"][0].lower(), \
            f"284.1: closing should leave one comment saying nothing is off: {issue['comments']}"
        assert "needs_you" not in g.kinds(), f"284.1: nothing waits on the owner, yet it was marked Needs you: {g.writes}"


def test_a_missing_board_field_is_reported_not_created(record_property, tmp_path):
    """A whole missing board field is only reported, never created.

    Proves 284.1. The faked board has no Priority field at all, which a repo may leave out on purpose, and its Action field lacks the
    Autopilot option. The run adds the Autopilot option, makes no board write about Priority, lists the missing field
    as still off and the Autopilot option as fixed, and marks the Setup issue Needs you."""
    record_property("proves", "284.1")
    a = audit("284.1")
    g = GitHub()
    del g.field_map["Priority"]
    del g.field_map["Action"]["Autopilot"]
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    assert "Priority" not in g.field_map, "284.1: the audit added the missing Priority field"
    assert not [w for w in g.writes if w[1] == BOARD and w[2] != "Action"], \
        f"284.1: a missing field led to board writes beyond the Action field: {g.writes}"
    listed_off(g, one_line(lines, "284.1", "the missing Priority field", "Priority"), "284.1",
               "the missing Priority field")
    listed_fixed(g, one_line(lines, "284.1", "the missing Autopilot option", "Action", "Autopilot"), "284.1",
                 "the missing Autopilot option")
    assert "needs_you" in g.kinds(), "284.1: the Setup issue reporting a missing field is not marked Needs you"


# 284.2: app permissions and branch rules are never changed, only reported

def test_permissions_and_branch_rules_are_only_reported(record_property, tmp_path):
    """App permissions and branch rules are never changed, only listed as still off.

    Proves 284.2. The faked app has issues: read and administration: write, main's rule lacks the all done-whens passed check, and
    the plan label is missing. After the run the permissions and the rule are exactly as before, the only writes are
    the plan label and the Setup issue's own, the three lines are listed as still off, the plan label as fixed, and
    the issue is marked Needs you."""
    record_property("proves", "284.2")
    a = audit("284.2")
    g = GitHub()
    g.perms["issues"] = "read"
    g.perms["administration"] = "write"
    g.rules["main"]["required_checks"] = ["all tests"]
    del g.label_list["plan"]
    perms, rules = copy.deepcopy(g.perms), copy.deepcopy(g.rules)
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    assert g.perms == perms and g.rules == rules, "284.2: the audit changed an app permission or a branch rule"
    other = [w for w in g.writes if w[0] not in ISSUE_WRITES and w[:3] != ("create_label", REPO, "plan")]
    assert not other, f"284.2: the audit wrote more than the plan label and the Setup issue: {other}"
    for what, words in (("the issues permission", ("issues", "read", "write")),
                        ("the administration permission", ("administration", "write", "read")),
                        ("main's rule", ("main", "all done-whens passed"))):
        listed_off(g, one_line(lines, "284.2", what, *words), "284.2", what)
    listed_fixed(g, one_line(lines, "284.2", "the plan label", "plan", "1d76db"), "284.2", "the plan label")
    assert "needs_you" in g.kinds(), "284.2: the Setup issue reporting permissions is not marked Needs you"


def test_a_missing_branch_rule_is_only_reported(record_property, tmp_path):
    """A branch with no rule is only reported, while a wrong label is fixed.

    Proves 284.2. The faked repo has no rule on main and a black work label. The run writes only the work label and the Setup
    issue, main still has no rule, the missing rule is listed as still off and the work label as fixed, on an open
    Setup issue marked Needs you."""
    record_property("proves", "284.2")
    a = audit("284.2")
    g = GitHub()
    del g.rules["main"]
    g.label_list["work"]["color"] = "000000"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    assert "main" not in g.rules, "284.2: the audit added a branch rule"
    other = [w for w in g.writes if w[0] not in ISSUE_WRITES and w[:3] != ("update_label", REPO, "work")]
    assert not other, f"284.2: a missing branch rule led to other writes: {other}"
    listed_off(g, one_line(lines, "284.2", "main's missing rule", "main"), "284.2", "main's missing rule")
    listed_fixed(g, one_line(lines, "284.2", "the work label", "work", "000000"), "284.2", "the work label")
    _, issue = setup(g, "284.2")
    assert issue["state"] == "open" and "needs_you" in g.kinds(), \
        "284.2: the Setup issue reporting a missing rule is not open and marked Needs you"


# 284.3: a fix GitHub refuses stays on the Setup issue as still off, with GitHub's reason

def test_a_refused_label_fix_stays_off_with_githubs_reason(record_property, tmp_path):
    """A refused label fix stays listed as still off, with GitHub's reason.

    Proves 284.3. GitHub answers 403 when the audit creates the plan label; the work label's color also differs. After the run the
    plan label is still missing and its line, listed as still off, carries GitHub's words; the work label is fixed and
    listed as fixed; the Setup issue is open and marked Needs you."""
    record_property("proves", "284.3")
    a = audit("284.3")
    g = GitHub(fail={"create_label": FORBIDDEN})
    del g.label_list["plan"]
    g.label_list["work"]["color"] = "000000"
    lines = a.compare(copy.deepcopy(g), REPO)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    n, issue = setup(g, "284.3")
    off, fixed = parts(issue["body"])
    refused = one_line(off, "284.3", "the refused plan label", "plan", "1d76db")
    assert "Resource not accessible by integration" in refused, \
        f"284.3: the refused plan label's line does not give GitHub's reason: {refused!r}"
    assert not [l for l in fixed if re.search(r"(?<![\w-])plan(?![\w-])", l)], \
        f"284.3: the plan label GitHub refused is listed as fixed: {fixed}"
    assert g.label_list.get("work") == manifest.LABELS["work"], "284.3: one refused fix stopped the other fixes"
    listed_fixed(g, one_line(lines, "284.3", "the work label", "work", "000000"), "284.3", "the work label")
    assert issue["state"] == "open" and "needs_you" in g.kinds(), \
        "284.3: a refused fix left the Setup issue closed or not marked Needs you"


def test_refused_option_and_view_fixes_stay_off_with_githubs_reason(record_property, tmp_path):
    """Refused option and view fixes stay still off, each with GitHub's reason.

    Proves 284.3. GitHub answers 502 to replacing a field's options and 403 to changing a view; the Action field lacks its Autopilot
    option and the Autopilot view filters on `label:autopilot`, and nothing else is off. The run opens a Setup issue
    marked Needs you whose still-off part holds both lines, the option's with the 502 words and the view's with the
    403 words, and nothing is listed as fixed."""
    record_property("proves", "284.3")
    a = audit("284.3")
    g = GitHub(fail={"set_options": BROKEN, "update_view": FORBIDDEN})
    del g.field_map["Action"]["Autopilot"]
    g.view_map["Autopilot"]["filter"] = "label:autopilot"
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    n, issue = setup(g, "284.3")
    off, fixed = parts(issue["body"])
    option = one_line(off, "284.3", "the refused Autopilot option", "Action", "Autopilot", "PURPLE")
    assert "Server Error (HTTP 502)" in option, f"284.3: the option's line does not give GitHub's reason: {option!r}"
    view = one_line(off, "284.3", "the refused view filter", "label:autopilot is:open")
    assert "Resource not accessible by integration" in view, \
        f"284.3: the view's line does not give GitHub's reason: {view!r}"
    assert fixed == [], f"284.3: fixes GitHub refused are listed as fixed: {fixed}"
    assert issue["state"] == "open" and "needs_you" in g.kinds(), \
        "284.3: refused fixes left the Setup issue closed or not marked Needs you"


# 284.4: fixing a field's options keeps every other option as it was, and every card keeps its value

def test_adding_an_option_keeps_every_other_option_and_every_card(record_property, tmp_path):
    """Adding an option keeps every other option as it was, and every card.

    Proves 284.4. The faked board's Action field lacks Autopilot and its Priority field also has the owner's own Someday option.
    Four cards are set: one to Needs you, one to Someday, one to High, one to the Plan status. After the run every
    option that was there is still there with the same id, name, color and description, Autopilot is added with the
    manifest's color and description, and all four cards keep exactly their values."""
    record_property("proves", "284.4")
    a = audit("284.4")
    g = GitHub()
    del g.field_map["Action"]["Autopilot"]
    g.field_map["Priority"]["Someday"] = {"color": "GRAY", "description": "Maybe later", "id": "Priority:Someday"}
    g.cards = {"c1": {"Action": "Action:Needs you"}, "c2": {"Priority": "Priority:Someday"},
               "c3": {"Priority": "Priority:High"}, "c4": {"Status": "Status:Plan"}}
    before, cards = options(g), copy.deepcopy(g.cards)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    after = options(g)
    for field, opts in before.items():
        for option, was in opts.items():
            assert after.get(field, {}).get(option) == was, \
                f"284.4: the {option} option of {field} was {was} and is now {after.get(field, {}).get(option)}"
    added = g.field_map["Action"].get("Autopilot")
    want = manifest.FIELDS["Action"]["Autopilot"]
    assert added and (added["color"], added["description"]) == (want["color"], want["description"]), \
        f"284.4: the Autopilot option was not added as the manifest has it: {added}"
    assert g.cards == cards, f"284.4: cards lost or changed their values: {cards} became {g.cards}"


def test_fixing_an_option_keeps_its_id_its_cards_and_the_other_options(record_property, tmp_path):
    """Fixing an option keeps its id, its cards and every other option.

    Proves 284.4. The faked High priority option is RED and a card is set to it; the owner's Someday option is set on another card.
    After the run High is ORANGE with the same id and name, both cards keep their values, and every other option of
    every field keeps its id, name, color and description."""
    record_property("proves", "284.4")
    a = audit("284.4")
    g = GitHub()
    g.field_map["Priority"]["High"]["color"] = "RED"
    g.field_map["Priority"]["Someday"] = {"color": "GRAY", "description": "Maybe later", "id": "Priority:Someday"}
    g.perms["issues"] = "read"
    g.cards = {"c1": {"Priority": "Priority:High"}, "c2": {"Priority": "Priority:Someday"}}
    before, cards = options(g), copy.deepcopy(g.cards)
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    after = options(g)
    assert after["Priority"].get("High") == ("Priority:High", "ORANGE", manifest.FIELDS["Priority"]["High"]["description"]), \
        f"284.4: the High option should keep its id and turn ORANGE, it is {after['Priority'].get('High')}"
    for field, opts in before.items():
        for option, was in opts.items():
            if (field, option) != ("Priority", "High"):
                assert after.get(field, {}).get(option) == was, \
                    f"284.4: the {option} option of {field} was {was} and is now {after.get(field, {}).get(option)}"
    assert g.cards == cards, f"284.4: cards lost or changed their values: {cards} became {g.cards}"


# 284.5: AGENTS.md says the audit sets the board's declared options and views

def board_section():
    """The text of AGENTS.md's section on the board."""
    text = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
    m = re.search(r"^## The board\n(.*?)(?=^## )", text, re.S | re.M)
    assert m, "284.5: AGENTS.md has no section headed '## The board'"
    return m.group(1)


def test_agents_md_says_the_audit_sets_the_boards_declared_options_and_views(record_property):
    """AGENTS.md says the audit sets the board's declared options and views.

    Proves 284.5. Reads the board section of AGENTS.md: no sentence there still says code never edits the field's options or calls
    the Autopilot option a one-time step, and one sentence says the audit sets (or fixes) the board's options and
    views."""
    record_property("proves", "284.5")
    section = board_section()
    old = [s for s in re.split(r"(?<=[.;])\s+", section)
           if re.search(r"never edits the field'?s options|one-time step", s, re.I)]
    assert not old, f"284.5: AGENTS.md still says code never edits the board's options: {old}"
    new = [s for s in re.split(r"(?<=\.)\s+", section)
           if re.search(r"\baudit\b", s, re.I) and re.search(r"\b(sets|fixes|restores)\b", s, re.I)
           and re.search(r"\boptions\b", s, re.I) and re.search(r"\bviews\b", s, re.I)]
    assert new, f"284.5: AGENTS.md's board section has no sentence saying the audit sets the board's options and views:\n{section}"


# 284.6: the audit never deletes or renames, and never touches what the manifest does not declare

def test_the_audit_never_deletes_renames_or_touches_undeclared_settings(record_property, tmp_path):
    """The audit never deletes, renames or touches settings the manifest does not declare.

    Proves 284.6. The faked repo is off in a label, an option and a view, and also has the owner's bug label, Someday priority
    option, Size field and Mine view. After the run every label, field, option and view that was there is still there
    under its name; the owner's ones are exactly as they were; and every fix write names a declared label, field or
    view."""
    record_property("proves", "284.6")
    a = audit("284.6")
    g = GitHub()
    del g.label_list["plan"]
    g.label_list["work"]["color"] = "000000"
    del g.field_map["Action"]["Autopilot"]
    g.view_map["Autopilot"]["filter"] = "label:autopilot"
    g.label_list["bug"] = {"color": "ffffff", "description": "Something is broken"}
    g.field_map["Priority"]["Someday"] = {"color": "GRAY", "description": "Maybe later", "id": "Priority:Someday"}
    g.field_map["Size"] = {"Small": {"color": "GREEN", "description": "", "id": "Size:Small"}}
    g.view_map["Mine"] = {"layout": "board", "filter": "assignee:@me"}
    before = copy.deepcopy((g.label_list, g.field_map, g.view_map))
    a.run(g, REPO, codeowners(tmp_path, "* @alice\n"))
    labels, fields, views = before
    assert set(labels) <= set(g.label_list), f"284.6: labels were deleted or renamed: {set(labels) - set(g.label_list)}"
    assert set(views) <= set(g.view_map), f"284.6: views were deleted or renamed: {set(views) - set(g.view_map)}"
    for field, opts in fields.items():
        assert set(opts) <= set(g.field_map.get(field, {})), \
            f"284.6: options of {field} were deleted or renamed: {set(opts) - set(g.field_map.get(field, {}))}"
    assert g.label_list["bug"] == labels["bug"], "284.6: the owner's bug label was changed"
    assert g.field_map["Priority"]["Someday"] == fields["Priority"]["Someday"], "284.6: the owner's Someday option was changed"
    assert g.field_map["Size"] == fields["Size"], "284.6: the owner's Size field was changed"
    assert g.view_map["Mine"] == views["Mine"], "284.6: the owner's Mine view was changed"
    declared = {"create_label": manifest.LABELS, "update_label": manifest.LABELS, "set_options": manifest.FIELDS,
                "create_view": manifest.VIEWS, "update_view": manifest.VIEWS}
    stray = [w for w in g.writes if w[0] in declared and w[2] not in declared[w[0]]]
    assert not stray, f"284.6: the audit wrote settings the manifest does not declare: {stray}"
    assert {w[0] for w in g.writes} & FIX_WRITES, f"284.6: the audit fixed nothing, so this proves nothing: {g.writes}"
