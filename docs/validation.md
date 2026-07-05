# Validation

TIP v0.1 includes a dependency-free Python validator for TIP JSON records.

## Validate records

```bash
python -m tip validate examples/json/
```

The compatibility command remains available:

```bash
python scripts/validate_examples.py
```

## Run validator tests

```bash
python -m unittest discover -s tests -v
```

The test suite checks that:

- valid records are accepted;
- invalid fixtures are rejected for the expected reason;
- malformed JSON is reported without crashing;
- an empty directory is reported as an error;
- canonical examples remain valid.

## Current checks

The validator currently covers:

- required and nested fields;
- JSON value types;
- enum values;
- numeric bounds;
- malformed JSON;
- file and directory discovery;
- selected TIP semantic rules.

The semantic rules currently prevent:

- a blocked record from recommending commitment;
- a record with high cooperation risk from recommending direct commitment.

Each semantic rule must have a negative test before it is added to the validator.

## CI

GitHub Actions runs these commands for pushes and pull requests targeting `main`:

```bash
python -m tip validate examples/json/
python -m unittest discover -s tests -v
```

## Known limits

The validator implements a focused subset of JSON Schema. It does not yet enforce every schema keyword.

## Future work

- broader JSON Schema support;
- additional semantic rules with matching tests;
- recursive directory validation;
- machine-readable CLI output;
- review assurance reports.
