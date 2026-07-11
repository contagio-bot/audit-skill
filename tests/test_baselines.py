import json
import unittest
from pathlib import Path

from _helpers import temp_repo, run_script


class BaselineTests(unittest.TestCase):
    def test_save_and_load_current_and_approved(self):
        root = temp_repo()
        payload = {
            "coverage": "full",
            "persistence_mode": "persist",
            "findings": [],
            "timestamp": "2026-07-10T12:00:00Z",
            "approved": True,
        }
        proc = run_script("save_baseline.py", input_text=json.dumps(payload), args=["--repo-root", str(root), "--audit-type", "security", "--commit", "abc123", "--scope", "repo", "--approved"])
        saved = json.loads(proc.stdout)
        self.assertTrue(Path(saved["current"]).exists())
        self.assertTrue(Path(saved["history"]).exists())
        self.assertTrue((root / ".audit" / "baselines" / "security" / "approved.json").exists())
        loaded = run_script("load_baseline.py", args=["--repo-root", str(root), "--audit-type", "security"])
        data = json.loads(loaded.stdout)
        self.assertEqual(data["commit"], "abc123")
        self.assertEqual(data["schema_version"], "1.0")
        self.assertIn("content_hash", data)


if __name__ == "__main__":
    unittest.main()
