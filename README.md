# UoT Robotics Competition

Codex-native multi-user agent workspace for the University of Toronto robotics competition.

## How the team works

- A pinned GitHub issue is the cross-user communication board.
- Every Codex session declares a human and functional role.
- GitHub task issues provide claimable work, status, dependencies, and acceptance criteria.
- Human-owned folders isolate individual work.
- `shared/` preserves canonical mechanical, electrical, controls, autonomy, and testing contracts.

Start with [AGENTS.md](AGENTS.md) and [the Codex team setup](docs/CODEX_TEAM_SETUP.md).

The shared operating standards are [the competition cadence](docs/COMPETITION_CADENCE.md), [commit standards](docs/COMMIT_STANDARDS.md), and the project-scoped skills under `.agents/skills/`.

```bash
gh auth login
tools/board whoami
tools/agent init <first-name> <role>
tools/board unread
```

Available roles:

- `coordinator`
- `mechanical`
- `electrical`
- `embedded-controls`
- `autonomy-perception`
- `integration-test`

The live board is [issue #1](https://github.com/Medhansh2407/uot-robotics-competition/issues/1).

## AdaptiveServe demand forecasting

The PyTorch prototype forecasts P10, P50, and P90 next-day demand for each planned menu item. See [the architecture](docs/MODEL_ARCHITECTURE.md) and [the data-collection protocol](docs/DATA_COLLECTION.md).

```bash
python3 -m unittest discover -s tests -v
python3 -m adaptive_serve.train --epochs 60 --output artifacts/demand_model.pt
```
