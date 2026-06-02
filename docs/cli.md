# CLI

TIP includes a small Python command-line interface.

## Validate a directory

```bash
python -m tip validate examples/json/
```

## Validate one file

```bash
python -m tip validate examples/json/startup-pivot.tip.json
```

## Custom schema

```bash
python -m tip validate examples/json/ --schema schemas/tip-record.schema.json
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | All checked records are valid. |
| 1 | At least one record is invalid, missing, or no records were found. |

## Current scope

The CLI currently validates:

- required fields;
- nested required fields;
- enum values;
- one file or one directory of `.tip.json` records.

It does not yet perform full JSON Schema validation or TIP semantic invariants.

## Roadmap

Future CLI versions should add:

- recursive directory validation;
- full schema validation;
- semantic invariant checks;
- machine-readable output;
- better error locations;
- package installation entry point.
