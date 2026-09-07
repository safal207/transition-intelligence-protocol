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

## Numeric admission

The shared JSON ingress in `tip/validator.py` (`load_json` / `loads_json`, used
for TIP, IFP and handoff records, JSON file evidence and schema files) rejects
`NaN`, `Infinity`, `-Infinity`, and numeric tokens that overflow to infinity,
such as `1e309` and `-1e309`. These raise `InvalidJSONError` (a `ValueError`).
Record and CLI error handlers report a failed validation rather than allowing
the parse error to be mistaken for an accepted record.

`NaN < 0.5` and `NaN > 1` are both false. Before this admission rule, NaN
confidence could evade both the range bounds and the low-confidence branch.
Infinity is also rejected at ingress, although unlike NaN it is ordered and
would already fail a finite confidence bound.

`validate_schema_subset` rejects non-finite floats supplied directly from
Python too. Finiteness is checked only for floats: Python integers are finite,
and passing an arbitrarily large integer to `math.isfinite` can overflow.

JSON admission still accepts finite values such as `0`, `0.5`, `1` and `1e308`.
Schema and semantic checks remain separate: confidence is still limited to
0 through 1, so `1e308` is not a valid confidence. Quoted strings like `"NaN"`
remain strings, but do not satisfy a numeric confidence field.

`tests/test_numeric_admission.py` checks ingress, in-memory numeric validation
and CLI behavior. `tests/test_numeric_entrypoints.py` additionally exercises
TIP, IFP, handoff, schema-loading and JSON-evidence entry points, including
invalid UTF-8 and clean CLI failures. These tests are discovered by the existing
workflow; no new runtime dependency is introduced.

These checks validate numeric representation, not the accuracy or calibration
of an assessor's confidence and not authorization to execute an action.

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
