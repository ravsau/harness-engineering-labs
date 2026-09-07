#!/usr/bin/env python3
"""Start, check, and show the dependency-free lesson workspaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABS = {
    "02": "02-baseline",
    "03": "03-map",
    "04": "04-guides",
    "05": "05-sensors",
    "06": "06-verifier",
    "07": "07-boundaries",
    "08": "08-handoff",
    "09": "09-shapes",
    "10": "10-evals",
}


def lesson_path(number: str) -> Path:
    try:
        return ROOT / "labs" / LABS[number]
    except KeyError as exc:
        raise SystemExit(f"lesson must be 02-10, got {number!r}") from exc


def copy_missing(source: Path, destination: Path) -> int:
    """Copy files only when absent; preserve every existing learner file."""
    copied = 0
    for source_path in sorted(source.rglob("*")):
        if source_path.is_dir():
            continue
        target = destination / source_path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        shutil.copy2(source_path, target)
        copied += 1
    return copied


def snapshot(workspace: Path) -> dict[str, tuple[str, int, int]]:
    """Capture every workspace file so read-only commands can prove it."""
    result = {}
    for path in sorted(p for p in workspace.rglob("*") if p.is_file()):
        info = path.stat()
        result[path.relative_to(workspace).as_posix()] = (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            stat.S_IMODE(info.st_mode),
            info.st_mtime_ns,
        )
    return result


def start(number: str, workspace: Path) -> int:
    lesson = lesson_path(number)
    workspace.mkdir(parents=True, exist_ok=True)
    # A fresh lesson gets the cumulative reference foundation. Existing work is
    # never replaced, so this is safe to rerun after a pause.
    if not any(workspace.iterdir()):
        for prior in sorted(LABS):
            if prior >= number:
                break
            copy_missing(lesson_path(prior) / "solution", workspace)
    copied = copy_missing(lesson / "starter", workspace)
    state_path = workspace / ".lab-state.jsonl"
    started = []
    if state_path.exists():
        started = [json.loads(line)["lesson"] for line in state_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if number not in started:
        with state_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"lesson": number}) + "\n")
    print(f"started {LABS[number]} in {workspace}")
    if copied == 0:
        print("no files added; existing work was preserved")
    return 0


def run_check(number: str, workspace: Path) -> int:
    workspace = workspace.resolve()
    lesson = lesson_path(number)
    check = lesson / "check.py"
    if not workspace.exists():
        print(f"FAIL {LABS[number]}: workspace does not exist: {workspace}")
        return 1
    before = snapshot(workspace)
    result = subprocess.run(
        [sys.executable, "-B", str(check), "--workspace", str(workspace)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    if output:
        print(output)
    if snapshot(workspace) != before:
        print(f"FAIL {LABS[number]}: check mutated the workspace")
        return 1
    return result.returncode


def check_all(workspace: Path) -> int:
    """Run every lesson check without changing the workspace."""
    if not workspace.exists():
        print(f"FAIL check-all: workspace does not exist: {workspace}")
        return 1
    result = 0
    for number in LABS:
        if run_check(number, workspace) != 0:
            result = 1
    return result


def show(number: str, workspace: Path) -> int:
    lesson = lesson_path(number)
    print(f"lesson={LABS[number]}")
    print(f"workspace={workspace}")
    print(f"started={'yes' if (workspace / '.lab-state.jsonl').exists() else 'no'}")
    files = sorted(p.relative_to(workspace).as_posix() for p in workspace.rglob("*") if p.is_file()) if workspace.exists() else []
    print("files=" + (",".join(files) if files else "none"))
    if workspace.exists():
        return run_check(number, workspace)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("start", "check", "check-all", "show"))
    parser.add_argument("lesson", choices=tuple(LABS), nargs="?")
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "check-all":
        if args.lesson is not None:
            parser.error("check-all does not take a lesson number")
        return check_all(args.workspace)
    if args.lesson is None:
        parser.error(f"{args.command} requires a lesson number")
    if args.command == "start":
        return start(args.lesson, args.workspace)
    if args.command == "check":
        return run_check(args.lesson, args.workspace)
    return show(args.lesson, args.workspace)


if __name__ == "__main__":
    raise SystemExit(main())
