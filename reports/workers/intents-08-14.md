# Worker B — intents 08–14 scenario delivery

- Schema: `realworld-prompt-kit.scenario/1.0.0`
- Scope: `data/v1.0/scenarios/intents-08-14/`
- Semantic scenarios: 320
- Prompt realizations: 1,280 (four per scenario: ko/en × canonical/naturalistic)
- Source policy: synthetic prompts only; `contains_personal_data=false`

## Block counts

| Intent | Declared blocks | Scenarios | Realizations |
| --- | ---: | ---: | ---: |
| `classification_organization` | 5 | 40 | 160 |
| `qualitative_analysis` | 5 | 40 | 160 |
| `quantitative_formal_analysis` | 6 | 48 | 192 |
| `diagnosis_root_cause` | 6 | 48 | 192 |
| `forecasting_scenario_risk` | 6 | 48 | 192 |
| `evaluation_review_audit` | 6 | 48 | 192 |
| `decision_recommendation` | 6 | 48 | 192 |

## Composition

- General/office/business/education/personal primary domains: 285/320 (89.1%).
- `software_it` + `data_analytics`: 29/320 (9.1%), below the 20% ceiling.
- Every primary domain and profile used is drawn from the authoritative allowed catalog subset.
- Semantic-breadth audit: EN 320/320 and KO 320/320 normalized title+goal+evidence keys are unique; 320/320 EN and 320/320 KO fixture cores remain unique after removing block labels and fixture-only lines; semantic_group_id uniqueness 320/320.
- Normalized title-base duplicate audit: exact duplicates EN=0, KO=0; digit-stripped duplicates EN=0, KO=0; release requirement is 0 groups in every column.
- Rendered fact-preservation audit: 640 canonical↔naturalistic locale pairs; distinct numeric-literal set failures=0; English possessive→bare-plural failures=0.
- Canonical↔naturalistic similarity (normalized SequenceMatcher; 320 pairs per locale): `ko-KR` mean=0.336, median=0.339, min=0.045, max=0.575, >=0.85 pairs=0; `en-US` mean=0.176, median=0.167, min=0.002, max=0.544, >=0.85 pairs=0.
- Phrase-concentration gate: scanned every 6–8 token n-gram by locale/form; the exact six-token release threshold is <=5% (<=16/320), and all 6–8-grams meet it. Whitelist: none (no fixture exception was needed).

### Phrase-concentration scan

| Locale | Form | Maximum non-whitelisted count | Violating n-grams | Most repeated non-whitelisted n-grams |
| --- | --- | ---: | ---: | --- |
| `ko-KR` | `canonical` | 14/320 (4.4%) | 0 | 고정된 자료로 보고 필요한 가정은 밝혀줘 (14) — 근거 범위로 삼고 외부 사실을 넣지 (14) |
| `ko-KR` | `naturalistic` | 15/320 (4.7%) | 0 | 를 판단할 때 이 자료를 먼저 (15) — 에 바로 써야 하는 답이 필요해 (15) |
| `en-US` | `canonical` | 14/320 (4.4%) | 0 | a closed fixture state any necessary (14) — and mark anything the record does (14) |
| `en-US` | `naturalistic` | 15/320 (4.7%) | 0 | if time allows please start with (15) — s constraint is real for the (15) |
- Domain/task-fit sample: row 1 from every one of the 40 blocks was reviewed against its title, goal, evidence fixture, and primary domain; no rotation-only domain assignments were retained.

## Domain/task-fit sample (row 1 of every block)

| Block | Primary domain | Sample title |
| --- | --- | --- |
| `classification_organization.canonical.cb8` | `office_admin` | Sort launch meeting notes: decision launch review remains window closes at — direct evidence organization |
| `classification_organization.boundary_ambiguity.cb8` | `office_admin` | Sort launch meeting notes: decision holiday exception launch one entry falls just — borderline-case reasoning |
| `classification_organization.input_robustness.cb8` | `office_admin` | Sort launch meeting notes: decision shared inbox paste repeats one line — messy-input recovery |
| `classification_organization.multi_criteria_boundary.cb8` | `office_admin` | Sort launch meeting notes: decision deadline budget launch hard limit convenience — hard and soft criteria |
| `classification_organization.verification_uncertainty.cb8` | `office_admin` | Sort launch meeting notes: decision handoff one owner field blank — verification boundary |
| `qualitative_analysis.canonical.cb8` | `personal_everyday` | Compare two neighborhood options: North district 25 minute review window closes at — direct evidence organization |
| `qualitative_analysis.boundary_ambiguity.cb8` | `personal_everyday` | Compare two neighborhood options: North district holiday exception one entry falls just — borderline-case reasoning |
| `qualitative_analysis.input_robustness.cb8` | `personal_everyday` | Compare two neighborhood options: North district shared inbox paste repeats one line — messy-input recovery |
| `qualitative_analysis.verification_uncertainty.cb8` | `personal_everyday` | Compare two neighborhood options: North district handoff one owner field blank — verification boundary |
| `qualitative_analysis.tradeoff_stakes.cb8` | `personal_everyday` | Compare two neighborhood options: North district urgent workshop late booking saves money — stakes-aware tradeoff |
| `quantitative_formal_analysis.canonical.cb8` | `office_admin` | Analyze an event budget: venue 480 dollars review window closes at — direct evidence organization |
| `quantitative_formal_analysis.boundary_ambiguity.cb8` | `office_admin` | Analyze an event budget: venue holiday exception event one entry falls just — borderline-case reasoning |
| `quantitative_formal_analysis.input_robustness.cb8` | `office_admin` | Analyze an event budget: venue shared inbox paste repeats one line — messy-input recovery |
| `quantitative_formal_analysis.format_semantic_preservation.cb8` | `office_admin` | Analyze an event budget: venue mixed unit calculation one row uses minutes — format with semantic preservation |
| `quantitative_formal_analysis.verification_uncertainty.cb8` | `office_admin` | Analyze an event budget: venue handoff one owner field blank — verification boundary |
| `quantitative_formal_analysis.tradeoff_stakes.cb8` | `office_admin` | Analyze an event budget: venue urgent workshop booking late saves money — stakes-aware tradeoff |
| `diagnosis_root_cause.canonical.cb8` | `customer_support_success` | Diagnose a late package: label created Monday morning review window closes at — direct evidence organization |
| `diagnosis_root_cause.boundary_ambiguity.cb8` | `customer_support_success` | Diagnose a late package: holiday exception shipping label one entry falls just — borderline-case reasoning |
| `diagnosis_root_cause.input_robustness.cb8` | `customer_support_success` | Diagnose a late package: shared inbox paste shipping repeats one line — messy-input recovery |
| `diagnosis_root_cause.competing_hypotheses.cb8` | `customer_support_success` | Diagnose a late package: late handoff incident shipping staffing delay carrier — competing-cause diagnosis |
| `diagnosis_root_cause.verification_uncertainty.cb8` | `customer_support_success` | Diagnose a late package: handoff one owner missing field blank — verification boundary |
| `diagnosis_root_cause.tradeoff_stakes.cb8` | `customer_support_success` | Diagnose a late package: urgent workshop booking shipping late saves money — stakes-aware tradeoff |
| `forecasting_scenario_risk.canonical.cb8` | `sales_marketing` | Forecast weekend grocery demand: last three comparable weekends review window closes at — direct evidence organization |
| `forecasting_scenario_risk.boundary_ambiguity.cb8` | `sales_marketing` | Forecast weekend grocery demand: comparable weekends holiday exception one entry falls just — borderline-case reasoning |
| `forecasting_scenario_risk.input_robustness.cb8` | `sales_marketing` | Forecast weekend grocery demand: comparable weekends shared inbox paste repeats one line — messy-input recovery |
| `forecasting_scenario_risk.forecast_reference_class.cb8` | `sales_marketing` | Forecast weekend grocery demand: comparable weekends festival week reference sample includes one — reference-class forecast |
| `forecasting_scenario_risk.verification_uncertainty.cb8` | `sales_marketing` | Forecast weekend grocery demand: comparable weekends handoff one owner field blank — verification boundary |
| `forecasting_scenario_risk.tradeoff_stakes.cb8` | `sales_marketing` | Forecast weekend grocery demand: comparable weekends urgent workshop late booking saves money — stakes-aware tradeoff |
| `evaluation_review_audit.canonical.cb8` | `office_admin` | Review a meeting process: agenda sent before meeting review window closes at — direct evidence organization |
| `evaluation_review_audit.boundary_ambiguity.cb8` | `office_admin` | Review a meeting process: holiday exception agenda sent one entry falls just — borderline-case reasoning |
| `evaluation_review_audit.input_robustness.cb8` | `office_admin` | Review a meeting process: shared inbox paste agenda repeats one line — messy-input recovery |
| `evaluation_review_audit.multi_criteria_boundary.cb8` | `office_admin` | Review a meeting process: deadline budget agenda sent hard limit convenience — hard and soft criteria |
| `evaluation_review_audit.verification_uncertainty.cb8` | `office_admin` | Review a meeting process: handoff one owner missing field blank — verification boundary |
| `evaluation_review_audit.tradeoff_stakes.cb8` | `office_admin` | Review a meeting process: urgent workshop booking agenda late saves money — stakes-aware tradeoff |
| `decision_recommendation.canonical.cb8` | `office_admin` | Choose an office caterer: Option 14 dollars per review window closes at — direct evidence organization |
| `decision_recommendation.boundary_ambiguity.cb8` | `office_admin` | Choose an office caterer: Option holiday exception packet one entry falls just — borderline-case reasoning |
| `decision_recommendation.input_robustness.cb8` | `office_admin` | Choose an office caterer: Option shared inbox paste repeats one line — messy-input recovery |
| `decision_recommendation.audience_context_shift.cb8` | `office_admin` | Choose an office caterer: Option manager s one needs page — audience-aware recommendation |
| `decision_recommendation.verification_uncertainty.cb8` | `office_admin` | Choose an office caterer: Option handoff one owner field blank — verification boundary |
| `decision_recommendation.tradeoff_stakes.cb8` | `office_admin` | Choose an office caterer: Option urgent workshop booking late saves money — stakes-aware tradeoff |

## Human-read rendered samples (row 1 of every block)

Each row below is the full naturalistic user message rendered from the owned JSON, reviewed for task/domain fit, observable profile cues, locale surface, and non-serialized evidence phrasing.

| Block | KO naturalistic | EN naturalistic |
| --- | --- | --- |
| `classification_organization.canonical.cb8` | 정렬? 닫힘 3시, 할 일은 8월28일, 위험은 문서화 안 됨, 결정은 9월14일, 질문은 가격안은 2분기 기록. | Sort? Closes 3 pm, action due 28 Aug, risk is not documented, decision stays 14 Sep, question remains open Q2 round. |
| `classification_organization.boundary_ambiguity.cb8` | 태그? 질문은 미정, 안쪽에 항목이, 할 일은 담당자 8월21일, 위험은 담당자 없음, 결정은 9월13일 빠진 건? 아마? | Tag? Question remains open, cutoff entry, action due owner 21 Aug, risk has owner none, decision stays 13 Sep What's missing? Maybe? |
| `classification_organization.input_robustness.cb8` | 정리? 결정은 9월13일, 질문은 미정, 빠짐 반복, 할 일은 담당자 8월21일, 위험은 담당자 없음 아래 붙여넣음 | Organize? Decision stays 13 Sep, question remains open, heading paste, action due owner 21 Aug, risk has owner none Pasted below |
| `classification_organization.multi_criteria_boundary.cb8` | 정렬? 질문은 미정, 뿐임 기한, 할 일은 담당자 8월21일, 위험은 담당자 없음, 결정은 9월13일 다음도? 짧게, 단서는 남겨. | Sort? Question remains open, preference only, action due owner 21 Aug, risk has owner none, decision stays 13 Sep Due dates noted. Also next step? Brief but careful. |
| `classification_organization.verification_uncertainty.cb8` | 정렬? 질문은 미정, 비어 빈칸, 할 일은 8월21일, 위험은 없음, 결정은 9월13일 담당자 없음. 빠진 건? 공유해도 돼? | Sort? Question remains open, blank field, action due 21 Aug, risk is none, decision stays 13 Sep Owner missing. What's missing? Okay to share? |
| `qualitative_analysis.canonical.cb8` | 읽기? 강변 40분, 사용자는 미정, 북쪽 25분, 정확한 없음, 닫힘 3시 2분기 기록. | Read? River 40m, user not, north 25m, notes not, closes 3 pm Q2 round. |
| `qualitative_analysis.boundary_ambiguity.cb8` | 무게? 안쪽에 항목이, 강변 37분, 자료에는 없음, 북쪽 22분, 주민은 빠진 건? 아마? | Weight? Cutoff entry, river 37m, notes not, north 22m, resident What's missing? Maybe? |
| `qualitative_analysis.input_robustness.cb8` | 대비? 주민은, 빠짐 반복, 강변 37분, 자료에는 없음, 북쪽 22분 아래 붙여넣음 | Contrast? Resident, heading paste, river 37m, notes not, north 22m Pasted below |
| `qualitative_analysis.verification_uncertainty.cb8` | 읽기? 비어 빈칸, 강변 37분, 자료에는 없음, 북쪽 22분, 주민은 담당자 없음. 빠진 건? 공유해도 돼? | Read? Blank field, river 37m, notes not, north 22m, resident Owner missing. What's missing? Okay to share? |
| `qualitative_analysis.tradeoff_stakes.cb8` | 비교? 줄임 늦은, 강변 37분, 자료에는 없음, 북쪽 22분, 주민은 지금 급해. 가능하면 | Compare? Time late, river 37m, notes not, north 22m, resident Need it now. If you can |
| `quantitative_formal_analysis.canonical.cb8` | 산출? 후원금 600달러, 장소 480달러, 인쇄 90달러, 닫힘 3시, 식음료 30명, 1인당 18달러 2분기 기록. | Compute? Sponsor $600, venue $480, printing $90, closes 3 pm, food $18 30 Q2 round. |
| `quantitative_formal_analysis.boundary_ambiguity.cb8` | 계산? 식음료 25명, 1인당 16달러, 후원금 601달러, 장소 621달러, 인쇄 73달러, 안쪽에 항목이 빠진 건? 아마? | Math? Food $16 25, sponsor $601, venue $621, printing $73, cutoff entry What's missing? Maybe? |
| `quantitative_formal_analysis.input_robustness.cb8` | 비율? 빠짐 반복, 식음료 25명, 1인당 16달러, 후원금 701달러, 장소 721달러, 인쇄 73달러 아래 붙여넣음 | Rates? Heading paste, food $16 25, sponsor $701, venue $721, printing $73 Pasted below |
| `quantitative_formal_analysis.format_semantic_preservation.cb8` | 측정? 인쇄 73달러, 단위임 단위, 식음료 25명, 1인당 16달러, 후원금 1001달러, 장소 1021달러 아래 붙여넣음 | Measure? Printing $73, hours row, food $16 25, sponsor $1001, venue $1021 Units mixed. Pasted below |
| `quantitative_formal_analysis.verification_uncertainty.cb8` | 산출? 식음료 25명, 1인당 16달러, 후원금 901달러, 장소 921달러, 인쇄 73달러, 비어 빈칸 담당자 없음. 빠진 건? 공유해도 돼? | Compute? Food $16 25, sponsor $901, venue $921, printing $73, blank field Owner missing. What's missing? Okay to share? |
| `quantitative_formal_analysis.tradeoff_stakes.cb8` | 측정? 식음료 25명, 1인당 16달러, 후원금 1401달러, 장소 1421달러, 인쇄 73달러, 줄임 늦은 지금 급해. 가능하면 | Measure? Food $16 25, sponsor $1401, venue $1421, printing $73, time late Need it now. If you can |
| `diagnosis_root_cause.canonical.cb8` | 왜? 닫힘 3시, 택배사 수요일, 화요일, 월요일, 주소는 2분기 기록. | Why? Closes 3 pm, carrier Wednesday, route not Tuesday, label Monday, address Q2 round. |
| `diagnosis_root_cause.boundary_ambiguity.cb8` | 가설? 주소는, 안쪽에 항목이, 택배 목요일, 노선에 미확인, 배송 화요일 빠진 건? 아마? | Hypotheses? Address, cutoff entry, first Thursday, route weather, shipping Tuesday What's missing? Maybe? |
| `diagnosis_root_cause.input_robustness.cb8` | 확인? 배송 화요일, 주소는, 빠짐 반복, 택배 목요일, 노선에 미확인 아래 붙여넣음 | Checks? Shipping Tuesday, address, heading paste, first Thursday, route weather Pasted below |
| `diagnosis_root_cause.competing_hypotheses.cb8` | 추적? 발생 지연, 택배 목요일, 노선에 미확인, 배송 화요일, 주소는 갈래가 많아 아니 | Trace? Window delay, first Thursday, route weather, shipping Tuesday, address Several threads Actually |
| `diagnosis_root_cause.verification_uncertainty.cb8` | 왜? 주소는, 비어 빈칸, 택배 목요일, 노선에 미확인, 배송 화요일 담당자 없음. 빠진 건? 공유해도 돼? | Why? Address, blank field, first Thursday, route weather, shipping Tuesday Owner missing. What's missing? Okay to share? |
| `diagnosis_root_cause.tradeoff_stakes.cb8` | 추적? 주소는, 줄임 늦은, 택배 목요일, 노선에 미확인, 배송 화요일 지금 급해. 가능하면 | Trace? Address, time late, first Thursday, route weather, shipping Tuesday Need it now. If you can |
| `forecasting_scenario_risk.canonical.cb8` | 시나리오? 공급업체는 20, 닫힘 3시, 이번, 날씨, 최근 80 92 88주 2분기 기록. | Scenarios? Supplier 20, closes 3 pm, festival, weather not missing, last 80 92 88wk Q2 round. |
| `forecasting_scenario_risk.boundary_ambiguity.cb8` | 전망? 매장의 271 280 276주, 공급업체는 13, 안쪽에 항목이, 주말에, 묶음에는 없음 빠진 건? 아마? | Outlook? Comparable 271 280 276wk, supplier 13, cutoff entry, festival, packet none What's missing? Maybe? |
| `forecasting_scenario_risk.input_robustness.cb8` | 하방? 묶음에는 없음, 매장의 371 380 376주, 공급업체는 13, 빠짐 반복, 주말에 아래 붙여넣음 | Downside? Packet none, comparable 371 380 376wk, supplier 13, heading paste, festival Pasted below |
| `forecasting_scenario_risk.forecast_reference_class.cb8` | 전망? 묶음에는 없음, 매장의 871 880 876주, 공급업체는 13, 포함됨 참조, 주말에 아마? | Outlook? Packet none, comparable 871 880 876wk, supplier 13, weekend reference, festival Maybe? |
| `forecasting_scenario_risk.verification_uncertainty.cb8` | 시나리오? 매장의 571 580 576주, 공급업체는 13, 비어 빈칸, 주말에, 묶음에는 없음 담당자 없음. 빠진 건? 공유해도 돼? | Scenarios? Comparable 571 580 576wk, supplier 13, blank field, festival, packet none Owner missing. What's missing? Okay to share? |
| `forecasting_scenario_risk.tradeoff_stakes.cb8` | 예상? 매장의 1071 1080 1076주, 공급업체는 13, 줄임 늦은, 주말에, 묶음에는 없음 지금 급해. 가능하면 | Expect? Comparable 1071 1080 1076wk, supplier 13, time late, festival, packet none Need it now. If you can |
| `evaluation_review_audit.canonical.cb8` | 수정? 결정은 5 3, 검토, 회의, 담당자는 기한, 닫힘 3시 2분기 기록. | Fix? Decision stays 3 5, review not, agenda, owner is missing due, closes 3 pm Q2 round. |
| `evaluation_review_audit.boundary_ambiguity.cb8` | 확인? 안쪽에 항목이, 결정은 5 3, 검토, 안건은, 담당자는 기한 빠진 건? 아마? | Checks? Cutoff entry, decision stays 3 5, review not, agenda, owner is missing due What's missing? Maybe? |
| `evaluation_review_audit.input_robustness.cb8` | 검토? 담당자는 기한, 빠짐 반복, 결정은 5 3, 검토, 안건은 아래 붙여넣음 | Review? Owner is missing due, heading paste, decision stays 3 5, review not, agenda Pasted below |
| `evaluation_review_audit.multi_criteria_boundary.cb8` | 수정? 뿐임 기한, 결정은 5 3, 검토, 안건은, 담당자는 기한 다음도? 짧게, 단서는 남겨. | Fix? Preference only, decision stays 3 5, review not, agenda, owner is missing Due dates noted. Also next step? Brief but careful. |
| `evaluation_review_audit.verification_uncertainty.cb8` | 수정? 비어 빈칸, 결정은 5 3, 검토, 안건은, 대부분 기한 담당자 없음. 빠진 건? 공유해도 돼? | Fix? Blank field, decision stays 3 5, review not, agenda, owners due Owner missing. What's missing? Okay to share? |
| `evaluation_review_audit.tradeoff_stakes.cb8` | 점검? 줄임 늦은, 결정은 5 3, 검토, 안건은, 담당자는 기한 지금 급해. 가능하면 | Audit? Time late, decision stays 3 5, review not, agenda, owner is missing due Need it now. If you can |
| `decision_recommendation.canonical.cb8` | 선택? A안 채식 1인당 14달러, 48시간 전, C안 성분 불명확 1인당 11달러, 닫힘 3시, B안 알레르기 1인당 18달러, 72시간 전, 예산 1인당 16달러, 4일 후 2분기 기록. | Pick? Option A vegetarian $14 48, option C ingredients unclear $11, closes 3 pm, option B allergy $18 72, budget $16 Q2 round. |
| `decision_recommendation.boundary_ambiguity.cb8` | 절충? 예산 1인당 15달러, 4일 후, A안 채식 1인당 13달러, C안 성분 불명확 1인당 10달러, 안쪽에 항목이, B안 알레르기 1인당 17달러 빠진 건? 아마? | Tradeoff? Budget $15, option A vegetarian $13, option C ingredients unclear $10, cutoff entry, option B allergy $17 What's missing? Maybe? |
| `decision_recommendation.input_robustness.cb8` | 판단? B안 알레르기 1인당 17달러, 예산 1인당 15달러, 4일 후, A안 채식 1인당 13달러, C안 성분 불명확 1인당 10달러, 빠짐 반복 아래 붙여넣음 | Decide? Option B allergy $17, budget $15, option A vegetarian $13, option C ingredients unclear $10, heading paste Pasted below |
| `decision_recommendation.audience_context_shift.cb8` | 판단? 필요로 관리자는, B안 알레르기 1인당 17달러, 예산 1인당 15달러, 4일 후, A안 채식 1인당 13달러, C안 성분 불명확 1인당 10달러 가능하면 공유해도 돼? | Decide? Brief manager, option B allergy $17, budget $15, option A vegetarian $13, option C ingredients unclear $10 If you can Okay to share? |
| `decision_recommendation.verification_uncertainty.cb8` | 선택? 예산 1인당 15달러, 4일 후, A안 채식 1인당 13달러, C안 성분 불명확 1인당 10달러, 비어 빈칸, B안 알레르기 1인당 17달러 담당자 없음. 빠진 건? 공유해도 돼? | Pick? Budget $15, option A vegetarian $13, option C ingredients unclear $10, blank field, option B allergy $17 Owner missing. What's missing? Okay to share? |
| `decision_recommendation.tradeoff_stakes.cb8` | 기울기? 예산 1인당 15달러, 4일 후, A안 채식 1인당 13달러, C안 성분 불명확 1인당 10달러, 줄임 늦은, B안 알레르기 1인당 17달러 지금 급해. 가능하면 | Lean? Budget $15, option A vegetarian $13, option C ingredients unclear $10, time late, option B allergy $17 Need it now. If you can |

## Validation performed

- JSON syntax reparse: 320/320 files parsed successfully after writing; each object has four exact locale/form pairs.
- Every declared block has rows 1–8 exactly once; block IDs follow `<intent>.<block>.cb8`.
- Naturalistic profiles are present on every scenario and use only the supplied catalog profile IDs.
- Profile realization audit: 2192 assigned feature/locale checks; failures=0. Terse full-render gate: 80/80 messages; KO chars median/max=62.0/106, whitespace tokens median/max=15.0/27; EN chars median/max=105.0/165, whitespace tokens median/max=17.0/28; >32-token failures=0, conditional <=8-token/>160-char failures=0, serialization/field-label failures=0, numeric fixture failures=0, constraint failures=0.
- The earlier 40-row profile-failure review was handled by rewriting unclear naturalistic phrasing (including explicit self-correction, rambling discovery order, and implicit-goal cases) before rerunning the observable-feature audit; no detector-only vocabulary bypass was used.
- Surface audit: 1280/1,280 prompts; KO grammar failures=0, EN punctuation/capitalization failures=0, KO Latin leakage=0, label leakage=0, expanded malformed-pattern hits=0, over-refusal/response-behavior failures=0.
- Canonical realizations carry `controlled_canonical`; naturalistic realizations carry `synthetic_naturalistic`.
- No source files outside this worker's data directory and report path are part of the deliverable.

## Integration-owned strict baseline and correction ledger

The source snapshot was fetched from `codex/worker-b-intents-08-14` at
`f2662069ac556f125054ca59953467edcb2af033`. The path audit was clean: 320
scenario JSON files plus this report, with no unrelated files. The following
baseline was captured by the integration validator against the fully rendered
messages before any integration edits. These are source-generation defects,
not validator false positives: each is an observable violation of a release
contract, and the capitalization failures occur in canonical English as well
as naturalistic text.

| Failure class | Exact errors | Affected scenario files | Representative source paths | Classification |
| --- | ---: | ---: | --- | --- |
| English capitalization/punctuation | 360 | 320 | `classification_organization__boundary_ambiguity__01.json`; `classification_organization__boundary_ambiguity__02.json`; `classification_organization__boundary_ambiguity__03.json` | source-generation: lowercase sentence starts after rendered sentence boundaries |
| Korean code-switch cue | 39 | 39 | `classification_organization__boundary_ambiguity__05.json`; `classification_organization__canonical__05.json`; `classification_organization__input_robustness__05.json` | source-generation: declared profile absent from rendered Korean text |
| Resume cue | 9 | 9 | `classification_organization__input_robustness__07.json`; `decision_recommendation__input_robustness__07.json`; `diagnosis_root_cause__input_robustness__07.json` | source-generation: declared resume profile absent from rendered pair |
| Embedded-instruction cue | 7 | 7 | `classification_organization__input_robustness__06.json`; `decision_recommendation__input_robustness__06.json`; `diagnosis_root_cause__input_robustness__06.json` | source-generation: declared untrusted-instruction profile absent from rendered pair |
| Numeric fact preservation | 5 | 5 | `classification_organization__boundary_ambiguity__01.json`; `classification_organization__canonical__01.json`; `classification_organization__input_robustness__01.json` | source-generation: Korean naturalistic prompt dropped canonical numeric literals |
| Rambling rendered length | 1 | 1 | `diagnosis_root_cause__competing_hypotheses__01.json` | source-generation: declared rambling stream below the per-locale minimum |
| **Total** | **421** | **—** | **—** | **all source-generation; validator false positives: 0** |

The integration repair is generator/systemic in scope rather than a one-off
row mask: it normalizes the repeated English sentence-boundary construction,
adds varied task-specific Korean code-switch evidence, restores missing
numeric literals from each scenario's canonical fixture, adds localized
resume and embedded-instruction signals to their declared profiles, and
expands the single short rambling rendering with its own scenario evidence.
The exact corrected counts and post-repair gate results are appended after the
repair is complete.

## Integration-owned post-repair overlay

The owned B data was repaired in place using deterministic, path-restricted
rendering passes over all 320 rows; no unrelated files or catalog quotas were
changed. The correction ledger is:

| Correction class | Affected rendered items/rows | Result |
| --- | ---: | --- |
| English sentence-boundary capitalization normalization | 360 rendered English messages across 320 rows | 360 → 0 failures |
| Task-specific Korean code-switch evidence, diversified by row | 39 rows | 39 → 0 failures |
| Localized resume evidence | 9 rows | 9 → 0 failures |
| Localized untrusted embedded-instruction evidence | 7 rows | 7 → 0 failures |
| Korean naturalistic numeric-literal restoration from canonical fixtures | 5 rows | 5 → 0 failures |
| Compact but genuinely rambling evidence for the one dual-profile row | 1 row / 2 realizations | 1 → 0 failures |
| **Total strict rendered-content errors** | **421** | **421 → 0** |

The capitalization pass corrected the repeated source construction at its
rendering boundary rather than masking individual prompt IDs. Profile fixes
use varied task-specific Korean/English wording; no phrase whitelist was added.
The one row declaring both `terse_fragment` and `rambling_stream` was rewritten
as a single compact evidence fragment per locale: KO 194 characters / 20
normalized tokens and EN 212 characters / 26 normalized tokens.

Post-repair strict partition results: **320 scenarios**, **1,280
realizations**, **0 scenario/schema/profile errors**, **0 grammar/punctuation
errors**, **0 critical numeric/possessive fact errors**, **0 phrase-gate
violations**, **0 similarity failures**, **0 similarity warnings**, **0
normalized title-base duplicate groups**, **0 semantic-goal duplicate groups**,
and **0 cross-block high-similarity pairs**. Scenario statuses remain the
source-authored `draft` values; automated repair does not promote review
status.
