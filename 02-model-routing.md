# 2. Model Routing

Pick the model once per session based on the task. Never switch mid-chat without a `/clear`.

| Task | Model | Effort |
|---|---|---|
| Development, architecture, production code | Opus 5.5 | medium |
| Reverse engineering (binary, hex, decompilation, APK/DEX/DOS, protocol reversing, memory inspection, obfuscated code) | Opus 4.6 | medium |
| Standard skills, scheduled routines, `/chrome` | Haiku 5.5 or Sonnet | — |
| Bulk subagent work (10+ sources, 40+ files) | Haiku 5.5 | — |
| Deep synthesis, complex code in subagents | Opus 5.5 | — |
| Reversing in subagents | Opus 4.6 | — |
| Subagents, when no multi-agent section exists | Haiku 5.5 | chosen by task complexity (see [step 11](11-subagent-orchestration.md)) |
| Chapters 15 and 16 (quota rotation, Android proxy) | Opus 4.6 | medium |

## Rules

- The agent cannot switch its own model. If the session is on the wrong one, tell the user which `/model` to choose before working.
- Lock the choice for the session. Model and effort are part of the cache key: switching mid-task rebuilds the cache and can cost more than staying on the bigger model ([step 20](20-prompt-cache-discipline.md)).
- For cheap side work, delegate to a subagent with `model: haiku` instead of `/model`. Avoid `opusplan` if you toggle plan mode often.
- Periodically audit routines: remove forgotten ones, downgrade over-provisioned ones.
