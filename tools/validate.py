#!/usr/bin/env python3
"""Validate scenario structure, identities, realization pairs, and CB8 coverage."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "v0.1" / "manifest.json"
DEFAULT_V1_MANIFEST = ROOT / "data" / "v1.0" / "manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def scenario_paths(manifest: dict[str, Any], root: Path = ROOT) -> list[Path]:
    pattern = manifest["scenario_glob"]
    return sorted(root.glob(pattern))


def validate_scenario(document: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "schema",
        "scenario_id",
        "revision",
        "status",
        "semantic_group_id",
        "title",
        "task",
        "coverage",
        "realizations",
        "evaluation",
        "provenance",
    }
    missing = sorted(required - document.keys())
    if missing:
        errors.append(f"{path}: missing top-level fields: {', '.join(missing)}")
        return errors

    if document["schema"] != "realworld-prompt-kit.scenario/0.1.0":
        errors.append(f"{path}: unsupported schema {document['schema']!r}")
    if document["provenance"].get("contains_personal_data") is not False:
        errors.append(f"{path}: public scenarios must declare contains_personal_data=false")
    if document["provenance"].get("origin") != "synthetic":
        errors.append(f"{path}: v0.1 public pack only permits synthetic scenario provenance")

    coverage = document["coverage"]
    if coverage.get("block_id") != "office-core-cb8":
        errors.append(f"{path}: unexpected coverage block")
    if not coverage.get("naturalistic_features"):
        errors.append(f"{path}: naturalistic_features must not be empty")

    realizations = document["realizations"]
    expected_pairs = {
        ("ko-KR", "canonical"),
        ("ko-KR", "naturalistic"),
        ("en-US", "canonical"),
        ("en-US", "naturalistic"),
    }
    actual_pairs = {(item.get("locale"), item.get("form")) for item in realizations}
    if actual_pairs != expected_pairs:
        errors.append(
            f"{path}: realization pairs differ from required ko/en canonical/naturalistic set"
        )
    if len(realizations) != 4:
        errors.append(f"{path}: expected exactly four realizations, got {len(realizations)}")

    for item in realizations:
        prompt_id = item.get("prompt_id", "<missing>")
        messages = item.get("messages", [])
        if not messages or not all(message.get("content", "").strip() for message in messages):
            errors.append(f"{path}: {prompt_id} has an empty message")
        form = item.get("form")
        origin = item.get("origin")
        features = item.get("features", [])
        if form == "canonical":
            if origin != "controlled_canonical":
                errors.append(f"{path}: canonical {prompt_id} has wrong origin")
            if features:
                errors.append(f"{path}: canonical {prompt_id} must not claim noise features")
        if form == "naturalistic":
            if origin not in {"synthetic_naturalistic", "rights_cleared_real_derived"}:
                errors.append(f"{path}: naturalistic {prompt_id} has unsupported origin")
            if not features:
                errors.append(f"{path}: naturalistic {prompt_id} needs at least one feature")

    evaluation = document["evaluation"]
    for field in ("response_mode", "invariants", "rubric_dimensions", "failure_signals"):
        if not evaluation.get(field):
            errors.append(f"{path}: evaluation.{field} must not be empty")
    return errors


def validate_pairwise_coverage(
    scenarios: list[dict[str, Any]], manifest: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    factor_levels: dict[str, list[str]] = manifest["coverage_facets"]
    rows = [scenario["coverage"]["facets"] for scenario in scenarios]

    for factor, levels in factor_levels.items():
        observed = {row.get(factor) for row in rows}
        if observed != set(levels):
            errors.append(
                f"coverage: {factor} expected levels {levels}, observed {sorted(observed)}"
            )

    for left, right in itertools.combinations(factor_levels, 2):
        expected = set(itertools.product(factor_levels[left], factor_levels[right]))
        observed = {(row.get(left), row.get(right)) for row in rows}
        if observed != expected:
            missing = sorted(expected - observed)
            errors.append(f"coverage: pair {left} × {right} missing {missing}")
    return errors


def _validate_v0_1_repository(
    manifest_path: Path = DEFAULT_MANIFEST, root: Path = ROOT
) -> list[str]:
    errors: list[str] = []
    manifest = load_json(manifest_path)
    paths = scenario_paths(manifest, root)
    expected_count = manifest["expected_scenarios"]
    if len(paths) != expected_count:
        errors.append(f"manifest: expected {expected_count} scenarios, found {len(paths)}")

    scenarios: list[dict[str, Any]] = []
    scenario_ids: set[str] = set()
    prompt_ids: set[str] = set()
    rows: set[int] = set()

    for path in paths:
        try:
            document = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        scenarios.append(document)
        errors.extend(validate_scenario(document, path))

        scenario_id = document.get("scenario_id")
        if scenario_id in scenario_ids:
            errors.append(f"{path}: duplicate scenario_id {scenario_id}")
        scenario_ids.add(scenario_id)

        row = document.get("coverage", {}).get("row")
        if row in rows:
            errors.append(f"{path}: duplicate coverage row {row}")
        rows.add(row)

        for realization in document.get("realizations", []):
            prompt_id = realization.get("prompt_id")
            if prompt_id in prompt_ids:
                errors.append(f"{path}: duplicate prompt_id {prompt_id}")
            prompt_ids.add(prompt_id)

    if len(scenarios) == expected_count:
        errors.extend(validate_pairwise_coverage(scenarios, manifest))
    return errors


def validate_repository(
    manifest_path: Path = DEFAULT_MANIFEST, root: Path = ROOT
) -> list[str]:
    """Validate either the legacy v0.1 pack or the standalone v1 pack."""
    manifest = load_json(manifest_path)
    if manifest.get("schema") == "realworld-prompt-kit.manifest/1.0.0":
        try:
            from .v1_validation import validate_v1_repository
        except ImportError:  # pragma: no cover - direct script execution
            from v1_validation import validate_v1_repository

        return validate_v1_repository(manifest_path, root).errors
    return _validate_v0_1_repository(manifest_path, root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = load_json(args.manifest)
    if manifest.get("schema") == "realworld-prompt-kit.manifest/1.0.0":
        try:
            from .v1_validation import validate_v1_repository
        except ImportError:  # pragma: no cover - direct script execution
            from v1_validation import validate_v1_repository

        report = validate_v1_repository(args.manifest)
        for warning in report.warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        if report.errors:
            for error in report.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(
            f"validated v1: {report.stats['semantic_scenarios']} semantic scenarios, "
            f"{report.stats['cb8_blocks']} CB8 blocks, "
            f"{report.stats['prompt_realizations']} prompt realizations"
        )
        return 0
    errors = validate_repository(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    paths = scenario_paths(manifest)
    prompt_count = sum(len(load_json(path)["realizations"]) for path in paths)
    print(
        f"validated {len(paths)} semantic scenarios, "
        f"{prompt_count} prompt realizations, and pairwise CB8 coverage"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
