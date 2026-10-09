<!-- dokima-record -->
<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue and asks you 1 question.

**User story:** Owners get a job id.

<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**

1. A slow call returns a job id.

<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #12

<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
- Should it retry? Assumed: It does not.

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

<details><summary><b>Concerns</b></summary>

- This overlaps #12. (dokima/board.py)

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
  "questions": [
   {
    "question": "Should it retry?",
    "assumption": "It does not."
   }
  ],
  "concerns": [
   {
    "text": "This overlaps #12.",
    "evidence": "dokima/board.py"
   }
  ]
 },
 "check": {
  "passed": true,
  "problems": []
 }
}
```

</details>

<sub><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 2.0 min · 9 turns · 1,000 tokens in, 200 out · $1.50 at API prices · [conversation](https://x/log) · [run](https://github.com/o/r/actions/runs/7)</sub>
