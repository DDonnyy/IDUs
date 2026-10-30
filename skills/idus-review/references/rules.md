# Shared writing rules

Draft, review and configure use this single canonical corpus and the same stable rule IDs.
Draft reads the short core and only the definitions needed for its sections; review follows the
relevant detailed checks and calibration. Configure compares candidate guidance with the full
corpus. Source provenance and limits remain in [sources.md](sources.md).

## Shared writing core

- Organise supplied research into question → method → result → bounded interpretation. Use the
  relevant Introduction/Methods/Results functions (IN1–IN7, ME1–ME10, RC1–RC5), without inventing
  research to fill a template. Missing facts stay explicit TODOs in draft or questions in review.
- Make the actor, action, quantity and connection recoverable. Apply the same A1–A3, B1–B4,
  C1–C8 and PA1–PA4 definitions below. A STYLE improvement needs a concrete reader benefit;
  clear prose, useful technical repetition and legitimate ellipsis/voice choices can stay.
- Preserve the scientific proposition: values, units, population, conditions, comparisons,
  negation, uncertainty and work status (A6, E1–E3, EC1–EC10). Fluent wording does not establish
  empirical support. Defined terms, notation and captions retain their actual meaning.
- Apply current scoped preferences and consistent spelling; private past choices are not defaults.
  Use D1–D3, F1–F2, G1–G5 and the punctuation/spelling section when needed.

Read selectively: [language checks](#language-checks), [academic calibration](#academic-readability-calibration),
[section structure](#section-structure-and-coherence), [evidence](#evidence-and-claim-safeguards),
[replacement checks](#choosing-replacement-wording), [wording candidates](#contextual-wording-candidates)
and [punctuation/spelling](#punctuation-and-spelling). The short core routes to these definitions;
it is not a separately maintained set of rules. Detailed review findings belong in the review output.

## Language checks

Use a rule only when its stated problem occurs. Correctness, readability and a selected style
preference are different verdicts. Keep clear prose when the alternative adds no reader benefit.
A grammatical sentence can still merit a readability improvement. Source families and limitations:
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
unestablished ground truth. `Error` is appropriate when a justified reference defines it. In captions,
retain low/high ranks or ratios unless an accuracy criterion is established; preserve which subset
is actually labelled.

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

**C1. Ellipsis.** Restore an omitted subject or verb when it prevents misreading or materially
eases a difficult parallel. Grammatical, immediately recoverable gapping can stay.

**C2. Compression.** Expand wording that hides a relation or comparison; preserve the original
logical connection and scientific content. A grammatical sentence can merit a STYLE proposal
when a more direct subject/action, a named quantity or a clearer parallel gives a concrete reader
benefit. State that benefit and provide the complete replacement; formality alone is insufficient.

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
`higher/lower`, `faster/slower` or a missing condition from proximity alone. Preserve whether a
comparison expresses an inequality or a dependency: `X is less than Y` does not by itself justify
`the greater Y, the smaller X`. Name the scale defined by the supplied equation.

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

Use [punctuation and spelling](#punctuation-and-spelling). Preserve clause scope and list
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

## Academic readability calibration

Synthetic examples. A proposed STYLE change needs the stated reader benefit and preserved meaning;
it does not establish that the grammatical original was an error. Retain a clear alternative.

| Context and input | Possible improvement or keep decision |
|---|---|
| A long group-size sentence: `In the second group, where records are incomplete, there are six sites.` | Consider `The second group, where records are incomplete, includes six sites.` The group becomes the subject; six and the condition remain; C2. |
| A difficult long parallel: `Source A records the entrance, source B the platform on the other side of the station.` | Consider `Source A records the entrance; source B records the platform on the other side of the station.` Repeating the short verb makes both actions explicit; C1/C2. |
| Several lengths compete; supplied notes identify segment length: `The parameter increases with length.` | Consider `The parameter increases with segment length.` Do not choose radius or span from proximity; B1/C2. |
| `There are two limitations.` introduces a clear two-item list. | Keep: a short existential introduction is useful; C2 does not ban there are. |
| Notes establish only `d < (r1+r2)/2`; proposal: `The larger the regions, the closer their centres.` | Reject the new dependency. Write `The centroid distance is less than the mean radius of the two regions.` Keep a comparative correlative when the supplied evidence actually establishes the dependency; C8. |
| A figure labels selected extreme ratios between two estimates, with no ground truth: `The underestimating and overestimating sites are labelled.` | Consider `The sites with the lowest and highest ratios are labelled.` Preserve rank and the selected subset; A4. Keep accuracy language with an explicit justified reference. |

## Section structure and coherence
Use the relevant section, not a compulsory template. Empirical, theoretical, software and review
papers can fulfil the same functions differently. Stable IDs derive from
[S-INTRO](sources.md#s-intro), [S-METHOD](sources.md#s-method) and the scoped feedback in
[S-CUS-R1R3](sources.md#s-cus-r1r3). Teaching examples do not establish scientific facts.

## Introduction

### IN1. Check four rhetorical moves
Identify the topic/problem, relevant research, supported gap and present study. Moves can overlap
or recur; do not impose four headings or a fixed sentence count. Source: S-INTRO, pp. 7–8.

### IN2. Give the general picture before details that depend on it
Provide audience-appropriate context and definitions before relying on them; avoid generic
importance claims and padding. Source: S-INTRO, pp. 3–4.

### IN3. Synthesize the literature around an organising question
Group supplied research by a useful conceptual, methodological or chronological relation. Explain
what the group establishes instead of listing disconnected summaries. Source: S-INTRO, p. 6.

### IN4. Make the gap specific, supported and consequential
Scope the unresolved issue and why it matters. No universal absence/novelty claim without an
adequate literature basis. Source: S-INTRO, p. 13; evidence safeguards: EC7.

### IN5. Connect the aim, research question and objectives to the gap
Make the intended contribution and scope recoverable; do not invent a rationale or objective to
repair a missing link. Source: S-INTRO, pp. 7, 14.

### IN6. Use tense and aspect for the intended time and claim
Distinguish completed work, current knowledge and ongoing relevance. A citation does not force
one tense. Source: S-INTRO, pp. 11–14.

### IN7. Check the Introduction against the Discussion
Trace the promised question/contribution to its actual answer and limitations; revise stale
promises within authorisation. Source: S-INTRO, p. 3; EC9.

## Methods

### ME1. Explain the context, the procedure and the analysis
Make design/material, actual operations and analysis intelligible, including supported reasons
for consequential choices. Source: S-METHOD, pp. 3–7, 11–15.

### ME2. Make the reported procedure transparent and reproducible
Supply enough detail to repeat the reported work; transparency alone does not prove validity.
Source: S-METHOD, p. 2.

### ME3. Identify the study material and its selection
State relevant setting, sampling/selection, exclusions, period and data characteristics. Include
ethics requirements only where applicable and supported. Source: S-METHOD, pp. 5–6, 13.

### ME4. Present steps in a recoverable procedural order
Use chronological or topical organisation with clear dependencies. Source: S-METHOD, pp. 7, 14.

### ME5. Define what is measured and how it is analysed
Specify variables, units, aggregation and reported tests/criteria as needed. Do not invent
analyses or parameters. Source: S-METHOD, pp. 5, 13, 15.

### ME6. Name the tools and the information needed to repeat the work
Include relevant tools/versions, configuration and implementation references when supplied.
Source: S-METHOD, pp. 14–15.

### ME7. Choose tense according to the operation being described
Keep completed procedures, general definitions and planned analyses distinct. Source: S-METHOD, p. 8.

### ME8. Use active or passive voice to identify the right agent and focus
Choose the form that expresses actor and focus clearly; first person and document/model subjects
are legitimate. Source: S-METHOD, pp. 8, 10.

### ME9. Prefer a direct verb when a nominalisation adds no meaning
Consider `We measured X` for empty `We performed a measurement of X`; preserve useful technical
nominalisations. Source: S-METHOD, p. 9.

### ME10. Report missing information without inventing the method
In review, report a gap/question. In draft, mark it with a specific TODO and continue supported
parts. Do not present unperformed work as complete. Source: S-CUS-R1R3; editorial safeguard.

## Paragraphs and connections

### PA1. Give each paragraph a recognisable function
Develop a coherent unit of background, comparison, procedure, finding or interpretation; no
universal sentence-count requirement. Source: S-INTRO, pp. 7–8, 15–16; S-CUS-R1R3.

### PA2. Order information so the next sentence can be understood
Introduce referents before relying on them; put necessary definitions near use. Missing reasoning
cannot be replaced by a cosmetic transition. Source: S-INTRO, pp. 4, 15–16; S-TEACHER.

### PA3. Make the connector match the logic
`Therefore`, `because` and `however` assert different relations. Use them only when supported;
sequence and association do not establish cause. Source: S-INTRO, p. 6; S-TEACHER.

### PA4. Remove avoidable repetition while preserving useful repetition
Remove redundant content while retaining reminders and defined terms that prevent ambiguity.
Source: S-INTRO, pp. 3, 6–8; S-TEACHER.

## Evidence and claim safeguards
Use these checks in drafting and review. Language confidence does not verify the underlying
science. Provenance: [sources.md](sources.md), chiefly S-CUS-R1R3, S-CUS-R2 and S-AUDITS.

## EC1. Preserve the logical content of an edit
Preserve actor, action, negation, quantifier, hedge, time, population, conditions and comparison
direction. Keep meaningful `may`, `approximately` and `to our knowledge` unless a supported content
change is authorised. Watch added exclusivity, priority, causality and undefined tolerances.

## EC2. Give numerical statements their full meaning
Retain value, unit, numerator/denominator, metric direction, population, period/budget, aggregation
and uncertainty. Identify the exact missing condition rather than inferring it from proximity.

## EC3. Keep the direction and criterion of a comparison
Establish what is compared, the baseline and whether higher/lower is better. Without the actual
criterion/data, a neutral-sounding replacement such as `exceeds` may reverse the intended result.

## EC4. Do not turn an aggregate into an individual guarantee
A median ratio of 0.98 does not establish individual errors below 2%, agreement for every case,
or equivalence. Such claims require the corresponding distribution or analysis.

## EC5. Distinguish observation, reference, proxy and truth
A difference between sources is not automatically error against ground truth. Use `accuracy`,
`validation`, `representative` or `robust` only with the meaning and support the study establishes;
retain formally defined metrics and appropriate uses of these terms.

## EC6. Match inference strength to design and analysis
Keep association/causation, prediction/explanation, descriptive comparison/validation and
non-detection/equivalence distinct. Do not invent tests, p-values, intervals, robustness, ethical
approval or randomisation. Planned work remains planned.

## EC7. Attach citations to the claim they support
Check citation scope and source contents when available. Metadata alone cannot establish support.
Never invent a citation, DOI, quote, page or literature gap. State actual retrieval/check scope;
mark missing support rather than manufacturing a plausible reference.

## EC8. Check definitions, equations and implementation references
Check symbol definitions, units, ratio direction, domain restrictions, weights and aggregation.
Prose/formula/code disagreement is substantive: show the conflict and ask which is intended;
a successful build cannot settle it.

## EC9. Trace every promise to a reported result
Map aims → methods → results → conclusions. Scope title/Abstract claims to supported cases and
conditions. Recheck the current version instead of recycling historical audit findings.

## EC10. Separate a missing fact from an editing decision
Use `NEEDS EVIDENCE` for an unavailable factual check and `AUTHOR DECISION` for intended meaning
or a consequential choice. Name the precise missing item. Keep wording and empirical verdicts separate.

## Section checks beyond Introduction and Methods

**RC1. Results:** organise around questions/analyses, define measures and conditions, connect to
tables/figures, retain contradictory subgroups and exploratory status. Combined Results/Discussion
sections are legitimate when appropriate.

**RC2. Discussion:** answer the question, compare with supported prior work, distinguish tested
mechanisms from interpretation, and explain each limitation's consequence without empty reassurance.

**RC3. Conclusion:** give a bounded takeaway supported by the study; introduce no stronger result,
population or recommendation. Do not remove needed findings merely to simplify a sentence.

**RC4. Abstract/title:** represent the actual question, design, result and implication. Keep
conditions needed to interpret headline numbers; use venue constraints only when known.

**RC5. Figures/tables:** compare labels, units, legends, captions and displayed values. Verify plot
definitions from the actual configuration and inspect changed output; extracted text alone is not
visual verification.

## Choosing replacement wording
Choose the smallest wording change that resolves a concrete problem while preserving the claim.
Use [language checks](#language-checks) and [claim safeguards](#evidence-and-claim-safeguards) for the relevant IDs.

1. Identify the intended actor, action, object, referent and measured quantity in the supplied context.
2. Identify an ambiguity, collocation/grammar issue, active preference or concrete readability
   benefit. A grammatical sentence can merit a STYLE proposal: name how the full replacement
   clarifies an action, referent or relation. A listed token or formality alone is insufficient.
3. Check the candidate against definitions, numbers, conditions, comparison direction and uncertainty.
   If intent or support is missing, ask instead of choosing a plausible scientific meaning.
4. Reread the complete sentence and neighbours after combining related replacements. Check clause
   boundaries, syntax and the claimed reader benefit. Preserve useful repetition; do not rotate
   technical terms just for variety.

| Situation | Decision |
|---|---|
| `The model predicts travel time.` | Keep: conventional technical agency |
| `We fitted a model. It predicts travel time.` | Keep: clear reference |
| `The vehicle spends 200 metres accelerating.` | Consider `covers 200 metres while accelerating` |
| `The relation is weak` with no definition of strength | Ask which quantity/criterion is meant |
| `associated with` → `determined` | Reject without causal/deterministic support |
| `may explain` → `explains` | Reject unless an authorised, supported strengthening |

A synonym is not a scientific correction. Source families: S-TEACHER and S-AUDITS in
[sources.md](sources.md); examples here are synthetic calibration cases.

## Contextual wording candidates
Inspect a match in its sentence and scientific context. This is not a banned-word list or a
replacement dictionary. Names, citations, code, quotations and defined terms need protection.
Origins: [S-TEACHER](sources.md#s-teacher) and [S-AUDITS](sources.md#s-audits); the examples below
are generalised editorial illustrations, not assertions about a particular manuscript.

| Candidate | Inspect | Possible clarification, only if meaning matches |
|---|---|---|
| `spends` with a distance | Inappropriate collocation? | `covers … while` |
| `knows`, `decides`, `holds` with data | Is the recorded relation clear? | `records`, `contains`, `estimates` |
| `cost` | Computational cost, distance or measured effect? | Name the actual quantity |
| `sparse` | Defined graph property or little coverage? | Keep technical sparsity; otherwise name coverage |
| `distance`, `intersection`, `boundary` | Technical sense or ordinary meaning? | Specify the intended difference/operation |
| `error`, `accuracy`, `validation` | Justified reference and criterion? | Name the discrepancy/comparison if truth is not established |
| `significant`, `robust`, `representative` | Statistical/empirical support or casual emphasis? | State the supported property |
| `first`, `only`, `all`, `always`, `never` | Priority/exclusivity/universality justified? | Preserve the supported scope |
| `noticeably`, `negligible`, `close` | Defined criterion or tolerance? | Supply the actual criterion, or ask |
| `it`, `this`, `former/latter`, `here/there` | More than one plausible referent? | Name the intended object only when needed |
| `by definition/construction/default` | Definition, built property or selected setting? | Choose the intended relation |
| `replace`, `substitute` | Replacement direction preserved? | State which object replaces which |
| `therefore`, `because`, `however` | Consequence, reason or contrast actually supported? | Use the actual relation or omit the connector |

Keep `The model predicts travel time`, a defined `sparse graph`, and an unambiguous `it`. Do not
change a term solely to obtain fewer dictionary matches. Project lexicon entries retain their own
context, source, ID and active/disabled status.

## Punctuation and spelling
Follow known venue requirements and the selected author profile. Preserve a consistent existing
style when none is specified. Provenance: [S-TEACHER](sources.md#s-teacher); conventions are scoped,
not universal language-error rules.

## Commas

- Preserve the intended scope of restrictive versus non-restrictive clauses; do not change the
  relevant subset merely to enforce a preference for `that` or `which`.
- Use a serial comma when selected or needed for grouping. Two coordinated items/verbs do not
  become a three-item list because another comma appears nearby.
- Assess introductory clauses/phrases by function and ambiguity. No blanket comma after every
  short opener, `So` or `Yet`. An inverted subject is not automatically a detached introduction.
- Separate complex list items with semicolons where useful; retain their logical grouping.

## Dashes and colons

Dashes, parentheses and colons can express different relations and emphasis. Recast only for
clarity or the active style; avoid changing claim scope. An em dash is not an error by itself.

## Spelling variety

Use the selected US, British or Oxford British convention in editable prose. Oxford British can
combine `colour` and `organize`; consistency is contextual, not a global search-and-replace rule.
Keep actual identifiers (`color=`), proper names, published titles, citations and quotations.
Scanners list candidates and cannot reliably distinguish all these cases.

## Numbers

Preserve precision, units, denominators and conditions. Follow known formatting conventions for
percentages, ranges and units without silently rounding or changing the quantity. Check changed
source/output where punctuation, TeX spacing or a caption/header edit can affect rendering.
