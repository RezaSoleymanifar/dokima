"""The planner's hand-back: check its shape, then write it into the issue.

    python3 -m dokima.planner check N OUT   # fail loudly unless OUT holds a well-formed plan or question
    python3 -m dokima.planner post N OUT    # write the plan into issue N, or post the question

The planner holds no GitHub key. It ends by writing exactly one of these to OUT:
  plan.json    {"objective": str, "criteria": [str, ...], "non_goals": [str, ...], "scope": [str, ...]}
               plus its tests in tests/; criterion k in the list is N.k
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
    if not isinstance(p, dict) or not isinstance(p.get("objective"), str) or not p["objective"].strip():
        raise Garbled("plan.json needs a non-empty objective")
    for key, required in (("criteria", True), ("scope", True), ("non_goals", False)):
        v = p.get(key, [] if not required else None)
        if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v) or (required and not v):
            raise Garbled(f"plan.json needs {key} as a {'non-empty ' if required else ''}list of non-empty strings")
    p.setdefault("non_goals", [])
    return "plan", p


def test_tags(paths, read=lambda p: open(p).read()):
    """Map each tested path::test to the criterion keys it proves."""
    found = {}
    for path in paths:
        current = None
        for line in read(path).splitlines():
            name = TEST_DEF.match(line)
            if name:
                current = f"{path}::{name.group(1)}"
            for key in PROVES.findall(line):
                found.setdefault(current or path, []).append(key)
    return found


def problems(number, plan, changed, tags):
    """What is wrong with a plan and the files it changed; empty when it can be posted."""
    out = [f"{p} is outside tests/; the planner may only write tests" for p in changed if not p.startswith("tests/")]
    if not any(p.startswith("tests/") for p in changed):
        out.append("the plan came with no tests")
    keys = {f"{number}.{k}" for k in range(1, len(plan["criteria"]) + 1)}
    proven = {k for ks in tags.values() for k in ks}
    out += [f"criterion {k} has no test" for k in sorted(keys - proven)]
    out += [f"{t} proves {k}, which is not a criterion of this plan" for t, ks in tags.items() for k in ks if k not in keys]
    return out


def original(body):
    """The owner's own text: kept from an earlier plan's fold, else the body as it is."""
    body = body or ""
    if ORIGINAL_START in body and ORIGINAL_END in body:
        inner = body.split(ORIGINAL_START, 1)[1].split(ORIGINAL_END, 1)[0]
        lines = [l for l in inner.splitlines() if l.startswith(">")]
        return "\n".join(l[2:] if l.startswith("> ") else l[1:] for l in lines)
    return body.strip()


def render(number, body, plan, tags):
    """The issue body for a plan, in the format dokima.plan reads, with the owner's text folded below."""
    lines = [f"- [ ] Objective: {plan['objective'].strip()}"]
    for k, c in enumerate(plan["criteria"], 1):
        tests = sorted(t for t, ks in tags.items() if f"{number}.{k}" in ks)
        lines.append(f"  - [ ] Acceptance criteria: {c.strip()}")
        lines.append("    Verified by: " + (", ".join(f"`{t}`" for t in tests) or "no test"))
    lines.append("")
    if plan["non_goals"]:
        lines.append("**Non-goals:** " + "; ".join(x.strip() for x in plan["non_goals"]))
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


def main(argv):
    action, number, out = argv[1], argv[2], argv[3]
    try:
        kind, result = read_output(out)
        if kind == "plan":
            changed = changed_files(os.environ.get("PLANNER_BASE", "HEAD"))
            tags = test_tags([p for p in changed if p.startswith("tests/") and p.endswith(".py")])
            bad = problems(number, result, changed, tags)
            if bad:
                raise Garbled("; ".join(bad))
    except Garbled as e:
        print(f"::error title=Planner output rejected::{e}")
        return 1
    if action == "post":
        repo = os.environ["GITHUB_REPOSITORY"]
        if kind == "question":
            gh("issue", "comment", number, "-R", repo, "--body", f"**Planner question**\n\n{result}")
        else:
            body = gh("issue", "view", number, "-R", repo, "--json", "body", "-q", ".body")
            gh("issue", "edit", number, "-R", repo, "--body-file", "-", input=render(number, body, result, tags))
            gh("issue", "comment", number, "-R", repo, "--body",
               f"Plan written above, tests on `work/issue-{number}`. Add `work` to approve it.")
    print(kind)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
