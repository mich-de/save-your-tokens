# 8. CLI over MCP

Prefer a CLI tool to an MCP server or raw API JSON.

## Why

- A CLI costs **zero context at startup** — no tool definitions loaded until you call it.
- An MCP server injects its full tool schema into context on every turn.
- CLI output is compact text; MCP responses are often verbose JSON.

## Examples

| Instead of | Use |
|---|---|
| GitHub MCP server | `gh` CLI |
| Vercel MCP server | `vercel` CLI |
| Supabase MCP server | `supabase` CLI |
| Google Cloud MCP server | `gcloud` CLI |
| Android device MCP | `adb` CLI |

## When MCP is fine

- When the CLI doesn't exist for that service.
- When you need real-time streaming or event subscriptions.
- When the MCP server provides capabilities the CLI lacks (e.g., Vercel MCP's 200+ specialized tools).

The key question: **does this tool need to be in context on every turn, or only when I call it?** If only when called, use the CLI.
