# 19. Harness Anatomy

The harness is the layer around the model that provides the tools and manages the context the model sees. Knowing what it sends on every request tells you where tokens actually go.

## Every turn resends everything

The model remembers nothing between requests. On every turn Claude Code resends:

1. the system prompt and tool definitions,
2. the project context (CLAUDE.md, auto memory, rules without `paths:`),
3. the whole conversation: every message and every tool result so far,
4. your new message.

Each tool call is a further request carrying that batch of results. A one-line question in a session open all day still pays for the entire conversation.

## Three layers, ordered by how often they change

| Layer | Contains | Changes when |
|---|---|---|
| System prompt | Core instructions, tool definitions | The set of loaded tools changes |
| Project context | CLAUDE.md, auto memory, rules without `paths:` | Session start, `/clear`, `/compact` |
| Conversation | Messages, replies, tool results | Every turn |

The prompt cache matches the prefix byte for byte. Anything that changes "high up" invalidates everything below it. See [step 20](20-prompt-cache-discipline.md).

## Fixed overhead before your first prompt

Third-party proxy measurements put Claude Code's first payload in the 20–35k token range, most of it tool definitions. These numbers depend on version and setup: measure your own with `/context` at the start of a session and keep it as a baseline.

## Cost by feature

| Feature | Weighs on every request? |
|---|---|
| CLAUDE.md, output style | Yes, in full |
| Skills | Description only (zero with `disable-model-invocation: true`) |
| MCP servers | Tool names only, schemas deferred via tool search |
| Subagents | No, isolated context |
| Hooks | No, except the output they return |

## Rules

- Measure the baseline with `/context` before optimizing anything.
- Keep CLAUDE.md under ~200 lines and output styles short: they ride on every request.
- Fewer turns beat a smaller prompt: the number of round-trips and cache hits matter more than fixed overhead.

Sources: Claude Code docs, [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) and [Context window](https://code.claude.com/docs/en/context-window); [Systima overhead comparison](https://systima.ai/blog/claude-code-vs-opencode-token-overhead).
