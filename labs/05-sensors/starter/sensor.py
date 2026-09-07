#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def issues(events):
    # Starter deliberately misses the most important negative signal.
    return ["malformed event"] if any("kind" not in event for event in events) else []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    found = issues(json.loads(args.fixture.read_text(encoding="utf-8")))
    for issue in found:
        print(issue)
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
