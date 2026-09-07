#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def score(fixture):
    checks = {
        "has_output": bool(fixture.get("output")),
        "has_evidence": bool(fixture.get("evidence")),
        "no_errors": not fixture.get("errors"),
    }
    passed = sum(checks.values())
    return {"status": "pass" if passed == len(checks) else "fail", "passed": passed, "total": len(checks), "checks": checks}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    result = score(json.loads(args.fixture.read_text(encoding="utf-8")))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
