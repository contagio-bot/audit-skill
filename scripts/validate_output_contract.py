#!/usr/bin/env python3
import argparse
import json
import os
import sys


COMMON_MARKDOWN_HEADINGS = [
    "Executive summary",
    "Scope and coverage",
    "Capability manifest",
    "Method and evidence",
    "Detailed findings",
    "Normalized findings",
    "Remediation",
    "Persistence disclosure",
]


def validate_markdown(text: str):
    errors = []
    for heading in COMMON_MARKDOWN_HEADINGS:
        if f"## {heading}" not in text and f"### {heading}" not in text:
            errors.append(f"missing heading: {heading}")
    return errors


def validate_json(data: dict):
    errors = []
    for key in ("coverage", "persistence_mode", "findings"):
        if key not in data:
            errors.append(f"missing key: {key}")
    findings = data.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
    return errors


def load_text(path: str):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    path = args.path
    if not os.path.exists(path):
        raise SystemExit(f"missing report: {path}")
    errors = []
    if path.endswith(".json"):
        errors = validate_json(json.loads(load_text(path)))
    else:
        errors = validate_markdown(load_text(path))
    if errors:
        json.dump({"valid": False, "errors": errors}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1
    json.dump({"valid": True, "errors": []}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
