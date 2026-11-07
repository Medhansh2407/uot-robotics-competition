---
name: robot-embedded-controls
description: Build and verify robot firmware, device drivers, motor control, control loops, state machines, telemetry, and safe actuator behavior. Use for microcontrollers, motor drivers, sensors, encoders, communications, and embedded debugging.
---

# Robot embedded controls

Confirm the board, framework, programmer, pinout, voltage levels, actuators, sensors, and stop behavior before implementation.

- Separate hardware-independent state/control logic from peripheral access.
- Use explicit units, ranges, timeouts, saturation, startup state, and fault behavior.
- Keep interrupt handlers bounded and non-blocking; move work to the main loop or task context.
- Default outputs to safe/off until initialization and validation complete.
- Test pure logic on the host when possible, then compile, bench-test unloaded hardware, and only then test the mechanism.
- Log commands, sensor readings, state transitions, faults, and loop timing needed for diagnosis.
- Publish firmware-to-electrical pin and protocol contracts in `shared/INTERFACES.md`.

Compilation is not proof of safe behavior. Stop for human confirmation before flashing, powering, or moving hardware.
