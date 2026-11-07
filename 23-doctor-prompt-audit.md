# 23. Doctor Prompt Audit

`/doctor prompt-audit` (alias `/checkup prompt-audit`, Claude Code 2.1.283+) reviews your own setup for instructions that waste context: stale facts, contradictions and prompting patterns written for older models. CLAUDE.md and output styles ride on every request ([step 19](19-harness-anatomy.md)), so every dead line costs tokens on every turn.

## What it reads

CLAUDE.md, AGENTS.md, CLAUDE.local.md, skills, subagents, slash commands, rules and output styles. It skips files that may hold secrets (`.mcp.json`, settings files): it is not a security audit.

## What it finds

| Category | Example |
|---|---|
| Stale paths | CLAUDE.md references a script that no longer exists |
| Stale commands | A skill runs an `npm` script removed from `package.json` |
| Contradictions | CLAUDE.md and a skill give opposite instructions |
| Older-model patterns | "Think step by step", repeated `MUST`, long history stories |
| Tool descriptions, request configuration | Instructions that fight the harness |

Each finding has file and line, evidence, confidence and an action (rewrite, remove, add, flag). It proposes a diff; nothing is applied until you confirm each hunk.

## How to run it

Interactive, from the project root:

```
/doctor prompt-audit
```

Headless and report-only:

```bash
claude -p "/doctor prompt-audit" --disallowedTools "Edit,Write,NotebookEdit"
```

Headless mode cannot read `~/.claude/` or parent folders, so user-level config is excluded: run it interactively to audit global CLAUDE.md and skills too.

## Cost and cadence

The audit itself spends tokens, and the cost grows with the size of your config (one reported run: 17 skills, 2 subagents, a 285-line CLAUDE.md → 63 turns, about $4 on Opus). So:

- Run it after a big setup change, or monthly, not every session.
- Run it at the start of a fresh session (`/clear` first), not in the middle of a task: the edits to CLAUDE.md only apply after `/clear` anyway ([step 20](20-prompt-cache-discipline.md)).
- Apply the fixes, then measure before/after with `/context` ([step 22](22-idle-burn-and-usage-audit.md)).

## Not to confuse with

- `/doctor` alone: checks installation and configuration health.
- `/claude-api prompt-audit`: reviews prompts in apps you build on the Claude API.

Sources: [ayautomate — /doctor prompt-audit, tested](https://www.ayautomate.com/blog/claude-code-prompt-audit), [claudcod — Claude Code Prompt Audit](https://claudcod.com/blog/claude-code-prompt-audit/).
