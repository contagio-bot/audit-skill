#!/usr/bin/env python3
import json
import sys


def bucket(finding: dict) -> str:
    sev = (finding.get("severity") or "").lower()
    if sev in {"critical", "high"}:
        return "immediate risk reduction"
    if sev in {"medium", "major"}:
        return "quick wins"
    return "deferred"


def main() -> int:
    data = json.load(sys.stdin)
    findings = data.get("findings", [])
    plan = {}
    for finding in findings:
        plan.setdefault(bucket(finding), []).append({
            "id": finding.get("id"),
            "title": finding.get("title"),
            "priority": finding.get("priority"),
            "affected_paths": finding.get("affected_paths", []),
        })
    json.dump(plan, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
