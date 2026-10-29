"""Configuration persists user extensions without touching manuscripts or installed rules."""

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import configuration
from schema_validation import ContractError, loads, read_json


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name).resolve()
        self.manuscript = self.workspace / "manuscript.txt"
        self.manuscript.write_text("Transit is not intratransit. TRANSIT desert.\n", encoding="utf-8")
        self.original_text = self.manuscript.read_bytes()
        examples = SCRIPTS.parent / "examples/configuration"
        self.rule = read_json(examples / "custom-rule.json")
        self.term = read_json(examples / "custom-term.json")

    def save(self, action, value=None, identifier=None):
        prepared = configuration.prepare_change(self.workspace, action, value, identifier)
        backup = configuration.apply_change(self.workspace, *prepared)
        self.assertEqual(self.manuscript.read_bytes(), self.original_text)
        return prepared[0], backup

    def test_read_and_preview_do_not_create_configuration(self):
        _, raw, config = configuration.load_config(self.workspace)
        self.assertIsNone(raw)
        self.assertIsNone(config["profile"]["base_profile"])
        target, original, proposed = configuration.prepare_change(self.workspace, "add-rule", self.rule)
        self.assertIn("USR-001", configuration.change_diff(target, original, proposed))
        self.assertFalse((self.workspace / ".idus").exists())
        self.assertEqual(self.manuscript.read_bytes(), self.original_text)

    def test_add_profile_update_and_recovery_copy_preserve_previous_bytes(self):
        target, _ = self.save("add-rule", self.rule)
        previous = target.read_bytes()
        _, backup = self.save("set-profile", {"spelling": "en-US"})
        self.assertEqual(backup.read_bytes(), previous)
        self.assertEqual(backup.stem, hashlib.sha256(previous).hexdigest())
        config = configuration.load_config(self.workspace)[2]
        self.assertEqual(config["revision"], 2)
        self.assertEqual(config["rules"][0]["id"], "USR-001")
        same = configuration.prepare_change(self.workspace, "set-profile", {"spelling": "en-US"})
        self.assertEqual(same[1], same[2])

    def test_invalid_entry_leaves_valid_configuration_unchanged(self):
        target, _ = self.save("add-rule", self.rule)
        previous = target.read_bytes()
        bad = copy.deepcopy(self.term)
        bad["preferred"] = None
        with self.assertRaises(ContractError):
            configuration.prepare_change(self.workspace, "add-term", bad)
        self.assertEqual(target.read_bytes(), previous)

    def test_add_does_not_replace_existing_id_and_update_keeps_id(self):
        self.save("add-rule", self.rule)
        changed = {**self.rule, "title": "Updated local clarification rule"}
        with self.assertRaises(ContractError):
            configuration.prepare_change(self.workspace, "add-rule", changed)
        self.save("update-rule", changed)
        rules = configuration.load_config(self.workspace)[2]["rules"]
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["id"], self.rule["id"])
        self.assertEqual(rules[0]["title"], changed["title"])
        self.save("remove-rule", identifier=self.rule["id"])
        self.assertEqual(configuration.load_config(self.workspace)[2]["rules"], [])

    def test_reserved_namespace_and_unknown_override_fields_are_rejected(self):
        with self.assertRaises(ContractError):
            configuration.prepare_change(self.workspace, "add-rule", {**self.rule, "id": "A1"})
        invalid = configuration.default_config()
        invalid["disable_meaning_checks"] = True
        with self.assertRaises(ContractError):
            configuration.validate_config(invalid)
        self.assertFalse((self.workspace / ".idus").exists())

    def test_stale_configuration_change_does_not_overwrite_newer_changes(self):
        self.save("init")
        prepared = configuration.prepare_change(self.workspace, "add-term", self.term)
        self.save("add-rule", self.rule)
        current = prepared[0].read_bytes()
        with self.assertRaisesRegex(ContractError, "changed after preview"):
            configuration.apply_change(self.workspace, *prepared)
        self.assertEqual(prepared[0].read_bytes(), current)

    def test_imported_backup_becomes_a_new_revision(self):
        target, _ = self.save("add-rule", self.rule)
        earlier = read_json(target)
        self.save("add-term", self.term)
        self.save("import", earlier)
        config = read_json(target)
        self.assertEqual(config["revision"], 3)
        self.assertEqual(config["lexicon"], [])
        self.assertEqual(config["rules"], earlier["rules"])

    def test_term_scan_is_contextual_case_aware_and_read_only(self):
        self.save("add-term", self.term)
        result = configuration.scan_terms(self.workspace, [self.manuscript])
        self.assertEqual([entry["matched"] for entry in result["candidates"]], ["Transit", "TRANSIT"])
        self.assertTrue(all(entry["context"] == self.term["context"] for entry in result["candidates"]))
        self.assertEqual(result["candidates"][0]["column"], 1)
        self.save("update-term", {**self.term, "status": "disabled"})
        self.assertEqual(configuration.scan_terms(self.workspace, [self.manuscript])["candidates"], [])
        self.assertEqual(self.manuscript.read_bytes(), self.original_text)

    def test_resolved_escape_is_rejected_without_symlink_privileges(self):
        original_resolve = Path.resolve
        target = self.workspace / ".idus/config.json"

        def resolve(path, *args, **kwargs):
            if path == target:
                return self.workspace.parent / "outside/config.json"
            return original_resolve(path, *args, **kwargs)

        with patch.object(Path, "resolve", resolve), self.assertRaisesRegex(ContractError, "escapes"):
            configuration.prepare_change(self.workspace, "init")
        self.assertFalse((self.workspace / ".idus").exists())

    def test_cli_dry_run_and_explicit_apply_use_workspace_not_current_directory(self):
        with tempfile.TemporaryDirectory() as unrelated:
            command = [sys.executable, str(SCRIPTS / "idus.py"), "config", "init", str(self.workspace)]
            dry = subprocess.run(command, cwd=unrelated, capture_output=True, text=True, check=False)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse((self.workspace / ".idus").exists())
            applied = subprocess.run(
                command + ["--apply"], cwd=unrelated, capture_output=True, text=True, check=False
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertTrue((self.workspace / ".idus/config.json").is_file())
            self.assertFalse((Path(unrelated) / ".idus").exists())

    def test_json_duplicate_keys_and_non_json_constants_are_rejected(self):
        for text in ['{"revision": 1, "revision": 2}', '{"revision": NaN}', '{"revision": 1e9999}']:
            with self.subTest(text=text), self.assertRaises(ContractError):
                loads(text)

    def test_legacy_configuration_is_preserved_and_usable_after_rename(self):
        legacy = self.workspace / ".paperidu/config.json"
        legacy.parent.mkdir()
        legacy.write_text(json.dumps(configuration.default_config()), encoding="utf-8")
        target, _ = self.save("add-rule", self.rule)
        self.assertEqual(target, legacy)
        self.assertFalse((self.workspace / ".idus").exists())
        self.assertEqual(configuration.load_config(self.workspace)[2]["rules"][0]["id"], "USR-001")

    def test_two_config_locations_are_an_explicit_conflict(self):
        for name in [".idus", ".paperidu"]:
            target = self.workspace / name / "config.json"
            target.parent.mkdir()
            target.write_text(json.dumps(configuration.default_config()), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "both"):
            configuration.prepare_change(self.workspace, "set-profile", {"spelling": "en-US"})

    def test_legacy_cli_forwards_to_the_current_tool(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "paperidu.py"), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), (SCRIPTS.parent / "VERSION").read_text().strip())

    def test_json_schema_integer_semantics_and_single_line_lexicon(self):
        config = configuration.default_config()
        config["revision"] = 1.0
        configuration.validate_config(config)
        config["revision"] = True
        with self.assertRaises(ContractError):
            configuration.validate_config(config)
        with self.assertRaises(ContractError):
            configuration.prepare_change(self.workspace, "add-term", {**self.term, "expression": "transit\n"})


if __name__ == "__main__":
    unittest.main()
