#!/usr/bin/env python3
import json
import sys


def load(path: str):
    with open(path) as fh:
        data = json.load(fh)
    return {f["fingerprint"]: f for f in data.get("findings", data)}


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_findings.py base.json head.json")
    base = load(sys.argv[1])
    head = load(sys.argv[2])
    new = sorted(set(head) - set(base))
    resolved = sorted(set(base) - set(head))
    unchanged = sorted(set(base) & set(head))
    result = {
        "new": [head[k] for k in new],
        "resolved": [base[k] for k in resolved],
        "unchanged": [head[k] for k in unchanged],
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
