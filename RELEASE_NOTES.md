# Transition Intelligence Protocol — v0.1-draft Release Notes

Status: Published as GitHub Release `v0.1-draft` from validated commit `a66adf7f087f4529a4212816ffedf67f5c41e30f`.

## What this draft establishes

v0.1-draft is the first stable checkpoint for the TIP protocol family.

It establishes three explicit layers:

```text
IFP readiness
-> verified handoff when IFP provenance is used
-> TIP transition reasoning and review
```

The canonical boundaries are:

- IFP establishes readiness; TIP reasons about transitions.
- IFP is optional when the TIP starting state is already trusted and sufficient.
- When IFP supplies the TIP starting state, the explicit handoff contract is required.
- The handoff is an interface contract, not a third protocol.

## Included in v0.1-draft

### TIP record and validator

- state, tension, cause, transition, cooperation, action, and review model;
- strict object validation with `additionalProperties: false` support;
- committed actions require a concrete action summary;
- reviewed records require concrete review notes;
- causal space-time guards for reversibility, impact scope, feedback latency, and review timing;
- low-confidence commitments are restricted to bounded, reversible, fast-feedback experiments;
- committed records cannot hide high cooperation defection risk;
- confidence provenance records assessor, method, rationale, alternatives, calibration evidence when applicable, and human escalation for high-consequence commitments.

### Initialization Feedback Protocol

- explicit readiness lifecycle;
- readiness evidence and feedback requirements;
- separation between initialization readiness and transition reasoning.

### IFP-to-TIP handoff

- explicit source and target record identity checks;
- exact ready-state to TIP-state mapping;
- repository-relative `file:` evidence references;
- rejection of missing, malformed, non-file, absolute, and repository-escaping evidence paths;
- verified file-based bundles must reference the exact IFP source and TIP target files.

### Documentation and contract assurance

- canonical protocol-boundary language across README, TIP spec, IFP spec, and handoff spec;
- documentation consistency tests for local links, canonical CLI commands, handoff references, release artifacts, and protocol boundaries;
- seven bounded implementation-tuning review lenses: Idea Analyst, Project Analyst, Implementation Analyst, Customer Advocate, Repository Reviewer, Stabilizer, and Innovator;
- deterministic validators and tests remain authoritative; tuning agents are review perspectives, not new protocols or autonomous authorities.

## Canonical validation commands

```bash
python -m tip validate examples/json/
python -m tip validate-ifp examples/ifp/
python -m tip validate-handoff \
  examples/handoff/project-to-next-step.handoff.json \
  --ifp examples/ifp/project-initialization.ifp.json \
  --tip examples/json/repository-next-step.tip.json
python -m unittest discover -s tests -v
```

## Validation evidence

GitHub Actions workflow `Validate protocol family` completed successfully on `main` for implementation commit:

`10bb5c77adeecea1a229657c18238d87a3ffc174`

Workflow run:

`30923751747`

That run validated the canonical TIP examples, canonical IFP examples, the canonical IFP-to-TIP handoff, validator self-tests, semantic invariants, and documentation consistency tests present at that commit.

## Current limitations

v0.1-draft deliberately does not claim:

- that `cause.confidence` is a universal calibrated probability;
- that a named human confirmer is cryptographically authenticated;
- that repository file evidence is immutable or signed;
- that remote URLs, database identifiers, or external systems are verified;
- that review proves causality rather than recording observed outcomes;
- recursive directory validation;
- machine-readable CLI output;
- automatic handoff discovery;
- a canonical transition-state library;
- autonomous multi-agent governance.

Signed provenance, scoring, registries, expanded transition libraries, and BAG repository artifacts remain outside the current scope.

## Next direction

The next practical work is CLI quality and real-world calibration:

1. machine-readable CLI output and stable error handling;
2. recursive validation with explicit fixture behavior;
3. real-life IFP -> handoff -> TIP example chains;
4. compare stated confidence with later reviewed outcomes before changing confidence policy.

## Release marker

GitHub Release `v0.1-draft` is published from validated commit `a66adf7f087f4529a4212816ffedf67f5c41e30f`: https://github.com/safal207/transition-intelligence-protocol/releases/tag/v0.1-draft
