# Implementation Tuning Agents

## Purpose

This document defines seven review lenses used to tune changes before they are integrated.

They are not new protocols, autonomous authorities, or runtime agents. They are named perspectives that make implementation review explicit and repeatable.

A maintainer remains responsible for the final decision. Deterministic validators and tests remain the executable source of acceptance or rejection.

## The seven tuning agents

### Idea Analyst

Checks whether the change preserves the central idea and uses concepts consistently.

Questions:

- What problem is the change solving?
- Does it preserve the difference between readiness, transition reasoning, and interface verification?
- Is a new concept truly required?

### Project Analyst

Checks scope, milestone fit, dependencies, and backlog alignment.

Questions:

- Does the change belong in the current version?
- Does it complete an existing backlog item before creating another one?
- Is the smallest useful change being proposed?

### Implementation Analyst

Checks schemas, validators, examples, tests, and failure paths.

Questions:

- Is the documented rule executable or mechanically checkable?
- Are positive and negative cases covered?
- Does the implementation preserve existing behavior unless change is intentional?

### Customer Advocate

Checks whether a user can understand when and why to use the feature.

Questions:

- What decision becomes easier for the user?
- Is the operational rule stated in plain language?
- Does the change create unnecessary work for ordinary use cases?

### Repository Reviewer

Checks repository-wide consistency and provenance.

Questions:

- Do README, specs, examples, validators, tests, backlog, roadmap, and CI agree?
- Are canonical paths and commands still valid?
- Has duplicated contract language been removed or protected against drift?

### Stabilizer

Checks safety, compatibility, regression risk, and scope creep.

Questions:

- What existing behavior could break?
- Can the change be smaller or more reversible?
- Is there evidence that the change works and a test that fails when it regresses?

The Stabilizer blocks integration when a known contract conflict, missing evidence, or failing deterministic test remains unresolved.

### Innovator

Searches for a smaller, clearer, or more valuable improvement after the contract is stable.

Questions:

- Can the same value be delivered with less machinery?
- Is there a bounded experiment that produces evidence quickly?
- What future opportunity should be recorded without expanding current scope?

The Innovator may propose changes but cannot override protocol boundaries, the Stabilizer, or failing tests.

## Review sequence

```text
idea
-> project scope
-> implementation
-> customer value
-> repository consistency
-> stabilization
-> bounded innovation
-> maintainer decision
```

Conflicts are resolved in this order:

1. executable contract and safety constraints;
2. stability and compatibility;
3. customer value and clarity;
4. innovation.

A novel idea does not override a broken contract. A stable implementation that creates no user value should be reconsidered rather than integrated automatically.

## Canonical protocol-boundary review

For IFP, TIP, and their handoff, every tuning review must preserve these statements:

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

## Lightweight review record

A change review may be summarized without creating a new schema:

```text
Idea: what problem and boundary are preserved?
Project: why now and why this scope?
Implementation: what files, behavior, and tests change?
Customer: what becomes clearer or safer?
Repository: what documentation and canonical paths must agree?
Stabilizer: what regression or scope risk was blocked?
Innovator: what bounded improvement remains possible?
Decision: integrate, revise, defer, or reject.
```

This review record is process guidance. TIP records remain the protocol artifact for transition reasoning.