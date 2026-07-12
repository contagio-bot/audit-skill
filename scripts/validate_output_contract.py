#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any


FORMAL_MARKDOWN_HEADINGS = [
    "Executive summary",
    "Scope and coverage",
    "Capability manifest",
    "Method and evidence",
    "Detailed findings",
    "Normalized findings",
    "Remediation",
    "Persistence disclosure",
]

STANDARD_MARKDOWN_HEADINGS = [
    "Summary",
    "Coverage and limits",
    "Findings",
    "Recommended next actions",
]

ALLOWED_COVERAGE = {"full", "partial", "batched", "risk-based", "sample"}
ALLOWED_PERSISTENCE = {"read-only", "default", "persist"}
ALLOWED_CLASSIFICATIONS = {"Observed", "Inferred", "Not verifiable"}
ALLOWED_STATUSES = {
    "new",
    "existing",
    "changed",
    "resolved",
    "accepted",
    "deferred",
    "false-positive",
    "not-verifiable",
    "superseded",
    "regressed",
}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low", "info", "n/a"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "n/a"}
ALLOWED_PRIORITY = {"P0", "P1", "P2", "P3", "P4"}


def validate_markdown(text: str, strict: bool = False, mode: str = "formal"):
    errors = []
    headings = STANDARD_MARKDOWN_HEADINGS if mode == "standard" else FORMAL_MARKDOWN_HEADINGS
    for heading in headings:
        if f"## {heading}" not in text and f"### {heading}" not in text:
            errors.append(f"missing heading: {heading}")
    if strict:
        if "schema_version" not in text:
            errors.append("missing schema_version")
        if "framework_version" not in text:
            errors.append("missing framework_version")
        if "fingerprint_version" not in text:
            errors.append("missing fingerprint_version")
    return errors


def validate_json(data: dict[str, Any], strict: bool = False):
    errors = []
    for key in ("schema_version", "framework_version", "coverage", "persistence_mode", "findings"):
        if key not in data:
            errors.append(f"missing key: {key}")

    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    if data.get("coverage") not in ALLOWED_COVERAGE:
        errors.append(f"invalid coverage: {data.get('coverage')}")
    if data.get("persistence_mode") not in ALLOWED_PERSISTENCE:
        errors.append(f"invalid persistence_mode: {data.get('persistence_mode')}")

    findings = data.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        return errors

    ids = set()
    fingerprints = set()
    evidence_ids = set()

    for item in findings:
        if not isinstance(item, dict):
            errors.append("finding must be an object")
            continue
        required = [
            "id", "title", "audit_type", "category", "status", "classification",
            "severity", "confidence", "impact", "priority", "summary",
            "evidence", "affected_paths", "scope", "recommendation",
            "fingerprint", "first_seen", "last_seen",
        ]
        for key in required:
            if key not in item:
                errors.append(f"{item.get('id', 'unknown')}: missing {key}")

        if item.get("classification") not in ALLOWED_CLASSIFICATIONS:
            errors.append(f"{item.get('id', 'unknown')}: invalid classification")
        if item.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{item.get('id', 'unknown')}: invalid status")
        if item.get("severity") not in ALLOWED_SEVERITIES:
            errors.append(f"{item.get('id', 'unknown')}: invalid severity")
        if item.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{item.get('id', 'unknown')}: invalid confidence")
        if item.get("priority") not in ALLOWED_PRIORITY:
            errors.append(f"{item.get('id', 'unknown')}: invalid priority")
        if not item.get("fingerprint"):
            errors.append(f"{item.get('id', 'unknown')}: missing fingerprint")

        fid = item.get("id")
        if fid in ids:
            errors.append(f"duplicate finding id: {fid}")
        ids.add(fid)
        fp = item.get("fingerprint")
        if fp in fingerprints:
            errors.append(f"duplicate fingerprint: {fp}")
        fingerprints.add(fp)

        evidence = item.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{item.get('id', 'unknown')}: evidence must be a non-empty list")
        else:
            evidence_ids.update(evidence)

        paths = item.get("affected_paths", [])
        if not isinstance(paths, list) or not paths:
            errors.append(f"{item.get('id', 'unknown')}: affected_paths must be a non-empty list")
        else:
            for path in paths:
                if not isinstance(path, str) or not path:
                    errors.append(f"{item.get('id', 'unknown')}: invalid affected path")
                elif strict and os.path.isabs(path):
                    errors.append(f"{item.get('id', 'unknown')}: absolute affected path not allowed")

        if item.get("classification") == "Observed" and not evidence:
            errors.append(f"{item.get('id', 'unknown')}: Observed finding requires evidence")

        first_seen = item.get("first_seen")
        last_seen = item.get("last_seen")
        if first_seen and last_seen and str(last_seen) < str(first_seen):
            errors.append(f"{item.get('id', 'unknown')}: last_seen before first_seen")

        if strict:
            version_fields = ["schema_version", "framework_version", "methodology_version", "fingerprint_version"]
            for key in version_fields:
                if key not in item and key not in data:
                    errors.append(f"{item.get('id', 'unknown')}: missing version field {key}")

    if strict:
        ledger = data.get("evidence_ledger", [])
        if ledger and isinstance(ledger, list):
            ledger_ids = set()
            for entry in ledger:
                if not isinstance(entry, dict):
                    errors.append("evidence ledger entry must be object")
                    continue
                eid = entry.get("id")
                if eid in ledger_ids:
                    errors.append(f"duplicate evidence id: {eid}")
                ledger_ids.add(eid)
                if eid not in evidence_ids:
                    # ledger may contain extra evidence, but every cited evidence should be present
                    pass
            missing_cited = evidence_ids - ledger_ids
            if missing_cited:
                errors.append(f"missing evidence ledger entries: {sorted(missing_cited)}")

        if data.get("coverage") == "full" and data.get("excluded_areas"):
            errors.append("full coverage cannot list excluded_areas")
        if data.get("persistence_mode") == "read-only" and data.get("writes_performed"):
            errors.append("read-only run cannot report writes_performed")

    return errors


def load_text(path: str):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--mode", choices=["standard", "formal"], default="formal")
    args = parser.parse_args()
    path = args.path
    if not os.path.exists(path):
        raise SystemExit(f"missing report: {path}")
    errors = []
    if path.endswith(".json"):
        errors = validate_json(json.loads(load_text(path)), strict=args.strict)
    else:
        errors = validate_markdown(load_text(path), strict=args.strict, mode=args.mode)
    if errors:
        json.dump({"valid": False, "errors": errors}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1
    json.dump({"valid": True, "errors": []}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
