"""Generated repository output is reproducible, checkable and cannot consume unrelated files."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_release
import sync_distribution


class DistributionSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        paths = {"VERSION", "packaging/release-readme.md.in"}
        paths.update(build_release.PUBLIC_NOTICES)
        paths.update(build_release.HELPER_GUIDES)
        paths.update(build_release.CORE)
        paths.update(build_release.ASSETS)
        paths.update("scripts/" + name for name in build_release.HELPERS)
        paths.update("examples/" + name for name in build_release.EXAMPLES)
        paths.update(f"packaging/skills/{name}/SKILL.md.in" for name in build_release.SKILLS)
        for relative in paths:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SCRIPTS.parent / relative, target)

    def test_bootstrap_check_is_read_only_and_write_then_check_is_idempotent(self):
        with self.assertRaisesRegex(ValueError, "stale"):
            sync_distribution.sync(self.root)
        self.assertFalse((self.root / "skills").exists())
        count, changed = sync_distribution.sync(self.root, write=True)
        self.assertGreater(changed, 0)
        self.assertEqual(sync_distribution.sync(self.root), (count, 0))

    def test_changed_generated_output_fails_check_and_can_be_regenerated(self):
        sync_distribution.sync(self.root, write=True)
        target = self.root / "skills/idus-draft/SKILL.md"
        original = target.read_bytes()
        target.write_text("Edited generated copy.", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "stale"):
            sync_distribution.sync(self.root)
        sync_distribution.sync(self.root, write=True)
        self.assertEqual(target.read_bytes(), original)

    def test_unmanaged_files_are_preserved_and_never_deleted(self):
        sync_distribution.sync(self.root, write=True)
        extra = self.root / "skills/idus-draft/private-notes.txt"
        extra.write_text("KEEP THIS", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            sync_distribution.sync(self.root, write=True)
        self.assertEqual(extra.read_text(encoding="utf-8"), "KEEP THIS")

    def test_unowned_manifest_collision_does_not_overwrite_user_data(self):
        target = self.root / "plugin.json"
        target.write_text('{"name":"keep-user-data"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unowned"):
            sync_distribution.sync(self.root, write=True)
        self.assertIn("keep-user-data", target.read_text())
        self.assertFalse((self.root / "skills").exists())

    def test_inventory_cannot_claim_files_outside_generated_roots(self):
        path = self.root / sync_distribution.INVENTORY
        path.write_text(json.dumps({"format_version": 1, "files": {"../outside.txt": "0" * 64}}))
        with self.assertRaisesRegex(ValueError, "invalid"):
            sync_distribution.sync(self.root, write=True)
        self.assertFalse((self.root / "skills").exists())


if __name__ == "__main__":
    unittest.main()
