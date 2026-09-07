#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    sensor = root / "sensor.py"
    negative = root / "fixtures" / "negative.json"
    valid = root / "fixtures" / "valid.json"
    malformed = root / "fixtures" / "malformed.json"
    if not all(path.is_file() for path in (sensor, negative, valid, malformed)):
        print("FAIL 05-sensors: sensor or fixtures missing")
        return 1
    bad = subprocess.run(["python3", "-B", str(sensor), str(negative)], text=True, capture_output=True)
    good = subprocess.run(["python3", "-B", str(sensor), str(valid)], text=True, capture_output=True)
    malformed_result = subprocess.run(["python3", "-B", str(sensor), str(malformed)], text=True, capture_output=True)
    if (bad.returncode == 0 or "missing evidence" not in bad.stdout.lower()
            or good.returncode != 0 or malformed_result.returncode == 0
            or "invalid" not in malformed_result.stdout.lower()):
        print("FAIL 05-sensors: negative fixture was not rejected cleanly")
        return 1
    print("PASS 05-sensors: negative completion claim is detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
