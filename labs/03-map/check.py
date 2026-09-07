#!/usr/bin/env python3
import argparse
import re
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    files = [root / "AGENTS.md", root / "CLAUDE.md", root / "architecture.md", root / "acceptance.md", root / "docs" / "runbook.md"]
    if any(not path.is_file() for path in files):
        print("FAIL 03-map: required map file is missing")
        return 1
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    bridge = (root / "CLAUDE.md").read_text(encoding="utf-8")
    runbook = (root / "docs" / "runbook.md").read_text(encoding="utf-8")
    architecture = (root / "architecture.md").read_text(encoding="utf-8")
    acceptance = (root / "acceptance.md").read_text(encoding="utf-8")
    if "TODO" in "\n".join([agents, bridge, runbook, architecture, acceptance]):
        print("FAIL 03-map: TODO remains in the repository map")
        return 1
    targets = set(re.findall(r'\[[^\]]+\]\(([^)]+)\)', agents))
    if not {"docs/runbook.md", "architecture.md", "acceptance.md"} <= targets:
        print("FAIL 03-map: AGENTS.md does not link the map")
        return 1
    if "@AGENTS.md" not in bridge or "python3" not in runbook or "features.json" not in architecture or "evidence" not in acceptance:
        print("FAIL 03-map: map lacks an executable contract")
        return 1
    init = subprocess.run(["sh", str(root / "init.sh")], cwd=root, text=True, capture_output=True)
    if init.returncode != 0 or init.stdout.strip() != "baseline ready; 2 features loaded":
        print("FAIL 03-map: runbook baseline command is not runnable")
        return 1
    print("PASS 03-map: repository map links resolve and state an evidence contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
