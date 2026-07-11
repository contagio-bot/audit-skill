import json
import unittest
from pathlib import Path

from _helpers import temp_repo, run_script


class PersistenceTests(unittest.TestCase):
    def test_current_and_history_are_written(self):
        root = temp_repo()
        payload = {"coverage": "full", "persistence_mode": "persist", "findings": [], "timestamp": "2026-07-10T12:00:00Z"}
        proc = run_script(
            "save_baseline.py",
            input_text=json.dumps(payload),
            args=["--repo-root", str(root), "--audit-type", "security", "--commit", "abc123", "--scope", "repo"],
        )
        saved = json.loads(proc.stdout)
        self.assertTrue(Path(saved["current"]).exists())
        self.assertTrue(Path(saved["history"]).exists())
        current = json.loads(Path(saved["current"]).read_text())
        self.assertEqual(current["audit_type"], "security")
        self.assertIn("content_hash", current)


if __name__ == "__main__":
    unittest.main()
