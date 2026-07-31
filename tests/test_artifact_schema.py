from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from tools.artifacts.schema_check import schema_definition_errors, schema_errors
from tools.artifacts.validation import validate_scenario


ROOT = Path(__file__).resolve().parents[1]
V01_SCHEMA_PATH = ROOT / "schemas" / "scenario.schema.json"
V02_SCHEMA_PATH = ROOT / "schemas" / "scenario-0.2.schema.json"
V02_COMPONENT_SCHEMA_PATHS = (
    ROOT / "schemas" / "artifact-contract.schema.json",
    ROOT / "schemas" / "atomic-rubric.schema.json",
    ROOT / "schemas" / "catalog-0.2.schema.json",
    ROOT / "schemas" / "manifest-0.2.schema.json",
)
SCENARIO_ROOT = ROOT / "data" / "v0.2" / "scenarios"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


class ArtifactSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.v01_schema = _load(V01_SCHEMA_PATH)
        cls.v02_schema = _load(V02_SCHEMA_PATH)
        cls.paths = sorted(SCENARIO_ROOT.glob("*.json"))
        cls.example_path = cls.paths[0]
        cls.example = _load(cls.example_path)

    def test_schema_is_resolvable_and_preserves_v0_1_vocabularies(self) -> None:
        self.assertEqual(
            schema_definition_errors(self.v02_schema, self.v02_schema), []
        )
        for path in V02_COMPONENT_SCHEMA_PATHS:
            component = _load(path)
            self.assertEqual(
                schema_definition_errors(component, component),
                [],
                path.name,
            )
        self.assertEqual(
            self.v02_schema["properties"]["schema"]["const"],
            "realworld-prompt-kit.scenario/0.2.0",
        )
        self.assertEqual(
            self.v02_schema["$defs"]["primary_intent"]["enum"],
            self.v01_schema["$defs"]["task"]["properties"]["primary_intent"]["enum"],
        )
        self.assertEqual(
            self.v02_schema["$defs"]["domain"]["enum"],
            self.v01_schema["$defs"]["domain"]["enum"],
        )
        self.assertEqual(
            self.v02_schema["$defs"]["naturalistic_profile"]["enum"],
            self.v01_schema["$defs"]["profile"]["enum"],
        )

    def test_all_release_scenarios_conform_and_cross_validate(self) -> None:
        self.assertEqual(len(self.paths), 12)
        failures: list[str] = []
        for path in self.paths:
            document = _load(path)
            errors, _, _ = validate_scenario(
                document,
                path,
                schema=self.v02_schema,
                root=ROOT,
                grade_reference=False,
            )
            failures.extend(errors)
        self.assertEqual(failures, [], "\n".join(failures))

    def test_schema_blocks_unearned_review_and_legacy_coverage_shape(self) -> None:
        unearned = copy.deepcopy(self.example)
        unearned["status"] = "reviewed"
        errors = schema_errors(unearned, self.v02_schema, self.v02_schema)
        self.assertTrue(errors)

        legacy = copy.deepcopy(self.example)
        legacy["coverage"]["interaction"] = "one_shot"
        errors = schema_errors(legacy, self.v02_schema, self.v02_schema)
        self.assertTrue(any("unexpected property" in error for error in errors))

    def test_schema_blocks_unsupported_output_media(self) -> None:
        broken = copy.deepcopy(self.example)
        broken["artifact_contract"]["outputs"][0]["media_type"] = "application/zip"
        errors = schema_errors(broken, self.v02_schema, self.v02_schema)
        self.assertTrue(any("outside the enum" in error for error in errors))

    def test_cross_validation_blocks_duplicate_ids_unknown_assets_and_hash_drift(self) -> None:
        mutations: list[tuple[dict[str, Any], str]] = []

        duplicate_gate = copy.deepcopy(self.example)
        duplicate_gate["evaluation"]["hard_gates"].append(
            copy.deepcopy(duplicate_gate["evaluation"]["hard_gates"][0])
        )
        mutations.append((duplicate_gate, "duplicate gate_id"))

        unknown_asset = copy.deepcopy(self.example)
        unknown_asset["realizations"][0]["messages"][0]["attachment_refs"] = [
            "missing_asset"
        ]
        mutations.append((unknown_asset, "attachment refs differ"))

        hash_drift = copy.deepcopy(self.example)
        hash_drift["assets"][0]["sha256"] = "0" * 64
        mutations.append((hash_drift, "asset hash mismatch"))

        planned = copy.deepcopy(self.example)
        planned["evaluation"]["hard_gates"][0]["scorer"][
            "implementation_status"
        ] = "planned"
        mutations.append((planned, "is still planned"))

        for document, expected in mutations:
            with self.subTest(expected=expected):
                errors, _, _ = validate_scenario(
                    document,
                    self.example_path,
                    schema=self.v02_schema,
                    root=ROOT,
                    grade_reference=False,
                )
                self.assertTrue(
                    any(expected in error for error in errors),
                    "\n".join(errors),
                )


if __name__ == "__main__":
    unittest.main()
