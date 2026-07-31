#!/usr/bin/env python3
"""Command-line entry point for RealWorld Prompt Kit release validators."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .validation import (
        DEFAULT_MANIFEST,
        ROOT,
        _validate_scenario,
        load_json,
        scenario_paths,
        validate_repository,
    )
except ImportError:  # pragma: no cover - direct script execution
    from validation import (
        DEFAULT_MANIFEST,
        ROOT,
        _validate_scenario,
        load_json,
        scenario_paths,
        validate_repository,
    )


def validate_scenario(
    document: dict,
    path: Path,
    manifest: dict | None = None,
    catalog: dict | None = None,
) -> list[str]:
    """Keep the small validation helper available for downstream callers."""
    active_manifest = manifest or load_json(DEFAULT_MANIFEST)
    active_catalog = catalog or load_json(ROOT / active_manifest["catalog_path"])
    return _validate_scenario(document, path, active_manifest, active_catalog)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a RealWorld Prompt Kit release.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    manifest_header = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest_header.get("schema") == "realworld-prompt-kit.manifest/0.2.0":
        try:
            from artifacts.validation import validate_repository as validate_artifact_release
        except ImportError as exc:  # pragma: no cover - import environment failure
            raise SystemExit(f"cannot load the v0.2 validator: {exc}") from exc
        report = validate_artifact_release(args.manifest)
        if report.errors:
            for error in report.errors:
                print(f"ERROR: {error}")
            return 1
        for warning in report.warnings:
            print(f"WARNING: {warning}")
        print(
            "validated v0.2 artifact core: "
            f"{report.stats.get('semantic_scenarios', 0)} scenarios, "
            f"{report.stats.get('prompt_realizations', 0)} prompt realizations, "
            f"{report.stats.get('input_assets', 0)} input assets, "
            f"{report.stats.get('reference_artifacts', 0)} reference artifacts"
        )
        return 0

    report = validate_repository(args.manifest)
    if report.errors:
        for error in report.errors:
            print(f"ERROR: {error}")
        return 1
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    print(
        "validated v0.1 release: "
        f"{report.stats.get('semantic_scenarios', 0)} semantic scenarios, "
        f"{report.stats.get('prompt_realizations', 0)} prompt realizations, "
        f"{report.stats.get('cb8_blocks', 0)} CB8 blocks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
