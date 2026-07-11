import json
import tempfile
import unittest
from pathlib import Path

from _helpers import FIXTURES, load_json, run_script


class DiffTests(unittest.TestCase):
    def test_compare_findings_classifies_new_and_unchanged(self):
        base = json.loads((FIXTURES / "findings-base.json").read_text())
        head = json.loads((FIXTURES / "findings-head.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            base_path = Path(td) / "base.json"
            head_path = Path(td) / "head.json"
            base_path.write_text(json.dumps(base))
            head_path.write_text(json.dumps(head))
            proc = run_script("compare_findings.py", args=[str(base_path), str(head_path)])
            result = load_json(proc.stdout)
        self.assertEqual(len(result["new"]), 1)
        self.assertEqual(len(result["unchanged"]), 1)
        self.assertEqual(result["meta"]["base"]["fingerprint_version"], None)


if __name__ == "__main__":
    unittest.main()
