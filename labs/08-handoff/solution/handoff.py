#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_rows(path):
    if not path.is_file():
        raise ValueError("missing handoff")
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"blank line {line_number}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"malformed JSON on line {line_number}") from exc
        if (not isinstance(row, dict) or row.get("seq") != line_number
                or not isinstance(row.get("task"), str) or not row["task"]
                or not isinstance(row.get("evidence_at"), int) or isinstance(row["evidence_at"], bool)):
            raise ValueError(f"invalid record on line {line_number}")
        rows.append(row)
    if not rows:
        raise ValueError("empty handoff")
    return rows


def record(path, task, evidence_at):
    rows = load_rows(path) if path.exists() else []
    seq = rows[-1]["seq"] + 1 if rows else 1
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"seq": seq, "task": task, "evidence_at": evidence_at}, sort_keys=True) + "\n")


def show(path, now, max_age=30):
    try:
        rows = load_rows(path)
    except ValueError as exc:
        return False, f"invalid: {exc}"
    row = rows[-1]
    if now - max_age <= row["evidence_at"] <= now:
        return True, "ready"
    return False, "stale"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("record", "show"))
    parser.add_argument("path", type=Path)
    parser.add_argument("--task", default="add-task")
    parser.add_argument("--evidence-at", type=int, default=100)
    parser.add_argument("--now", type=int, default=100)
    args = parser.parse_args()
    if args.command == "record":
        try:
            record(args.path, args.task, args.evidence_at)
        except ValueError as exc:
            print(f"invalid: {exc}")
            return 1
    else:
        ok, message = show(args.path, args.now)
        print(message)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
