# Save Your Tokens — Index

A zero-waste token protocol for Claude Code, OpenCode and similar AI coding agents.

Read each step in order, or jump to the one you need.

## Steps

1. [Boot Sequence](01-boot-sequence.md) — what to check at session start
2. [Model Routing](02-model-routing.md) — which model for which task
3. [Session Lifecycle](03-session-lifecycle.md) — checkpoints, error recovery, context ceiling
4. [HANDOFF.md Protocol](04-handoff-protocol.md) — the 6-section handoff file
5. [ASCII Wireframe Gate](05-ascii-wireframe-gate.md) — sketch before code
6. [Memory and Skill Hygiene](06-memory-and-skill-hygiene.md) — keep instruction files lean
7. [Deterministic Hooks and Media](07-deterministic-hooks-and-media.md) — scripts over model calls for PDF/OCR
8. [CLI over MCP](08-cli-over-mcp.md) — prefer CLIs to MCP servers
9. [Graph Navigation](09-graph-navigation.md) — when to use a code graph
10. [Deterministic Code Conversion](10-deterministic-code-conversion.md) — AI for judgment, code for everything else
11. [Subagent Orchestration](11-subagent-orchestration.md) — when (and when not) to spawn subagents
12. [Anti-Patterns and Output Style](12-anti-patterns-and-output.md) — what to avoid
13. [Network and Naming Rules](13-network-and-naming.md) — proxy routing and file naming
14. [OpenCode Free Models](14-opencode-free-models.md) — find $0 models deterministically
15. [OpenCode Quota Rotation](15-opencode-quota-rotation.md) — IP rotation on rate limits
16. [Android as Network Proxy](16-android-proxy-setup.md) — use a phone to bypass network blocks

## Scripts

- [`scripts/extract_pdf.py`](scripts/extract_pdf.py) — PDF to text without the model
- [`scripts/extract_image_ocr.py`](scripts/extract_image_ocr.py) — screenshot OCR without the model
- [`scripts/list_free_models.py`](scripts/list_free_models.py) — list free OpenCode models from models.dev
