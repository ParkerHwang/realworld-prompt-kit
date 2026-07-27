# v1 Release Criteria

The v1 release counts semantic breadth separately from prompt realizations.
The broad core is complete only when the checked-in artifacts and the
dependency-free validator agree on every gate below:

- 21 task intents, 110 disjoint CB8 blocks, and 880 unique semantic scenarios;
- exactly eight rows numbered 1 through 8 in every block, with the seven
  two-level facets and complete pairwise coverage;
- exactly four realizations per scenario: Korean and English, each canonical
  and naturalistic, for 3,520 realizations total;
- globally unique `scenario_id`, `semantic_group_id`, and `prompt_id` values;
- only the 28 catalog domain IDs and 24 naturalistic profile IDs;
- domain and profile minimum-presence overlays plus the broad composition
  ratios in `data/v1.0/manifest.json`;
- synthetic provenance, MIT rights basis, and
  `contains_personal_data=false` on every public scenario;
- no exact or normalized prompt duplicates, placeholder leakage, missing
  language, canonical/naturalistic identity, or insufficient prompt substance;
- similarity lint with a warning at 0.75 and a failure at 0.85. High-similarity
  exceptions must be rare and recorded in the release report;
- naturalistic feature evidence and response-boundary lint across all four
  realizations. Objective profiles such as message bursts, rambling streams,
  emoji, pasted/format-noise cues, and explicit correction or resumption cues
  must be observable. `rambling_stream` also requires at least 180 characters
  in each locale, while `terse_fragment` stays at or below 32 whitespace
  tokens per locale; a semicolon field template is not a terse fragment.
  Delimited topic/context/result field strings and overlong messages with very
  few whitespace tokens are rejected as serialized templates.
- canonical numeric facts must remain present in each same-locale naturalistic
  rendering; English possessive-to-bare-plural corruption is rejected;
  Softer discourse labels remain in the block review evidence rather than
  being inferred from generic boilerplate. Benign
  coaching/support prompts must not use `refuse_or_escalate` without a concrete
  risk or authority boundary;
- exact six-token phrase-concentration lint with no generic whitelist. The
  denominator is semantic scenarios per locale/form: every non-whitelisted
  n-gram above 5% fails. The scan runs once over the 880-scenario union and
  independently over the 224-, 320-, and 336-scenario partitions. Counting an
  exact six-token presence is sufficient to catch every longer n-gram because
  every longer n-gram has a six-token prefix;
- semantic-duplicate lint that rejects reusing one latent topic, fixture, or
  goal across multiple blocks under different condition labels;
- rendered-message grammar lint, including the known Korean malformed-particle
  and -라고 constructions, English capitalization/punctuation defects, and
  transport-specific retrieval tails in non-transport titles/goals;
- a review sample from every block with semantic-fit and naturalistic-realism
  evidence recorded in the release review report.

`status=reviewed` means a row-level human or named review pass has been
recorded; it is not a synonym for “the automated validator passed.” The v1
manifest remains `release_candidate` while any rows are still `draft`, and the
coverage report must publish the full status distribution. A block sample does
not authorize bulk promotion of its other seven rows. Only a separately
evidenced release may use `status=released` with no draft rows.

The broad core does not claim OpenSocrates method routing, confusable-edge
coverage, adapter conformance, dynamic-live behavior, side-effect safety,
additional locales, or modality overlays. Those remain planned extension suites
with separate manifests and evidence requirements under `suites/templates/`.

Run the release checks from the repository root:

```bash
python3 tools/validate.py --manifest data/v0.1/manifest.json
python3 tools/validate.py --manifest data/v1.0/manifest.json
python3 -m unittest discover -s tests
python3 tools/export_jsonl.py --manifest data/v1.0/manifest.json --output build/realworld-prompt-kit-v1.jsonl
python3 tools/coverage_report.py
```

The coverage report retains the earlier requirements-only zero-observation
audit as a dated `pre_generation` baseline. It must not be relabeled as current
coverage, and current counts are generated only from the checked-in scenario
artifacts.

Integration provenance and repairs are recorded in the manifest's
`release_evidence` and the three worker reports. In particular, the independent
B baseline was 421 rendered-content failures (360 English sentence-boundary
capitalization, 39 Korean code-switch cues, 9 resume cues, 7 embedded-
instruction cues, 5 numeric fact losses, and 1 rambling-length failure); the
path-restricted integration repair reduced every class to zero without adding
a phrase whitelist or promoting scenario status.

The v0.1 manifest and validator remain supported. A v1 release may add files
under `data/v1.0/` without rewriting or reinterpreting the v0.1 pack.
