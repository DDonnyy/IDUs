"""Standard-library validation for IDUs's bundled JSON contracts.

This implements only the keywords used by the bundled schemas, not a general JSON Schema engine.
Unknown schema keywords fail closed. It neither fetches schemas nor validates scientific meaning.
"""

import json
import math
import re
from pathlib import Path

SCHEMA_DIRECTORY = Path(__file__).resolve().parent / "schemas"
KEYWORDS = {
    "$schema",
    "$defs",
    "$ref",
    "title",
    "description",
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "minItems",
    "uniqueItems",
    "minLength",
    "maxLength",
    "pattern",
    "enum",
    "const",
    "minimum",
}


class ContractError(ValueError):
    """Malformed JSON or an invalid IDUs contract."""


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads(text):
    def invalid_constant(value):
        raise ContractError(f"non-JSON numeric constant: {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ContractError("JSON number exceeds finite runtime range")
        return number

    return json.loads(
        text, object_pairs_hook=_pairs, parse_constant=invalid_constant, parse_float=finite_float
    )


def read_json(path):
    return loads(Path(path).read_text(encoding="utf-8-sig"))


def _check_schema(schema):
    if not isinstance(schema, dict) or set(schema) - KEYWORDS:
        raise ContractError("unsupported keyword or invalid bundled schema")
    for key in ("properties", "$defs"):
        for child in schema.get(key, {}).values():
            _check_schema(child)
    if "items" in schema:
        _check_schema(schema["items"])
    if isinstance(schema.get("additionalProperties"), dict):
        _check_schema(schema["additionalProperties"])


def _is_type(value, name):
    types = {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: type(value) is int
        or (type(value) is float and math.isfinite(value) and value.is_integer()),
        "boolean": lambda: type(value) is bool,
        "null": lambda: value is None,
    }
    if name not in types:
        raise ContractError(f"unsupported bundled schema type: {name}")
    return types[name]()


def _validate(value, schema, root, location):
    def fail(message):
        raise ContractError(f"{location}: {message}")

    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/$defs/"):
            fail("only local definition references are supported")
        definition = reference[len("#/$defs/") :]
        if definition not in root.get("$defs", {}):
            fail(f"unknown definition {definition}")
        _validate(value, root["$defs"][definition], root, location)
    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(value, name) for name in names):
            fail(f"expected {' or '.join(names)}")
    canonical = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if "const" in schema and canonical != json.dumps(schema["const"], sort_keys=True, ensure_ascii=False):
        fail(f"expected constant {schema['const']!r}")
    if "enum" in schema and canonical not in {
        json.dumps(item, sort_keys=True, ensure_ascii=False) for item in schema["enum"]
    }:
        fail(f"expected one of {schema['enum']!r}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                fail(f"missing required field {key}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                _validate(item, properties[key], root, f"{location}.{key}")
            elif schema.get("additionalProperties") is False:
                fail(f"unknown field {key}")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            fail("not enough items")
        if schema.get("uniqueItems"):
            items = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(items)) != len(items):
                fail("duplicate array items")
        for index, item in enumerate(value):
            if "items" in schema:
                _validate(item, schema["items"], root, f"{location}[{index}]")
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", float("inf")):
            fail("string length outside allowed bounds")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            fail(f"does not match {schema['pattern']!r}")
    elif type(value) in {int, float} and value < schema.get("minimum", value):
        fail("integer below minimum")


def validate_contract(value, name):
    if name not in {"config", "request", "report", "proposal"}:
        raise ContractError(f"unknown contract: {name}")
    schema = read_json(SCHEMA_DIRECTORY / f"{name}.schema.json")
    _check_schema(schema)
    _validate(value, schema, schema, name)


def unique_ids(entries, location):
    identifiers = [entry["id"] for entry in entries]
    if len(identifiers) != len(set(identifiers)):
        raise ContractError(f"{location}: duplicate IDs")
