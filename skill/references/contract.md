# Contract

## Purpose
Agent stacks overspend by routing every step to a frontier model without measuring task complexity.

## Input
JSON task profile with complexity, risk, latency target, privacy class and token budget.

## Output
Recommended model tier, context strategy, maximum iterations and escalation conditions.

## Failure behavior
Reject malformed JSON. Report missing or unsafe fields explicitly. Never invent evidence or authorization.
