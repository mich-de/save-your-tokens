# 3. Session Lifecycle

## Checkpoint rule

At every completed milestone (sub-feature, module, reverse-engineering stage), update `HANDOFF.md` and tell the user to run `/clear` before the next task. Do not chain checkpoints in one growing conversation.

## Error recovery

When a path fails, prefer `/rewind` to stacked corrective prompts. Corrective prompts pile up in context and cost tokens on every future turn.

## No `/compact`, no auto-compact

Summarizing re-processes the entire conversation and can silently drop architectural details you need later. Disabled at boot, never used mid-session.

## 40–50% context ceiling

If a task reaches 40–50% context before a natural checkpoint:

1. Write `HANDOFF.md` autonomously (don't wait for the user to ask).
2. Tell the user to run `/clear`.
3. Resume from `HANDOFF.md` in the next session.

## Auto-resume

A global `SessionStart` hook checks for a fresh `HANDOFF.md` (modified < 2 hours ago) and injects a reminder to read it. The agent reads it and continues without the user needing to say anything.
