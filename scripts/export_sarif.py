#!/usr/bin/env python3
import json
import sys


def main() -> int:
    data = json.load(sys.stdin)
    findings = data.get("findings", [])
    results = []
    for finding in findings:
        paths = finding.get("affected_paths") or []
        if not paths:
            continue
        results.append({
            "ruleId": finding.get("id", "AUDIT"),
            "level": "warning",
            "message": {"text": finding.get("summary", finding.get("title", ""))},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": paths[0]}
                }
            }],
        })
    sarif = {
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "audit-skill"}}, "results": results}],
    }
    json.dump(sarif, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
