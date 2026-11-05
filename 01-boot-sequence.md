# 1. Boot Sequence

At the start of every session, run these checks in order:

## `/context` audit

Ask the user to run `/context` (only the user can run slash commands) to verify the cold-start footprint.

- **Target**: 3–6% context usage at boot.
- **Over budget (>10–20%)**: stop and audit with `/context` and `/usage` (session limits, weekly quota, parallel sessions, top skills).

## Auto-compact off

Keep auto-compact disabled (set through `/config`). Summarizing re-processes the whole chat and can drop architectural details. Never use `/compact` either.

## Output style

Set to `concise`. Every token counts — lead with results, skip ceremony.

## Model routing

At the first prompt, decide the model for the session (see [02-model-routing.md](02-model-routing.md)). The agent cannot switch its own model: if the session is on the wrong one, tell the user which `/model` to choose before working.

## Instruction files

Load `CLAUDE.md` or, as a fallback, `AGENTS.md` — never both, so instructions are not duplicated in context.

## HANDOFF.md check

If `HANDOFF.md` exists and was modified in the last 2 hours, read it and resume from where the previous session left off. A `SessionStart` hook in global settings can inject this reminder automatically.

## Status line

When configured, show: context %, model, session limit, weekly quota.
