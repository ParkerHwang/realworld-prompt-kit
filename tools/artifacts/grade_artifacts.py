#!/usr/bin/env python3
"""Grade a v0.2 artifact submission or the checked-in reference artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from .inspect_ooxml import inspect_artifact
except ImportError:  # pragma: no cover - direct script execution
    from inspect_ooxml import inspect_artifact


ROOT = Path(__file__).resolve().parents[2]
IGNORED_SUBMISSION_FILES = {".DS_Store", "Thumbs.db"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_repo_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    candidate.relative_to(root.resolve())
    return candidate


def _artifact_paths(
    scenario: dict[str, Any],
    *,
    submission_dir: Path | None,
    reference: bool,
    root: Path,
) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for output in scenario["artifact_contract"]["outputs"]:
        if reference:
            path = _safe_repo_path(root, output["reference_path"])
        else:
            if submission_dir is None:
                raise ValueError("submission_dir is required outside reference mode")
            path = (submission_dir / output["filename"]).resolve()
            path.relative_to(submission_dir.resolve())
        paths[output["artifact_id"]] = path
    return paths


def _run_output_check(
    check: dict[str, Any],
    *,
    output: dict[str, Any],
    path: Path,
    inspection: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    check_type = check["type"]
    if check_type == "contains_text":
        haystack = inspection.get("text", "")
        case_sensitive = check.get("case_sensitive", False)
        if not case_sensitive:
            haystack = haystack.casefold()
        for expected in check.get("values", []):
            needle = expected if case_sensitive else expected.casefold()
            if needle not in haystack:
                errors.append(f"{output['artifact_id']}: missing text {expected!r}")
    elif check_type == "minimum_feature":
        feature = check.get("feature", "")
        minimum = check.get("minimum")
        if not feature or not isinstance(minimum, int):
            errors.append(f"{check['check_id']}: minimum_feature needs feature and minimum")
        elif inspection.get(feature, 0) < minimum:
            errors.append(
                f"{output['artifact_id']}: {feature}={inspection.get(feature, 0)} "
                f"is below {minimum}"
            )
    elif check_type == "required_sheet_names":
        missing = sorted(set(check.get("values", [])) - set(inspection.get("sheet_names", [])))
        if missing:
            errors.append(f"{output['artifact_id']}: missing sheets {missing}")
    elif check_type == "json_keys":
        missing = sorted(set(check.get("values", [])) - set(inspection.get("json_keys", [])))
        if missing:
            errors.append(f"{output['artifact_id']}: missing JSON keys {missing}")
    elif check_type == "parseable":
        if not inspection.get("parseable"):
            errors.append(
                f"{output['artifact_id']}: parse failed: "
                f"{inspection.get('error', 'unknown error')}"
            )
    elif check_type == "media_type":
        if inspection.get("media_type") != output["media_type"]:
            errors.append(
                f"{output['artifact_id']}: expected {output['media_type']}, "
                f"found {inspection.get('media_type')}"
            )
    elif check_type == "required_features":
        missing = sorted(
            set(output["required_features"]) - set(inspection.get("features", []))
        )
        if missing:
            errors.append(f"{output['artifact_id']}: missing features {missing}")
    elif check_type == "artifact_present":
        if not path.is_file():
            errors.append(f"{output['artifact_id']}: {path.name} is missing")
    elif check_type in {
        "bundle_exact_files",
        "reference_checks",
        "source_hashes_match",
    }:
        errors.append(f"{check['check_id']}: check must run at scenario scope")
    else:
        errors.append(f"{check['check_id']}: unsupported check type {check_type!r}")
    return errors


def _run_scenario_check(
    check: dict[str, Any],
    *,
    scenario: dict[str, Any],
    output_refs: list[str],
    outputs_by_id: dict[str, dict[str, Any]],
    paths: dict[str, Path],
    inspections: dict[str, dict[str, Any]],
    submission_dir: Path | None,
    root: Path,
) -> list[str]:
    check_type = check["type"]
    if check_type == "source_hashes_match":
        errors: list[str] = []
        for asset in scenario["assets"]:
            path = _safe_repo_path(root, asset["path"])
            if not path.is_file():
                errors.append(f"{asset['asset_id']}: source asset is missing")
            elif sha256(path) != asset["sha256"]:
                errors.append(f"{asset['asset_id']}: source SHA-256 mismatch")
        return errors
    if check_type == "bundle_exact_files":
        if submission_dir is None:
            directories = {path.parent for path in paths.values()}
            if len(directories) != 1:
                return ["reference outputs do not share one package directory"]
            active_dir = next(iter(directories))
        else:
            active_dir = submission_dir.resolve()
        observed = {
            path.name
            for path in active_dir.iterdir()
            if path.is_file() and path.name not in IGNORED_SUBMISSION_FILES
        }
        expected = set(check.get("values", []))
        if observed != expected:
            return [
                f"bundle files differ: missing={sorted(expected - observed)}, "
                f"unexpected={sorted(observed - expected)}"
            ]
        return []
    if check_type == "reference_checks":
        errors: list[str] = []
        for output_id in output_refs:
            output = outputs_by_id[output_id]
            for child in output["reference_checks"]:
                errors.extend(
                    _run_output_check(
                        child,
                        output=output,
                        path=paths[output_id],
                        inspection=inspections[output_id],
                    )
                )
        return errors

    errors = []
    for output_id in output_refs:
        output = outputs_by_id[output_id]
        errors.extend(
            _run_output_check(
                check,
                output=output,
                path=paths[output_id],
                inspection=inspections[output_id],
            )
        )
    return errors


def grade_scenario(
    scenario: dict[str, Any],
    *,
    submission_dir: Path | None = None,
    reference: bool = False,
    root: Path = ROOT,
) -> dict[str, Any]:
    paths = _artifact_paths(
        scenario,
        submission_dir=submission_dir,
        reference=reference,
        root=root,
    )
    outputs_by_id = {
        output["artifact_id"]: output
        for output in scenario["artifact_contract"]["outputs"]
    }
    inspections = {
        output_id: inspect_artifact(path)
        for output_id, path in paths.items()
    }

    hard_gate_results: list[dict[str, Any]] = []
    for gate in scenario["evaluation"]["hard_gates"]:
        check = gate["scorer"].get("check")
        if not check:
            errors = [f"{gate['gate_id']}: implemented hard gate has no check"]
        else:
            errors = _run_scenario_check(
                check,
                scenario=scenario,
                output_refs=gate["artifact_refs"],
                outputs_by_id=outputs_by_id,
                paths=paths,
                inspections=inspections,
                submission_dir=submission_dir,
                root=root,
            )
        hard_gate_results.append(
            {
                "gate_id": gate["gate_id"],
                "category": gate["category"],
                "status": "pass" if not errors else "fail",
                "errors": errors,
            }
        )

    rubric_results: list[dict[str, Any]] = []
    dimension_scores: dict[str, list[float]] = defaultdict(list)
    for item in scenario["evaluation"]["atomic_rubric_items"]:
        scorer = item["scorer"]
        check = scorer.get("check")
        if scorer["method"] in {"human", "model_judge"} and check is None:
            result = {
                "rubric_id": item["rubric_id"],
                "dimension": item["dimension"],
                "status": "unscored",
                "score": None,
                "errors": [],
            }
            rubric_results.append(result)
            continue
        output_refs = [
            evidence["ref"]
            for evidence in item["evidence_refs"]
            if evidence["source"] == "output"
        ]
        errors = (
            [f"{item['rubric_id']}: implemented scorer has no executable check"]
            if check is None
            else _run_scenario_check(
                check,
                scenario=scenario,
                output_refs=output_refs,
                outputs_by_id=outputs_by_id,
                paths=paths,
                inspections=inspections,
                submission_dir=submission_dir,
                root=root,
            )
        )
        score = 0.0 if errors else 1.0
        dimension_scores[item["dimension"]].append(score)
        rubric_results.append(
            {
                "rubric_id": item["rubric_id"],
                "dimension": item["dimension"],
                "status": "pass" if not errors else "fail",
                "score": score,
                "errors": errors,
            }
        )

    artifact_valid = sum(
        bool(inspection.get("parseable"))
        for inspection in inspections.values()
    )
    hard_gate_pass = all(item["status"] == "pass" for item in hard_gate_results)
    full_pass = hard_gate_pass
    return {
        "schema": "realworld-prompt-kit.artifact-result/0.2.0",
        "scenario_id": scenario["scenario_id"],
        "mode": "reference" if reference else "submission",
        "full_pass": full_pass,
        "artifact_valid_rate": (
            artifact_valid / len(inspections) if inspections else 0.0
        ),
        "hard_gate_results": hard_gate_results,
        "rubric_results": rubric_results,
        "atomic_score_by_dimension": {
            dimension: sum(scores) / len(scores)
            for dimension, scores in sorted(dimension_scores.items())
        },
        "unscored_item_count": sum(
            result["status"] == "unscored" for result in rubric_results
        ),
        "artifacts": {
            output_id: {
                "path": (
                    paths[output_id].relative_to(root).as_posix()
                    if reference
                    else str(paths[output_id])
                ),
                "parseable": inspection.get("parseable", False),
                "media_type": inspection.get("media_type"),
                "features": inspection.get("features", []),
            }
            for output_id, inspection in inspections.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--submission-dir", type=Path)
    parser.add_argument("--reference", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.reference == (args.submission_dir is not None):
        raise SystemExit("choose exactly one of --reference or --submission-dir")
    result = grade_scenario(
        load_json(args.scenario),
        submission_dir=args.submission_dir,
        reference=args.reference,
    )
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result["full_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
