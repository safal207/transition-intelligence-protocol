# Backlog

This backlog keeps the protocol family small, inspectable, and implementation-led.

## Working principle

Every protocol rule must move through the same chain:

```text
idea
-> documented rule
-> schema or validator behavior
-> positive example
-> negative test
-> CI execution
```

Do not add a new protocol when a smaller validation rule, example, or document cleanup is enough.

## Epic 1 — Validator correctness

Goal: make the existing validators match the schemas they claim to enforce.

### 1.1 Enforce `additionalProperties: false`

Status: Done

Cause:

- Schemas declare strict objects.
- The dependency-free schema subset must reject unknown object fields.
- Otherwise strict schemas can create a false pass.

Completed:

- reject unknown fields when `additionalProperties` is `false`;
- add negative tests for unknown top-level fields;
- add negative tests for unknown nested fields;
- cover TIP, IFP, and handoff validation paths;
- document the supported schema subset.

Definition of Done:

- invalid records with unknown fields fail;
- failure path points to the unexpected field;
- validator self-tests cover TIP, IFP, and handoff additional-property failures;
- CI runs the updated tests.

### 1.2 Add more semantic invariants

Status: In progress

Completed:

- committed TIP records require a non-empty concrete action summary;
- negative test proves a whitespace-only committed action is rejected;
- TIP specification documents the commitment rule.

Remaining tasks:

- reviewed TIP records require outcome or review notes;
- define a justified policy for low cause confidence before blocking commitment;
- handoff evidence should reference existing files where possible.

Definition of Done:

- every new invariant has a negative test;
- each error message names the failing protocol path.

## Epic 2 — Documentation and schema consistency

Goal: prevent README, specs, schemas, examples, validators, and CI from drifting apart.

### 2.1 Add documentation consistency tests

Status: Planned

Tasks:

- verify CLI commands in docs match workflow commands;
- verify README links point to existing canonical files;
- verify handoff docs reference the canonical handoff example;
- verify roadmap release scope matches existing files.

Definition of Done:

- broken links or stale canonical commands fail tests;
- docs consistency tests run in CI.

### 2.2 Consolidate protocol contract language

Status: Planned

Tasks:

- keep IFP focused on readiness only;
- keep TIP focused on transitions only;
- keep handoff as an interface contract, not a protocol;
- document that IFP is optional when the starting state is already known and sufficient;
- remove duplicate handoff descriptions when they drift.

Definition of Done:

- README, IFP spec, TIP spec, and handoff spec use the same boundaries.

## Epic 3 — CLI usability

Goal: make validation easier for humans, CI, and future agents.

### 3.1 Add machine-readable output

Status: Planned

Tasks:

- add `--json` output to `validate`;
- add `--json` output to `validate-ifp`;
- add `--json` output to `validate-handoff`;
- include `ok`, `path`, `errors`, and protocol kind.

Definition of Done:

- existing text output remains default;
- JSON output has tests;
- invalid examples produce stable machine-readable errors.

### 3.2 Add recursive validation

Status: Planned

Tasks:

- support recursive directory scanning;
- avoid accidentally validating fixtures unless requested;
- document the behavior.

Definition of Done:

- recursive mode validates nested canonical examples;
- fixture behavior is explicit and tested.

## Epic 4 — Real-life examples

Goal: prove the protocol family works outside repository self-description.

### 4.1 Add job-search example set

Status: Planned

Tasks:

- add `examples/ifp/job-search-initialization.ifp.json`;
- add `examples/json/job-search-next-step.tip.json`;
- add `examples/handoff/job-search.handoff.json`;
- validate the handoff in tests or CI.

Definition of Done:

- example explains a human decision clearly;
- all three records validate;
- the handoff proves the IFP ready state becomes the TIP state.

### 4.2 Add product-pivot example set

Status: Later

Tasks:

- convert existing startup example into full IFP -> handoff -> TIP chain;
- keep the old standalone TIP example if still useful.

## Epic 5 — Release readiness

Goal: prepare a trustworthy v0.1-draft marker.

### 5.1 Add changelog or release notes

Status: Planned

Tasks:

- add `CHANGELOG.md` or `RELEASE_NOTES.md`;
- document v0.1-draft scope;
- list current limitations honestly.

Definition of Done:

- release notes match README, roadmap, schemas, examples, and CI.

### 5.2 Create v0.1-draft marker

Status: Blocked until visible CI success

Tasks:

- verify workflow success on `main`;
- create tag or release marker;
- link release marker from README or roadmap.

## Discovery — Human memory representation

Status: Research only

Goal: test whether personal, confirmed metaphors improve understanding and later recall before building storage infrastructure.

Tasks:

- define a minimal Memory Card candidate format;
- keep concept, metaphor, retrieval cues, source, and status separate;
- distinguish textual metaphor from an optional rendered image;
- test one learning use case with delayed recall;
- do not make memory cards a new protocol until the user value is demonstrated.

## Not now

Do not start these until Epics 1-3 are stronger:

- scoring;
- transition state library expansion;
- signed provenance;
- registries;
- new protocols;
- BAG as repository artifact.
