# 24. Field Notes: a Product Designer's AI Workflow

What a working product designer does with Claude Code day to day, and where the tokens go. These notes are taken from an interview, not from benchmarks. Each lesson links to the step that covers the rule.

Source: Marcello Ascani, *Il Lavoro del Designer Non Sarà Più lo Stesso* ([YouTube](https://youtu.be/8nPiBtYQZcA)), series *AI Future for Work* with Talent Garden. The guest is Massimiliano "Max" Bolognesi, product designer at an Italian HR and payroll startup with 11 designers and a product team of 80–90 people.

## How the workflow changed

| Period | Workflow |
|---|---|
| Before | Design everything in Figma, then hand it to developers. |
| Vibe-coding tools | Build an interactive prototype first (Lovable, Figma Make), test it with customers, then design. |
| Early agents in the codebase | Try building the feature directly in a copy of the codebase. It works, but the result is not good enough yet. |
| Current frontier models | Figma only for direction: 3–4 screens. Then give Claude the screens, the design system and the codebase, and ask for the feature. Features ship to production. |

The designer now works much closer to the developers. The developers also write code with AI and are becoming more product-oriented.

## Token lessons

### 1. The codebase is the brief

"What is in the codebase is what the product actually is." The design system (components, colors, fonts) is already in the code, so the agent reads it from there.

- Don't paste the design rules into the prompt. Point to where they live in the code.
- Keep design tokens in one file ([step 17](17-design-skill-token-saver.md), rule 8), so one read gives the agent the whole style.
- A few Figma screens plus the codebase are enough context. A full Figma file is not needed.

### 2. Context still has to be built

"AI works well when you give it a lot of context, and you have to build that context." The team connects Claude to its internal wiki through connectors.

- Every connector adds tool definitions to every request ([step 19](19-harness-anatomy.md)). Connect the one or two sources you really use, and prefer a CLI or an exported file when one exists ([step 8](08-cli-over-mcp.md)).
- Write the context once, in a file or a skill. Don't re-explain it in every chat.

### 3. Parallel sessions empty the plan

While the agent works, you wait. The temptation is to start another feature, then another: "while it thinks you have already sent seven other prompts". That is why the guest had run out of credits for the top model during the recording, and had to demo with the next model down.

- Every parallel session pays for its own context, and none of them shares a cache.
- The guest's own limit: past a few sessions "you struggle to keep up". Cap it at 2–3 sessions you can actually review.
- Use the wait for review, not for new prompts. Use subagents for side work, with a cheap model ([step 11](11-subagent-orchestration.md)).

### 4. Hard work to the big model, easy work to the small one

"The more intelligent the model, the more tokens you use", so hard tasks go to advanced models and easy ones to cheaper models. This is [step 2](02-model-routing.md). Running out of credits on the top model is the expensive way to learn it.

### 5. Shared team skills

The team packages its development, design and discovery skills into one shared bundle for the whole product team. A developer can build a feature using the design skill, without asking a designer for help.

- One shared package means one copy of each instruction, versioned and reviewed, instead of everyone pasting their own prompts.
- Load only the skills a task needs, and prune the ones nobody uses ([step 6](06-memory-and-skill-hygiene.md), [step 23](23-doctor-prompt-audit.md)).
- The guest expects skills to matter less as models improve, so re-check each one with an A/B run ([step 22](22-idle-burn-and-usage-audit.md)).

### 6. Look at the token timeline

The team is building an internal tool that loads the chat's JSONL export and shows a timeline of what happened. That way you see where you spent "a huge amount of tokens" on something trivial.

Claude Code already saves that JSONL for every session, under `~/.claude/projects/`. Read it locally, at zero model tokens:

```bash
python scripts/session_timeline.py                 # most recent session
python scripts/session_timeline.py session.jsonl --top 10
```

For each of your messages it prints how many requests it generated, the tools used, and the tokens: **new** (input plus cache writes, paid at full price or more), **cache** (cache reads, about a tenth of the price) and **out** (output). At the end it lists the most expensive requests.

Example from the session that wrote this step:

```
  # ora   rich   nuovi   cache    out  messaggio / tool
  3 14:56    1      24   91.8k    533  Ma perché non riesci ad analizzarlo?
  4 14:57    2   33.1k  153.7k    871  Riprova
```

Turn 4 came right after a `/model` switch. Changing the model rebuilt the cache, so one short retry cost 33k new tokens. A plain question one turn earlier cost 24. This is the cost [step 20](20-prompt-cache-discipline.md) warns about, made visible.

What to look for:

- A turn with large **new** tokens and a small message: a cache break (model switch, connector change, CLAUDE.md edit) or a big file read.
- Many requests for one message: the agent is looping. Give it a better brief, or stop it.
- The same tool repeated many times: a missing script or hook ([step 10](10-deterministic-code-conversion.md)).

### 7. Voice prompts

The guest dictates prompts with a push-to-talk app: much faster than typing. Spoken prompts are longer and full of filler, though. Dictate, then trim before sending, or say the goal, the constraint and what "done" means in three sentences.

## What the AI doesn't do (yet)

According to the guest:

- Product vision: talking to people and finding the real opportunities.
- Building the context the model needs.
- Problems the AI still can't automate well. For his company, that is Italian bureaucracy, and it is the business opportunity.

His advice for a designer starting today: learn the tools, follow the AI startups and their founders, read a weekly design newsletter, and do hackathons to learn the whole flow from problem to product. He expects roles to become horizontal: "builders" who go from the problem to the shipped feature, covering research, design and development.
