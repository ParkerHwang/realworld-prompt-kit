from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V01_ROOT = ROOT / "data" / "v0.1"
V01_SCENARIO_ROOT = V01_ROOT / "scenarios"
V02_ROOT = ROOT / "data" / "v0.2"
V02_SCENARIO_ROOT = V02_ROOT / "scenarios"


def _release_surface_files() -> list[Path]:
    roots = [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / ".gitignore",
        ROOT / ".github",
        ROOT / "docs",
        ROOT / "schemas",
        ROOT / "tools",
        ROOT / "tests",
        ROOT / "reports",
        ROOT / "suites",
        ROOT / "data" / "v0.1" / "catalog.json",
        ROOT / "data" / "v0.1" / "manifest.json",
        ROOT / "data" / "v0.2" / "catalog.json",
        ROOT / "data" / "v0.2" / "manifest.json",
        ROOT / "data" / "v0.2" / "scenarios",
        ROOT / "data" / "v0.2" / "public-calibration" / "README.md",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
            )
    return sorted(set(files))


class ReleaseNamingTests(unittest.TestCase):
    def test_release_surface_has_no_parallel_version_residue(self) -> None:
        release_version_one = "v" + "1"
        release_version_one_zero = release_version_one + ".0"
        schema_version_one = "1" + ".0.0"
        old_seed_name = "office-" + "core-cb8"
        forbidden = (
            release_version_one,
            release_version_one_zero,
            schema_version_one,
            "data/" + release_version_one_zero,
            old_seed_name,
        )
        failures = []
        for path in _release_surface_files():
            text = path.read_text(encoding="utf-8")
            lowered = text.casefold()
            hits = [term for term in forbidden if term.casefold() in lowered]
            if hits:
                failures.append(f"{path.relative_to(ROOT)}: {hits}")
        self.assertEqual(failures, [], "release-version residue found:\n" + "\n".join(failures))

    def test_release_surface_has_no_live_branch_refs(self) -> None:
        # Build the branch marker dynamically so this regression test does not
        # become a false positive in the repository-wide tracked-text scan.
        branch_prefix = "co" + "dex/"
        legacy_release = "v" + "1"
        forbidden = (
            branch_prefix,
            branch_prefix + "worker-",
            branch_prefix + "coverage-audit",
            branch_prefix + "v0.1-full-core-consolidation",
            branch_prefix + legacy_release + "-full-kit-integration",
        )
        failures = []
        for path in _release_surface_files():
            text = path.read_text(encoding="utf-8")
            hits = [term for term in forbidden if term.casefold() in text.casefold()]
            if hits:
                failures.append(f"{path.relative_to(ROOT)}: {hits}")
        self.assertEqual(failures, [], "live branch reference found:\n" + "\n".join(failures))

    def test_only_v0_1_and_v0_2_data_roots_and_scenario_schemas(self) -> None:
        data_dirs = sorted(path.name for path in (ROOT / "data").iterdir() if path.is_dir())
        self.assertEqual(data_dirs, ["v0.1", "v0.2"])
        self.assertTrue(V01_ROOT.is_dir())
        self.assertTrue(V02_ROOT.is_dir())
        self.assertFalse((ROOT / "data" / ("v" + "1.0")).exists())

        manifest = json.loads((V01_ROOT / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((V01_ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "realworld-prompt-kit.manifest/0.1.0")
        self.assertEqual(catalog["schema"], "realworld-prompt-kit.catalog/0.1.0")
        self.assertEqual(manifest["catalog_path"], "data/v0.1/catalog.json")
        self.assertEqual(manifest["scenario_glob"], "data/v0.1/scenarios/**/*.json")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(catalog["version"], "0.1.0")

        scenarios = sorted(V01_SCENARIO_ROOT.rglob("*.json"))
        self.assertEqual(len(scenarios), 880)
        schemas = {
            json.loads(path.read_text(encoding="utf-8"))["schema"] for path in scenarios
        }
        self.assertEqual(schemas, {"realworld-prompt-kit.scenario/0.1.0"})

        manifest = json.loads((V02_ROOT / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((V02_ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "realworld-prompt-kit.manifest/0.2.0")
        self.assertEqual(catalog["schema"], "realworld-prompt-kit.catalog/0.2.0")
        self.assertEqual(manifest["catalog_path"], "data/v0.2/catalog.json")
        self.assertEqual(manifest["scenario_glob"], "data/v0.2/scenarios/*.json")
        self.assertEqual(manifest["version"], "0.2.0")
        self.assertEqual(catalog["version"], "0.2.0")

        scenarios = sorted(V02_SCENARIO_ROOT.glob("*.json"))
        self.assertEqual(len(scenarios), 12)
        schemas = {
            json.loads(path.read_text(encoding="utf-8"))["schema"] for path in scenarios
        }
        self.assertEqual(schemas, {"realworld-prompt-kit.scenario/0.2.0"})


if __name__ == "__main__":
    unittest.main()
