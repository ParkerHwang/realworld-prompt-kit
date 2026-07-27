# Worker report: intents 15–21

Generated against the authoritative v1.0 prompt-kit catalog recovered from the orchestrator handoff.

## Deliverable

- Semantic scenarios: **336**
- Prompt realizations: **1344** (ko/en canonical/naturalistic per scenario)
- Coverage blocks: **42**, each with exactly 8 rows
- Primary intents: planning_strategy_design=48, communication_collaboration_negotiation=40, one_off_tool_execution=56, automation_integration=56, operations_monitoring_improvement=48, coaching_conversational_support=40, ai_agent_meta=48
- Schema: `realworld-prompt-kit.scenario/1.0.0`
- Provenance: synthetic; `contains_personal_data=false`; MIT

## Block quota

| Intent | Block | Scenarios |
| --- | --- | ---: |
| `ai_agent_meta` | `boundary_ambiguity` | 8 |
| `ai_agent_meta` | `canonical` | 8 |
| `ai_agent_meta` | `execution_failure_recovery` | 8 |
| `ai_agent_meta` | `input_robustness` | 8 |
| `ai_agent_meta` | `meta_evaluation` | 8 |
| `ai_agent_meta` | `verification_uncertainty` | 8 |
| `automation_integration` | `boundary_ambiguity` | 8 |
| `automation_integration` | `canonical` | 8 |
| `automation_integration` | `execution_failure_recovery` | 8 |
| `automation_integration` | `input_robustness` | 8 |
| `automation_integration` | `long_running_state` | 8 |
| `automation_integration` | `tradeoff_stakes` | 8 |
| `automation_integration` | `verification_uncertainty` | 8 |
| `coaching_conversational_support` | `audience_context_shift` | 8 |
| `coaching_conversational_support` | `boundary_ambiguity` | 8 |
| `coaching_conversational_support` | `canonical` | 8 |
| `coaching_conversational_support` | `human_boundary` | 8 |
| `coaching_conversational_support` | `tradeoff_stakes` | 8 |
| `communication_collaboration_negotiation` | `audience_context_shift` | 8 |
| `communication_collaboration_negotiation` | `boundary_ambiguity` | 8 |
| `communication_collaboration_negotiation` | `canonical` | 8 |
| `communication_collaboration_negotiation` | `stakeholder_conflict` | 8 |
| `communication_collaboration_negotiation` | `tradeoff_stakes` | 8 |
| `one_off_tool_execution` | `boundary_ambiguity` | 8 |
| `one_off_tool_execution` | `canonical` | 8 |
| `one_off_tool_execution` | `execution_failure_recovery` | 8 |
| `one_off_tool_execution` | `format_semantic_preservation` | 8 |
| `one_off_tool_execution` | `input_robustness` | 8 |
| `one_off_tool_execution` | `tradeoff_stakes` | 8 |
| `one_off_tool_execution` | `verification_uncertainty` | 8 |
| `operations_monitoring_improvement` | `boundary_ambiguity` | 8 |
| `operations_monitoring_improvement` | `canonical` | 8 |
| `operations_monitoring_improvement` | `execution_failure_recovery` | 8 |
| `operations_monitoring_improvement` | `input_robustness` | 8 |
| `operations_monitoring_improvement` | `long_running_state` | 8 |
| `operations_monitoring_improvement` | `verification_uncertainty` | 8 |
| `planning_strategy_design` | `boundary_ambiguity` | 8 |
| `planning_strategy_design` | `canonical` | 8 |
| `planning_strategy_design` | `input_robustness` | 8 |
| `planning_strategy_design` | `stakeholder_conflict` | 8 |
| `planning_strategy_design` | `tradeoff_stakes` | 8 |
| `planning_strategy_design` | `verification_uncertainty` | 8 |

## Primary-domain distribution

| Domain | Primary scenarios |
| --- | ---: |
| `communication_meetings` | 14 |
| `construction_real_estate` | 5 |
| `creative_media` | 4 |
| `customer_support_success` | 26 |
| `data_analytics` | 18 |
| `education_research` | 38 |
| `energy_environment` | 1 |
| `finance_accounting_tax` | 12 |
| `government_public_policy` | 3 |
| `health_care` | 11 |
| `hr_people_labor` | 16 |
| `legal_compliance` | 4 |
| `manufacturing_quality` | 3 |
| `nonprofit_social_impact` | 1 |
| `office_admin` | 30 |
| `personal_everyday` | 20 |
| `privacy_security` | 18 |
| `project_product_management` | 13 |
| `retail_ecommerce` | 1 |
| `safety_emergency` | 8 |
| `sales_marketing` | 14 |
| `science_rd` | 11 |
| `software_it` | 28 |
| `strategy_business_operations` | 15 |
| `supply_chain_logistics` | 16 |
| `travel_hospitality` | 6 |

Assigned domain tags intentionally widen coverage across office, general-life, business, education, personal, regulated, industry, creative, and technical catalog domains. Software/IT and data analytics are used as supporting or primary domains only where the task requires them.

## Naturalistic profile distribution

| Profile | Scenario assignments |
| --- | ---: |
| `anaphora_prior_context` | 42 |
| `code_switching_jargon` | 42 |
| `emoji_shorthand` | 42 |
| `followup_without_restatement` | 168 |
| `hedged_exploratory_request` | 42 |
| `implicit_goal_or_output` | 42 |
| `interleaved_instruction_and_paste` | 42 |
| `message_burst` | 168 |
| `mid_task_change` | 42 |
| `missing_decisive_detail` | 42 |
| `multi_intent_mixed_priority` | 42 |
| `ocr_copy_format_noise` | 42 |
| `rambling_stream` | 42 |
| `resume_after_interruption` | 42 |
| `self_correction_scope_shift` | 42 |
| `speech_to_text_disfluency` | 42 |
| `terse_fragment` | 42 |
| `typo_spacing_punctuation` | 42 |

## Semantic breadth audit

- Normalized semantic fields checked across blocks: **1344** (title, topic, evidence facts, and requested deliverable per scenario).
- Unique normalized semantic field values: **1344**.
- Duplicate normalized titles, topics, evidence fixtures, or deliverables are treated as generator errors; block modifiers do not count as new breadth.

## Similarity review

Canonical↔naturalistic similarity was measured independently for each locale using normalized sequence ratio and token-set Jaccard overlap. Pairs at or above 0.85 were individually investigated and documented below.

| Locale | Sequence ratio | Token Jaccard |
| --- | --- | --- |
| `ko-KR` | min=0.072, mean=0.615, max=0.800 | min=0.254, mean=0.388, max=0.593 |
| `en-US` | min=0.003, mean=0.178, max=0.799 | min=0.333, mean=0.455, max=0.635 |
- High-similarity pairs investigated: **0**.

## Per-block semantic-fit samples

One first-row scenario from every declared block was inspected for task/domain fit; domain assignment follows the described latent task rather than block rotation.

| Block | Row | Primary domain | Topic sample | Supporting tags |
| --- | ---: | --- | --- | --- |
| `ai_agent_meta.boundary_ambiguity.cb8` | 1 | `software_it` | defining what a smart agent should do | `education_research`, `strategy_business_operations` |
| `ai_agent_meta.canonical.cb8` | 1 | `education_research` | evaluating a prompt against a task scenario | `education_research`, `communication_meetings` |
| `ai_agent_meta.execution_failure_recovery.cb8` | 1 | `software_it` | recovering from an agent tool timeout | `education_research`, `strategy_business_operations` |
| `ai_agent_meta.input_robustness.cb8` | 1 | `privacy_security` | an agent policy from contradictory notes | `education_research`, `communication_meetings` |
| `ai_agent_meta.meta_evaluation.cb8` | 1 | `education_research` | judging two prompts without revealing their identities | `communication_meetings`, `data_analytics` |
| `ai_agent_meta.verification_uncertainty.cb8` | 1 | `software_it` | verifying an agent's tool-call claim | `education_research`, `data_analytics` |
| `automation_integration.boundary_ambiguity.cb8` | 1 | `office_admin` | automating report distribution | `privacy_security`, `data_analytics` |
| `automation_integration.canonical.cb8` | 1 | `education_research` | a form-to-acknowledgement workflow | `office_admin`, `communication_meetings` |
| `automation_integration.execution_failure_recovery.cb8` | 1 | `software_it` | recovering from duplicate webhook delivery | `strategy_business_operations`, `data_analytics` |
| `automation_integration.input_robustness.cb8` | 1 | `office_admin` | turning a messy SOP into an automation | `strategy_business_operations`, `legal_compliance` |
| `automation_integration.long_running_state.cb8` | 1 | `sales_marketing` | a month-long campaign tracking workflow | `data_analytics`, `strategy_business_operations` |
| `automation_integration.tradeoff_stakes.cb8` | 1 | `office_admin` | choosing a no-code or scripted workflow | `software_it`, `strategy_business_operations` |
| `automation_integration.verification_uncertainty.cb8` | 1 | `software_it` | a dual-write synchronization workflow | `data_analytics`, `strategy_business_operations` |
| `coaching_conversational_support.audience_context_shift.cb8` | 1 | `hr_people_labor` | coaching people at different experience levels | `communication_meetings`, `project_product_management` |
| `coaching_conversational_support.boundary_ambiguity.cb8` | 1 | `personal_everyday` | support for feeling overwhelmed | `health_care`, `communication_meetings` |
| `coaching_conversational_support.canonical.cb8` | 1 | `communication_meetings` | preparing for a difficult work conversation | `hr_people_labor`, `project_product_management` |
| `coaching_conversational_support.human_boundary.cb8` | 1 | `personal_everyday` | supporting someone grieving at work | `hr_people_labor`, `communication_meetings` |
| `coaching_conversational_support.tradeoff_stakes.cb8` | 1 | `communication_meetings` | coaching that balances empathy and accountability | `hr_people_labor`, `project_product_management` |
| `communication_collaboration_negotiation.audience_context_shift.cb8` | 1 | `software_it` | a technical release note for customers | `customer_support_success`, `sales_marketing` |
| `communication_collaboration_negotiation.boundary_ambiguity.cb8` | 1 | `project_product_management` | whether to announce a project delay | `communication_meetings`, `customer_support_success` |
| `communication_collaboration_negotiation.canonical.cb8` | 1 | `project_product_management` | a project status update for executives | `communication_meetings`, `strategy_business_operations` |
| `communication_collaboration_negotiation.stakeholder_conflict.cb8` | 1 | `project_product_management` | a cross-team deadline negotiation | `communication_meetings`, `sales_marketing` |
| `communication_collaboration_negotiation.tradeoff_stakes.cb8` | 1 | `customer_support_success` | a customer reply balancing brevity and completeness | `communication_meetings`, `office_admin` |
| `one_off_tool_execution.boundary_ambiguity.cb8` | 1 | `office_admin` | a calendar update with an ambiguous target | `communication_meetings`, `personal_everyday` |
| `one_off_tool_execution.canonical.cb8` | 1 | `office_admin` | creating a calendar event for a design review | `communication_meetings`, `project_product_management` |
| `one_off_tool_execution.execution_failure_recovery.cb8` | 1 | `office_admin` | recovering from a calendar tool timeout | `software_it`, `education_research` |
| `one_off_tool_execution.format_semantic_preservation.cb8` | 1 | `data_analytics` | converting a CSV export to JSON | `office_admin`, `software_it` |
| `one_off_tool_execution.input_robustness.cb8` | 1 | `data_analytics` | preparing a malformed CSV upload | `software_it`, `office_admin` |
| `one_off_tool_execution.tradeoff_stakes.cb8` | 1 | `office_admin` | choosing between deletion and archiving | `privacy_security`, `legal_compliance` |
| `one_off_tool_execution.verification_uncertainty.cb8` | 1 | `office_admin` | preparing an archive action with a backup check | `software_it`, `privacy_security` |
| `operations_monitoring_improvement.boundary_ambiguity.cb8` | 1 | `software_it` | a service-health monitoring definition | `strategy_business_operations`, `customer_support_success` |
| `operations_monitoring_improvement.canonical.cb8` | 1 | `project_product_management` | a weekly team-capacity dashboard | `data_analytics`, `office_admin` |
| `operations_monitoring_improvement.execution_failure_recovery.cb8` | 1 | `data_analytics` | recovering from a stale operations dashboard | `strategy_business_operations`, `office_admin` |
| `operations_monitoring_improvement.input_robustness.cb8` | 1 | `data_analytics` | a KPI review from conflicting spreadsheets | `sales_marketing`, `office_admin` |
| `operations_monitoring_improvement.long_running_state.cb8` | 1 | `project_product_management` | a 90-day rollout monitoring plan | `strategy_business_operations`, `data_analytics` |
| `operations_monitoring_improvement.verification_uncertainty.cb8` | 1 | `data_analytics` | a KPI definition audit | `strategy_business_operations`, `office_admin` |
| `planning_strategy_design.boundary_ambiguity.cb8` | 1 | `strategy_business_operations` | the scope of a budget request | `office_admin`, `finance_accounting_tax` |
| `planning_strategy_design.canonical.cb8` | 1 | `project_product_management` | a product launch readiness sequence | `communication_meetings`, `office_admin` |
| `planning_strategy_design.input_robustness.cb8` | 1 | `communication_meetings` | a plan from conflicting meeting notes | `project_product_management`, `office_admin` |
| `planning_strategy_design.stakeholder_conflict.cb8` | 1 | `office_admin` | an office-relocation decision plan | `strategy_business_operations`, `construction_real_estate` |
| `planning_strategy_design.tradeoff_stakes.cb8` | 1 | `hr_people_labor` | remote and hybrid work policy options | `office_admin`, `privacy_security` |
| `planning_strategy_design.verification_uncertainty.cb8` | 1 | `supply_chain_logistics` | a vendor proposal plan with evidence checks | `manufacturing_quality`, `strategy_business_operations` |

## Corpus phrase concentration and language scan

Distinct-document counts for normalized 6-, 7-, and 8-token n-grams were checked separately by locale and form. No repeated naturalistic phrase may exceed 20% of the 336 rows.

| Locale | Form | N | Most common n-gram | Rows | Share |
| --- | --- | ---: | --- | ---: | ---: |
| `en-US` | `canonical` | 6 | prepare a one time tool action | 16 | 4.8% |
| `en-US` | `canonical` | 7 | messy planning inputs into a workable plan | 8 | 2.4% |
| `en-US` | `canonical` | 8 | turn these messy planning inputs into a workable | 8 | 2.4% |
| `en-US` | `naturalistic` | 6 | i m trying to sort out | 42 | 12.5% |
| `en-US` | `naturalistic` | 7 | but here s what i actually know | 42 | 12.5% |
| `en-US` | `naturalistic` | 8 | in mind if one missing detail would change | 42 | 12.5% |
| `ko-KR` | `canonical` | 6 | 범위가 덜 정해진 다음 계획을 임시안으로 | 8 | 2.4% |
| `ko-KR` | `canonical` | 7 | 범위가 덜 정해진 다음 계획을 임시안으로 잡아줘 | 8 | 2.4% |
| `ko-KR` | `canonical` | 8 | 다음 일회성 도구 작업을 실행할 수 있게 준비해줘 | 8 | 2.4% |
| `ko-KR` | `naturalistic` | 6 | 앞서 정한 범위는 유지해줘 결정을 바꿀 | 42 | 12.5% |
| `ko-KR` | `naturalistic` | 7 | 정한 범위는 유지해줘 결정을 바꿀 정보가 빠졌다면 | 42 | 12.5% |
| `ko-KR` | `naturalistic` | 8 | 좋겠어 앞서 정한 범위는 유지해줘 결정을 바꿀 정보가 | 42 | 12.5% |

- Concentration violations: **0**.
- Naturalistic grammar-duplication hits: **0**.
- Generated-label leakage hits in naturalistic messages: **0**.
- The word `canonical`, when present in a message, is treated as task content only when it is part of a scenario fact; schema/form labels are not inserted into naturalistic message text.

## Validation performed

- JSON was serialized with Python's standard JSON encoder for every file.
- Every block was checked for all seven binary facet levels and all strength-2 facet pairs.
- Scenario IDs and prompt IDs were checked for global uniqueness within this worker slice.
- Every scenario has exactly four realizations and every naturalistic realization has catalogued profile IDs.
- Primary domains and domain tags were checked against the authoritative allowed catalog IDs; software/data primary-domain share was checked against the 20% ceiling.
- Normalized title/topic/facts/deliverable uniqueness was checked across all 42 blocks before generation.
- Generator checks: **PASS**.
