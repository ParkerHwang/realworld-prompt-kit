# Authoring Guide

## Start from a user situation

Write the latent situation before writing prompt text:

- who is trying to do what;
- what information they have;
- what information is missing;
- what outcome is useful;
- what the model must not invent or do.

This becomes one `scenario_id`.

## Write the canonical realization

The canonical prompt should be natural and clear, but not artificially optimized
for a specific model. It should expose the intended task and all information
needed for the declared response mode.

## Write the naturalistic realization independently

Do not mechanically corrupt the canonical text. Imagine how the same person
would type it into a chat box:

- lead with the problem or with context;
- leave ordinary shorthand intact;
- use realistic fragments and transitions;
- split messages when a person would send a follow-up;
- keep every decision-critical fact required by the semantic relation;
- avoid random noise that no real user would produce.

Korean and English should be authored as native messages. They may differ in
politeness, sentence order, and workplace idiom while preserving the same goal.

Each naturalistic profile must be visible in the prompt itself. A label is not
evidence: `message_burst` means two or more user messages, `rambling_stream`
means at least 180 characters in each locale, and `terse_fragment` means no
more than 32 whitespace tokens in each locale. Paste/format-noise,
emoji, code-switching, correction, change, and resumption profiles need a
corresponding cue. Ambiguous discourse labels such as an implicit goal or
polite request are reviewed from the complete utterance; generic FOCUS,
boundary, safety, or a literal word such as `jargon` alone does not satisfy
them; code-switching should use a task-specific field or technical term in the
localized message. The v0.1 validator checks
the objective cues and the release review records the softer judgments.

Do not reuse a latent topic across blocks and call the condition new breadth.
Before assigning the row, record a distinct evidence fixture, user goal, and
expected artifact. The normalized semantic-duplicate lint compares these
fields across blocks and the canonical-similarity lint catches copied prompt
templates.

Naturalistic diversity has a corpus-level limit as well as a pairwise one. For
each locale/form, count exact six-token n-grams by distinct scenario presence.
Any non-whitelisted n-gram in more than 5% of the full union or its originating
worker partition is a release error. A longer repeated phrase is already
captured by its six-token prefix; no generic boilerplate is whitelisted.

Retrieval guidance must fit the latent fixture. The validator rejects known
transport tails such as 도시·노선·운행일 / city, route, service day and
stop/route-missing variants when the title and goal contain no transport
context. Korean particle and ending defects are also release errors; do not
repair quota failures by appending a domain- or transport-irrelevant sentence.
An apparent terse prompt with eight or fewer whitespace tokens must also stay
under the configured short-message character cap and must not serialize
topic/context/result fields with delimiters.

Keep decision-critical numeric literals in both localized naturalistic
realizations. The validator checks presence of canonical numeric facts and
flags English possessive nouns that become bare plurals.

## Set the response boundary

Choose the expected mode before reviewing outputs. Ask:

1. Can a competent person safely infer the missing detail?
2. Would a wrong inference materially change the action?
3. Can the answer proceed with a visible assumption?
4. Is one short clarification enough?

Encode the result instead of rewarding whichever behavior the evaluated model
happened to take.

## Write evaluation rules

Invariants should be observable and scenario-specific. Good examples:

- preserve every owner and date from the notes;
- distinguish an unresolved question from a decision;
- do not recommend an option that violates a hard constraint;
- do not promise a refund arrival date that was not provided.

Rubric dimensions should describe qualities, not a preferred writing style.
Failure signals should be concrete enough for a reviewer to cite.
