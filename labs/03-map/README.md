# 03 — Repository map

Make the repository legible before adding automation. Add a short map for an
agent, then link the runbook, architecture, and acceptance contract. The
`CLAUDE.md` file is a small bridge to the portable `AGENTS.md` rules.

Run `python3 lab.py check 03 --workspace work` from the repository root after
you have filled the starter files. The check resolves links and required headings;
it does not trust a completion flag.

After editing the five map files, run:

```bash
python3 lab.py check 03 --workspace work
```

Expected stdout:

```text
PASS 03-map: repository map links resolve and state an evidence contract
```
