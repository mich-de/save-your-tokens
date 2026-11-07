# 23. Doctor and Prompt Audit

Instruction files ride on every request ([step 19](19-harness-anatomy.md)). Stale, contradictory or over-specified rules cost tokens on every turn and make the agent work around them. Claude Code has built-in audits for this: run them instead of reviewing by hand.

Requires Claude Code **v2.1.283 or later** (`claude --version`).

## The three commands

| Command | What it checks | Use it for |
|---|---|---|
| `/doctor prompt-audit` (alias `/checkup prompt-audit`) | Instruction text: CLAUDE.md, CLAUDE.local.md, AGENTS.md, rules, skills, commands, subagents, output styles | Dated, conflicting or stale instructions |
| `/skill-doctor` | Skills: context cost and actual usage | Pruning or disabling skills that cost context but are never used |
| `/doctor` (alias `/checkup`) | General setup | Install and configuration health |

Bare `claude doctor` from the terminal is a different, read-only install diagnostic.

## What `/doctor prompt-audit` flags

- **Dated prompt text:** shouting (MUST, NEVER, CRITICAL) without reasons; hedges on real requirements.
- **Replaced scaffolds:** "think step by step", scratchpad tags and other tricks the model or API now handles.
- **Over-specification:** choreographed steps for judgment work, long prohibition lists.
- **Fossils:** workarounds for a retired model's habits.
- **Thinking instructions** that the current model cannot follow (on Opus 5.5 effort is the only control).
- **Stale facts:** paths, commands and flags that no longer exist in the repo.
- **Contradictions** between instruction files (`git blame` decides which is newer; safety rules are left for you to decide).
- **Unenforced instructions:** rules nothing checks.
- **History narratives:** incident IDs, past tense, pinned model names.

Output: a report ordered by confidence, each finding with `file:line`, the quoted text, why it is obsolete and a proposed edit. **Nothing changes until you ask Claude to apply the edits.** It never reads settings, `.mcp.json` or `~/.claude.json` (they can hold secrets).

## How to run it cheaply

1. Set the target model first with `/model`, at session start ([step 20](20-prompt-cache-discipline.md)): the audit judges instructions against the session's model.
2. Run it in a dedicated session, then `/clear`: the report is long and you do not want it in your working context.
3. Narrow the scope when you only changed one thing: `/doctor prompt-audit .claude/skills/deploy/SKILL.md`. Extra words after the command are passed through unchanged and drop the default scope, so do not add comments.
4. Apply edits between tasks: CLAUDE.md changes only take effect after `/clear`, `/compact` or restart.
5. Measure before and after with `/context` and a representative task ([step 22](22-idle-burn-and-usage-audit.md)).

## When to run it

- After every model change, including default-model changes you did not choose.
- After adding or editing skills, rules or a large CLAUDE.md section.
- As part of the weekly audit in [step 22](22-idle-burn-and-usage-audit.md), together with `/skill-doctor`.

## Tips

- Keep reasons in present tense inside the file; keep incident history and model names in commit messages.
- Before deleting an "unenforced" rule, grep for its exact text: tests or log parsers may match on it.
- The audit depends on the bundled `claude-api` skill: it will not run if that skill is disabled in `skillOverrides` or `disableBundledSkills` is set.

Sources: [claude/for — How to run /doctor prompt-audit](https://claude-for.com/guides/how-do-i-run-claude-code-doctor-prompt-audit); [max.nardit.com — /doctor prompt-audit](https://max.nardit.com/articles/prompt-audit-claude-md).
