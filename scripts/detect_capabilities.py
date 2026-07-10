#!/usr/bin/env python3
import json
import os
import shutil
import socket
import subprocess
import sys


TOOLS = ["git", "python3", "node", "npm", "pnpm", "yarn", "docker", "rg", "pytest"]


def has_network() -> bool:
    try:
        socket.gethostbyname("github.com")
        return True
    except OSError:
        return False


def detect_languages(root: str):
    langs = []
    if os.path.exists(os.path.join(root, "package.json")):
        langs.append("javascript-or-typescript")
    if os.path.exists(os.path.join(root, "pyproject.toml")) or os.path.exists(os.path.join(root, "requirements.txt")):
        langs.append("python")
    if os.path.exists(os.path.join(root, "go.mod")):
        langs.append("go")
    if os.path.exists(os.path.join(root, "Cargo.toml")):
        langs.append("rust")
    return langs


def main() -> int:
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    available = [tool for tool in TOOLS if shutil.which(tool)]
    unavailable = [tool for tool in TOOLS if tool not in available]
    writable = os.access(root, os.W_OK)
    git_root = None
    if shutil.which("git"):
        try:
            git_root = subprocess.check_output(
                ["git", "-C", root, "rev-parse", "--show-toplevel"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError:
            git_root = None
    result = {
        "target": root,
        "languages": detect_languages(root),
        "available_tools": available,
        "unavailable_tools": unavailable,
        "network": has_network(),
        "writable": writable,
        "git_root": git_root,
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
