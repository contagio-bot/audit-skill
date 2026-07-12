import json
import re
import sys
import unittest

from _helpers import REPO, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from resolve_command import REPORT_COMMANDS_LOAD_FINDING_CONTRACT  # noqa: E402


def load_json(relative_path: str):
    with open(REPO / relative_path, encoding="utf-8") as fh:
        return json.load(fh)


def referenced_paths(text: str) -> set[str]:
    """Backtick-quoted bundled paths, e.g. `audit/reference/foo.md` or `reference/foo.md`."""
    found = set()
    for match in re.findall(r"`(?:audit/)?((?:reference|methodologies)/[^`]+)`", text):
        found.add(match)
    return found


class ReferenceBudgetTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_json("config/audits.json")
        self.budget = load_json("config/loading-budget.json")

    def budget_for(self, command: str) -> dict:
        return self.budget.get(command, self.budget["default"])

    def test_every_manifest_command_has_a_reference_file(self):
        for command, entry in self.manifest.items():
            self.assertTrue((REPO / entry["reference"]).exists(), command)
            if entry.get("methodology"):
                self.assertTrue((REPO / entry["methodology"]).exists(), command)

    def test_common_references_do_not_exceed_budget(self):
        common = {
            "reference/bootstrap.md",
            "reference/persistence-protocol.md",
            "reference/finding-contract.md",
            "reference/output-contract.md",
        }
        for command, entry in self.manifest.items():
            if command not in REPORT_COMMANDS_LOAD_FINDING_CONTRACT:
                continue
            source = entry.get("methodology") or entry["reference"]
            text = (REPO / source).read_text(encoding="utf-8")
            loaded_common = referenced_paths(text) & common
            budget = self.budget_for(command)
            self.assertLessEqual(
                len(loaded_common),
                budget["max_common_references"],
                f"{command} loads {sorted(loaded_common)}, over budget {budget['max_common_references']}",
            )

    def test_methodology_files_per_command_within_budget(self):
        for command, entry in self.manifest.items():
            budget = self.budget_for(command)
            count = 1 if entry.get("methodology") else 0
            self.assertLessEqual(count, budget["max_methodology_files"], command)

    def test_dd_budget_marks_it_sequential(self):
        dd_budget = self.budget["dd"]
        self.assertTrue(dd_budget["sequential"])
        self.assertEqual(dd_budget["max_active_methodologies"], 1)


if __name__ == "__main__":
    unittest.main()
