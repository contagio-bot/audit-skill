#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import sys


def now_stamp() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_payload() -> dict:
    return json.load(sys.stdin)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--audit-type", required=True)
    parser.add_argument("--commit", default=None)
    parser.add_argument("--scope", default=None)
    args = parser.parse_args()

    payload = read_payload()
    root = os.path.abspath(args.repo_root)
    audit_type = args.audit_type
    commit = args.commit or payload.get("commit") or "unknown"
    scope = args.scope or payload.get("scope") or payload.get("resolved_scope") or "unknown"
    timestamp = payload.get("timestamp") or now_stamp()
    baseline = {
        "audit_type": audit_type,
        "repository_root": root,
        "scope": scope,
        "commit": commit,
        "coverage": payload.get("coverage", "unknown"),
        "persistence_mode": payload.get("persistence_mode", "unknown"),
        "timestamp": timestamp,
        "findings": payload.get("findings", []),
        "evidence": payload.get("evidence", []),
    }

    base_dir = os.path.join(root, ".audit", "baselines", audit_type)
    history_dir = os.path.join(base_dir, "history")
    ensure_dir(history_dir)

    safe_commit = commit.replace("/", "_")
    history_name = f"{timestamp.replace(':', '').replace('-', '')}-{safe_commit}.json"
    history_path = os.path.join(history_dir, history_name)
    current_path = os.path.join(base_dir, "current.json")

    with open(history_path, "w", encoding="utf-8") as fh:
        json.dump(baseline, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(current_path, "w", encoding="utf-8") as fh:
        json.dump(baseline, fh, indent=2, sort_keys=True)
        fh.write("\n")

    json.dump({"current": current_path, "history": history_path}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
