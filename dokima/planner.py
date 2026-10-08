"""The planner's hand-back: check its shape, then write it into the issue.

    python3 -m dokima.planner check N OUT   # fail loudly unless OUT holds a well-formed plan
    python3 -m dokima.planner post N OUT    # write the plan into issue N, or post the proposed split
    python3 -m dokima.planner rejected N OUT  # say on issue N why the run was rejected

The planner holds no GitHub key. It ends by writing one plan.json to OUT, of kind user_story or feature (see
dokima/roles/planner.md), with its questions for the owner listed inside it, plus its tests in tests/. Every
criterion's source is issue N or one of its comments; every test it names is in the repo, filed under one of the
plan's criteria. Every older test it changes, renames or deletes needs a reason in test_changes. Every new test has a
one-sentence summary and fails on today's code.
Nothing is posted unless `check` passes.
"""

import ast
import json
import os
import re
import subprocess
import sys

from dokima.checks import PROVES, TEST_DEF
from dokima.agent import problems_questions  # noqa: E402

ORIGINAL_START = "<!-- dokima-original -->"
ORIGINAL_END = "<!-- /dokima-original -->"
NEW_TEST_TIMEOUT = 60  # seconds one new test may run on today's code before it is stopped and rejected


class Garbled(Exception):
    pass


ALWAYS = ("the planner always hands back a plan, a plan.json of kind user_story or feature, "
          "with its questions listed inside it")


def issue_link(number):
    """This issue's link on GitHub, from the repo the check runs in."""
    server = os.environ.get("GITHUB_SERVER_URL") or "https://github.com"
    return f"{server}/{os.environ.get('GITHUB_REPOSITORY', '')}/issues/{number}"


def read_output(out, number=None):
    """('plan', dict) or ('feature', str); Garbled if OUT holds anything else.

    Given the issue number, every criterion's source must be that issue's link or one of its comment links.
    """
    if os.path.exists(os.path.join(out, "question.md")):
        raise Garbled(f"found question.md: {ALWAYS}")
    if not os.path.exists(os.path.join(out, "plan.json")):
        raise Garbled(f"found no plan.json: {ALWAYS}")
    try:
        p = json.load(open(os.path.join(out, "plan.json")))
    except ValueError as e:
        raise Garbled(f"plan.json is not valid JSON: {e}")
    if not isinstance(p, dict):
        raise Garbled(f"plan.json must be an object, not a {type(p).__name__}: {ALWAYS}")
    if "kind" not in p:
        raise Garbled(f"plan.json has no kind: {ALWAYS}")
    return from_kind(p, issue_link(number) if number is not None else None)


def strings(v):
    return isinstance(v, list) and all(isinstance(x, str) and x.strip() for x in v)


def check_source(where, source, issue):
    """Garbled unless the source is this issue's link or one of its comment links; no issue given, nothing to check."""
    if issue and not re.fullmatch(re.escape(issue) + r"(#issuecomment-\d+)?", source.strip()):
        raise Garbled(f"{where} has the source {source}, which is not this issue ({issue}) or one of its comments")


def check_stories(stories, issue=None):
    """Garbled unless every story of a split is complete, its criteria cite this issue, and its dependencies point at
    the split's own stories with no loop. Stories are named counting from 1, as the split's card numbers them;
    depends_on counts from 0."""
    for n, s in enumerate(stories, 1):
        if not isinstance(s, dict):
            raise Garbled(f"story {n} must be an object with its title, user_story, acceptance_criteria and depends_on")
        for key in ("title", "user_story"):
            if not isinstance(s.get(key), str) or not s[key].strip():
                raise Garbled(f"story {n} has no {key}")
        ac = s.get("acceptance_criteria")
        if not isinstance(ac, list) or not ac:
            raise Garbled(f"story {n} needs acceptance_criteria as a non-empty list")
        for k, c in enumerate(ac, 1):
            if not isinstance(c, dict):
                raise Garbled(f"story {n}: acceptance criterion {k} must be an object with its text and source")
            for key in ("text", "source"):
                if not isinstance(c.get(key), str) or not c[key].strip():
                    raise Garbled(f"story {n}: acceptance criterion {k} has no {key}")
            check_source(f"story {n}: acceptance criterion {k}", c["source"], issue)
        nfr = s.get("non_functional", [])
        if not isinstance(nfr, list):
            raise Garbled(f"story {n} needs non_functional as a list (empty for none)")
        for k, c in enumerate(nfr, 1):
            if not isinstance(c, dict):
                raise Garbled(f"story {n}: non-functional requirement {k} must be an object with its text and why")
            for key in ("text", "why"):
                if not isinstance(c.get(key), str) or not c[key].strip():
                    raise Garbled(f"story {n}: non-functional requirement {k} needs its text and why as non-empty "
                                  f"text, and its {key} is not")
        if not isinstance(s.get("depends_on"), list):
            raise Garbled(f"story {n} needs depends_on as a list (empty for no dependencies)")
    last = len(stories) - 1
    for n, s in enumerate(stories, 1):
        for d in s["depends_on"]:
            if not isinstance(d, int) or isinstance(d, bool) or not 0 <= d <= last:
                raise Garbled(f"story {n} depends on {d!r}, which is no story index of this split (0 to {last})")
            if d == n - 1:
                raise Garbled(f"story {n} depends on itself")
    state = {}  # index -> "open" while on the path, "done" once every story it waits on is clear

    def visit(i, path):
        state[i] = "open"
        for d in stories[i]["depends_on"]:
            if state.get(d) == "open":
                loop = path[path.index(d):]
                raise Garbled("stories wait on each other in a loop: " + ", ".join(f"story {j + 1}" for j in loop))
            if d not in state:
                visit(d, path + [d])
        state[i] = "done"

    for i in range(len(stories)):
        if i not in state:
            visit(i, [i])


def from_kind(p, issue=None):
    """Read a plan.json written in the agreed shape (user_story or feature) into what the rest of the code uses.

    A story becomes a plan: its acceptance criteria come first, then its non-functional requirements, numbered N.1,
    N.2 ... in that order. A feature is shown to the owner as handed back, as a comment. Given this issue's link,
    every criterion's source must be it or one of its comment links.
    """
    kind = p["kind"]
    if kind == "feature":
        stories = p.get("stories")
        if not isinstance(stories, list) or not 2 <= len(stories) <= 5:
            raise Garbled("a feature needs 2 to 5 stories")
        check_stories(stories, issue)
        bad = problems_questions(p.get("questions", []))
        if bad:
            raise Garbled("; ".join(bad))
        return "feature", json.dumps(p, indent=2)
    if kind != "user_story":
        raise Garbled(f"plan.json kind is {kind!r}: {ALWAYS}")
    if not isinstance(p.get("user_story"), str) or not p["user_story"].strip():
        raise Garbled("a story needs a non-empty user_story")
    ac, nfr = p.get("acceptance_criteria"), p.get("non_functional", [])
    if not isinstance(ac, list) or not ac:
        raise Garbled("a story needs a non-empty list of acceptance_criteria")
    for k, c in enumerate(ac, 1):
        if not isinstance(c, dict):
            raise Garbled(f"acceptance criterion {k} must be an object with its text and source")
        for key in ("text", "source"):
            if not isinstance(c.get(key), str) or not c[key].strip():
                raise Garbled(f"acceptance criterion {k} has no {'source link' if key == 'source' else key}: "
                              f"its {key} must be non-empty text")
        check_source(f"acceptance criterion {k}", c["source"], issue)
    if not isinstance(nfr, list):
        raise Garbled("a story needs non_functional as a list (empty for none)")
    for k, c in enumerate(nfr, 1):
        if not isinstance(c, dict):
            raise Garbled(f"non-functional requirement {k} must be an object with its text and why")
        for key in ("text", "why"):
            if not isinstance(c.get(key), str) or not c[key].strip():
                raise Garbled(f"non-functional requirement {k} needs its text and why as non-empty text, "
                              f"and its {key} is not")
    if not strings(p.get("scope")) or not p["scope"]:
        raise Garbled("a story needs scope as a non-empty list of files")
    if not strings(p.get("out_of_scope", [])):
        raise Garbled("out_of_scope must be a list of sentences")
    tests = p.get("tests")
    if not isinstance(tests, dict) or not all(isinstance(k, str) and strings(v) for k, v in tests.items()):
        raise Garbled("a story needs tests as a map from each criterion (N.k) to its tests")
    tc = p.get("test_changes", {})
    if not isinstance(tc, dict) or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in tc.items()):
        raise Garbled("plan.json test_changes must map each changed older test to a non-empty reason")
    return "plan", {"objective": p["user_story"].strip(),
                    "criteria": [c["text"].strip() for c in ac] + [f"{c['text'].strip()} ({c['why'].strip()})" for c in nfr],
                    "non_goals": p.get("out_of_scope", []), "scope": p["scope"], "test_changes": tc,
                    "declared": tests, "raw": p}


def declared_by_test(declared):
    """Each test the plan names -> the criterion keys it is filed under."""
    by_test = {}
    for key, names in declared.items():
        for t in names:
            by_test.setdefault(t, []).append(key)
    return by_test


def declared_labels(tc, declared):
    """Use the criteria the plan declares for each test, never labels guessed from the test's text."""
    by_test = declared_by_test(declared)
    added = {t: by_test.get(t, []) for t in tc["added"]}
    renamed = tc.get("renamed", {})
    changed = {t: (old, by_test.get(renamed.get(t, t), old)) for t, (old, _) in tc["changed"].items()}
    return dict(tc, added=added, changed=changed)


def test_functions(text):
    """Each test function in a file: name -> (its source, the criterion keys it proves)."""
    out, name, block = {}, None, []
    for line in (text or "").splitlines() + ["\x00end"]:
        top = line[:1] not in ("", " ", "\t")
        if top and name:
            src = "\n".join(block).rstrip()
            out[name] = (src, PROVES.findall(src))
            name, block = None, []
        found = TEST_DEF.match(line)
        if found:
            name = found.group(1)
        if name:
            block.append(line)
    return out


def test_changes(paths, before, after):
    """Tests the planner touched, by path::name: added, changed (with their old keys) and deleted.

    A test whose source is unchanged apart from its name is a rename: a change, filed under its old name, with its
    new name under renamed (old -> new), a key that is there only when something was renamed.
    """
    added, changed, deleted, renamed = {}, {}, {}, {}
    for path in paths:
        old, new = test_functions(before(path)), test_functions(after(path))
        gone = [name for name in old if name not in new]
        for name, (src, keys) in new.items():
            if name not in old:
                was = next((o for o in gone if old[o][0].replace(f"def {o}(", f"def {name}(", 1) == src), None)
                if was:
                    gone.remove(was)
                    changed[f"{path}::{was}"] = (old[was][1], keys)
                    renamed[f"{path}::{was}"] = f"{path}::{name}"
                else:
                    added[f"{path}::{name}"] = keys
            elif old[name][0] != src:
                changed[f"{path}::{name}"] = (old[name][1], keys)
        for name in gone:
            deleted[f"{path}::{name}"] = old[name][1]
    return dict({"added": added, "changed": changed, "deleted": deleted}, **({"renamed": renamed} if renamed else {}))


def proving(tc):
    """Each added or changed test with the keys it proves now."""
    return dict(tc["added"], **{t: new for t, (_, new) in tc["changed"].items()})


def missing_tests(names):
    """The named tests (path::name) that are not in the repo: no such file, or no such test in it."""
    return [t for t in names if t.partition("::")[2] not in test_functions(read_now(t.partition("::")[0]))]


def problems(number, plan, files, tc, declared=None):
    """What is wrong with a plan and the tests it touched; empty when it can be posted.

    Given the tests the plan declares, each must be in the repo and filed under one of the plan's criteria, and an
    older test already in the repo counts as proof of the criteria it is filed under.
    """
    out = [f"{p} is outside tests/; the planner may only write tests" for p in files if not p.startswith("tests/")]
    if not tc["added"] and not tc["changed"]:
        out.append("the plan came with no tests")
    keys = {f"{number}.{k}" for k in range(1, len(plan["criteria"]) + 1)}
    proven = {k for ks in proving(tc).values() for k in ks}
    if declared is not None:
        names = sorted(declared_by_test(declared))
        out += [f"the plan names {t}, which is not in the repo" for t in missing_tests(names)]
        out += [f"tests are filed under {k}, which is not a criterion of this plan ({number}.1 to {number}.{len(keys)})"
                for k in sorted(declared) if k not in keys]
        proven |= {k for k, ts in declared.items() if ts}
    out += [f"criterion {k} has no test" for k in sorted(keys - proven)]
    out += [f"{t} proves {k}, which is not a criterion of this plan" for t, ks in tc["added"].items() for k in ks if k not in keys]
    out += [f"{t} now proves {k}, which is neither a criterion of this plan nor what it proved before"
            for t, (old, new) in tc["changed"].items() for k in new if k not in keys and k not in old]
    older = [t for t in tc["changed"] if not set(tc["changed"][t][0]) <= keys] + list(tc["deleted"])
    out += [f"{t} is an older test the planner changed or deleted, with no reason in test_changes"
            for t in older if t not in plan["test_changes"]]
    return out


def unreadable(paths):
    """Each test file that cannot be read as Python, with why."""
    out = []
    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                ast.parse(f.read(), path)
        except (SyntaxError, ValueError) as e:
            out.append(f"{path} cannot be read as Python ({type(e).__name__}: {e})")
    return out


def one_sentence(line):
    """True when the line is one sentence ending in '.', '?' or '!', with no other sentence end inside it."""
    return bool(line) and line[-1] in ".?!" and not re.search(r"[.?!]\s", line)


def unsummarized(added):
    """The new tests (path::name) whose docstring's first line is not one sentence on one line."""
    out = []
    for path in sorted({t.partition("::")[0] for t in added}):
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), path)
        for node in tree.body:
            t = f"{path}::{getattr(node, 'name', '')}"
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and t in added:
                doc = ast.get_docstring(node, clean=False) or ""
                if not one_sentence(doc.split("\n")[0].strip()):
                    out.append(f"{t} is a new test with no one-sentence summary: the first line of its docstring must "
                               f"be one sentence on one line, ending in '.', '?' or '!'")
    return out


def passing_today(added):
    """Run each new test (path::name) on today's code; the ones that pass or are skipped, or run past the limit."""
    out = []
    for t in sorted(added):
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", t],
                               capture_output=True, text=True, timeout=NEW_TEST_TIMEOUT)
        except subprocess.TimeoutExpired:
            out.append(f"{t} is a new test still running after {NEW_TEST_TIMEOUT} s on today's code; it was stopped")
            continue
        if r.returncode in (0, 5):  # 0: passed or skipped, 5: nothing ran
            out.append(f"{t} is a new test that passes today (or is skipped); every new test must fail on today's code")
    return out


def original(body):
    """The owner's own text: kept from an earlier plan's fold, else the body as it is."""
    body = body or ""
    if ORIGINAL_START in body and ORIGINAL_END in body:
        inner = body.split(ORIGINAL_START, 1)[1].split(ORIGINAL_END, 1)[0]
        lines = [l for l in inner.splitlines() if l.startswith(">")]
        return "\n".join(l[2:] if l.startswith("> ") else l[1:] for l in lines)
    return body.strip()


def render(number, body, plan, tags, older=()):
    """The issue body for a plan, in the format dokima.plan reads, with the owner's text folded below."""
    lines = [f"- [ ] Objective: {plan['objective'].strip()}"]
    for k, c in enumerate(plan["criteria"], 1):
        tests = sorted(t for t, ks in tags.items() if f"{number}.{k}" in ks)
        lines.append(f"  - [ ] Acceptance criteria: {c.strip()}")
        lines.append("    Verified by: " + (", ".join(f"`{t}`" for t in tests) or "no test"))
    lines.append("")
    if plan["non_goals"]:
        lines.append("**Out of scope:** " + "; ".join(x.strip() for x in plan["non_goals"]))
        lines.append("")
    if older:
        lines.append("**Changes to older tests:**")
        lines += [f"- `{t}`: {plan['test_changes'].get(t, 'no reason given')}" for t in older]
        lines.append("")
    lines.append("**Scope:**")
    lines += [f"- `{s.strip()}`" for s in plan["scope"]]
    text = original(body)
    lines += ["", "<details><summary>Original issue</summary>", "", ORIGINAL_START]
    lines += [f"> {l}" if l else ">" for l in text.splitlines()]
    lines += [ORIGINAL_END, "</details>"]
    return "\n".join(lines) + "\n"


def changed_files(base):
    """Every file the planner added or changed since `base`, committed or not, ignoring git-ignored files."""
    run = lambda *a: subprocess.run(["git", *a], check=True, capture_output=True, text=True).stdout.split("\n")
    return sorted({p for p in run("diff", "--name-only", base) + run("ls-files", "--others", "--exclude-standard") if p})


def gh(*args, **kw):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, **kw).stdout


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def read_at(base):
    return lambda path: (lambda r: r.stdout if r.returncode == 0 else "")(git("show", f"{base}:{path}"))


def read_now(path):
    return open(path).read() if os.path.exists(path) else ""


def main(argv):
    action, number, out = argv[1], argv[2], argv[3]
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if action == "rejected":
        path = os.path.join(out, "rejected.txt")
        why = open(path).read().strip() if os.path.exists(path) else "the planner run failed before handing anything back"
        run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
        gh("issue", "comment", number, "-R", repo, "--body", f"**Plan rejected:** {why}\n\n[See the run]({run})")
        return 0
    try:
        kind, result = read_output(out, number)
        if kind == "plan":
            base = os.environ.get("PLANNER_BASE", "HEAD")
            files = changed_files(base)
            paths = [p for p in files if p.startswith("tests/") and p.endswith(".py")]
            bad = unreadable(paths)
            if bad:
                raise Garbled("; ".join(bad))
            tc = test_changes(paths, read_at(base), read_now)
            if "declared" in result:
                tc = declared_labels(tc, result["declared"])
            # Only what the planner changed in this run counts against "tests only": on a re-plan the branch may
            # already hold the worker's code, which is not the planner's doing.
            run_base = os.environ.get("PLANNER_RUN_BASE")
            own = changed_files(run_base) if run_base else files
            bad = problems(number, result, own, tc, result.get("declared"))
            bad += problems_questions(result["raw"].get("questions", []))
            bad += unsummarized(tc["added"]) + passing_today(tc["added"])
            if bad:
                raise Garbled("; ".join(bad))
    except Garbled as e:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "rejected.txt"), "w").write(str(e))
        print(f"::error title=Planner output rejected::{e}")
        return 1
    if action == "post":
        if kind == "feature":
            gh("issue", "comment", number, "-R", repo, "--body", f"**Planner proposes a split**\n\n```json\n{result}\n```")
        else:
            older = sorted(t for t in tc["changed"] if not set(tc["changed"][t][0]) <= {f"{number}.{k}" for k in range(1, len(result["criteria"]) + 1)}) + sorted(tc["deleted"])
            body = gh("issue", "view", number, "-R", repo, "--json", "body", "-q", ".body")
            gh("issue", "edit", number, "-R", repo, "--body-file", "-", input=render(number, body, result, dict(proving(tc), **declared_by_test(result["declared"])), older))
            gh("issue", "comment", number, "-R", repo, "--body",
               f"Plan written above, tests on `work/issue-{number}`. Add `work` to approve it.")
    print(kind)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
