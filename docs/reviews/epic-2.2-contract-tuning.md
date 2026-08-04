# Epic 2.2 Contract Tuning Review

Status: Implemented; visible CI confirmation pending.

## Change under review

Consolidate the language that separates IFP, TIP, and the IFP-to-TIP handoff.

## Idea Analyst

Finding:

The core distinction is conceptual rather than technical:

- IFP establishes whether a starting state is ready;
- TIP reasons about a transition from a known state;
- the handoff proves provenance when the state moves from IFP into TIP.

Risk found:

Direct wording such as `IFP Ready State -> TIP State` can hide the verification interface and make the handoff appear optional even when IFP provenance is claimed.

Adjustment:

Adopt one canonical four-statement boundary across all contract surfaces.

## Project Analyst

Finding:

The work belongs to Epic 2.2 and does not require a new protocol, schema, or repository split.

Risk found:

Turning review roles into autonomous runtime agents would expand scope beyond documentation consistency.

Adjustment:

Keep the change limited to contract language, review guidance, repository assertions, and existing CI execution.

## Implementation Analyst

Finding:

README, IFP spec, TIP spec, and handoff spec previously described the relationship with different levels of precision.

Risk found:

The IFP specification duplicated a partial handoff shape that could drift away from the canonical handoff schema and validator.

Adjustment:

- remove the duplicate handoff shape from the IFP spec;
- link to the canonical handoff contract;
- add exact boundary assertions to `tests/test_documentation.py`.

## Customer Advocate

Finding:

A user needs two operational answers:

1. Do I need IFP before every TIP record?
2. When is the handoff mandatory?

Adjustment:

State plainly:

- IFP is not required when the TIP starting state is already trusted and sufficient;
- the explicit handoff is required when IFP supplies that state.

This avoids ceremony for ordinary TIP use while preserving provenance when initialization evidence matters.

## Repository Reviewer

Finding:

The contract must agree across README, both specifications, the handoff document, backlog, roadmap, validation documentation, tests, and CI.

Adjustment:

- add `docs/tuning-agents.md`;
- add the tuning guide to README and release scope;
- extend documentation tests to cover contract language and tuning-agent limits;
- update backlog, roadmap, and validation documentation.

## Stabilizer

Finding:

Named review agents can create false confidence if their outputs are not bounded or mechanically checked.

Adjustment:

- keep maintainers responsible for final decisions;
- keep deterministic validators and tests authoritative;
- prevent the Innovator from overriding protocol boundaries or failing tests;
- make a missing canonical boundary fail documentation tests.

Focused validation:

- clean documentation reconstruction: 6 of 6 checks passed;
- removal of one canonical boundary: rejected;
- removal of one tuning-agent role: rejected;
- clean restoration: passed again.

The full repository suite was not run locally because the execution environment could not resolve `github.com` for cloning.

## Innovator

Finding:

The seven perspectives are useful beyond this change, but a new agent protocol or scoring system would be premature.

Adjustment:

Document a lightweight reusable sequence:

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

Deferred opportunity:

Later, reviewed implementation changes may be compared with real regressions and customer outcomes. No scoring or autonomous orchestration is added in v0.1.

## Decision

Integrate.

The final contract is:

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

The change remains documentation-and-test focused and does not alter TIP, IFP, or handoff runtime validation behavior.