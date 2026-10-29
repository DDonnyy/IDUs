# Language rules

Use a rule only when its stated problem occurs. Correctness, readability and a selected style
preference are different verdicts. Keep clear prose unchanged. Source families and limitations:
[S-TEACHER](sources.md#s-teacher), [S-CUS-R1R3](sources.md#s-cus-r1r3),
[S-AUDITS](sources.md#s-audits). IDs are stable; historical manuscript choices are not defaults.

## A. Words

**A1. Figurative wording.** Clarify a metaphor when it obscures the measured relation. Conventional
subjects such as `The model predicts` or `This section describes` are valid.

**A2. Technical senses.** Resolve a real ambiguity between ordinary and technical meanings; retain
correct defined terms such as graph sparsity or set intersection.

**A3. Stable terminology.** Use each defined term for the same object. Do not introduce synonyms
that could imply another quantity or method.

**A4. Evaluation versus measurement.** Describe the measured difference without implying an
unestablished ground truth. `Error` is appropriate when a justified reference defines it.

**A5. Idioms.** Replace an idiom only for unclear meaning, unsuitable register or an active style
requirement. Familiar academic expressions are not errors by membership in a list.

**A6. Claim preservation.** Keep negation, quantifiers, uncertainty and scope. Adding `first`,
`only`, `all` or an undefined tolerance requires support; removing `may` can strengthen a claim.

## B. Reference

**B1. Competing referents.** Name the intended referent when two interpretations are plausible.
An ordinary pronoun with one accessible referent can stay; do not guess missing intent.

**B2. Articles and demonstratives.** Check whether `the`, `that` or a shortened noun has an
accessible referent in context; naming it in the same paragraph is not compulsory.

**B3. Paragraph-level reference.** After a long passage, specify what `This` refers to if several
operations or findings could be intended.

**B4. Backward references.** Replace `former/latter`, `here/there` or `one/other` with nouns when
resolving them imposes a real reading cost.

## C. Sentence structure

**C1. Ellipsis.** Restore omitted subjects or verbs only when omission causes misreading.
Grammatical, immediately recoverable gapping can stay.

**C2. Compression.** Expand wording that hides a relation or comparison; preserve the original
logical connection and scientific content.

**C3. Misparsed noun phrases.** Add a relative marker or recast a phrase when its nouns could be
read as a different subject or verb.

**C4. Absolute constructions.** Use a finite clause if an absolute construction overloads the
sentence or leaves its actor uncertain.

**C5. Apposition.** Move or separate an apposition when it resembles another list item or creates
uncertain attachment.

**C6. Inversion and clefts.** Simplify only for a demonstrated reading problem or selected style.
Preserve conditional force and do not add exclusivity.

**C7. Qualifier placement.** Put a qualifier near the quantity/action it modifies; remove emphasis
only when it carries no needed meaning.

**C8. Comparisons.** State comparable quantities, direction and baseline clearly. Do not choose
`higher/lower`, `faster/slower` or a missing condition from proximity alone.

**C9. Openers and first person.** Judge function and active style. `And`, `Yet`, first person and
passive voice are not automatic errors; changing a connector may change the argument.

**C10. Opening appositions.** Recast an opener if it reads as a second subject or attaches to the
wrong actor.

**C11. Paragraph length.** Merge or develop a paragraph when its argument is detached or incomplete.
A short paragraph with a clear function may stand alone.

## D. Notation

**D1. Symbols.** Introduce symbols before use and keep their grammar/definitions consistent.
`Let X be`, `Define X as` and `X denotes` are legitimate alternatives.

**D2. Named quantities.** Name the ratio or quantity before using it, especially where several
estimates compete.

**D3. Threshold statements.** Identify which quantity is above/below a threshold; avoid wording
that could be read as a location in the document.

## E. Precision

**E1. Numerical conditions.** Make units, population, time budget, radius or other necessary
conditions recoverable from the sentence/context; never invent the missing condition.

**E2. Definitions and defaults.** Distinguish `by definition` (a definition), `by construction`
(a property of how something is built) and `by default` (a selected setting).

**E3. Replacement direction.** `A is substituted for B` means A replaces B. Verify direction
before suggesting either `replace` or `is replaced by`.

## F. Names

**F1. Identification.** Disambiguate names for the audience when needed. Follow supplied naming
requirements; do not infer spelling, administrative status or country from memory.

**F2. Complex lists.** Consider semicolons when list items contain their own commas or clauses.
Preserve grouping.

## G. Captions and headers

**G1. Caption function.** Name what is shown, the relevant comparison and panel labels clearly.

**G2. Caption reference.** Specify the object of `the study` or similar wording only if unclear.

**G3. Plot definitions.** Describe the actual plot implementation. An IQR cutoff and the last
observation within it are different; inspect code/configuration before asserting whisker endpoints.

**G4. Header consistency.** Use the same term for the same quantity in text, tables and captions.
Update dependent source keys if an authorised header change requires them.

**G5. Informative headers.** Name column contents without unnecessary caption duplication; inspect
rendered layout after changes that can alter widths.

## H. Punctuation

Use [punctuation_and_spelling.md](punctuation_and_spelling.md). Preserve clause scope and list
grouping; serial commas and dash styles depend on the selected convention.

## I. Spelling

Follow the selected variety consistently in prose. Protect identifiers, names, titles and quotes.

## K. Author and journal preferences

Apply only the current, explicitly scoped profile. A preference is not a universal language error
and cannot override scientific meaning or evidence requirements.

## M. Whole sections

**M1. Abstract clarity.** Explain what the study does and finds in language the target audience
can understand, without promises stronger than the supplied work.

**M2. Limitations.** Give each distinct limitation and its interpretive consequence. Avoid empty
repetition, but retain necessary qualifications and recheck whether a limitation is still current.

**M3. Submission notes.** Remove identified internal editorial notes only within authorised
submission cleanup. TeX comments and escaped percent signs can affect output; never delete all `%`.

**M4. Conclusion focus.** Give a sentence a manageable point while preserving needed findings,
conditions and uncertainty. Numerical limits per sentence are style choices, not general rules.

## L. What not to change

Protect defined terms, numerical content, equations, citations, names and code identifiers.
Respect accepted human edits unless a specific error/conflict is demonstrated. Report scientific
discrepancies separately from wording. No edit quota or inference of AI authorship applies.

## Minimal calibration

| Input/proposal | Decision |
|---|---|
| `The model predicts travel time.` | Keep: conventional technical agency; A1 |
| `We fitted a model. It predicts travel time.` | Keep: accessible referent; B1 |
| `The vehicle spends 200 metres accelerating.` | Consider `covers 200 metres while accelerating`; A1 |
| `Every study we know of` → `Every known study` | Reject: removes the authors' knowledge limit; A6 |
| `The relations are missing` → `Only the relations are missing` | Reject without support: adds exclusivity; A6 |
