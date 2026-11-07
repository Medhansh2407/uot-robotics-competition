---
name: robot-autonomy-perception
description: Build or review robot perception, calibration, localization, coordinate frames, planning, autonomous state machines, and high-level behavior. Use for cameras, vision, sensor fusion, trajectory logic, and mission execution.
---

# Robot autonomy and perception

Define the observable mission behavior and failure behavior before choosing algorithms.

- Specify coordinate frames, units, timestamps, update rates, latency budget, confidence, and stale-data behavior.
- Make calibration artifacts reproducible and versioned.
- Separate recorded-data processing from live device I/O so tests can replay deterministic inputs.
- Establish a simple baseline before adding learned or complex methods.
- Test nominal, boundary, occlusion, noise, dropped-data, and recovery cases.
- Bound motion commands and require the controls layer to enforce final safety limits.
- Record message and frame contracts in `shared/INTERFACES.md`.

Simulation or replay success is necessary but not sufficient; integration must verify the real sensor placement and environment.
