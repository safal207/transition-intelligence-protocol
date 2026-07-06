# IFP-to-TIP Handoff

## Purpose

The handoff connects a verified Initialization Feedback Protocol record to a Transition Intelligence Protocol record.

It preserves a strict boundary:

- IFP proves that a starting state is ready;
- TIP reasons about the next transition from that state.

```text
IFP Ready State
-> verified handoff
-> TIP State
-> Tension
-> Cause
-> Transition
-> Cooperation
-> Action
```

## TIP initialization metadata

A TIP record may include an optional `initialization` object:

```json
{
  "initialization": {
    "source_protocol": "IFP",
    "source_record_id": "ifp.example.project_initialization",
    "ready_state": "Repository has a specification, examples, validation, and automated feedback",
    "evidence": [
      "schemas/tip-record.schema.json",
      "tests/test_validator.py"
    ]
  }
}
```

TIP records that do not originate from IFP may omit this object.

## Cross-record invariants

The handoff is valid only when:

1. both records are individually valid;
2. the IFP record has `status = ready`;
3. IFP feedback passed;
4. IFP readiness is confirmed;
5. IFP declares `next_protocol = TIP`;
6. TIP declares `source_protocol = IFP`;
7. TIP `source_record_id` matches the IFP record id;
8. TIP `ready_state` matches the IFP target state;
9. TIP handoff evidence is a non-empty subset of IFP readiness evidence.

## CLI

```bash
python -m tip validate-handoff \
  examples/json/protocol-family-next-step.tip.json \
  examples/ifp/project-initialization.ifp.json
```

Exit code `0` means the handoff is valid. Exit code `1` means record validation or cross-record provenance failed.

## Why separate validation matters

Two records may both be structurally valid while their relationship is false.

Examples:

- TIP references a different IFP record id;
- IFP is configured but not ready;
- TIP copies evidence that is absent from the source record;
- IFP targets another protocol;
- TIP describes a different ready state than the one IFP established.

The handoff validator detects these relationship failures.

## Scope

The current handoff is file-based and local. It does not yet resolve records from registries, URLs, databases, or signed provenance stores.
