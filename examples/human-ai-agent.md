# Example: Human-AI Agent

## Situation

A human asks an AI agent to send a message, change a file, or make a decision.

## State

The agent has an instruction, partial context, and possible tool access.

## Tension

The user wants progress, but the agent may not have enough context to act safely.

## Cause

The user request creates intent, but intent alone is not enough. The agent needs a clear basis for the action.

## Transition

Move from request interpretation to verified action readiness.

## Cooperation check

Participants:

- human: wants useful execution;
- agent: must avoid overclaiming or acting on weak context;
- external parties: may be affected by the action;
- future reviewer: needs a reason trail.

Cooperation is stable when the agent makes limits visible and preserves why action was taken.

## Action

Clarify missing context when needed, or perform the smallest safe action that is clearly justified.

## Review question

Can a future reviewer understand why the agent acted and whether the action respected the human's actual intent?
