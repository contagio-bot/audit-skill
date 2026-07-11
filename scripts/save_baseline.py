#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from typing import Any


SCHEMA_VERSION = "1.0"
FRAMEWORK_VERSION = "0.4.0"
FINGERPRINT_VERSION = "1"


def now_stamp() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_payload() -> dict[str, Any]:
    return json.load(sys.stdin)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def sanitize(value: str, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"invalid {label}")
    if value in {".", ".."}:
        raise SystemExit(f"invalid {label}")
    if any(sep in value for sep in ("/", "\\")):
        raise SystemExit(f"invalid {label}")
    if not re.fullmatch(r"[A-Za-z0-9._:-]+", value):
        raise SystemExit(f"invalid {label}")
    return value


def stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def atomic_write(path: str, payload: dict[str, Any]) -> None:
    directory = os.path.dirname(path)
    ensure_dir(directory)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def validate_baseline(payload: dict[str, Any]) -> None:
    required = [
        "schema_version",
        "framework_version",
        "methodology_version",
        "fingerprint_version",
        "audit_type",
        "repository_root",
        "scope",
        "commit",
        "coverage",
        "persistence_mode",
        "timestamp",
        "findings",
        "evidence",
    ]
    for key in required:
        if key not in payload:
            raise SystemExit(f"missing baseline field: {key}")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise SystemExit("schema_version mismatch")
    if payload["coverage"] not in {"full", "partial", "batched", "risk-based", "sample"}:
        raise SystemExit("invalid coverage")
    if payload["persistence_mode"] not in {"read-only", "persist"}:
        raise SystemExit("invalid persistence_mode")


def build_baseline(args, payload: dict[str, Any]) -> dict[str, Any]:
    root = os.path.abspath(args.repo_root)
    audit_type = sanitize(args.audit_type, "audit type")
    commit = sanitize(str(args.commit or payload.get("commit") or "unknown"), "commit")
    scope = str(args.scope or payload.get("scope") or payload.get("resolved_scope") or "unknown")
    timestamp = payload.get("timestamp") or now_stamp()
    methodology_version = str(payload.get("methodology_version") or args.methodology_version or "generic/1.0")
    baseline = {
        "schema_version": SCHEMA_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "methodology_version": methodology_version,
        "fingerprint_version": FINGERPRINT_VERSION,
        "audit_type": audit_type,
        "repository_root": root,
        "scope": scope,
        "commit": commit,
        "coverage": payload.get("coverage", "unknown"),
        "persistence_mode": payload.get("persistence_mode", "unknown"),
        "timestamp": timestamp,
        "findings": payload.get("findings", []),
        "evidence": payload.get("evidence", []),
        "profile": payload.get("profile"),
        "approved": bool(payload.get("approved", False) or args.approved),
    }
    baseline["content_hash"] = stable_hash(baseline)
    validate_baseline(baseline)
    return baseline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--audit-type", required=True)
    parser.add_argument("--commit", default=None)
    parser.add_argument("--scope", default=None)
    parser.add_argument("--methodology-version", default=None)
    parser.add_argument("--approved", action="store_true")
    args = parser.parse_args()

    payload = read_payload()
    baseline = build_baseline(args, payload)
    root = baseline["repository_root"]
    audit_type = baseline["audit_type"]
    base_dir = os.path.join(root, ".audit", "baselines", audit_type)
    history_dir = os.path.join(base_dir, "history")
    ensure_dir(history_dir)

    safe_commit = baseline["commit"].replace("/", "_")
    stamp = baseline["timestamp"].replace(":", "").replace("-", "")
    history_name = f"{stamp}-{safe_commit}.json"
    history_path = os.path.join(history_dir, history_name)
    current_path = os.path.join(base_dir, "current.json")
    approved_path = os.path.join(base_dir, "approved.json")
    lock_path = os.path.join(base_dir, ".lock")

    if os.path.exists(lock_path):
        raise SystemExit("baseline store locked")

    try:
        with open(lock_path, "w", encoding="utf-8") as lock:
            lock.write(str(os.getpid()))
        atomic_write(history_path, baseline)
        atomic_write(current_path, baseline)
        if baseline["approved"]:
            atomic_write(approved_path, baseline)
    finally:
        if os.path.exists(lock_path):
            os.unlink(lock_path)

    json.dump({"current": current_path, "history": history_path, "approved": approved_path if baseline["approved"] else None}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
