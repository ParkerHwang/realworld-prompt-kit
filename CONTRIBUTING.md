# Contributing

Thank you for helping build a benchmark around real user language rather than
only polished benchmark prose.

## Contribution unit

The preferred contribution is one complete coverage block:

1. a named semantic coverage goal;
2. eight distinct scenarios selected with a covering array or documented
   boundary rationale;
3. canonical and naturalistic realizations;
4. evaluation invariants, rubric dimensions, and failure signals;
5. provenance and privacy metadata;
6. a passing validator run.

Smaller corrections are welcome when they fix a factual, linguistic, privacy,
schema, or scoring problem.

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

## Validation

Run:

```bash
python3 tools/validate.py
python3 -m unittest discover -s tests
```

## Pull requests

Explain:

- which coverage cell is added or corrected;
- why each scenario is meaningfully distinct;
- how canonical and naturalistic prompts remain semantically paired;
- how expected behavior is scored;
- the data origin and privacy review status.

Keep real or real-derived data out of a pull request unless the repository's
rights and privacy process has explicitly approved it.
