# Validation

The repository includes validators for TIP records, IFP records, and IFP-to-TIP handoffs.

## TIP

```bash
python -m tip validate examples/json/
```

Compatibility command:

```bash
python scripts/validate_examples.py
```

## IFP

```bash
python -m tip validate-ifp examples/ifp/
```

## Handoff

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

The handoff command checks the interface record together with the referenced IFP and TIP records.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite covers:

- valid TIP, IFP, and handoff examples;
- required fields and nested fields;
- JSON value types and enum values;
- numeric bounds;
- malformed JSON handling;
- empty directory handling;
- TIP semantic rules;
- IFP readiness rules;
- handoff record ID matching;
- IFP readiness at handoff time;
- IFP ready-state and TIP state matching;
- handoff verification evidence.

Each semantic rule must have a matching negative test.

## CI

GitHub Actions runs:

```bash
python -m tip validate examples/json/
python -m tip validate-ifp examples/ifp/
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
python -m unittest discover -s tests -v
```

## Known limits

The validators implement a focused subset of JSON Schema.

## Future work

- broader JSON Schema support;
- recursive directory validation;
- machine-readable CLI output;
- automatic handoff discovery;
- review assurance reports.
