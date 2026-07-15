import json
import sys
import unittest

from _helpers import REPO, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from resolve_command import resolve, ALWAYS_FORMAL_COMMANDS  # noqa: E402


REPORT_COMMANDS = [
    "deadcode", "arch", "perf", "security", "pentest", "deps",
    "supply-chain", "ci", "testing", "data", "api", "cloud",
    "operability", "privacy", "ai", "licensing",
]


def load_json(relative_path: str):
    with open(REPO / relative_path, encoding="utf-8") as fh:
        return json.load(fh)


class ReferenceBudgetTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_json("config/audits.json")
        self.budget = load_json("config/loading-budget.json")["default"]

    def test_every_manifest_command_has_a_reference_or_methodology(self):
        for command, entry in self.manifest.items():
            self.assertTrue(entry.get("reference") or entry.get("methodology"), command)
            if entry.get("reference"):
                self.assertTrue((REPO / entry["reference"]).exists(), command)
            if entry.get("methodology"):
                self.assertTrue((REPO / entry["methodology"]).exists(), command)

    def test_standard_mode_does_not_load_formal_only_files(self):
        for command in REPORT_COMMANDS:
            plan = resolve(command)
            self.assertEqual(plan["mode"], "standard", command)
            for formal_only in ("reference/finding-contract.md", "reference/formal-delta.md", "reference/output-contract.md"):
                self.assertNotIn(formal_only, plan["load"], command)
            self.assertIn("reference/persistence-protocol.md", plan["load"], command)
            self.assertLessEqual(len(plan["load"]), self.budget["max_files_standard"], command)

    def test_formal_mode_loads_the_formal_trio(self):
        for command in REPORT_COMMANDS:
            plan = resolve(command, formal=True)
            self.assertEqual(plan["mode"], "formal", command)
            for required in ("reference/finding-contract.md", "reference/formal-delta.md", "reference/output-contract.md"):
                self.assertIn(required, plan["load"], command)
            self.assertLessEqual(len(plan["load"]), self.budget["max_files_formal"], command)

    def test_always_formal_commands_are_formal_without_the_flag(self):
        for command in ALWAYS_FORMAL_COMMANDS:
            plan = resolve(command)
            self.assertEqual(plan["mode"], "formal", command)

    def test_non_markdown_format_forces_formal(self):
        plan = resolve("security", fmt="json")
        self.assertEqual(plan["mode"], "formal")

    def test_persistence_protocol_always_loaded(self):
        # persistence-protocol.md governs default (persist-by-default)
        # behavior, so every command loads it.
        plan = resolve("security")
        self.assertIn("reference/persistence-protocol.md", plan["load"])

    def test_common_standard_footprint_within_line_budget(self):
        bootstrap_lines = len((REPO / "reference/bootstrap-lite.md").read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(bootstrap_lines, self.budget["max_common_lines_standard"])

    def test_dd_budget_marks_it_sequential(self):
        dd_budget = load_json("config/loading-budget.json")["dd"]
        self.assertTrue(dd_budget["sequential"])
        self.assertEqual(dd_budget["max_active_methodologies"], 1)


if __name__ == "__main__":
    unittest.main()
