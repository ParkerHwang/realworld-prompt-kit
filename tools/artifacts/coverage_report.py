#!/usr/bin/env python3
"""Write the v0.2 release validation and coverage report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .validation import DEFAULT_MANIFEST, ROOT, validate_repository
except ImportError:  # pragma: no cover - direct script execution
    from validation import DEFAULT_MANIFEST, ROOT, validate_repository


DEFAULT_JSON = ROOT / "reports" / "v0.2" / "release-validation.json"
DEFAULT_MARKDOWN = ROOT / "reports" / "v0.2" / "release-validation.md"


def markdown_report(payload: dict[str, Any]) -> str:
    stats = payload["stats"]
    lines = [
        "# v0.2 Artifact Core Release Validation",
        "",
        f"- Validation: **{payload['status'].upper()}**",
        f"- Manifest status: **`{stats.get('manifest_status', '')}`**",
        f"- Semantic scenarios: **{stats.get('semantic_scenarios', 0)}**",
        f"- Prompt realizations: **{stats.get('prompt_realizations', 0)}**",
        f"- Input assets: **{stats.get('input_assets', 0)}**",
        f"- Reference artifacts: **{stats.get('reference_artifacts', 0)}**",
        f"- Reference hard-gate full passes: **{stats.get('reference_full_pass_count', 0)}/{stats.get('reference_result_count', 0)}**",
        "",
        "## Module coverage",
        "",
        "| Module | Episodes |",
        "| --- | ---: |",
    ]
    for name, count in stats.get("module_counts", {}).items():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "## Workflow-job coverage",
            "",
            "| Workflow job | Episodes |",
            "| --- | ---: |",
        ]
    )
    for name, count in stats.get("workflow_job_counts", {}).items():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "## Output artifacts",
            "",
            "| Family | Reference artifacts |",
            "| --- | ---: |",
        ]
    )
    for name, count in stats.get("output_family_counts", {}).items():
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "## Calibration boundary",
            "",
            "- Every public reference passes the executable hard gates and deterministic rubric checks.",
            f"- Human-only rubric items left unscored: **{stats.get('human_unscored_rubric_items', 0)}**.",
            "- Human practitioner calibration, external replication, and a global leaderboard claim remain explicitly false.",
            "- Reference files are conformance fixtures, not byte-for-byte gold answers for model submissions.",
        ]
    )
    if payload["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in payload["warnings"])
    if payload["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in payload["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    report = validate_repository(args.manifest)
    try:
        manifest_label = args.manifest.relative_to(ROOT).as_posix()
    except ValueError:
        manifest_label = str(args.manifest)
    payload = {
        "schema": "realworld-prompt-kit.artifact-release-report/0.2.0",
        "manifest": manifest_label,
        "status": "pass" if report.ok else "fail",
        "stats": report.stats,
        "warnings": report.warnings,
        "errors": report.errors,
        "reference_results": report.reference_results,
    }
    for path in (args.json_output, args.markdown_output):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(markdown_report(payload), encoding="utf-8")
    print(
        f"wrote v0.2 release report to {args.json_output} "
        f"and {args.markdown_output}"
    )
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
