"""Validate report structure/source quotations and render the same findings as Markdown."""

import hashlib
import re
from pathlib import Path

from schema_validation import ContractError, unique_ids, validate_contract


def validate_request(request):
    validate_contract(request, "request")
    unique_ids(request["documents"], "request documents")


def validate_report(report, snapshots=None):
    validate_contract(report, "report")
    unique_ids(report["documents"], "report documents")
    unique_ids(report["findings"], "findings")
    documents = {entry["id"]: entry for entry in report["documents"]}
    covered = set()
    for entry in report["coverage"]:
        if entry["document_id"] not in documents:
            raise ContractError("coverage refers to an unknown document")
        covered.add(entry["document_id"])
    if covered != set(documents):
        raise ContractError("every document needs an explicit coverage entry")
    for finding in report["findings"]:
        if finding["document_id"] not in documents:
            raise ContractError(f"{finding['id']}: unknown document")
        if finding["evidence_status"] == "VERIFIED" and not finding["evidence"]:
            raise ContractError(f"{finding['id']}: VERIFIED needs an evidence locator")
        if finding["application_status"] == "applied":
            if report["mode"] != "edit":
                raise ContractError("an audit cannot contain applied manuscript edits")
            if finding["wording_verdict"] not in {"ACCEPT", "ACCEPT WITH FIX"}:
                raise ContractError(f"{finding['id']}: applied wording must be accepted")
            if finding["source_anchor"] is None or finding["proposal"] is None:
                raise ContractError(f"{finding['id']}: applied edit needs a source anchor and replacement")
            if finding["evidence_dependent"] and finding["evidence_status"] != "VERIFIED":
                raise ContractError(f"{finding['id']}: evidence-dependent edit lacks verified evidence")
    checked = []
    for document_id, filename in (snapshots or {}).items():
        if document_id not in documents:
            raise ContractError(f"unknown snapshot document {document_id}")
        raw = Path(filename).read_bytes()
        expected = documents[document_id]["sha256"]
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise ContractError(f"{document_id}: stale snapshot hash")
        text = raw.decode("utf-8-sig")
        for finding in report["findings"]:
            if finding["document_id"] == document_id and finding["original"] not in text:
                raise ContractError(f"{finding['id']}: original is not verbatim in the supplied snapshot")
        checked.append(document_id)
    return {
        "status": "valid",
        "snapshots_checked": checked,
        "notice": "Contract and supplied quotations only; meaning, empirical support and source-form anchors need review.",
    }


def _block(text):
    lengths = [len(match.group()) for match in re.finditer(r"`+", text)]
    fence = "`" * max(3, max(lengths, default=0) + 1)
    return f"{fence}text\n{text}\n{fence}"


def render_markdown(report):
    validate_report(report)
    lines = [
        "# IDUs review report",
        "",
        report["summary"],
        "",
        f"Toolkit: {report['toolkit_version']}; mode: {report['mode']}; "
        f"configuration revision: {report.get('configuration_revision')}",
        "",
        "## Coverage",
        "",
    ]
    for item in report["coverage"]:
        lines.append(f"- {item['document_id']}: {item['scope']} ({item['status']}).")
        lines.extend(f"  - Limitation: {limit}" for limit in item["limitations"])
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("No findings recorded in the reviewed scope.")
    for item in report["findings"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"Location: {item['document_id']} / {item['location']}",
                "",
                f"{item['category']}; priority {item['priority']}; confidence {item['confidence']}",
                "",
                "Original:",
                "",
                _block(item["original"]),
                "",
                "Proposal:",
                "",
                _block(item["proposal"]) if item["proposal"] is not None else "Author input needed.",
                "",
                item["reason"],
                "",
                f"Rules: {', '.join(item['rule_ids']) or 'none specified'}",
                "",
                f"Wording: {item['wording_verdict']}; evidence: {item['evidence_status']}; "
                f"application: {item['application_status']}",
                "",
                f"Authorisation: {item['authorisation']}",
                "",
            ]
        )
        for evidence in item["evidence"]:
            lines.extend([f"- Evidence: {evidence['locator']}: {evidence['detail']}", ""])
        if item["source_anchor"] is not None:
            anchor = item["source_anchor"]
            lines.extend(
                [
                    f"Source-form anchor: {anchor['path']} (SHA-256 {anchor['sha256']})",
                    "",
                    _block(anchor["old"]),
                    "",
                ]
            )
    lines.extend(["## Questions", ""])
    lines.extend(f"- {question}" for question in report["questions"])
    if not report["questions"]:
        lines.append("No open questions recorded.")
    lines.extend(
        [
            "",
            "Contract validation does not establish scientific validity or independently verify evidence.",
            "",
        ]
    )
    return "\n".join(lines)
