from __future__ import annotations

import copy
import unittest

from tools.validate import DEFAULT_MANIFEST, ROOT, load_json, scenario_paths
from tools.validate import validate_repository, validate_scenario


class ValidationTests(unittest.TestCase):
    def test_repository_is_valid(self) -> None:
        self.assertEqual(validate_repository(), [])

    def test_duplicate_realization_pair_is_rejected(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        document = load_json(scenario_paths(manifest, ROOT)[0])
        broken = copy.deepcopy(document)
        broken["realizations"][1]["form"] = "canonical"
        errors = validate_scenario(broken, ROOT / "synthetic-broken.json")
        self.assertTrue(any("realization pairs" in error for error in errors))

    def test_naturalistic_features_are_required(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        document = load_json(scenario_paths(manifest, ROOT)[0])
        broken = copy.deepcopy(document)
        naturalistic = next(
            item for item in broken["realizations"] if item["form"] == "naturalistic"
        )
        naturalistic["features"] = []
        errors = validate_scenario(broken, ROOT / "synthetic-broken.json")
        self.assertTrue(any("needs at least one feature" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
