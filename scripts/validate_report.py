#!/usr/bin/env python3
import json
import sys


def main() -> int:
    data = json.load(sys.stdin)
    findings = data.get("findings", [])
    errors = []
    for finding in findings:
        if not finding.get("evidence"):
            errors.append(f"{finding.get('id', 'unknown')}: missing evidence")
        if not finding.get("classification"):
            errors.append(f"{finding.get('id', 'unknown')}: missing classification")
    if errors:
        json.dump({"valid": False, "errors": errors}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1
    json.dump({"valid": True, "errors": []}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
