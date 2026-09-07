#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    verifier = root / "verify.py"
    fixtures = root / "fixtures" / "06-verifier"
    names = ("good", "stale", "missing", "failed", "malformed")
    if not verifier.is_file() or not all((fixtures / f"{name}.json").is_file() for name in names):
        print("FAIL 06-verifier: verifier or fixed fixtures missing")
        return 1
    results = {}
    for name in names:
        results[name] = subprocess.run(["python3", "-B", str(verifier), str(fixtures / f"{name}.json"), "--now", "100"], text=True, capture_output=True)
    if (results["good"].returncode != 0 or results["stale"].returncode == 0
            or results["missing"].returncode == 0 or results["failed"].returncode == 0
            or results["malformed"].returncode == 0):
        print("FAIL 06-verifier: freshness gates do not distinguish fixtures")
        return 1
    print("PASS 06-verifier: fresh evidence passes while stale, missing, failed, and malformed evidence fail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
