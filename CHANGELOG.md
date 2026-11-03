# Changelog

## Unreleased

- Added formulaic prose patterns FP1–FP9 (dashes as connectors, contrastive framing, clefts, colon
  chains, filler, closing restatements, one-sentence paragraphs, figurative verbs, placeholder
  nouns): draft avoids them, review reports recurring ones as STYLE.
- Added an opt-in strict set, `examples/configuration/formulaic-prose-rules.json`; `add-rule` and
  `add-term` now accept a list of entries and apply all of them or none.
- Added RR1–RR3 for responses to reviewers: verify claims of change against the final manuscript,
  check what a manuscript edit answers, quote the final version.
- Refined B4, A2, C4, D3, G4, RC5, M2, EC2, commas, numbers, wording candidates and calibration from
  a second expert comparison of a whole manuscript; added a revision restraint to L.
- Fixed Unicode output in Windows pipelines for configuration, proposal search, scanners and edit application.
- Excluded ignored local review output and caches from public-document link checks.

## 0.8.0

- Scoped each skill's references, examples and helpers to its task; resources load as needed.
- Condensed writing/review guidance while preserving stable rule IDs, evidence safeguards and provenance.
- Removed private manuscript history, development comparisons and intermediate reports from public content.
- Kept standalone prompts, project configuration compatibility, contribution review and reproducible packaging.
