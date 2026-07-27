# v1 Coverage Report

- Manifest: `data/v1.0/manifest.json`
- Validation: **PASS**
- Manifest status: **`release_candidate`**
- Semantic scenarios: **880**
- CB8 blocks: **110**
- Prompt realizations: **3520**
- Broad ratio: **69.3%**
- Software + data ratio: **11.1%**
- Scenario statuses: **draft=656, reviewed=224**

## Intent quotas

| Intent | Scenarios |
| --- | ---: |
| `ai_agent_meta` | 48 |
| `automation_integration` | 56 |
| `classification_organization` | 40 |
| `coaching_conversational_support` | 40 |
| `communication_collaboration_negotiation` | 40 |
| `creative_ideation` | 32 |
| `decision_recommendation` | 48 |
| `diagnosis_root_cause` | 48 |
| `evaluation_review_audit` | 48 |
| `explanation_teaching` | 32 |
| `extraction_parsing` | 24 |
| `forecasting_scenario_risk` | 48 |
| `information_retrieval` | 32 |
| `one_off_tool_execution` | 56 |
| `operations_monitoring_improvement` | 48 |
| `planning_strategy_design` | 48 |
| `practical_writing` | 40 |
| `qualitative_analysis` | 40 |
| `quantitative_formal_analysis` | 48 |
| `summarization_synthesis` | 32 |
| `transformation_rewriting` | 32 |

## Primary-domain counts

| Domain | Scenarios |
| --- | ---: |
| `agriculture_food` | 2 |
| `communication_meetings` | 42 |
| `construction_real_estate` | 6 |
| `creative_media` | 8 |
| `customer_support_success` | 54 |
| `data_analytics` | 34 |
| `education_research` | 93 |
| `energy_environment` | 4 |
| `finance_accounting_tax` | 14 |
| `general_knowledge` | 30 |
| `government_public_policy` | 7 |
| `health_care` | 13 |
| `hr_people_labor` | 19 |
| `legal_compliance` | 7 |
| `manufacturing_quality` | 6 |
| `nonprofit_social_impact` | 4 |
| `office_admin` | 136 |
| `personal_everyday` | 117 |
| `privacy_security` | 19 |
| `project_product_management` | 46 |
| `retail_ecommerce` | 4 |
| `safety_emergency` | 11 |
| `sales_marketing` | 44 |
| `science_rd` | 14 |
| `software_it` | 64 |
| `strategy_business_operations` | 48 |
| `supply_chain_logistics` | 18 |
| `travel_hospitality` | 16 |

## Scenario status distribution

| Status | Scenarios |
| --- | ---: |
| `draft` | 656 |
| `reviewed` | 224 |

## Naturalistic profile counts

| Profile | Scenario rows |
| --- | ---: |
| `anaphora_prior_context` | 115 |
| `code_switching_jargon` | 99 |
| `colloquial_slang_dialect` | 20 |
| `contradictory_constraints` | 62 |
| `emoji_shorthand` | 102 |
| `followup_without_restatement` | 276 |
| `frustration_urgency_emotion` | 96 |
| `hedged_exploratory_request` | 119 |
| `implicit_goal_or_output` | 114 |
| `implicit_permission_or_authority` | 40 |
| `indirect_polite_request` | 84 |
| `interleaved_instruction_and_paste` | 150 |
| `message_burst` | 224 |
| `mid_task_change` | 63 |
| `missing_decisive_detail` | 214 |
| `multi_intent_mixed_priority` | 120 |
| `ocr_copy_format_noise` | 68 |
| `rambling_stream` | 103 |
| `resume_after_interruption` | 94 |
| `self_correction_scope_shift` | 113 |
| `speech_to_text_disfluency` | 100 |
| `terse_fragment` | 105 |
| `typo_spacing_punctuation` | 56 |
| `untrusted_embedded_instruction` | 15 |

## Quality lint

- Per-scenario validation errors: 0
- Non-transport context retrieval-tail errors: 0
- Critical numeric/possessive fact errors: 0
- Similarity warnings: 9 (0.5%)
- Similarity failures: 0 (0.0%)
- Exact duplicate groups: 0
- Normalized duplicate groups: 0
- Semantic title duplicate groups: 0
- Semantic goal duplicate groups: 0
- High canonical cross-block similarity pairs: 0

## Exact six-token phrase gate

- Metric: `distinct-scenario presence count for exact six-token n-grams; every longer n-gram has a six-token prefix`
- Union denominator: **880 semantic scenarios per locale/form**
- Union violations: **0**
- Union review candidates: **0**

| Partition | Scenarios | Prompt realizations | Phrase violations | Phrase reviews |
| --- | ---: | ---: | ---: | ---: |
| `core-worker-1` | 224 | 896 | 0 | 0 |
| `core-worker-2` | 320 | 1280 | 0 | 0 |
| `core-worker-3` | 336 | 1344 | 0 | 0 |

The scan counts distinct-scenario presence for exact six-token n-grams independently by locale/form. A longer repeated n-gram is covered by its six-token prefix; no generic boilerplate is whitelisted.

OpenSocrates method routing and adapter conformance remain planned, unpopulated extension suites and receive no broad-core coverage credit.

## Integration evidence

Worker source refs and integration-owned corrections are recorded in the manifest and worker reports; source-reported QA is not substituted for the independent integration gates.

- `core-worker-1` source/base `d737e782f60ae9a1441f3ba5c92fdc71bffd8d7a`; post-repair errors=0; overlay=`reports/workers/intents-01-07.md`
- `core-worker-2` source/base `f2662069ac556f125054ca59953467edcb2af033`; post-repair errors=0; overlay=`reports/workers/intents-08-14.md`
  - B correction ledger: english_sentence_boundary_capitalization=360, korean_code_switch_profile=39, resume_profile=9, untrusted_instruction_profile=7, numeric_fact_restoration=5, rambling_length_profile=1
- `core-worker-3` source/base `9b73b72b6871c2369d82f649bd768d4597384803`; post-repair errors=0; overlay=`reports/workers/intents-15-21.md`
- Coverage audit `16ae05cdf2fba02ac9827fca1c10e26b77f3acb8` is retained as `dated_pre_generation_baseline` at `reports/coverage/coverage-audit.json`.

## Block review samples

The release review samples one scenario from every observed CB8 block. The sampled IDs are recorded in the JSON report for traceability.

- `ai_agent_meta.boundary_ambiguity.cb8` → `rwpk.ai_agent_meta.boundary_ambiguity.0001`
- `ai_agent_meta.canonical.cb8` → `rwpk.ai_agent_meta.canonical.0001`
- `ai_agent_meta.execution_failure_recovery.cb8` → `rwpk.ai_agent_meta.execution_failure_recovery.0001`
- `ai_agent_meta.input_robustness.cb8` → `rwpk.ai_agent_meta.input_robustness.0001`
- `ai_agent_meta.meta_evaluation.cb8` → `rwpk.ai_agent_meta.meta_evaluation.0001`
- `ai_agent_meta.verification_uncertainty.cb8` → `rwpk.ai_agent_meta.verification_uncertainty.0001`
- `automation_integration.boundary_ambiguity.cb8` → `rwpk.automation_integration.boundary_ambiguity.0001`
- `automation_integration.canonical.cb8` → `rwpk.automation_integration.canonical.0001`
- `automation_integration.execution_failure_recovery.cb8` → `rwpk.automation_integration.execution_failure_recovery.0001`
- `automation_integration.input_robustness.cb8` → `rwpk.automation_integration.input_robustness.0001`
- `automation_integration.long_running_state.cb8` → `rwpk.automation_integration.long_running_state.0001`
- `automation_integration.tradeoff_stakes.cb8` → `rwpk.automation_integration.tradeoff_stakes.0001`
- `automation_integration.verification_uncertainty.cb8` → `rwpk.automation_integration.verification_uncertainty.0001`
- `classification_organization.boundary_ambiguity.cb8` → `rwpk.classification_organization.boundary_ambiguity_01.8009`
- `classification_organization.canonical.cb8` → `rwpk.classification_organization.canonical_01.8001`
- `classification_organization.input_robustness.cb8` → `rwpk.classification_organization.input_robustness_01.8017`
- `classification_organization.multi_criteria_boundary.cb8` → `rwpk.classification_organization.multi_criteria_boundary_01.8025`
- `classification_organization.verification_uncertainty.cb8` → `rwpk.classification_organization.verification_uncertainty_01.8033`
- `coaching_conversational_support.audience_context_shift.cb8` → `rwpk.coaching_conversational_support.audience_context_shift.0001`
- `coaching_conversational_support.boundary_ambiguity.cb8` → `rwpk.coaching_conversational_support.boundary_ambiguity.0001`
- `coaching_conversational_support.canonical.cb8` → `rwpk.coaching_conversational_support.canonical.0001`
- `coaching_conversational_support.human_boundary.cb8` → `rwpk.coaching_conversational_support.human_boundary.0001`
- `coaching_conversational_support.tradeoff_stakes.cb8` → `rwpk.coaching_conversational_support.tradeoff_stakes.0001`
- `communication_collaboration_negotiation.audience_context_shift.cb8` → `rwpk.communication_collaboration_negotiation.audience_context_shift.0001`
- `communication_collaboration_negotiation.boundary_ambiguity.cb8` → `rwpk.communication_collaboration_negotiation.boundary_ambiguity.0001`
- `communication_collaboration_negotiation.canonical.cb8` → `rwpk.communication_collaboration_negotiation.canonical.0001`
- `communication_collaboration_negotiation.stakeholder_conflict.cb8` → `rwpk.communication_collaboration_negotiation.stakeholder_conflict.0001`
- `communication_collaboration_negotiation.tradeoff_stakes.cb8` → `rwpk.communication_collaboration_negotiation.tradeoff_stakes.0001`
- `creative_ideation.audience_context_shift.cb8` → `rwpk.creative_ideation.audience_context_shift.0001`
- `creative_ideation.boundary_ambiguity.cb8` → `rwpk.creative_ideation.boundary_ambiguity.0001`
- `creative_ideation.canonical.cb8` → `rwpk.creative_ideation.canonical.0001`
- `creative_ideation.creativity_diversity.cb8` → `rwpk.creative_ideation.creativity_diversity.0001`
- `decision_recommendation.audience_context_shift.cb8` → `rwpk.decision_recommendation.audience_context_shift_01.8297`
- `decision_recommendation.boundary_ambiguity.cb8` → `rwpk.decision_recommendation.boundary_ambiguity_01.8281`
- `decision_recommendation.canonical.cb8` → `rwpk.decision_recommendation.canonical_01.8273`
- `decision_recommendation.input_robustness.cb8` → `rwpk.decision_recommendation.input_robustness_01.8289`
- `decision_recommendation.tradeoff_stakes.cb8` → `rwpk.decision_recommendation.tradeoff_stakes_01.8313`
- `decision_recommendation.verification_uncertainty.cb8` → `rwpk.decision_recommendation.verification_uncertainty_01.8305`
- `diagnosis_root_cause.boundary_ambiguity.cb8` → `rwpk.diagnosis_root_cause.boundary_ambiguity_01.8137`
- `diagnosis_root_cause.canonical.cb8` → `rwpk.diagnosis_root_cause.canonical_01.8129`
- `diagnosis_root_cause.competing_hypotheses.cb8` → `rwpk.diagnosis_root_cause.competing_hypotheses_01.8153`
- `diagnosis_root_cause.input_robustness.cb8` → `rwpk.diagnosis_root_cause.input_robustness_01.8145`
- `diagnosis_root_cause.tradeoff_stakes.cb8` → `rwpk.diagnosis_root_cause.tradeoff_stakes_01.8169`
- `diagnosis_root_cause.verification_uncertainty.cb8` → `rwpk.diagnosis_root_cause.verification_uncertainty_01.8161`
- `evaluation_review_audit.boundary_ambiguity.cb8` → `rwpk.evaluation_review_audit.boundary_ambiguity_01.8233`
- `evaluation_review_audit.canonical.cb8` → `rwpk.evaluation_review_audit.canonical_01.8225`
- `evaluation_review_audit.input_robustness.cb8` → `rwpk.evaluation_review_audit.input_robustness_01.8241`
- `evaluation_review_audit.multi_criteria_boundary.cb8` → `rwpk.evaluation_review_audit.multi_criteria_boundary_01.8249`
- `evaluation_review_audit.tradeoff_stakes.cb8` → `rwpk.evaluation_review_audit.tradeoff_stakes_01.8265`
- `evaluation_review_audit.verification_uncertainty.cb8` → `rwpk.evaluation_review_audit.verification_uncertainty_01.8257`
- `explanation_teaching.audience_context_shift.cb8` → `rwpk.explanation_teaching.audience_context_shift.0001`
- `explanation_teaching.boundary_ambiguity.cb8` → `rwpk.explanation_teaching.boundary_ambiguity.0001`
- `explanation_teaching.canonical.cb8` → `rwpk.explanation_teaching.canonical.0001`
- `explanation_teaching.input_robustness.cb8` → `rwpk.explanation_teaching.input_robustness.0001`
- `extraction_parsing.boundary_ambiguity.cb8` → `rwpk.extraction_parsing.boundary_ambiguity.0001`
- `extraction_parsing.canonical.cb8` → `rwpk.extraction_parsing.canonical.0001`
- `extraction_parsing.input_robustness.cb8` → `rwpk.extraction_parsing.input_robustness.0001`
- `forecasting_scenario_risk.boundary_ambiguity.cb8` → `rwpk.forecasting_scenario_risk.boundary_ambiguity_01.8185`
- `forecasting_scenario_risk.canonical.cb8` → `rwpk.forecasting_scenario_risk.canonical_01.8177`
- `forecasting_scenario_risk.forecast_reference_class.cb8` → `rwpk.forecasting_scenario_risk.forecast_reference_class_01.8201`
- `forecasting_scenario_risk.input_robustness.cb8` → `rwpk.forecasting_scenario_risk.input_robustness_01.8193`
- `forecasting_scenario_risk.tradeoff_stakes.cb8` → `rwpk.forecasting_scenario_risk.tradeoff_stakes_01.8217`
- `forecasting_scenario_risk.verification_uncertainty.cb8` → `rwpk.forecasting_scenario_risk.verification_uncertainty_01.8209`
- `information_retrieval.boundary_ambiguity.cb8` → `rwpk.information_retrieval.boundary_ambiguity.0001`
- `information_retrieval.canonical.cb8` → `rwpk.information_retrieval.canonical.0001`
- `information_retrieval.freshness_source_conflict.cb8` → `rwpk.information_retrieval.freshness_source_conflict.0001`
- `information_retrieval.input_robustness.cb8` → `rwpk.information_retrieval.input_robustness.0001`
- `one_off_tool_execution.boundary_ambiguity.cb8` → `rwpk.one_off_tool_execution.boundary_ambiguity.0001`
- `one_off_tool_execution.canonical.cb8` → `rwpk.one_off_tool_execution.canonical.0001`
- `one_off_tool_execution.execution_failure_recovery.cb8` → `rwpk.one_off_tool_execution.execution_failure_recovery.0001`
- `one_off_tool_execution.format_semantic_preservation.cb8` → `rwpk.one_off_tool_execution.format_semantic_preservation.0001`
- `one_off_tool_execution.input_robustness.cb8` → `rwpk.one_off_tool_execution.input_robustness.0001`
- `one_off_tool_execution.tradeoff_stakes.cb8` → `rwpk.one_off_tool_execution.tradeoff_stakes.0001`
- `one_off_tool_execution.verification_uncertainty.cb8` → `rwpk.one_off_tool_execution.verification_uncertainty.0001`
- `operations_monitoring_improvement.boundary_ambiguity.cb8` → `rwpk.operations_monitoring_improvement.boundary_ambiguity.0001`
- `operations_monitoring_improvement.canonical.cb8` → `rwpk.operations_monitoring_improvement.canonical.0001`
- `operations_monitoring_improvement.execution_failure_recovery.cb8` → `rwpk.operations_monitoring_improvement.execution_failure_recovery.0001`
- `operations_monitoring_improvement.input_robustness.cb8` → `rwpk.operations_monitoring_improvement.input_robustness.0001`
- `operations_monitoring_improvement.long_running_state.cb8` → `rwpk.operations_monitoring_improvement.long_running_state.0001`
- `operations_monitoring_improvement.verification_uncertainty.cb8` → `rwpk.operations_monitoring_improvement.verification_uncertainty.0001`
- `planning_strategy_design.boundary_ambiguity.cb8` → `rwpk.planning_strategy_design.boundary_ambiguity.0001`
- `planning_strategy_design.canonical.cb8` → `rwpk.planning_strategy_design.canonical.0001`
- `planning_strategy_design.input_robustness.cb8` → `rwpk.planning_strategy_design.input_robustness.0001`
- `planning_strategy_design.stakeholder_conflict.cb8` → `rwpk.planning_strategy_design.stakeholder_conflict.0001`
- `planning_strategy_design.tradeoff_stakes.cb8` → `rwpk.planning_strategy_design.tradeoff_stakes.0001`
- `planning_strategy_design.verification_uncertainty.cb8` → `rwpk.planning_strategy_design.verification_uncertainty.0001`
- `practical_writing.audience_context_shift.cb8` → `rwpk.practical_writing.audience_context_shift.0001`
- `practical_writing.boundary_ambiguity.cb8` → `rwpk.practical_writing.boundary_ambiguity.0001`
- `practical_writing.canonical.cb8` → `rwpk.practical_writing.canonical.0001`
- `practical_writing.format_semantic_preservation.cb8` → `rwpk.practical_writing.format_semantic_preservation.0001`
- `practical_writing.verification_uncertainty.cb8` → `rwpk.practical_writing.verification_uncertainty.0001`
- `qualitative_analysis.boundary_ambiguity.cb8` → `rwpk.qualitative_analysis.boundary_ambiguity_01.8049`
- `qualitative_analysis.canonical.cb8` → `rwpk.qualitative_analysis.canonical_01.8041`
- `qualitative_analysis.input_robustness.cb8` → `rwpk.qualitative_analysis.input_robustness_01.8057`
- `qualitative_analysis.tradeoff_stakes.cb8` → `rwpk.qualitative_analysis.tradeoff_stakes_01.8073`
- `qualitative_analysis.verification_uncertainty.cb8` → `rwpk.qualitative_analysis.verification_uncertainty_01.8065`
- `quantitative_formal_analysis.boundary_ambiguity.cb8` → `rwpk.quantitative_formal_analysis.boundary_ambiguity_01.8089`
- `quantitative_formal_analysis.canonical.cb8` → `rwpk.quantitative_formal_analysis.canonical_01.8081`
- `quantitative_formal_analysis.format_semantic_preservation.cb8` → `rwpk.quantitative_formal_analysis.format_semantic_preservation_01.8105`
- `quantitative_formal_analysis.input_robustness.cb8` → `rwpk.quantitative_formal_analysis.input_robustness_01.8097`
- `quantitative_formal_analysis.tradeoff_stakes.cb8` → `rwpk.quantitative_formal_analysis.tradeoff_stakes_01.8121`
- `quantitative_formal_analysis.verification_uncertainty.cb8` → `rwpk.quantitative_formal_analysis.verification_uncertainty_01.8113`
- `summarization_synthesis.audience_context_shift.cb8` → `rwpk.summarization_synthesis.audience_context_shift.0001`
- `summarization_synthesis.boundary_ambiguity.cb8` → `rwpk.summarization_synthesis.boundary_ambiguity.0001`
- `summarization_synthesis.canonical.cb8` → `rwpk.summarization_synthesis.canonical.0001`
- `summarization_synthesis.input_robustness.cb8` → `rwpk.summarization_synthesis.input_robustness.0001`
- `transformation_rewriting.audience_context_shift.cb8` → `rwpk.transformation_rewriting.audience_context_shift.0001`
- `transformation_rewriting.canonical.cb8` → `rwpk.transformation_rewriting.canonical.0001`
- `transformation_rewriting.format_semantic_preservation.cb8` → `rwpk.transformation_rewriting.format_semantic_preservation.0001`
- `transformation_rewriting.input_robustness.cb8` → `rwpk.transformation_rewriting.input_robustness.0001`

## Warnings

- partition core-worker-3: quality: 9 locale pairs exceed similarity warning threshold 0.75
- quality: 9 locale pairs exceed similarity warning threshold 0.75
