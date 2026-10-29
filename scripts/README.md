# Proofreading helpers

These scripts use only the Python standard library. Run the examples below from
the repository root, replacing the manuscript and review paths with your own.
They assist an already verified review; they cannot decide whether wording keeps
the authors' scientific meaning.

## Configure a project and validate reports

`idus.py` provides configuration and report operations without a model API or server:

```text
python scripts/idus.py --version
python scripts/idus.py config init path/to/manuscript
python scripts/idus.py config add-rule path/to/manuscript rule.json --apply
python scripts/idus.py config add-term path/to/manuscript term.json --apply
python scripts/idus.py scan-terms path/to/manuscript text-export.txt
python scripts/idus.py validate-report report.json --snapshot doc-1=text-export.txt
```

Configuration mutations preview by default; explicit `--apply` persists an authorised change and
retains previous bytes. Existing IDs need an update command. See
[configuration.md](../configuration.md) for the complete workflow and examples. The custom term
scanner is read-only and makes no promise to distinguish every quoted term, name, or code string.

Request/report validation checks structure, relationships and optionally explicitly supplied
snapshot quotations/hashes. It does not open arbitrary source paths from JSON, inspect cited
evidence or decide whether a rewrite preserves meaning. See [contracts.md](../contracts.md).
`--markdown FILE` renders the same report into a new file and refuses to overwrite an existing one.

## Check and apply an edit batch

```text
python scripts/apply_edits.py ROOT EDITS [--mode text|py] [--apply]
```

`ROOT` is the existing directory containing the manuscript sources. `EDITS` is a
UTF-8 file, resolved from the current working directory, with blocks in this exact
format. This illustrative example repairs subject-verb agreement:

```text
@@ main.tex
<<<
The results is shown in Table~1.
===
The results are shown in Table~1.
>>>
```

Paths after `@@ ` are relative to `ROOT`. Add another `@@ relative/path` header to
edit another file, or another `<<<` block under the same header to edit the same
file. Delimiter lines must appear exactly as shown, without indentation. Blank
lines between blocks are allowed. Other notes, comments, incomplete blocks, an
empty old text, and a file header without an edit block are errors. The replacement
may be empty when deletion was explicitly approved.

First validate without writing:

```text
python scripts/apply_edits.py path/to/manuscript review/edits.txt
```

This is a dry run by default. `--dry` and `--dry-run` are optional aliases for the
same behavior. After the batch has been checked and applying it is authorized:

```text
python scripts/apply_edits.py path/to/manuscript review/edits.txt --apply
```

Use `--mode text` (the default) for raw text sources. Whitespace between words in
the old fragment may span multiple spaces or lines in the source. Markup is still
literal: `Table~1` and `Table 1` differ. Matching is case-sensitive and may match
part of a larger word, so use an adequately specific source fragment and review
the resulting diff. The new fragment is inserted literally, with the source's
CRLF convention retained when present.

Use `--mode py` only when manuscript prose is stored in simple adjacent
double-quoted Python string literals. In addition to ordinary whitespace, this
mode can match a line break between literals if there is an actual space or tab
inside at least one of the literals. For example, old `ratio was` can match:

```python
TEXT = (
    "The ratio "
    "was measured."
)
```

It does not match `"ratio"` followed by `"was"`, whose combined string has no word
boundary. This is a limited regex convenience, not a Python prose parser. It does
not decode escape sequences or support every Python string form. For complex
strings, write a source-specific fragment in text mode or use the project's
normal editor. Both old and new fragments must respect the actual source markup;
replacement quotes and backslashes must already be escaped correctly. Every
edited `.py` file is compiled for syntax checking without executing it. This does
not establish that its runtime behavior or scientific content is unchanged.

Before writing, the script checks the complete batch against the original file
snapshots. Every old fragment must match exactly once. Duplicate and overlapping
edits are rejected; an edit cannot depend on another edit's newly inserted text.
Combine dependent changes into one block. Absolute paths, `..`, Windows drive or
stream paths, and resolved paths outside `ROOT` (including escaping symlinks) are
rejected. Targets must be existing UTF-8 files. Unrelated strings are never
rewrapped; the former `--width` option has been removed.

All validation finishes before any source file is replaced. The script stages
all replacements and backup bytes beside the source files, checks for intervening
source changes, and attempts rollback if an ordinary write/replacement error
occurs. A rollback failure reports retained recovery copies. These are individual
filesystem replacements, not a crash-safe multi-file transaction or a lock
against concurrent edits. Keep the manuscript's normal backup/version-control
workflow and check the final diff and build after applying changes.

## Read-only candidate scanners

```text
python scripts/comma_candidates.py FILE [FILE ...]
python scripts/spelling_pass.py FILE [FILE ...] [--stop-at MARKER] [--py-literals-only]
```

Both commands only print candidates and never rewrite input files. Prefer plain
prose exported from the source used by the manuscript build. Feed accepted changes
back through the verified edit batch or the normal source editor.

`comma_candidates.py` looks for possible missing serial commas and introductory
commas. It prints the input path and a candidate sentence index, not a reliable
source line number. Its sentence splitter can misread abbreviations; its patterns
can flag two-item phrases and introductory phrases that already have a valid
comma. Select punctuation conventions in the paper profile, then inspect each
candidate in context. A zero-candidate scan does not prove punctuation is correct.

`spelling_pass.py` lists limited, lowercase candidates for British Oxford spelling
and some associated style choices. Use it only when that variety is selected in
the paper profile. A suggested `licenses` -> `licences` is wrong for a verb;
`meter` may denote an instrument. Every hit needs contextual review. It is not a
complete spellchecker, reference parser, or code/prose classifier.

Simple masks skip single-line backticks, URL patterns, underscore names, and a
small list of phrases in the script. They do not guarantee protection of all
identifiers, names, quotations, reference titles, or code. `--stop-at MARKER`
skips the matching line and everything after it; choose a marker that identifies
the intended boundary. `--py-literals-only` merely selects lines beginning with a
double quote: it can miss prose or include non-prose strings. The former
`--apply` option is deliberately rejected.

## Regression checks

```text
python -m unittest discover -s scripts/tests -v
```

The checks exercise default dry runs, explicit application, late validation
failure without partial writes, unsafe paths, duplicate/overlapping/dependent
edits, ambiguous matches, invalid Python, intervening source changes, rollback on
a locked second file, and read-only scanners. They also check Python literal joins
with and without a real word boundary and a mocked resolved path outside `ROOT`.

The source checkout also tests project configuration, JSON contracts and release packaging.
Helper/scanner tests remain in the source checkout and are excluded from installed skills. A real symlink test may be skipped if Windows does not grant creation
privileges; a mocked resolved-escape check covers the containment decision independently.
## Shared-rule contribution helpers

`idus.py proposal check FILE` validates a proposal's contract and existing target IDs.
`proposal overlaps FILE` lists lexical hints from the full local editorial corpus; the agent must
perform semantic comparison. `proposal check FILE --ready` additionally requires the current
version/fingerprint, reviewed overlap and a sharing declaration. `proposal export FILE NEW_DIR`
creates only the proposal JSON, PR body and checksums; it never runs Git or sends anything.
See [contributions.md](../contributions.md) for expert provenance, counterexamples, limitations,
upstream rechecking and maintainer decisions. Export declarations do not prove rule quality or privacy.


## Repository distribution

`python scripts/sync_distribution.py --write` refreshes owned generated skills/manifests.
`python scripts/check_repository.py` checks links/resources and exact generated consistency.
Both are development helpers, without Git/network actions. See
[repository maintenance](https://github.com/DDonnyy/IDUs/blob/main/docs/repository-maintenance.md).
The previous `scripts/paperidu.py` CLI remains a forwarding alias.
