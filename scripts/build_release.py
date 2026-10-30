"""Build self-contained IDUs plugin/skill archives from an explicit public-resource allowlist."""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/DDonnyy/IDUs"
PUBLIC_NOTICES = ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md")
SKILLS = ("idus-review", "idus-configure", "idus-draft")
DRAFT_CORE = ("drafting.md", "rules.md", "sources.md", "checklists/draft_check.md", "examples/draft_case.md")
DRAFT_ASSETS = ("templates/draft_brief.md", "templates/draft_delivery.md")
RULE_CORE = (
    "rules.md",
    "sources.md",
)
REVIEW_CORE = (*RULE_CORE, "ALGORITHM.md", "configuration.md", "contracts.md", "checklists/final_check.md")
CONFIGURE_CORE = (*RULE_CORE, "configuration.md", "contributions.md", "drafting.md")
CORE = tuple(dict.fromkeys((*REVIEW_CORE, *CONFIGURE_CORE, *DRAFT_CORE)))
COMMON_HELPERS = (
    "idus.py",
    "cli_io.py",
    "paperidu.py",
    "configuration.py",
    "schema_validation.py",
    "README.md",
    "schemas/config.schema.json",
)
REVIEW_HELPERS = (
    *COMMON_HELPERS,
    "apply_edits.py",
    "comma_candidates.py",
    "spelling_pass.py",
    "review_report.py",
    "schemas/request.schema.json",
    "schemas/report.schema.json",
)
CONFIGURE_HELPERS = (*COMMON_HELPERS, "contributions.py", "schemas/proposal.schema.json")
HELPERS = tuple(dict.fromkeys((*REVIEW_HELPERS, *CONFIGURE_HELPERS)))
ASSETS = ("templates/paper_profile.md", "templates/review_report.md", *DRAFT_ASSETS)
REVIEW_EXAMPLES = ("report/request.json", "report/report.json", "report/manuscript.txt")
CONFIGURE_EXAMPLES = (
    "configuration/custom-rule.json",
    "configuration/custom-term.json",
    "configuration/profile.json",
    "configuration/config.json",
    "contributions/proposal.json",
)
EXAMPLES = (*REVIEW_EXAMPLES, *CONFIGURE_EXAMPLES)
HELPER_GUIDES = ("packaging/helpers/idus-review.md.in", "packaging/helpers/idus-configure.md.in")
LINK = re.compile(r"\[([^\]\n]+)\]\((<[^>]+>|[^)\n]+)\)")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_source(root, relative, observed):
    path = root / relative
    if path.is_symlink() or not path.resolve(strict=True).is_relative_to(root) or not path.is_file():
        raise ValueError(f"public resource is not an ordinary file inside source root: {relative}")
    data = path.read_bytes()
    observed[relative] = digest(data)
    if path.suffix in {".md", ".py", ".json", ".in", ".txt"} or path.name in {"VERSION", "LICENSE", "NOTICE"}:
        data = data.replace(b"\r\n", b"\n")
    return data


def _destinations(skill_name):
    if skill_name == "idus-draft":
        core, assets, helpers, examples = DRAFT_CORE, DRAFT_ASSETS, (), ()
    elif skill_name == "idus-review":
        core, assets, helpers, examples = REVIEW_CORE, ASSETS[:2], REVIEW_HELPERS, REVIEW_EXAMPLES
    elif skill_name == "idus-configure":
        core, assets, helpers, examples = CONFIGURE_CORE, (), CONFIGURE_HELPERS, CONFIGURE_EXAMPLES
    else:
        raise ValueError("unknown skill: " + skill_name)
    result = {name: "references/" + name for name in core}
    result.update({name: "assets/" + name for name in assets})
    result.update({"scripts/" + name: "scripts/" + name for name in helpers})
    result.update({"examples/" + name: "examples/" + name for name in examples})
    return result


def rewrite_markdown(body, origin, destination, mapping):
    def rewrite(match):
        label, target = match.groups()
        target = unquote(target.strip("<>"))
        if "://" in target or target.startswith("#"):
            return match.group()
        filename, separator, fragment = target.partition("#")
        normalized = os.path.normpath(os.path.join(os.path.dirname(origin), filename)).replace("\\", "/")
        if normalized.startswith("references/local/") or normalized in {
            "references/local",
            "references/README.md",
        }:
            return f"{label} (local source; not bundled)"
        resolved = mapping.get(normalized)
        if resolved is None:
            prefix = normalized.rstrip("/") + "/"
            options = [
                value[: -len(key[len(prefix) :])].rstrip("/")
                for key, value in mapping.items()
                if key.startswith(prefix)
            ]
            if options and len(set(options)) == 1:
                resolved = options[0]
        if resolved is None:
            raise ValueError(f"unbundled operational link in {origin}: {target}")
        relative = os.path.relpath(resolved, os.path.dirname(destination)).replace("\\", "/")
        return f"[{label}]({relative}{separator}{fragment})"

    return LINK.sub(rewrite, body)


def _put(root, relative, data):
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def _index(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"package path escapes root: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def validate_skill(root):
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (\"[^\n]+\")\n---\n", text)
    if not match or match[1] != root.name or not 1 <= len(match[1]) <= 64 or "--" in match[1]:
        raise ValueError(f"invalid skill metadata: {root}")
    description = json.loads(match[2])  # quoted strings are a YAML-compatible JSON subset
    if not description.strip() or len(description) > 1024:
        raise ValueError("invalid skill description")
    root = root.resolve()
    for path in root.rglob("*.md"):
        body = path.read_text(encoding="utf-8")
        if "\ufffd" in body or body.count("```") % 2:
            raise ValueError(f"invalid text or code fences: {path}")
        if re.search(r"[A-Za-z]:[/\\](?:Users|Downloads)[/\\]", body):
            raise ValueError(f"developer-specific absolute path in {path}")
        for match in LINK.finditer(body):
            target = unquote(match[2].strip("<>"))
            if "://" in target:
                continue
            filename, _, fragment = target.partition("#")
            resolved = (path.parent / filename).resolve() if filename else path
            if not resolved.is_relative_to(root) or not resolved.exists():
                raise ValueError(f"missing or escaping skill link: {path}: {target}")
            if fragment and resolved.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", resolved.read_text(encoding="utf-8"), re.M)
                anchors = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in headings}
                if fragment not in anchors:
                    raise ValueError(f"missing heading anchor: {target}")
    _index(root)


def _zip(root, target):
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def build_release(source_root=ROOT, output_root=None):
    source_root = Path(source_root).resolve(strict=True)
    output_root = Path(output_root or source_root / "dist").resolve()
    observed = {}
    version = read_source(source_root, "VERSION", observed).decode("utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must contain three numeric components")
    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output_root, prefix=".idus-build-") as temporary:
        staging = Path(temporary).resolve()
        plugin = staging / "idus"
        plugin.mkdir()
        identity = {
            "name": "idus",
            "version": version,
            "description": "IDUs — IDU-scientist: academic drafting, manuscript review and expert-informed community rules.",
            "author": {"name": "IDUs contributors"},
            "homepage": REPOSITORY,
            "repository": REPOSITORY,
            "license": "Apache-2.0",
        }
        _put(
            plugin,
            "plugin.json",
            _json({"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", **identity}),
        )
        _put(plugin, ".claude-plugin/plugin.json", _json(identity))
        _put(plugin, ".codex-plugin/plugin.json", _json({**identity, "skills": "./skills/"}))
        _put(
            plugin,
            ".claude-plugin/marketplace.json",
            _json(
                {
                    "name": "idus",
                    "owner": identity["author"],
                    "metadata": {"description": identity["description"], "version": version},
                    "plugins": [{"name": "idus", "source": "./", "description": identity["description"]}],
                }
            ),
        )
        for relative in PUBLIC_NOTICES:
            _put(plugin, relative, read_source(source_root, relative, observed))
        readme = read_source(source_root, "packaging/release-readme.md.in", observed).decode("utf-8")
        _put(plugin, "README.md", readme.replace("{{VERSION}}", version).encode("utf-8"))
        for name in SKILLS:
            mapping = _destinations(name)
            skill = plugin / "skills" / name
            entry = read_source(source_root, f"packaging/skills/{name}/SKILL.md.in", observed)
            _put(skill, "SKILL.md", entry)
            _put(skill, "VERSION", (version + "\n").encode("utf-8"))
            for relative in PUBLIC_NOTICES:
                _put(skill, relative, read_source(source_root, relative, observed))
            for origin, destination in mapping.items():
                actual = f"packaging/helpers/{name}.md.in" if origin == "scripts/README.md" else origin
                data = read_source(source_root, actual, observed)
                if origin.endswith(".md"):
                    body = data.decode("utf-8")
                    data = rewrite_markdown(body, origin, destination, mapping).encode("utf-8")
                _put(skill, destination, data)
            validate_skill(skill)
            _put(
                skill,
                "checksums.json",
                _json({"generator": "idus-build/1", "version": version, "files": _index(skill)}),
            )
        _put(
            plugin,
            "checksums.json",
            _json({"generator": "idus-build/1", "version": version, "files": _index(plugin)}),
        )
        products = [(plugin, output_root / f"idus-{version}")]
        for root, name in [
            (plugin, "idus-plugin"),
            *[(plugin / "skills" / name, name) for name in SKILLS],
        ]:
            archive = staging / f"{name}-{version}.zip"
            _zip(root, archive)
            products.append((archive, output_root / archive.name))
        hashes = {target.name: digest(path.read_bytes()) for path, target in products if path.is_file()}
        checksum_path = staging / f"idus-{version}.sha256"
        checksum_path.write_text(
            "".join(f"{value}  {name}\n" for name, value in sorted(hashes.items())), encoding="utf-8"
        )
        products.append((checksum_path, output_root / checksum_path.name))
        for relative, expected in observed.items():
            if digest((source_root / relative).read_bytes()) != expected:
                raise ValueError(f"source changed while building: {relative}")
        for path, target in products:
            if not target.resolve().is_relative_to(output_root) or target.is_symlink():
                raise ValueError("build output escaped its root")
            if target.exists():
                same = target.is_dir() and path.is_dir() and _index(target) == _index(path)
                same = same or (
                    target.is_file() and path.is_file() and target.read_bytes() == path.read_bytes()
                )
                if not same:
                    raise ValueError(
                        f"immutable release already exists with different content: {target}; choose a new version/output directory"
                    )
        for path, target in products:
            if not target.exists():
                os.replace(path, target)
        return [target for _, target in products]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        for path in build_release(output_root=args.output_dir):
            print(path)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
