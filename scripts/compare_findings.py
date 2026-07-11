#!/usr/bin/env python3
import json
import sys


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    findings = data.get("findings", data)
    return {
        "meta": {
            "schema_version": data.get("schema_version"),
            "framework_version": data.get("framework_version"),
            "methodology_version": data.get("methodology_version"),
            "fingerprint_version": data.get("fingerprint_version"),
        },
        "findings": {f["fingerprint"]: f for f in findings},
    }


def classify(base: dict, head: dict):
    base_keys = set(base["findings"])
    head_keys = set(head["findings"])
    new = sorted(head_keys - base_keys)
    resolved = sorted(base_keys - head_keys)
    common = sorted(base_keys & head_keys)
    unchanged = []
    for key in common:
        if base["findings"][key] == head["findings"][key]:
            unchanged.append(key)
    return {
        "new": [head["findings"][k] for k in new],
        "resolved": [base["findings"][k] for k in resolved],
        "unchanged": [head["findings"][k] for k in unchanged],
        "changed": [head["findings"][k] for k in common if k not in unchanged],
        "meta": {"base": base["meta"], "head": head["meta"]},
    }


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_findings.py base.json head.json")
    result = classify(load(sys.argv[1]), load(sys.argv[2]))
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
