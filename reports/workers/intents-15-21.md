# Worker report: intents 15–21

Generated against the authoritative v0.1 prompt-kit catalog recovered from the orchestrator handoff.

## Deliverable

- Semantic scenarios: **336**
- Prompt realizations: **1344** (ko/en canonical/naturalistic per scenario)
- Coverage blocks: **42**, each with exactly 8 rows
- Primary intents: planning_strategy_design=48, communication_collaboration_negotiation=40, one_off_tool_execution=56, automation_integration=56, operations_monitoring_improvement=48, coaching_conversational_support=40, ai_agent_meta=48
- Schema: `realworld-prompt-kit.scenario/0.1.0`
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

## Critical fact preservation review

- Stable fixture checks: **103** across all 336 KO/EN naturalistic scenario pairs; unresolved identifier/date/time/numeric fixture omissions: **0** (**0 unresolved**).
- The 42 row-1 KO/EN terse pairs were independently reviewed for qualitative evidence, requested artifact, and guardrail preservation: **0 decision-critical omissions**.
- A prior exact-token heuristic reported 29 apparent omissions; manual review classified them as intentional meaning-preserving shorthand or synonym changes (for example `45m`, `6mo`, `Thu`/`next Mon`, `+3`, `criteria`, `auto`, and `owner`), not missing facts. The exact-token heuristic is not used as the release gate.
- The accepted shorthand list is finite and documented in this report; no unresolved semantic fact mismatch remains.

## Similarity review

Canonical↔naturalistic similarity was measured independently for each locale using normalized sequence ratio and token-set Jaccard overlap. Pairs at or above 0.85 were individually investigated and documented below.

| Locale | Sequence ratio | Token Jaccard |
| --- | --- | --- |
| `ko-KR` | min=0.084, mean=0.592, max=0.771 | min=0.043, mean=0.397, max=0.610 |
| `en-US` | min=0.004, mean=0.278, max=0.835 | min=0.196, mean=0.468, max=0.694 |
- High-similarity pairs investigated: **0**.
- The two prior EN-US gate hits were human-reviewed and independently re-authored: `rwpk.planning_strategy_design.canonical.0004` (prior 0.862) is now 0.143, and `rwpk.planning_strategy_design.stakeholder_conflict.0004` (prior 0.869) is now 0.023; current high-similarity exceptions: **0**.

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

## Global naturalistic and behavior review

All 336 scenarios and all 1,344 realizations were scanned, with naturalistic messages checked for evidence of every declared profile, including message-burst structure and follow-ups that do not restate the topic.
- Observable naturalistic-feature issues: **0**.
- Korean/English grammar, particle/ending, capitalization, and punctuation issues: **0**.
- Response-mode validity or over-refusal issues: **0**.
- Benign coaching human-boundary over-refusal issues: **0**; the grief-support case is reviewed as `state_assumptions_and_answer` rather than `refuse_or_escalate`.
- `terse_fragment` KO length: **whitespace tokens median/max=17/24, chars median/max=62/82**; EN length: **words median/max=17/25, chars median/max=136/182**.
- Terse authoring uses **42 KO** and **42 EN** topic-specific fragments, independently phrased with fact fragments plus the requested artifact; manual semantic review found no decision-critical omissions. Abbreviations such as `Thu`, `6mo`, `+3`, and `dedup` are meaning-preserving shorthand.
- Critical fact preservation: **103** stable-fixture checks, **0** unresolved; all 42 terse KO/EN pairs had manual decision-critical-fact review.

## Profile realization audit

Each declared profile was checked against an observable criterion and one representative KO/EN sample ID was manually inspected after generation; evidence must cover every declared realization.

| Profile | Declared realizations | Evidence hits | KO sample | EN sample | Observable criterion |
| --- | ---: | ---: | --- | --- | --- |
| `anaphora_prior_context` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0002` | `rwpk.planning_strategy_design.canonical.0002` | explicit return/back-reference marker |
| `code_switching_jargon` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0006` | `rwpk.planning_strategy_design.canonical.0006` | API/workflow/schema or equivalent jargon marker |
| `emoji_shorthand` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0008` | `rwpk.planning_strategy_design.canonical.0008` | emoji or shorthand marker |
| `followup_without_restatement` | 336 | 336 | `rwpk.planning_strategy_design.canonical.0002` | `rwpk.planning_strategy_design.canonical.0002` | second message omits normalized scenario topic |
| `hedged_exploratory_request` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0003` | `rwpk.planning_strategy_design.canonical.0003` | conditional, tentative, or provisional wording marker |
| `implicit_goal_or_output` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0001` | `rwpk.planning_strategy_design.canonical.0001` | artifact remains a noun-phrase fragment; separators present; no direct imperative/request wording |
| `interleaved_instruction_and_paste` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0006` | `rwpk.planning_strategy_design.canonical.0006` | pasted notes/background/instruction marker |
| `message_burst` | 336 | 336 | `rwpk.planning_strategy_design.canonical.0002` | `rwpk.planning_strategy_design.canonical.0002` | at least two user messages |
| `mid_task_change` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0005` | `rwpk.planning_strategy_design.canonical.0005` | mid-task change/focus marker |
| `missing_decisive_detail` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0003` | `rwpk.planning_strategy_design.canonical.0003` | explicit missing/unknown/gap evidence marker |
| `multi_intent_mixed_priority` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0004` | `rwpk.planning_strategy_design.canonical.0004` | multiple loose-end/extra-scope marker |
| `ocr_copy_format_noise` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0007` | `rwpk.planning_strategy_design.canonical.0007` | OCR/copy/raw/noisy punctuation marker |
| `rambling_stream` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0004` | `rwpk.planning_strategy_design.canonical.0004` | multiple loose-end/extra-scope marker |
| `resume_after_interruption` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0002` | `rwpk.planning_strategy_design.canonical.0002` | explicit resume/continue marker |
| `self_correction_scope_shift` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0005` | `rwpk.planning_strategy_design.canonical.0005` | actually/focus/scope-shift marker |
| `speech_to_text_disfluency` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0008` | `rwpk.planning_strategy_design.canonical.0008` | speech hesitation/disfluency marker |
| `terse_fragment` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0001` | `rwpk.planning_strategy_design.canonical.0001` | one message; KO <=24 whitespace tokens/100 chars, EN <=28 words/190 chars; >=2 fragment separators; no direct-request opener |
| `typo_spacing_punctuation` | 84 | 84 | `rwpk.planning_strategy_design.canonical.0007` | `rwpk.planning_strategy_design.canonical.0007` | copy/OCR/raw/noisy punctuation marker |

## Corpus phrase concentration and language scan

The release gate is an exact-six-token presence gate: any non-whitelisted normalized 6-token n-gram present in more than 5.0% of a locale/form's 336 distinct documents fails release; normalized 7- and 8-token n-grams were also checked, so longer repeats cannot bypass the gate.
Counts are distinct documents rather than raw occurrences. The whitelist is empty; only unavoidable fixed fixture terms could be whitelisted, and none were exempted here.

| Locale | Form | N | Most common n-gram | Rows | Share |
| --- | --- | ---: | --- | ---: | ---: |
| `en-US` | `canonical` | 6 | prepare a one time tool action | 16 | 4.8% |
| `en-US` | `canonical` | 7 | messy planning inputs into a workable plan | 8 | 2.4% |
| `en-US` | `canonical` | 8 | messy planning inputs into a workable plan for | 8 | 2.4% |
| `en-US` | `naturalistic` | 6 | keep old limits visible if the | 14 | 4.2% |
| `en-US` | `naturalistic` | 7 | decision depends on a missing detail ask | 7 | 2.1% |
| `en-US` | `naturalistic` | 8 | limits visible if the next decision depends on | 7 | 2.1% |
| `ko-KR` | `canonical` | 6 | 덜 정해진 다음 계획을 임시안으로 잡아줘 | 8 | 2.4% |
| `ko-KR` | `canonical` | 7 | 범위가 덜 정해진 다음 계획을 임시안으로 잡아줘 | 8 | 2.4% |
| `ko-KR` | `canonical` | 8 | 다음 일회성 도구 작업을 실행할 수 있게 준비해줘 | 8 | 2.4% |
| `ko-KR` | `naturalistic` | 6 | 계획 형태로 해줄래 빠진 입력은 말해줘 | 9 | 2.7% |
| `ko-KR` | `naturalistic` | 7 | 범위도 봐줘 다음 결정에 정보가 빠졌다면 질문하고 | 7 | 2.1% |
| `ko-KR` | `naturalistic` | 8 | 범위도 봐줘 다음 결정에 정보가 빠졌다면 질문하고 가정은 | 7 | 2.1% |

- Concentration violations above the 5.0% non-whitelisted threshold: **0**.
- N-gram whitelist entries: **0**; whitelist is empty and no boilerplate is exempted.
- Global Korean/English grammar and punctuation hits: **0**; English lowercase-after-sentence hits: **0**.
- Naturalistic feature-realization hits: **0**.
- Response-mode / behavior-boundary hits: **0**.
- Generated-label leakage hits in naturalistic messages: **0**.
- The word `canonical`, when present in a message, is treated as task content only when it is part of a scenario fact; schema/form labels are not inserted into naturalistic message text.

## Validation performed

- JSON was serialized with Python's standard JSON encoder for every file.
- Every block was checked for all seven binary facet levels and all strength-2 facet pairs.
- Scenario IDs and prompt IDs were checked for global uniqueness within this worker slice.
- Every scenario has exactly four realizations and every naturalistic realization has catalogued profile IDs.
- All 1,344 realizations received a language scan; all 672 naturalistic realizations received profile-evidence, label-leakage, and response-mode boundary scans.
- Primary domains and domain tags were checked against the authoritative allowed catalog IDs; software/data primary-domain share was checked against the 20% ceiling.
- Exact 6-token, 7-token, and 8-token non-whitelisted n-gram presence was checked at the per-locale/form 5.0% concentration ceiling.
- Normalized title/topic/facts/deliverable uniqueness was checked across all 42 blocks before generation.
- Stable fixture preservation was checked across every naturalistic locale/form pair; qualitative row-1 compact renderings were manually compared against source evidence and deliverables.
- Generator checks: **PASS**.

## Integration-owned acceptance overlay

The source snapshot was fetched from `codex/worker-c-intents-15-21` at
`9b73b72b6871c2369d82f649bd768d4597384803`. Before union acceptance, the
integration branch independently rendered every message and corrected 12
C-owned rows: two remaining semicolon field-template fragments, three Korean
rambling prompts below the 180-character per-locale minimum, six code-switch
rows whose Korean text lacked a task-specific English field or jargon cue, and
one additional delimiter-serialized terse fragment caught by the final
short-message profile gate. The source report above records worker evidence;
the current union report is authoritative for the post-integration values.

With those owned-path corrections, the integration validator reports for this
partition: **336 scenarios**, **1,344 realizations**, **0 scenario/schema or
profile-evidence errors**, **0 grammar/punctuation errors**, **0 critical
numeric/possessive fact-preservation errors**, **0 phrase-gate violations**, and
**0 similarity failures**. It records 9 similarity warnings at the 0.75 review
threshold and no whitelist entries. Scenario statuses remain source-authored
and are not promoted by this overlay.

Post-correction `terse_fragment` rendered lengths are KO **16/21
whitespace-token median/max, 61/82 character median/max** and EN **17/25
word median/max, 135/182 character median/max** across the 42 naturalistic
pairs. The strict profile gate also rejects a terse message over 160
characters when it has eight or fewer whitespace tokens, and rejects
delimiter-serialized topic/context/result fields.
