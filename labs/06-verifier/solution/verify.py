#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def verify(claim, now, max_age=30):
    if claim.get("status") != "completed" or claim.get("checks_failed") or claim.get("errors"):
        return False, "rejected: no acceptable recent result"
    evidence_items = claim.get("evidence", [])
    if not isinstance(evidence_items, list):
        return False, "rejected: no acceptable recent result"
    for evidence in evidence_items:
        if not isinstance(evidence, dict):
            continue
        observed = evidence.get("observed_at")
        exit_code = evidence.get("exit_code")
        command = evidence.get("command")
        if (isinstance(observed, int) and not isinstance(observed, bool)
                and isinstance(exit_code, int) and not isinstance(exit_code, bool)
                and isinstance(command, str) and command.strip()
                and now - max_age <= observed <= now and exit_code == 0):
            return True, "accepted: recent successful result"
    return False, "rejected: no acceptable recent result"


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
