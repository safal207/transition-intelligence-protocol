# Transition Intelligence Protocol

[![Validate protocol family](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml)

**Transition Intelligence Protocol** is a framework for reasoning about state, tension, cause, transition, cooperation, and action.

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
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

TIP reasons about the next transition from a known state:

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

Specification: [`spec/v0.1.md`](spec/v0.1.md)

### Explicit handoff

The handoff is an interface contract, not a third protocol:

```text
IFP Ready State
-> verified handoff record
-> TIP State
-> validated transition
```

Handoff contract: [`protocols/ifp/tip-handoff.md`](protocols/ifp/tip-handoff.md)

IFP answers: **Is the system ready to begin?**

TIP answers: **What transition is justified next?**

The handoff answers: **Did this exact ready state become this exact TIP state?**

### Kairos research integration

The optional Kairos profile exports a justified TIP transition proposal for research-only phase-window assessment:

```text
IFP Ready State
-> TIP justified transition
-> versioned TIP export
-> Kairos phase-window assessment
```

This is a bounded interoperability profile, not a third protocol and not a merger of TIP with Kairos. Neither side gains execution, clinical, approval, ownership, delivery, or merge authority.

Profile: [`integrations/kairos/v0.1.md`](integrations/kairos/v0.1.md)

## Why this exists

Many decision systems answer only one question:

> What should be done next?

Transition Intelligence asks:

1. What state are we in?
2. What tension is creating pressure for change?
3. What cause makes the transition meaningful?
4. What transition is likely to happen?
5. Will the transition preserve cooperation?
6. What action is justified now?

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

Validate the TIP-to-Kairos export profile through its regression suite:

```bash
python -m unittest tests.test_kairos_profile -v
```

Run all validator self-tests:

```bash
python -m unittest discover -s tests -v
```

Compatibility command:

```bash
python scripts/validate_examples.py
```

See [`docs/validation.md`](docs/validation.md) and [`docs/cli.md`](docs/cli.md).

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

Transition
  -> movement from one state to another

Cooperation
  -> whether the new state remains stable among participants

Action
  -> the smallest justified next step
```

## Repository structure

```text
transition-intelligence-protocol/
  README.md
  ROADMAP.md
  spec/
    v0.1.md
  protocols/
    ifp/
      spec.md
      tip-handoff.md
  integrations/
    kairos/
      v0.1.md
      profile.v0.1.json
  schemas/
    tip-record.schema.json
    ifp-record.schema.json
    ifp-tip-handoff.schema.json
  examples/
    json/
      startup-pivot.tip.json
      human-ai-agent.tip.json
      family-conflict.tip.json
      repository-next-step.tip.json
    ifp/
      project-initialization.ifp.json
    handoff/
      project-to-next-step.handoff.json
    integrations/
      kairos-export.tip.json
  tip/
    __main__.py
    validator.py
    ifp_validator.py
    handoff_validator.py
    kairos_profile.py
  tests/
    test_validator.py
    test_ifp_validator.py
    test_handoff_validator.py
    test_kairos_profile.py
  docs/
    cli.md
    validation.md
  scripts/
    validate_examples.py
```

## Assurance rule

A semantic rule is added only together with a negative test that proves the validator can detect its violation.

```text
new rule
-> negative case
-> expected failure assertion
-> CI execution
```

## Status

Early protocol-family foundation.

Current focus:

- keep TIP and IFP records small and inspectable;
- require negative tests for semantic rules;
- preserve explicit provenance from IFP readiness into TIP state reasoning;
- keep external integrations as small, versioned profiles rather than protocol mergers;
- avoid splitting protocols into separate repositories before their interfaces stabilize.

## License

MIT
