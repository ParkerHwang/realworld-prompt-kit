# Contributing

Thank you for helping build a benchmark around real user language rather than
only polished benchmark prose.

## Contribution units

For the v0.1 Broad Core, the preferred contribution is one complete coverage
block:

1. a named semantic coverage goal;
2. eight distinct scenarios selected with a covering array or documented
   boundary rationale;
3. canonical and naturalistic realizations;
4. evaluation invariants, rubric dimensions, and failure signals;
5. provenance and privacy metadata;
6. a passing validator run.

For the v0.2 Artifact Core, the preferred contribution is one complete work
episode:

1. a distinct workplace goal and one primary workflow job;
2. synthetic, rights-cleared input files with fixed SHA-256 hashes;
3. four paired Korean/English canonical/naturalistic requests;
4. an exact editable-output and authority contract;
5. non-compensable hard gates and atomic, evidence-linked rubric items;
6. executable checks plus a usable reference artifact;
7. explicit practitioner-calibration and review status;
8. passing v0.1 and v0.2 validators and tests.

Smaller corrections are welcome when they fix a factual, linguistic, privacy,
schema, scoring, file-format, or rendering problem.

## Authoring rules

- Write Korean and English as native utterances, not literal translations.
- Preserve the same latent user goal across paired realizations.
- Do not create "naturalistic" prompts by adding random typos alone.
- Label synthetic prompts as synthetic.
- Never submit private conversations, credentials, contact details, customer
  data, health data, payment data, or other identifying information.
- Do not silently fill decisive missing facts. Encode whether the expected
  response should infer, state assumptions, clarify, hold, or escalate.
- Do not count translations, paraphrases, treatment arms, or repeated runs as
  new semantic scenarios.
- Do not compare an artifact byte-for-byte with one reference when multiple
  valid structures can satisfy the contract.
- Do not mark an episode reviewed because automated checks pass. Human
  calibration requires separately recorded practitioner evidence.
- Keep all side effects within the declared authority boundary; v0.2 accepts
  only read-only, draft-only, and local reversible work.

## Validation

Run:

```bash
python3 tools/validate.py
python3 tools/validate.py --manifest data/v0.2/manifest.json
python3 -m unittest discover -s tests
```

## Pull requests

Explain:

- which coverage cell is added or corrected;
- why each scenario is meaningfully distinct;
- how canonical and naturalistic prompts remain semantically paired;
- how expected behavior is scored;
- the data origin and privacy review status.

For v0.2 episodes, also explain:

- why each attachment is necessary and which source is authoritative;
- which output properties are hard gates versus human quality judgments;
- how reference files were rendered and inspected;
- what remains uncalibrated and which claim boundaries still apply.

Keep real or real-derived data out of a pull request unless the repository's
rights and privacy process has explicitly approved it.
