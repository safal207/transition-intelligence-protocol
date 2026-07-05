# Transition Intelligence Protocol

[![Validate protocol family](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml/badge.svg)](https://github.com/safal207/transition-intelligence-protocol/actions/workflows/validate.yml)

**Transition Intelligence Protocol** is a framework for reasoning about state, tension, cause, transition, cooperation, and action.

It treats decisions not as isolated outputs, but as **state transitions** that must be understood, justified, and tested for cooperative stability.

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

## Protocol family

This repository now contains two cooperating protocols.

### Initialization Feedback Protocol (IFP)

IFP establishes a checked starting state:

```text
Undefined -> Configured -> Feedback Received -> Corrected -> Ready
```

Its draft specification is available at [`protocols/ifp/spec.md`](protocols/ifp/spec.md).

### Transition Intelligence Protocol (TIP)

TIP reasons about the next transition from a known state:

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

### Handoff

```text
IFP Ready State
-> TIP State
-> Validated Transition
```

IFP answers: **Is the system ready to begin?**

TIP answers: **What transition is justified next?**

## Why this exists

Many decision systems answer only one question:

> What should be done next?

Transition Intelligence asks a deeper sequence of questions:

1. What state are we in?
2. What tension is creating pressure for change?
3. What cause makes the transition meaningful or permitted?
4. What transition is likely to happen?
5. Will the transition preserve cooperation between participants?
6. What action is justified now?

This makes the protocol useful for human-AI cooperation, agent safety, strategic decisions, startup pivots, conflict analysis, and any system where a wrong transition can create long-term damage.

## v0.1 draft

The first TIP draft specification is available here:

- [`spec/v0.1.md`](spec/v0.1.md)

v0.1 defines the minimal **TIP Record** format:

```text
state + tension + cause + transition + cooperation -> action
```

A record is invalid if it contains an action without the reasoning chain that makes the action inspectable.

## Validation and CLI

Validate TIP records:

```bash
python -m tip validate examples/json/
```

Validate IFP records:

```bash
python -m tip validate-ifp examples/ifp/
```

Run all validator self-tests:

```bash
python -m unittest discover -s tests -v
```

The compatibility command remains available:

```bash
python scripts/validate_examples.py
```

See [`docs/validation.md`](docs/validation.md) and [`docs/cli.md`](docs/cli.md) for details.

## Intellectual frame

The protocol is inspired by three ideas:

- **I Ching / Book of Changes** as a historical model of transition states.
- **Nash cooperation and equilibrium** as a model of strategic stability between actors.
- **Causal reasoning** as a way to preserve why an action was allowed, not merely what happened.

This project does **not** treat the I Ching as mysticism or prediction. It uses the 64-state structure as a design metaphor for transition mapping.

## Core TIP model

```text
State
  -> current configuration

Tension
  -> pressure, contradiction, imbalance, or unresolved force

Cause
  -> why a transition is happening or why an action is permitted

Transition
  -> movement from one state to another

Cooperation
  -> whether the new state remains stable among participants

Action
  -> the smallest justified step that can be taken now
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
  docs/
    cli.md
    concept.md
    64-transition-states.md
    nash-cooperation.md
    cause-and-transition.md
    protocol-model.md
    validation.md
  schemas/
    tip-record.schema.json
    ifp-record.schema.json
    transition-state.schema.json
    cause.schema.json
    cooperation-check.schema.json
  examples/
    json/
      startup-pivot.tip.json
      human-ai-agent.tip.json
      family-conflict.tip.json
    ifp/
      project-initialization.ifp.json
  tip/
    __init__.py
    __main__.py
    validator.py
    ifp_validator.py
  tests/
    test_validator.py
    test_ifp_validator.py
    fixtures/
  scripts/
    validate_examples.py
  LICENSE.md
```

## Example TIP use

```text
Situation:
A founder wants to pivot a product.

State:
The current product has usage but weak retention.

Tension:
Users like the idea but do not build a habit around it.

Cause:
The current workflow does not connect to an urgent enough pain.

Transition:
Move from broad productivity tool to narrow decision-support protocol.

Cooperation:
Check whether users, founder, team, and future partners all gain from the new direction.

Action:
Run one narrow pilot before changing the full product.
```

## Status

Early protocol-family foundation.

Current focus:

- keep TIP and IFP records small and inspectable;
- require negative tests for semantic invariants;
- establish explicit handoff from IFP readiness into TIP state reasoning;
- avoid splitting protocols into separate repositories before their interfaces stabilize.

## License

MIT
