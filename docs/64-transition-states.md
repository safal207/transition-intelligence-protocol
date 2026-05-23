# 64 Transition States

The 64 transition states are a design metaphor inspired by the 64 hexagrams of the I Ching.

This project does not use the I Ching as prediction or mysticism. It uses the structure as a historical example of mapping situations as combinations of simpler forces.

## Why sixty-four

The classical structure comes from six binary positions. Each position has two possible forms. Together, this creates sixty-four possible combinations.

In protocol terms, each position can represent a domain-specific polarity such as:

- active or receptive;
- visible or hidden;
- stable or unstable;
- cooperative or adversarial;
- committed or reversible;
- clear or ambiguous.

## Protocol interpretation

A transition state is a structured description of a situation before action.

Each state should capture:

- current configuration;
- dominant tension;
- hidden or visible cause;
- possible transition direction;
- cooperation risk;
- recommended action posture.

## Action postures

| Posture | Meaning |
| --- | --- |
| Wait | Do not force the transition yet. |
| Clarify | Gather more signal before acting. |
| Stabilize | Reduce volatility before change. |
| Negotiate | Cooperation is the main constraint. |
| Commit | Preconditions are strong enough for action. |
| Retreat | The transition would create avoidable damage. |

## Minimal transition-state shape

```json
{
  "state_id": "transition.state.example",
  "name": "Example State",
  "summary": "A short description of the situation.",
  "tension": "The pressure that may cause change.",
  "cause": "Why the transition exists or why action may be permitted.",
  "transition_direction": "Where the state appears to be moving.",
  "cooperation_risk": "low | medium | high",
  "recommended_posture": "wait | clarify | stabilize | negotiate | commit | retreat"
}
```

## Future work

Later versions may define a canonical set of 64 transition states. For now, this document establishes the design frame only.
