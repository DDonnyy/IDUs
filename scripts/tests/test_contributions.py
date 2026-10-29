"""Proposal transport safeguards; these tests cannot establish editorial novelty or privacy."""

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import contributions
from schema_validation import ContractError, read_json


class ContributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.proposal = read_json(SCRIPTS.parent / "examples/contributions/proposal.json")

    def ready(self):
        proposal = copy.deepcopy(self.proposal)
        proposal["overlap_review"].update(
            {
                "status": "reviewed",
                "corpus_sha256": contributions.corpus()["sha256"],
                "summary": "Synthetic test declaration; no actual editorial novelty or privacy claim.",
                "comparisons": [
                    {
                        "rule_id": "B1",
                        "relationship": "refines",
                        "reason": "Synthetic scoped example refinement.",
                    }
                ],
            }
        )
        proposal["privacy"].update(status="safe_to_share", note="Synthetic test-only data.")
        return proposal

    def test_pending_example_can_be_checked_but_cannot_be_exported(self):
        contributions.validate_proposal(self.proposal)
        target = self.workspace / "export"
        with self.assertRaisesRegex(ContractError, "overlap review"):
            contributions.export_proposal(self.proposal, target)
        self.assertFalse(target.exists())

    def test_export_contains_only_declared_fields_and_verified_checksums(self):
        private = self.workspace / "private-manuscript.txt"
        private.write_text("PRIVATE_CANARY_NOT_AN_ATTACHMENT", encoding="utf-8")
        self.proposal = self.ready()
        target = self.workspace / "export"
        result = contributions.export_proposal(self.proposal, target)
        self.assertFalse(result["published"])
        self.assertEqual(
            {path.name for path in target.iterdir()}, {"proposal.json", "PR_BODY.md", "checksums.json"}
        )
        for name, expected in read_json(target / "checksums.json").items():
            self.assertEqual(hashlib.sha256((target / name).read_bytes()).hexdigest(), expected)
        exported = (target / "proposal.json").read_text(encoding="utf-8")
        self.assertNotIn("PRIVATE_CANARY", exported)
        self.assertEqual(json.loads(exported), self.proposal)

    def test_existing_export_or_empty_directory_is_not_overwritten(self):
        target = self.workspace / "keep"
        target.mkdir()
        with self.assertRaisesRegex(ContractError, "already exists"):
            contributions.export_proposal(self.ready(), target)
        self.assertEqual(list(target.iterdir()), [])

    def test_unreviewed_privacy_and_stale_base_block_export(self):
        for field in ["privacy", "base_version", "digest"]:
            with self.subTest(field=field):
                proposal = self.ready()
                if field == "privacy":
                    proposal["privacy"]["status"] = "unreviewed"
                elif field == "base_version":
                    proposal["base_version"] = "0.0.1"
                else:
                    proposal["overlap_review"]["corpus_sha256"] = "0" * 64
                with self.assertRaises(ContractError):
                    contributions.validate_proposal(proposal, ready=True)

    def test_duplicate_or_conflicting_guidance_does_not_export_as_ready(self):
        for relationship in ["duplicate", "conflicts"]:
            proposal = self.ready()
            proposal["overlap_review"]["comparisons"][0]["relationship"] = relationship
            with self.assertRaisesRegex(ContractError, "duplicate proposal|conflicting guidance"):
                contributions.validate_proposal(proposal, ready=True)

    def test_refinements_keep_known_ids_and_must_be_compared(self):
        for change in ["missing", "unknown", "wrong_relationship", "new_with_refinement", "repeated"]:
            with self.subTest(change=change):
                proposal = self.ready()
                if change == "missing":
                    proposal["target_ids"] = []
                elif change == "unknown":
                    proposal["target_ids"] = ["B9999"]
                elif change == "wrong_relationship":
                    proposal["overlap_review"]["comparisons"][0]["relationship"] = "related"
                elif change == "new_with_refinement":
                    proposal.update(change="new_rule", target_ids=[])
                else:
                    proposal["overlap_review"]["comparisons"] *= 2
                with self.assertRaises(ContractError):
                    contributions.validate_proposal(proposal, ready=True)

    def test_empty_examples_and_keep_cases_are_required_and_fixes_must_change(self):
        for field in ["examples", "counterexamples", "unchanged", "whitespace"]:
            proposal = self.ready()
            if field == "unchanged":
                proposal["examples"][0]["proposed"] = proposal["examples"][0]["original"]
            elif field == "whitespace":
                proposal["scope"] = "  \n "
            else:
                proposal[field] = []
            with self.assertRaises(ContractError):
                contributions.validate_proposal(proposal)

    def test_non_id_guidance_also_invalidates_fingerprint(self):
        root = self.workspace / "toolkit"
        root.mkdir()
        shutil.copyfile(SCRIPTS.parent / "VERSION", root / "VERSION")
        for relative in contributions.CORPUS_FILES:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SCRIPTS.parent / relative, destination)
        proposal = self.ready()
        contributions.validate_proposal(proposal, root, ready=True)
        with (root / "lexicon.md").open("a", encoding="utf-8") as stream:
            stream.write("\nA new contextual exception.\n")
        with self.assertRaisesRegex(ContractError, "current corpus"):
            contributions.validate_proposal(proposal, root, ready=True)

    def test_search_returns_candidates_without_semantic_verdict_or_mutation(self):
        before = copy.deepcopy(self.proposal)
        result = contributions.overlap_candidates(self.proposal)
        self.assertEqual(self.proposal, before)
        self.assertTrue(any(item["rule_id"] == "B1" for item in result["candidates"]))
        self.assertIn("lexicon.md", result["resources"])
        self.assertNotIn("novel", result)
        self.assertNotIn("accepted", result)

    def test_render_keeps_provenance_counterexamples_and_safe_code_fences(self):
        proposal = self.ready()
        proposal["examples"][0]["original"] = "before ``` literal"
        text = contributions.render_proposal(proposal)
        self.assertIn("````text\nbefore ``` literal\n````", text)
        self.assertIn(proposal["counterexamples"][0]["text"], text)
        self.assertIn("synthetic / synthetic", text)
        self.assertIn("maintainer acceptance pending", text)

    def test_repository_proposals_are_structurally_valid_and_named_by_id(self):
        # Historical proposals may target an older corpus. Submission needs a separate --ready check.
        for path in (SCRIPTS.parent / "contributions/proposals").glob("*.json"):
            with self.subTest(proposal=path.name):
                proposal = read_json(path)
                self.assertEqual(path.stem, proposal["id"])
                contributions.validate_proposal(proposal)


if __name__ == "__main__":
    unittest.main()
