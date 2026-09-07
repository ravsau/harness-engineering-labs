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
    script, fixtures = root / "scorecard.py", root / "fixtures" / "10-evals"
    if not script.is_file() or not all((fixtures / name).is_file() for name in ("good.json", "bad.json", "missing.json")):
        print("FAIL 10-evals: scorecard or fixed fixtures missing")
        return 1
    results = {}
    for name in ("good", "bad", "missing"):
        results[name] = subprocess.run(["python3", "-B", str(script), str(fixtures / f"{name}.json")], text=True, capture_output=True)
    good = json.loads(results["good"].stdout.splitlines()[0])
    bad = json.loads(results["bad"].stdout.splitlines()[0])
    missing = json.loads(results["missing"].stdout.splitlines()[0])
    if results["good"].returncode != 0 or good.get("status") != "pass" or results["bad"].returncode == 0 or bad.get("status") != "fail" or results["missing"].returncode == 0 or missing.get("status") != "fail":
        print("FAIL 10-evals: scorecard did not distinguish fixed fixtures")
        return 1
    if "improvement claim" not in results["good"].stdout:
        print("FAIL 10-evals: scorecard overclaims")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        task_file = Path(tmp) / "tasks.json"
        task_file.write_text(json.dumps([
            {"id": 1, "text": "open item", "done": False},
            {"id": 2, "text": "closed item", "done": True},
        ]) + "\n", encoding="utf-8")
        normal = subprocess.run(["python3", "-B", str(root / "taskboard.py"), "list", "--file", str(task_file)], text=True, capture_output=True)
        cli = subprocess.run(["python3", "-B", str(root / "taskboard.py"), "list", "--open", "--file", str(task_file)], text=True, capture_output=True)
    if normal.returncode != 0 or normal.stdout.strip() != "1: [ ] open item\n2: [x] closed item":
        print("FAIL 10-evals: real taskboard list acceptance failed")
        return 1
    if cli.returncode != 0 or cli.stdout.strip() != "1: [ ] open item":
        print("FAIL 10-evals: real taskboard --open acceptance failed")
        return 1
    print("PASS 10-evals: scorecard fixtures and real taskboard --open behavior pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
