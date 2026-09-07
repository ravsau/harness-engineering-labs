#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def run(shape, tasks, limit=3):
    if shape == "chain":
        return [{"shape": "chain", "owner": owner, "task": tasks[0]["id"]} for owner in ("planner", "builder", "evaluator")]
    if shape == "fanout":
        return [{"shape": "fanout", "owner": f"worker-{task['id']}", "task": task["id"]} for task in tasks]
    if shape == "advisor":
        return [{"shape": "advisor", "owner": "advisor", "action": "review", "mutates": False}]
    events = [{"shape": "loop", "owner": "loop", "attempt": attempt} for attempt in range(max(0, limit))]
    events.append({"shape": "loop", "owner": "loop", "stopped": True, "reason": "attempt ceiling"})
    return events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("shape", choices=("chain", "fanout", "advisor", "loop"))
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(run(args.shape, json.loads(args.fixture.read_text(encoding="utf-8")), args.limit)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
