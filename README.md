# Save Your Tokens

A practical protocol for keeping Claude Code (and similar AI coding agents) lean on context, deterministic where possible, and reliable across sessions.

## What this is

A set of rules, scripts and conventions born from real daily use of Claude Code, OpenCode and other AI coding CLIs. The goal: **spend tokens on judgment, not on ceremony**.

## Key ideas

- **Checkpoint, don't compact.** Write a `HANDOFF.md` at every milestone, then `/clear`. Never auto-compact — it re-processes everything and can drop details.
- **Model routing by task.** Opus 5.5 for code, Opus 4.6 for reverse engineering, Haiku for bulk/scheduled work. Pick once per session.
- **Deterministic over probabilistic.** If a step is repeatable, make it a script or a hook. The LLM handles judgment; everything else is code.
- **CLI over MCP.** `gh`, `vercel`, `adb` cost zero context at boot and return compact output only when called.
- **ASCII before pixels.** Sketch the layout in ASCII first, iterate cheaply, write production code after approval.
- **Android as a network proxy.** When your network blocks AI services, route traffic through a phone over USB tethering + VPN.
- **Design skill, cheaply.** Use the most installed design skill (`frontend-design`) with wireframe-first, one-pass generation and a short design brief.

## Structure

See **[CLAUDE.md](CLAUDE.md)** for the full index — each step is a separate file you can read in order or jump to directly.

The `scripts/` folder contains four Python utilities that replace expensive model calls:

| Script | Replaces | Requires |
|---|---|---|
| `extract_pdf.py` | Native PDF read (1500-3000 tokens/page) | `pypdf` |
| `extract_image_ocr.py` | Vision model on text screenshots | `tesseract` |
| `list_free_models.py` | Browsing for free OpenCode models | (stdlib only) |
| `statusline.py` | Checking `/context`, `/usage` and network by hand ([step 18](18-status-line.md)) | (stdlib only) |

## Quick start

1. Copy the `scripts/` folder into your skill or project.
2. Read `CLAUDE.md` and the step files that matter to your setup.
3. Add the boot-sequence checks to your `CLAUDE.md` or skill.
4. Set up `HANDOFF.md` checkpointing in your workflow.

## License

Public domain. Use however you like.
