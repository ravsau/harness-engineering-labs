# 02 — Baseline

Start with a tiny runnable surface. Inspect `taskboard.py`, `features.json`, and
`init.sh`. Run the smoke check before changing anything. This lesson is the
shared starting point for all later lessons.

```bash
cd work
sh init.sh
python3 taskboard.py add "ship the first task"
python3 taskboard.py list
cd ..
```

Before the edit, `python3 lab.py check 02 --workspace work` prints:

```text
FAIL 02-baseline: init.sh lacks the feature-count sanity check
```

After adding the count to `init.sh`, the expected complete output is:

```text
PASS 02-baseline: baseline CLI, init.sh, and feature ledger are runnable
```

The starter's `init.sh` omits the feature-count sanity line. Add that check,
then the lesson passes. The check executes the CLI and validates string and
boolean feature fields with unique IDs; it does not trust a completion flag.
