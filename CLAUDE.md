# Save Your Tokens — Router

A zero-waste token protocol for Claude Code, OpenCode and similar AI coding agents.

This file is the only part always in context. It routes: find the trigger, read **that step only**, run the script instead of the model where one exists. The hook in `scripts/hooks/token_router.py` does the same routing automatically (see below).

## Route by moment

### Session start

| Trigger | Go to |
|---|---|
| New session | [01 Boot Sequence](01-boot-sequence.md): `/context` audit, auto-compact off, concise output |
| First prompt of the session | [02 Model Routing](02-model-routing.md): pick model and effort once |
| `HANDOFF.md` modified < 2 h ago | [04 HANDOFF.md Protocol](04-handoff-protocol.md): read it, resume from "Next step" |

### During the task

| Trigger | Go to |
|---|---|
| Milestone done, context growing, error loop | [03 Session Lifecycle](03-session-lifecycle.md) → write HANDOFF.md, `/clear` |
| UI, page, component, layout, mockup | [05 ASCII Wireframe Gate](05-ascii-wireframe-gate.md), then [17 Design Skill](17-design-skill-token-saver.md) |
| Large or unknown codebase | [09 Graph Navigation](09-graph-navigation.md) |
| A step repeats itself | [10 Deterministic Code Conversion](10-deterministic-code-conversion.md): make it a script |
| Tempted to spawn subagents or parallel sessions | [11 Subagent Orchestration](11-subagent-orchestration.md), [24 §3](24-field-notes-designer-workflow.md) |
| Tempted to `/model`, add an MCP, edit CLAUDE.md mid-task | [20 Prompt Cache Discipline](20-prompt-cache-discipline.md): don't, it rebuilds the cache |
| Compact, rewind or clear? | [21 Compaction Economics](21-compaction-economics.md) |
| Writing the answer | [12 Anti-Patterns and Output Style](12-anti-patterns-and-output.md) |

### Input that is not text

| Trigger | Run, don't read |
|---|---|
| PDF | `python scripts/extract_pdf.py file.pdf out.txt` ([07](07-deterministic-hooks-and-media.md)) |
| Screenshot of text, logs, code | `python scripts/extract_image_ocr.py shot.png out.txt` ([07](07-deterministic-hooks-and-media.md)) |
| YouTube video | `python scripts/fetch_subtitles.py URL out.txt` on the user's machine ([07](07-deterministic-hooks-and-media.md)) |
| Chart, mockup, diagram that must be seen | Native image read, once ([07 Visual exception](07-deterministic-hooks-and-media.md)) |

### Setup and tooling

| Trigger | Go to |
|---|---|
| Hooks, "always do X when Y" | [07 Deterministic Hooks](07-deterministic-hooks-and-media.md) |
| MCP server, connector, plugin | [08 CLI over MCP](08-cli-over-mcp.md), then [06 Memory and Skill Hygiene](06-memory-and-skill-hygiene.md) |
| Network blocked, proxy, `curl` checks, file names | [13 Network and Naming](13-network-and-naming.md); phone as proxy: [16](16-android-proxy-setup.md) |
| Free models, rate limits on OpenCode | [14 Free Models](14-opencode-free-models.md) (`scripts/list_free_models.py`), [15 Quota Rotation](15-opencode-quota-rotation.md) |
| Status bar | [18 Status Line](18-status-line.md) (`scripts/statusline.py`) |

### Audit

| Trigger | Go to |
|---|---|
| "Where did the tokens go?" | `python scripts/session_timeline.py` ([24 §6](24-field-notes-designer-workflow.md)) |
| What every request resends, what a feature costs | [19 Harness Anatomy](19-harness-anatomy.md) |
| Weekly, or before adding a skill/hook/MCP | [22 Idle Burn and Usage Audit](22-idle-burn-and-usage-audit.md): A/B it |
| Monthly, or after big setup changes | [23 Doctor and Prompt Audit](23-doctor-prompt-audit.md) in a fresh session |
| How a real team works with this | [24 Field Notes: Designer Workflow](24-field-notes-designer-workflow.md) |

## Router hook (deterministic routing)

`scripts/hooks/token_router.py` applies the tables above without the model deciding:

- `UserPromptSubmit`: matches triggers in the prompt, injects one line ("→ step 07, run extract_pdf.py"). No match, no output, no tokens.
- `PreToolUse` on `Read`: denies native PDF reads, asks before image reads, points to the script.
- `SessionStart`: injects the HANDOFF.md reminder when the file is fresh.

Registered for this repo in `.claude/settings.json`. For all projects, see [07 → Router hook](07-deterministic-hooks-and-media.md#router-hook).

## Cache discipline (harness)

- Model + effort decided at session start. Never `/model` mid-task; use a subagent (`model: haiku`) for cheap side work.
- No MCP/plugin connect/disconnect mid-task. Keep tool search on. Deny rules: scoped, not whole tools.
- CLAUDE.md edits apply only after `/clear`, `/compact` or restart: edit between tasks.
- Before a break longer than the cache TTL: finish the task, write `HANDOFF.md`, `/clear` on return.
- Check `/usage` → "Prompt cache (main)": misses with a likely cause = fix the cause.
- Monthly or after big setup changes: `/doctor prompt-audit` in a fresh session (step 23).

# Compact instructions

When compacting, keep: current task goal, files changed, failing tests and errors,
decisions with reasons, next step. Drop: exploration output, full logs, resolved errors.
