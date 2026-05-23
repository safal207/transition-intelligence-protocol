# Transition Intelligence Protocol

**Transition Intelligence Protocol** is a framework for reasoning about state, tension, cause, transition, cooperation, and action.

It treats decisions not as isolated outputs, but as **state transitions** that must be understood, justified, and tested for cooperative stability.

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

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

## Intellectual frame

The protocol is inspired by three ideas:

- **I Ching / Book of Changes** as a historical model of transition states.
- **Nash cooperation and equilibrium** as a model of strategic stability between actors.
- **Causal reasoning** as a way to preserve why an action was allowed, not merely what happened.

This project does **not** treat the I Ching as mysticism or prediction. It uses the 64-state structure as a design metaphor for transition mapping.

## Core model

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
  docs/
    concept.md
    64-transition-states.md
    nash-cooperation.md
    cause-and-transition.md
    protocol-model.md
  schemas/
    transition-state.schema.json
    cause.schema.json
    cooperation-check.schema.json
  examples/
    startup-decision.md
    human-ai-agent.md
    family-conflict.md
  LICENSE
```

## Example use

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

Early conceptual foundation.

Current goal: define a clean protocol vocabulary before implementation.

## License

MIT
