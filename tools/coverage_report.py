#!/usr/bin/env python3
"""Write a machine-readable and human-readable v0.1 coverage report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .validation import DEFAULT_MANIFEST, ROOT, load_json, validate_repository
except ImportError:  # pragma: no cover - direct script execution
    from validation import DEFAULT_MANIFEST, ROOT, load_json, validate_repository


def markdown_report(report: Any, manifest_path: Path) -> str:
    stats = report.stats
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        manifest = {}
    release_evidence = manifest.get("release_evidence", {})
    try:
        manifest_label = str(manifest_path.relative_to(ROOT))
    except ValueError:
        manifest_label = str(manifest_path)
    lines = [
        "# v0.1 Coverage Report",
        "",
        f"- Manifest: `{manifest_label}`",
        f"- Validation: **{'PASS' if report.ok else 'FAIL'}**",
        f"- Manifest status: **`{stats.get('manifest_status', '')}`**",
        f"- Semantic scenarios: **{stats.get('semantic_scenarios', 0)}**",
        f"- CB8 blocks: **{stats.get('cb8_blocks', 0)}**",
        f"- Prompt realizations: **{stats.get('prompt_realizations', 0)}**",
        f"- Broad ratio: **{stats.get('broad_ratio', 0):.1%}**",
        f"- Software + data ratio: **{stats.get('software_data_ratio', 0):.1%}**",
        f"- Scenario statuses: **{', '.join(f'{status}={count}' for status, count in stats.get('status_counts', {}).items()) or 'none'}**",
        "",
        "## Intent quotas",
        "",
        "| Intent | Scenarios |",
        "| --- | ---: |",
    ]
    for intent, count in stats.get("intent_counts", {}).items():
        lines.append(f"| `{intent}` | {count} |")
    lines.extend(["", "## Primary-domain counts", "", "| Domain | Scenarios |", "| --- | ---: |"])
    for domain, count in stats.get("domain_counts", {}).items():
        lines.append(f"| `{domain}` | {count} |")
    lines.extend(["", "## Scenario status distribution", "", "| Status | Scenarios |", "| --- | ---: |"])
    for status, count in stats.get("status_counts", {}).items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Naturalistic profile counts", "", "| Profile | Scenario rows |", "| --- | ---: |"])
    for profile, count in stats.get("profile_counts", {}).items():
        lines.append(f"| `{profile}` | {count} |")
    lines.extend(
        [
            "",
            "## Quality lint",
            "",
            f"- Per-scenario validation errors: {stats.get('scenario_validation_error_count', 0)}",
            f"- Non-transport context retrieval-tail errors: {stats.get('transport_tail_error_count', 0)}",
            f"- Critical numeric/possessive fact errors: {stats.get('critical_fact_error_count', 0)}",
            f"- Similarity warnings: {stats.get('similarity_warning_pairs', 0)} ({stats.get('similarity_warning_fraction', 0):.1%})",
            f"- Similarity failures: {stats.get('similarity_failure_pairs', 0)} ({stats.get('similarity_failure_fraction', 0):.1%})",
            f"- Exact duplicate groups: {stats.get('exact_duplicate_groups', 0)}",
            f"- Normalized duplicate groups: {stats.get('normalized_duplicate_groups', 0)}",
            f"- Semantic title duplicate groups: {stats.get('semantic_title_duplicate_groups', 0)}",
            f"- Semantic goal duplicate groups: {stats.get('semantic_goal_duplicate_groups', 0)}",
            f"- High canonical cross-block similarity pairs: {stats.get('high_similarity_cross_block_pairs', 0)}",
            "",
            "## Exact six-token phrase gate",
            "",
            f"- Metric: `{stats.get('phrase_concentration_metric', '')}`",
            f"- Union denominator: **{stats.get('phrase_scenario_denominator', 0)} semantic scenarios per locale/form**",
            f"- Union violations: **{stats.get('phrase_concentration_violation_count', 0)}**",
            f"- Union review candidates: **{stats.get('phrase_concentration_review_count', 0)}**",
            "",
            "| Partition | Scenarios | Prompt realizations | Phrase violations | Phrase reviews |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for partition_id, partition in stats.get("partition_quality", {}).items():
        lines.append(
            f"| `{partition_id}` | {partition.get('scenario_count', 0)} | "
            f"{partition.get('prompt_realization_count', 0)} | "
            f"{partition.get('phrase_concentration_violation_count', 0)} | "
            f"{partition.get('phrase_concentration_review_count', 0)} |"
        )
    lines.extend(
        [
            "",
            "The scan counts distinct-scenario presence for exact six-token n-grams "
            "independently by locale/form. A longer repeated n-gram is covered by "
            "its six-token prefix; no generic boilerplate is whitelisted.",
            "",
            "OpenSocrates method routing and adapter conformance remain planned, "
            "unpopulated extension suites and receive no broad-core coverage credit.",
            "",
            "## Integration evidence",
            "",
            "Worker source refs and integration-owned corrections are recorded in "
            "the manifest and worker reports; source-reported QA is not substituted "
            "for the independent integration gates.",
            "",
        ]
    )
    for worker_id, evidence in release_evidence.get("worker_sources", {}).items():
        source_sha = evidence.get(
            "source_sha", evidence.get("accepted_integration_base_sha", "")
        )
        lines.append(
            f"- `{worker_id}` source/base `{source_sha}`; "
            f"post-repair errors={evidence.get('integration_post_repair_errors', 'n/a')}; "
            f"overlay=`{evidence.get('integration_overlay_report', '')}`"
        )
        correction_classes = evidence.get("integration_correction_classes", {})
        if correction_classes:
            lines.append(
                "  - B correction ledger: "
                + ", ".join(f"{name}={count}" for name, count in correction_classes.items())
            )
    audit = release_evidence.get("coverage_audit", {})
    if audit:
        lines.append(
            f"- Coverage audit `{audit.get('sha', '')}` is retained as "
            f"`{audit.get('status', '')}` at `{audit.get('report', '')}`."
        )
    lines.extend(
        [
            "",
            "## Block review samples",
            "",
            "The release review samples one scenario from every observed CB8 block. The sampled IDs are recorded in the JSON report for traceability.",
            "",
        ]
    )
    for block_id, block in stats.get("blocks", {}).items():
        lines.append(f"- `{block_id}` → `{block.get('sample_scenario_id', '')}`")
    if report.warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report.warnings)
    if report.errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json-output", type=Path, default=ROOT / "reports" / "coverage" / "coverage.json")
    parser.add_argument("--markdown-output", type=Path, default=ROOT / "reports" / "coverage" / "coverage.md")
    args = parser.parse_args()

    report = validate_repository(args.manifest)
    try:
        manifest_label = str(args.manifest.relative_to(ROOT))
    except ValueError:
        manifest_label = str(args.manifest)
    payload = {
        "schema": "realworld-prompt-kit.coverage-report/0.1.0",
        "manifest": manifest_label,
        "status": "pass" if report.ok else "fail",
        "stats": report.stats,
        "warnings": report.warnings,
        "errors": report.errors,
        "release_evidence": load_json(args.manifest).get("release_evidence", {})
        if args.manifest.exists()
        else {},
    }
    for output in (args.json_output, args.markdown_output):
        output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(markdown_report(report, args.manifest), encoding="utf-8")
    print(f"wrote coverage report to {args.json_output} and {args.markdown_output}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
