---
name: competition-code-delivery
description: Implement or review competition software with small scoped changes, test-first evidence, repository commit standards, and board handoffs. Use for coding, debugging, refactoring, tests, commits, and pull requests in this repository.
---

# Competition code delivery

Before editing, state the task interpretation, risky assumptions, observable success condition, and narrowest useful verification.

- Implement the smallest slice that meets the claimed issue.
- Match the current toolchain and style; do not add frameworks or dependencies without a concrete need.
- Keep hardware-independent logic separate from device access so it can run on a host computer.
- For bugs, reproduce the failing behavior before changing implementation.
- Test at the cheapest layer that can observe the behavior, then move upward only as needed: host unit → integration → simulation → bench → hardware-in-loop → field.
- Do not mock the unit under test or weaken correct assertions to obtain a pass.
- Touch only task-related files and clean up only artifacts introduced by the change.

Before committing, follow `docs/COMMIT_STANDARDS.md`, run relevant checks, and post evidence or remaining risk through `tools/agent`.
