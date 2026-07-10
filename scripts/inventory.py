#!/usr/bin/env python3
import json
import os
import sys
from collections import defaultdict

EXCLUDE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".next",
    "dist", "build", "coverage", ".turbo", ".cache"
}


def classify(path: str) -> str:
    low = path.lower()
    if any(part in EXCLUDE_DIRS for part in path.split(os.sep)):
        return "excluded"
    if "/tests/" in low or low.startswith("tests/") or "/test/" in low:
        return "tests"
    if low.endswith((".md", ".rst", ".txt")):
        return "docs"
    if any(name in low for name in ("docker-compose", "terraform", ".github/workflows", "k8s", "helm")):
        return "infra"
    if any(name in low for name in ("schema", "migration", "alembic", "prisma", "sql")):
        return "data"
    if low.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".env.example")):
        return "config"
    return "source"


def main() -> int:
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    buckets = defaultdict(list)
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            full = os.path.join(current, name)
            rel = os.path.relpath(full, root)
            buckets[classify(rel)].append(rel)
    result = {
        "repository_root": root,
        "counts": {k: len(v) for k, v in buckets.items()},
        "samples": {k: v[:25] for k, v in buckets.items()},
        "excluded_dirs": sorted(EXCLUDE_DIRS),
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
