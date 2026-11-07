---
name: robot-electrical-design
description: Design or review robot power, wiring, sensors, actuators, connectors, grounding, protection, pinouts, and electrical BOMs. Use for component selection, wiring plans, power budgets, and electrical bring-up.
---

# Robot electrical design

Use manufacturer datasheets and measured hardware identities. Do not infer voltage, polarity, current, or logic level from appearance.

- Build a power budget with nominal, peak, and stall current plus regulator and battery limits.
- Record supply voltage, logic level, connector, pin, polarity, fuse/protection, wire gauge, and common-ground assumptions.
- Keep high-current paths, logic power, and signal routing explicit.
- Define safe power-up, current-limited smoke test, emergency isolation, and power-down procedures.
- Publish the canonical pinout and wiring revision in `shared/INTERFACES.md`.
- Hand firmware agents machine-readable names and units for every signal.

Stop for human confirmation before energizing, probing, soldering, rewiring, or connecting a battery.
