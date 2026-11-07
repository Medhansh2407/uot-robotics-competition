# UoT Robotics Codex Team Rules

This repository is operated by multiple people, each using Codex. Read this file before every task.

## Start every Codex session

1. Run `tools/agent identity`. If unconfigured, run `tools/agent init <human-first-name> <role>`.
2. Run `tools/board unread` before planning or editing.
3. Claim a GitHub task with `tools/agent claim <issue-number>` before doing the work.
4. Keep one `tools/board wait --timeout 300` running while actively working. Re-run it after it returns.
5. Run `tools/board unread` before commits, after merges, and before ending the session.

Codex does not have Claude-style repository hooks. These commands are the portable coordination mechanism for every teammate's Codex session.

## Human owners

| Folder | GitHub username |
|---|---|
| `medhansh/` | `@Medhansh2407` |
| `zayan/` | `@zayanishtiaq78-prog` |
| `aayush/` | `@aayush2187` |
| `haran/` | `@haranlakshman` |
| `ishanvir/` | `@ishanvir` |
| `shared/` | Team-owned; announce interface changes on the board |

Do not edit another person's folder without a board handoff or explicit permission. A functional role does not override human folder ownership.

## Functional agents

Every Codex session declares one role. Role instructions live in `agents/roles/`.

- `coordinator`
- `mechanical`
- `electrical`
- `embedded-controls`
- `autonomy-perception`
- `integration-test`

One human may run more than one role, but each active Codex session uses one role identity so messages remain attributable.

## Task states

`status:open` → `status:active` → `status:review` → `status:done`

Use `status:blocked` while waiting on another task, decision, measurement, component, or person. Every task must have an owner, role, acceptance criteria, and links to dependencies.

## Board protocol

The pinned GitHub issue is the shared control plane. Messages use:

`[Human's Codex][agent:role][type:event][task:#N][to:@user-or-agent] message`

Valid event types are `online`, `claim`, `update`, `request`, `blocked`, `handoff`, `decision`, `review`, `done`, and `heartbeat`.

- A direct mention or `@all` requires action or a useful response.
- Read unaddressed messages and adjust only when they affect your work.
- Do not post acknowledgement-only noise.
- Interface changes must include the affected contract, units, assumptions, and effective commit or task.
- Hardware actions that could move, energize, heat, cut, or damage anything require a human to perform or approve them.

## Source-control rules

1. Work from fresh `main` on `<issue>-<short-name>`.
2. Make small commits and stage only files belonging to the task.
3. Fetch and rebase before pushing. Never force-push a shared branch.
4. Open a PR with `Closes #N` and acceptance-test evidence.
5. Announce merged interface, pinout, dimension, schema, or dependency changes on the board.

## Shared contracts

Canonical cross-discipline facts live in:

- `shared/INTERFACES.md`
- `shared/DECISIONS.md`
- `shared/TEST_PLAN.md`

Chat and board posts coordinate work; these files preserve final decisions.

