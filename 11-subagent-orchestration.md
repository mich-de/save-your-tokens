# 11. Subagent Orchestration

Subagents have hidden overhead: each one loads context, tools, and instructions independently.

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
