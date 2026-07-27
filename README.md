# RealWorld Prompt Kit

RealWorld Prompt Kit is an open, bilingual benchmark source for the way people
actually talk to AI systems. It pairs a controlled prompt with an independently
authored naturalistic version of the same semantic situation so capability and
real-world utterance robustness can be measured separately.

## The v0.1 broad core

The repository has one initial validation release: the `v0.1` broad core.
It is a `release_candidate`, not a production-stable benchmark claim.

- 21 task intents
- 110 disjoint `CB8` blocks
- 880 genuinely distinct semantic scenarios
- 3,520 prompt realizations, exactly four per scenario:
  Korean/English × canonical/naturalistic
- 224 scenarios marked `reviewed` and 656 kept `draft`
- 28 authorized primary-domain IDs and 24 authorized naturalistic profiles
- synthetic, rights-cleared project-authored content with no personal data

The release contract lives in [data/v0.1/catalog.json](data/v0.1/catalog.json)
and [data/v0.1/manifest.json](data/v0.1/manifest.json). Translations,
paraphrases, and coverage conditions do not add semantic breadth: each latent
situation, evidence fixture, and goal is counted once by `scenario_id`.

OpenSocrates method-routing and adapter-conformance suites are planned-only
extensions. They are not populated and receive no coverage credit in this
release.

## Quality gates

The dependency-free validator checks exact counts, CB8 rows and pairwise facet
coverage, globally unique IDs, authorized domains and profiles, quota overlays,
composition ratios, synthetic provenance, exact/normalized duplicates,
placeholder leakage, language presence, canonical/naturalistic identity,
similarity, semantic reuse, rendered Korean/English grammar, response
boundaries, profile realization, critical fact preservation, and minimum prompt
substance.

Naturalistic pair similarity at or above 0.75 is reviewed and at or above 0.85
fails. The exact six-token phrase gate runs by locale/form over the full 880-row
union and independently over the 224/320/336 partitions; any non-whitelisted
phrase above 5% fails. A six-token presence scan also catches every longer
n-gram because every longer phrase has a six-token prefix. No generic task,
boundary, or safety boilerplate is whitelisted.

## Quick start

Validate the sole release, run tests, create reports, and export one JSONL file:

```bash
python3 tools/validate.py
python3 -m unittest discover -s tests
python3 tools/coverage_report.py
python3 tools/review.py
python3 tools/export_jsonl.py --output build/realworld-prompt-kit.jsonl
```

Every exported row retains its parent `scenario_id`, coverage metadata, and
evaluation contract. The status report records the candid `reviewed=224` /
`draft=656` distribution; automated validation and one sample per block never
promote unsampled rows.

## Repository layout

```text
data/v0.1/
├── catalog.json
├── manifest.json
└── scenarios/
    ├── intents-01-07/
    ├── intents-08-14/
    └── intents-15-21/
schemas/
└── scenario.schema.json
tools/
├── validation.py
├── validate.py
├── coverage_report.py
├── review.py
└── export_jsonl.py
reports/
├── coverage/
└── review/
build/
└── realworld-prompt-kit.jsonl
```

## Authoring principles

Write the latent situation before its prompt text. Keep canonical and
naturalistic realizations semantically paired, author the naturalistic forms
independently in each language, preserve decision-critical facts, and make
declared profile evidence observable in the rendered messages. Do not multiply
one topic across blocks by changing only a condition label or adding a wrapper.

See [docs/DESIGN.md](docs/DESIGN.md), [docs/AUTHORING.md](docs/AUTHORING.md),
and [docs/RELEASE.md](docs/RELEASE.md) for the contract and review policy.

## Privacy and license

Private conversations, secrets, and personal data are not accepted. Synthetic
naturalistic prompts are labeled as synthetic. Real or derived samples require
a documented rights basis, de-identification, and privacy review. See
[docs/PRIVACY.md](docs/PRIVACY.md).

MIT. See [LICENSE](LICENSE).
