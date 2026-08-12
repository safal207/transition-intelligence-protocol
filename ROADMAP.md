# Roadmap

## Current foundation

Goal: make initialization and transition reasoning inspectable and mechanically checkable.

Completed:

- minimal TIP Record specification;
- Initialization Feedback Protocol draft;
- TIP and IFP JSON schemas;
- canonical TIP and IFP examples;
- dependency-free validators;
- command-line validation for files and directories;
- validator self-tests with negative cases;
- documentation consistency tests for local links, canonical commands, handoff references, release artifacts, and protocol boundaries;
- canonical contract language across README, IFP spec, TIP spec, and handoff spec;
- seven bounded implementation-tuning lenses for idea, project, implementation, customer, repository, stabilization, and innovation review;
- GitHub Actions workflow;
- explicit IFP-to-TIP handoff record;
- cross-record handoff validation;
- repository-relative file evidence checks for handoff bundles;
- reviewed TIP records with observed outcomes and next states;
- causal space-time guards for impact scope, feedback latency, reversibility, and review timing;
- confidence provenance with named assessors, alternatives, calibration references, and human escalation for high-consequence commitments;
- successful `Validate protocol family` run `30923751747` on implementation commit `10bb5c77adeecea1a229657c18238d87a3ffc174`;
- `RELEASE_NOTES.md` for the v0.1-draft checkpoint.

## Next milestones

### v0.1-draft release marker

Status: release preparation committed; create the marker after the release-preparation head itself is green on `main`.

Release scope:

- `RELEASE_NOTES.md`;
- `spec/v0.1.md`;
- `protocols/ifp/spec.md`;
- `protocols/ifp/tip-handoff.md`;
- `schemas/tip-record.schema.json`;
- `schemas/ifp-record.schema.json`;
- `schemas/ifp-tip-handoff.schema.json`;
- `examples/json/startup-pivot.tip.json`;
- `examples/json/bounded-learning-pilot.tip.json`;
- `examples/json/pilot-review.tip.json`;
- `examples/ifp/project-initialization.ifp.json`;
- `examples/handoff/project-to-next-step.handoff.json`;
- `tip/validator.py`;
- `tip/ifp_validator.py`;
- `tip/handoff_validator.py`;
- `docs/tuning-agents.md`;
- validator and documentation consistency tests;
- `.github/workflows/validate.yml`.

Marker rule:

```text
release-preparation main commit
-> Validate protocol family = success
-> v0.1-draft tag or GitHub Release
```

### v0.2 CLI quality

Make validation easier for humans, CI, and future agents without changing the protocol boundary.

Planned capabilities:

- machine-readable CLI output;
- stable error codes;
- recursive directory validation;
- package installation entry point;
- automatic handoff record discovery.

### v0.3 Confidence calibration and review learning

Use real reviewed cases to improve operational confidence policies without pretending that one threshold represents universal truth.

Planned work:

- compare stated confidence with later reviewed outcomes;
- document domain-specific calibration limits;
- preserve alternative explanations through review;
- distinguish observed consequence from proven causality;
- keep high-consequence human escalation explicit.

Every new invariant must have a matching negative test.

### v0.4 Transition State Library

Start a small canonical library of transition states only after the existing contracts and validation surface are stable.

The goal is not to define all states at once, but to establish a stable pattern for naming and using transition states.

## Principle

Keep the protocol family small, inspectable, and useful before expanding the theory.
