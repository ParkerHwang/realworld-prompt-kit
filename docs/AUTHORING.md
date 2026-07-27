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
