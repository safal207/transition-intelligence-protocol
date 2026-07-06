# IFP to TIP Handoff — Draft v0.1

## Purpose

The handoff connects one verified Initialization Feedback Protocol record to one Transition Intelligence Protocol record.

It is an interface contract, not a third protocol.

```text
IFP Record
  status = ready
  readiness.ready = true
  readiness.next_protocol = TIP
        ↓
IFP-to-TIP Handoff
        ↓
TIP Record
  state = verified IFP ready state
```

## Why the handoff is explicit

Without an explicit handoff, a TIP record may claim a starting state without showing where that state came from.

The handoff preserves:

- the source IFP record identifier;
- the target TIP record identifier;
- the ready state produced by IFP;
- the state consumed by TIP;
- evidence used to verify the mapping.

## Required checks

A verified handoff requires:

1. the referenced IFP record is valid;
2. the IFP record has `status = ready`;
3. the IFP record has `readiness.ready = true`;
4. the IFP record has `readiness.next_protocol = TIP`;
5. the referenced TIP record is valid;
6. handoff record identifiers match the referenced records;
7. the handoff ready state matches the IFP target state;
8. the handoff target state matches the TIP state summary;
9. verification evidence is present.

## Command

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

A handoff is valid only when the three records are valid together.
