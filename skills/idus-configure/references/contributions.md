# Shared-rule proposals

Suggest a contribution when expert feedback reveals a useful reusable gap, exception or false
positive. Explain its value briefly; do not turn every review into contribution work. Expertise
and repetition are evidence to assess, not proof of a universal rule.

For requested preparation:

1. Compare actual source versions, edits and comments. Distinguish an explicit expert diagnosis
   from an inferred reason; check preserved scientific meaning. A highlight alone is not a diagnosis.
2. Compare existing local guidance and the full canonical corpus: [language](rules.md),
   [structure](academic_writing.md), [evidence](evidence_and_claims.md), [lexicon](lexicon.md),
   [word choice](choosing_words.md), [punctuation](punctuation_and_spelling.md) and [drafting](drafting.md).
   Read meanings and neighbouring rules, not only keyword matches. Check current upstream/open
   proposals when accessible and state when only a local snapshot was available.
3. Classify duplicate/refines/conflicts/related/distinct. Reference a duplicate instead of adding
   it; prefer a narrow existing-ID amendment or calibration example. Keep author/journal preferences
   local/in profiles. Resolve conflicts before exporting a ready proposal.
4. Record scope, rationale, sanitised source interpretation, a fix and a legitimate keep example.
   Use synthetic or shareable excerpts; do not collect full manuscripts, confidential reviews,
   identities or complete project configs. Synthetic examples are not verbatim expert evidence.
5. Validate/export a local packet. Submission needs explicit instruction for the target repository;
   maintainers accept, request changes, retain locally or decline. A proposal never activates itself.

```text
python scripts/idus.py proposal check proposal.json
python scripts/idus.py proposal overlaps proposal.json
python scripts/idus.py proposal check proposal.json --ready
python scripts/idus.py proposal export proposal.json NEW_DIRECTORY
```

The [proposal contract](../scripts/schemas/proposal.schema.json) records `PROP-...`, base version,
existing target IDs, examples, comparisons, corpus fingerprint and sharing declarations. Lexical
search cannot establish semantic novelty. Ready export requires the current local fingerprint/
version and completed reviews; declarations do not prove editorial validity or sharing rights.
Export writes only proposal JSON, PR body and checksums into a new directory. It never attaches
source files, runs Git, submits a PR or edits canonical guidance. Existing destinations are preserved.

If submission is requested, verify the actual upstream/branch, recheck overlap and the exact
sanitised diff, and use a focused fork branch/PR. Honour submission permission already given.
Use the exported body; do not stage an entire manuscript workspace. Missing access leaves a local
packet with a precise limitation. Maintainers preserve IDs/provenance and update canonical rules,
related resources and calibration before release. Full developer workflow:
[CONTRIBUTING.md](https://github.com/DDonnyy/IDUs/blob/main/CONTRIBUTING.md).
