#!/usr/bin/env python3
"""Create the integration review record for one sample from every v1 block."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path
from typing import Any

try:
    from .v1_validation import (
        DEFAULT_V1_MANIFEST,
        ROOT,
        _naturalistic_feature_errors,
        _validate_v1_scenario,
        load_json,
        normalize_text,
        realization_text,
        scenario_paths,
        validate_v1_repository,
    )
except ImportError:  # pragma: no cover - direct script execution
    from v1_validation import (
        DEFAULT_V1_MANIFEST,
        ROOT,
        _naturalistic_feature_errors,
        _validate_v1_scenario,
        load_json,
        normalize_text,
        realization_text,
        scenario_paths,
        validate_v1_repository,
    )


REVIEW_DATE = "2026-07-27"


def _markdown_excerpt(value: str) -> str:
    return value.strip().replace("\n", " / ").replace("`", "'")


def _sample_review(
    document: dict[str, Any],
    path: Path,
    manifest: dict[str, Any],
    catalog: dict[str, Any],
) -> dict[str, Any]:
    coverage = document.get("coverage", {})
    task = document.get("task", {})
    title = document.get("title", {})
    goal = task.get("user_goal", {})
    evaluation = document.get("evaluation", {})
    block_id = str(coverage.get("block_id", ""))
    intent = block_id.split(".", 1)[0]
    realizations = {
        (item.get("locale"), item.get("form")): item
        for item in document.get("realizations", [])
        if isinstance(item, dict)
    }

    semantic_checks = {
        "intent_matches_block": intent == task.get("primary_intent"),
        "row_is_one_based": coverage.get("row") in range(1, 9),
        "localized_title_present": bool(str(title.get("ko", "")).strip() and str(title.get("en", "")).strip()),
        "localized_goal_present": bool(str(goal.get("ko", "")).strip() and str(goal.get("en", "")).strip()),
        "expected_artifact_present": bool(str(task.get("expected_artifact", "")).strip()),
        "primary_domain_present": bool(str(task.get("primary_domain", "")).strip()),
    }

    similarity: dict[str, float] = {}
    naturalistic_checks = {
        "four_required_pairs": set(realizations) == {
            ("ko-KR", "canonical"),
            ("ko-KR", "naturalistic"),
            ("en-US", "canonical"),
            ("en-US", "naturalistic"),
        },
        "features_match_coverage": True,
        "localized_language_present": True,
        "minimum_substance": True,
        "response_mode_contract": isinstance(evaluation.get("response_mode"), dict)
        and bool(evaluation.get("response_mode", {}).get("canonical"))
        and bool(evaluation.get("response_mode", {}).get("naturalistic")),
        "behavior_boundary": True,
    }
    response_modes = evaluation.get("response_mode", {})
    if response_modes.get("naturalistic") == "refuse_or_escalate":
        behavior_text = " ".join(
            [
                str(title.get("ko", "")),
                str(title.get("en", "")),
                str(goal.get("ko", "")),
                str(goal.get("en", "")),
                str(task.get("expected_artifact", "")),
            ]
        ).casefold()
        risk_markers = (
            r"self[- ]?harm|suicid|immediate danger|abuse|harass|panic|emergency|"
            r"crisis|diagnos|prescri|medical appointment|safety concern|긴급|위험|"
            r"자해|자살|학대|괴롭힘|공황|응급|진단|처방|안전 우려"
        )
        naturalistic_checks["behavior_boundary"] = bool(re.search(risk_markers, behavior_text))
    declared_profiles = set(coverage.get("naturalistic_features", []))
    for (locale, form), realization in realizations.items():
        text = realization_text(realization)
        naturalistic_checks["minimum_substance"] &= len(text) >= 40
        if locale == "ko-KR":
            naturalistic_checks["localized_language_present"] &= bool(re.search(r"[가-힣]", text))
        if locale == "en-US":
            naturalistic_checks["localized_language_present"] &= bool(re.search(r"[A-Za-z]", text))
        if form == "naturalistic":
            naturalistic_checks["features_match_coverage"] &= set(realization.get("features", [])) == declared_profiles
    for locale in ("ko-KR", "en-US"):
        canonical = realizations.get((locale, "canonical"))
        naturalistic = realizations.get((locale, "naturalistic"))
        if canonical and naturalistic:
            similarity[locale] = round(
                difflib.SequenceMatcher(
                    None,
                    normalize_text(realization_text(canonical)),
                    normalize_text(realization_text(naturalistic)),
                ).ratio(),
                4,
            )

    feature_errors = _naturalistic_feature_errors(document, path, manifest)
    scenario_validation_errors = _validate_v1_scenario(document, path, manifest, catalog)
    semantic_fit = all(semantic_checks.values())
    naturalistic_realism = all(naturalistic_checks.values()) and not feature_errors and all(
        score < 0.85 for score in similarity.values()
    ) and not scenario_validation_errors
    prompt_evidence = {
        f"{locale}/{form}": realization_text(realization)[:320]
        for (locale, form), realization in realizations.items()
    }
    return {
        "path": str(path),
        "scenario_id": document.get("scenario_id"),
        "semantic_group_id": document.get("semantic_group_id"),
        "block_id": block_id,
        "row": coverage.get("row"),
        "primary_intent": task.get("primary_intent"),
        "primary_domain": task.get("primary_domain"),
        "scenario_status": document.get("status"),
        "title_en": title.get("en"),
        "goal_en": goal.get("en"),
        "expected_artifact": task.get("expected_artifact"),
        "response_mode": response_modes,
        "prompt_evidence": prompt_evidence,
        "declared_profiles": sorted(declared_profiles),
        "semantic_checks": semantic_checks,
        "naturalistic_checks": naturalistic_checks,
        "naturalistic_feature_errors": feature_errors,
        "scenario_validation_errors": scenario_validation_errors,
        "canonical_naturalistic_similarity": similarity,
        "semantic_fit": "pass" if semantic_fit else "fail",
        "naturalistic_realism": "pass" if naturalistic_realism else "fail",
        "reviewed_by": "release-integrator",
        "reviewed_at": REVIEW_DATE,
    }


def build_review(manifest_path: Path = DEFAULT_V1_MANIFEST, root: Path = ROOT) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    catalog = load_json(root / manifest["catalog_path"])
    grouped: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for path in scenario_paths(manifest, root):
        document = load_json(path)
        block_id = str(document.get("coverage", {}).get("block_id", ""))
        grouped.setdefault(block_id, []).append((path, document))

    samples = []
    for block_id, rows in sorted(grouped.items()):
        path, document = min(rows, key=lambda pair: int(pair[1].get("coverage", {}).get("row", 99)))
        samples.append(_sample_review(document, path.relative_to(root), manifest, catalog))

    validation = validate_v1_repository(manifest_path, root)
    try:
        manifest_label = str(manifest_path.relative_to(root))
    except ValueError:
        manifest_label = str(manifest_path)
    failed_samples = [
        sample
        for sample in samples
        if sample["semantic_fit"] != "pass" or sample["naturalistic_realism"] != "pass"
    ]
    return {
        "schema": "realworld-prompt-kit.review-report/1.0.0",
        "reviewed_at": REVIEW_DATE,
        "reviewer": "release-integrator",
        "review_method": "one row-1-or-lowest-row sample per declared CB8 block; objective checks plus recorded text evidence",
        "manifest": manifest_label,
        "validation_status": "pass" if validation.ok else "fail",
        "validation_error_count": len(validation.errors),
        "scenario_status_counts": validation.stats.get("status_counts", {}),
        "block_count": len(samples),
        "sample_count": len(samples),
        "failed_sample_count": len(failed_samples),
        "samples": samples,
        "planned_extensions_reviewed": False,
        "planned_extensions_note": "OpenSocrates method-routing and adapter-conformance extensions remain unpopulated and receive no broad-core review credit.",
    }


def markdown_review(payload: dict[str, Any]) -> str:
    lines = [
        "# v1 Scenario Review",
        "",
        f"- Reviewed at: **{payload['reviewed_at']}**",
        f"- Reviewer: **{payload['reviewer']}**",
        f"- Validation status at review: **{payload['validation_status'].upper()}**",
        f"- Blocks sampled: **{payload['sample_count']} / {payload['block_count']}**",
        f"- Failed samples: **{payload['failed_sample_count']}**",
        "",
        payload["review_method"],
        "The sample includes the English title, goal, artifact, declared profiles, "
        "and objective evidence outcomes so that semantic fit and naturalistic "
        "realism can be audited without treating a block label as semantic breadth.",
        "",
        "| Block | Scenario | Status | Domain | Semantic fit | Naturalistic realism | KO sim | EN sim |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for sample in payload["samples"]:
        similarity = sample["canonical_naturalistic_similarity"]
        lines.append(
            f"| `{sample['block_id']}` | `{sample['scenario_id']}` | `{sample['scenario_status']}` | "
            f"`{sample['primary_domain']}` | {sample['semantic_fit']} | "
            f"{sample['naturalistic_realism']} | {similarity.get('ko-KR', '')} | {similarity.get('en-US', '')} |"
        )
    lines.extend([
        "",
        "## Review evidence",
        "",
    ])
    for sample in payload["samples"]:
        lines.extend([
            f"### `{sample['block_id']}` / `{sample['scenario_id']}`",
            "",
            f"- English title: {sample['title_en']}",
            f"- English goal: {sample['goal_en']}",
            f"- Expected artifact: {sample['expected_artifact']}",
            f"- Profiles: {', '.join(sample['declared_profiles'])}",
            "- Prompt evidence excerpts:",
            *[
                f"  - `{key}`: {_markdown_excerpt(value)}"
                for key, value in sorted(sample["prompt_evidence"].items())
            ],
            f"- Semantic checks: `{json.dumps(sample['semantic_checks'], sort_keys=True)}`",
            f"- Naturalistic checks: `{json.dumps(sample['naturalistic_checks'], sort_keys=True)}`",
            f"- Feature errors: `{json.dumps(sample['naturalistic_feature_errors'], ensure_ascii=False)}`",
            f"- Full scenario validation errors: `{json.dumps(sample['scenario_validation_errors'], ensure_ascii=False)}`",
            "",
        ])
    lines.extend([
        "OpenSocrates method-routing and adapter-conformance extensions are not "
        "populated and are intentionally outside this review.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_V1_MANIFEST)
    parser.add_argument("--json-output", type=Path, default=ROOT / "reports/review/v1-scenario-review.json")
    parser.add_argument("--markdown-output", type=Path, default=ROOT / "reports/review/v1-scenario-review.md")
    args = parser.parse_args()
    payload = build_review(args.manifest)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(markdown_review(payload), encoding="utf-8")
    print(f"wrote review report to {args.json_output} and {args.markdown_output}")
    return 0 if payload["validation_status"] == "pass" and payload["failed_sample_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
