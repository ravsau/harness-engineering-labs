#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def record(path, task, evidence_at):
    path.write_text(json.dumps({"seq": 1, "task": task, "evidence_at": evidence_at}) + "\n", encoding="utf-8")


def show(path, now, max_age=30):
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    return "ready" if row.get("evidence_at", 0) >= now - max_age else "stale"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("record", "show"))
    parser.add_argument("path", type=Path)
    parser.add_argument("--task", default="add-task")
    parser.add_argument("--evidence-at", type=int, default=100)
    parser.add_argument("--now", type=int, default=100)
    args = parser.parse_args()
    if args.command == "record":
        record(args.path, args.task, args.evidence_at)
    else:
        print(show(args.path, args.now))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
