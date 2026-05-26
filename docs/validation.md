# Validation

TIP v0.1 includes a small Python validator for JSON examples.

## Run

```bash
python scripts/validate_examples.py
```

Expected output:

```text
OK   examples/json/family-conflict.tip.json
OK   examples/json/human-ai-agent.tip.json
OK   examples/json/startup-pivot.tip.json
```

## Scope

The current validator is intentionally minimal. It checks:

- required fields;
- nested required fields;
- enum values;
- example file discovery.

It does not yet implement full JSON Schema validation.

## Future work

Later versions may add:

- dependency-free full schema validation;
- CI workflow;
- negative examples;
- richer protocol invariants;
- CLI output formats.
