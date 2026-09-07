#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    router = root / "router.py"
    fixture = root / "fixtures" / "calls.json"
    if not router.is_file() or not fixture.is_file():
        print("FAIL 07-boundaries: router or fixture missing")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(["python3", "-B", str(router), str(fixture), tmp], text=True, capture_output=True)
        ceiling = subprocess.run(["python3", "-B", str(router), str(fixture), tmp, "--attempts", "4"], text=True, capture_output=True)
        ceiling_fixture = Path(tmp) / "ceiling.json"
        ceiling_fixture.write_text(json.dumps([{"name": "read_task", "args": {"path": "tasks.json"}}] * 5), encoding="utf-8")
        stepped = subprocess.run(["python3", "-B", str(router), str(ceiling_fixture), tmp], text=True, capture_output=True)
        sandbox = Path(tmp) / "sandbox"
        sandbox.mkdir()
        outside = Path(tmp) / "outside"
        outside.mkdir()
        link = sandbox / "link"
        link.symlink_to(outside, target_is_directory=True)
        symlink_fixture = sandbox / "symlink.json"
        symlink_fixture.write_text(json.dumps([{"name": "read_task", "args": {"path": "link/escape.txt"}}]), encoding="utf-8")
        symlink = subprocess.run(["python3", "-B", str(router), str(symlink_fixture), sandbox], text=True, capture_output=True)
        malformed_fixture = Path(tmp) / "malformed.json"
        malformed_fixture.write_text(json.dumps([None, {"name": [], "args": {"path": "tasks.json"}}]), encoding="utf-8")
        malformed = subprocess.run(["python3", "-B", str(router), str(malformed_fixture), tmp], text=True, capture_output=True)
        negative = subprocess.run(["python3", "-B", str(router), str(fixture), tmp, "--attempts", "-1"], text=True, capture_output=True)
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    if result.returncode or len(rows) != 4 or not rows[0][0] or rows[1][0] or "unknown" not in rows[1][1] or rows[2][0] or "outside" not in rows[2][1] or rows[3][0] or "typed" not in rows[3][1]:
        print("FAIL 07-boundaries: typed router did not reject the fixture cases")
        return 1
    stepped_rows = [json.loads(line) for line in stepped.stdout.splitlines()]
    if ("ceiling" not in ceiling.stdout or "outside" not in symlink.stdout
            or sum(row[0] for row in stepped_rows) != 4
            or "attempt ceiling exceeded" not in stepped.stdout
            or any("invalid" not in line for line in malformed.stdout.splitlines())
            or negative.returncode != 0 or "invalid attempt count" not in negative.stdout):
        print("FAIL 07-boundaries: attempt ceiling was not enforced")
        return 1
    print("PASS 07-boundaries: typed tool calls enforce names, paths, and attempt limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
