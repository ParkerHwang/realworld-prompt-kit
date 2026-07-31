"""Repository-level validation for the v0.2 Artifact Core release."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from .grade_artifacts import grade_scenario
    from .inspect_ooxml import inspect_artifact
    from .schema_check import schema_definition_errors, schema_errors
except ImportError:  # pragma: no cover - direct script execution
    from grade_artifacts import grade_scenario
    from inspect_ooxml import inspect_artifact
    from schema_check import schema_definition_errors, schema_errors


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "data" / "v0.2" / "manifest.json"
SCENARIO_SCHEMA_PATH = ROOT / "schemas" / "scenario-0.2.schema.json"
ARTIFACT_CONTRACT_SCHEMA_PATH = ROOT / "schemas" / "artifact-contract.schema.json"
ATOMIC_RUBRIC_SCHEMA_PATH = ROOT / "schemas" / "atomic-rubric.schema.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "manifest-0.2.schema.json"
CATALOG_SCHEMA_PATH = ROOT / "schemas" / "catalog-0.2.schema.json"
EXPECTED_MANIFEST_SCHEMA = "realworld-prompt-kit.manifest/0.2.0"
EXPECTED_CATALOG_SCHEMA = "realworld-prompt-kit.catalog/0.2.0"
EXPECTED_SCENARIO_SCHEMA = "realworld-prompt-kit.scenario/0.2.0"


@dataclass
class ArtifactValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    reference_results: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _relative(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    path.relative_to(root.resolve())
    return path


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scenario_paths(manifest: dict[str, Any], root: Path = ROOT) -> list[Path]:
    return sorted(root.glob(manifest["scenario_glob"]))


def _messages_text(realization: dict[str, Any]) -> str:
    return "\n".join(
        message.get("content", "")
        for message in realization.get("messages", [])
        if message.get("content")
    )


def _normalize(value: str) -> str:
    return " ".join(re.sub(r"[^\w가-힣]+", " ", value.casefold()).split())


def _id_duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _all_checks(document: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for output in document["artifact_contract"]["outputs"]:
        checks.extend(output["reference_checks"])
    for item in [
        *document["evaluation"]["hard_gates"],
        *document["evaluation"]["atomic_rubric_items"],
    ]:
        check = item["scorer"].get("check")
        if check:
            checks.append(check)
    return checks


def validate_scenario(
    document: dict[str, Any],
    path: Path,
    *,
    schema: dict[str, Any],
    root: Path = ROOT,
    grade_reference: bool = True,
) -> tuple[list[str], list[str], dict[str, Any] | None]:
    label = _relative(path, root)
    errors = [
        f"{label}: {error}"
        for error in schema_errors(document, schema, schema)
    ]
    warnings: list[str] = []
    if errors:
        return errors, warnings, None

    scenario_id = document["scenario_id"]
    if path.stem != scenario_id:
        errors.append(f"{label}: filename must equal scenario_id")
    if document["semantic_group_id"] != scenario_id.replace("rwpk.", "rwpg.", 1):
        errors.append(f"{label}: semantic_group_id must derive from scenario_id")

    asset_ids = [asset["asset_id"] for asset in document["assets"]]
    output_ids = [
        output["artifact_id"] for output in document["artifact_contract"]["outputs"]
    ]
    gate_ids = [gate["gate_id"] for gate in document["evaluation"]["hard_gates"]]
    rubric_ids = [
        item["rubric_id"] for item in document["evaluation"]["atomic_rubric_items"]
    ]
    check_ids = [check["check_id"] for check in _all_checks(document)]
    for name, values in (
        ("asset_id", asset_ids),
        ("artifact_id", output_ids),
        ("gate_id", gate_ids),
        ("rubric_id", rubric_ids),
        ("check_id", check_ids),
    ):
        duplicates = _id_duplicates(values)
        if duplicates:
            errors.append(f"{label}: duplicate {name} values {duplicates}")

    known_assets = set(asset_ids)
    known_outputs = set(output_ids)
    expected_pairs = {
        ("ko-KR", "canonical"),
        ("ko-KR", "naturalistic"),
        ("en-US", "canonical"),
        ("en-US", "naturalistic"),
    }
    observed_pairs = {
        (item["locale"], item["form"]) for item in document["realizations"]
    }
    if observed_pairs != expected_pairs:
        errors.append(
            f"{label}: realization pairs differ: "
            f"missing={sorted(expected_pairs - observed_pairs)}, "
            f"unexpected={sorted(observed_pairs - expected_pairs)}"
        )
    if set(document["coverage"]["request_forms"]) != {"canonical", "naturalistic"}:
        errors.append(f"{label}: request_forms must declare canonical and naturalistic")
    for realization in document["realizations"]:
        expected_prompt_id = (
            f"{scenario_id}.{realization['locale']}.{realization['form']}"
        )
        if realization["prompt_id"] != expected_prompt_id:
            errors.append(
                f"{label}: prompt_id {realization['prompt_id']!r} "
                f"must be {expected_prompt_id!r}"
            )
        expected_origin = (
            "controlled_canonical"
            if realization["form"] == "canonical"
            else "synthetic_naturalistic"
        )
        if realization["origin"] != expected_origin:
            errors.append(
                f"{label}: {realization['prompt_id']} has incorrect origin"
            )
        expected_features = (
            set()
            if realization["form"] == "canonical"
            else set(document["coverage"]["naturalistic_features"])
        )
        if set(realization["features"]) != expected_features:
            errors.append(
                f"{label}: {realization['prompt_id']} features do not match coverage"
            )
        attachment_refs = {
            ref
            for message in realization["messages"]
            for ref in message.get("attachment_refs", [])
        }
        if attachment_refs != known_assets:
            errors.append(
                f"{label}: {realization['prompt_id']} attachment refs differ: "
                f"missing={sorted(known_assets - attachment_refs)}, "
                f"unknown={sorted(attachment_refs - known_assets)}"
            )
        text = _messages_text(realization)
        if len(text.strip()) < 40:
            errors.append(f"{label}: {realization['prompt_id']} is too short")
        if realization["locale"] == "ko-KR" and not re.search(r"[가-힣]", text):
            errors.append(f"{label}: {realization['prompt_id']} has no Korean text")
        if realization["locale"] == "en-US" and not re.search(
            r"\b[A-Za-z]{3,}\b", text
        ):
            errors.append(f"{label}: {realization['prompt_id']} has no English text")

    for locale in ("ko-KR", "en-US"):
        canonical = next(
            item
            for item in document["realizations"]
            if item["locale"] == locale and item["form"] == "canonical"
        )
        naturalistic = next(
            item
            for item in document["realizations"]
            if item["locale"] == locale and item["form"] == "naturalistic"
        )
        ratio = difflib.SequenceMatcher(
            None,
            _normalize(_messages_text(canonical)),
            _normalize(_messages_text(naturalistic)),
        ).ratio()
        if ratio >= 0.85:
            errors.append(
                f"{label}: {locale} canonical/naturalistic similarity "
                f"{ratio:.3f} reaches the 0.85 failure threshold"
            )
        elif ratio >= 0.75:
            warnings.append(
                f"{label}: {locale} canonical/naturalistic similarity "
                f"{ratio:.3f} reaches the 0.75 review threshold"
            )

    asset_families = {asset["artifact_family"] for asset in document["assets"]}
    output_families = {
        output["artifact_family"]
        for output in document["artifact_contract"]["outputs"]
    }
    if set(document["coverage"]["input_artifact_families"]) != asset_families:
        errors.append(f"{label}: input artifact-family coverage differs from assets")
    if set(document["coverage"]["output_artifact_families"]) != output_families:
        errors.append(f"{label}: output artifact-family coverage differs from outputs")
    if (
        document["coverage"]["authority"]
        != document["artifact_contract"]["side_effect_scope"]
    ):
        errors.append(f"{label}: coverage authority and artifact contract differ")

    for asset in document["assets"]:
        try:
            asset_path = _safe_path(root, asset["path"])
        except ValueError:
            errors.append(f"{label}: asset path escapes repository: {asset['path']}")
            continue
        expected_parent = (
            root / "data" / "v0.2" / "assets" / scenario_id
        ).resolve()
        if asset_path.parent != expected_parent:
            errors.append(
                f"{label}: asset {asset['asset_id']} must live under its scenario directory"
            )
        if not asset_path.is_file():
            errors.append(f"{label}: missing asset {asset['path']}")
            continue
        if _digest(asset_path) != asset["sha256"]:
            errors.append(f"{label}: asset hash mismatch for {asset['asset_id']}")
        inspection = inspect_artifact(asset_path)
        if not inspection.get("parseable"):
            errors.append(
                f"{label}: asset {asset['asset_id']} does not parse: "
                f"{inspection.get('error')}"
            )
        if inspection.get("media_type") != asset["media_type"]:
            errors.append(
                f"{label}: asset {asset['asset_id']} media type differs from file"
            )
        if "native_file" not in asset["allowed_delivery_modes"]:
            errors.append(
                f"{label}: v0.2 asset {asset['asset_id']} must permit native_file"
            )

    outputs_by_id = {
        output["artifact_id"]: output
        for output in document["artifact_contract"]["outputs"]
    }
    for output in outputs_by_id.values():
        try:
            reference_path = _safe_path(root, output["reference_path"])
        except ValueError:
            errors.append(
                f"{label}: reference path escapes repository: {output['reference_path']}"
            )
            continue
        expected_parent = (
            root / "data" / "v0.2" / "public-calibration" / scenario_id
        ).resolve()
        if reference_path.parent != expected_parent:
            errors.append(
                f"{label}: reference {output['artifact_id']} must live under its scenario directory"
            )
        if reference_path.name != output["filename"]:
            errors.append(
                f"{label}: output filename and reference basename differ for "
                f"{output['artifact_id']}"
            )
        if not reference_path.is_file():
            errors.append(f"{label}: missing reference {output['reference_path']}")
        elif _digest(reference_path) != output["reference_sha256"]:
            errors.append(
                f"{label}: reference hash mismatch for {output['artifact_id']}"
            )

    for gate in document["evaluation"]["hard_gates"]:
        unknown = set(gate["artifact_refs"]) - known_outputs
        if unknown:
            errors.append(
                f"{label}: gate {gate['gate_id']} references unknown outputs {sorted(unknown)}"
            )
    for item in [
        *document["evaluation"]["hard_gates"],
        *document["evaluation"]["atomic_rubric_items"],
    ]:
        scorer = item["scorer"]
        if scorer["implementation_status"] == "planned":
            errors.append(
                f"{label}: release scorer {item.get('gate_id', item.get('rubric_id'))} "
                "is still planned"
            )
        if scorer["method"] in {"deterministic", "office_engine", "rule_assisted"}:
            if "check" not in scorer:
                errors.append(
                    f"{label}: executable scorer "
                    f"{item.get('gate_id', item.get('rubric_id'))} has no check"
                )
        for evidence in item["evidence_refs"]:
            if evidence["source"] == "asset" and evidence["ref"] not in known_assets:
                errors.append(
                    f"{label}: unknown asset evidence ref {evidence['ref']!r}"
                )
            if evidence["source"] == "output" and evidence["ref"] not in known_outputs:
                errors.append(
                    f"{label}: unknown output evidence ref {evidence['ref']!r}"
                )

    calibration = document["evaluation"]["human_calibration"]
    if document["status"] == "calibration_ready":
        if calibration["status"] not in {"not_run", "in_progress"}:
            errors.append(
                f"{label}: calibration_ready scenario must not claim completed calibration"
            )
        if document["provenance"]["review"]["human_practitioner_review"]:
            errors.append(
                f"{label}: calibration release must not claim practitioner review"
            )
    elif document["status"] in {"reviewed", "frozen"}:
        if calibration["status"] != "completed":
            errors.append(
                f"{label}: reviewed/frozen scenario needs completed human calibration"
            )

    reference_result = None
    if grade_reference and not errors:
        reference_result = grade_scenario(document, reference=True, root=root)
        if not reference_result["full_pass"]:
            failed = [
                result["gate_id"]
                for result in reference_result["hard_gate_results"]
                if result["status"] == "fail"
            ]
            errors.append(f"{label}: reference hard gates failed {failed}")
        failed_rubrics = [
            result["rubric_id"]
            for result in reference_result["rubric_results"]
            if result["status"] == "fail"
        ]
        if failed_rubrics:
            errors.append(f"{label}: reference rubric checks failed {failed_rubrics}")
    return errors, warnings, reference_result


def validate_repository(
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    root: Path = ROOT,
) -> ArtifactValidationReport:
    report = ArtifactValidationReport()
    if not manifest_path.is_absolute():
        manifest_path = (root / manifest_path).resolve()
    try:
        manifest = load_json(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.errors.append(f"{_relative(manifest_path, root)}: {exc}")
        return report
    try:
        manifest_schema = load_json(MANIFEST_SCHEMA_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.errors.append(f"manifest schema: {exc}")
        return report
    report.errors.extend(
        f"manifest schema: {error}"
        for error in schema_definition_errors(manifest_schema, manifest_schema)
    )
    report.errors.extend(
        f"manifest: {error}"
        for error in schema_errors(manifest, manifest_schema, manifest_schema)
    )
    if manifest.get("schema") != EXPECTED_MANIFEST_SCHEMA:
        report.errors.append(
            f"manifest schema must be {EXPECTED_MANIFEST_SCHEMA!r}"
        )
        return report
    if manifest.get("status") != "calibration_release":
        report.errors.append("v0.2 manifest status must be calibration_release")
    claims = manifest.get("claim_boundaries", {})
    for claim in (
        "leaderboard_valid",
        "human_calibration_complete",
        "external_replication_complete",
    ):
        if claims.get(claim) is not False:
            report.errors.append(f"claim boundary {claim} must remain false in v0.2")

    try:
        catalog_path = _safe_path(root, manifest["catalog_path"])
        catalog = load_json(catalog_path)
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        report.errors.append(f"catalog: {exc}")
        return report
    if catalog.get("schema") != EXPECTED_CATALOG_SCHEMA:
        report.errors.append(f"catalog schema must be {EXPECTED_CATALOG_SCHEMA!r}")
    try:
        catalog_schema = load_json(CATALOG_SCHEMA_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.errors.append(f"catalog schema: {exc}")
        return report
    report.errors.extend(
        f"catalog schema: {error}"
        for error in schema_definition_errors(catalog_schema, catalog_schema)
    )
    report.errors.extend(
        f"catalog: {error}"
        for error in schema_errors(catalog, catalog_schema, catalog_schema)
    )

    try:
        scenario_schema = load_json(SCENARIO_SCHEMA_PATH)
        artifact_contract_schema = load_json(ARTIFACT_CONTRACT_SCHEMA_PATH)
        atomic_rubric_schema = load_json(ATOMIC_RUBRIC_SCHEMA_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.errors.append(f"scenario component schema: {exc}")
        return report
    for name, active_schema in (
        ("scenario", scenario_schema),
        ("artifact contract", artifact_contract_schema),
        ("atomic rubric", atomic_rubric_schema),
    ):
        definition_errors = schema_definition_errors(active_schema, active_schema)
        report.errors.extend(
            f"{name} schema: {error}" for error in definition_errors
        )

    paths = scenario_paths(manifest, root)
    scenarios: list[dict[str, Any]] = []
    for path in paths:
        try:
            scenario = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            report.errors.append(f"{_relative(path, root)}: {exc}")
            continue
        errors, warnings, reference_result = validate_scenario(
            scenario,
            path,
            schema=scenario_schema,
            root=root,
        )
        report.errors.extend(errors)
        label = _relative(path, root)
        report.errors.extend(
            f"{label}: artifact contract: {error}"
            for error in schema_errors(
                scenario.get("artifact_contract"),
                artifact_contract_schema,
                artifact_contract_schema,
            )
        )
        for index, item in enumerate(
            scenario.get("evaluation", {}).get("atomic_rubric_items", [])
        ):
            report.errors.extend(
                f"{label}: atomic rubric {index}: {error}"
                for error in schema_errors(
                    item,
                    atomic_rubric_schema,
                    atomic_rubric_schema,
                )
            )
        report.warnings.extend(warnings)
        if reference_result is not None:
            report.reference_results.append(reference_result)
        scenarios.append(scenario)

    scenario_ids = [scenario.get("scenario_id", "") for scenario in scenarios]
    semantic_ids = [scenario.get("semantic_group_id", "") for scenario in scenarios]
    prompt_ids = [
        realization.get("prompt_id", "")
        for scenario in scenarios
        for realization in scenario.get("realizations", [])
    ]
    for name, values in (
        ("scenario_id", scenario_ids),
        ("semantic_group_id", semantic_ids),
        ("prompt_id", prompt_ids),
    ):
        duplicates = _id_duplicates(values)
        if duplicates:
            report.errors.append(f"globally duplicate {name} values {duplicates}")

    module_counts = Counter(
        scenario["coverage"]["module"] for scenario in scenarios
    )
    workflow_counts = Counter(
        scenario["task"]["workflow_job"] for scenario in scenarios
    )
    output_family_counts = Counter(
        output["artifact_family"]
        for scenario in scenarios
        for output in scenario["artifact_contract"]["outputs"]
    )
    status_counts = Counter(scenario["status"] for scenario in scenarios)
    calibration_counts = Counter(
        scenario["evaluation"]["human_calibration"]["status"]
        for scenario in scenarios
    )
    expected_scenarios = manifest["expected_scenarios"]
    expected_realizations = manifest["expected_realizations"]
    observed_realizations = sum(len(item["realizations"]) for item in scenarios)
    if len(scenarios) != expected_scenarios:
        report.errors.append(
            f"expected {expected_scenarios} scenarios, found {len(scenarios)}"
        )
    if observed_realizations != expected_realizations:
        report.errors.append(
            f"expected {expected_realizations} realizations, found {observed_realizations}"
        )
    if dict(module_counts) != manifest["required_modules"]:
        report.errors.append(
            f"module counts differ: expected {manifest['required_modules']}, "
            f"found {dict(module_counts)}"
        )
    missing_jobs = sorted(
        set(manifest["required_workflow_jobs"]) - set(workflow_counts)
    )
    if missing_jobs:
        report.errors.append(f"required workflow jobs are missing: {missing_jobs}")
    missing_output_families = sorted(
        set(manifest["required_output_families"]) - set(output_family_counts)
    )
    if missing_output_families:
        report.errors.append(
            f"required output families are missing: {missing_output_families}"
        )
    if set(status_counts) != {"calibration_ready"}:
        report.errors.append(
            f"v0.2 release scenarios must all be calibration_ready: {dict(status_counts)}"
        )

    catalog_episodes = {
        item["scenario_id"]: item for item in catalog.get("episodes", [])
    }
    if set(catalog_episodes) != set(scenario_ids):
        report.errors.append(
            "catalog episode IDs differ from checked-in scenario IDs"
        )
    for scenario in scenarios:
        item = catalog_episodes.get(scenario["scenario_id"])
        if not item:
            continue
        expected_path = _relative(
            root / "data" / "v0.2" / "scenarios" / f"{scenario['scenario_id']}.json",
            root,
        )
        if item["path"] != expected_path:
            report.errors.append(
                f"catalog path differs for {scenario['scenario_id']}"
            )

    report.stats = {
        "manifest_status": manifest["status"],
        "semantic_scenarios": len(scenarios),
        "prompt_realizations": observed_realizations,
        "input_assets": sum(len(item["assets"]) for item in scenarios),
        "reference_artifacts": sum(
            len(item["artifact_contract"]["outputs"]) for item in scenarios
        ),
        "module_counts": dict(sorted(module_counts.items())),
        "workflow_job_counts": dict(sorted(workflow_counts.items())),
        "output_family_counts": dict(sorted(output_family_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "human_calibration_status_counts": dict(sorted(calibration_counts.items())),
        "reference_full_pass_count": sum(
            result["full_pass"] for result in report.reference_results
        ),
        "reference_result_count": len(report.reference_results),
        "human_unscored_rubric_items": sum(
            result["unscored_item_count"] for result in report.reference_results
        ),
    }
    return report
