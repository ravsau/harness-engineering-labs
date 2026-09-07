# 09 — Shapes

Use one scripted fixture to compare four orchestration shapes: a sequential
chain, independent fanout, an advisor that cannot own the work, and a bounded
loop. Each event names its owner. The loop must stop at its explicit ceiling.

Run the scripted chain and bounded loop:

```bash
python3 work/shapes.py chain work/fixtures/tasks.json
python3 work/shapes.py loop work/fixtures/tasks.json --limit 2
python3 lab.py check 09 --workspace work
```

The chain contains owners `planner`, `builder`, and `evaluator`. The loop ends
with `{"shape": "loop", "owner": "loop", "stopped": true, "reason": "attempt ceiling"}`.
The final stdout is:

```text
PASS 09-shapes: chain, fanout, advisor, and bounded loop are inspectable
```
