"""The planner finds the open issues this one is blocked by, blocks or relates to, and the owner sees them on the card.

Issue #231. The planner's starting pack holds the repo's open issues; its prompt tells it to find the links; its
hand-back carries them in a `links` field of three lists; the round check every planner run does
(`python3 -m dokima.agent check-round planner FILE PACK`) rejects a missing or malformed field, a number that is not
one of the open issues in the pack, and a link to the issue itself; and the issue card shows each list with its own icon.

GitHub is faked: `gh issue view` and `gh pr list` answer for issue 231, and the repo's open issues are served to both
ways of listing them, `gh issue list` (which honours `--limit`/`-L`, 30 by default, as gh does) and
`gh api repos/o/r/issues` (which pages at `per_page`, 30 by default, unless `--paginate` is given, and also lists pull
requests, each with a `pull_request` key, as GitHub's API does). Any other GitHub call fails the test naming it.
"""
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urlparse

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from dokima import agent, card  # noqa: E402

N = 231
PROMPT = os.path.join(ROOT, "dokima", "roles", "planner.md")
ICONS = os.path.join(ROOT, "dokima", "icons")
STATUS_ICONS = {"passed", "failed", "running", "none", "queued", "cancelled"}
SRC = f"https://github.com/o/r/issues/{N}"
STORY = {"kind": "user_story", "summary": "Links between issues.", "user_story": "The owner sees what waits on what.",
         "acceptance_criteria": [{"text": "A thing happens.", "source": SRC}],
         "non_functional": [], "scope": ["dokima/x.py"], "out_of_scope": [],
         "tests": {f"{N}.1": ["tests/test_x.py::test_a"]}}
FEATURE = {"kind": "feature", "summary": "Two stories.", "feature": "f", "stories": [
    {"title": "One", "user_story": "u1", "acceptance_criteria": [{"text": "a", "source": SRC}], "non_functional": [],
     "depends_on": []},
    {"title": "Two", "user_story": "u2", "acceptance_criteria": [{"text": "b", "source": SRC}], "non_functional": [],
     "depends_on": [0]}]}
GOOD_LINKS = {"blocked_by": [12, 13], "blocks": [15], "relates_to": [18]}


def open_issue(n):
    """One open issue as GitHub lists it."""
    return {"number": n, "title": f"Issue title {n}", "body": f"Issue body {n}", "state": "OPEN"}


def fake_github(monkeypatch, issues, prs=(), fail=False):
    """Fake GitHub for agent.gh: issue 231 with no comments and no pull request, and these open issues and PRs.

    With fail set, listing the open issues fails as a GitHub outage would."""
    def gh(*args):
        if args[:2] == ("issue", "view"):
            return json.dumps({"number": N, "title": "Links", "body": "the ask", "comments": []})
        if args[:2] == ("pr", "list"):
            return "[]"
        if args[:2] == ("issue", "list"):
            if fail:
                raise subprocess.CalledProcessError(1, ["gh", *args], "", "HTTP 502: Bad Gateway")
            limit = 30
            for flag in ("--limit", "-L"):
                if flag in args:
                    limit = int(args[args.index(flag) + 1])
            return json.dumps([open_issue(n) for n in issues][:limit])
        if args[0] == "api" and re.match(r"/?repos/o/r/issues(\?|$)", args[1]):
            if fail:
                raise subprocess.CalledProcessError(1, ["gh", *args], "", "HTTP 502: Bad Gateway")
            items = sorted([open_issue(n) for n in issues] + [dict(open_issue(n), pull_request={"url": "u"}) for n in prs],
                           key=lambda i: i["number"])
            if "--paginate" in args:
                return json.dumps([items] if "--slurp" in args else items)
            q = parse_qs(urlparse(args[1]).query)
            per, page = int(q.get("per_page", ["30"])[0]), int(q.get("page", ["1"])[0])
            return json.dumps(items[(page - 1) * per:page * per])
        raise AssertionError(f"unexpected GitHub call: gh {' '.join(map(str, args))}")
    monkeypatch.setattr(agent, "gh", gh)


def planner_pack(monkeypatch, where, issues, prs=()):
    """Build the planner's starting pack for issue 231 the way a run does, from the faked GitHub."""
    fake_github(monkeypatch, issues, prs)
    dest = str(where / "pack")
    agent.pack("o/r", N, "planner", "", dest)
    return dest


def check_round(where, handback, pack):
    """Run the round check a planner run does on this hand-back; return (exit code, stdout, stderr)."""
    f = where / "plan.json"
    f.write_text(json.dumps(handback))
    r = subprocess.run([sys.executable, "-m", "dokima.agent", "check-round", "planner", str(f), pack], cwd=ROOT,
                       capture_output=True, text=True, env={**os.environ, "PYTHONPATH": ROOT}, timeout=60)
    return r.returncode, r.stdout, r.stderr


def test_the_planners_pack_holds_every_open_issue_of_the_repo(record_property, tmp_path, monkeypatch):
    """The planner's starting pack lists every open issue of the repo, with its number, title and body, and no pull requests.

    Fakes a repo with 250 open issues (more than any single page or gh's default of 30) and three open pull requests,
    builds the planner's pack, and reads open_issues.json: it must list exactly the 250 issues, each with its own
    title and body, and none of the pull requests."""
    record_property("proves", "231.1")
    issues, prs = list(range(1, 251)), [300, 301, 302]
    pack = planner_pack(monkeypatch, tmp_path, issues, prs)
    path = os.path.join(pack, "open_issues.json")
    assert os.path.isfile(path), "231.1: the planner's pack has no open_issues.json listing the repo's open issues"
    listed = json.load(open(path))
    assert isinstance(listed, list) and all(isinstance(i, dict) for i in listed), \
        "231.1: open_issues.json is not a list of issues, one object each"
    numbers = sorted(i.get("number") for i in listed)
    assert not set(prs) & set(numbers), f"231.1: open_issues.json lists pull requests {sorted(set(prs) & set(numbers))}"
    assert numbers == issues, (f"231.1: open_issues.json lists {len(numbers)} issues, not all {len(issues)} open ones "
                               f"(missing e.g. {sorted(set(issues) - set(numbers))[:5]})")
    for i in listed:
        assert (i.get("title"), i.get("body")) == (f"Issue title {i['number']}", f"Issue body {i['number']}"), \
            f"231.1: issue #{i['number']} is listed without its own title and body: {i}"
    assert os.path.isfile(os.path.join(pack, "issue.md")), "231.1: the pack lost issue.md"


def test_the_planners_prompt_tells_it_to_find_and_hand_back_the_links(record_property):
    """The planner's prompt tells it to read the open issues and hand back which ones this issue is blocked by, blocks and relates to.

    Reads dokima/roles/planner.md, the prompt every planner run starts from: it must name the pack's
    open_issues.json, say "blocked by", "blocks" and "relates to", and show the links field with its three lists,
    blocked_by, blocks and relates_to, in the hand-back's shape."""
    record_property("proves", "231.2")
    text = open(PROMPT, encoding="utf-8").read()
    low = text.lower()
    assert "open_issues.json" in text, "231.2: the planner's prompt never points it at the pack's open_issues.json"
    for words in ("blocked by", "blocks", "relates to"):
        assert words in low, f"231.2: the planner's prompt never asks which open issues this one {words}"
    for field in ('"links"', '"blocked_by"', '"blocks"', '"relates_to"'):
        assert field in text, f"231.2: the hand-back shape in the planner's prompt has no {field} field"


def test_the_links_field_must_be_there_and_well_formed(record_property, tmp_path, monkeypatch):
    """A planner hand-back passes with a well-formed links field and is rejected, naming the field, when it is missing or malformed.

    Builds the pack with open issues 12, 13, 15, 18 and 231, then runs the real round check: three lists of open issue
    numbers pass, as do three empty lists, on a story and on a split. No links field, links as a list, a missing list,
    a list that is not a list, a number written as text and true as a number are each rejected (exit 1) naming the
    field at fault, never with a crash."""
    record_property("proves", "231.3")
    pack = planner_pack(monkeypatch, tmp_path, [12, 13, 15, 18, N])
    empty = {"blocked_by": [], "blocks": [], "relates_to": []}
    for name, h in (("a story with links", {**STORY, "links": GOOD_LINKS}), ("a story with no links", {**STORY, "links": empty}),
                    ("a split with links", {**FEATURE, "links": GOOD_LINKS})):
        code, out, err = check_round(tmp_path, h, pack)
        assert (code, out.strip()) == (0, ""), f"231.3: {name} was rejected: {out}{err[-400:]}"
    no_relates = {k: v for k, v in GOOD_LINKS.items() if k != "relates_to"}
    bad = [("no links field", STORY, "links"), ("links as a list", {**STORY, "links": [12]}, "links"),
           ("no relates_to list", {**STORY, "links": no_relates}, "relates_to"),
           ("blocks as one number", {**STORY, "links": {**GOOD_LINKS, "blocks": 15}}, "blocks"),
           ("a number written as text", {**STORY, "links": {**GOOD_LINKS, "blocked_by": ["12"]}}, "blocked_by"),
           ("true as a number", {**STORY, "links": {**GOOD_LINKS, "relates_to": [True]}}, "relates_to"),
           ("a split with no links field", FEATURE, "links")]
    for name, h, field in bad:
        code, out, err = check_round(tmp_path, h, pack)
        assert "Traceback" not in err, f"231.3: the round check crashed on {name}:\n{err[-600:]}"
        assert code == 1, f"231.3: a hand-back with {name} passed the round check"
        assert field in out, f"231.3: the rejection of {name} does not name {field}: {out}"


def test_links_name_only_real_open_issues_and_never_the_issue_itself(record_property, tmp_path, monkeypatch):
    """A link to a number that is not an open issue of the repo, or to the issue itself, is rejected naming it; real ones pass.

    Builds the pack with open issues 12, 13, 15, 18 and 231 and open pull request 300, then runs the real round check:
    links to 12, 13, 15 and 18 pass. A link to 999 (no such open issue), to 300 (a pull request, not an issue) or to
    231 (the issue itself, in any of the three lists) is rejected (exit 1) naming the number, and the self-link says
    "itself"; with two bad links at once, both are named. A split is held to the same rule."""
    record_property("proves", "231.3")
    pack = planner_pack(monkeypatch, tmp_path, [12, 13, 15, 18, N], prs=[300])
    code, out, err = check_round(tmp_path, {**STORY, "links": GOOD_LINKS}, pack)
    assert (code, out.strip()) == (0, ""), f"231.3: links to real open issues were rejected: {out}{err[-400:]}"
    cases = [("a link to #999, no open issue", {**GOOD_LINKS, "blocks": [15, 999]}, ["999"]),
             ("a link to pull request #300", {**GOOD_LINKS, "relates_to": [300]}, ["300"])]
    cases += [(f"the issue linked to itself in {k}", {**GOOD_LINKS, k: [N]}, [str(N), "itself"]) for k in GOOD_LINKS]
    cases += [("two bad links at once", {"blocked_by": [N], "blocks": [999], "relates_to": []}, [str(N), "itself", "999"])]
    for name, links, said in cases:
        for kind, h in (("story", STORY), ("split", FEATURE)):
            code, out, err = check_round(tmp_path, {**h, "links": links}, pack)
            assert "Traceback" not in err, f"231.3: the round check crashed on a {kind} with {name}:\n{err[-600:]}"
            assert code == 1, f"231.3: a {kind} with {name} passed the round check"
            for s in said:
                assert s in out, f"231.3: the rejection of a {kind} with {name} does not say {s!r}: {out}"


def planner_record(links=None):
    """A planner record that passed its check, with these links (none at all when None, as older plans have)."""
    h = dict(STORY, **({"links": links} if links is not None else {}))
    return {"role": "planner", "stage": None, "handback": h, "check": {"passed": True, "problems": []},
            "run": "https://github.com/o/r/actions/runs/1"}


def draw(links=None, page="issue"):
    """The issue card for issue 231 drawn from one planner record, on the issue or its pull request."""
    items = card.as_items([planner_record(links)], "owner")
    pr = {"number": 5, "merged": False, "state": "open"} if page == "pr" else None
    found = {"recs": agent.records(items), "items": items, "pr": pr, "check_runs": [], "reviews": [],
             "owners": {"owner"}, "tests": {}, "worker": None, "children": []}
    return card.render("o/r", {"number": N, "url": SRC}, found, page=page)


def icons_on(line):
    """The names of Dokima's icons drawn on one line of a card."""
    return re.findall(r'src="[^"]*/dokima/icons/([\w-]+)\.svg"', line)


def link_icons(text):
    """Dokima's icons on a card that are not the verdict and run icons."""
    return {i for line in text.splitlines() for i in icons_on(line) if i not in STATUS_ICONS}


def test_the_card_shows_each_kind_of_link_with_its_own_icon(record_property):
    """The card shows the issues this one is blocked by, blocks and relates to, each kind on its own line with its own icon.

    Draws the issue card, on the issue and on its pull request, from a plan blocked by #12 and #13, blocking #15 and
    relating to #18. Each kind sits on one line with its label (Blocked by, Blocks, Relates to), exactly its own
    numbers, and one icon of its own: three different icons, none of them a verdict or run icon, each an SVG file in
    dokima/icons."""
    record_property("proves", "231.4")
    for page in ("issue", "pr"):
        text = draw(GOOD_LINKS, page)
        lines = text.splitlines()
        seen = {}
        for kind, label, mine in (("blocked_by", "blocked by", [12, 13]), ("blocks", "blocks", [15]),
                                  ("relates_to", "relates to", [18])):
            rows = [l for l in lines if re.search(rf"#{mine[0]}\b", l)]
            assert len(rows) == 1, f"231.4: the {page} card shows #{mine[0]} ({label}) on {len(rows)} lines, not one:\n{text}"
            row = rows[0]
            assert label in row.lower(), f"231.4: the {page} card's line for #{mine[0]} does not say {label}: {row}"
            for n in (12, 13, 15, 18):
                assert bool(re.search(rf"#{n}\b", row)) == (n in mine), \
                    f"231.4: the {page} card's {label} line {'misses' if n in mine else 'also shows'} #{n}: {row}"
            own = [i for i in icons_on(row) if i not in STATUS_ICONS]
            assert len(own) == 1, f"231.4: the {page} card's {label} line has {len(own)} icons of its own, not one: {row}"
            seen[kind] = own[0]
        assert len(set(seen.values())) == 3, f"231.4: the three kinds of link share icons on the {page} card: {seen}"
    for name in seen.values():
        path = os.path.join(ICONS, f"{name}.svg")
        assert os.path.isfile(path), f"231.4: the card draws the icon {name}, but dokima/icons/{name}.svg does not exist"
        assert ET.parse(path).getroot().tag.endswith("svg"), f"231.4: dokima/icons/{name}.svg is not an SVG"


def test_the_card_shows_no_line_for_a_kind_with_no_links(record_property):
    """The card leaves out every kind of link the plan has none of, and a plan from before links draws as it did.

    Draws the card from a plan blocking only #15: the Blocks line is there with its icon, and nothing says blocked by
    or relates to. Then from a plan with three empty lists and from an older plan with no links field: neither shows
    any link icon or link line, and both still draw."""
    record_property("proves", "231.4")
    full = draw(GOOD_LINKS)
    found = [i for l in full.splitlines() if re.search(r"#15\b", l) for i in icons_on(l) if i not in STATUS_ICONS]
    assert found, f"231.4: the card for a plan blocking #15 draws no Blocks line with its own icon:\n{full}"
    blocks_icon = found[0]
    only = draw({"blocked_by": [], "blocks": [15], "relates_to": []})
    assert re.search(r"#15\b", only), f"231.4: a plan blocking only #15 does not show #15 on the card:\n{only}"
    assert link_icons(only) == {blocks_icon}, f"231.4: a plan blocking only #15 draws link icons {link_icons(only)}"
    for words in ("blocked by", "relates to"):
        assert words not in only.lower(), f"231.4: a plan with no {words} links still shows a {words} line:\n{only}"
    for name, links in (("three empty lists", {"blocked_by": [], "blocks": [], "relates_to": []}), ("no links field", None)):
        text = draw(links)
        assert "**Acceptance criteria**" in text, f"231.4: the card with {name} no longer draws the plan:\n{text}"
        assert not link_icons(text), f"231.4: the card with {name} draws link icons {link_icons(text)}"
        for words in ("blocked by", "relates to"):
            assert words not in text.lower(), f"231.4: the card with {name} shows a {words} line:\n{text}"


def test_the_planner_never_plans_without_the_open_issues(record_property, tmp_path, monkeypatch):
    """When the open issues cannot be read, the planner's pack fails instead of handing it an empty list, and its hand-back is refused.

    Fakes GitHub failing to list the open issues: building the planner's pack must fail with GitHub's error, and must
    leave no open_issues.json behind. Then runs the real round check on a well-formed hand-back against a pack with no
    open_issues.json: it is rejected (exit 1) naming open_issues.json."""
    record_property("proves", "231.5")
    fake_github(monkeypatch, [12], fail=True)
    dest = tmp_path / "pack"
    with pytest.raises(Exception) as e:
        agent.pack("o/r", N, "planner", "", str(dest))
    assert not isinstance(e.value, AssertionError), f"231.5: the pack made a GitHub call the fake does not know: {e.value}"
    assert not (dest / "open_issues.json").exists(), "231.5: the pack wrote open_issues.json though GitHub could not list them"
    bare = tmp_path / "bare"
    (bare / "in").mkdir(parents=True)
    (bare / "issue.md").write_text(f"# Issue #{N}: Links\n\nthe ask\n\n## Comments\n")
    (bare / "open_blockers.json").write_text("[]")
    code, out, err = check_round(tmp_path, {**STORY, "links": {"blocked_by": [], "blocks": [], "relates_to": []}}, str(bare))
    assert "Traceback" not in err, f"231.5: the round check crashed on a pack with no open issues:\n{err[-600:]}"
    assert code == 1 and "open_issues.json" in out, \
        f"231.5: a hand-back was accepted against a pack with no open_issues.json (exit {code}): {out}"
