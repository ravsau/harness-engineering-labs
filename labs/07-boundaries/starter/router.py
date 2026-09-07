#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def route(call, workspace, attempts, ceiling=3):
    # Starter intentionally trusts the name and path.
    if attempts > ceiling:
        return False, "attempt ceiling exceeded"
    return True, f"accepted {call.get('name')}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--attempts", type=int, default=0)
    args = parser.parse_args()
    for call in json.loads(args.fixture.read_text(encoding="utf-8")):
        print(json.dumps(route(call, args.workspace, args.attempts)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
