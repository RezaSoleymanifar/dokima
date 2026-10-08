"""Tests for #282: one manifest in code declares everything Dokima needs from GitHub.

The manifest is `dokima/manifest.py`, plain data read without a network:
    LABELS        {label name: {"color": "rrggbb", "description": str}}
    FIELDS        {board field name: {option name: {"color": GitHub option color, "description": str}}}
    VIEWS         {view name: {"layout": "table" | "board" | "roadmap", "filter": str}}
    CHECKS        [required check name, ...]
    BRANCH_RULES  {branch name: {"required_checks": [check name, ...], ...}}
    PERMISSIONS   {app permission: "read" | "write"}, the same as dokima/app.json's default_permissions
    undeclared(root) -> [str, ...]: one line per setting the code or workflows under `root` rely on that the manifest
        leaves out, naming the setting and the file (path relative to root, with forward slashes). It reads the
        manifest's data when called, so a test can take an entry out and see the guard report it.

What counts as relying on a setting:
    label       a workflow started by it (github.event.label.name == '...'), or code adding it ("labels[]": "...",
                labels[]=...)
    field       code setting it: board.set(iid, "Field", "Option"); the option counts too
    view        code adding it: add_view("Name", ...)
    check       code looking a check run up by name: r["name"] == "..." or r["name"] == NAME, where NAME = "..." in that
                file (a name subscripted once, so p["label"]["name"] == "plan" is a label, not a check)
    branch rule code reading a branch's rule: branches/<branch>/protection or rules/branches/<branch>
    permission  a workflow asking an app token for it (permission-<name>: <level>), or code calling
                branches/<branch>/protection, which needs administration: read to read it, write to change it
                (-X PUT/POST/PATCH/DELETE, or rest("PUT", ...)); a level higher than the manifest's is left out too
"""
import importlib
import json
import os
import subprocess
import sys
import textwrap

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OPTION_COLORS = {"GRAY", "BLUE", "GREEN", "YELLOW", "ORANGE", "RED", "PINK", "PURPLE"}


def manifest(criterion):
    """The manifest module, or a failure naming the criterion when it is missing."""
    try:
        return importlib.import_module("dokima.manifest")
    except ModuleNotFoundError as e:
        if e.name != "dokima.manifest":
            raise
        pytest.fail(f"{criterion}: there is no manifest module, dokima/manifest.py")


def workflow_job_names():
    """Every job's name across the repo's workflows: the names GitHub gives their checks."""
    names = set()
    folder = os.path.join(ROOT, ".github", "workflows")
    for f in os.listdir(folder):
        for line in open(os.path.join(folder, f)):
            s = line.strip()
            if line.startswith("    name:") and not line.startswith("     "):
                names.add(s.split(":", 1)[1].strip().strip("'\""))
    return names


# 282.1: one manifest module declares every setting Dokima needs

def test_the_manifest_declares_every_label_dokima_uses(record_property):
    """The manifest declares exactly the labels Dokima uses: plan, work, autopilot, blocker, high, parked.

    Proves 282.1. Each has a six-digit hex color and a description, and the board's own label names (autopilot and the priority
    labels) are among them."""
    record_property("proves", "282.1")
    m = manifest("282.1")
    from dokima import board
    assert set(m.LABELS) == {"plan", "work", "autopilot", "blocker", "high", "parked"}, \
        f"282.1: the manifest declares the labels {sorted(m.LABELS)}, not plan, work, autopilot, blocker, high, parked"
    for name, label in m.LABELS.items():
        color = label.get("color", "")
        assert len(color) == 6 and all(c in "0123456789abcdefABCDEF" for c in color), \
            f"282.1: label {name} has color {color!r}, not six hex digits"
        assert isinstance(label.get("description"), str) and label["description"].strip(), \
            f"282.1: label {name} has no description"
    assert board.AUTOPILOT in m.LABELS and set(board.PRIORITY) <= set(m.LABELS), \
        "282.1: a label the board code reads is not in the manifest"


def test_the_manifest_declares_the_board_fields_and_their_options(record_property):
    """The manifest declares the Status, Action and Priority fields with exactly the options Dokima sets.

    Proves 282.1. Status is Backlog, Plan, Work, Review, Done in that order; Action is Needs you and Autopilot; Priority is Blocker,
    High and Parked, the options the board sets from the priority labels. Every option has a GitHub option color and a
    description."""
    record_property("proves", "282.1")
    m = manifest("282.1")
    from dokima import board
    assert set(m.FIELDS) == {"Status", "Action", "Priority"}, f"282.1: the manifest declares the fields {sorted(m.FIELDS)}"
    assert list(m.FIELDS["Status"]) == ["Backlog", "Plan", "Work", "Review", "Done"], \
        f"282.1: Status has the options {list(m.FIELDS['Status'])}"
    assert set(m.FIELDS["Action"]) == {"Needs you", "Autopilot"}, f"282.1: Action has the options {list(m.FIELDS['Action'])}"
    assert set(m.FIELDS["Priority"]) == set(board.PRIORITY.values()) == {"Blocker", "High", "Parked"}, \
        f"282.1: Priority has the options {list(m.FIELDS['Priority'])}"
    for field, options in m.FIELDS.items():
        for name, option in options.items():
            assert option.get("color") in OPTION_COLORS, \
                f"282.1: option {name} of {field} has color {option.get('color')!r}, not one of GitHub's {sorted(OPTION_COLORS)}"
            assert isinstance(option.get("description"), str), f"282.1: option {name} of {field} has no description"


def test_the_manifest_declares_views_checks_and_branch_rules(record_property):
    """The manifest declares the Autopilot table view, the required checks and main's branch rule.

    Proves 282.1. The required checks are the two Dokima's merge waits on, "all tests" and "all done-whens passed", each the name of
    a real job in the repo's workflows, and main's branch rule requires exactly those checks."""
    record_property("proves", "282.1")
    m = manifest("282.1")
    assert set(m.VIEWS) == {"Autopilot"}, f"282.1: the manifest declares the views {sorted(m.VIEWS)}"
    assert m.VIEWS["Autopilot"]["layout"] == "table", f"282.1: the Autopilot view is {m.VIEWS['Autopilot']}"
    assert set(m.CHECKS) == {"all tests", "all done-whens passed"}, f"282.1: the required checks are {m.CHECKS}"
    jobs = workflow_job_names()
    for check in m.CHECKS:
        assert check in jobs, f"282.1: required check {check!r} is the name of no job in .github/workflows/"
    assert "main" in m.BRANCH_RULES, f"282.1: the manifest declares branch rules for {sorted(m.BRANCH_RULES)}, not main"
    assert set(m.BRANCH_RULES["main"]["required_checks"]) == set(m.CHECKS), \
        f"282.1: main's branch rule requires {m.BRANCH_RULES['main']['required_checks']}, not the required checks {m.CHECKS}"


def test_the_manifest_declares_the_app_permissions(record_property):
    """The manifest declares the app permissions Dokima needs, each read or write.

    Proves 282.1."""
    record_property("proves", "282.1")
    m = manifest("282.1")
    assert m.PERMISSIONS, "282.1: the manifest declares no app permissions"
    for name, level in m.PERMISSIONS.items():
        assert level in ("read", "write"), f"282.1: app permission {name} is {level!r}, not read or write"


# 282.2: the Autopilot option and view as declared, and the board reads the view's filter from the manifest

def test_the_autopilot_option_is_purple_running_on_its_own(record_property):
    """The Autopilot option is purple and described "Running on its own".

    Proves 282.2."""
    record_property("proves", "282.2")
    m = manifest("282.2")
    assert m.FIELDS["Action"]["Autopilot"] == {"color": "PURPLE", "description": "Running on its own"}, \
        f"282.2: the Autopilot option is {m.FIELDS['Action']['Autopilot']}, not purple, \"Running on its own\""


class FakeBoard:
    """A board with no views and #57 on autopilot; it records views added."""

    def __init__(self):
        self.added, self.fields = [], {"Action": ("A", {"Needs you": "n", "Autopilot": "a"})}

    def autopilot(self, kind, number):
        return True

    def open_pr(self, number):
        return None

    def item(self, kind, number):
        return (kind, number)

    def value(self, iid, field):
        return None

    def set(self, iid, field, option):
        pass

    def label(self, kind, number, on):
        pass

    def parent(self, number):
        return None

    def views(self):
        return [v[0] for v in self.added]

    def add_view(self, name, layout, filter):
        self.added.append((name, layout, filter))


def test_the_board_adds_the_autopilot_view_with_the_manifests_filter(record_property, monkeypatch):
    """The board adds the Autopilot view with the manifest's filter, `label:autopilot is:open`.

    Proves 282.2. The manifest declares the filter `label:autopilot is:open`, and switching #57 on autopilot adds the Autopilot table
    view with it. With the manifest's filter changed for the test, the board adds the view with the changed filter, so
    the board takes it from the manifest rather than a copy of its own."""
    record_property("proves", "282.2")
    m = manifest("282.2")
    from dokima import board
    assert m.VIEWS["Autopilot"]["filter"] == "label:autopilot is:open", \
        f"282.2: the manifest declares the Autopilot filter {m.VIEWS['Autopilot']['filter']!r}"
    b = FakeBoard()
    board.switch(b, 57)
    assert b.added == [("Autopilot", "table", "label:autopilot is:open")], \
        f"282.2: switching #57 on autopilot added the views {b.added}, not Autopilot filtered to label:autopilot is:open"
    monkeypatch.setitem(m.VIEWS, "Autopilot", {"layout": "table", "filter": "label:autopilot is:open no:assignee"})
    b = FakeBoard()
    board.switch(b, 57)
    assert b.added == [("Autopilot", "table", "label:autopilot is:open no:assignee")], \
        f"282.2: with the manifest's filter changed, the board added {b.added}: it does not read the filter from the manifest"


# 282.3: a guard reports every setting the code or workflows rely on that the manifest leaves out

def write(root, path, text):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(textwrap.dedent(text))


def reported(lines, setting, path):
    """Whether one of the guard's lines names both the setting and the file."""
    return any(setting in line and path in line for line in lines)


UNDECLARED = [
    (".github/workflows/deploy.yml", "deploy", """\
        on:
          issues:
            types: [labeled]
        jobs:
          go:
            if: github.event.label.name == 'deploy'
            runs-on: ubuntu-24.04
            steps:
              - run: echo hi
        """),
    ("dokima/ship.py", "Shipped", """\
        def ship(board, iid):
            board.set(iid, "Status", "Shipped")
        """),
    ("dokima/stage.py", "Stage", """\
        def stage(board, iid):
            board.set(iid, "Stage", "Plan")
        """),
    ("dokima/mine.py", "Mine", """\
        def mine(board):
            board.add_view("Mine", "table", "label:mine")
        """),
    ("dokima/rest_label.py", "deploy", """\
        def put(rest, path):
            rest("POST", path, **{"labels[]": "deploy"})
        """),
    ("dokima/gh_label.py", "deploy", """\
        def put(gh, repo, n):
            gh("api", "-X", "POST", f"repos/{repo}/issues/{n}/labels", "-f", "labels[]=deploy")
        """),
    ("dokima/lint.py", "lint", """\
        def lint(runs):
            return next(r for r in runs if r["name"] == "lint")
        """),
    ("dokima/lint_name.py", "lint", """\
        LINT = "lint"


        def lint(runs):
            return next(r for r in runs if r["name"] == LINT)
        """),
    ("dokima/release_rule.py", "release", """\
        def rule(gh, repo):
            return gh("api", f"repos/{repo}/branches/release/protection")
        """),
    ("dokima/release_rules.py", "release", """\
        def rules(gh, repo):
            return gh("api", f"repos/{repo}/rules/branches/release")
        """),
    (".github/workflows/pages.yml", "pages", """\
        on: workflow_dispatch
        jobs:
          go:
            runs-on: ubuntu-24.04
            steps:
              - uses: actions/create-github-app-token@v2
                id: app
                with:
                  app-id: ${{ vars.DOKIMA_APP_ID }}
                  private-key: ${{ secrets.DOKIMA_APP_KEY }}
                  permission-pages: write
        """),
    ("dokima/protect.py", "administration", """\
        def protect(gh, repo):
            gh("api", "-X", "PUT", f"repos/{repo}/branches/main/protection", "--input", "rule.json")
        """),
    ("dokima/protect_rest.py", "administration", """\
        def protect(rest, repo):
            rest("PUT", f"repos/{repo}/branches/main/protection")
        """),
]


@pytest.mark.parametrize("path,setting,text", UNDECLARED, ids=[p for p, _, _ in UNDECLARED])
def test_the_guard_names_an_undeclared_setting_and_its_file(record_property, tmp_path, path, setting, text):
    """The guard names a setting the manifest leaves out, and the file relying on it.

    Proves 282.3. A repo holding only one file that relies on an undeclared setting gets a line from the guard naming that setting
    and that file: a workflow keyed on the label deploy; code setting the option Shipped or the field Stage, adding the
    view Mine, or adding the label deploy through the REST or gh form; code looking up the check lint by name, written
    out or through a constant; code reading the branch rule of release either way; a workflow asking an app token for
    pages; and code changing main's branch rule, which needs administration write where the manifest grants read."""
    record_property("proves", "282.3")
    m = manifest("282.3")
    write(str(tmp_path), path, text)
    lines = m.undeclared(str(tmp_path))
    assert reported(lines, setting, path), \
        f"282.3: {path} relies on {setting!r}, which the manifest leaves out, and the guard said {lines}"


def test_the_guard_passes_settings_the_manifest_declares(record_property, tmp_path):
    """The guard stays quiet for declared settings, and the repo as it is passes.

    Proves 282.3. A workflow keyed on the label plan and asking an app token for issues write and administration read, and code
    setting Status to Done, adding the Autopilot view, adding the label autopilot both ways, looking up the checks
    "all tests" and "all done-whens passed" by name and through a constant, and reading main's branch rule both ways,
    gets no line from the guard, and neither does the repo as it is."""
    record_property("proves", "282.3")
    m = manifest("282.3")
    write(str(tmp_path), ".github/workflows/plan.yml", """\
        on:
          issues:
            types: [labeled]
        jobs:
          go:
            if: github.event.label.name == 'plan'
            runs-on: ubuntu-24.04
            steps:
              - uses: actions/create-github-app-token@v2
                id: app
                with:
                  app-id: ${{ vars.DOKIMA_APP_ID }}
                  private-key: ${{ secrets.DOKIMA_APP_KEY }}
                  permission-issues: write
                  permission-administration: read
        """)
    write(str(tmp_path), "dokima/fine.py", """\
        DONE_WHENS = "all done-whens passed"


        def fine(board, rest, gh, iid, path, runs, repo):
            board.set(iid, "Status", "Done")
            board.add_view("Autopilot", "table", "label:autopilot is:open")
            rest("POST", path, **{"labels[]": "autopilot"})
            gh("api", "-X", "POST", path, "-f", "labels[]=autopilot")
            tests = next(r for r in runs if r["name"] == "all tests")
            whens = next(r for r in runs if r["name"] == DONE_WHENS)
            gh("api", f"repos/{repo}/branches/main/protection")
            rest("GET", f"repos/{repo}/rules/branches/main")
            return tests, whens
        """)
    assert m.undeclared(str(tmp_path)) == [], f"282.3: the guard reported declared settings: {m.undeclared(str(tmp_path))}"
    assert m.undeclared(ROOT) == [], f"282.3: code or workflows in this repo rely on settings the manifest leaves out: {m.undeclared(ROOT)}"


@pytest.mark.parametrize("label,path", [("plan", ".github/workflows/planner.yml"), ("work", ".github/workflows/worker.yml")])
def test_the_guard_catches_a_label_taken_out_of_the_manifest(record_property, monkeypatch, label, path):
    """A label taken out of the manifest is named by the guard with its workflow.

    Proves 282.3. With plan (or work) left out of the manifest's labels, the guard run on this repo names that label and the
    workflow that starts on it."""
    record_property("proves", "282.3")
    m = manifest("282.3")
    monkeypatch.delitem(m.LABELS, label)
    lines = m.undeclared(ROOT)
    assert reported(lines, label, path), \
        f"282.3: with {label} left out of the manifest, the guard did not name it and {path}: {lines}"


def test_the_guard_catches_a_check_taken_out_of_the_manifest(record_property, monkeypatch):
    """A check taken out of the manifest is named with the code that looks it up.

    Proves 282.3. With "all tests" left out of the manifest's required checks, the guard run on this repo names "all tests" and
    dokima/card.py, which finds that check by name."""
    record_property("proves", "282.3")
    m = manifest("282.3")
    monkeypatch.setattr(m, "CHECKS", [c for c in m.CHECKS if c != "all tests"])
    lines = m.undeclared(ROOT)
    assert reported(lines, "all tests", "dokima/card.py"), \
        f"282.3: with \"all tests\" left out of the manifest, the guard did not name it and dokima/card.py: {lines}"


def test_the_guard_catches_a_branch_rule_or_permission_taken_out_of_the_manifest(record_property, monkeypatch, tmp_path):
    """A branch rule or permission taken out of the manifest is named with its file.

    Proves 282.3. Code reading main's branch rule passes while the manifest declares main and administration read. With main
    left out of the branch rules the guard names main and the file; with administration left out of the permissions it
    names administration and the file."""
    record_property("proves", "282.3")
    m = manifest("282.3")
    write(str(tmp_path), "dokima/rule.py", """\
        def rule(gh, repo):
            return gh("api", f"repos/{repo}/branches/main/protection")
        """)
    assert m.undeclared(str(tmp_path)) == [], f"282.3: the guard reported main's declared rule: {m.undeclared(str(tmp_path))}"
    with monkeypatch.context() as mp:
        mp.delitem(m.BRANCH_RULES, "main")
        lines = m.undeclared(str(tmp_path))
        assert reported(lines, "main", "dokima/rule.py"), \
            f"282.3: with main left out of the branch rules, the guard did not name it and dokima/rule.py: {lines}"
    with monkeypatch.context() as mp:
        mp.delitem(m.PERMISSIONS, "administration")
        lines = m.undeclared(str(tmp_path))
        assert reported(lines, "administration", "dokima/rule.py"), \
            f"282.3: with administration left out of the permissions, the guard did not name it and dokima/rule.py: {lines}"


# 282.4: the manifest's app permissions match dokima/app.json, with Administration read

def test_the_manifest_permissions_match_the_app_with_administration_read(record_property):
    """The manifest's app permissions equal dokima/app.json's, both with Administration read.

    Proves 282.4. Neither asks for Administration write."""
    record_property("proves", "282.4")
    m = manifest("282.4")
    app = json.load(open(os.path.join(ROOT, "dokima", "app.json")))["default_permissions"]
    assert app.get("administration") == "read", \
        f"282.4: dokima/app.json asks for Administration {app.get('administration')!r}, not read"
    assert m.PERMISSIONS.get("administration") == "read", \
        f"282.4: the manifest asks for Administration {m.PERMISSIONS.get('administration')!r}, not read"
    assert m.PERMISSIONS == app, f"282.4: the manifest's permissions {m.PERMISSIONS} differ from dokima/app.json's {app}"


# 282.5: the manifest is plain data, read without a network

def test_the_manifest_is_read_with_no_network_and_no_github_calls(record_property, tmp_path):
    """The manifest loads and its guard runs with the network and commands blocked.

    Proves 282.5. A fresh Python with sockets and subprocesses made to fail imports the manifest, turns every declared setting into
    JSON (so it is plain data) and runs the guard on the repo."""
    record_property("proves", "282.5")
    manifest("282.5")
    code = textwrap.dedent("""\
        import json, socket, subprocess, sys
        def refuse(*a, **k):
            raise RuntimeError("the manifest reached outside: network or a command")
        socket.socket.connect = refuse
        socket.create_connection = refuse
        subprocess.Popen.__init__ = refuse
        from dokima import manifest as m
        for name in ("LABELS", "FIELDS", "VIEWS", "CHECKS", "BRANCH_RULES", "PERMISSIONS"):
            json.dumps(getattr(m, name))
        m.undeclared(sys.argv[1])
        print("ok")
        """)
    run = subprocess.run([sys.executable, "-c", code, ROOT], cwd=ROOT, capture_output=True, text=True,
                         env={**os.environ, "GH_TOKEN": "", "GITHUB_TOKEN": "", "PYTHONPATH": ROOT})
    assert run.returncode == 0 and run.stdout.strip() == "ok", \
        f"282.5: reading the manifest needed the network, a command or non-JSON data: {run.stderr.strip()[-800:]}"
