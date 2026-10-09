"""Tests for #284: `python3 -m dokima.audit OWNER/REPO` fixes declared labels, options and views through `gh`.

The in-memory tests in tests/test_audit_fix.py prove what the audit decides; these prove it really writes GitHub the
way GitHub works. Each runs the command from outside, as tests/test_audit_cli.py does, against the fake `gh` in
tests/fake_gh.py, whose docstring lists every call it answers. The fake replaces a field's options the way GitHub's
updateProjectV2Field does: an option passed without its id gets a new one, and an option left out is deleted, which
clears every card on it. So keeping the owner's options and cards can only pass by sending each kept option back with
its id.

How the command is expected to fix things (any one way the fake answers):
    a label             gh api -X POST repos/OWNER/REPO/labels or -X PATCH repos/OWNER/REPO/labels/NAME
                        (or gh label create / gh label edit)
    a board option      gh api graphql, updateProjectV2Field with every option of the field, kept ones with their ids
    a view              gh api -X POST orgs/OWNER/projectsV2/1/views to add it, updateProjectV2View to change it
The Setup issue reads as tests/test_audit_fix.py describes: what is still off, then a line holding the word "fixed",
then each fixed setting.
"""
import copy
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dokima import manifest  # noqa: E402
from test_audit_cli import FORBIDDEN, Audit, clean, created, drifted, one_line  # noqa: E402
from test_audit_fix import parts  # noqa: E402

WRITE_FLAGS = {"-f", "-F", "--field", "--raw-field", "--input"}


def options(state):
    """Every board option as {field: {option: (id, color, description)}}, ids as the fake answers them."""
    return {f: {o: (v.get("id") or f"O_{f}_{o.replace(' ', '_')}", v["color"], v["description"])
                for o, v in opts.items()} for f, opts in state["fields"].items()}


def settled(a, criterion):
    """The fake's state after a run, failing on any call the fake could not answer."""
    s = a.state()
    assert not s.get("unsupported"), f"{criterion}: the command made calls the fake gh does not answer\n{a.why()}"
    return s


# 284.1: declared labels, options and views that are missing or differ are set, and listed as fixed

def test_the_command_fixes_labels_options_and_views_and_lists_them_as_fixed(record_property, tmp_path):
    """The command fixes labels, options and views on GitHub and lists them as fixed.

    Proves 284.1. Runs the command against a fake repo off in one setting of each kind: no plan label, the work label's description,
    no Autopilot option on the Action field, a RED High option, the Autopilot view's old filter, main's rule and the
    app's issues permission. Afterwards GitHub holds the manifest's plan and work labels, the Autopilot and High options
    and the view's filter; the Setup issue lists the five fixed lines as fixed and the rule and permission as off."""
    record_property("proves", "284.1")
    a = Audit(tmp_path, drifted())
    a.run("284.1")
    s = settled(a, "284.1")
    for name in ("plan", "work"):
        assert s["labels"].get(name) == manifest.LABELS[name], \
            f"284.1: the {name} label is {s['labels'].get(name)} on GitHub, not the manifest's\n{a.why()}"
    for field, option in (("Action", "Autopilot"), ("Priority", "High")):
        have, want = s["fields"][field].get(option) or {}, manifest.FIELDS[field][option]
        assert (have.get("color"), have.get("description")) == (want["color"], want["description"]), \
            f"284.1: the {option} option of {field} is {have} on GitHub, not the manifest's {want}\n{a.why()}"
    assert s["views"].get("Autopilot") == manifest.VIEWS["Autopilot"], \
        f"284.1: the Autopilot view is {s['views'].get('Autopilot')} on GitHub, not the manifest's\n{a.why()}"
    n, issue = created(a, "284.1")
    off, fixed = parts(issue["body"])
    for what, words in (("the plan label", ("plan", "1d76db")), ("the work label", ("work", "Old words")),
                        ("the Autopilot option", ("Action", "Autopilot", "PURPLE")),
                        ("the High option", ("High", "RED", "ORANGE")),
                        ("the view's filter", ("label:autopilot is:open",))):
        one_line(fixed, "284.1", f"{what}, listed as fixed", *words)
        assert not [l for l in off if all(w in l for w in words)], f"284.1: {what} was fixed but is listed as off: {off}"
    one_line(off, "284.1", "main's rule, still off", "main", "all done-whens passed")
    one_line(off, "284.1", "the issues permission, still off", "issues", "read", "write")


def test_the_command_adds_a_missing_view_and_closes_once_all_is_fixed(record_property, tmp_path):
    """The command adds a missing view, then lists it and closes the Setup issue.

    Proves 284.1. The fake board has no Autopilot view and matches the manifest otherwise. After the run the board has the
    manifest's Autopilot view; the one Setup issue lists the view as fixed, is closed with one comment saying nothing is
    off, and its card is not marked Needs you."""
    record_property("proves", "284.1")
    s = clean()
    del s["views"]["Autopilot"]
    a = Audit(tmp_path, s)
    a.run("284.1")
    s = settled(a, "284.1")
    assert s["views"].get("Autopilot") == manifest.VIEWS["Autopilot"], \
        f"284.1: the missing Autopilot view was not added: {s['views']}\n{a.why()}"
    n, issue = created(a, "284.1")
    one_line(parts(issue["body"])[1], "284.1", "the Autopilot view, listed as fixed", "Autopilot", "table")
    assert issue["state"] == "closed", f"284.1: with everything fixed, the Setup issue was left open\n{a.why()}"
    assert len(issue["comments"]) == 1 and "nothing is off" in issue["comments"][0].lower(), \
        f"284.1: closing should leave one comment saying nothing is off: {issue['comments']}"
    card = s["items"].get(f"PVTI_I_{n}", {})
    assert "Action" not in card, f"284.1: nothing waits on the owner, yet the card is marked: {card}"


# 284.2: app permissions and branch rules are never changed through gh

def test_the_command_never_writes_branch_rules_or_permissions(record_property, tmp_path):
    """The command only ever reads branch rules and app permissions.

    Proves 284.2. Runs the command against the drifted fake repo, whose main rule lacks a check, whose app has issues: read and also
    administration: write. Every call it made about branch protection, rulesets or the app's installation is a plain
    read (no -X other than GET, no fields), the fake's rule and permissions are unchanged, and the Setup issue lists
    the rule and both permissions as still off while it did fix the plan label."""
    record_property("proves", "284.2")
    s = drifted()
    s["permissions"]["administration"] = "write"
    rule, perms = copy.deepcopy(s["protection"]), copy.deepcopy(s["permissions"])
    a = Audit(tmp_path, s)
    a.run("284.2")
    s = settled(a, "284.2")
    touching = [c for c in s["calls"] if any(re.search(r"protection|rulesets|/installation|branches/", arg or "")
                                             for arg in c)]
    assert touching, "284.2: the command never read the branch rule or the app's permissions"
    writes = [c for c in touching
              if any(arg in WRITE_FLAGS for arg in c)
              or any(c[k] in ("-X", "--method") and c[k + 1].upper() != "GET" for k in range(len(c) - 1))]
    assert not writes, f"284.2: the command tried to change a branch rule or a permission: {writes}"
    assert s["protection"] == rule and s["permissions"] == perms, "284.2: a branch rule or a permission changed"
    n, issue = created(a, "284.2")
    off, fixed = parts(issue["body"])
    one_line(off, "284.2", "main's rule, still off", "main", "all done-whens passed")
    one_line(off, "284.2", "the issues permission, still off", "issues", "read", "write")
    one_line(off, "284.2", "the administration permission, still off", "administration", "write", "read")
    one_line(fixed, "284.2", "the plan label, listed as fixed", "plan", "1d76db")
    assert s["items"].get(f"PVTI_I_{n}", {}).get("Action") == "O_Action_Needs_you", \
        f"284.2: the Setup issue reporting permissions is not marked Needs you\n{a.why()}"


# 284.3: a fix GitHub refuses stays on the Setup issue as still off, with GitHub's reason

def test_the_command_keeps_a_refused_fix_as_off_with_githubs_reason(record_property, tmp_path):
    """A label write GitHub refuses stays still off with GitHub's reason.

    Proves 284.3. The fake repo lacks the plan label and has a RED High option; GitHub answers 403 to every label write. After the
    run the plan label is still missing, the Setup issue lists it as still off with GitHub's words, lists the High
    option as fixed, and is open and marked Needs you."""
    record_property("proves", "284.3")
    s = clean()
    del s["labels"]["plan"]
    s["fields"]["Priority"]["High"]["color"] = "RED"
    s["fail"] = {"label_write": FORBIDDEN}
    a = Audit(tmp_path, s)
    a.run("284.3")
    s = a.state()
    assert "plan" not in s["labels"], "284.3: the fake refused the label, yet it exists"
    n, issue = created(a, "284.3")
    off, fixed = parts(issue["body"])
    line = one_line(off, "284.3", "the refused plan label, still off", "plan", "1d76db")
    assert "Resource not accessible by integration" in line, f"284.3: the line does not give GitHub's reason: {line!r}"
    one_line(fixed, "284.3", "the High option, listed as fixed", "High", "RED", "ORANGE")
    assert s["fields"]["Priority"]["High"]["color"] == "ORANGE", "284.3: a refused label stopped the option's fix"
    assert issue["state"] == "open", f"284.3: a refused fix closed the Setup issue\n{a.why()}"
    assert s["items"].get(f"PVTI_I_{n}", {}).get("Action") == "O_Action_Needs_you", \
        f"284.3: the Setup issue with a refused fix is not marked Needs you\n{a.why()}"


# 284.4: fixing options keeps every other option and every card's value

def test_the_command_keeps_every_other_option_and_every_card(record_property, tmp_path):
    """On GitHub, fixing options keeps every other option and every card's value.

    Proves 284.4. The fake board lacks the Action field's Autopilot option, has a RED High option and the owner's Someday option;
    four cards are set to Needs you, Someday, High and Plan. After the run every option keeps its id, name, color and
    description (High only turns ORANGE), Autopilot exists with the manifest's values, and all four cards keep exactly
    their values."""
    record_property("proves", "284.4")
    s = clean()
    del s["fields"]["Action"]["Autopilot"]
    s["fields"]["Priority"]["High"]["color"] = "RED"
    s["fields"]["Priority"]["Someday"] = {"color": "GRAY", "description": "Maybe later"}
    s["items"] = {"PVTI_I_5": {"Action": "O_Action_Needs_you", "Priority": "O_Priority_Someday"},
                  "PVTI_I_6": {"Priority": "O_Priority_High", "Status": "O_Status_Plan"}}
    before, cards = options(s), copy.deepcopy(s["items"])
    a = Audit(tmp_path, s)
    a.run("284.4")
    s = settled(a, "284.4")
    after = options(s)
    for field, opts in before.items():
        for option, (oid, color, description) in opts.items():
            want = (oid, "ORANGE", description) if (field, option) == ("Priority", "High") else (oid, color, description)
            assert after.get(field, {}).get(option) == want, \
                f"284.4: the {option} option of {field} should be {want}, it is {after.get(field, {}).get(option)}"
    added = s["fields"]["Action"].get("Autopilot") or {}
    want = manifest.FIELDS["Action"]["Autopilot"]
    assert (added.get("color"), added.get("description")) == (want["color"], want["description"]), \
        f"284.4: the Autopilot option was not added as the manifest has it: {added}"
    for item, values in cards.items():
        assert s["items"].get(item) == values, f"284.4: the card {item} was {values} and is now {s['items'].get(item)}"


# 284.6: never deletes or renames, never touches what the manifest does not declare

def test_the_command_never_deletes_renames_or_touches_undeclared_settings(record_property, tmp_path):
    """On GitHub, the command deletes and renames nothing, and leaves undeclared settings alone.

    Proves 284.6. Runs the command against the drifted fake repo that also has the owner's bug label, Someday option, Size field and
    Mine view. No delete is made, every label, field, option and view keeps its name, the owner's ones are exactly as
    they were, and the command did fix the declared ones."""
    record_property("proves", "284.6")
    s = drifted()
    s["labels"]["bug"] = {"color": "ffffff", "description": "Something is broken"}
    s["fields"]["Priority"]["Someday"] = {"color": "GRAY", "description": "Maybe later"}
    s["fields"]["Size"] = {"Small": {"color": "GREEN", "description": ""}}
    s["views"]["Mine"] = {"layout": "board", "filter": "assignee:@me"}
    before = copy.deepcopy(s)
    a = Audit(tmp_path, s)
    a.run("284.6")
    s = settled(a, "284.6")
    kinds = [w["kind"] for w in s["writes"]]
    assert not [k for k in kinds if k.endswith("_delete")], f"284.6: the command deleted something: {s['writes']}"
    assert {"label", "field", "view"} <= set(kinds), f"284.6: the command fixed nothing, so this proves nothing: {kinds}"
    assert set(before["labels"]) <= set(s["labels"]), "284.6: a label was deleted or renamed"
    assert set(before["views"]) <= set(s["views"]), "284.6: a view was deleted or renamed"
    for field, opts in before["fields"].items():
        assert set(opts) <= set(s["fields"].get(field, {})), f"284.6: an option of {field} was deleted or renamed"
    assert s["labels"]["bug"] == before["labels"]["bug"], "284.6: the owner's bug label was changed"
    assert options(s)["Priority"]["Someday"] == options(before)["Priority"]["Someday"], \
        "284.6: the owner's Someday option was changed"
    assert options(s)["Size"] == options(before)["Size"], "284.6: the owner's Size field was changed"
    assert s["views"]["Mine"] == before["views"]["Mine"], "284.6: the owner's Mine view was changed"
