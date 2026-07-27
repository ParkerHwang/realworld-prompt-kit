# RealWorld Prompt Kit

RealWorld Prompt Kit is an open, bilingual benchmark source for the way people
actually talk to AI systems.

Most prompt sets are cleaner than real messages. Users send fragments, paste
notes into instructions, change their mind mid-sentence, mix languages, omit
context, and split one request across several messages. This project pairs a
controlled prompt with a naturalistic version of the same semantic scenario so
model capability and real-world utterance robustness can be measured separately.

## What is in v0.1

- One complete `CB8` office-work coverage block
- 8 semantic scenarios
- 4 prompt realizations per scenario:
  - Korean canonical
  - Korean naturalistic
  - English canonical
  - English naturalistic
- 32 runnable prompt realizations
- Expected response behavior, invariants, rubric dimensions, and failure signals
- A dependency-free validator and JSONL exporter
- A JSON Schema and a GitHub Actions validation workflow

This is a seed release, not a claim that the full benchmark is complete.

## Why scenario count and prompt count differ

A translated, paraphrased, or A/B-tested prompt is not a new semantic task.

```text
semantic breadth = unique scenario_id values
prompt instances = sum of localized and naturalistic realizations
executions       = prompt instances × models × conditions × repeat policy
```

The v0.1 pack therefore contains 8 scenarios and 32 prompt instances. Reporting
only "32 tests" would overstate its semantic breadth.

## Quick start

Validate the repository:

```bash
python3 tools/validate.py
python3 -m unittest discover -s tests
```

Export flattened JSONL for a harness:

```bash
python3 tools/export_jsonl.py --output build/office-core-cb8.jsonl
```

Each exported row is one prompt realization and retains its parent
`scenario_id`, coverage metadata, and evaluation contract.

## Repository layout

```text
data/v0.1/
├── manifest.json
└── scenarios/
    └── *.json
docs/
├── AUTHORING.md
├── DESIGN.md
└── PRIVACY.md
schemas/
└── scenario.schema.json
tools/
├── export_jsonl.py
└── validate.py
```

## Design principles

1. The semantic scenario is independent of language, model, and harness.
2. Canonical and naturalistic realizations stay paired.
3. Messy wording is not automatically adversarial wording.
4. The expected behavior may be to infer, state assumptions, clarify, or hold.
5. Objective invariants and anchored rubrics are preferred over one global score.
6. Public data must be synthetic or rights-cleared and privacy-reviewed.
7. New packs are added as coverage blocks, not by chasing a headline total.

See [DESIGN.md](docs/DESIGN.md) for the full model.

## Current coverage

The first block focuses on ordinary office work:

- meeting follow-up
- vendor selection
- expense-policy interpretation
- project status synthesis
- customer complaint response
- schedule planning
- invoice discrepancy diagnosis
- onboarding checklist organization

The roadmap expands into general knowledge, education, personal tasks,
professional domains, creative work, tool use, multimodal input, and plugin or
agent conformance.

## Privacy

This repository does not accept copied private conversations, secrets, or
personal data. Synthetic naturalistic prompts are labeled as synthetic. Real or
real-derived samples require a documented rights basis, de-identification, and
privacy review, and verbatim raw messages must not be published in the public
suite. See [PRIVACY.md](docs/PRIVACY.md).

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). A contribution should add or
complete a named coverage cell, include both Korean and English when applicable,
and ship its evaluation contract with the prompt.

## License

MIT. See [LICENSE](LICENSE).
