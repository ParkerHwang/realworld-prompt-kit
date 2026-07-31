#!/usr/bin/env python3
"""Flatten the v0.2 Artifact Core into portable prompt-realization rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .validation import (
        DEFAULT_MANIFEST,
        ROOT,
        load_json,
        scenario_paths,
        validate_repository,
    )
except ImportError:  # pragma: no cover - direct script execution
    from validation import (  # type: ignore
        DEFAULT_MANIFEST,
        ROOT,
        load_json,
        scenario_paths,
        validate_repository,
    )


DEFAULT_OUTPUT = ROOT / "build" / "realworld-prompt-kit-v0.2.jsonl"


def flatten(document: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for realization in document["realizations"]:
        rows.append(
            {
                "schema": "realworld-prompt-kit.sample/0.2.0",
                "scenario_id": document["scenario_id"],
                "scenario_revision": document["revision"],
                "scenario_status": document["status"],
                "semantic_group_id": document["semantic_group_id"],
                "title": document["title"],
                "prompt_id": realization["prompt_id"],
                "locale": realization["locale"],
                "form": realization["form"],
                "origin": realization["origin"],
                "features": realization["features"],
                "messages": realization["messages"],
                "task": document["task"],
                "coverage": document["coverage"],
                "assets": document["assets"],
                "artifact_contract": document["artifact_contract"],
                "evaluation": document["evaluation"],
                "human_calibration": document["evaluation"]["human_calibration"],
                "provenance": document["provenance"],
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = validate_repository(args.manifest)
    if not report.ok:
        raise SystemExit("v0.2 validation failed; run tools/artifacts/validate.py")

    manifest = load_json(args.manifest)
    rows: list[dict[str, Any]] = []
    for path in scenario_paths(manifest, ROOT):
        rows.extend(flatten(load_json(path)))

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
    print(f"wrote {len(rows)} v0.2 prompt realizations to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
