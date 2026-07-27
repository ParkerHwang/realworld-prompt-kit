# v1.0 pre-generation coverage baseline

Status: **dated pre-generation baseline** (2026-07-27). This audit records the
requirements-only state of origin/main before v1 artifacts were generated; it
is not the current release report and its zero observations must not be used to
describe the checked-in v1 package. Current evidence is generated at
`reports/coverage/v1-coverage.json` and `reports/coverage/v1-coverage.md`.

## Bottom line

The requested v1.0 basis is 21 task intents, 110 CB8 blocks, 880 semantic scenarios, and four realizations per scenario (3,520 prompt realizations). The three core worker partitions can be planned to produce the 880-scenario broad core:

| partition | intent range | semantic scenarios |
| --- | ---: | ---: |
| core-worker-1 | 1–7 | 224 |
| core-worker-2 | 8–14 | 320 |
| core-worker-3 | 15–21 | 336 |
| **total** | **1–21** | **880** |

origin/main at commit f8dc8d9ba376c64e44613ebcc0b9119a2530064f contains the earlier v0.1 pack (8 scenario files), not v1.0 catalog/scenario artifacts. Observed v1 coverage is therefore zero.

## Coverage planes

| plane | broad-core overlap | separate evidence required |
| --- | --- | --- |
| task intent | yes | exact 21 intent quotas and 110 CB8 membership |
| domain | yes, as primary/secondary overlays | exact 28-domain quotas and composition guardrails |
| naturalistic profile | yes, without increasing semantic breadth | four realization pairs, profile quotas, rights/privacy policy |
| OpenSocrates method/family | scenario IDs may overlap | route receipts, negative/contraindicated/hold/handoff blocks |
| confusable method edge | not claimable | external edge registry plus one CB8 per edge |
| adapter/tool/workflow | no automatic credit | adapter-conformance runs, sandbox and run-record evidence |
| live/side-effect/locale/modality overlays | conditional only | dedicated dynamic, security, locale, or adapter suite |

## OpenSocrates routing requirements

The verified method catalog has 48 methods across 12 families. Each method requires 6 CB8 / 48 assignments; each family requires 3 CB8 / 24 assignments; no-route requires 6 CB8 / 48 assignments. The catalog has no documented confusable-edge list, so edge coverage is intentionally unresolved.

## Adapter requirements

Each adapter requires 12 contracts × 1 CB8 = 96 assignments. The 12 contracts are discovery/install, activation/identity/receipt, routing participation, request/response schema, permission/approval, filesystem/data boundary, state/resume, timeout/retry/idempotency, concurrency/cancel, observability/privacy, version compatibility, and uninstall/rollback. Tool/workflow/modality additions are separate quotas.

## Quotas that the three core partitions cannot satisfy alone

- OpenSocrates per-method, per-family, confusable-edge, and no-route packs.
- Adapter contracts, tool-class additions, multi-tool workflow families, and modality-adapter additions.
- Dynamic-live and external-side-effect overlays.
- Independent domain review for the seven regulated domains.

These may reuse semantic scenario IDs, but they do not inherit release credit from the 880-scenario broad core.

## Exact release gates

1. Pin catalog/schema/method revisions and an external confusable-edge registry if edge coverage is claimed.
2. Prove 880 unique v1 scenario IDs in 110 disjoint CB8 blocks.
3. Prove the three partition union is disjoint and complete (224 + 320 + 336).
4. Prove exactly four realizations per core scenario (3,520 total).
5. Pass all 21 intent quotas, 28 domain quotas, 24 naturalistic profile quotas, and composition guardrails.
6. Pass all 48-method/12-family/no-route routing gates; do not claim edge coverage without a registry.
7. Pass every adapter/tool/workflow/modality conformance formula with sandboxed evidence.
8. Pass regulated-domain reviewer/evidence/uncertainty/escalation gates.
9. Pass schema, identity, hash, split, leakage, privacy, and deterministic-scoring checks.
10. Publish only a manifest whose counts match present artifacts.

At the audit timestamp these gates were **not met** because origin/main held
only v0.1. The baseline is retained for evidence separation; after generation,
the current release status comes only from the v1 manifest, scenario files, and
the current coverage report.
