#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def issues(events):
    found = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            found.append(f"event {index}: event must be an object")
            continue
        evidence = event.get("evidence")
        if event.get("kind") == "completed" and not evidence:
            found.append(f"event {index}: completed claim has missing evidence")
        if evidence:
            if not isinstance(evidence, list):
                found.append(f"event {index}: evidence must be a list")
            else:
                for item in evidence:
                    if (not isinstance(item, dict)
                            or not isinstance(item.get("command"), str) or not item["command"].strip()
                            or not isinstance(item.get("exit_code"), int) or isinstance(item["exit_code"], bool)
                            or not isinstance(item.get("observed_at"), int) or isinstance(item["observed_at"], bool)):
                        found.append(f"event {index}: evidence has invalid command, exit_code, or observed_at")
                        break
        if event.get("claimed") and event.get("kind") not in {"completed", "failed"}:
            found.append(f"event {index}: claimed event has unknown kind")
    return found


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
