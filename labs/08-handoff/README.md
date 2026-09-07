# 08 — Handoff

Make progress durable across process boundaries. A handoff is an append-only
JSONL record with a sequence number, task, and evidence timestamp. A fresh
process can read it and decide whether the next step is ready. Recording a new
handoff must preserve every earlier line.

Record twice, then read from a fresh process:

```bash
python3 work/handoff.py record work/handoff.jsonl --task first --evidence-at 95
python3 work/handoff.py record work/handoff.jsonl --task second --evidence-at 100
wc -l work/handoff.jsonl
python3 work/handoff.py show work/handoff.jsonl --now 100
```

Expected stdout includes `2` from `wc -l` and then:

```text
ready
```

Stale `show` output exits nonzero. A malformed existing log also exits nonzero,
and a new record is not appended to it. The lesson check prints:

```text
PASS 08-handoff: append-only handoff survives restart and gates stale evidence
```
