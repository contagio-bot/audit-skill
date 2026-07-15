#!/usr/bin/env python3
"""Resolve an `audit` command name to the full loading plan it needs.

Keeps the command -> reference/methodology mapping, and the
standard-vs-formal loading decision, in one place (config/audits.json,
config/modes.json) instead of duplicated across SKILL.md prose.
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(REPO, "config", "audits.json")
MODES_PATH = os.path.join(REPO, "config", "modes.json")

CATEGORY_LABELS = [
    ("quality", "Quality"),
    ("risk", "Risk"),
    ("continuity", "Continuity"),
    ("remediation", "Remediation"),
    ("context", "Context"),
    ("profiles", "Profiles"),
]

# Compare fingerprints or compose other audits -> always the normalized/formal shape.
ALWAYS_FORMAL_COMMANDS = {"baseline", "diff", "verify", "recheck", "dd"}

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def is_formal(command: str, formal: bool = False, fmt: str = "markdown") -> bool:
    return bool(formal) or fmt != "markdown" or command in ALWAYS_FORMAL_COMMANDS


def resolve(command: str, formal: bool = False, fmt: str = "markdown") -> dict:
    manifest = load_json(MANIFEST_PATH)
    if command not in manifest:
        raise SystemExit(f"unknown audit command: {command}")
    entry = manifest[command]
    mode = "formal" if is_formal(command, formal, fmt) else "standard"

    # persistence-protocol.md governs the default (persist) behavior for
    # every report-producing command, not just an opt-in `--persist` run,
    # so it is always loaded.
    to_load = ["reference/bootstrap-lite.md", "reference/persistence-protocol.md"]
    if mode == "formal":
        to_load += [
            "reference/formal-delta.md",
            "reference/finding-contract.md",
            "reference/output-contract.md",
        ]
    if entry.get("reference"):
        to_load.append(entry["reference"])
    if entry.get("methodology"):
        to_load.append(entry["methodology"])

    return {
        "command": command,
        "category": entry["category"],
        "mode": mode,
        "load": to_load,
        "scripts": ["scripts/detect_capabilities.py", "scripts/inventory.py"],
        "validate": "formal-strict" if mode == "formal" else "standard",
    }


def menu() -> str:
    manifest = load_json(MANIFEST_PATH)
    by_category: dict[str, list[str]] = {}
    for command, entry in manifest.items():
        by_category.setdefault(entry["category"], []).append(command)
    lines = []
    for key, label in CATEGORY_LABELS:
        commands = by_category.get(key, [])
        if commands:
            lines.append(f"{label}: {', '.join(commands)}")
    return "\n".join(lines)


def main() -> int:
    raw = sys.argv[1:]
    if "--menu" in raw:
        sys.stdout.write(menu() + "\n")
        return 0

    # `--profile` is itself a command name, so it can't be parsed as a
    # generic argparse flag mixed in with the real modifier flags.
    command = "--profile" if "--profile" in raw else None
    rest = [a for a in raw if a != "--profile"]

    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--format", default="markdown")
    args = parser.parse_args(rest)

    command = command or args.command
    if not command:
        manifest = load_json(MANIFEST_PATH)
        json.dump(sorted(manifest.keys()), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    result = resolve(command, formal=args.formal, fmt=args.format)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
