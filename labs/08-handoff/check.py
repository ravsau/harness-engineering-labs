#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    script = root / "handoff.py"
    if not script.is_file():
        print("FAIL 08-handoff: handoff.py missing")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "handoff.jsonl"
        subprocess.run(["python3", "-B", str(script), "record", str(path), "--task", "first", "--evidence-at", "95"], check=True)
        first = path.read_text(encoding="utf-8")
        subprocess.run(["python3", "-B", str(script), "record", str(path), "--task", "second", "--evidence-at", "100"], check=True)
        lines = path.read_text(encoding="utf-8").splitlines()
        fresh = subprocess.run(["python3", "-B", str(script), "show", str(path), "--now", "100"], text=True, capture_output=True)
        stale = subprocess.run(["python3", "-B", str(script), "show", str(path), "--now", "200"], text=True, capture_output=True)
        corrupt = Path(tmp) / "corrupt.jsonl"
        corrupt.write_text('{"seq": 1, "task": "first", "evidence_at": 100}\nnot-json\n', encoding="utf-8")
        before = corrupt.read_bytes()
        rejected_append = subprocess.run(["python3", "-B", str(script), "record", str(corrupt), "--task", "second"], text=True, capture_output=True)
        rejected_show = subprocess.run(["python3", "-B", str(script), "show", str(corrupt), "--now", "100"], text=True, capture_output=True)
        after = corrupt.read_bytes()
    if (len(lines) != 2 or lines[0] + "\n" != first or fresh.returncode != 0
            or fresh.stdout.strip() != "ready" or stale.returncode == 0 or stale.stdout.strip() != "stale"
            or rejected_append.returncode == 0 or rejected_append.stdout.strip() != "invalid: malformed JSON on line 2"
            or after != before or rejected_show.returncode == 0):
        print("FAIL 08-handoff: records were overwritten or freshness is wrong")
        return 1
    print("PASS 08-handoff: append-only handoff survives restart and gates stale evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
