"""Redirected helper output must remain usable outside a UTF-8 system locale."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]


class UnicodeCLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "проект-測試"
        self.workspace.mkdir()
        self.env = {**os.environ, "PYTHONIOENCODING": "ascii:strict", "PYTHONUTF8": "0"}

    def run_cli(self, script, *args, expected_exit=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / script), *map(str, args)],
            cwd=self.workspace,
            env=self.env,
            capture_output=True,
            check=False,
        )
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
        self.assertEqual(result.returncode, expected_exit, stderr)
        return stdout, stderr

    def test_configuration_and_legacy_alias_preserve_unicode_in_pipes(self):
        profile = self.workspace / "profile.json"
        language = "Русский → 中文"
        profile.write_text(json.dumps({"report_language": language}, ensure_ascii=False), encoding="utf-8")
        output, _ = self.run_cli("idus.py", "config", "set-profile", self.workspace, profile)
        self.assertIn(language, output)
        self.assertFalse((self.workspace / ".idus").exists())
        self.run_cli("idus.py", "config", "set-profile", self.workspace, profile, "--apply")
        output, _ = self.run_cli("paperidu.py", "config", "show", self.workspace)
        self.assertEqual(json.loads(output)["profile"]["report_language"], language)
        missing = self.workspace / "не-найден-缺.json"
        _, error = self.run_cli("idus.py", "config", "set-profile", self.workspace, missing, expected_exit=1)
        self.assertIn(missing.name, error)

    def test_overlap_search_can_print_the_existing_rule_corpus(self):
        proposal = json.loads((SCRIPTS.parent / "examples/contributions/proposal.json").read_text(encoding="utf-8"))
        proposal["instruction"] = "Preserve aims, methods, results and conclusions."
        source = self.workspace / "proposal.json"
        source.write_text(json.dumps(proposal), encoding="utf-8")
        output, _ = self.run_cli("idus.py", "proposal", "overlaps", source)
        result = json.loads(output)
        self.assertTrue(any("→" in item["text"] for item in result["candidates"]))

    def test_scanners_and_applier_handle_unicode_text_and_paths(self):
        manuscript = self.workspace / "文章.txt"
        original = "The color of λ is shown. We compared λ, beta and gamma.\n"
        manuscript.write_text(original, encoding="utf-8")
        for script in ["spelling_pass.py", "comma_candidates.py"]:
            with self.subTest(script=script):
                output, _ = self.run_cli(script, manuscript)
                self.assertIn(manuscript.name, output)
                self.assertIn("λ", output)
                self.assertEqual(manuscript.read_text(encoding="utf-8"), original)
        edits = self.workspace / "edits.txt"
        edits.write_text("@@ 文章.txt\n<<<\nThe color\n===\nThe colour\n>>>\n", encoding="utf-8")
        self.run_cli("apply_edits.py", self.workspace, edits)
        self.assertEqual(manuscript.read_text(encoding="utf-8"), original)
        output, _ = self.run_cli("apply_edits.py", self.workspace, edits, "--apply")
        self.assertIn(manuscript.name, output)
        self.assertEqual(manuscript.read_text(encoding="utf-8"), original.replace("The color", "The colour"))


if __name__ == "__main__":
    unittest.main()
