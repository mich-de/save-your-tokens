# 22. Idle Burn and Usage Audit

Long sessions spend tokens even when you are not typing. And every harness change should be measured, not assumed.

## Idle burn sources and switches

| Source | Switch |
|---|---|
| Scheduled `/loop` tasks resend the whole context on every tick | Stop the ones you no longer need |
| Messages from other sessions | `crossSessionInbound: hold` |
| Goal check-ins (up to three per goal between prompts) | `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0` |
| Prompt suggestions | Turn off when close to your limit |
| Finished subagents and teammates still alive | Close them |

Agent teams are expensive: each teammate has its own context window (roughly 7× a standard session when teammates are in plan mode). Keep teams small, teammates on Sonnet, spawn prompts short.

## Weekly audit

1. `/usage` — attribution per skill, MCP and subagent; read the recommendations (press `f` for details).
2. `/usage` → **Prompt cache (main)** — hit rate and likely causes of misses ([step 20](20-prompt-cache-discipline.md)).
3. `/insights` — recurring patterns.
4. `/context` — compare with the baseline from [step 19](19-harness-anatomy.md).

## A/B every harness change

A new skill, hook, MCP server or CLAUDE.md rule is a change to the harness, and harness changes can cost more than they save. Automated harness optimization research (e.g. Harness², Google/Northwestern 2026) spends roughly 8–40× the tokens to find changes that actually matter.

Do the cheap manual version:

1. Pick one representative task.
2. Run it before and after the change, same model, effort and starting state.
3. Compare total tokens, cache hit rate and whether the task succeeded.
4. Keep the change only if it improves the result or cost. Revert otherwise.

Note: availability of some commands and fields depends on the Claude Code version; check `claude --version` against the docs.

Source: [Claude Code docs — Manage costs effectively](https://code.claude.com/docs/en/costs).
