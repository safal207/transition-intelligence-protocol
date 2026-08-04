# Initialization Feedback Protocol — Draft v0.1

## Purpose

Initialization Feedback Protocol (IFP) moves a subject from an undefined or unverified condition into a testable initial state.

IFP does not decide the next strategic transition. It answers a narrower question:

> Has the initial state been configured, observed, corrected when necessary, and shown to be ready?

## Core flow

```text
Undefined
-> Configured
-> Feedback Received
-> Corrected (when needed)
-> Ready
```

A blocked initialization may stop before `Ready`.

## Canonical boundaries

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

IFP should be used when the starting state still needs configuration, observation, correction, or readiness evidence. It should not be created only to satisfy ceremony around a TIP record whose state is already trusted and sufficient.

## Relationship with TIP

When IFP supplies the starting state, the relationship is:

```text
IFP Ready State
-> verified handoff record
-> TIP State
-> Tension
-> Cause
-> Transition
-> Cooperation
-> Action
```

The handoff proves that the exact checked state produced by IFP became the exact state consumed by TIP. It does not authorize the later transition or action.

The canonical interface is documented in [`tip-handoff.md`](tip-handoff.md). This specification intentionally does not duplicate the handoff record shape.

## IFP Record

An IFP record contains:

- `id` — stable record identifier;
- `title` — human-readable name;
- `status` — lifecycle state;
- `subject` — what is being initialized;
- `setup` — initial parameters and assumptions;
- `feedback` — how the system responded;
- `correction` — changes made after feedback;
- `readiness` — whether initialization is complete and what evidence supports that result.

## Status values

```text
draft
configured
feedback_received
corrected
ready
blocked
```

## Minimal invariants

1. `status = ready` requires `feedback.passed = true`.
2. `status = ready` requires `readiness.ready = true`.
3. `readiness.ready = true` requires at least one evidence item.
4. `correction.required = true` requires at least one recorded change.
5. Failed feedback cannot produce a ready result.

## Handoff to TIP

A ready IFP record may provide the initial state for a TIP record only through the explicit handoff contract.

The handoff preserves the source record, ready state, target TIP record, consumed TIP state, and verification evidence. A valid handoff establishes provenance for the starting state; it does not guarantee that every future action is valid.
