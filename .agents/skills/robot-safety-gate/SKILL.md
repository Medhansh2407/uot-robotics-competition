---
name: robot-safety-gate
description: Review and gate actions that can energize, move, heat, cut, flash, fabricate, or damage competition hardware. Use before physical bring-up, firmware flashing, actuator tests, battery connection, fabrication, and hazardous debugging.
---

# Robot safety gate

Agents prepare procedures and evidence; humans authorize and perform physical actions.

Before a hazardous step, state:

- exact hardware and revision
- energy source and limits
- expected behavior
- hazards and exclusion zone
- emergency stop or disconnect
- test duration and abort thresholds
- required PPE, restraints, current limiting, or unloaded configuration
- named human confirmation required

Pause until a human explicitly confirms the specific step. Authorization for one step does not authorize later voltage changes, loaded motion, different firmware, rewiring, or fabrication operations.

When uncertain, default to de-energized inspection, simulation, host tests, continuity checks, or current-limited unloaded testing.
