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
- GitHub Actions workflow;
- explicit IFP-to-TIP handoff record;
- cross-record handoff validation;
- negative handoff tests for ID, readiness, state, and evidence errors.

## Next milestones

### v0.1-draft release marker

Create a public release or tag after the validation workflow is visibly successful on `main`.

Release scope:

- `spec/v0.1.md`
- `protocols/ifp/spec.md`
- `protocols/ifp/tip-handoff.md`
- `schemas/*.json`
- canonical examples;
- CLI validators;
- validator self-tests;
- `.github/workflows/validate.yml`

### v0.2 CLI packaging

Turn the current module commands into an installable command:

```bash
tip validate examples/json/
tip validate-ifp examples/ifp/
tip validate-handoff examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

Planned capabilities:

- package installation entry point;
- recursive directory validation;
- machine-readable output;
- stable error codes;
- automatic handoff record discovery.

### v0.3 Semantic invariants

Add protocol-level checks beyond JSON shape and current readiness rules:

- action support from cause and evidence;
- cooperation recommendation alignment with risk;
- reviewed records with outcome notes;
- evidence freshness and provenance;
- handoff evidence consistency.

Every new invariant must have a matching negative test.

### v0.4 Transition State Library

Start a small canonical library of transition states.

The goal is not to define all states at once, but to establish a stable pattern for naming and using transition states.

## Principle

Keep the protocol family small, inspectable, and useful before expanding the theory.
