# Design

## Root question

Can a model or agent complete the same user goal when the request is expressed
as controlled benchmark prose and as ordinary, unpolished conversation?

## Canonical layers

The kit separates:

1. `scenario_id`: the latent user situation and goal;
2. `prompt_id`: one language and discourse realization;
3. coverage: the task, domain, input, risk, and utterance cells represented;
4. evaluation: expected response mode, invariants, rubric, and failure signals;
5. execution: the model, harness, tools, treatment, and repeat policy;
6. records: immutable outputs and re-creatable scores.

Only the first four live in the prompt kit. Execution systems should flatten or
adapt them without changing the source scenario.

## CB8

`CB8` is an eight-scenario coverage block. The initial pack uses an
eight-row, seven-factor, two-level orthogonal array. Every pair of factor levels
appears together, avoiding an exhaustive Cartesian product while exposing
interactions.

The seven v0.1 factors are:

- context scale: short / long
- goal clarity: explicit / implicit
- output shape: prose / structured
- evidence state: complete / incomplete
- stakes: low / moderate
- interaction: single / message burst
- surface noise: light / heavy

CB8 is a coverage primitive, not a universal claim that eight examples are
enough for every risk. High-stakes, multi-level, tool-mutating, or known failure
interactions require additional blocks.

## Naturalistic utterances

Naturalistic prompts may contain:

- fragments or omitted subjects;
- colloquial language and shorthand;
- thoughts written in discovery order;
- multiple requests or mixed priorities;
- self-correction and scope change;
- code-switching and workplace jargon;
- pasted material interleaved with instructions;
- message bursts and follow-ups that rely on prior context;
- emotional urgency without changing the underlying task.

Naturalistic is not synonymous with unsafe or adversarial. Prompt injection,
ambiguous authority, and conflicting constraints are separate coverage tags.

## Infer or clarify

Robustness is not measured by guessing every omitted fact. Every scenario
declares an expected response mode:

- `answer_directly`
- `infer_and_answer`
- `state_assumptions_and_answer`
- `ask_one_clarifying_question`
- `clarification_dialogue`
- `hold`
- `refuse_or_escalate`

A system fails if it asks needless questions for an inferable low-risk request,
or silently invents decisive information for a consequential request.

## Scoring

Each scenario includes:

- invariants: conditions that must hold;
- rubric dimensions: qualities that require anchored judgment;
- failure signals: observable mistakes;
- expected response mode by prompt form.

Pairwise A/B preference can be added by a harness, but it should not replace
absolute scoring. Reports should separate canonical task success, naturalistic
task success, and the paired expression-robustness delta.

## Harness independence

An adapter should:

1. declare supported capabilities;
2. compile messages and fixtures without silent semantic edits;
3. snapshot the rendered request;
4. execute under a versioned profile;
5. normalize output, tool events, cost, and errors;
6. distinguish unsupported capability from model failure.

The flattened JSONL export is intentionally simple enough to map into custom
evaluators, Inspect tasks, lm-evaluation-harness tasks, OpenAI Evals, or another
future runner.

## Expansion tree

New packs should expand by coverage need:

- task intent
  - retrieval, extraction, synthesis, writing, analysis, decision, planning,
    communication, execution, automation, monitoring, coaching
- domain
  - general, office, education, personal, professional, technical, industry,
    creative
- utterance condition
  - omission, disorganization, surface noise, conversation state, affect,
    conflict, permissions
- execution environment
  - text, multimodal, tool, plugin, hook, multi-agent

The total scenario count is an output of these coverage requirements, never the
starting target.
