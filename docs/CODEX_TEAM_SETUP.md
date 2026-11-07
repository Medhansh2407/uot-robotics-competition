# Codex Team Setup

Each teammate clones the repository, authenticates GitHub CLI, and initializes their local Codex identity:

```bash
gh auth login
tools/board whoami
tools/agent init <first-name> <role>
tools/board unread
```

Example:

```bash
tools/agent init Medhansh coordinator
```

The identity is stored locally in `.agent/identity` and is never committed. Different users and separate clones can run different roles simultaneously.

## Starting Codex

Open the repository in Codex and use this first prompt:

> Read AGENTS.md and your role file. Run tools/agent identity and tools/board unread. Claim only one ready task, coordinate dependencies on the board, implement it, verify it, and post a handoff or completion update.

Codex automatically reads repository `AGENTS.md` instructions. There are intentionally no Claude hooks or Claude-specific files.

## Daily operating loop

1. Coordinator creates task issues with `tools/agent task`.
2. A role agent claims a ready task with `tools/agent claim`.
3. Agents communicate blockers and handoffs through `tools/agent block` and `tools/agent handoff`.
4. Canonical interfaces and decisions are updated in `shared/`.
5. Integration verifies acceptance criteria and marks the task done.

The board is communication infrastructure, not an autonomous agent host. A Codex session must be open and working for that agent to act. `tools/board wait` supplies cross-user events while a session is active.

