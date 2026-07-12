import unittest

from _helpers import FIXTURES, run_script_file


class ValidationTests(unittest.TestCase):
    def test_good_markdown_passes(self):
        proc = run_script_file("validate_output_contract.py", FIXTURES / "report-good.md")
        self.assertIn('"valid": true', proc.stdout.lower())

    def test_bad_markdown_fails(self):
        proc = run_script_file("validate_output_contract.py", FIXTURES / "report-bad.md", check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing heading", proc.stdout)

    def test_good_json_passes(self):
        proc = run_script_file("validate_output_contract.py", FIXTURES / "report-good.json")
        self.assertIn('"valid": true', proc.stdout.lower())

    def test_good_standard_markdown_passes_in_standard_mode(self):
        proc = run_script_file(
            "validate_output_contract.py",
            FIXTURES / "report-good-standard.md",
            args=["--mode", "standard"],
        )
        self.assertIn('"valid": true', proc.stdout.lower())

    def test_good_standard_markdown_fails_in_formal_mode(self):
        proc = run_script_file(
            "validate_output_contract.py",
            FIXTURES / "report-good-standard.md",
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing heading", proc.stdout)


if __name__ == "__main__":
    unittest.main()
