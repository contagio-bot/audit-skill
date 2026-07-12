import json
import sys
import unittest

from _helpers import REPO, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from resolve_command import menu  # noqa: E402


REPORT_COMMANDS = [
    "deadcode", "arch", "perf", "security", "pentest", "deps",
    "supply-chain", "ci", "testing", "data", "api", "cloud",
    "operability", "privacy", "ai", "licensing",
]


def load_json(relative_path: str):
    with open(REPO / relative_path, encoding="utf-8") as fh:
        return json.load(fh)


class LoadingPlanTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_json("config/audits.json")

    def _source_text(self, command: str) -> str:
        entry = self.manifest[command]
        path = entry.get("methodology") or entry["reference"]
        return (REPO / path).read_text(encoding="utf-8")

    def test_standard_audits_do_not_load_baseline_by_default(self):
        for command in REPORT_COMMANDS:
            text = self._source_text(command)
            self.assertNotIn("baseline-protocol.md", text, command)
            self.assertNotIn("save_baseline.py", text, command)

    def test_standard_audits_do_not_load_export_by_default(self):
        for command in REPORT_COMMANDS:
            text = self._source_text(command)
            self.assertNotIn("export-formats.md", text, command)
            self.assertNotIn("export_sarif.py", text, command)

    def test_scoring_rubric_only_loaded_where_scoring_applies(self):
        for command in REPORT_COMMANDS:
            text = self._source_text(command)
            loads_scoring = "scoring-rubric.md" in text
            if command == "arch":
                self.assertTrue(loads_scoring, "arch is the scored, categorized review")
            else:
                self.assertFalse(loads_scoring, command)

    def test_methodologies_do_not_read_json_schemas_directly(self):
        for path in (REPO / "methodologies").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("schemas/", text, str(path))

    def test_dd_workflow_does_not_instruct_reading_other_methodologies_in_full(self):
        text = (REPO / "methodologies/dd/SKILL.md").read_text(encoding="utf-8")
        workflow = text.split("## Workflow", 1)[1]
        self.assertNotIn("methodologies/arch/SKILL.md", workflow)
        self.assertNotIn("methodologies/security/generic.md", workflow)
        self.assertIn("investigation-protocol.md", workflow)

    def test_dd_workflow_is_sequential_with_scratch_files(self):
        text = (REPO / "methodologies/dd/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".audit/tmp/", text)
        self.assertIn("one at a time", text)

    def test_no_argument_menu_is_grouped_by_category(self):
        menu_block = menu()
        for category in ("Quality:", "Risk:", "Continuity:", "Remediation:"):
            self.assertIn(category, menu_block)
        self.assertNotIn("--persist", menu_block)
        self.assertNotIn("--formal", menu_block)

    def test_skill_md_delegates_menu_rendering_to_the_script(self):
        text = (REPO / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("resolve_command.py --menu", text)
        self.assertNotIn("```text\nQuality:", text)


if __name__ == "__main__":
    unittest.main()
