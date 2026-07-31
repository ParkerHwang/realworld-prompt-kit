#!/usr/bin/env python3
"""Validate the v0.2 Artifact Core calibration release."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .validation import DEFAULT_MANIFEST, validate_repository
except ImportError:  # pragma: no cover - direct script execution
    from validation import DEFAULT_MANIFEST, validate_repository


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    report = validate_repository(args.manifest)
    for error in report.errors:
        print(f"ERROR: {error}")
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    if report.errors:
        return 1
    print(
        "validated v0.2 artifact core: "
        f"{report.stats['semantic_scenarios']} scenarios, "
        f"{report.stats['prompt_realizations']} prompt realizations, "
        f"{report.stats['input_assets']} input assets, "
        f"{report.stats['reference_artifacts']} reference artifacts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
