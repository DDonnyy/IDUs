"""Project-local, additive IDUs configuration. No manuscript text is modified."""

import copy
import difflib
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

from schema_validation import ContractError, loads, unique_ids, validate_contract


def default_config():
    return {
        "schema_version": "1.0",
        "revision": 0,
        "profile": {"base_profile": None, "spelling": "preserve"},
        "rules": [],
        "lexicon": [],
    }


def validate_config(config):
    validate_contract(config, "config")
    unique_ids(config["rules"], "rules")
    unique_ids(config["lexicon"], "lexicon")
    for entry in [*config["rules"], *config["lexicon"]]:
        if entry["id"] != entry["id"].strip():
            raise ContractError("custom IDs cannot have surrounding whitespace")
    for term in config["lexicon"]:
        if "\n" in term["expression"] or "\r" in term["expression"]:
            raise ContractError("lexicon expressions must fit on one line")
        if term["action"] == "prefer" and term["preferred"] is None:
            raise ContractError(f"{term['id']}: prefer requires a preferred expression")


def target_path(workspace):
    root = Path(workspace).resolve(strict=True)
    if not root.is_dir():
        raise ContractError("workspace must be an existing directory")
    primary = root / ".idus/config.json"
    legacy = root / ".paperidu/config.json"
    for candidate in (primary, legacy):
        if candidate.parent.exists() and not candidate.parent.is_dir():
            raise ContractError(f"{candidate.parent.name} must be a directory")
        if candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
            raise ContractError("configuration path escapes workspace or is a symlink")
        if candidate.exists() and not candidate.is_file():
            raise ContractError("configuration target is not a file")
    if primary.exists() and legacy.exists():
        raise ContractError("both .idus and .paperidu configurations exist; choose one and archive the other")
    target = legacy if legacy.exists() else primary
    return root, target


def load_config(workspace):
    _, target = target_path(workspace)
    raw = target.read_bytes() if target.exists() else None
    config = loads(raw.decode("utf-8-sig")) if raw is not None else default_config()
    validate_config(config)
    return target, raw, config


def prepare_change(workspace, action, value=None, identifier=None):
    target, original, current = load_config(workspace)
    updated = copy.deepcopy(current)
    if action == "init":
        if original is not None:
            raise ContractError("configuration already exists; use set-profile or an entry command")
    elif action == "import":
        validate_config(value)
        updated = copy.deepcopy(value)
        updated["revision"] = current["revision"]
    elif action == "set-profile":
        if not isinstance(value, dict):
            raise ContractError("profile patch must be a JSON object")
        updated["profile"].update(value)
    elif action in {"add-rule", "update-rule", "remove-rule", "add-term", "update-term", "remove-term"}:
        collection = updated["rules" if action.endswith("rule") else "lexicon"]
        if action.startswith("remove"):
            found = [entry for entry in collection if entry["id"] == identifier]
            if not found:
                raise ContractError(f"no custom entry {identifier!r}")
            collection.remove(found[0])
        else:
            if not isinstance(value, dict) or not isinstance(value.get("id"), str):
                raise ContractError("entry must be a JSON object with an id")
            found = [entry for entry in collection if entry["id"] == value["id"]]
            if action.startswith("add") and found:
                raise ContractError(f"custom entry {value['id']} already exists; use update")
            if action.startswith("update") and not found:
                raise ContractError(f"no custom entry {value['id']} to update")
            if found:
                collection[collection.index(found[0])] = copy.deepcopy(value)
            else:
                collection.append(copy.deepcopy(value))
    else:
        raise ContractError(f"unknown configuration action {action}")
    validate_config(updated)
    if original is not None and updated == current:
        return target, original, original
    updated["revision"] = current["revision"] + 1
    proposed = (json.dumps(updated, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return target, original, proposed


def change_diff(target, original, proposed):
    before = original.decode("utf-8-sig").splitlines(keepends=True) if original is not None else []
    after = proposed.decode("utf-8").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(before, after, fromfile=str(target), tofile=str(target) + " (proposed)")
    )


def apply_change(workspace, target, original, proposed):
    root, expected = target_path(workspace)
    if expected != target:
        raise ContractError("configuration target changed")

    def check_current():
        _, checked = target_path(root)
        raw = checked.read_bytes() if checked.exists() else None
        if raw != original:
            raise ContractError("configuration changed after preview; prepare the change again")

    check_current()
    if original == proposed:
        return None
    validate_config(loads(proposed.decode("utf-8")))
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if original is not None:
        digest = hashlib.sha256(original).hexdigest()
        backup = target.parent / "backups" / f"{digest}.json"
        if backup.is_symlink() or not backup.resolve().is_relative_to(root):
            raise ContractError("backup path escapes workspace or is a symlink")
        backup.parent.mkdir(exist_ok=True)
        if backup.exists():
            if backup.read_bytes() != original:
                raise ContractError("existing recovery copy does not match the previous configuration")
        else:
            with backup.open("xb") as stream:
                stream.write(original)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".config-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(proposed)
        check_current()
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return backup


def scan_terms(workspace, files):
    _, _, config = load_config(workspace)
    candidates = []
    for filename in files:
        path = Path(filename)
        text = path.read_text(encoding="utf-8-sig")
        for term in config["lexicon"]:
            if term["status"] != "active":
                continue
            expression = term["expression"]
            left = r"(?<!\w)" if expression[0].isalnum() or expression[0] == "_" else ""
            right = r"(?!\w)" if expression[-1].isalnum() or expression[-1] == "_" else ""
            flags = 0 if term["match_case"] else re.IGNORECASE
            for match in re.finditer(left + re.escape(expression) + right, text, flags):
                before = text[: match.start()]
                candidates.append(
                    {
                        "path": str(path),
                        "line": before.count("\n") + 1,
                        "column": len(before.rsplit("\n", 1)[-1]) + 1,
                        "id": term["id"],
                        "matched": match.group(),
                        "action": term["action"],
                        "preferred": term["preferred"],
                        "context": term["context"],
                    }
                )
    return {
        "configuration_revision": config["revision"],
        "candidates": candidates,
        "notice": "Candidates only; inspect context, names, citations and code. No files were changed.",
    }
