from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.artifacts.export_jsonl import flatten
from tools.artifacts.validation import load_json, scenario_paths, validate_repository


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "v0.2" / "manifest.json"


class ArtifactReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_json(MANIFEST_PATH)
        cls.paths = scenario_paths(cls.manifest, ROOT)
        cls.scenarios = [load_json(path) for path in cls.paths]
        cls.report = validate_repository(MANIFEST_PATH)

    def test_release_validator_and_exact_counts(self) -> None:
        self.assertEqual(self.report.errors, [], "\n".join(self.report.errors))
        self.assertEqual(self.report.stats["semantic_scenarios"], 12)
        self.assertEqual(self.report.stats["prompt_realizations"], 48)
        self.assertEqual(self.report.stats["input_assets"], 20)
        self.assertEqual(self.report.stats["reference_artifacts"], 18)
        self.assertEqual(set(self.report.stats["module_counts"].values()), {2})

    def test_reference_artifacts_pass_deterministic_contracts(self) -> None:
        self.assertEqual(len(self.report.reference_results), 12)
        for result in self.report.reference_results:
            with self.subTest(scenario_id=result["scenario_id"]):
                self.assertTrue(result["full_pass"])
                self.assertEqual(result["artifact_valid_rate"], 1.0)
                self.assertFalse(
                    any(
                        item["status"] == "fail"
                        for item in result["rubric_results"]
                    )
                )

    def test_release_has_real_input_and_editable_output_families(self) -> None:
        input_suffixes = {
            (ROOT / asset["path"]).suffix.lower()
            for scenario in self.scenarios
            for asset in scenario["assets"]
        }
        output_suffixes = {
            Path(output["filename"]).suffix.lower()
            for scenario in self.scenarios
            for output in scenario["artifact_contract"]["outputs"]
        }
        self.assertTrue({".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt"} <= input_suffixes)
        self.assertTrue({".docx", ".pptx", ".xlsx"} <= output_suffixes)

    def test_claim_boundaries_remain_calibration_only(self) -> None:
        claims = self.manifest["claim_boundaries"]
        self.assertIs(claims["leaderboard_valid"], False)
        self.assertIs(claims["human_calibration_complete"], False)
        self.assertIs(claims["external_replication_complete"], False)
        self.assertTrue(
            all(
                scenario["evaluation"]["human_calibration"]["status"] == "not_run"
                for scenario in self.scenarios
            )
        )

    def test_jsonl_flattening_is_four_rows_per_episode(self) -> None:
        rows = [row for scenario in self.scenarios for row in flatten(scenario)]
        self.assertEqual(len(rows), 48)
        self.assertEqual(
            {row["schema"] for row in rows},
            {"realworld-prompt-kit.sample/0.2.0"},
        )
        self.assertEqual(len({row["prompt_id"] for row in rows}), 48)
        self.assertTrue(all(row["assets"] for row in rows))
        self.assertTrue(all(row["artifact_contract"]["outputs"] for row in rows))


if __name__ == "__main__":
    unittest.main()
