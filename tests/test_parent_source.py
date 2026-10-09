"""A criterion may cite the owner's words anywhere in this repo, checked by code (#334).

On #331 the planner linked its criteria to #330, the parent issue where the owner wrote them, and code rejected the
plan twice: a source had to be the story's own issue or one of its comments. The owner then widened the ask: a source
may be any issue of this repo or a comment on one; code checks the source was written by a code owner and that the
quoted words are really there; and the plan reviewer, which judges whether those words are the owner's latest word on
that point, gets the planner's open-issues list plus the full text and comments of every issue the plan cites.

The shape these tests hold code to:
- Each acceptance criterion may carry "quote": the owner's words it traces to, word for word (white space aside). A
  criterion citing the story's own issue or one of its comments is checked as before, with or without a quote. A
  criterion citing any other issue must carry a quote, its source must be written by a code owner (the issue's
  author for its own text, the comment's author for a comment), and the quote must be in that text: for an issue,
  in the owner's part below the card's marker.
- The planner's check (`python3 -m dokima.planner check N OUT`) holds no GitHub key. It reads the owner's words from
  the starting pack named by $PACK, built while the run held a key (`python3 -m dokima.agent pack N ROLE STAGE DEST`).
  With no pack of issue N, only issue N counts as a source, as before.
- The plan review's check (`python3 -m dokima.agent check review`) and the river (`python3 -m dokima.agent next`) do
  the same for an accepted assumption's matched words; the river asks GitHub itself.

The fake GitHub answers the ways GitHub gives an issue and its comments: `gh issue view N --json ...` (with author and
comments), REST `repos/o/r/issues` (the list, by state), `repos/o/r/issues/N`, `repos/o/r/issues/N/comments` and
`repos/o/r/issues/comments` (every comment of the repo). It serves no GraphQL. Reads of an issue listed in
fail_numbers fail as GitHub does (HTTP 502).
"""
import json
import os
import re
import subprocess
import sys

import test_autopilot_river as tr
import test_start as ts
from dokima import agent

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OWNER, STRANGER, BOT = "owner-ann", "stranger-cy", agent.BOT
MARKER = "<!-- dokima-ask -->"


def url(n, comment=None):
    """An issue's link, or one of its comments' links, on the fake GitHub."""
    return f"https://github.com/o/r/issues/{n}" + (f"#issuecomment-{comment}" if comment else "")


def carded(ask, card="The card says what is true now."):
    """An issue body as Dokima keeps it: card above the marker, ask below."""
    return f"<!-- dokima-card -->\n{card}\n<!-- /dokima-card -->\n\n{MARKER}\n\n{ask}"


def said(cid, login, body, t):
    """One comment on the fake GitHub."""
    return {"id": cid, "login": login, "body": body, "createdAt": t}


# --- The repo: #331 is a story of #330; #329 another open issue; #328 opened by someone else; #300 and #299 closed. --

STORY_N, PARENT_N, OTHER_N, STRANGERS_N, CLOSED_N, UNCITED_N = 331, 330, 329, 328, 300, 299
PARENT_ASK = "Every card names the step that failed,\nin plain words.\n\nA second paragraph of the parent."
REPO = {
    STORY_N: {"author": BOT, "state": "open", "body": carded("From the approved plan of #330: the card names the step."),
              "comments": [said(33101, OWNER, "/plan Keep the card short.", "2026-09-30T08:01:01Z")]},
    PARENT_N: {"author": OWNER, "state": "open", "body": carded(PARENT_ASK, card="The board glows red today."),
               "comments": [said(33001, OWNER, "The card should list each step's time too.", "2026-09-30T08:00:01Z"),
                            said(33002, STRANGER, "Make the card blue.", "2026-09-30T08:00:02Z"),
                            said(33003, BOT, "Autopilot said these words.", "2026-09-30T08:00:03Z")]},
    OTHER_N: {"author": OWNER, "state": "open", "body": "Runs that fail say so on the board.",
              "comments": [said(32901, OWNER, "Board pills never lie.", "2026-09-29T07:00:01Z"),
                           said(32902, OWNER, "A later word of the owner on 329.", "2026-09-29T07:00:02Z")]},
    STRANGERS_N: {"author": STRANGER, "state": "open", "body": "The board should be green.", "comments": []},
    CLOSED_N: {"author": OWNER, "state": "closed", "body": "Closed words of the owner.\nMore closed words.",
               "comments": [said(30001, OWNER, "Closed comment of the owner.", "2026-09-28T06:00:01Z")]},
    UNCITED_N: {"author": OWNER, "state": "closed", "body": "Uncited closed words.",
                "comments": [said(29901, OWNER, "Uncited closed comment.", "2026-09-27T05:00:01Z")]},
}

PACK_GH = r'''#!/usr/bin/env python3
"""A fake gh serving the repo in issues.json: issues with their authors, states, bodies and comments; no PRs."""
import json, os, re, sys
a = sys.argv[1:]
d = os.environ["FAKE_GH_DIR"]
ISSUES = {int(k): v for k, v in json.load(open(os.path.join(d, "issues.json"))).items()}
FAIL = set(json.load(open(os.path.join(d, "options.json"))).get("fail_numbers", []))
open(os.path.join(d, "calls.jsonl"), "a").write(json.dumps(a) + "\n")
def flag(*names):
    for name in names:
        if name in a:
            i = a.index(name)
            return a[i + 1] if i + 1 < len(a) else ""
    return None
def link(n, cid=None):
    return "https://github.com/o/r/issues/%d" % n + ("#issuecomment-%d" % cid if cid else "")
def rest_issue(n):
    i = ISSUES[n]
    return {"id": n * 10, "node_id": "I_%d" % n, "number": n, "title": "Issue %d" % n, "body": i["body"],
            "state": i["state"], "html_url": link(n), "url": "https://api.github.com/repos/o/r/issues/%d" % n,
            "user": {"login": i["author"]}, "comments": len(i["comments"]), "labels": []}
def rest_comment(n, c):
    return {"id": c["id"], "node_id": "IC_%d" % c["id"], "html_url": link(n, c["id"]), "body": c["body"],
            "user": {"login": c["login"]}, "created_at": c["createdAt"], "updated_at": c["createdAt"],
            "issue_url": "https://api.github.com/repos/o/r/issues/%d" % n}
def fail_on(n):
    if n in FAIL:
        sys.stderr.write("HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/%d)\n" % n)
        sys.exit(1)
def missing(n):
    sys.stderr.write("gh: Not Found (HTTP 404) issue %d\n" % n)
    sys.exit(1)
def emit(obj, paged=False):
    q = flag("-q", "--jq")
    if q and re.fullmatch(r"\.[A-Za-z_]+", q.strip()) and isinstance(obj, dict):
        print(obj.get(q.strip()[1:], ""))
    elif paged and "--slurp" in a:
        print(json.dumps([obj]))
    else:
        print(json.dumps(obj))
if a[:2] == ["issue", "view"]:
    n = int(str(a[2]).rstrip("/").rsplit("/", 1)[-1].lstrip("#"))
    fail_on(n)
    if n not in ISSUES:
        sys.stderr.write("GraphQL: Could not resolve to an issue or pull request with the number of %d.\n" % n)
        sys.exit(1)
    i = ISSUES[n]
    emit({"number": n, "title": "Issue %d" % n, "body": i["body"], "url": link(n), "state": i["state"].upper(),
          "author": {"login": i["author"]}, "labels": [],
          "comments": [{"id": "IC_%d" % c["id"], "author": {"login": c["login"]}, "body": c["body"],
                        "url": link(n, c["id"]), "createdAt": c["createdAt"]} for c in i["comments"]]})
elif a[:2] == ["pr", "list"]:
    print("" if (flag("-q") or flag("--jq")) else "[]")
elif a[:2] == ["run", "download"]:
    pass
elif a[:1] == ["api"] and "graphql" in a:
    sys.stderr.write("fake gh: this fake GitHub serves no GraphQL\n")
    sys.exit(1)
elif a[:1] == ["api"]:
    path = next((x for x in a[1:] if re.match(r"/?repos/", x)), "")
    path, _, query = path.lstrip("/").partition("?")
    m = re.fullmatch(r"repos/o/r/issues/(\d+)(/comments)?", path)
    if path == "repos/o/r/issues":
        st = re.search(r"state=(\w+)", query)
        state = st.group(1) if st else "open"
        emit([rest_issue(n) for n in sorted(ISSUES, reverse=True) if state == "all" or ISSUES[n]["state"] == state], paged=True)
    elif path == "repos/o/r/issues/comments":
        for n in ISSUES:
            fail_on(n)
        emit([rest_comment(n, c) for n in sorted(ISSUES) for c in ISSUES[n]["comments"]], paged=True)
    elif m:
        n = int(m.group(1))
        fail_on(n)
        if n not in ISSUES:
            missing(n)
        emit([rest_comment(n, c) for c in ISSUES[n]["comments"]] if m.group(2) else rest_issue(n), paged=bool(m.group(2)))
    elif re.fullmatch(r"repos/o/r/(pulls|issues/\d+/(sub_issues|parent|timeline|events|labels)).*", path):
        if path.endswith("/parent") and int(path.split("/")[4]) == 331:
            emit(rest_issue(330))
        elif path.endswith("/parent"):
            missing(int(path.split("/")[4]))
        else:
            emit([], paged=True)
    else:
        sys.stderr.write("fake gh: unsupported call: gh %s\n" % " ".join(a))
        sys.exit(1)
else:
    sys.stderr.write("fake gh: unsupported call: gh %s\n" % " ".join(a))
    sys.exit(1)
'''

NO_KEY_GH = r'''#!/usr/bin/env python3
"""gh with no key, as on the machine where code checks a hand-back: every call fails."""
import sys
sys.stderr.write("gh: To use GitHub CLI in a GitHub Actions workflow, set the GH_TOKEN environment variable.\n")
sys.exit(4)
'''


def tool(dirname, script):
    """Write a gh script into dirname and return the folder, for the front of PATH."""
    os.makedirs(dirname, exist_ok=True)
    path = os.path.join(dirname, "gh")
    open(path, "w").write(script.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
    os.chmod(path, 0o755)
    return dirname


def build_pack(tmp, role, stage, plan=None, fail_numbers=(), number=STORY_N):
    """Build #331's starting pack the way a run does, from the fake GitHub.

    With a plan, #331's comments end with the bot's record of that plan, so the plan reviewer has a plan to review.
    Returns (the pack folder, the command's exit code, its stderr)."""
    t = str(tmp)
    fake = f"{t}/gh"
    os.makedirs(fake, exist_ok=True)
    repo = {n: json.loads(json.dumps(i)) for n, i in REPO.items()}
    if plan is not None:
        repo[STORY_N]["comments"].append({"id": 33199, "login": BOT, "body": agent.render(ts.planner_record(plan)),
                                          "createdAt": "2026-09-30T09:00:00Z"})
    json.dump({str(k): v for k, v in repo.items()}, open(f"{fake}/issues.json", "w"))
    json.dump({"fail_numbers": list(fail_numbers)}, open(f"{fake}/options.json", "w"))
    env = {k: v for k, v in os.environ.items() if k not in ("PACK", "PLANNER_BASE", "PLANNER_RUN_BASE")}
    env.update(PATH=tool(f"{t}/bin", PACK_GH) + ":" + os.environ["PATH"], FAKE_GH_DIR=fake, GITHUB_REPOSITORY="o/r",
               GITHUB_SERVER_URL="https://github.com", GH_TOKEN="fake-github-token", OWNERS=OWNER, PYTHONPATH=ROOT)
    p = subprocess.run([sys.executable, "-m", "dokima.agent", "pack", str(number), role, stage, f"{t}/pack"], cwd=ROOT,
                       env=env, capture_output=True, text=True, timeout=60)
    return f"{t}/pack", p.returncode, p.stderr


def planner_pack(tmp):
    """#331's planner pack, built from the fake GitHub; setup fails if it does not build."""
    pack, code, err = build_pack(tmp, "planner", "")
    assert code == 0, f"test setup: #331's planner pack did not build (exit {code}):\n{err[-1500:]}"
    return pack


def run_check(tmp, plan, pack, number=STORY_N):
    """Run the planner's check on a plan, reading the given pack (None: no pack).

    Runs where code checks a hand-back: no GitHub key (gh fails), no OWNERS, from an empty git repo whose
    CODEOWNERS names the owner, so the check finds no changed tests of its own.
    Returns (exit code, everything it printed and its rejected.txt)."""
    t = str(tmp)
    out, repo = f"{t}/out", f"{t}/repo"
    os.makedirs(out, exist_ok=True)
    os.makedirs(f"{repo}/.github", exist_ok=True)
    open(f"{repo}/.github/CODEOWNERS", "w").write(f"* @{OWNER}\n")
    json.dump(plan, open(f"{out}/plan.json", "w"))
    for cmd in (["init", "-q"], ["config", "user.name", "Test"], ["config", "user.email", "test@example.com"],
                ["add", "-A"], ["commit", "-q", "-m", "start"]):
        subprocess.run(["git", *cmd], cwd=repo, check=True, capture_output=True)
    env = {k: v for k, v in os.environ.items()
           if k not in ("PLANNER_BASE", "PLANNER_RUN_BASE", "PACK", "OWNERS", "GH_TOKEN", "GITHUB_TOKEN")}
    env.update(PATH=tool(f"{t}/nokey", NO_KEY_GH) + ":" + os.environ["PATH"], GITHUB_REPOSITORY="o/r",
               GITHUB_SERVER_URL="https://github.com", PYTHONPATH=ROOT)
    if pack is not None:
        env["PACK"] = pack
    p = subprocess.run([sys.executable, "-m", "dokima.planner", "check", str(number), out], cwd=repo, env=env,
                       capture_output=True, text=True, timeout=60)
    rejected = open(f"{out}/rejected.txt").read() if os.path.exists(f"{out}/rejected.txt") else ""
    return p.returncode, p.stdout + p.stderr + rejected


def crit(source, quote=None, k=1):
    """One acceptance criterion citing this source, with the owner's quoted words when given."""
    c = {"text": f"Criterion {k} holds.", "source": source}
    return c if quote is None else {**c, "quote": quote}


def story(criteria, number=STORY_N):
    """A one-story plan of the issue with these acceptance criteria."""
    return {"kind": "user_story", "summary": "Cards show what is true now.", "user_story": "Cards show what is true now.",
            "acceptance_criteria": criteria, "non_functional": [], "scope": ["dokima/x.py"], "out_of_scope": [],
            "tests": {f"{number}.{k}": [f"tests/test_x.py::test_{k}"] for k in range(1, len(criteria) + 1)},
            "links": {"blocked_by": [], "blocks": [], "relates_to": []}}


def feature(criteria):
    """A two-story split of #331 whose first story has these acceptance criteria."""
    return {"kind": "feature", "summary": "Two stories.", "feature": "Cards show what is true now.",
            "stories": [{"title": "One", "user_story": "u1", "non_functional": [], "depends_on": [],
                         "acceptance_criteria": criteria},
                        {"title": "Two", "user_story": "u2", "non_functional": [], "depends_on": [0],
                         "acceptance_criteria": [crit(url(STORY_N))]}],
            "links": {"blocked_by": [], "blocks": [], "relates_to": []}}


def names(text, k):
    """Whether a rejection names acceptance criterion k (and not, say, k0)."""
    return re.search(rf"acceptance criterion {k}\b", text) is not None


GOOD = crit(url(PARENT_N), "Every card names the step that failed, in plain words.")


def assert_rejected(tmp, pack, bad, case, cid):
    """A story and a split with `bad` second are rejected, naming only that criterion.

    The first criterion cites the owner's real words in the parent, so it must never be named."""
    code, text = run_check(tmp / "story", story([GOOD, bad]), pack)
    assert code != 0, f"{cid} ({case}): the planner's check passed a criterion citing {bad['source']}"
    assert names(text, 2) and bad["source"] in text, \
        f"{cid} ({case}): the rejection does not name acceptance criterion 2 and its source {bad['source']}:\n{text[-1500:]}"
    assert not names(text, 1), f"{cid} ({case}): criterion 1, the owner's real words in #330, was rejected too:\n{text[-1500:]}"
    code, text = run_check(tmp / "split", feature([GOOD, bad]), pack)
    assert code != 0 and "story 1" in text and names(text, 2) and bad["source"] in text, \
        f"{cid} ({case}): a split citing {bad['source']} was not rejected naming story 1, criterion 2 and the source:\n{text[-1500:]}"


def slug(case):
    """A folder name for a case."""
    return re.sub(r"[^a-z0-9]+", "-", case.lower()).strip("-")


# --- 334.1 to 334.4: the planner's check. -------------------------------------------------------------------------

def test_a_criterion_may_cite_the_owners_words_in_any_issue_of_this_repo(record_property, tmp_path):
    """A criterion may cite the owner's words in its own issue, parent or another issue.

    Builds #331's planner pack from a fake GitHub, then runs the real planner check with no GitHub key. A split whose
    criteria cite #331 and its comment (no quote, as before), the parent #330's text (the quote spans a line break
    there) and a code owner's comment on it, and the unrelated #329's text and a code owner's comment on it, each
    with the owner's words, must pass; a story citing the same must raise nothing about any criterion. Proves 334.1."""
    record_property("proves", "334.1")
    pack = planner_pack(tmp_path / "pack")
    criteria = [crit(url(STORY_N)), crit(url(STORY_N, 33101)), GOOD,
                crit(url(PARENT_N, 33001), "list each step's time too"),
                crit(url(OTHER_N), "Runs that fail say so on the board."),
                crit(url(OTHER_N, 32901), "Board pills never lie.")]
    code, text = run_check(tmp_path / "split", feature(criteria), pack)
    assert code == 0, f"334.1: the planner's check rejected a split citing the owner's words in #331, #330 or #329:\n{text[-1500:]}"
    code, text = run_check(tmp_path / "story", story(criteria), pack)
    for k, c in enumerate(criteria, 1):
        assert not names(text, k), f"334.1: the planner's check named acceptance criterion {k} ({c['source']}):\n{text[-1500:]}"


def test_the_planners_prompt_asks_for_the_owners_words_on_each_criterion(record_property):
    """The planner is told to quote the owner's words on each criterion.

    Reads the planner's prompt: the acceptance criterion's shape must show "quote" beside "source", so plans
    the check now asks for can be written at all. Proves 334.1."""
    record_property("proves", "334.1")
    prompt = open(os.path.join(ROOT, "dokima", "roles", "planner.md")).read()
    shape = next((l for l in prompt.splitlines() if '"acceptance_criteria": [{' in l), "")
    assert '"source"' in shape and '"quote"' in shape, \
        f"334.1: the planner's prompt does not show \"quote\" in the acceptance criterion's shape: {shape.strip()!r}"


def test_a_source_not_written_by_a_code_owner_is_rejected(record_property, tmp_path):
    """Words in another issue count only when a code owner wrote them there.

    Runs the real planner check on #331's pack. A criterion quoting the words of an issue someone else opened
    (#328), of someone else's comment on the parent, or of the bot's comment on it must be rejected, naming the
    criterion and the source, while the first criterion, the owner's own words in #330, is never named. Proves 334.2."""
    record_property("proves", "334.2")
    pack = planner_pack(tmp_path / "pack")
    for case, bad in (("an issue someone else opened", crit(url(STRANGERS_N), "The board should be green.", 2)),
                      ("someone else's comment", crit(url(PARENT_N, 33002), "Make the card blue.", 2)),
                      ("the bot's comment", crit(url(PARENT_N, 33003), "Autopilot said these words.", 2))):
        assert_rejected(tmp_path / slug(case), pack, bad, case, "334.2")


def test_quoted_words_not_in_the_source_are_rejected(record_property, tmp_path):
    """A criterion's quoted words must really be in the source it cites, word for word.

    Runs the real planner check on #331's pack. A criterion citing #330 is rejected, naming the criterion and the
    source, when its quote is not in #330, is only in the card above the marker, is in another issue but not in the
    comment it cites, cites a comment that does not exist, or has no quote or an empty one. Proves 334.3."""
    record_property("proves", "334.3")
    pack = planner_pack(tmp_path / "pack")
    for case, bad in (("words not in the issue", crit(url(PARENT_N), "Show the cost of every run.", 2)),
                      ("words only in the card", crit(url(PARENT_N), "The board glows red today.", 2)),
                      ("words from another comment", crit(url(PARENT_N, 33001), "Board pills never lie.", 2)),
                      ("a comment that does not exist", crit(url(PARENT_N, 33099), "Board pills never lie.", 2)),
                      ("no quote", crit(url(PARENT_N), None, 2)),
                      ("an empty quote", crit(url(PARENT_N), "  ", 2))):
        assert_rejected(tmp_path / slug(case), pack, bad, case, "334.3")


def test_a_source_outside_this_repo_or_unreadable_is_still_rejected(record_property, tmp_path):
    """A source outside this repo, or one the check cannot read, is rejected.

    Runs the real planner check on #331's pack. Criteria quoting the parent's real words but citing the same number
    in another repo, on another site, as a pull request or bare, an issue that does not exist, and the owner's real
    words in a closed issue (not in the pack) are each rejected, naming acceptance criterion 2 and its source. Proves 334.4."""
    record_property("proves", "334.4")
    pack = planner_pack(tmp_path / "pack")
    words = "Every card names the step that failed"
    for case, bad in (("another repo", crit(f"https://github.com/x/r/issues/{PARENT_N}", words, 2)),
                      ("another site", crit(f"https://example.com/o/r/issues/{PARENT_N}", words, 2)),
                      ("a pull request", crit(f"https://github.com/o/r/pull/{PARENT_N}", words, 2)),
                      ("a bare number", crit(f"#{PARENT_N}", words, 2)),
                      ("an issue that does not exist", crit(url(3301), words, 2)),
                      ("a closed issue", crit(url(CLOSED_N), "Closed words of the owner.", 2))):
        assert_rejected(tmp_path / slug(case), pack, bad, case, "334.4")


# --- 334.5: the plan review's check and the river accept the owner's words in any issue of this repo. -------------

N, PARENT, OTHER, STRANGERS = int(ts.N), 56, 58, 59
RIVER_ISSUES = {
    PARENT: {"author": ts.OWNER, "body": carded("Every card names the step that failed, in plain words.",
                                                card="The board glows red today."),
             "comments": [{"url": url(PARENT, 501), "login": ts.OWNER, "body": "The card should name the failing step, always."},
                          {"url": url(PARENT, 502), "login": "stranger", "body": "Cards should name the step that broke."},
                          {"url": url(PARENT, 503), "login": BOT, "body": "Autopilot said these words."}]},
    OTHER: {"author": ts.OWNER, "body": "Cards always say which step failed.",
            "comments": [{"url": url(OTHER, 581), "login": ts.OWNER, "body": "Name the step that failed on the card."}]},
    STRANGERS: {"author": "stranger", "body": "Every card names the step that failed, in plain words.", "comments": []},
}

WORDS_SNIPPET = r'''
WORDS = __WORDS__
def _wnum(x):
    try:
        return int(str(x).rstrip("/").rsplit("/", 1)[-1].lstrip("#"))
    except ValueError:
        return None
def _wfail(n):
    if opts.get("fail_words"):
        sys.stderr.write("HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/%d)\n" % n)
        sys.exit(1)
def _wrest(n):
    i = WORDS[str(n)]
    return {"id": n * 10, "number": n, "title": "Issue %d" % n, "body": i["body"], "state": "open",
            "html_url": "https://github.com/o/r/issues/%d" % n, "user": {"login": i["author"]}, "labels": []}
if a[:1] == ["api"] and "graphql" not in a:
    _wp = next((x for x in a if re.fullmatch(r"/?repos/o/r/issues/\d+(/comments)?(\?.*)?", x)), None)
    if _wp and (flag("-X", "--method") or "GET").upper() == "GET":
        _wn = int(re.search(r"issues/(\d+)", _wp).group(1))
        if str(_wn) in WORDS:
            _wfail(_wn)
            if "/comments" in _wp:
                print(json.dumps([{"id": int(c["url"].rsplit("-", 1)[1]), "html_url": c["url"], "user": {"login": c["login"]},
                                   "body": c["body"], "created_at": "2026-10-01T00:00:00Z"} for c in WORDS[str(_wn)]["comments"]]))
            else:
                print(json.dumps(_wrest(_wn)))
            sys.exit(0)
if a[:2] == ["issue", "view"] and len(a) > 2 and str(_wnum(a[2])) in WORDS:
    _wn = _wnum(a[2])
    _wfail(_wn)
    _wi = WORDS[str(_wn)]
    print(json.dumps({"number": _wn, "title": "Issue %d" % _wn, "body": _wi["body"], "url": "https://github.com/o/r/issues/%d" % _wn,
                      "state": "OPEN", "author": {"login": _wi["author"]}, "labels": [],
                      "comments": [{"author": {"login": c["login"]}, "body": c["body"], "url": c["url"],
                                    "createdAt": "2026-10-01T00:00:00Z"} for c in _wi["comments"]]}))
    sys.exit(0)
'''


def fake_with_words(labels):
    """test_autopilot_river's fake GitHub, also serving #56's, #58's and #59's text and comments."""
    base = tr.fake_gh(labels)
    marker = "INITIAL_LABELS = "
    assert marker in base, "test setup: could not find where to teach the fake GitHub other issues' words"
    return base.replace(marker, WORDS_SNIPPET.replace("__WORDS__", repr({str(k): v for k, v in RIVER_ISSUES.items()}))
                        + marker, 1)


def decide(tmp, rec, fail_words=False):
    """Decide what follows a plan review's record on #57, on autopilot, against the fake GitHub.

    Runs `python3 -m dokima.agent next 57`. Returns what it printed, the card with its Next line, where it put the
    card on the board, and its stderr."""
    t = str(tmp)
    for d in ("bin", "gh", "out"):
        os.makedirs(f"{t}/{d}")
    open(f"{t}/bin/gh", "w").write(fake_with_words(tr.ON).replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
    os.chmod(f"{t}/bin/gh", 0o755)
    json.dump({"fail_words": fail_words}, open(f"{t}/gh/options.json", "w"))
    json.dump({"number": N, "title": "Stuck issue", "body": "Fix it.", "author": {"login": ts.OWNER},
               "comments": tr.STORY_Q_PLANNED}, open(f"{t}/gh/issue.json", "w"))
    json.dump(rec, open(f"{t}/out/record.json", "w"))
    open(f"{t}/out/comment.md", "w").write(agent.render(rec))
    env = {k: v for k, v in os.environ.items() if k != "PACK"}
    env.update(PATH=f"{t}/bin:" + os.environ["PATH"], FAKE_GH_DIR=f"{t}/gh", GITHUB_REPOSITORY="o/r",
               GITHUB_SERVER_URL="https://github.com", OWNERS=ts.OWNER, GH_TOKEN="fake-github-token", PYTHONPATH=ROOT)
    p = subprocess.run([sys.executable, "-m", "dokima.agent", "next", str(N), f"{t}/out"], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=60)
    board = open(f"{t}/out/board.txt").read().strip() if os.path.exists(f"{t}/out/board.txt") else ""
    return p.stdout.strip(), open(f"{t}/out/comment.md").read(), board, p.stderr


def judged(matched, source):
    """An approving plan review of #57, its second question accepted on these words."""
    return ts.review_record({**tr.APPROVE, "assumptions": [tr.ACCEPT_1, {**tr.ACCEPT_2, "matched": matched, "source": source}]})


def test_the_plan_reviews_check_accepts_the_owners_words_in_any_issue_of_this_repo(record_property, tmp_path):
    """A plan review may cite the owner's words in any issue of this repo.

    Runs the real code check of plan reviews of #57. An accepted assumption whose source is the parent #56, a comment
    on it, the unrelated #58 or a comment on it passes. One whose source is in another repo, on another site, a pull
    request or bare text is rejected, the problem naming the source. Proves 334.5."""
    record_property("proves", "334.5")
    for case, source in (("the parent", url(PARENT)), ("a comment on the parent", url(PARENT, 501)),
                         ("another issue", url(OTHER)), ("a comment on another issue", url(OTHER, 581))):
        review = {**tr.APPROVE, "assumptions": [tr.ACCEPT_1, {**tr.ACCEPT_2, "source": source}]}
        code, out = tr.check_review(tmp_path / slug(case), review, tr.STORY_Q)
        assert code == 0, f"334.5 ({case}): the plan review's check rejected the owner's words sourced to {source}:\n{out}"
    for case, source in (("another repo", f"https://github.com/x/r/issues/{PARENT}"),
                         ("another site", "https://example.com/post"),
                         ("a pull request", f"https://github.com/o/r/pull/{PARENT}"),
                         ("bare text", "the owner said so")):
        review = {**tr.APPROVE, "assumptions": [tr.ACCEPT_1, {**tr.ACCEPT_2, "source": source}]}
        code, out = tr.check_review(tmp_path / slug(case), review, tr.STORY_Q)
        assert code != 0 and "source" in out, f"334.5 ({case}): the plan review's check accepted words sourced to {source}:\n{out}"


def test_on_autopilot_the_owners_words_in_any_issue_count_only_when_really_theirs(record_property, tmp_path):
    """On autopilot, words in another issue count only when the owner really wrote them.

    Decides what follows an approving plan review of #57 with two questions, on autopilot. The worker starts when
    the second question's words are word for word in the text of the parent #56 or the unrelated #58 (both opened
    by the owner), or in a code owner's comment on either. The river stops for the owner, naming that question, when
    the words are not there, only in #56's card, in someone else's or the bot's comment, or in an issue someone
    else opened (#59). Proves 334.5."""
    record_property("proves", "334.5")
    q2 = tr.QUESTIONS[1]["question"]
    good = (("the parent's text", "names the step that failed, in plain", url(PARENT)),
            ("a code owner's comment on the parent", "name the failing step, always", url(PARENT, 501)),
            ("another issue's text", "Cards always say which step failed.", url(OTHER)),
            ("a code owner's comment on another issue", "Name the step that failed", url(OTHER, 581)))
    for case, matched, source in good:
        out, card, board, err = decide(tmp_path / slug(case), judged(matched, source))
        assert out == "start worker" and board == "Work none", \
            f"334.5 ({case}): the owner's words in {source} did not let the worker start: {out!r} {board!r} {tr.next_of(card)!r}\n{err[-800:]}"
    bad = (("words not in the parent", "Show the cost of every run.", url(PARENT)),
           ("words only in the parent's card", "The board glows red today.", url(PARENT)),
           ("someone else's comment", "Cards should name the step that broke.", url(PARENT, 502)),
           ("the bot's comment", "Autopilot said these words.", url(PARENT, 503)),
           ("an issue someone else opened", "names the step that failed", url(STRANGERS)))
    for case, matched, source in bad:
        out, card, board, err = decide(tmp_path / slug(case), judged(matched, source))
        nxt = tr.next_of(card)
        assert out == "stop" and q2 in nxt and board == "Plan needs", \
            f"334.5 ({case}): words the owner did not write in {source} let the river go on: {out!r} {nxt!r} {board!r}\n{err[-800:]}"


# --- 334.6 and 334.7: the plan reviewer's pack. ------------------------------------------------------------------

CITING = feature([crit(url(STORY_N)), GOOD, crit(url(OTHER_N, 32901), "Board pills never lie."),
                  crit(url(CLOSED_N), "Closed words of the owner.")])


def pack_text(pack):
    """Everything in a pack as text, JSON strings also read back unescaped."""
    parts = []
    for base, _, files in os.walk(pack):
        for f in files:
            raw = open(os.path.join(base, f), errors="replace").read()
            parts.append(raw)
            try:
                parts.append(json.dumps(json.loads(raw), ensure_ascii=False))
            except ValueError:
                pass
    return "\n".join(parts)


def test_the_plan_reviewers_pack_holds_the_planners_open_issues_list(record_property, tmp_path):
    """The plan reviewer gets the same open-issues list the planner gets.

    Builds #331's planner pack and its plan reviewer's pack from the same fake GitHub. The reviewer's
    open_issues.json must equal the planner's and list every open issue; and every open issue's text or comment
    the planner's pack holds must be in the reviewer's pack too. Proves 334.6."""
    record_property("proves", "334.6")
    planner = planner_pack(tmp_path / "planner")
    reviewer, code, err = build_pack(tmp_path / "reviewer", "reviewer", "plan", plan=CITING)
    assert code == 0, f"334.6: the plan reviewer's pack did not build (exit {code}):\n{err[-1500:]}"
    path = os.path.join(reviewer, "open_issues.json")
    assert os.path.exists(path), f"334.6: the plan reviewer's pack has no open_issues.json: {sorted(os.listdir(reviewer))}"
    mine, theirs = json.load(open(path)), json.load(open(os.path.join(planner, "open_issues.json")))
    assert mine == theirs, "334.6: the plan reviewer's open_issues.json differs from the planner's"
    listed = {i.get("number") for i in mine if isinstance(i, dict)}
    assert listed == {n for n, i in REPO.items() if i["state"] == "open"}, f"334.6: the open-issues list holds {sorted(listed)}"
    p_text, r_text = pack_text(planner), pack_text(reviewer)
    for n, i in REPO.items():
        if i["state"] != "open":
            continue
        for words in [l.strip() for l in i["body"].split(MARKER)[-1].splitlines() if l.strip()] + [c["body"] for c in i["comments"]]:
            if words in p_text:
                assert words in r_text, f"334.6: the planner's pack holds {words!r} from #{n} but the plan reviewer's does not"


def test_the_plan_reviewers_pack_holds_every_cited_issue_in_full(record_property, tmp_path):
    """The plan reviewer gets every cited issue in full, closed ones too.

    Builds #331's plan reviewer pack for a plan citing #330, a comment on #329 and the closed #300. The pack must
    hold each cited issue's text and every one of its comments with its author and time, the closed #300 included;
    the closed #299, which no criterion cites, must not be there. Proves 334.7."""
    record_property("proves", "334.7")
    pack, code, err = build_pack(tmp_path / "reviewer", "reviewer", "plan", plan=CITING)
    assert code == 0, f"334.7: the plan reviewer's pack did not build (exit {code}):\n{err[-1500:]}"
    text, quoted = pack_text(pack), json.dumps(CITING)
    for n in (PARENT_N, OTHER_N, CLOSED_N):
        i = REPO[n]
        lines = [l.strip() for l in i["body"].split(MARKER)[-1].splitlines() if l.strip()]
        checked = 0
        for words in lines + [c["body"] for c in i["comments"]]:
            if words in quoted:
                continue  # the plan itself quotes these words, so finding them proves nothing
            checked += 1
            assert words in text, f"334.7: the plan reviewer's pack lacks {words!r} from #{n}, which the plan cites"
        assert checked >= 2, f"test setup: too few of #{n}'s words are left unquoted by the plan to check"
        for c in i["comments"]:
            assert c["createdAt"] in text, f"334.7: the plan reviewer's pack lacks when #{n}'s comment {c['id']} was written"
    assert STRANGER in text, "334.7: the plan reviewer's pack does not say who wrote the comments on #330"
    for words in ("Uncited closed words.", "Uncited closed comment."):
        assert words not in text, f"334.7: the plan reviewer's pack holds the closed #299, which the plan does not cite: {words!r}"


# --- 334.8: the reviewer checks the words are the owner's latest. -------------------------------------------------

def test_the_reviewers_prompt_asks_it_to_check_the_owners_latest_word(record_property):
    """The plan reviewer is told to check each quote is the owner's latest word.

    Whether words are the owner's latest on a point is the reviewer's judgement, so the prompt is what code ships:
    the plan reviewer's prompt must tell it to check the quote is the owner's latest word, to read the cited
    issues in its pack, and to accept a source in any issue of this repo, not only this issue. Proves 334.8."""
    record_property("proves", "334.8")
    prompt = " ".join(open(os.path.join(ROOT, "dokima", "roles", "reviewer.md")).read().split())
    low = prompt.lower()
    assert "latest word" in low, "334.8: the reviewer's prompt does not ask it to check the owner's latest word"
    at = low.index("latest word")
    near = low[max(0, at - 400): at + 400]
    assert "quote" in near, f"334.8: the reviewer's prompt does not tie the latest word to each criterion's quote: {near!r}"
    assert "open_issues.json" in prompt, "334.8: the reviewer's prompt does not point it to the open-issues list in its pack"
    assert "the issue's own link, the link of a code owner's comment on it, or AGENTS.md" not in prompt, \
        "334.8: the reviewer's prompt still limits an assumption's source to this issue, its comments or AGENTS.md"


# --- 334.9 and 334.10: failing closed. ---------------------------------------------------------------------------

def test_when_github_cannot_give_a_cited_issues_words_nothing_counts(record_property, tmp_path):
    """When GitHub cannot give a cited issue's words, nothing counts as said there.

    Builds #331's plan reviewer pack while every read of the cited #300 fails as GitHub does (HTTP 502): the
    build must fail, its last error line naming #300, where it builds when GitHub answers. Then decides what follows
    an approving plan review of #57 on autopilot accepted on the owner's words in #58: with GitHub failing to give
    #58 the river stops for the owner naming that question, and with GitHub answering the worker starts. Proves 334.9."""
    record_property("proves", "334.9")
    _, code, err = build_pack(tmp_path / "ok", "reviewer", "plan", plan=CITING)
    assert code == 0, f"334.9: setup: with GitHub answering, the plan reviewer's pack did not build:\n{err[-1500:]}"
    _, code, err = build_pack(tmp_path / "fail", "reviewer", "plan", plan=CITING, fail_numbers=[CLOSED_N])
    last = (err.strip().splitlines() or [""])[-1]
    assert code != 0 and str(CLOSED_N) in last, \
        f"334.9: with GitHub failing to give the cited #300, the pack built anyway or did not name #300 (exit {code}): {last!r}"
    rec = judged("Cards always say which step failed.", url(OTHER))
    out, card, board, err = decide(tmp_path / "river-ok", rec)
    assert out == "start worker", f"334.9: setup: with GitHub answering, the owner's words in #58 did not count: {out!r}\n{err[-800:]}"
    out, card, board, err = decide(tmp_path / "river-fail", rec, fail_words=True)
    nxt = tr.next_of(card)
    assert out == "stop" and tr.QUESTIONS[1]["question"] in nxt and board == "Plan needs", \
        f"334.9: with GitHub failing to give #58, the river went on on its words: {out!r} {nxt!r} {board!r}\n{err[-800:]}"


def test_with_no_pack_of_this_issue_only_its_own_issue_counts(record_property, tmp_path):
    """With no pack of this issue, only its own issue counts as a source.

    Runs the real planner check on a plan citing the owner's real words in #330: with #331's own pack it passes;
    with no pack, and for #329 checked against #331's pack, it is rejected naming the criterion and source. A plan
    citing only its own issue still passes with no pack. Proves 334.10."""
    record_property("proves", "334.10")
    pack = planner_pack(tmp_path / "pack")
    code, text = run_check(tmp_path / "own-pack", feature([GOOD]), pack)
    assert code == 0, f"334.10: setup: with #331's own pack, the owner's words in #330 were rejected:\n{text[-1500:]}"
    for case, number, where in (("no pack", STORY_N, None), ("another issue's pack", OTHER_N, pack)):
        plan = feature([GOOD])
        plan["stories"][1]["acceptance_criteria"] = [crit(url(number))]
        code, text = run_check(tmp_path / slug(case), plan, where, number=number)
        assert code != 0 and names(text, 1) and GOOD["source"] in text, \
            f"334.10 ({case}): the check accepted #330 as a source without #{number}'s pack:\n{text[-1500:]}"
    code, text = run_check(tmp_path / "own-only", feature([crit(url(STORY_N), k=1)]), None)
    assert code == 0, f"334.10: with no pack, a plan citing only its own issue was rejected:\n{text[-1500:]}"
