Describe the concrete review problem and the smallest useful change.

- Proposal ID and destination: existing rule refinement, calibration example, new rule, lexicon or profile.
- Provenance: explicit expert comment, inference from an edit, journal requirement or author preference.
- Scope and exceptions; why this belongs in shared guidance.
- Existing rules/proposals compared, relationships and what this adds.
- A fix example and a legitimate no-change example, with sharing basis.
- Validation actually run and checks still pending.

For rule proposals, attach the sanitised proposal JSON under `contributions/proposals/` and use
the generated `PR_BODY.md` as the description if available. Do not attach private manuscripts or
review reports. A proposal PR requests maintainer assessment; it does not establish a new rule.

Maintainers: preserve IDs and provenance, prefer a narrow amendment over a duplicate, and record
accept/request changes/local-only/duplicate/decline with reasons. Accepted guidance needs a patch
to canonical files and calibration before it is included in a release. See [CONTRIBUTING.md](../CONTRIBUTING.md).
