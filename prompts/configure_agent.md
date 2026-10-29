# Standalone configuration prompt

Configure IDUs only in the selected manuscript workspace, keeping installed skills and manuscripts
unchanged. Read existing `.idus/config.json`, or a sole legacy `.paperidu/config.json`; report a
conflict if both exist. Infer the target from supplied context; ask only when it cannot be determined.

Turn requested guidance into scoped `USR-...` rules and `TERM-...` lexicon entries with provenance,
context, rationale and active/disabled status. Preserve existing IDs and unrelated settings.
Distinguish correctness, readability and preferences; do not infer a universal rule from one edit,
remove meaning safeguards or treat settings as evidence or permission. Terms remain candidates.

When available, follow [configuration.md](../configuration.md), preview/validate with
`scripts/idus.py config`, and persist requested changes with `--apply` within existing permission.
Use separate add/update/remove operations and retain previous bytes/backups. Without Python retain
a baseline/diff and disclose unrun validation. Report path, revision, changed IDs and unresolved issues.
For shared-rule preparation follow [contributions.md](../contributions.md); do not promote rules
or publish feedback automatically. Configuration does not start drafting or review.
