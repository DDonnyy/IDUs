# Project settings

Store scoped profile choices, rules and terms in the selected manuscript workspace's
`.idus/config.json`, outside the installed skill. Read active entries during draft/review and record
its revision. Without settings preserve consistent existing style. Settings do not establish facts,
grant editing permission or override meaning/evidence safeguards.

The [schema](scripts/schemas/config.schema.json) uses contract version `1.0`:

- `revision` increases after each changed save.
- `profile` records spelling, report language, journal, audience and an optional inherited profile.
  Apply only available profile details. Legacy profile identifiers remain parseable; private author
  profiles are not bundled or activated by default.
- `rules` use stable `USR-...` IDs with instruction, context, rationale, source and active/disabled status.
- `lexicon` uses `TERM-...` IDs with expression, action, context, case handling, source and status.
  `prefer` needs a preferred expression; `preserve` and `flag` remain contextual candidates.

## Commands

Resolve helper paths from the actual skill location; Python 3.10+ and the standard library suffice.

```text
python scripts/idus.py config show WORKSPACE
python scripts/idus.py config add-rule WORKSPACE rule.json
python scripts/idus.py config add-term WORKSPACE term.json --apply
python scripts/idus.py config validate WORKSPACE
python scripts/idus.py scan-terms WORKSPACE text-export.txt
```

Mutations preview by default; use `--apply` within existing permission. Use separate update/remove
commands for existing IDs; add never silently replaces. `set-profile` patches profile fields;
`import` restores a valid configuration/backup as a new revision. Previous exact bytes are retained
in `.idus/backups/<sha256>.json`; stale prepared changes are rejected. Saves use a staged replacement,
not a lock against every concurrent editor. Unchanged settings do not increment the revision.
Scans list literal candidates without editing or reliably separating prose, names, quotes and code.

## Compatibility and contributions

A sole legacy `.paperidu/config.json` is read/updated in place with backups there. If both files
exist, choose one and archive the other before writes. For deliberate migration preserve a backup
and move the complete config to `.idus/config.json`. The former CLI name remains a forwarding alias.

Configure only when requested; review/draft do not change settings automatically. From expert
feedback, compare useful patterns with existing IDs and keep private preferences scoped.
Proactively suggest a concrete shared contribution when it adds value; duplicates need a reference
rather than a new rule. Prepare it through `idus-configure`, with semantic
overlap review, scoped provenance and fix/keep examples; public submission needs explicit instruction.
