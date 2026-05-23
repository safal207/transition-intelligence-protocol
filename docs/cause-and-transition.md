# Cause and Transition

A cause is the reason a transition begins or the reason an action is permitted.

In this protocol, cause is not treated as decoration. It is the bridge between state and responsibility.

## Simple definition

```text
Cause = why a state begins to change.
Transition = how the state changes.
Action = what is done inside that change.
```

## Why cause matters

Without cause, a system can record what happened but not why it was justified.

A simple log may say:

```text
Agent sent message.
```

A causal record asks:

```text
Why was the message allowed?
Who requested it?
What intention did it serve?
What previous state made it necessary?
What boundary was checked?
```

## Cause types

| Cause type | Meaning |
| --- | --- |
| Intent cause | A human or system intention created pressure for action. |
| Constraint cause | A limit or boundary forced a transition. |
| Conflict cause | Two values, goals, or actors became misaligned. |
| Opportunity cause | A new opening made transition possible. |
| Risk cause | A threat required stabilization or retreat. |
| Permission cause | A rule, consent, or authority allowed action. |

## Cause chain

Most important transitions do not have one cause. They have a chain.

```text
signal -> interpretation -> tension -> cause -> decision -> action -> consequence
```

The protocol should preserve enough of this chain for later review.

## Practical invariant

```text
No meaningful action should be treated as complete unless its cause can be inspected.
```

## Human version

When a person says, "I reacted because of what happened," Transition Intelligence asks:

- What exactly happened?
- What did it mean to the person?
- What hidden pressure was already present?
- What transition did the reaction create?
- Did the reaction preserve or damage cooperation?

## Agent version

When an AI agent acts, Transition Intelligence asks:

- What state was the agent in?
- What instruction or signal created tension?
- What cause permitted action?
- What transition did the action create?
- Can the cause be reviewed later?
