<!-- dokima-record -->
<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner's run ended with its hand-back rejected by code.

- the hand-back has no tests for 299.1
- the merge clashed on main

<details><summary><b>Non-functional requirements</b></summary>

- Nothing leaks. (safety; Fail closed)

</details>

<details><summary><b>Scope</b></summary>

- dokima/agent.py

</details>

<details><summary><b>Out of scope</b></summary>

- The board.

</details>

<details><summary><b>Tests</b></summary>

- 299.1: tests/test_a.py::test_one

</details>

<details><summary>Full record</summary>

```json
{
 "role": "planner",
 "stage": null,
 "run_id": "7",
 "run": "https://github.com/o/r/actions/runs/7",
 "log": "https://x/log",
 "models": [
  "claude-opus-5-5"
 ],
 "report": {
  "duration_ms": 120000,
  "turns": 9,
  "cost_usd": 1.5,
  "tokens_in": 1000,
  "tokens_out": 200
 },
 "handback": {
  "kind": "user_story",
  "summary": "Slow calls hand back a job id.",
  "user_story": "Owners get a job id.",
  "acceptance_criteria": [
   {
    "text": "A slow call returns a job id.",
    "source": "https://github.com/o/r/issues/299"
   }
  ],
  "non_functional": [
   {
    "text": "Nothing leaks.",
    "why": "safety",
    "principle": "Fail closed"
   }
  ],
  "scope": [
   "dokima/agent.py"
  ],
  "out_of_scope": [
   "The board."
  ],
  "tests": {
   "299.1": [
    "tests/test_a.py::test_one"
   ]
  },
  "test_changes": {},
  "links": {
   "blocked_by": [],
   "blocks": [],
   "relates_to": [
    12
   ]
  },
  "raises": [
   {
    "kind": "question",
    "to": "owner",
    "label": "Board column",
    "text": "Should a cancelled run keep its column?",
    "evidence": "dokima/board.py",
    "raised_by": "planner",
    "id": "P17"
   }
  ]
 },
 "check": {
  "passed": false,
  "problems": [
   "the hand-back has no tests for 299.1",
   "the merge clashed on main"
  ]
 }
}
```

</details>

<sub><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 2.0 min · 9 turns · 1,000 tokens in, 200 out · $1.50 at API prices · [conversation](https://x/log) · [run](https://github.com/o/r/actions/runs/7)</sub>
