# 20. Prompt Cache Discipline

The biggest lever is not "use less context" but **don't break the prompt cache**. Cached prefix tokens are billed at a fraction of the normal rate, but only while the prefix stays identical.

## What breaks the cache

- Switching model (`/model`), including `opusplan` on every plan-mode toggle, automatic model fallback, and skills or commands with a different `model:` in their frontmatter.
- Changing effort (on most models; on some current models via API key or subscription the cache survives — check your version).
- Turning on fast mode (once per conversation).
- Connecting or removing MCP servers or plugins with MCP servers, when their tools are not deferred.
- Denying a whole tool with a deny rule, when tool search is off.
- Compacting (the conversation layer is rebuilt by design).
- Piling up many images or PDFs (they are dropped in batches).
- Updating Claude Code (first turn after restart is uncached).

## What does not break it

Editing repo files, editing CLAUDE.md mid-session (but the edit only applies after `/clear`, `/compact` or restart), changing permission mode, changing output style, invoking skills and commands, `/rewind`, starting a subagent.

## Golden rules

1. Pick model and effort at session start. Never `/model` mid-task.
2. Need a cheaper model for side work? Delegate to a subagent with `model: haiku` instead of switching. At 100k tokens of context, switching Opus → Haiku for one easy question costs *more* than letting Opus answer, because the Haiku cache must be built from scratch.
3. Avoid `opusplan` if you toggle plan mode often.
4. No MCP/plugin connect or disconnect mid-task. Keep tool search on (don't set `ENABLE_TOOL_SEARCH=false`). Prefer scoped deny rules (`Bash(rm *)`) to denying whole tools.
5. Update Claude Code between sessions, not during one (`DISABLE_AUTOUPDATER=1` if you want to control when).

## Cache TTL

| Setup | Main conversation | Subagents, fork, compaction |
|---|---|---|
| Claude subscription, within included usage | 1 hour | 5 minutes |
| API key, cloud provider, usage credits | 5 minutes | 5 minutes |

`promptCacheTtl` and `subagentPromptCacheTtl` (`5m` or `1h`, recent versions) let you choose. On an API key with frequent 5–60 minute pauses, `1h` pays off; for bursty work without pauses, keep `5m` (1h writes cost more).

The first message after a pause longer than the TTL reprocesses everything. Before a long break: finish the task, write `HANDOFF.md`, `/clear` on return.

## Proxies and gateways

If a gateway or proxy strips the `cache_control` markers, the whole history is billed uncached on every turn. Check this before routing through one (see [step 16](16-android-proxy-setup.md) for the network-level proxy, which does not touch the payload).

## Measure

- `/usage` → **Prompt cache (main)** line: hit rate, misses and a "likely cause". A miss with a cause = fix the cause.
- `cache_read_input_tokens` vs `cache_creation_input_tokens`: if creation stays high turn after turn, something in the prefix keeps changing. Surface it in the [status line](18-status-line.md).

Sources: [Claude Code docs — Prompt caching](https://code.claude.com/docs/en/prompt-caching); [Lessons from building Claude Code: Prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything).
