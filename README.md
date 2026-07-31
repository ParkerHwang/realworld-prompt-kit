# RealWorld Prompt Kit

RealWorld Prompt Kit is an open, bilingual benchmark source for evaluating how
AI systems handle realistic workplace requests. It separates semantic task
breadth from prompt phrasing and, beginning with v0.2, evaluates durable office
artifacts created from attached files.

## Releases

### v0.2 Artifact Core

v0.2 is a public **calibration release** for file-grounded office work. It asks
a model or agent to inspect supplied files and create, revise, validate, or
package usable deliverables.

- 12 complete work episodes across 6 modules
- 48 request realizations: Korean/English × canonical/naturalistic
- 20 real attached inputs in PDF, DOCX, PPTX, XLSX, CSV, and TXT
- 18 editable reference outputs in DOCX, PPTX, XLSX, and JSON
- all 8 workflow jobs: inspect, extract, synthesize, create, revise, repurpose,
  validate, and package
- hash-pinned assets, explicit authority boundaries, non-compensable hard
  gates, atomic rubrics, and deterministic reference grading

Every reference artifact passes the checked-in structural and source-grounded
checks. Human practitioner calibration and external replication have not yet
been run, so v0.2 does **not** support a global leaderboard or a claim about
population-level office-worker performance.

The release contract lives in
[data/v0.2/manifest.json](data/v0.2/manifest.json), with design rationale in
[docs/V0.2-DESIGN.md](docs/V0.2-DESIGN.md) and the operational release note in
[docs/V0.2-RELEASE.md](docs/V0.2-RELEASE.md).

### v0.1 Broad Core

v0.1 remains the text-only breadth track and is a `release_candidate`.

- 21 task intents
- 110 disjoint `CB8` blocks
- 880 distinct semantic scenarios
- 3,520 request realizations
- 224 scenarios marked `reviewed` and 656 retained as `draft`

The v0.1 contracts live in
[data/v0.1/catalog.json](data/v0.1/catalog.json) and
[data/v0.1/manifest.json](data/v0.1/manifest.json). Translation, paraphrase,
and prompt form do not add semantic breadth: each latent situation is counted
once by `scenario_id`.

## Quick start

Validate both releases, run the tests, write reports, and export portable
JSONL:

```bash
python3 tools/validate.py --manifest data/v0.1/manifest.json
python3 tools/validate.py --manifest data/v0.2/manifest.json
python3 -m unittest discover -s tests
python3 tools/coverage_report.py
python3 tools/artifacts/coverage_report.py
python3 tools/export_jsonl.py --output build/realworld-prompt-kit.jsonl
python3 tools/artifacts/export_jsonl.py
```

Grade a model-produced v0.2 artifact package:

```bash
python3 tools/artifacts/grade_artifacts.py \
  --scenario data/v0.2/scenarios/<scenario_id>.json \
  --submission-dir /path/to/submission
```

The reference files are conformance fixtures and examples, not byte-for-byte
gold answers. A valid submission may use a different structure when it still
satisfies the task-specific contract.

## Repository layout

```text
data/
├── v0.1/                         # text-only breadth release
└── v0.2/
    ├── assets/                   # attached source files
    ├── public-calibration/       # editable reference outputs
    ├── scenarios/                # work-episode contracts
    ├── catalog.json
    └── manifest.json
schemas/
├── scenario.schema.json
├── scenario-0.2.schema.json
├── artifact-contract.schema.json
└── atomic-rubric.schema.json
tools/
├── validate.py
└── artifacts/                    # build, inspect, grade, render, validate
reports/
├── coverage/
└── v0.2/
```

## Authoring principles

Write the latent workplace situation before its prompt text. Keep canonical
and naturalistic realizations semantically paired, preserve decision-critical
facts, and make profile evidence observable. For artifact episodes, include
rights-cleared source files, exact output and authority contracts, executable
checks, and honest human-calibration status. Do not create extra semantic
breadth by translating, paraphrasing, or converting a file format.

See [docs/AUTHORING.md](docs/AUTHORING.md),
[docs/RELEASE.md](docs/RELEASE.md), and
[CONTRIBUTING.md](CONTRIBUTING.md).

## Privacy and license

Private conversations, secrets, and personal data are not accepted. All v0.2
fixtures are synthetic, project-authored, and marked
`contains_personal_data=false`. Real or derived samples require a documented
rights basis, de-identification, and privacy review. See
[docs/PRIVACY.md](docs/PRIVACY.md).

MIT. See [LICENSE](LICENSE).
