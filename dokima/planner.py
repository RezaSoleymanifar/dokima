"""The planner's hand-back: check its shape, then write it into the issue.

    python3 -m dokima.planner check N OUT   # fail loudly unless OUT holds a well-formed plan or question
    python3 -m dokima.planner post N OUT    # write the plan into issue N, or post the question
    python3 -m dokima.planner rejected N OUT  # say on issue N why the run was rejected

The planner holds no GitHub key. It ends by writing exactly one of these to OUT:
  plan.json    {"objective": str, "criteria": [str, ...], "non_goals": [str, ...], "scope": [str, ...],
                "test_changes": {"path::test": "why", ...}}
               plus its tests in tests/; criterion k in the list is N.k. Every older test it changes
               or deletes needs a reason in test_changes.
  question.md  one question for the owner, ending in "?"
Nothing is posted unless `check` passes.
"""
import json
import os
import subprocess
import sys

from dokima.checks import PROVES, TEST_DEF

ORIGINAL_START = "<!-- dokima-original -->"
ORIGINAL_END = "<!-- /dokima-original -->"


class Garbled(Exception):
    pass


def read_output(out):
    """('plan', dict) or ('question', str); Garbled if OUT holds anything else."""
    has_plan = os.path.exists(os.path.join(out, "plan.json"))
    has_q = os.path.exists(os.path.join(out, "question.md"))
    if has_plan == has_q:
        raise Garbled("the planner must hand back exactly one of plan.json or question.md, found "
                      + ("both" if has_plan else "neither"))
    if has_q:
        q = open(os.path.join(out, "question.md")).read().strip()
        if not q.endswith("?"):
            raise Garbled("question.md must hold one question ending in '?'")
        return "question", q
    try:
        p = json.load(open(os.path.join(out, "plan.json")))
    except ValueError as e:
        raise Garbled(f"plan.json is not valid JSON: {e}")
    if isinstance(p, dict) and "kind" in p:
        return from_kind(p)
    if not isinstance(p, dict) or not isinstance(p.get("objective"), str) or not p["objective"].strip():
        raise Garbled("plan.json needs a non-empty objective")
    for key, required in (("criteria", True), ("scope", True), ("non_goals", False)):
        v = p.get(key, [] if not required else None)
        if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v) or (required and not v):
            raise Garbled(f"plan.json needs {key} as a {'non-empty ' if required else ''}list of non-empty strings")
    p.setdefault("non_goals", [])
    tc = p.setdefault("test_changes", {})
    if not isinstance(tc, dict) or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in tc.items()):
        raise Garbled("plan.json test_changes must map each changed older test to a non-empty reason")
    return "plan", p


def strings(v):
    return isinstance(v, list) and all(isinstance(x, str) and x.strip() for x in v)


def from_kind(p):
    """Read a plan.json written in the agreed shape (user_story, feature or question) into what the rest of the code uses.

    A story becomes a plan: its acceptance criteria come first, then its non-functional requirements, numbered N.1,
    N.2 ... in that order. A feature or a question is shown to the owner as handed back, as a comment.
    """
    kind = p["kind"]
    if kind == "question":
        q = p.get("question")
        if not isinstance(q, str) or not q.strip().endswith("?"):
            raise Garbled("a question needs one question ending in '?'")
        opts = p.get("options") or []
        text = q.strip() + "".join(f"\n- {o}" for o in opts if isinstance(o, str))
        if isinstance(p.get("recommendation"), str) and p["recommendation"].strip():
            text += f"\n\nRecommended: {p['recommendation'].strip()}"
        return "question", text
    if kind == "feature":
        stories = p.get("stories")
        if not isinstance(stories, list) or not 2 <= len(stories) <= 5:
            raise Garbled("a feature needs 2 to 5 stories")
        return "feature", json.dumps(p, indent=2)
    if kind != "user_story":
        raise Garbled(f"plan.json kind must be user_story, feature or question, not {kind!r}")
    if not isinstance(p.get("user_story"), str) or not p["user_story"].strip():
        raise Garbled("a story needs a non-empty user_story")
    ac, nfr = p.get("acceptance_criteria"), p.get("non_functional", [])
    if not isinstance(ac, list) or not ac:
        raise Garbled("a story needs a non-empty list of acceptance_criteria")
    for c in ac:
        if not isinstance(c, dict) or not str(c.get("text", "")).strip():
            raise Garbled("every acceptance criterion needs its text")
        if not str(c.get("source", "")).strip():
            raise Garbled(f"acceptance criterion '{c['text'][:60]}' has no source link")
    if not isinstance(nfr, list) or not all(isinstance(c, dict) and str(c.get("text", "")).strip() and str(c.get("why", "")).strip() for c in nfr):
        raise Garbled("every non-functional requirement needs its text and why")
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


def declared_labels(tc, declared):
    """Use the criteria the plan declares for each test, never labels guessed from the test's text."""
    by_test = {}
    for key, names in declared.items():
        for t in names:
            by_test.setdefault(t, []).append(key)
    added = {t: by_test.get(t, []) for t in tc["added"]}
    changed = {t: (old, by_test.get(t, old)) for t, (old, _) in tc["changed"].items()}
    return {"added": added, "changed": changed, "deleted": tc["deleted"]}


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
    """Tests the planner touched, by path::name: added, changed (with their old keys) and deleted."""
    added, changed, deleted = {}, {}, {}
    for path in paths:
        old, new = test_functions(before(path)), test_functions(after(path))
        for name, (src, keys) in new.items():
            if name not in old:
                added[f"{path}::{name}"] = keys
            elif old[name][0] != src:
                changed[f"{path}::{name}"] = (old[name][1], keys)
        for name, (_, keys) in old.items():
            if name not in new:
                deleted[f"{path}::{name}"] = keys
    return {"added": added, "changed": changed, "deleted": deleted}


def proving(tc):
    """Each added or changed test with the keys it proves now."""
    return dict(tc["added"], **{t: new for t, (_, new) in tc["changed"].items()})


def problems(number, plan, files, tc):
    """What is wrong with a plan and the tests it touched; empty when it can be posted."""
    out = [f"{p} is outside tests/; the planner may only write tests" for p in files if not p.startswith("tests/")]
    if not tc["added"] and not tc["changed"]:
        out.append("the plan came with no tests")
    keys = {f"{number}.{k}" for k in range(1, len(plan["criteria"]) + 1)}
    proven = {k for ks in proving(tc).values() for k in ks}
    out += [f"criterion {k} has no test" for k in sorted(keys - proven)]
    out += [f"{t} proves {k}, which is not a criterion of this plan" for t, ks in tc["added"].items() for k in ks if k not in keys]
    out += [f"{t} now proves {k}, which is neither a criterion of this plan nor what it proved before"
            for t, (old, new) in tc["changed"].items() for k in new if k not in keys and k not in old]
    older = [t for t in tc["changed"] if not set(tc["changed"][t][0]) <= keys] + list(tc["deleted"])
    out += [f"{t} is an older test the planner changed or deleted, with no reason in test_changes"
            for t in older if t not in plan["test_changes"]]
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
        kind, result = read_output(out)
        if kind == "plan":
            base = os.environ.get("PLANNER_BASE", "HEAD")
            files = changed_files(base)
            tc = test_changes([p for p in files if p.startswith("tests/") and p.endswith(".py")], read_at(base), read_now)
            if "declared" in result:
                tc = declared_labels(tc, result["declared"])
            bad = problems(number, result, files, tc)
            if bad:
                raise Garbled("; ".join(bad))
    except Garbled as e:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "rejected.txt"), "w").write(str(e))
        print(f"::error title=Planner output rejected::{e}")
        return 1
    if action == "post":
        if kind == "question":
            gh("issue", "comment", number, "-R", repo, "--body", f"**Planner question**\n\n{result}")
        elif kind == "feature":
            gh("issue", "comment", number, "-R", repo, "--body", f"**Planner proposes a split**\n\n```json\n{result}\n```")
        else:
            older = sorted(t for t in tc["changed"] if not set(tc["changed"][t][0]) <= {f"{number}.{k}" for k in range(1, len(result["criteria"]) + 1)}) + sorted(tc["deleted"])
            body = gh("issue", "view", number, "-R", repo, "--json", "body", "-q", ".body")
            gh("issue", "edit", number, "-R", repo, "--body-file", "-", input=render(number, body, result, proving(tc), older))
            gh("issue", "comment", number, "-R", repo, "--body",
               f"Plan written above, tests on `work/issue-{number}`. Add `work` to approve it.")
    print(kind)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
