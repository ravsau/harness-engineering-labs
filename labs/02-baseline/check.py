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
    required = ("taskboard.py", "init.sh", "features.json")
    if any(not (root / name).is_file() for name in required):
        print("FAIL 02-baseline: missing baseline artifact")
        return 1
    init = subprocess.run(["sh", str(root / "init.sh")], cwd=root, text=True, capture_output=True)
    if init.returncode != 0 or init.stdout.strip() != "baseline ready; 2 features loaded":
        print("FAIL 02-baseline: init.sh lacks the feature-count sanity check")
        return 1
    features = json.loads((root / "features.json").read_text(encoding="utf-8"))
    if not isinstance(features, list) or not features:
        print("FAIL 02-baseline: feature ledger must be a non-empty list")
        return 1
    ids = []
    for item in features:
        if (not isinstance(item, dict) or set(item) != {"id", "description", "passes"}
                or not isinstance(item.get("id"), str) or not item["id"]
                or not isinstance(item.get("description"), str) or not item["description"]
                or not isinstance(item.get("passes"), bool)):
            print("FAIL 02-baseline: feature fields need string id/description and boolean passes")
            return 1
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        print("FAIL 02-baseline: feature IDs must be unique")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        task_file = Path(tmp) / "tasks.json"
        add = subprocess.run(["python3", "-B", str(root / "taskboard.py"), "add", "learn", "--file", str(task_file)], text=True, capture_output=True)
        listing = subprocess.run(["python3", "-B", str(root / "taskboard.py"), "list", "--file", str(task_file)], text=True, capture_output=True)
    if add.returncode or listing.returncode or "added 1: learn" not in add.stdout or "1: [ ] learn" not in listing.stdout:
        print("FAIL 02-baseline: CLI smoke test failed")
        return 1
    print("PASS 02-baseline: baseline CLI, init.sh, and feature ledger are runnable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
