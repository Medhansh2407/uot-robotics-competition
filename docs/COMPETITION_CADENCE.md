# Competition operating cadence

This cadence is provisional until organizers publish the event schedule. It scales by percentage of remaining time.

## Phase 1 — Intake and architecture (first 10%)

- Ingest official rules into `shared/REQUIREMENTS.md`.
- Inventory hardware, software, tools, fabrication capacity, and team availability.
- Choose the simplest scoring strategy and one fallback.
- Freeze initial mechanical, electrical, software, and coordinate-frame contracts.
- Create claimable issues with dependencies and acceptance criteria.

## Phase 2 — Parallel subsystem proof (next 40%)

- Work in 30-minute cycles: claim → contract → build → verify → post.
- One active task per agent.
- End every cycle with a board update, handoff, blocker, or evidence link.
- Integrate at least every second cycle; do not let branches diverge for hours.

## Phase 3 — Integrated mission proof (next 30%)

- Stop optimizing isolated subsystems.
- Run complete mission attempts and record failure categories.
- Fix the earliest or highest-impact failure, then rerun regression tests.
- Maintain one known-good configuration and calibration set.

## Phase 4 — Freeze and rehearse (final 20%)

- No new features unless the coordinator declares the current design non-viable.
- Allow only verified fixes, calibration, robustness, documentation, and spare preparation.
- Run repeated competition-format rehearsals with reset and recovery procedures.
- Produce final `GO`, `GO WITH LIMITS`, or `NO-GO` evidence.

## Every 30-minute cycle

1. Read the board and confirm the claimed task is still relevant.
2. Restate inputs, outputs, units, dependencies, and pass criteria.
3. Implement or design the smallest demonstrable slice.
4. Verify at the cheapest valid layer.
5. Commit using `docs/COMMIT_STANDARDS.md`.
6. Post evidence, blocker, decision, or handoff.

Immediately interrupt normal work for a safety hazard, rule change, interface break, damaged component, unavailable critical tool, or failure of the known-good configuration. Post the event to the board and let the coordinator replan.
