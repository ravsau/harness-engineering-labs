# 06 — Verifier

A verifier gates one claim with fresh evidence. It does not prove the whole
system. Use the fixed clock supplied on the command line so the exercise is
deterministic: good evidence is recent and successful; stale, missing,
malformed, or explicitly failed accompanying checks fail.

Use the fixed clock to observe the gate directly:

```bash
python3 work/verify.py work/fixtures/06-verifier/good.json --now 100
python3 lab.py check 06 --workspace work
```

Expected stdout from the first command:

```text
accepted: recent successful result
```

Expected check output:

```text
PASS 06-verifier: fresh evidence passes while stale, missing, failed, and malformed evidence fail
```
