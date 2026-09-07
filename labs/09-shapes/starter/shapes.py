#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def run(shape, tasks, limit=3):
    return [{"shape": shape, "owner": "agent", "task": task["id"]} for task in tasks]


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
