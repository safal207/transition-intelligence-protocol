# Roadmap

## v0.1 Draft

Goal: make one transition inspectable and mechanically checkable.

Completed foundation:

- minimal TIP Record specification;
- canonical JSON schema;
- JSON examples;
- local validator;
- GitHub Actions validation workflow.

## Next milestones

### v0.1-draft release marker

Create a public release/tag once the validation workflow passes on `main`.

Release scope:

- `spec/v0.1.md`
- `schemas/tip-record.schema.json`
- `examples/json/*.tip.json`
- `scripts/validate_examples.py`
- `.github/workflows/validate.yml`

### v0.2 CLI

Add a small command-line interface:

```bash
tip validate examples/json/startup-pivot.tip.json
```

Expected capabilities:

- validate one file;
- validate a directory;
- print readable errors;
- return non-zero exit code on invalid records.

### v0.3 Invariants

Add protocol-level checks beyond JSON shape:

- action must be supported by cause;
- cooperation recommendation must match risk level;
- blocked records should not contain committed actions;
- reviewed records should include outcome notes.

### v0.4 Transition State Library

Start a small canonical library of transition states.

The goal is not to define all states at once, but to establish a stable pattern for naming and using transition states.

## Principle

Keep the protocol small, inspectable, and useful before expanding the theory.
