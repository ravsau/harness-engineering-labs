# Lesson author contract

Keep this file synchronized with the lesson folders. Writers must specify real
file edits and the observable command output below. `starter/` must fail its
lesson check for lessons 03–10 and for the Lab 02 sanity edit; `solution/` must
pass. Checks must not read a learner completion boolean.

All commands run from the repository root. Use a fresh `work` directory for an
independent lesson or reuse it for a cumulative sequence.

| Lesson | Learner files | Concrete exercise | Passing command and stdout |
| --- | --- | --- | --- |
| 02 baseline | `taskboard.py`, `init.sh`, `features.json` | Add the feature-count sanity line to `init.sh`; keep a non-empty list of unique string `id`/`description` fields and boolean `passes`; run the actual add/list CLI | `python3 lab.py check 02 --workspace work` → `PASS 02-baseline: baseline CLI, init.sh, and feature ledger are runnable` |
| 03 map | `AGENTS.md`, `CLAUDE.md`, `docs/runbook.md`, `architecture.md`, `acceptance.md` | Replace TODOs with links, commands, architecture, and an evidence rule | `python3 lab.py check 03 --workspace work` → `PASS 03-map: repository map links resolve and state an evidence contract` |
| 04 guides | `.agents/skills/taskboard/SKILL.md`, `prompts/one-task.md` | Add inspect, one-task, verify, handoff, and stop instructions | `python3 lab.py check 04 --workspace work` → `PASS 04-guides: skill and one-task prompt define bounded work and evidence` |
| 05 sensors | `sensor.py`, `fixtures/{negative,valid,malformed}.json` | Reject a scripted completion event with no evidence or invalid evidence types; accept the valid event | `python3 lab.py check 05 --workspace work` → `PASS 05-sensors: negative completion claim is detected` |
| 06 verifier | `verify.py`, `fixtures/06-verifier/{good,stale,missing,failed,malformed}.json` | Gate one claim on successful fresh evidence, with strict command/exit/timestamp types and no explicit failed checks/errors; state that it is partial | `python3 lab.py check 06 --workspace work` → `PASS 06-verifier: fresh evidence passes while stale, missing, failed, and malformed evidence fail` |
| 07 boundaries | `router.py`, `fixtures/calls.json` | Route only typed `read_task`/`write_task`; reject malformed calls, unknown names, symlink/out-of-workspace paths, negative counts, and the fifth call at a four-call ceiling | `python3 lab.py check 07 --workspace work` → `PASS 07-boundaries: typed tool calls enforce names, paths, and attempt limits` |
| 08 handoff | `handoff.py`, `fixtures/seed.jsonl` | Append two JSONL handoffs; preserve the first line; return nonzero for stale or corrupt logs and reject append to a corrupt log | `python3 lab.py check 08 --workspace work` → `PASS 08-handoff: append-only handoff survives restart and gates stale evidence` |
| 09 shapes | `shapes.py`, `fixtures/tasks.json` | Demonstrate chain, independent fanout owners, read-only advisor, and bounded loop | `python3 lab.py check 09 --workspace work` → `PASS 09-shapes: chain, fanout, advisor, and bounded loop are inspectable` |
| 10 evals | `scorecard.py`, `taskboard.py`, `fixtures/10-evals/{good,bad,missing}.json` | Score fixed evidence fixtures; add and test real `taskboard.py list --open` filtering | `python3 lab.py check 10 --workspace work` → `PASS 10-evals: scorecard fixtures and real taskboard --open behavior pass` |

The root runner is the only lesson lifecycle interface:

```bash
python3 lab.py start NN --workspace work
python3 lab.py check NN --workspace work
python3 lab.py check-all --workspace work
python3 lab.py show NN --workspace work
```

`start` copies cumulative prior solutions only into a new empty workspace, then
copies the current starter only where a destination file is absent. It appends
one JSON record to `.lab-state.jsonl` and never overwrites learner files.
`check` and `show` snapshot every file's bytes, mode, and mtime before and after
the check subprocess; mutation fails the command. All child Python processes
run with `-B`.

Optional agent use means pasting `prompt.md` into an agent after granting access
to the lesson workspace. The repository contains no provider SDK, API key path,
network call, or paid inference code.
