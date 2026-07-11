#!/usr/bin/env python3
import argparse
import json
import os
import sys


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--audit-type", required=True)
    args = parser.parse_args()
    root = os.path.abspath(args.repo_root)
    base_dir = os.path.join(root, ".audit", "baselines", args.audit_type)
    approved = os.path.join(base_dir, "approved.json")
    current = os.path.join(base_dir, "current.json")
    history_dir = os.path.join(base_dir, "history")

    for candidate in (approved, current):
        if os.path.exists(candidate):
            json.dump(load(candidate), sys.stdout, indent=2, sort_keys=True)
            sys.stdout.write("\n")
            return 0

    if not os.path.isdir(history_dir):
        json.dump({"found": False, "reason": "no baseline"}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1

    candidates = sorted(
        os.path.join(history_dir, name)
        for name in os.listdir(history_dir)
        if name.endswith(".json")
    )
    if not candidates:
        json.dump({"found": False, "reason": "no baseline"}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1
    json.dump(load(candidates[-1]), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
