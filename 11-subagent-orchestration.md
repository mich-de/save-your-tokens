# 11. Subagent Orchestration

Subagents have hidden overhead: each one loads context, tools, and instructions independently.

## Default when no multi-agent section exists

If the project, `CLAUDE.md` or task prompt has no multi-agent section (no explicit rules for which subagent model to use), default to **Haiku 5.5**, the fast frontier model, for every subagent. Set the effort yourself according to the complexity of the task:

| Task | Effort |
|---|---|
| Lookup, grep, single-file read, format check | low |
| Multi-file analysis, summaries, simple edits | medium |
| Multi-step reasoning that Haiku still handles | high |

If the task is too hard for Haiku even at high effort, do not silently switch models. Tell the user and use the routing table in [step 2](02-model-routing.md).

An explicit multi-agent section always overrides this default.

## Rules

- **Never spawn a subagent for a single task or small read.** Do it yourself.
- **Bulk only**: 10+ sources or 40+ files in parallel justify subagents.
- **Model selection for subagents**:
  - Standard bulk work → Haiku 5.5
  - Deep synthesis, complex code → Opus 5.5
  - Reverse engineering → Opus 4.6

## The cost

Each subagent:
- Loads its own copy of the system prompt
- Loads tool definitions
- Reads any instruction files in scope
- Processes the task prompt

For a simple file read, that overhead dwarfs the actual work. For 40 files in parallel, the parallelism pays for the overhead.
