#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def score(fixture):
    # Starter trusts the output string and ignores missing evidence.
    return {"status": "pass" if fixture.get("output") else "fail", "checks": 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    print(json.dumps(score(json.loads(args.fixture.read_text(encoding="utf-8"))), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
