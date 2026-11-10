# Tyxuan AI

## Picking a model (save credits)

This repo's `.claude/settings.json` sets the model to `opusplan`: Opus while in plan mode, Sonnet when carrying out the plan. Subagents default to Haiku through `CLAUDE_CODE_SUBAGENT_MODEL`.

- **Haiku** (`/model haiku`): quick lookups, renames, formatting, small one-file edits, summarising files or logs.
- **Sonnet** (`/model sonnet`): everyday coding, tests, bug fixes, refactors. The default for implementation.
- **Opus** (`/model opus`, or plan mode under `opusplan`): architecture, tricky multi-file changes, hard bugs that Sonnet couldn't crack.

When delegating to a subagent, keep it on Haiku for searching and reading. Pass `sonnet` or `opus` only when the subagent has to write or reason about non-trivial code.

## Agent skills

### Issue tracker

Issues are tracked in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Uses the five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
