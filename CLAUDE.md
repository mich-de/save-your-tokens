# Save Your Tokens — Index

A zero-waste token protocol for Claude Code, OpenCode and similar AI coding agents.

Read each step in order, or jump to the one you need.

## Steps

1. [Boot Sequence](01-boot-sequence.md) — what to check at session start
2. [Model Routing](02-model-routing.md) — which model for which task
3. [Session Lifecycle](03-session-lifecycle.md) — checkpoints, error recovery, context ceiling
4. [HANDOFF.md Protocol](04-handoff-protocol.md) — the 6-section handoff file
5. [ASCII Wireframe Gate](05-ascii-wireframe-gate.md) — sketch before code
6. [Memory and Skill Hygiene](06-memory-and-skill-hygiene.md) — trim idle MCPs, instruction files and skills
7. [Deterministic Hooks and Media](07-deterministic-hooks-and-media.md) — hooks over prompts, local scripts for PDF/OCR
8. [CLI over MCP](08-cli-over-mcp.md) — prefer CLIs to MCP servers
9. [Graph Navigation](09-graph-navigation.md) — when to use a code graph
10. [Deterministic Code Conversion](10-deterministic-code-conversion.md) — AI for judgment, code for everything else
11. [Subagent Orchestration](11-subagent-orchestration.md) — when (and when not) to spawn subagents
12. [Anti-Patterns and Output Style](12-anti-patterns-and-output.md) — what to avoid, and the concise output style
13. [Network and Naming Rules](13-network-and-naming.md) — proxy routing, `curl.exe` checks, generic file names
14. [OpenCode Free Models](14-opencode-free-models.md) — find $0 models with a command, plus quota limits
15. [OpenCode Quota Rotation](15-opencode-quota-rotation.md) — IP rotation on rate limits (Opus 4.6 only)
16. [Android as Network Proxy](16-android-proxy-setup.md) — use a phone to bypass network blocks (Opus 4.6 only)
17. [Design Skill in Token-Saver Mode](17-design-skill-token-saver.md) — best design skill, used cheaply
18. [Status Line](18-status-line.md) — 3-line bar: limits, context, tools, network, remote control
19. [Harness Anatomy](19-harness-anatomy.md) — what every request resends, and what each feature costs
20. [Prompt Cache Discipline](20-prompt-cache-discipline.md) — what breaks the cache, TTLs, golden rules
21. [Compaction Economics](21-compaction-economics.md) — compact, rewind or clear: warm vs cold cache
22. [Idle Burn and Usage Audit](22-idle-burn-and-usage-audit.md) — tokens spent while idle, and A/B-testing harness changes

## Cache discipline (harness)

- Model + effort decided at session start. Never `/model` mid-task; use a subagent (`model: haiku`) for cheap side work.
- No MCP/plugin connect/disconnect mid-task. Keep tool search on. Deny rules: scoped, not whole tools.
- CLAUDE.md edits apply only after `/clear`, `/compact` or restart: edit between tasks.
- Before a break longer than the cache TTL: finish the task, write `HANDOFF.md`, `/clear` on return.
- Check `/usage` → "Prompt cache (main)": misses with a likely cause = fix the cause.

# Compact instructions

When compacting, keep: current task goal, files changed, failing tests and errors,
decisions with reasons, next step. Drop: exploration output, full logs, resolved errors.

## Scripts

- [`scripts/extract_pdf.py`](scripts/extract_pdf.py) — PDF to text without the model
- [`scripts/extract_image_ocr.py`](scripts/extract_image_ocr.py) — screenshot OCR without the model
- [`scripts/statusline.py`](scripts/statusline.py) — 3-line status bar, zero model tokens
- [`scripts/list_free_models.py`](scripts/list_free_models.py) — list free OpenCode models from models.dev
