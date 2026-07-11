import json
import unittest

from _helpers import FIXTURES, run_script


class ExportTests(unittest.TestCase):
    def test_sarif_export_contains_localizable_findings(self):
        proc = run_script("export_sarif.py", input_text=(FIXTURES / "findings-head.json").read_text())
        sarif = json.loads(proc.stdout)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(sarif["runs"][0]["results"]), 2)

    def test_fix_plan_groups_findings(self):
        proc = run_script("build_fix_plan.py", input_text=(FIXTURES / "findings-head.json").read_text())
        plan = json.loads(proc.stdout)
        self.assertIn("deferred", plan)
        self.assertTrue(plan["deferred"])


if __name__ == "__main__":
    unittest.main()
