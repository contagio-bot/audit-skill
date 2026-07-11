import json
import unittest
from pathlib import Path

from _helpers import REPO


class SchemaTests(unittest.TestCase):
    def test_finding_schema_has_required_versioning(self):
        schema = json.loads((REPO / "schemas" / "finding.schema.json").read_text())
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0")
        self.assertIn("fingerprint_version", schema["properties"])
        self.assertIn("status", schema["properties"])
        self.assertIn("audit_type", schema["properties"])
        self.assertIn("first_seen", schema["required"])

    def test_report_schema_requires_versions(self):
        schema = json.loads((REPO / "schemas" / "audit-report.schema.json").read_text())
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0")
        self.assertIn("framework_version", schema["required"])
        self.assertIn("findings", schema["required"])
        self.assertIn("coverage", schema["properties"])

    def test_baseline_schema_requires_content_hash(self):
        schema = json.loads((REPO / "schemas" / "audit-baseline.schema.json").read_text())
        self.assertIn("content_hash", schema["required"])
        self.assertIn("approved", schema["properties"])


if __name__ == "__main__":
    unittest.main()
