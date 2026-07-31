"""Small dependency-free JSON Schema subset used by the v0.2 validator."""

from __future__ import annotations

import json
import re
from typing import Any


SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "allOf",
    "const",
    "contains",
    "description",
    "enum",
    "exclusiveMinimum",
    "if",
    "items",
    "maxContains",
    "maxItems",
    "maximum",
    "minContains",
    "minItems",
    "minLength",
    "minProperties",
    "minimum",
    "oneOf",
    "pattern",
    "properties",
    "required",
    "then",
    "title",
    "type",
    "uniqueItems",
}


def resolve_local_ref(root_schema: dict[str, Any], ref: str) -> Any:
    if not ref.startswith("#/"):
        raise ValueError(f"only local schema refs are supported, got {ref!r}")
    value: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        value = value[part]
    return value


def schema_definition_errors(
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(schema) - SUPPORTED_SCHEMA_KEYWORDS)
    if unknown:
        errors.append(f"{path}: unsupported schema keywords {unknown}")
    if "$ref" in schema:
        try:
            resolve_local_ref(root_schema, schema["$ref"])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{path}: unresolved $ref {schema['$ref']!r}: {exc}")
    if "pattern" in schema:
        try:
            re.compile(schema["pattern"])
        except (re.error, TypeError) as exc:
            errors.append(f"{path}: invalid pattern: {exc}")
    for field in ("properties", "$defs"):
        children = schema.get(field, {})
        if isinstance(children, dict):
            for name, child in children.items():
                if isinstance(child, dict):
                    errors.extend(
                        schema_definition_errors(
                            child,
                            root_schema,
                            f"{path}/{field}/{name}",
                        )
                    )
    for field in ("items", "contains", "if", "then"):
        child = schema.get(field)
        if isinstance(child, dict):
            errors.extend(
                schema_definition_errors(child, root_schema, f"{path}/{field}")
            )
    for field in ("allOf", "oneOf"):
        children = schema.get(field, [])
        if isinstance(children, list):
            for index, child in enumerate(children):
                if isinstance(child, dict):
                    errors.extend(
                        schema_definition_errors(
                            child,
                            root_schema,
                            f"{path}/{field}/{index}",
                        )
                    )
    return errors


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return False


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        resolved = resolve_local_ref(root_schema, schema["$ref"])
        errors = schema_errors(value, resolved, root_schema, path)
        siblings = {key: item for key, item in schema.items() if key != "$ref"}
        if siblings:
            errors.extend(schema_errors(value, siblings, root_schema, path))
        return errors

    errors: list[str] = []
    if "type" in schema and not _type_matches(value, schema["type"]):
        return [f"{path}: expected {schema['type']}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is outside the enum")

    for index, child in enumerate(schema.get("allOf", [])):
        errors.extend(schema_errors(value, child, root_schema, f"{path}.allOf[{index}]"))
    if "oneOf" in schema:
        matches = sum(
            not schema_errors(value, child, root_schema, path)
            for child in schema["oneOf"]
        )
        if matches != 1:
            errors.append(f"{path}: expected exactly one oneOf match, got {matches}")
    if "if" in schema and not schema_errors(value, schema["if"], root_schema, path):
        if "then" in schema:
            errors.extend(schema_errors(value, schema["then"], root_schema, path))

    if isinstance(value, dict):
        if len(value) < schema.get("minProperties", 0):
            errors.append(f"{path}: too few properties")
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for extra in sorted(set(value) - set(properties)):
                errors.append(f"{path}: unexpected property {extra!r}")
        for name, child in properties.items():
            if name in value:
                errors.extend(
                    schema_errors(value[name], child, root_schema, f"{path}.{name}")
                )

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: too many items")
        if schema.get("uniqueItems"):
            normalized = [
                json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value
            ]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path}: duplicate array items")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(
                    schema_errors(
                        item,
                        schema["items"],
                        root_schema,
                        f"{path}[{index}]",
                    )
                )
        if isinstance(schema.get("contains"), dict):
            match_count = sum(
                not schema_errors(item, schema["contains"], root_schema, path)
                for item in value
            )
            minimum = schema.get("minContains", 1)
            maximum = schema.get("maxContains")
            if match_count < minimum:
                errors.append(f"{path}: contains matched {match_count}, minimum {minimum}")
            if maximum is not None and match_count > maximum:
                errors.append(f"{path}: contains matched {match_count}, maximum {maximum}")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: string does not match {schema['pattern']!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: number is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: number is above maximum")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: number is not above exclusiveMinimum")
    return errors
