import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path("/Users/giorgio.contarini/.claude/skills/audit")
SCRIPTS = REPO / "scripts"
FIXTURES = REPO / "tests" / "fixtures"


def run_script(script: str, input_text: str = "", args=None, check=True):
    args = args or []
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} failed: {proc.stdout}\n{proc.stderr}")
    return proc


def run_script_file(script: str, path: Path, args=None, check=True):
    args = args or []
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args, str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} failed: {proc.stdout}\n{proc.stderr}")
    return proc


def temp_repo():
    root = Path(tempfile.mkdtemp(prefix="audit-skill-test-"))
    (root / ".audit").mkdir(parents=True, exist_ok=True)
    return root


def load_json(text: str):
    return json.loads(text)
