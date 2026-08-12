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

Status: Done

Completed:

- committed TIP records require a non-empty concrete action summary;
- negative test proves a whitespace-only committed action is rejected;
- TIP specification documents the commitment rule;
- reviewed TIP records require non-empty review notes;
- the schema supports a bounded `review` object with summary, actual consequence, evidence, and next state;
- positive and negative tests cover reviewed records;
- a canonical reviewed pilot example closes the action-to-review loop;
- handoff file evidence uses explicit repository-relative `file:` references;
- missing files, malformed JSON, directories, absolute paths, and repository-root escapes are rejected;
- verified file-based bundles must reference the exact IFP source and TIP target files;
- evidence validation has positive and negative tests and is documented;
- the first confidence guard blocked low-confidence, low-reversibility commitments while allowing reversible pilots;
- a causal space-time transition audit found that reversibility alone did not constrain impact scope or feedback delay;
- the transition schema now supports `impact_scope` and `feedback_latency`;
- all committed records must explicitly declare impact scope and feedback latency so consequence checks cannot be bypassed by omission;
- low-confidence commitments require high reversibility, local or bounded impact, immediate or short feedback, and a concrete review point;
- committed records cannot hide high cooperation defection risk;
- separate negative tests identify failures in reversibility, spatial reach, feedback latency, review planning, and cooperation stability;
- `bounded-learning-pilot.tip.json` demonstrates a valid evidence-producing commitment under low confidence;
- the specification states that `0.5` is an operational guardrail, not a truth threshold;
- committed records require a `confidence_assessment` provenance object;
- confidence provenance records the assessor, assessor type, method, rationale, alternative explanations, and human confirmation state;
- statistical and calibrated-model assessments require a calibration reference;
- high-consequence commitments require explicit human confirmation;
- a true human-confirmation flag requires a named `human_confirmer` so responsibility is inspectable;
- bounded reversible pilots may use AI assessment without pretending that the estimate is human-confirmed;
- negative tests cover missing provenance, missing alternatives, missing calibration evidence, anonymous confirmation, missing consequence coordinates, and missing human confirmation;
- positive tests cover human-confirmed high-consequence action and bounded AI-assessed experimentation;
- GitHub Actions run `30923751747` completed successfully on `main` for implementation commit `10bb5c77adeecea1a229657c18238d87a3ffc174`.

Definition of Done:

- every new invariant has a negative test;
- each error message names the failing protocol path;
- the completed invariant set passes the repository validation workflow.

## Epic 2 — Documentation and schema consistency

Goal: prevent README, specs, schemas, examples, validators, and CI from drifting apart.

### 2.1 Add documentation consistency tests

Status: Done

Completed:

- added `tests/test_documentation.py`;
- repository-local Markdown links must resolve to existing paths inside the repository root;
- canonical TIP, IFP, handoff, and unittest commands must match across README, CLI docs, validation docs, and the GitHub Actions workflow;
- handoff surfaces must reference `examples/handoff/project-to-next-step.handoff.json`;
- release-scope artifacts must exist and remain explicitly listed in `ROADMAP.md`;
- README structure entries are checked for canonical validators, tests, examples, and tuning guidance;
- canonical protocol-boundary language is checked across README, IFP spec, TIP spec, and handoff spec;
- the seven tuning agents and their authority limits are checked in `docs/tuning-agents.md`;
- deliberate broken-link and stale-command mutations were rejected before the clean suite passed again;
- GitHub Actions run `30923751747` completed successfully with the documentation consistency module included.

Definition of Done:

- broken links or stale canonical commands fail tests;
- docs consistency tests run successfully in CI.

### 2.2 Consolidate protocol contract language

Status: Done

Completed:

- IFP is explicitly limited to readiness;
- TIP is explicitly limited to transition, cooperation, action, and review reasoning;
- IFP is optional when a TIP starting state is already trusted and sufficient;
- an explicit handoff is required when IFP supplies the TIP starting state;
- the handoff is consistently defined as an interface contract rather than a third protocol;
- standalone TIP records are prohibited from claiming IFP provenance without a valid handoff;
- duplicate handoff record guidance was removed from the IFP specification in favor of the canonical handoff contract;
- README, IFP spec, TIP spec, and handoff spec use the same four canonical boundary statements;
- `docs/tuning-agents.md` defines Idea, Project, Implementation, Customer, Repository, Stabilizer, and Innovator review lenses without creating new protocol authority;
- documentation tests fail when a canonical boundary or tuning-agent limit drifts;
- GitHub Actions run `30923751747` completed successfully for the consolidated contract language.

Definition of Done:

- README, IFP spec, TIP spec, and handoff spec use the same boundaries;
- those boundaries are protected by repository assertions and passing CI.

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

Status: Done

Completed:

- added `RELEASE_NOTES.md`;
- documented v0.1-draft scope and canonical protocol boundaries;
- recorded the successful implementation validation run and commit;
- listed current limitations without claiming signed provenance, universal confidence calibration, or external evidence verification;
- recorded the next practical CLI and calibration work.

Definition of Done:

- release notes match README, roadmap, schemas, examples, and validated implementation scope.

### 5.2 Create v0.1-draft marker

Status: Ready — marker creation pending

Completed:

- implementation head `10bb5c77adeecea1a229657c18238d87a3ffc174` passed workflow run `30923751747`;
- release-preparation head `f298ba3a71ad8a4437507162b7fd7ab143d04107` passed workflow run `31584460771`;
- release notes and README now describe the v0.1-draft checkpoint and marker rule.

Remaining task:

- create tag or GitHub Release `v0.1-draft` pointing to a green release-preparation commit.

Definition of Done:

- the marker points to a green `main` commit;
- release notes and marker identify the same v0.1-draft scope.

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
