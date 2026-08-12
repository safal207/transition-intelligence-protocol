# Transition Intelligence Protocol

[![Validate protocol family](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml)

**Transition Intelligence Protocol** is a framework for reasoning about state, tension, cause, transition, cooperation, action, and the observed result of a reviewed action.

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

Reviewed records may close the loop:

```text
Action -> Review -> Next State
```

## Protocol family

This repository contains two cooperating protocols.

### Initialization Feedback Protocol (IFP)

IFP establishes a checked starting state:

```text
Undefined -> Configured -> Feedback Received -> Corrected -> Ready
```

Specification: [`protocols/ifp/spec.md`](protocols/ifp/spec.md)

### Transition Intelligence Protocol (TIP)

TIP reasons about the next transition from a known state and may later record the observed result:

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action -> Review
```

Specification: [`spec/v0.1.md`](spec/v0.1.md)

### Explicit handoff

The handoff connects a verified IFP ready state to the exact TIP state that consumes it:

```text
IFP Ready State
-> verified handoff record
-> TIP State
-> validated transition
```

Handoff contract: [`protocols/ifp/tip-handoff.md`](protocols/ifp/tip-handoff.md)

### Canonical boundaries

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

IFP answers: **Is the system ready to begin?**

TIP answers: **What transition is justified next, and what happened when it was reviewed?**

The handoff answers: **Did this exact IFP ready state become this exact TIP state?**

A standalone TIP record does not need an artificial IFP record when its starting state is already trusted and sufficient. It must not claim IFP provenance unless the explicit handoff is present and valid.

## Why this exists

Many decision systems answer only one question:

> What should be done next?

Transition Intelligence asks:

1. What state are we in?
2. What tension is creating pressure for change?
3. What cause makes the transition meaningful?
4. Who assessed confidence in that cause, by what method, and what alternatives remain?
5. What transition is likely to happen?
6. Will the transition preserve cooperation?
7. What action is justified now?
8. What was actually observed after the action?

This makes the protocol useful for human-AI cooperation, agent safety, strategic decisions, startup pivots, conflict analysis, and systems where a wrong transition can create long-term damage.

## Validation and CLI

Validate TIP records:

```bash
python -m tip validate examples/json/
```

Validate IFP records:

```bash
python -m tip validate-ifp examples/ifp/
```

Validate the canonical IFP-to-TIP handoff:

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

Run validator and documentation consistency tests:

```bash
python -m unittest discover -s tests -v
```

Compatibility command:

```bash
python scripts/validate_examples.py
```

See [`docs/validation.md`](docs/validation.md) and [`docs/cli.md`](docs/cli.md).

## v0.1-draft checkpoint

Release scope and current limitations are recorded in [`RELEASE_NOTES.md`](RELEASE_NOTES.md).

The release marker is created only from a `main` commit whose `Validate protocol family` workflow succeeds. This keeps the public marker tied to the same executable checks described by the repository.

## Intellectual frame

The project is inspired by:

- **I Ching / Book of Changes** as a historical model of transition states;
- **Nash cooperation and equilibrium** as a model of strategic stability;
- **causal reasoning** as a way to preserve why an action was justified.

The project does not use the I Ching as prediction. It uses the 64-state structure as a design metaphor for transition mapping.

## Core TIP model

```text
State
  -> current configuration

Tension
  -> pressure, contradiction, imbalance, or unresolved force

Cause
  -> why a transition is happening
  -> who assessed confidence, how, and against which alternatives

Transition
  -> movement from one state to another
  -> spatial reach, feedback delay, and reversibility

Cooperation
  -> whether the new state remains stable among participants

Action
  -> the smallest justified next step

Review
  -> the observed result, evidence, and next state after action
```

## Implementation tuning

Changes may be reviewed through seven named tuning lenses: Idea Analyst, Project Analyst, Implementation Analyst, Customer Advocate, Repository Reviewer, Stabilizer, and Innovator.

These are review perspectives, not additional protocols or autonomous authorities. Their responsibilities and conflict rules are documented in [`docs/tuning-agents.md`](docs/tuning-agents.md).

## Repository structure

```text
transition-intelligence-protocol/
  README.md
  ROADMAP.md
  BACKLOG.md
  RELEASE_NOTES.md
  spec/
    v0.1.md
  protocols/
    ifp/
      spec.md
      tip-handoff.md
  schemas/
    tip-record.schema.json
    ifp-record.schema.json
    ifp-tip-handoff.schema.json
  examples/
    json/
      startup-pivot.tip.json
      bounded-learning-pilot.tip.json
      human-ai-agent.tip.json
      family-conflict.tip.json
      repository-next-step.tip.json
      pilot-review.tip.json
    ifp/
      project-initialization.ifp.json
    handoff/
      project-to-next-step.handoff.json
  tip/
    __main__.py
    validator.py
    ifp_validator.py
    handoff_validator.py
  tests/
    test_validator.py
    test_ifp_validator.py
    test_handoff_validator.py
    test_documentation.py
  docs/
    cli.md
    validation.md
    tuning-agents.md
  scripts/
    validate_examples.py
```

## Assurance rule

A semantic or documentation rule is added only together with a negative test or repository assertion that proves drift can be detected.

```text
new rule
-> negative case or consistency assertion
-> expected failure
-> CI execution
```

## Status

v0.1-draft release preparation.

Current focus:

- keep TIP and IFP records small and inspectable;
- require negative tests for semantic rules;
- preserve explicit provenance from IFP readiness into TIP state reasoning;
- preserve confidence provenance before a value can authorize committed action;
- close the action-to-review loop without claiming more causality than the evidence supports;
- keep canonical protocol boundaries, documentation links, and commands synchronized with executable behavior;
- use tuning agents as bounded review lenses rather than adding new protocols;
- create the v0.1-draft marker only from a green release-preparation `main` commit.

## License

MIT
