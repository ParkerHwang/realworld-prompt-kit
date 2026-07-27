# Worker report: intents 01–07

This worker owns the first seven catalog task intents. The files are synthetic, bilingual, and authored as four realizations per semantic scenario: Korean/English canonical plus Korean/English naturalistic.

## Output and quota

- Semantic scenarios: **224**
- Prompt realizations: **896**
- Schema: `realworld-prompt-kit.scenario/1.0.0`
- Each block has exactly 8 rows and uses a strength-2 pairwise CB8 design over the seven binary coverage facets.

| Intent | Blocks | Scenarios | Realizations |
|---|---:|---:|---:|
| `information_retrieval` | 4 | 32 | 128 |
| `extraction_parsing` | 3 | 24 | 96 |
| `summarization_synthesis` | 4 | 32 | 128 |
| `transformation_rewriting` | 4 | 32 | 128 |
| `explanation_teaching` | 4 | 32 | 128 |
| `practical_writing` | 5 | 40 | 160 |
| `creative_ideation` | 4 | 32 | 128 |

## Composition

- General/office/business/education/personal primary domains: **155/224 (69.2%)**.
- Software + data primary domains: **22/224 (9.8%)**.
- All catalog domain classes are represented, including regulated and industry-specialist contexts. High-stakes contexts carry explicit uncertainty and official/professional escalation boundaries.

### Primary-domain counts

| Domain | Count |
|---|---:|
| `agriculture_food` | 2 |
| `communication_meetings` | 22 |
| `construction_real_estate` | 2 |
| `creative_media` | 8 |
| `customer_support_success` | 12 |
| `data_analytics` | 10 |
| `education_research` | 14 |
| `energy_environment` | 2 |
| `finance_accounting_tax` | 3 |
| `general_knowledge` | 13 |
| `government_public_policy` | 3 |
| `health_care` | 3 |
| `hr_people_labor` | 3 |
| `legal_compliance` | 3 |
| `manufacturing_quality` | 2 |
| `nonprofit_social_impact` | 2 |
| `office_admin` | 26 |
| `personal_everyday` | 22 |
| `privacy_security` | 3 |
| `project_product_management` | 20 |
| `retail_ecommerce` | 2 |
| `safety_emergency` | 3 |
| `sales_marketing` | 10 |
| `science_rd` | 2 |
| `software_it` | 12 |
| `strategy_business_operations` | 16 |
| `supply_chain_logistics` | 2 |
| `travel_hospitality` | 2 |

## Naturalistic profile coverage

All profile ids used below come from the catalog naturalistic profile list. Canonical realizations have empty `features`; naturalistic realizations carry the listed profile ids.

| Profile | Scenario rows using profile |
|---|---:|
| `anaphora_prior_context` | 33 |
| `code_switching_jargon` | 17 |
| `colloquial_slang_dialect` | 20 |
| `contradictory_constraints` | 16 |
| `emoji_shorthand` | 20 |
| `followup_without_restatement` | 28 |
| `frustration_urgency_emotion` | 14 |
| `hedged_exploratory_request` | 9 |
| `implicit_goal_or_output` | 22 |
| `implicit_permission_or_authority` | 8 |
| `indirect_polite_request` | 19 |
| `interleaved_instruction_and_paste` | 15 |
| `message_burst` | 16 |
| `mid_task_change` | 21 |
| `missing_decisive_detail` | 34 |
| `multi_intent_mixed_priority` | 24 |
| `ocr_copy_format_noise` | 15 |
| `rambling_stream` | 14 |
| `resume_after_interruption` | 12 |
| `self_correction_scope_shift` | 28 |
| `speech_to_text_disfluency` | 18 |
| `terse_fragment` | 23 |
| `typo_spacing_punctuation` | 14 |
| `untrusted_embedded_instruction` | 8 |

## Validation performed

- JSON parsing for every scenario file.
- Required v1.0.0 top-level shape, locale/form pair, synthetic provenance, scenario/prompt identity, catalog intent/domain/profile ids, and high-stakes boundary checks.
- Exact per-block count (8), exact declared block set for intents 01–07, unique scenario and prompt ids, and pairwise CB8 coverage.
- Domain-composition guardrails: general/office/business/education/personal at least 60%; software/data below 20%.
