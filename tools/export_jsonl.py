#!/usr/bin/env python3
"""Flatten scenario realizations to portable JSONL rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .validation import DEFAULT_MANIFEST, ROOT, load_json, scenario_paths, validate_repository
except ImportError:  # pragma: no cover - direct script execution
    from validation import validate_repository
    from validation import DEFAULT_MANIFEST, ROOT, load_json, scenario_paths


def flatten(document: dict[str, Any]) -> list[dict[str, Any]]:
    sample_schema = (
        "realworld-prompt-kit.sample/0.1.0"
        if document.get("schema") == "realworld-prompt-kit.scenario/0.1.0"
        else "realworld-prompt-kit.sample/0.1.0"
    )
    rows: list[dict[str, Any]] = []
    for realization in document["realizations"]:
        rows.append(
            {
                "schema": sample_schema,
                "scenario_id": document["scenario_id"],
                "scenario_revision": document["revision"],
                "semantic_group_id": document["semantic_group_id"],
                "prompt_id": realization["prompt_id"],
                "locale": realization["locale"],
                "form": realization["form"],
                "origin": realization["origin"],
                "features": realization["features"],
                "messages": realization["messages"],
                "task": document["task"],
                "coverage": document["coverage"],
                "evaluation": document["evaluation"],
                "provenance": document["provenance"],
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    report = validate_repository(args.manifest)
    if report.errors:
        raise SystemExit("validation failed; run tools/validate.py for details")

    rows: list[dict[str, Any]] = []
    paths = scenario_paths(manifest, ROOT)
    for path in paths:
        rows.extend(flatten(load_json(path)))

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
    print(f"wrote {len(rows)} prompt realizations to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
