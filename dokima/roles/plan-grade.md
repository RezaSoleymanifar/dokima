# Plan grade (shared by the planner and the reviewer of a plan)
The planner walks this list before it hands back a plan. The reviewer grades the plan against the same list, in the same
order: right criteria first, then right tests.

## The bar
Dokima ships exactly what the owner asked for, or nothing. The process is built so that wrong, partial or guessed work
is near impossible to merge: every gate must be passed on proof, never on trust. Tokens, time and extra rounds are cheap;
a wrong merge is not. Nothing is guessed: when the owner's intent is unclear, ask; when a proof is unclear, block.

## The one question: every test must break on any deviation
Ask it of every test: **would this fail if the behavior the owner asked for were not shipped exactly?**
Exactly means every way the work can deviate is caught by some test: the behavior missing, partial, wrong, too broad
(it also fires where it should not) or too narrow (it misses a case the owner named). A check that says no to everything
is wrong: every "rejects the bad case" test needs a "passes the good case" beside it.
A proof can prove something and still not prove the thing. A test that passes against a stub, checks a format, a word or
that a file exists, or proves a neighbour of the promise instead of the promise, proves nothing.

## The list
Blockers: a plan that fails any of 1 to 5 goes back to the planner.
1. Right criteria, exactly. Every behavior the owner asked for is an acceptance criterion, traced to the owner's own words
   (the issue or a specific comment). Nothing dropped, nothing added, nothing reinterpreted, and never a narrower
   thing that is easier to pass. Where the words allow two
   readings, or an ask cannot be tested, the plan raises a question for the owner; it never picks one silently and
   never drops an ask.
2. Every criterion is observable and precise: a value, a message, a file, an exit code, a state the owner can see. The
   scope lists every file the work needs.
3. Every criterion has a test, or is marked (manual) with a reason a reviewer accepts. If a criterion promises A, B and C,
   the tests prove A, B and C, not only A.
4. Every test passes the one question: any deviation from its criterion, in either direction, turns it red. Prefer tests
   that run the thing over tests that read code.
5. Today, every new test fails for the right reason: the feature is missing, not a crash, a missing tool or a bad path.
Never blockers:
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
