import unittest
from pathlib import Path

from _helpers import load_json, run_script


class FingerprintTests(unittest.TestCase):
    def test_compare_findings_uses_fingerprint(self):
        fixtures = Path(__file__).resolve().parent / "fixtures"
        base = load_json((fixtures / "findings-base.json").read_text())
        head = load_json((fixtures / "findings-head.json").read_text())
        import json
        import tempfile
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
