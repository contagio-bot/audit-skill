#!/usr/bin/env python3
import hashlib
import json
import os
import sys


VALID_CLASSIFICATIONS = {"Observed", "Inferred", "Not verifiable"}


def fingerprint(finding: dict) -> str:
    parts = [
        finding.get("audit_type", "unknown"),
        finding.get("category", "unknown"),
        ",".join(finding.get("affected_paths", [])),
        finding.get("title", ""),
    ]
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def main() -> int:
    data = json.load(sys.stdin)
    findings = data if isinstance(data, list) else data.get("findings", [])
    out = []
    for idx, item in enumerate(findings, start=1):
        item.setdefault("id", f"F-{idx:03d}")
        item.setdefault("classification", "Not verifiable")
        if item["classification"] not in VALID_CLASSIFICATIONS:
            raise SystemExit(f"invalid classification for {item['id']}")
        item.setdefault("affected_paths", [])
        item.setdefault("evidence", [])
        item.setdefault("fingerprint", fingerprint(item))
        if item.get("validate_paths"):
            for path in item["affected_paths"]:
                if not os.path.exists(path):
                    raise SystemExit(f"path does not exist: {path}")
        out.append(item)
    json.dump({"findings": out}, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
