# IFP to TIP Handoff — Draft v0.1

## Purpose

The handoff connects one verified Initialization Feedback Protocol record to one Transition Intelligence Protocol record.

## Canonical boundaries

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

The handoff applies when a TIP record uses a starting state produced by IFP. A standalone TIP record with an independently trusted and sufficient state does not require an artificial handoff.

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

When IFP supplies the source state, the handoff shows that the exact checked ready state became the exact state used for TIP transition reasoning.

The handoff preserves:

- the source IFP record identifier;
- the target TIP record identifier;
- the ready state produced by IFP;
- the state consumed by TIP;
- evidence used to verify the mapping.

The handoff establishes starting-state provenance. It does not decide the transition, recommend an action, or replace TIP validation.

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
9. verification evidence is present;
10. repository file evidence exists, stays inside the repository root, and is readable;
11. JSON evidence files contain valid JSON;
12. a verified file-based bundle references the exact IFP source file and TIP target file.

## File evidence

Repository files use an explicit evidence prefix:

```text
file:examples/ifp/project-initialization.ifp.json
```

The part after `file:` is resolved relative to the repository root. Absolute paths and paths that escape the repository root are rejected.

A file reference proves only that the named artifact exists and can be read. The bundle validator separately checks the IFP source against the IFP schema and semantic rules, checks the TIP target against the TIP schema and semantic rules, and then compares their identifiers and states with the handoff.

Plain strings remain available for non-file evidence, but they do not replace the required source and target file references in a verified file-based bundle.

## Command

```bash
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
```

A handoff is valid only when the three records and their evidence are valid together.
