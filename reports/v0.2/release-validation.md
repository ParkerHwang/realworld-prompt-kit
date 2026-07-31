# v0.2 Artifact Core Release Validation

- Validation: **PASS**
- Manifest status: **`calibration_release`**
- Semantic scenarios: **12**
- Prompt realizations: **48**
- Input assets: **20**
- Reference artifacts: **18**
- Reference hard-gate full passes: **12/12**

## Module coverage

| Module | Episodes |
| --- | ---: |
| `artifact_quality_control_delivery` | 2 |
| `attached_file_grounding` | 2 |
| `cross_artifact_workflow` | 2 |
| `document_work` | 2 |
| `presentation_work` | 2 |
| `spreadsheet_work` | 2 |

## Workflow-job coverage

| Workflow job | Episodes |
| --- | ---: |
| `create` | 3 |
| `extract` | 1 |
| `inspect` | 1 |
| `package` | 2 |
| `repurpose` | 1 |
| `revise` | 2 |
| `synthesize` | 1 |
| `validate` | 1 |

## Output artifacts

| Family | Reference artifacts |
| --- | ---: |
| `document` | 7 |
| `presentation` | 5 |
| `response_only` | 1 |
| `spreadsheet` | 5 |

## Calibration boundary

- Every public reference passes the executable hard gates and deterministic rubric checks.
- Human-only rubric items left unscored: **12**.
- Human practitioner calibration, external replication, and a global leaderboard claim remain explicitly false.
- Reference files are conformance fixtures, not byte-for-byte gold answers for model submissions.
