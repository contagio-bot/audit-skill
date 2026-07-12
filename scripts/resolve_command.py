#!/usr/bin/env python3
"""Resolve an `audit` command name to the bundled files it should load.

Keeps the command -> reference/methodology mapping in one place
(config/audits.json) instead of duplicated across SKILL.md prose.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(REPO, "config", "audits.json")

ALWAYS_LOAD = [
    "reference/bootstrap.md",
    "reference/persistence-protocol.md",
]

REPORT_COMMANDS_LOAD_FINDING_CONTRACT = {
    "deadcode", "arch", "perf", "security", "pentest", "deps",
    "supply-chain", "ci", "testing", "data", "api", "cloud",
    "operability", "privacy", "ai", "licensing", "dd",
}


def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def resolve(command: str) -> dict:
    manifest = load_manifest()
    if command not in manifest:
        raise SystemExit(f"unknown audit command: {command}")
    entry = manifest[command]
    to_load = list(ALWAYS_LOAD)
    if command in REPORT_COMMANDS_LOAD_FINDING_CONTRACT:
        to_load.append("reference/finding-contract.md")
        to_load.append("reference/output-contract.md")
    to_load.append(entry["reference"])
    if entry.get("methodology"):
        to_load.append(entry["methodology"])
    return {
        "command": command,
        "category": entry["category"],
        "load": to_load,
    }


def main() -> int:
    if len(sys.argv) < 2:
        manifest = load_manifest()
        json.dump(sorted(manifest.keys()), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    result = resolve(sys.argv[1])
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
