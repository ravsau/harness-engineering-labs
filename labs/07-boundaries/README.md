# 07 — Boundaries

Build a typed toy router for two taskboard tools: `read_task` and `write_task`.
The router rejects unknown tool names, malformed arguments, paths outside the
workspace, and calls after a fixed attempt ceiling. This is a capability
boundary for structured tools, not a generic shell blocker.
The router only decides whether a typed call is admitted; it does not execute
the tool or claim production-grade isolation.

Run the structured calls against an explicit workspace:

```bash
python3 work/router.py work/fixtures/calls.json work
python3 lab.py check 07 --workspace work
```

The first four JSON lines contain these results:

```text
[true, "admitted read_task at tasks.json"]
[false, "unknown tool"]
[false, "path outside workspace"]
[false, "invalid typed arguments"]
```

The final check output is:

```text
PASS 07-boundaries: typed tool calls enforce names, paths, and attempt limits
```
