"""Check or apply an explicitly approved set of language edits.

    python apply_edits.py <root dir> <edits file> [--mode text|py] [--apply]

The default is a dry run. The UTF-8 edits file contains one or more blocks:

    @@ relative/path/to/file
    <<<
    old text
    ===
    new text
    >>>

Repeat the header for another file; additional <<< blocks may follow the same
header. Delimiter lines are reserved. Blank lines between blocks are allowed.
Paths must resolve to existing files inside root, without absolute paths or '..'.

Old text matches across whitespace. In py mode it also matches joins between
adjacent double-quoted Python string literals. New text is literal SOURCE text:
escape quotes and preserve any necessary source markup yourself. This tool does
not parse prose or decide whether an edit preserves scientific meaning.

All matches are checked against the original files, so dependent or overlapping
edits are rejected. All validation and Python syntax checks finish before writes.
No unrelated string literals are rewrapped. Writes use staged replacements with
rollback on ordinary I/O errors; this is not a crash-safe multi-file transaction.
"""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path, PureWindowsPath

BOUNDS = {
    "text": r"\s+",
    "py": r'(?:\s+|[ \t]+"\r?\n[ \t]*"[ \t]*|"\r?\n[ \t]*"[ \t]+)',
}


def read_edits(path: Path) -> list[tuple[str, str, str]]:
    """Parse the complete file, rejecting every unrecognised or incomplete block."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    edits = []
    name = None
    header_needs_block = False
    index = 0

    def fail(message: str) -> None:
        raise ValueError(f"{path}:{index + 1}: {message}")

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("@@ "):
            if header_needs_block:
                fail("previous file header has no edit block")
            name = line[3:].strip()
            if not name:
                fail("file path is empty")
            header_needs_block = True
            index += 1
            continue
        if line != "<<<" or name is None:
            fail("expected '@@ relative/path' or '<<<' after a file header")
        index += 1
        old_lines = []
        while index < len(lines) and lines[index] != "===":
            if lines[index] in {"<<<", ">>>"} or lines[index].startswith("@@ "):
                fail("expected '===' after old text")
            old_lines.append(lines[index])
            index += 1
        if index == len(lines):
            fail("missing '===' delimiter")
        old = "\n".join(old_lines)
        if not old.strip():
            fail("old text must not be empty or whitespace-only")
        index += 1
        new_lines = []
        while index < len(lines) and lines[index] != ">>>":
            if lines[index] in {"<<<", "==="} or lines[index].startswith("@@ "):
                fail("expected '>>>' after new text")
            new_lines.append(lines[index])
            index += 1
        if index == len(lines):
            fail("missing '>>>' delimiter")
        edits.append((name, old, "\n".join(new_lines)))
        header_needs_block = False
        index += 1
    if header_needs_block:
        fail("file header has no edit block")
    if not edits:
        raise ValueError(f"{path}: no edit blocks found")
    return edits


def target_path(root: Path, name: str) -> Path:
    """Reject path traversal, Windows drive/ADS paths and symlink escapes."""
    portable = PureWindowsPath(name)
    if portable.is_absolute() or portable.drive or portable.root or ":" in name or ".." in portable.parts:
        raise ValueError(f"unsafe path: {name!r}; use a relative path inside root")
    target = (root / Path(*portable.parts)).resolve(strict=True)
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError(f"path is not a file inside root: {name!r}")
    return target


def prepare_edits(root: Path, edits: list[tuple[str, str, str]], mode: str) -> dict[Path, tuple[bytes, bytes]]:
    """Validate the entire batch and return original/proposed byte snapshots."""
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")
    snapshots = {}
    replacements = {}
    seen = set()
    for name, old, new in edits:
        if not old.strip():
            raise ValueError(f"{name}: old text must not be empty or whitespace-only")
        target = target_path(root, name)
        if target not in snapshots:
            raw = target.read_bytes()
            snapshots[target] = (raw, raw.decode("utf-8"))
        raw, text = snapshots[target]
        key = (target, " ".join(old.split()))
        if key in seen:
            raise ValueError(f"{name}: duplicate edit for {old[:100]!r}")
        seen.add(key)
        pattern = BOUNDS[mode].join(re.escape(part) for part in old.split())
        matches = list(re.finditer(pattern, text))
        if len(matches) != 1:
            raise ValueError(f"{name}: {len(matches)} matches (expected exactly 1) for {old[:100]!r}")
        match = matches[0]
        if any(match.start() < end and start < match.end() for start, end, _ in replacements.get(target, [])):
            raise ValueError(f"{name}: overlapping edits; combine them into one block")
        # Keep the source file's existing line-ending convention.
        if "\r\n" in text:
            new = new.replace("\n", "\r\n")
        replacements.setdefault(target, []).append((match.start(), match.end(), new))
    prepared = {}
    for target, spans in replacements.items():
        raw, proposed = snapshots[target]
        for start, end, new in sorted(spans, reverse=True):
            proposed = proposed[:start] + new + proposed[end:]
        encoded = proposed.encode("utf-8")
        if target.suffix.lower() == ".py":
            compile(encoded, str(target), "exec")
        prepared[target] = (raw, encoded)
    return prepared


def write_prepared(prepared: dict[Path, tuple[bytes, bytes]]) -> None:
    """Stage every output before replacing files, rolling back reported failures."""
    staged = {}
    backups = {}
    replaced = []
    try:
        for target, (original, proposed) in prepared.items():
            if target.read_bytes() != original:
                raise ValueError(f"source changed after validation: {target}")
            for data, collection in [(proposed, staged), (original, backups)]:
                with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".proofreading-", delete=False) as stream:
                    temporary = Path(stream.name)
                    collection[target] = temporary
                    stream.write(data)
        for target, (original, _) in prepared.items():
            if target.read_bytes() != original:
                raise ValueError(f"source changed after validation: {target}")
        for target in prepared:
            os.replace(staged[target], target)
            replaced.append(target)
    except (OSError, ValueError):
        rollback_errors = []
        for target in reversed(replaced):
            try:
                os.replace(backups[target], target)
            except OSError as error:
                rollback_errors.append(f"{target}: {error}; original retained at {backups[target]}")
        if rollback_errors:
            # Keep surviving backups for recovery instead of deleting them below.
            backups.clear()
            raise OSError("rollback incomplete: " + "; ".join(rollback_errors))
        raise
    finally:
        for temporary in [*staged.values(), *backups.values()]:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", type=Path)
    parser.add_argument("edits", type=Path)
    parser.add_argument("--mode", choices=BOUNDS, default="text")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--apply", action="store_true", help="write the validated batch")
    action.add_argument("--dry", "--dry-run", action="store_true", help="check only (the default)")
    args = parser.parse_args()
    try:
        edits = read_edits(args.edits)
        prepared = prepare_edits(args.root, edits, args.mode)
        print(f"{len(edits)} edits validated in {len(prepared)} files")
        if not args.apply:
            print("dry run: no files written; use --apply for approved edits")
            return
        write_prepared(prepared)
        for target in prepared:
            print("written", target)
    except (OSError, ValueError, SyntaxError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
