#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def run(script, shape, fixture, limit=3):
    result = subprocess.run(["python3", "-B", str(script), shape, str(fixture), "--limit", str(limit)], text=True, capture_output=True)
    return result.returncode, json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    script, fixture = root / "shapes.py", root / "fixtures" / "tasks.json"
    if not script.is_file() or not fixture.is_file():
        print("FAIL 09-shapes: script or fixture missing")
        return 1
    chain_code, chain = run(script, "chain", fixture)
    fanout_code, fanout = run(script, "fanout", fixture)
    advisor_code, advisor = run(script, "advisor", fixture)
    loop_code, loop = run(script, "loop", fixture, 2)
    if any(code != 0 for code in (chain_code, fanout_code, advisor_code, loop_code)):
        print("FAIL 09-shapes: a child demonstration exited unsuccessfully")
        return 1
    if [row.get("owner") for row in chain] != ["planner", "builder", "evaluator"]:
        print("FAIL 09-shapes: chain ownership is unclear")
        return 1
    if len({row.get("owner") for row in fanout}) != 2 or any(row.get("owner") == "agent" for row in fanout):
        print("FAIL 09-shapes: fanout does not give work independent owners")
        return 1
    if advisor != [{"shape": "advisor", "owner": "advisor", "action": "review", "mutates": False}]:
        print("FAIL 09-shapes: advisor is not read-only")
        return 1
    if len([row for row in loop if "attempt" in row]) != 2 or not loop[-1].get("stopped"):
        print("FAIL 09-shapes: loop ignored its attempt ceiling")
        return 1
    print("PASS 09-shapes: chain, fanout, advisor, and bounded loop are inspectable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
