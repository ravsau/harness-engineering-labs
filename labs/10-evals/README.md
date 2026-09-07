# 10 — Evals

Finish with a small scorecard over fixed fixtures, then make one real change to
the taskboard CLI. The scorecard measures observable checks on good, bad, and
missing scripted control evidence. The capstone adds `list --open`, exercises
the actual CLI with a subprocess, and does not call a model or claim that a
model improved.

Score the fixed good fixture, then run the complete check:

```bash
python3 work/scorecard.py work/fixtures/10-evals/good.json
python3 lab.py check 10 --workspace work
```

Expected stdout from the first command:

```text
{"checks": {"has_evidence": true, "has_output": true, "no_errors": true}, "passed": 3, "status": "pass", "total": 3}
deterministic fixture score; no model improvement claim
```

The check also runs the fixed bad and missing fixtures and prints:

```text
PASS 10-evals: scorecard fixtures and real taskboard --open behavior pass
```
