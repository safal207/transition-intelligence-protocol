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
- confidence provenance and high-consequence human escalation;
- IFP readiness rules;
- handoff record ID matching;
- IFP readiness at handoff time;
- explicit `readiness.next_protocol = TIP` at handoff time;
- IFP ready-state and TIP state matching;
- missing handoff evidence files;
- malformed JSON evidence files;
- evidence paths that escape the repository root;
- exact source and target file evidence for verified bundles;
- repository-local Markdown links;
- canonical CLI command consistency across README, CLI docs, validation docs, and workflow;
- canonical handoff references;
- release-scope artifact existence and README structure entries;
- canonical IFP, TIP, and handoff boundary language across all contract surfaces;
- completeness and bounded authority of the seven implementation tuning agents.

`tests/test_documentation.py` keeps human-facing documentation aligned with executable repository behavior. A stale command, broken local link, missing release artifact, outdated canonical path, missing protocol boundary, or drifted tuning-agent definition fails the normal test command and therefore the existing CI workflow.

The tuning agents are documented in [`tuning-agents.md`](tuning-agents.md). They are review lenses rather than new protocols or autonomous authorities.

Each semantic rule must have a matching negative test. Each documentation contract must have a repository assertion that fails when the contract drifts.

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

Documentation tests validate repository-local paths, canonical command text, contract language, and tuning-agent boundaries. They do not make external websites available, prove that external links remain healthy, or execute autonomous agent reasoning.

## Future work

- broader JSON Schema support;
- recursive directory validation;
- machine-readable CLI output;
- automatic handoff discovery;
- content hashes for immutable evidence;
- review assurance reports.
