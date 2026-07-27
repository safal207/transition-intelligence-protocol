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

Repository file evidence uses `file:<repository-relative path>`. The validator rejects missing files, directories used as files, invalid JSON evidence, absolute paths, and paths that escape the repository root. A verified file-based bundle must reference the exact IFP source file and TIP target file passed to the command.

The existence of an evidence file is only the first check. The IFP and TIP files are also validated against their own schemas and semantic rules before their identifiers and state mapping are compared with the handoff.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite covers:

- valid TIP, IFP, and handoff examples;
- required fields and nested fields;
- rejection of unknown fields when `additionalProperties` is `false`;
- JSON value types and enum values;
- numeric bounds;
- malformed JSON handling;
- empty directory handling;
- TIP semantic rules;
- IFP readiness rules;
- handoff record ID matching;
- IFP readiness at handoff time;
- explicit `readiness.next_protocol = TIP` at handoff time;
- IFP ready-state and TIP state matching;
- missing handoff evidence files;
- malformed JSON evidence files;
- evidence paths that escape the repository root;
- exact source and target file evidence for verified bundles.

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

Supported subset:

- `type`;
- `enum`;
- `required`;
- `properties`;
- `items`;
- `minimum`;
- `maximum`;
- `additionalProperties: false`.

File evidence validation currently applies to repository-relative `file:` references. Remote URLs, database identifiers, signatures, and content hashes are not yet verified.

## Future work

- broader JSON Schema support;
- recursive directory validation;
- machine-readable CLI output;
- automatic handoff discovery;
- content hashes for immutable evidence;
- review assurance reports.
