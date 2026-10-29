# Contributing to IDUs

Use a focused branch/PR from `main`. Original contributions use Apache-2.0; retain attribution
and submit only material you can share. See [GOVERNANCE.md](GOVERNANCE.md) for decisions and
[SECURITY.md](SECURITY.md) for sensitive reports.

For rules/lexicon/profile proposals follow [contributions.md](contributions.md): provide scoped
provenance, semantic overlap comparisons, a fix and a legitimate keep example. Distinguish an
expert's explicit diagnosis from inferred intent. Prefer an existing-ID clarification/example
instead of duplication. Private preferences stay local; do not attach manuscripts or full reviews.

Place proposal JSON in `contributions/proposals/PROP-....json`; it is data, not active guidance.
Run `proposal check FILE --ready` against the current target checkout before submission. Historical
proposals can retain their original fingerprint. Maintainers record accept/request changes/local-only/
duplicate/decline and reasons. Acceptance updates canonical rules, related resources and calibration.

Edit sources rather than generated `skills/`, then run:

```text
python scripts/sync_distribution.py --write
python -m unittest discover -s scripts/tests -v
python scripts/check_repository.py
python scripts/build_release.py
```

Include source and regenerated diffs, actual validation results and unresolved checks. CI establishes
file/contract/package behaviour, not editorial quality. Use examples/regression_cases.md to assess
meaning preservation and false positives when prompts change. See
[maintenance](docs/repository-maintenance.md) for CI/releases/settings.
