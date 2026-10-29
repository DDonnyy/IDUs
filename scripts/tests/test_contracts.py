"""Meaningful report invariants, including unverified facts and distinct source-form anchors."""

import copy
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from review_report import render_markdown, validate_report, validate_request
from schema_validation import ContractError, read_json


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.examples = SCRIPTS.parent / "examples/report"
        self.report = read_json(self.examples / "report.json")
        self.finding = self.report["findings"][0]

    def make_applied(self):
        self.report["mode"] = "edit"
        self.finding["application_status"] = "applied"
        self.finding["source_anchor"] = {
            "path": "paper.tex",
            "old": self.finding["original"],
            "sha256": "0" * 64,
        }

    def test_review_contracts_stay_audit_edit_with_draft_and_configuration_separate(self):
        request = read_json(self.examples / "request.json")
        validate_request(request)
        for mode in ["draft", "write", "configure"]:
            with self.subTest(mode=mode), self.assertRaises(ContractError):
                validate_request({**request, "mode": mode})
            with self.subTest(report_mode=mode), self.assertRaises(ContractError):
                validate_report({**self.report, "mode": mode})

    def test_clean_report_is_valid_with_explicit_coverage(self):
        self.report["findings"] = []
        result = validate_report(self.report)
        self.assertEqual(result["snapshots_checked"], [])
        self.assertIn("No findings", render_markdown(self.report))
        self.report["coverage"] = []
        with self.assertRaises(ContractError):
            validate_report(self.report)

    def test_audit_cannot_claim_applied_edits(self):
        self.finding["application_status"] = "applied"
        with self.assertRaisesRegex(ContractError, "audit"):
            validate_report(self.report)

    def test_unrelated_grammar_edit_can_preserve_unchecked_empirical_status(self):
        self.make_applied()
        self.assertEqual(self.finding["evidence_status"], "NOT CHECKED")
        validate_report(self.report)
        self.finding["evidence_dependent"] = True
        with self.assertRaisesRegex(ContractError, "evidence-dependent"):
            validate_report(self.report)

    def test_verified_evidence_needs_a_recorded_locator(self):
        self.finding["evidence_status"] = "VERIFIED"
        with self.assertRaisesRegex(ContractError, "locator"):
            validate_report(self.report)
        self.finding["evidence"] = [
            {"locator": "Table 1 / column N", "detail": "Recorded for a synthetic test only."}
        ]
        validate_report(self.report)

    def test_rejected_wording_or_missing_anchor_cannot_be_recorded_as_applied(self):
        self.make_applied()
        self.finding["wording_verdict"] = "REJECT"
        with self.assertRaises(ContractError):
            validate_report(self.report)
        self.finding["wording_verdict"] = "ACCEPT"
        self.finding["source_anchor"] = None
        with self.assertRaises(ContractError):
            validate_report(self.report)

    def test_duplicate_ids_unknown_documents_and_uncovered_documents_fail(self):
        report = copy.deepcopy(self.report)
        report["findings"].append(copy.deepcopy(report["findings"][0]))
        with self.assertRaisesRegex(ContractError, "duplicate"):
            validate_report(report)
        self.finding["document_id"] = "unknown"
        with self.assertRaisesRegex(ContractError, "unknown"):
            validate_report(self.report)
        self.finding["document_id"] = "doc-1"
        self.report["documents"].append({"id": "doc-2", "description": "Not supplied", "sha256": None})
        with self.assertRaisesRegex(ContractError, "coverage"):
            validate_report(self.report)

    def test_snapshot_hash_and_quotation_are_checked_only_when_explicitly_supplied(self):
        snapshot = self.examples / "manuscript.txt"
        self.assertEqual(validate_report(self.report, {"doc-1": snapshot})["snapshots_checked"], ["doc-1"])
        self.report["documents"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ContractError, "stale"):
            validate_report(self.report, {"doc-1": snapshot})
        self.report["documents"][0]["sha256"] = None
        self.finding["original"] = "This quotation is not present."
        with self.assertRaisesRegex(ContractError, "verbatim"):
            validate_report(self.report, {"doc-1": snapshot})

    def test_export_quote_and_source_form_can_differ(self):
        source = 'TEXT = ("The results " "is shown in Table 1.")'
        self.finding["source_anchor"] = {
            "path": "paper.py",
            "old": source,
            "sha256": hashlib.sha256(source.encode()).hexdigest(),
        }
        validate_report(self.report, {"doc-1": self.examples / "manuscript.txt"})
        rendered = render_markdown(self.report)
        self.assertIn(source, rendered)
        self.assertIn(self.finding["original"], rendered)
        self.assertIn("NOT CHECKED", rendered)
        self.assertIn("proposed", rendered)

    def test_renderer_keeps_quoted_backticks_and_cli_never_overwrites_existing_output(self):
        self.finding["original"] = "An inline ``` fence is source text."
        self.assertIn("````text", render_markdown(self.report))
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "existing-manuscript.md"
            target.write_text("Keep this author's text.", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "idus.py"),
                    "validate-report",
                    str(self.examples / "report.json"),
                    "--markdown",
                    str(target),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual(target.read_text(encoding="utf-8"), "Keep this author's text.")


if __name__ == "__main__":
    unittest.main()
