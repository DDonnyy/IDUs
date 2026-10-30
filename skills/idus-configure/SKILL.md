---
name: idus-configure
description: "Configure project review rules, terminology and style, or prepare shared-rule proposals from expert linguistic feedback."
---

# Configure IDUs

Maintain only the selected manuscript workspace's settings; keep installed files and manuscripts
unchanged. Use [configuration.md](references/configuration.md) for scoped `USR-...` rules,
`TERM-...` entries, schema, backups and legacy-config handling. Preserve IDs, provenance and unrelated
settings. Terms remain contextual candidates; settings cannot establish facts or grant permission.

For a simple preference, read existing settings and the configuration guide/schema. With expert
edits, assess positive academic patterns as well as slips: record the reader benefit, preserved
meaning and whether the diagnosis is explicit or inferred. Compare the relevant shared
[rules](references/rules.md); distinguish already covered, refinement, new, local and one-off guidance.

When a pattern has wider value, proactively suggest a concrete contribution and explain its value
and overlap. Read [contributions.md](references/contributions.md) before preparing a packet and
compare the full corpus. Prefer an existing-ID refinement/example over duplication; keep private
choices local. Prepare or save within the requested scope; a suggestion does not send a PR.

Resolve `scripts/idus.py` from this skill's actual location. Commands preview by default; use
`--apply` for requested writes within existing permission. See [helper usage](scripts/README.md)
and [examples](examples/configuration/) as needed. Without Python keep a baseline/diff and state
unrun validation. Report path, revision, changed IDs, recovery location and conflicts.

A local proposal is pending maintainers. Sending a reviewed, sanitised PR needs explicit instruction;
reuse permission already given. Do not publish source reviews/configs or start draft/review automatically.
