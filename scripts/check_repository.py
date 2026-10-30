"""Read-only public-document/resource checks and generated-distribution consistency."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import build_release
from schema_validation import read_json
from sync_distribution import MANIFESTS, sync

SKIP = {".git", ".config", ".idus", ".paperidu", ".venv", "__pycache__", "dist", "output", "tmp"}


def check(root=build_release.ROOT, release_tag=None):
    root = Path(root).resolve(strict=True)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if release_tag is not None and release_tag != "v" + version:
        raise ValueError("release tag must equal v + VERSION")
    errors = []
    count = 0
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if set(relative.parts) & SKIP or relative.parts[:2] == ("references", "local"):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(f"escaping/symlink Markdown: {relative}")
            continue
        count += 1
        body = path.read_text(encoding="utf-8-sig")
        if "\ufffd" in body or body.count("```") % 2:
            errors.append(f"encoding/code-fence issue: {relative}")
        for match in build_release.LINK.finditer(body):
            target = unquote(match[2].strip("<>"))
            if "://" in target:
                continue
            filename, _, fragment = target.partition("#")
            destination = (path.parent / filename).resolve() if filename else path
            if not destination.is_relative_to(root):
                errors.append(f"escaping link: {relative}: {target}")
                continue
            if destination.is_relative_to(root / "references/local"):
                continue
            if not destination.exists():
                errors.append(f"missing link: {relative}: {target}")
            elif fragment and destination.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(encoding="utf-8-sig"), re.M)
                anchors = {re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-") for text in headings}
                if fragment not in anchors:
                    errors.append(f"missing anchor: {relative}: {target}")
    if errors:
        raise ValueError("\n".join(errors))
    for name in build_release.SKILLS:
        build_release.validate_skill(root / "skills" / name)
    for relative in MANIFESTS:
        read_json(root / relative)
    managed, _ = sync(root)
    print(f"Checked {count} Markdown files and {managed} generated distribution files; version {version}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-tag")
    args = parser.parse_args()
    try:
        check(release_tag=args.release_tag)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
