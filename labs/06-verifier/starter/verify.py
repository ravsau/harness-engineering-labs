#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def verify(claim, now, max_age=30):
    # Starter trusts the claim and demonstrates why a gate is needed.
    return claim.get("status") == "completed", "claim accepted"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--now", type=int, required=True)
    args = parser.parse_args()
    ok, message = verify(json.loads(args.fixture.read_text(encoding="utf-8")), args.now)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
