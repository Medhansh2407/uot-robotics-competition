---
name: competition-intake
description: Extract a robotics competition brief, rubric, field specification, schedule, or organizer update into traceable requirements and unresolved questions. Use when rules arrive or change; do not use to invent missing rules.
---

# Competition intake

Read every supplied source before proposing a design. Separate exact requirements from interpretation.

1. Record each rule in `shared/REQUIREMENTS.md` with a stable ID, source location, requirement, verification method, and affected roles.
2. Extract scoring opportunities, hard constraints, prohibited actions, dimensions, timing, inspection rules, submission requirements, available parts, and ambiguity.
3. Normalize units while preserving the source value. Flag contradictions instead of silently choosing one.
4. Post blocking questions to the board and mark the affected requirement `Unconfirmed`.
5. Ask the coordinator to create issues only after each task can cite requirement IDs and measurable acceptance criteria.

Do not treat a summary, memory, teammate paraphrase, or agent inference as an official rule. When rules change, update the same requirement IDs, record the revision, and announce downstream impact.
