#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("add", "list"))
    parser.add_argument("text", nargs="?")
    parser.add_argument("--open", action="store_true", help="list only unfinished tasks")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    args = parser.parse_args()
    tasks = json.loads(args.file.read_text(encoding="utf-8")) if args.file.exists() else []
    if args.command == "add":
        if not args.text:
            parser.error("add requires text")
        tasks.append({"id": len(tasks) + 1, "text": args.text, "done": False})
        args.file.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
        print(f"added {tasks[-1]['id']}: {args.text}")
    else:
        for task in tasks:
            if not args.open or not task["done"]:
                print(f"{task['id']}: [{'x' if task['done'] else ' '}] {task['text']}")


if __name__ == "__main__":
    main()
