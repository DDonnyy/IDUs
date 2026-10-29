# Review JSON contracts

JSON is optional; text reviews use the same separation of wording, evidence and application.
[request.schema.json](../scripts/schemas/request.schema.json) accepts audit/edit, supplied document
IDs/text/paths and scope. [report.schema.json](../scripts/schemas/report.schema.json) records findings,
coverage, questions and independent statuses. Draft uses its lightweight brief/delivery instead.
Contract version remains `1.0`; unique IDs and coverage must agree with the report's documents.

```text
python scripts/idus.py validate-request request.json
python scripts/idus.py validate-report report.json --snapshot doc-1=text-export.txt
python scripts/idus.py validate-report report.json --markdown NEW_REPORT.md
```

The standard-library validator implements the bundled schema subset and relationship checks,
rejecting duplicate JSON keys/non-finite values. It does not fetch schemas, inspect evidence links,
verify science or apply edits. VERIFIED evidence needs a locator; evidence-dependent application
requires verification, accepted wording, edit mode, authorisation and a source-form anchor.
An unrelated grammar repair can leave empirical evidence NOT CHECKED.

Explicit `--snapshot ID=FILE` mappings check hash/quotation against that export. Source-form anchors
are separate records, not opened or applied here; TeX/literal joining may change source representation.
`--markdown` renders the same report into a new file and refuses overwrite. Configuration has its
own schema/workflow; shared proposals belong to `idus-configure`.
