from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.validation import (
    DEFAULT_MANIFEST,
    ROOT,
    _quality_lint,
    _naturalistic_feature_errors,
    _validate_scenario,
    load_json,
    validate_repository,
)


class ValidationTests(unittest.TestCase):
    def test_catalog_has_authorized_vocabularies(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        catalog = load_json(ROOT / manifest["catalog_path"])
        self.assertEqual(len(catalog["task_intents"]), 21)
        self.assertEqual(len(catalog["authorized_domain_ids"]), 28)
        self.assertEqual(len(catalog["authorized_naturalistic_profile_ids"]), 24)
        self.assertEqual(sum(item["expected_scenarios"] for item in catalog["task_intents"]), 880)
        self.assertEqual(sum(len(item["blocks"]) for item in catalog["task_intents"]), 110)

    def test_repository_is_valid(self) -> None:
        report = validate_repository()
        self.assertEqual(report.errors, [], "\n".join(report.errors[:20]))
        self.assertEqual(report.stats["semantic_scenarios"], 880)
        self.assertEqual(report.stats["prompt_realizations"], 3520)

    def test_similarity_lint_rejects_wrapper_identity(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        scenario = load_json(scenario_path)
        broken = copy.deepcopy(scenario)
        naturalistic = next(item for item in broken["realizations"] if item["form"] == "naturalistic")
        canonical = next(item for item in broken["realizations"] if item["form"] == "canonical")
        naturalistic["messages"] = copy.deepcopy(canonical["messages"])
        errors, _warnings, _stats = _quality_lint([broken], manifest, ROOT)
        self.assertTrue(any("identical after normalization" in error for error in errors))

    def test_schema_is_valid_json(self) -> None:
        with (ROOT / "schemas/scenario.schema.json").open(encoding="utf-8") as handle:
            schema = json.load(handle)
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schema"]["const"], "realworld-prompt-kit.scenario/0.1.0")

    def test_profile_realism_rejects_non_terse_prompt(self) -> None:
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        scenario = load_json(scenario_path)
        broken = copy.deepcopy(scenario)
        broken["coverage"]["naturalistic_features"] = ["terse_fragment"]
        for realization in broken["realizations"]:
            if realization["form"] == "naturalistic":
                realization["messages"] = [{
                    "role": "user",
                    "content": "이것은 너무 긴 자연어 입력입니다 " * 12
                    if realization["locale"] == "ko-KR"
                    else "This is deliberately a long naturalistic prompt " * 12,
                }]
        errors = _naturalistic_feature_errors(broken, Path("synthetic-broken.json"), load_json(DEFAULT_MANIFEST))
        self.assertTrue(any("32-token per-locale limit" in error for error in errors))

    def test_profile_realism_rejects_serialized_terse_message(self) -> None:
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        broken = copy.deepcopy(load_json(scenario_path))
        broken["coverage"]["naturalistic_features"] = ["terse_fragment"]
        for realization in broken["realizations"]:
            if realization["form"] == "naturalistic":
                realization["messages"] = [{
                    "role": "user",
                    "content": (
                        "주제: 일정 | 맥락: 확인할 항목 | 결과: 짧은 답을 원함"
                        if realization["locale"] == "ko-KR"
                        else "topic: schedule | context: checks | result: short answer"
                    ),
                }]
        errors = _naturalistic_feature_errors(
            broken, Path("synthetic-serialized-terse.json"), load_json(DEFAULT_MANIFEST)
        )
        self.assertTrue(any("serialized field list" in error for error in errors))

    def test_code_switch_cue_allows_korean_particle_after_english_token(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        scenario = copy.deepcopy(load_json(scenario_path))
        scenario["coverage"]["naturalistic_features"] = ["code_switching_jargon"]
        for realization in scenario["realizations"]:
            if realization["form"] == "naturalistic":
                realization["messages"] = [{
                    "role": "user",
                    "content": (
                        "회의 기록의 owner는 비워 두고 status는 확인 전으로 남겨줘"
                        if realization["locale"] == "ko-KR"
                        else "Leave the owner blank and keep the status marked pending."
                    ),
                }]
        errors = _naturalistic_feature_errors(
            scenario, Path("synthetic-mixed-script-cue.json"), manifest
        )
        self.assertFalse(any("code_switching_jargon" in error for error in errors))

    def test_phrase_gate_uses_distinct_scenario_presence(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        source = load_json(scenario_path)
        scenarios = []
        for index in range(21):
            scenario = copy.deepcopy(source)
            scenario["scenario_id"] = f"rwpk.synthetic.test.{index:04d}"
            scenario["semantic_group_id"] = f"rwpg.synthetic.test.{index:04d}"
            for realization in scenario["realizations"]:
                locale = realization["locale"]
                form = realization["form"]
                realization["prompt_id"] = f"{scenario['scenario_id']}.{locale}.{form}"
                if locale == "en-US" and form == "canonical":
                    phrase = "shared phrase alpha beta gamma delta"
                    suffix = f"unique canonical {index}"
                    content = f"{phrase if index < 2 else 'different phrase alpha beta gamma'} {suffix}"
                else:
                    content = f"unique {locale} {form} scenario number {index}"
                realization["messages"] = [{"role": "user", "content": content}]
            scenarios.append(scenario)
        errors, _warnings, stats = _quality_lint(scenarios, manifest, ROOT)
        self.assertGreater(stats["phrase_concentration_violation_count"], 0)
        self.assertTrue(any("phrase concentration exceeds" in error for error in errors))

    def test_semantic_title_base_duplicate_is_release_error(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        source_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        left = copy.deepcopy(load_json(source_path))
        right = copy.deepcopy(left)
        right["scenario_id"] = "rwpk.synthetic.semantic_duplicate.0002"
        right["semantic_group_id"] = "rwpg.synthetic.semantic_duplicate.0002"
        right["coverage"]["block_id"] = "synthetic.other_block.cb8"
        left["scenario_id"] = "rwpk.synthetic.semantic_duplicate.0001"
        left["semantic_group_id"] = "rwpg.synthetic.semantic_duplicate.0001"
        left["coverage"]["block_id"] = "synthetic.first_block.cb8"
        for scenario in (left, right):
            for realization in scenario["realizations"]:
                realization["prompt_id"] = (
                    f"{scenario['scenario_id']}.{realization['locale']}.{realization['form']}"
                )
        errors, _warnings, stats = _quality_lint([left, right], manifest, ROOT)
        self.assertEqual(stats["semantic_title_duplicate_groups"], 1)
        self.assertTrue(any("duplicate normalized title bases" in error for error in errors))

    def test_rendered_message_grammar_gate_catches_known_b_defects(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        catalog = load_json(ROOT / "data/v0.1/catalog.json")
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        broken = copy.deepcopy(load_json(scenario_path))
        for realization in broken["realizations"]:
            if realization["form"] != "naturalistic":
                continue
            realization["messages"] = [{
                "role": "user",
                "content": "4일 후 시작라고 요청을 정리해줘" if realization["locale"] == "ko-KR"
                else "The option a entry is at 4 p.m;",
            }]
        errors = _validate_scenario(broken, Path("synthetic-broken.json"), manifest, catalog)
        self.assertTrue(any("known Korean grammar defect" in error for error in errors))
        self.assertTrue(any("known English capitalization or punctuation defect" in error for error in errors))

    def test_transport_retrieval_tail_must_fit_semantic_context(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        catalog = load_json(ROOT / "data/v0.1/catalog.json")
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        broken = copy.deepcopy(load_json(scenario_path))
        broken["title"] = {"ko": "제품 보증 비교", "en": "Product warranty comparison"}
        broken["task"]["primary_domain"] = "customer_support_success"
        broken["task"]["domain_tags"] = []
        broken["task"]["user_goal"] = {
            "ko": "제품 보증 기간과 수리 제외 조건을 비교해줘",
            "en": "Compare warranty periods and repair exclusions.",
        }
        for realization in broken["realizations"]:
            suffix = (
                " 공식 자료에서 도시·노선·운행일이 비면 알려줘"
                if realization["locale"] == "ko-KR"
                else " Check official material for city, route, and service day."
            )
            realization["messages"][0]["content"] += suffix
        errors = _validate_scenario(
            broken, Path("synthetic-transport-tail.json"), manifest, catalog
        )
        self.assertTrue(any("transport-specific retrieval tail" in error for error in errors))

    def test_critical_fact_gate_catches_dropped_number_and_possessive(self) -> None:
        manifest = load_json(DEFAULT_MANIFEST)
        catalog = load_json(ROOT / "data/v0.1/catalog.json")
        scenario_path = sorted((ROOT / "data/v0.1/scenarios").rglob("*.json"))[0]
        broken = copy.deepcopy(load_json(scenario_path))
        canonical = next(
            item
            for item in broken["realizations"]
            if item["locale"] == "en-US" and item["form"] == "canonical"
        )
        naturalistic = next(
            item
            for item in broken["realizations"]
            if item["locale"] == "en-US" and item["form"] == "naturalistic"
        )
        canonical["messages"] = [{
            "role": "user",
            "content": "The team's budget is 30 dollars and the date is 2026-07-27.",
        }]
        naturalistic["messages"] = [{
            "role": "user",
            "content": "Teams need a budget and the date is 2026-07-27.",
        }]
        errors = _validate_scenario(
            broken, Path("synthetic-fact-loss.json"), manifest, catalog
        )
        self.assertTrue(any("drops canonical numeric fact" in error for error in errors))
        self.assertTrue(any("bare plural" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
