---
name: robot-integration-test
description: Plan and execute robot verification from unit tests through simulation, bench, hardware-in-loop, field rehearsal, and readiness review. Use for test planning, interface verification, regression, failure triage, and go/no-go decisions.
---

# Robot integration and test

Maintain `shared/TEST_PLAN.md` as the evidence ledger.

- Map every test to requirement IDs, interfaces, prerequisites, observable pass criteria, owner, and evidence.
- Progress through host unit, integration, simulation, bench, hardware-in-loop, and field levels without skipping a cheaper level that can catch the failure.
- Test safe startup, stop, timeout, sensor loss, communication loss, saturation, brownout recovery, and operator recovery.
- Preserve failing evidence and identify the earliest layer where the defect appears.
- Re-run affected regression tests after every interface, calibration, wiring, or mechanical change.
- Report readiness as `GO`, `GO WITH LIMITS`, or `NO-GO` with evidence and unresolved risks.

Do not mark a task done because code compiles, a CAD file opens, or one successful run occurred.
