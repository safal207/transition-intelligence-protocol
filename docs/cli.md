# CLI

The repository includes a small Python command-line interface for the protocol family.

## Validate TIP records

Directory:

```bash
python -m tip validate examples/json/
```

Single file:

```bash
python -m tip validate examples/json/startup-pivot.tip.json
```

Custom schema:

```bash
python -m tip validate examples/json/ --schema schemas/tip-record.schema.json
```

## Validate IFP records

Directory:

```bash
python -m tip validate-ifp examples/ifp/
```

Single file:

```bash
python -m tip validate-ifp examples/ifp/project-initialization.ifp.json
```

Custom schema:

```bash
python -m tip validate-ifp examples/ifp/ --schema schemas/ifp-record.schema.json
```

## Run validator self-tests

```bash
python -m unittest discover -s tests -v
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | All checked records are valid. |
| 1 | At least one record is invalid, missing, or no records were found. |

## Current scope

The CLI currently validates:

- required and nested fields;
- supported JSON value types;
- enum values;
- numeric bounds;
- malformed JSON handling;
- one file or one matching directory;
- selected TIP and IFP semantic invariants.

Directory discovery is currently non-recursive:

- TIP: `*.tip.json`
- IFP: `*.ifp.json`

## Current IFP readiness rules

The IFP validator rejects:

- `status = ready` when feedback did not pass;
- `status = ready` without readiness confirmation;
- readiness without evidence;
- required correction without recorded changes;
- failed feedback combined with a ready result.

## Roadmap

Future CLI versions should add:

- recursive directory validation;
- broader JSON Schema support;
- machine-readable output;
- better error locations;
- package installation entry point;
- explicit IFP-to-TIP handoff validation.
