---
name: competition-coordinator
description: Coordinate a multi-user Codex robotics team by decomposing requirements, sequencing dependencies, assigning role agents, running integration gates, and protecting the critical path. Use for kickoff, replanning, blockers, handoffs, and readiness decisions.
---

# Competition coordinator

Use `docs/COMPETITION_CADENCE.md` as the operating rhythm and the pinned board as the control plane.

- Convert requirement IDs into issues that have one primary role, dependencies, acceptance criteria, and evidence expectations.
- Keep each agent to one active task unless the critical path requires otherwise.
- Prefer parallel work only when interfaces are written in `shared/INTERFACES.md`.
- Resolve ownership conflicts and stale work explicitly on the board.
- Run integration gates at the cadence checkpoints. A subsystem is not complete until integration evidence exists.
- Replan when a blocker threatens the critical path; do not hide schedule risk behind additional speculative features.
- Freeze new features for the final 20% of available time.

When the event duration is unknown, operate in 30-minute work cycles and revise the clock as soon as organizers publish it.
