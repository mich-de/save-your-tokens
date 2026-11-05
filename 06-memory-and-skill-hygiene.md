# 6. Memory and Skill Hygiene

## Idle MCPs

Review with `/mcp`, disable the unused ones. Every active MCP server adds tool definitions to context at boot.

## Root instruction file

Keep `CLAUDE.md` (or `AGENTS.md`) under 200 lines. Use it as a routing map — point to per-folder files for detailed rules.

It is re-read on every message, so every line costs tokens on every turn.

## Per-folder instruction files

Detailed rules live in the folder they concern and load only when entering that folder. This keeps the root file lean and avoids paying for irrelevant rules.

```
project/
  CLAUDE.md          ← routing map, <200 lines
  src/
    CLAUDE.md        ← src-specific rules, loaded only when working in src/
  infra/
    CLAUDE.md        ← infra-specific rules
```

## Skills

- Archive unused skills — they appear in the skill listing and add to context.
- Keep descriptions short — they are loaded at boot.
- Test triggers after compressing descriptions to make sure they still fire.
