#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    root = parser.parse_args().workspace
    skill = root / ".agents" / "skills" / "taskboard" / "SKILL.md"
    prompt = root / "prompts" / "one-task.md"
    if not skill.is_file() or not prompt.is_file():
        print("FAIL 04-guides: skill or prompt is missing")
        return 1
    skill_text = skill.read_text(encoding="utf-8")
    prompt_text = prompt.read_text(encoding="utf-8")
    text = skill_text + prompt_text
    parts = skill_text.split("---", 2)
    if len(parts) != 3:
        print("FAIL 04-guides: skill needs YAML frontmatter")
        return 1
    metadata = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    if metadata.get("name") != "taskboard-work" or not metadata.get("description"):
        print("FAIL 04-guides: skill frontmatter is incomplete")
        return 1
    if "TODO" in text:
        print("FAIL 04-guides: guide is unfinished")
        return 1
    required = ("inspect", "exactly one", "run", "observed output", "evidence", "handoff", "stop",
                "python3 taskboard.py list --file tasks.json", "python3 ../lab.py check 04 --workspace .")
    if not all(item.lower() in text.lower() for item in required):
        print("FAIL 04-guides: guide lacks a bounded workflow")
        return 1
    print("PASS 04-guides: skill and one-task prompt define bounded work and evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
