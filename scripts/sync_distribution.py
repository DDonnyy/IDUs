"""Generate or check repository-installable skills/manifests from canonical sources. No Git/network."""

import argparse
import json
import sys
import tempfile
from pathlib import Path, PurePosixPath

import build_release
from schema_validation import read_json

INVENTORY = "generated-distribution.json"
MANIFESTS = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
)


def owned(relative):
    path = PurePosixPath(relative)
    return (
        isinstance(relative, str)
        and "\\" not in relative
        and not path.is_absolute()
        and ".." not in path.parts
        and ":" not in relative
        and (
            relative in MANIFESTS
            or len(path.parts) >= 3
            and path.parts[0] == "skills"
            and path.parts[1] in build_release.SKILLS
        )
    )


def checked_path(root, relative):
    target = root / relative
    if target.is_symlink() or not target.resolve().is_relative_to(root):
        raise ValueError(f"generated path escapes root or is a symlink: {relative}")
    if target.exists() and not target.is_file():
        raise ValueError(f"generated target is not a file: {relative}")
    return target


def sync(root=build_release.ROOT, write=False):
    root = Path(root).resolve(strict=True)
    inventory_path = checked_path(root, INVENTORY)
    previous = read_json(inventory_path) if inventory_path.exists() else {"format_version": 1, "files": {}}
    if (
        set(previous) != {"format_version", "files"}
        or previous["format_version"] != 1
        or not isinstance(previous["files"], dict)
        or any(
            not owned(name) or not isinstance(sha, str) or len(sha) != 64
            for name, sha in previous["files"].items()
        )
    ):
        raise ValueError("invalid generated-file inventory")
    with tempfile.TemporaryDirectory(prefix="idus-sync-") as temporary:
        products = build_release.build_release(root, Path(temporary) / "build")
        plugin = next(path for path in products if path.is_dir())
        payloads = {relative: (plugin / relative).read_bytes() for relative in MANIFESTS}
        for path in (plugin / "skills").rglob("*"):
            if path.is_file():
                payloads[path.relative_to(plugin).as_posix()] = path.read_bytes()
        expected = {relative: build_release.digest(data) for relative, data in sorted(payloads.items())}
        actual_files = {
            path.relative_to(root).as_posix()
            for path in (root / "skills").rglob("*")
            if path.is_file() or path.is_symlink()
        }
        unexpected = actual_files - set(expected) - set(previous["files"])
        if unexpected:
            raise ValueError(
                "unmanaged files in skills/; preserve/move them before regenerating: "
                + ", ".join(sorted(unexpected))
            )
        stale = set(previous["files"]) - set(expected)
        changes = []
        baselines = {}
        for relative in sorted(set(expected) | stale):
            target = checked_path(root, relative)
            before = target.read_bytes() if target.exists() else None
            baselines[relative] = before
            after = payloads.get(relative)
            if before != after:
                if relative not in previous["files"] and before is not None:
                    raise ValueError(f"refusing to overwrite an unowned file: {relative}")
                if (
                    relative in stale
                    and before is not None
                    and build_release.digest(before) != previous["files"][relative]
                ):
                    raise ValueError(f"stale generated file has local changes; preserve it first: {relative}")
                changes.append(relative)
        index = (
            json.dumps({"format_version": 1, "files": expected}, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        old_index = inventory_path.read_bytes() if inventory_path.exists() else None
        if old_index != index:
            changes.append(INVENTORY)
        if changes and not write:
            raise ValueError(
                "generated distribution is stale; run python scripts/sync_distribution.py --write\n"
                + "\n".join(changes)
            )
        if write:
            # Validate every path/collision before touching generated files. No recursive deletion.
            for relative in changes:
                if relative == INVENTORY:
                    continue
                target = checked_path(root, relative)
                current = target.read_bytes() if target.exists() else None
                if current != baselines[relative]:
                    raise ValueError("generated file changed while preparing: " + relative)
                if relative in stale:
                    target.unlink(missing_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(payloads[relative])
            if old_index != index:
                inventory_path.write_bytes(index)
    return len(expected), len(changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="refresh only owned generated files")
    mode.add_argument("--check", action="store_true", help="read-only check (default)")
    args = parser.parse_args()
    try:
        count, changed = sync(write=args.write)
        print(f"Distribution consistent: {count} managed files; {changed} refreshed.")
    except (OSError, ValueError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
