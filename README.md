# Harness Engineering Labs

This repository is a small, offline course companion. You improve one local
Python CLI, `taskboard`, and add checks around it.

The runtime uses only Python 3.11+ standard-library modules. It never imports a
model SDK, sends a network request, or needs an API key. You may paste the lab
prompts into a coding agent, but the prompts are optional and the checks run
locally.

## Quickstart

```bash
git clone https://github.com/ravsau/harness-engineering-labs
cd harness-engineering-labs
python3 --version
python3 lab.py start 02 --workspace work
python3 lab.py check 02 --workspace work
python3 lab.py show 02 --workspace work
```

The starter check fails until you add the feature-count sanity line described in
`labs/02-baseline/README.md`. After that real edit, the complete baseline shows:

```text
started 02-baseline in work
PASS 02-baseline: baseline CLI, init.sh, and feature ledger are runnable
lesson=02-baseline
workspace=work
started=yes
files=.lab-state.jsonl,features.json,init.sh,taskboard.py
PASS 02-baseline: baseline CLI, init.sh, and feature ledger are runnable
```

The workspace is intentionally explicit. `start` adds missing files and never
overwrites a learner's work. `check` and `show` are read-only. To begin a lesson
independently, run `start NN` in a new workspace; the runner adds the baseline
and earlier finished lesson artifacts before adding that lesson's starter. To
continue a course sequence, use the same workspace and call `start 02`, then
`start 03`, through `start 10`.

Each lesson has `README.md`, `prompt.md`, `starter/`, and `solution/`. Each starter has a bug or an unfinished file. Try the repair, then compare it
with the solution. The checks inspect the code, output, and required files.

## Commands

```bash
python3 lab.py start NN --workspace PATH
python3 lab.py check NN --workspace PATH
python3 lab.py check-all --workspace PATH
python3 lab.py show NN --workspace PATH
python3 -m unittest discover -s tests -v
```

The lesson number is one of `02` through `10`. Every stateful command requires
`--workspace`; there is no hidden current-directory state.

## Lesson map

| Lesson | Focus | What the check covers |
| --- | --- | --- |
| 02 baseline | runnable CLI, `init.sh`, `features.json` | CLI smoke test and ledger schema |
| 03 map | `AGENTS.md`, runbook, architecture, acceptance, `CLAUDE.md` bridge | required map links resolve |
| 04 guides | a skill and a focused prompt | required workflow and stop conditions |
| 05 sensors | negative fixture and sensor | bad signals are rejected |
| 06 verifier | fresh evidence gates | old, missing, malformed, or explicitly failed results are rejected |
| 07 boundaries | typed toy tool router | unknown and out-of-workspace calls reject; attempts cap |
| 08 handoff | durable files and fresh evidence | restart reconstructs state without overwrite |
| 09 shapes | chain, fanout, advisor, bounded loop | scripted events show owners and retry limits |
| 10 evals | fixed good, bad, missing scorecard | saved-record checks and real `list --open` behavior |

Use these labs on their own, or follow the [CloudYeti course](https://learn.cloudyeti.io/courses/harness-engineering)
for the walkthroughs, diagrams, troubleshooting questions, and exercises for
your own repository. All starter files, prompts, checks, and finished examples
are included here.

For contributors, [`AUTHOR-CONTRACT.md`](AUTHOR-CONTRACT.md) lists the files and
expected command output used by the lessons.
