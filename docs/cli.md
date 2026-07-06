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

## Validate an IFP-to-TIP handoff

The handoff validator checks one interface record together with the referenced IFP and TIP records:

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

Optional schema overrides:

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json \
  --handoff-schema schemas/ifp-tip-handoff.schema.json \
  --ifp-schema schemas/ifp-record.schema.json \
  --tip-schema schemas/tip-record.schema.json
```

The command verifies:

- all three records are structurally and semantically valid;
- the source and target record IDs match;
- the IFP source is ready;
- the handoff ready state matches the IFP target state;
- the handoff target state matches the TIP state summary;
- a verified handoff contains verification evidence.

## Run validator self-tests

```bash
python -m unittest discover -s tests -v
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | All checked records and relationships are valid. |
| 1 | At least one record or relationship is invalid, missing, or empty. |

## Current scope

The CLI currently validates:

- required and nested fields;
- supported JSON value types;
- enum values;
- numeric bounds;
- malformed JSON handling;
- one file or one matching directory;
- selected TIP and IFP semantic invariants;
- explicit cross-record IFP-to-TIP handoffs.

Directory discovery is currently non-recursive:

- TIP: `*.tip.json`
- IFP: `*.ifp.json`

## Roadmap

Future CLI versions should add:

- recursive directory validation;
- broader JSON Schema support;
- machine-readable output;
- better error locations;
- package installation entry point;
- automatic handoff record discovery.
