#!/usr/bin/env python3
import hashlib
import json
import os
import sys


SCHEMA_VERSION = "1.0"
FINGERPRINT_VERSION = "1"
FRAMEWORK_VERSION = "0.4.0"
VALID_CLASSIFICATIONS = {"Observed", "Inferred", "Not verifiable"}
DEFAULT_METHODLOGY_VERSION = "generic/1.0"


def fingerprint(finding: dict) -> str:
    parts = [
        finding.get("audit_type", "unknown"),
        finding.get("category", "unknown"),
        finding.get("status", "unknown"),
        finding.get("classification", "unknown"),
        ",".join(finding.get("affected_paths", [])),
        finding.get("title", ""),
        finding.get("scope", {}).get("component", "") if isinstance(finding.get("scope"), dict) else str(finding.get("scope", "")),
    ]
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def main() -> int:
    data = json.load(sys.stdin)
    findings = data if isinstance(data, list) else data.get("findings", [])
    report_versions = {
        "schema_version": data.get("schema_version", SCHEMA_VERSION) if isinstance(data, dict) else SCHEMA_VERSION,
        "framework_version": data.get("framework_version", FRAMEWORK_VERSION) if isinstance(data, dict) else FRAMEWORK_VERSION,
        "methodology_version": data.get("methodology_version", DEFAULT_METHODLOGY_VERSION) if isinstance(data, dict) else DEFAULT_METHODLOGY_VERSION,
        "fingerprint_version": data.get("fingerprint_version", FINGERPRINT_VERSION) if isinstance(data, dict) else FINGERPRINT_VERSION,
    }
    out = []
    for idx, item in enumerate(findings, start=1):
        item.setdefault("id", f"F-{idx:03d}")
        item.setdefault("classification", "Not verifiable")
        if item["classification"] not in VALID_CLASSIFICATIONS:
            raise SystemExit(f"invalid classification for {item['id']}")
        item.setdefault("status", "new")
        item.setdefault("affected_paths", [])
        item.setdefault("evidence", [])
        item.setdefault("scope", {})
        item.setdefault("recommendation", "")
        item.setdefault("summary", item.get("title", ""))
        item.setdefault("first_seen", data.get("timestamp", "1970-01-01") if isinstance(data, dict) else "1970-01-01")
        item.setdefault("last_seen", item["first_seen"])
        item.setdefault("schema_version", report_versions["schema_version"])
        item.setdefault("framework_version", report_versions["framework_version"])
        item.setdefault("methodology_version", report_versions["methodology_version"])
        item.setdefault("fingerprint_version", report_versions["fingerprint_version"])
        item.setdefault("fingerprint", fingerprint(item))
        if item.get("validate_paths"):
            for path in item["affected_paths"]:
                if not os.path.exists(path):
                    raise SystemExit(f"path does not exist: {path}")
        out.append(item)
    json.dump({"findings": out, **report_versions}, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
