#!/usr/bin/env python3
"""Command-line entry point for the sole v0.1 release validator."""

from __future__ import annotations

import argparse
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
    parser = argparse.ArgumentParser(description="Validate the realworld-prompt-kit v0.1 release.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

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
