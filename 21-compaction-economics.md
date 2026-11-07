# 21. Compaction Economics

Compaction is not always expensive. It depends on whether the cache is warm.

- **Warm cache** (within the TTL): the summary request reuses the session prefix ("cache-safe forking"), so `/compact` costs a fraction of what the context size suggests.
- **Cold cache** (after a pause beyond the TTL, or a resumed old session): the whole history is reprocessed at full price.

## Decision tree

| Situation | Do |
|---|---|
| Task finished, cache warm, next task related | `/compact focus on <what matters next>` |
| Took a wrong branch | `/rewind` (returns to an already-cached prefix) |
| Topic change, or cache cold | Write `HANDOFF.md`, then `/clear` |
| Context climbing mid-task | Never let auto-compact fire mid-task: checkpoint first ([step 3](03-session-lifecycle.md)) |

## What survives compaction

- Re-injected from disk: root CLAUDE.md, rules without `paths:`, auto memory, the plan-mode plan.
- Lost until a matching file is touched again: rules with `paths:`, nested CLAUDE.md files.
- Up to 5 recently read files are re-read (files over ~5k tokens come back only as a reference).
- Invoked skill bodies come back capped at ~5k tokens per skill and ~25k total, **cut from the end**.

Implications:

- Rules that must survive go in the root CLAUDE.md or in rules without `paths:`.
- Put the critical instructions at the **top** of each `SKILL.md`.

## Compact instructions

Add this section to the root CLAUDE.md. It is re-injected after every compaction, so it governs the event itself:

```markdown
# Compact instructions
When compacting, keep: current task goal, files changed, failing tests and errors,
decisions with reasons, next step. Drop: exploration output, full logs, resolved errors.
```

## Tuning

- `/autocompact <N>` moves the auto-compact threshold earlier or later.
- Idle compaction (`idleCompaction`, 1h TTL) compacts sessions left idle; turn it off if you prefer `/clear` + `HANDOFF.md`.
- Thrashing: huge tool outputs can trigger repeated compactions. Filter them with a hook ([step 7](07-deterministic-hooks-and-media.md)).

Sources: [Claude Code docs — Context window](https://code.claude.com/docs/en/context-window), [Prompt caching](https://code.claude.com/docs/en/prompt-caching).
