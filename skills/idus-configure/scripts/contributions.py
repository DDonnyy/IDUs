"""Local proposal checks and export. No network, Git, manuscript edits or automatic promotion."""

import hashlib
import json
import re
from pathlib import Path

from schema_validation import ContractError, validate_contract

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
CORPUS_FILES = (
    "rules.md",
    "drafting.md",
)
RULE_START = re.compile(r"^(?:#{2,3}\s+|\*\*)([A-Z]+[0-9]+)\.\s+", re.M)
SECTION_START = re.compile(r"^#{1,3}\s+", re.M)


def corpus(root=PACKAGE_ROOT):
    """Index the exact installed/source corpus; digest is independent of absolute location."""
    root = Path(root).resolve(strict=True)
    reference = root if (root / "rules.md").is_file() else root / "references"
    hasher = hashlib.sha256()
    entries = []
    ids = set()
    for relative in CORPUS_FILES:
        path = reference / relative
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(root):
            raise ContractError(f"corpus resource escapes toolkit: {relative}")
        data = path.read_bytes()
        # Length-prefixed labels and content make the digest unambiguous.
        for part in (relative.encode("utf-8"), data):
            hasher.update(len(part).to_bytes(8, "big"))
            hasher.update(part)
        text = data.decode("utf-8-sig")
        markers = {match.start(): None for match in SECTION_START.finditer(text)}
        markers.update({match.start(): match[1] for match in RULE_START.finditer(text)})
        markers.setdefault(0, None)
        positions = sorted(markers)
        for start, end in zip(positions, positions[1:] + [len(text)]):
            identifier = markers[start]
            if identifier:
                if identifier in ids:
                    raise ContractError(f"duplicate built-in rule ID: {identifier}")
                ids.add(identifier)
            body = text[start:end].strip()
            if body:
                entries.append(
                    {
                        "rule_id": identifier,
                        "resource": relative,
                        "line": text[:start].count("\n") + 1,
                        "text": body,
                    }
                )
    return {
        "sha256": hasher.hexdigest(),
        "resources": list(CORPUS_FILES),
        "rule_ids": sorted(ids),
        "entries": entries,
    }


def overlap_candidates(proposal, root=PACKAGE_ROOT):
    """Lexical recall aid only: an empty list cannot establish semantic novelty."""
    validate_contract(proposal, "proposal")
    index = corpus(root)
    query = " ".join(proposal[key] for key in ("title", "instruction", "scope", "rationale"))
    tokens = set(re.findall(r"[a-z]{4,}", query.lower()))
    tokens -= {"that", "this", "with", "from", "when", "rule", "text", "must", "should", "only", "than"}
    candidates = []
    for entry in index["entries"]:
        matched = tokens & set(re.findall(r"[a-z]{4,}", entry["text"].lower()))
        if matched or entry["rule_id"] in proposal["target_ids"]:
            candidates.append({**entry, "matched_tokens": sorted(matched), "score": len(matched)})
    candidates.sort(key=lambda entry: (-entry["score"], entry["resource"], entry["line"]))
    return {
        "corpus_sha256": index["sha256"],
        "resources": index["resources"],
        "candidates": candidates,
        "notice": "Lexical hints only. Read the whole corpus, including non-ID guidance; no absence-of-overlap verdict.",
    }


def validate_proposal(proposal, root=PACKAGE_ROOT, ready=False):
    validate_contract(proposal, "proposal")
    index = corpus(root)
    version = (Path(root) / "VERSION").read_text(encoding="utf-8").strip()
    target_ids = set(proposal["target_ids"])
    comparisons = proposal["overlap_review"]["comparisons"]
    compared_ids = [item["rule_id"] for item in comparisons]
    if len(compared_ids) != len(set(compared_ids)):
        raise ContractError("one overlap comparison per existing rule ID is required")
    if (target_ids | set(compared_ids)) - set(index["rule_ids"]):
        raise ContractError("unknown existing rule ID; check the selected toolkit version")
    if proposal["change"] == "refine_rule" and not target_ids:
        raise ContractError("refine_rule requires existing target_ids; preserve those IDs")
    if proposal["change"] != "refine_rule" and target_ids:
        raise ContractError("only refine_rule uses target_ids")
    for example in proposal["examples"]:
        if example["original"] == example["proposed"]:
            raise ContractError(
                "positive example must demonstrate a change; use counterexamples for keep cases"
            )
    if ready:
        if proposal["base_version"] != version:
            raise ContractError("proposal base_version is stale; compare against the current target version")
        review = proposal["overlap_review"]
        if review["status"] != "reviewed" or review["corpus_sha256"] != index["sha256"]:
            raise ContractError("complete semantic overlap review against the current corpus before export")
        if proposal["privacy"]["status"] != "safe_to_share":
            raise ContractError("review sharing rights and sanitise material before export")
        if any(item["relationship"] == "duplicate" for item in comparisons):
            raise ContractError(
                "duplicate proposal: reference the existing rule or describe a distinct refinement"
            )
        if any(item["relationship"] == "conflicts" for item in comparisons):
            raise ContractError(
                "resolve conflicting guidance before export; maintainer discussion can stay local"
            )
        refinements = {item["rule_id"] for item in comparisons if item["relationship"] == "refines"}
        if refinements != target_ids:
            raise ContractError(
                "each refined rule needs a refines comparison; choose refine_rule for overlapping refinements"
            )
    return {
        "id": proposal["id"],
        "ready_for_export": ready,
        "corpus_sha256": index["sha256"],
        "notice": "Structure and declarations checked; editorial validity, privacy and novelty need human review.",
    }


def _block(text):
    longest = max((len(item) for item in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def render_proposal(proposal):
    lines = [
        f"# {proposal['id']}: {proposal['title']}",
        "",
        "Proposed guidance; maintainer acceptance pending.",
        "",
        f"Change: {proposal['change']}; base version: {proposal['base_version']}",
        "Targets: " + (", ".join(proposal["target_ids"]) or "maintainer to select destination/ID"),
        "",
        "## Proposed guidance",
        "",
        proposal["instruction"],
        "",
        "Scope: " + proposal["scope"],
        "",
        "Rationale: " + proposal["rationale"],
        "",
        "## Provenance",
        "",
    ]
    for source in proposal["sources"]:
        lines.append(f"- {source['kind']} / {source['interpretation']}: {source['reference']}")
    lines += ["", "## Fix examples", ""]
    for item in proposal["examples"]:
        lines += [
            item["context"],
            "",
            "Original:",
            _block(item["original"]),
            "Proposed:",
            _block(item["proposed"]),
            item["reason"],
            "Sharing basis: " + item["sharing_basis"],
            "",
        ]
    lines += ["## Keep examples", ""]
    for item in proposal["counterexamples"]:
        lines += [
            item["context"],
            _block(item["text"]),
            item["why_keep"],
            "Sharing basis: " + item["sharing_basis"],
            "",
        ]
    lines += [
        "## Overlap review",
        "",
        proposal["overlap_review"]["summary"],
        "Corpus SHA-256: " + str(proposal["overlap_review"]["corpus_sha256"]),
        "",
    ]
    for item in proposal["overlap_review"]["comparisons"]:
        lines.append(f"- {item['rule_id']}: {item['relationship']} — {item['reason']}")
    lines += [
        "",
        "## Sharing review",
        "",
        proposal["privacy"]["note"],
        "",
        "## Maintainer review",
        "",
        "- [ ] Confirm diagnosis and source interpretation; expert edits are not automatically correct.",
        "- [ ] Recheck overlap against current upstream, including open proposals and recent decisions.",
        "- [ ] Prefer a scoped amendment/example over a duplicate rule; preserve existing IDs and exceptions.",
        "- [ ] Check fix/keep cases for meaning, uncertainty and over-editing; inspect sharing rights.",
        "- [ ] Accept, request changes, retain as local/profile guidance, or decline with a reason.",
        "- [ ] If accepted, update canonical guidance, provenance, prompts/checklists and calibration together.",
        "",
    ]
    return "\n".join(lines)


def export_proposal(proposal, output, root=PACKAGE_ROOT):
    """Export only declared shareable fields; never collect attachments, config or manuscript files."""
    result = validate_proposal(proposal, root, ready=True)
    output = Path(output).absolute()
    # An existing directory/file, including an empty directory or symlink, must never be replaced.
    if output.exists() or output.is_symlink():
        raise ContractError("export destination already exists; choose a new directory")
    payloads = {
        "proposal.json": (json.dumps(proposal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        "PR_BODY.md": render_proposal(proposal).encode("utf-8"),
    }
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}
    payloads["checksums.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    output.mkdir(parents=True, exist_ok=False)
    # Failures can leave a partial new export. Do not erase anything; retry at a new destination.
    for name, data in payloads.items():
        with (output / name).open("xb") as stream:
            stream.write(data)
    return {**result, "output": str(output), "files": list(payloads), "published": False}
