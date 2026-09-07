# 04 — Guides

Turn repeated behavior into two discoverable artifacts: a short skill for the
agent and a prompt for one bounded task. The skill states what to inspect, what
to change, how to verify, and when to stop. The prompt names the exact task and
the evidence to return.

Inspect the real files, then check them:

```bash
sed -n '1,12p' work/.agents/skills/taskboard/SKILL.md
python3 lab.py check 04 --workspace work
```

Expected final stdout:

```text
PASS 04-guides: skill and one-task prompt define bounded work and evidence
```
