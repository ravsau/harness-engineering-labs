#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


TOOLS = {
    "read_task": {"path"},
    "write_task": {"path", "text"},
}


def route(call, workspace, attempts, ceiling=4):
    if (not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 0
            or not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 0):
        return False, "invalid attempt count"
    if attempts >= ceiling:
        return False, "attempt ceiling exceeded"
    if not isinstance(call, dict):
        return False, "invalid call"
    name = call.get("name")
    args = call.get("args")
    if not isinstance(name, str):
        return False, "invalid typed arguments"
    if name not in TOOLS:
        return False, "unknown tool"
    if not isinstance(args, dict) or set(args) != TOOLS[name]:
        return False, "invalid typed arguments"
    if not isinstance(args.get("path"), str) or (name == "write_task" and not isinstance(args.get("text"), str)):
        return False, "invalid typed arguments"
    candidate = (workspace / args["path"]).resolve()
    try:
        candidate.relative_to(workspace.resolve())
    except ValueError:
        return False, "path outside workspace"
    return True, f"admitted {name} at {candidate.relative_to(workspace.resolve())}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--attempts", type=int, default=0)
    args = parser.parse_args()
    for offset, call in enumerate(json.loads(args.fixture.read_text(encoding="utf-8"))):
        print(json.dumps(route(call, args.workspace, args.attempts + offset)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
