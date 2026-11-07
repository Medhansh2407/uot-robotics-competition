# Competition commit standards

These standards optimize rapid parallel work, traceability, and safe rollback.

## Format

Use `<type>(<area>): <imperative outcome>`.

Types are `feat`, `fix`, `test`, `docs`, `refactor`, and `chore`. Areas normally match roles or subsystems: `mechanical`, `electrical`, `controls`, `firmware`, `perception`, `autonomy`, `integration`, or `board`.

Examples:

```text
feat(controls): add encoder timeout stop
fix(electrical): correct left motor polarity contract
test(perception): replay low-light target sequence
docs(mechanical): publish gripper mounting envelope
```

## Rules

- Imperative subject, 72 characters or fewer, no trailing period.
- One small, testable task slice per commit.
- Do not mix formatting, generated artifacts, refactors, and behavior changes unless inseparable.
- Stage only task files; never use broad staging without reviewing the result.
- Reference the issue in the PR with `Closes #N`; use the commit body only when the reason or risk is not clear from the diff.
- Never add AI attribution or `Co-Authored-By` trailers.
- Generated CAD, firmware binaries, logs, videos, or datasets require a source file or documented reproduction command.
- Before committing: run relevant checks, inspect the diff, update affected interface/test documents, and post blocking contract changes.

Use `chore(integration): checkpoint <description>` only for a verified, recoverable integration state before risky physical or cross-subsystem changes. A checkpoint is not a substitute for a working slice.
