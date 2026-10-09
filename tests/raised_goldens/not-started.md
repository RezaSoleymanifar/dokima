<!-- dokima-record -->
<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/worker.svg" width="16" height="16" align="absmiddle" alt="worker"> The worker stopped before any agent started.

- main is red: all tests failed on abc1234

<details><summary>Full record</summary>

```json
{
 "role": "not-started",
 "attempt": "worker",
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
 "handback": {},
 "check": {
  "passed": false,
  "problems": [
   "main is red: all tests failed on abc1234"
  ]
 }
}
```

</details>

<sub>No agent ran · [run](https://github.com/o/r/actions/runs/7)</sub>
