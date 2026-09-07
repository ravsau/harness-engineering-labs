---
name: taskboard-work
description: Complete one taskboard task with evidence and a handoff.
---

# Taskboard work

1. Inspect the current task list and read the acceptance rule.
2. Select exactly one incomplete task; do not widen the request.
3. Implement the smallest change that satisfies that task.
4. Run `python3 taskboard.py list --file tasks.json` and record its observed output.
5. Append a handoff with the task ID, evidence command, and next step.
6. Stop after one task or when the check fails; never mark work complete by
   changing a status field alone.

From the repository root, run `python3 lab.py check 04 --workspace work`.
