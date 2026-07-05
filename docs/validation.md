# Validation

The repository includes dependency-free Python validators for TIP and IFP JSON records.

## Validate TIP records

```bash
python -m tip validate examples/json/
```

The compatibility command remains available:

```bash
python scripts/validate_examples.py
```

## Validate IFP records

```bash
python -m tip validate-ifp examples/ifp/
```

## Run validator tests

```bash
python -m unittest discover -s tests -v
```

The test suite checks that:

- valid TIP and IFP records are accepted;
- invalid fixtures are rejected for the expected reason;
- malformed JSON is reported without crashing;
- an empty directory is reported as an error;
- canonical examples remain valid.

## Shared structural checks

The validators currently cover:

- required and nested fields;
- JSON value types;
- enum values;
- numeric bounds;
- malformed JSON;
- file and directory discovery.

## TIP semantic checks

The TIP validator currently rejects:

- a blocked record recommending commitment;
- a record with high cooperation risk recommending direct commitment.

## IFP semantic checks

The IFP validator currently rejects:

- ready status without passed feedback;
- ready status without readiness confirmation;
- readiness without evidence;
- required correction without recorded changes;
- failed feedback combined with a ready result.

Each semantic rule must have a matching negative test before it is added to a validator.

## CI

GitHub Actions runs these commands for pushes and pull requests targeting `main`:

```bash
python -m tip validate examples/json/
python -m tip validate-ifp examples/ifp/
python -m unittest discover -s tests -v
```

## Known limits

The validators implement a focused subset of JSON Schema. They do not yet enforce every schema keyword.

## Future work

- broader JSON Schema support;
- additional semantic rules with matching tests;
- recursive directory validation;
- machine-readable CLI output;
- explicit IFP-to-TIP handoff validation;
- review assurance reports.
