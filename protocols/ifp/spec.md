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

## Relationship with TIP

```text
IFP Ready State
-> TIP State
-> Tension
-> Cause
-> Transition
-> Cooperation
-> Action
```

IFP establishes a trustworthy starting point. TIP reasons about the next transition from that point.

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

A ready IFP record may provide the initial state for a TIP record.

Recommended handoff fields:

```json
{
  "source_protocol": "IFP",
  "source_record_id": "ifp.example.project",
  "ready_state": "Repository initialized and validation feedback passed"
}
```

The handoff does not guarantee that every future action is valid. It only establishes that the starting state has been checked.
