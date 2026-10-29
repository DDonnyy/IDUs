"""Distribution isolation, resource completeness, reproducibility and public-file boundaries."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "source"
        self.output = self.root / "releases"
        paths = {"VERSION", "packaging/release-readme.md.in"}
        paths.update(build_release.PUBLIC_NOTICES)
        paths.update(build_release.HELPER_GUIDES)
        paths.update(build_release.CORE)
        paths.update("scripts/" + name for name in build_release.HELPERS)
        paths.update(build_release.ASSETS)
        paths.update("examples/" + name for name in build_release.EXAMPLES)
        paths.update(f"packaging/skills/{name}/SKILL.md.in" for name in build_release.SKILLS)
        for relative in paths:
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SCRIPTS.parent / relative, target)
        for relative in [
            "references/local/private.pdf",
            ".idus/config.json",
            ".config/secret.json",
            "contributions/proposals/PROP-PRIVATE.json",
        ]:
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("PRIVATE_CANARY_MUST_NOT_SHIP", encoding="utf-8")

    def build(self):
        products = build_release.build_release(self.source, self.output)
        plugin = next(path for path in products if path.is_dir())
        return products, plugin

    def test_archives_are_allowlisted_and_contain_no_private_source_material(self):
        products, plugin = self.build()
        manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertNotIn("mcpServers", manifest)
        self.assertFalse((plugin / "mcp.json").exists())
        self.assertEqual(
            sorted(path.name for path in (plugin / "skills").iterdir()), sorted(build_release.SKILLS)
        )
        self.assertFalse(any("write" in path.name for path in (plugin / "skills").iterdir()))
        for product in products:
            if product.suffix != ".zip":
                continue
            with zipfile.ZipFile(product) as archive:
                for name in archive.namelist():
                    self.assertNotIn("references/local/", name)
                    self.assertNotIn(".idus/", name)
                    self.assertNotIn(".config/", name)
                    self.assertNotIn("contributions/proposals/", name)
                    self.assertNotIn("profiles/", name)
                    self.assertNotIn("case_cus_2026", name)
                    self.assertNotIn("regression_cases.md", name)
                    self.assertNotIn("scripts/tests/", name)
                    self.assertNotIn("verification.md", name)
                    self.assertNotIn("PRIVATE_CANARY_MUST_NOT_SHIP", archive.read(name).decode("utf-8"))

    def test_every_checksums_entry_matches_and_standalone_archives_have_one_skill(self):
        products, plugin = self.build()
        index = json.loads((plugin / "checksums.json").read_text(encoding="utf-8"))["files"]
        actual = {path.relative_to(plugin).as_posix() for path in plugin.rglob("*") if path.is_file()}
        self.assertEqual(actual, set(index) | {"checksums.json"})
        for relative, expected in index.items():
            self.assertEqual(hashlib.sha256((plugin / relative).read_bytes()).hexdigest(), expected)
        standalone = [path for path in products if path.suffix == ".zip" and "plugin" not in path.name]
        self.assertEqual(len(standalone), len(build_release.SKILLS))
        for product in standalone:
            with zipfile.ZipFile(product) as archive:
                skills = [name for name in archive.namelist() if name.endswith("SKILL.md")]
                self.assertEqual(skills, ["SKILL.md"])

    def test_repeated_build_is_byte_identical_and_does_not_overwrite_unknown_changes(self):
        products, plugin = self.build()
        before = {path.name: path.read_bytes() for path in products if path.is_file()}
        rebuilt, _ = self.build()
        self.assertEqual(before, {path.name: path.read_bytes() for path in rebuilt if path.is_file()})
        unexpected = plugin / "keep-user-data.txt"
        unexpected.write_text("Do not erase.", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "different content"):
            self.build()
        self.assertEqual(unexpected.read_text(encoding="utf-8"), "Do not erase.")

    def test_copied_skills_work_independently_from_an_unrelated_workspace(self):
        products, _ = self.build()
        unrelated = self.root / "unrelated"
        unrelated.mkdir()
        manuscript = self.root / "manuscript"
        manuscript.mkdir()
        for name in build_release.SKILLS:
            archive_path = next(
                path for path in products if path.name.startswith(name + "-") and path.suffix == ".zip"
            )
            installed = unrelated / ".agents/skills" / name
            installed.mkdir(parents=True)
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(installed)
            before = build_release._index(installed)
            if name == "idus-draft":
                # Usable offline without Python helpers, review/configure or the source tree.
                build_release.validate_skill(installed)
                self.assertTrue((installed / "references/drafting.md").is_file())
                self.assertTrue((installed / "assets/templates/draft_brief.md").is_file())
                self.assertTrue((installed / "references/examples/draft_case.md").is_file())
                self.assertFalse((installed / "scripts").exists())
                self.assertEqual(build_release._index(installed), before)
                continue
            helper = installed / "scripts/idus.py"
            # Use a new workspace for each independently installed skill.
            target_workspace = manuscript / name
            target_workspace.mkdir()
            if name == "idus-review":
                self.assertFalse((installed / "scripts/contributions.py").exists())
                report = subprocess.run(
                    [
                        sys.executable,
                        str(helper),
                        "validate-report",
                        str(installed / "examples/report/report.json"),
                        "--snapshot",
                        "doc-1=" + str(installed / "examples/report/manuscript.txt"),
                    ],
                    cwd=unrelated,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(report.returncode, 0, report.stderr)
            else:
                self.assertFalse((installed / "scripts/review_report.py").exists())
                result = subprocess.run(
                    [
                        sys.executable,
                        str(helper),
                        "config",
                        "add-rule",
                        str(target_workspace),
                        str(installed / "examples/configuration/custom-rule.json"),
                        "--apply",
                    ],
                    cwd=unrelated,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                config = json.loads((target_workspace / ".idus/config.json").read_text(encoding="utf-8"))
                self.assertEqual(config["rules"][0]["id"], "USR-001")
                proposal = subprocess.run(
                    [
                        sys.executable,
                        str(helper),
                        "proposal",
                        "check",
                        str(installed / "examples/contributions/proposal.json"),
                    ],
                    cwd=unrelated,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proposal.returncode, 0, proposal.stderr)
            help_result = subprocess.run(
                [sys.executable, str(helper), "--help"],
                cwd=unrelated,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertEqual("validate-report" in help_result.stdout, name == "idus-review")
            self.assertEqual("proposal" in help_result.stdout, name == "idus-configure")
            self.assertEqual(build_release._index(installed), before)

    def test_draft_distribution_is_self_contained_without_the_review_workflow(self):
        products, plugin = self.build()
        skill = plugin / "skills/idus-draft"
        build_release.validate_skill(skill)
        self.assertFalse((skill / "references/ALGORITHM.md").exists())
        self.assertFalse((skill / "references/prompts/main_agent.md").exists())
        self.assertFalse((skill / "assets/templates/review_report.md").exists())
        archive_path = next(
            path for path in products if path.name.startswith("idus-draft-") and path.suffix == ".zip"
        )
        with zipfile.ZipFile(archive_path) as archive:
            self.assertFalse(any(name.startswith("scripts/") for name in archive.namelist()))
            expected = json.loads(archive.read("checksums.json"))["files"]
            self.assertEqual(set(archive.namelist()), set(expected) | {"checksums.json"})
            for name, sha in expected.items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), sha)

    def test_missing_public_resource_fails_before_any_release_is_published(self):
        (self.source / "rules.md").unlink()
        with self.assertRaises(OSError):
            self.build()
        self.assertFalse(list(self.output.glob("*.zip")))
        self.assertFalse(list(self.output.glob("idus-*")))

    def test_crlf_source_checkout_produces_identical_archives(self):
        products, _ = self.build()
        before = {path.name: path.read_bytes() for path in products if path.is_file()}
        for path in self.source.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        rebuilt, _ = self.build()
        self.assertEqual(before, {path.name: path.read_bytes() for path in rebuilt if path.is_file()})


if __name__ == "__main__":
    unittest.main()
