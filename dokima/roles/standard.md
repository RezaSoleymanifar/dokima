# The standard (shared by planner and reviewer)
The planner walks this list before it hands back a plan. The reviewer grades the plan against the same list, in the same
order. Right criteria first, then right tests.

## The one question: every test must break if the behavior does not exist
Ask it of every test: **would this fail if the behavior the owner asked for were not shipped?**
A proof can prove something and still not prove the thing. A test that passes against a stub, checks a format, a word or
that a file exists, or proves a neighbour of the promise instead of the promise, proves nothing.
Two sides, both required. A test breaks when the behavior is missing, and it breaks when the behavior is wrong. A check
that says no to everything is wrong: every "rejects the bad case" test needs a "passes the good case" next to it, or a
checker that rejects everything would turn it green.

## The list
Blockers: a plan that fails any of 1 to 5 goes back to the planner.
1. Right criteria. Every behavior the owner asked for is an acceptance criterion, traced to the owner's own words (the
   issue or a specific comment). Nothing the owner asked for is dropped; nothing they did not ask for is added. If the
   owner promised A, B and C, the criteria say A, B and C.
2. Every criterion is observable, and the scope lists every file the work needs.
3. Every criterion has a test, or is marked (manual) with a reason a reviewer accepts. If a criterion promises A, B and C,
   the tests prove A, B and C, not only A.
4. Every test passes the one question: it breaks if the behavior is missing, and it breaks if the behavior is wrong.
   Prefer tests that run the thing over tests that read code.
5. Today, every new test fails for the right reason: the feature is missing, not a crash, a missing tool or a bad path.
Notes, never blockers:
6. Every failure the criterion implies is tested: bad input, empty result, two at once. Two cases when it says "every".
7. A promise like "never collides" or "same output" gets its own test that repeats or breaks something.
8. Each failing test says which criterion failed and why, in plain words.
9. The size is right: more than five criteria, more than one independent goal, or unrelated parts of the code means a
   split. A split names its rule and gives every promise of the issue to exactly one child.

## Examples
Bad: a test changed into a folder that only existed on the author's machine. It failed on every run however good the
work was, and the worker burned its budget against it.
Good: the fixed test runs from the repo root and fails with "1.2: slow call did not return a job id within 20 s".
Bad: the plan promised seven outcomes and the tests proved one of each kind. Code doing only the tested path would pass.
Good: one test per promised outcome, the outside service faked on a local port.
Bad: a temp git repo with no user identity, so every test failed on git, not on the feature.
Good: one test that runs the real tool from outside and names its criterion on each failure.
