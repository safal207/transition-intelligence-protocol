# Protocol Model

This document defines the first working model of the Transition Intelligence Protocol.

## Pipeline

```text
State -> Tension -> Cause -> Transition -> Cooperation -> Action
```

## 1. State

The current configuration of the situation.

A state should include:

- actors;
- context;
- known facts;
- constraints;
- unresolved signals.

## 2. Tension

The pressure that makes the current state unstable or incomplete.

Tension may come from:

- conflict;
- ambiguity;
- urgency;
- risk;
- opportunity;
- contradiction;
- unmet need.

## 3. Cause

The reason a transition exists or an action may be permitted.

Cause must be inspectable. A system should be able to explain why the transition was considered.

## 4. Transition

The movement from one state to another.

A transition should identify:

- previous state;
- next possible state;
- trigger;
- reversibility;
- expected consequence;
- uncertainty.

## 5. Cooperation

The strategic stability of the transition among participants.

A cooperation check asks whether the new state remains acceptable and rational for the important actors.

## 6. Action

The concrete step taken after the transition is understood.

The action should be:

- justified by cause;
- proportional to tension;
- compatible with cooperation;
- reviewable after execution.

## Minimal protocol record

```json
{
  "id": "tip.record.example",
  "state": {},
  "tension": {},
  "cause": {},
  "transition": {},
  "cooperation": {},
  "action": {},
  "status": "draft"
}
```

## Status values

| Status | Meaning |
| --- | --- |
| draft | The record is being formed. |
| clarified | State and tension are clear enough. |
| blocked | Action is not justified. |
| committed | Action is allowed. |
| reviewed | Outcome has been inspected. |

## Design rule

```text
Do not jump from state to action.
Pass through tension, cause, transition, and cooperation first.
```
