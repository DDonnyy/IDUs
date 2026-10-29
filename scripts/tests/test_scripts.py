"""Regression checks for accidental source changes and incomplete edit batches.

Run without project dependencies:
    python -m unittest discover -s scripts/tests -v
"""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import apply_edits  # noqa: E402
import comma_candidates  # noqa: E402
import spelling_pass  # noqa: E402


class ApplyEditsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.first = self.root / "first.txt"
        self.second = self.root / "second.txt"
        self.first.write_bytes(b"The ratio was 0.75.\r\n")
        self.second.write_bytes(b"The stops were mapped.\n")
        self.originals = {self.first: self.first.read_bytes(), self.second: self.second.read_bytes()}

    def assert_originals_unchanged(self):
        for path, original in self.originals.items():
            self.assertEqual(path.read_bytes(), original)

    def edit_file(self, contents):
        path = self.root / "edits.txt"
        path.write_text(contents, encoding="utf-8")
        return path

    def test_default_cli_is_dry_run_and_apply_changes_only_approved_text(self):
        edits = self.edit_file("@@ first.txt\n<<<\nThe ratio\n===\nThe median ratio\n>>>\n")
        command = [sys.executable, str(SCRIPTS / "apply_edits.py"), str(self.root), str(edits)]
        dry = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertIn("dry run", dry.stdout)
        self.assert_originals_unchanged()
        applied = subprocess.run(command + ["--apply"], capture_output=True, text=True, check=False)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(self.first.read_bytes(), b"The median ratio was 0.75.\r\n")
        self.assertEqual(self.second.read_bytes(), self.originals[self.second])

    def test_late_failure_leaves_earlier_file_unchanged(self):
        edits = self.edit_file(
            "@@ first.txt\n<<<\nThe ratio\n===\nThe median ratio\n>>>\n"
            "@@ second.txt\n<<<\nMissing phrase\n===\nReplacement\n>>>\n"
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "apply_edits.py"), str(self.root), str(edits), "--apply"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("0 matches", result.stderr)
        self.assert_originals_unchanged()

    def test_multiple_matches_do_not_guess_an_occurrence(self):
        self.first.write_text("The ratio and the ratio", encoding="utf-8")
        before = self.first.read_bytes()
        with self.assertRaisesRegex(ValueError, "2 matches"):
            apply_edits.prepare_edits(self.root, [("first.txt", "ratio", "share")], "text")
        self.assertEqual(self.first.read_bytes(), before)

    def test_absolute_traversal_and_windows_stream_paths_rejected(self):
        unsafe = [str(self.first), "../first.txt", "sub/../../first.txt", r"C:\first.txt", "first.txt:stream"]
        for name in unsafe:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "unsafe path"):
                apply_edits.prepare_edits(self.root, [(name, "ratio", "share")], "text")
        self.assert_originals_unchanged()

    def test_symlink_outside_root_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / "outside.txt"
            destination.write_text("The ratio", encoding="utf-8")
            link = self.root / "linked.txt"
            try:
                link.symlink_to(destination)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaisesRegex(ValueError, "inside root"):
                apply_edits.prepare_edits(self.root, [("linked.txt", "ratio", "share")], "text")
            self.assertEqual(destination.read_text(encoding="utf-8"), "The ratio")

    def test_resolved_path_outside_root_is_rejected_without_symlink_privileges(self):
        with tempfile.TemporaryDirectory() as outside:
            destination = (Path(outside) / "outside.txt").resolve()
            destination.write_text("The ratio", encoding="utf-8")
            # Emulate the filesystem result of following an escaping symlink.
            with patch.object(Path, "resolve", return_value=destination):
                with self.assertRaisesRegex(ValueError, "inside root"):
                    apply_edits.target_path(self.root, "linked.txt")
            self.assertEqual(destination.read_text(encoding="utf-8"), "The ratio")

    def test_malformed_or_empty_edits_are_not_silently_ignored(self):
        malformed = [
            "", "a note, not an edit", "@@ first.txt\n", "@@ first.txt\n<<<\nratio\n===\nshare\n",
            "@@ first.txt\n<<<\nratio\n>>>\n", "@@ first.txt\n<<<\n \n===\nshare\n>>>\n",
            "@@ first.txt\n<<<\nratio\n===\nshare\n>>>\ntrailing unparsed text\n",
            "@@ first.txt\n@@ second.txt\n<<<\nstops\n===\npositions\n>>>\n",
        ]
        for contents in malformed:
            with self.subTest(contents=contents), self.assertRaises(ValueError):
                apply_edits.read_edits(self.edit_file(contents))
        self.assert_originals_unchanged()

    def test_duplicate_and_overlapping_edits_rejected(self):
        batches = [
            [("first.txt", "The ratio", "The share"), ("./first.txt", "The  ratio", "A share")],
            [("first.txt", "The ratio", "The share"), ("first.txt", "ratio was", "share is")],
        ]
        for edits in batches:
            with self.subTest(edits=edits), self.assertRaises(ValueError):
                apply_edits.prepare_edits(self.root, edits, "text")
        self.assert_originals_unchanged()

    def test_dependent_edits_do_not_match_another_edits_output(self):
        with self.assertRaisesRegex(ValueError, "0 matches"):
            apply_edits.prepare_edits(
                self.root, [("first.txt", "ratio", "discrepancy"), ("first.txt", "discrepancy", "share")], "text"
            )
        self.assert_originals_unchanged()

    def test_python_joined_strings_and_unrelated_literals_preserved(self):
        target = self.root / "paper.py"
        original = 'TEXT = (\n    "The ratio "\n    "was measured."\n)\nLABEL = "unchanged long label"\n'
        target.write_text(original, encoding="utf-8")
        prepared = apply_edits.prepare_edits(
            self.root, [("paper.py", "ratio was", "share was")], "py"
        )
        apply_edits.write_prepared(prepared)
        expected = original.replace('ratio "\n    "was', "share was")
        self.assertEqual(target.read_text(encoding="utf-8"), expected)
        namespace = {}
        exec(compile(target.read_bytes(), str(target), "exec"), namespace)
        self.assertEqual(namespace["TEXT"], "The share was measured.")
        self.assertEqual(namespace["LABEL"], "unchanged long label")

    def test_python_join_without_space_does_not_invent_a_word_boundary(self):
        target = self.root / "paper.py"
        original = 'TEXT = (\n    "The ratio"\n    "was measured."\n)\n'
        target.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "0 matches"):
            apply_edits.prepare_edits(self.root, [("paper.py", "ratio was", "share was")], "py")
        self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_invalid_python_rejects_entire_batch(self):
        target = self.root / "paper.py"
        target.write_text('TEXT = "A ratio"\n', encoding="utf-8")
        original = target.read_bytes()
        with self.assertRaises(SyntaxError):
            apply_edits.prepare_edits(
                self.root, [("first.txt", "ratio", "share"), ("paper.py", "ratio", 'bad " quote')], "text"
            )
        self.assert_originals_unchanged()
        self.assertEqual(target.read_bytes(), original)

    def test_write_failure_rolls_back_already_replaced_files(self):
        prepared = apply_edits.prepare_edits(
            self.root, [("first.txt", "ratio", "share"), ("second.txt", "stops", "positions")], "text"
        )
        replace = os.replace
        failed = False

        def fail_once(source, destination):
            nonlocal failed
            if destination == self.second and not failed:
                failed = True
                raise PermissionError("simulated locked second file")
            return replace(source, destination)

        with patch.object(apply_edits.os, "replace", side_effect=fail_once), self.assertRaises(PermissionError):
            apply_edits.write_prepared(prepared)
        self.assert_originals_unchanged()
        self.assertEqual(list(self.root.glob(".proofreading-*")), [])

    def test_changed_source_cannot_be_overwritten_by_stale_plan(self):
        prepared = apply_edits.prepare_edits(self.root, [("first.txt", "ratio", "share")], "text")
        self.first.write_bytes(b"An intervening author edit.\n")
        with self.assertRaisesRegex(ValueError, "source changed"):
            apply_edits.write_prepared(prepared)
        self.assertEqual(self.first.read_bytes(), b"An intervening author edit.\n")


class CandidateScannerTests(unittest.TestCase):
    def test_spelling_scan_never_changes_source_and_apply_flag_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.py"
            # Includes a verb and code that a regex cannot safely edit.
            contents = 'TEXT = "The company licenses color tools."\ncolor = "gray"\n'
            path.write_bytes(contents.encode("utf-8"))
            before = path.read_bytes()
            with patch.object(sys, "argv", ["spelling_pass.py", str(path)]), contextlib.redirect_stdout(io.StringIO()):
                spelling_pass.main()
            self.assertEqual(path.read_bytes(), before)
            with patch.object(sys, "argv", ["spelling_pass.py", str(path), "--apply"]):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                    spelling_pass.main()
            self.assertEqual(raised.exception.code, 2)
            self.assertEqual(path.read_bytes(), before)

    def test_comma_scan_identifies_candidates_without_mutating_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "text.txt"
            path.write_bytes(b"In this sample the stops, routes and feeds differed.\n")
            before = path.read_bytes()
            output = io.StringIO()
            with patch.object(sys, "argv", ["comma_candidates.py", str(path)]), contextlib.redirect_stdout(output):
                comma_candidates.main()
            self.assertIn(str(path), output.getvalue())
            self.assertIn("Candidate scan only", output.getvalue())
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
