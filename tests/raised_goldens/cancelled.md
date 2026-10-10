<!-- dokima-record -->
<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/cancelled.svg" width="16" height="16" align="absmiddle" alt="cancelled"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review run was cancelled after its agent started, and nothing it handed back is used.

<details><summary><b><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Stats</b></summary>

Opus 5.5 · 2.0 min · 9 turns · 1K tokens in, 200 out · $1.50 at API prices · [conversation](https://x/log) · [run](https://github.com/o/r/actions/runs/7)

</details>

<details><summary>Full record</summary>

```json
{
 "role": "cancelled",
 "attempt": "reviewer",
 "stage": "pr",
 "agent_started": true,
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
 "handback": {},
 "check": {
  "passed": false,
  "problems": []
 }
}
```

</details>
