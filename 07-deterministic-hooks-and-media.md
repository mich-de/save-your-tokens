# 7. Deterministic Hooks and Media Protocol

## Hooks over prompts

Prompts are probabilistic — the model might skip a rule. Hooks are deterministic — the harness always runs them.

Use hooks for mandatory rules: "always do X when Y" belongs in a hook, not in a prompt.

Hooks cost zero tokens, except the output they return to the model (`additionalContext`, stdout on some events). A hook that injects text on every turn is a CLAUDE.md you can't see: check what it returns.

## Recommended hooks (code-reviewed)

Third-party hooks run with your permissions. The projects below were read file by file in November 2026 (no code executed). Re-check before installing a newer version.

| Hook | Source | Verdict | Why |
|---|---|---|---|
| `guard-pack` | [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks) (MIT) | Recommended | Seven safety guards (dangerous commands, secrets, git, tests, config) in one PreToolUse process. No network, no deps, fails open. Don't also install the single guards: every check would run twice. |
| `subagent-spawn-cap` | same | Recommended | Asks at 20 subagent spawns per session, denies at 60. Simple, correct, prunes its own files. Pairs with [step 11](11-subagent-orchestration.md). |
| `cache-tax` | same | With caveats | Warns (or blocks once with `CACHE_TAX_BLOCK=1`) when your next message would rebuild an expired cache over 50k tokens. Saves only if you act on it; price table is hard-coded. Pairs with [step 20](20-prompt-cache-discipline.md). |
| `context-hogs` | same | With caveats | Ranks files by context cost (bytes/4, rough). Reports only; saves nothing by itself. |
| [ecotokens](https://github.com/hansipie/ecotokens) | MIT, build from source | With caveats | Filters Bash output, keeps exit codes and stderr, no telemetry. But: generic outputs over 200 lines keep only the first and last 20 (an error in the middle disappears); stores masked outputs and file snippets on disk; its Read/Grep PostToolUse hook *adds* context on Claude Code. Install only the Bash hook, set `raw_recovery_enabled` off if you don't want logs. |
| [squeez](https://github.com/claudioemmanuel/squeez) | Apache-2.0 | Avoid by default | Auto-approves almost every Bash command (`permissionDecision: allow`) with a short substring deny list, rewrites `~/.claude/CLAUDE.md` every session (persona + prose compression), takes over the status line and reads the OAuth token, collapses successful `git push`/installs to `ok`. npm install pipes an unpinned script to `sh`. Not malicious, but it bypasses permission prompts and edits the prefix ([step 20](20-prompt-cache-discipline.md)). |

Not recommended: the popular "7 token-saving hooks" gist by yurukusa ships only the `settings.json` snippet; the scripts are in a paid book and the quick install runs `npx` on another repo. Nothing to review, so nothing to install.

Common caveats:

- `guard-pack` and the karanb192 guards log full commands to `~/.claude/hooks-logs/`, never pruned: secrets typed inline end up there. Clean the folder periodically.
- Prefer hooks that **warn** or **filter** over hooks that **approve**: a hook returning `allow` skips your permission prompts.
- Measure before and after any hook ([step 22](22-idle-burn-and-usage-audit.md)).

To browse more: [loqimean/awesome-claude-code-hooks](https://github.com/loqimean/awesome-claude-code-hooks) (curated, by category).

## Install globally (all projects)

Hooks at **user** level (`~/.claude/`) run in every project; project-level ones (`.claude/` in the repo) only there.

`/plugin` works only in Claude Code (terminal, IDE or desktop Code tab), not in the Claude chat app ("`/plugin` isn't available in this environment"). Run it on your own machine.

Inside a Claude Code session:

```
/plugin marketplace add karanb192/claude-code-hooks
/plugin install guard-pack@claude-code-hooks
/plugin install subagent-spawn-cap@claude-code-hooks
```

Pick scope **user** when asked: user = all your projects, project = everyone using that repo, local = only you in that repo.

From a terminal, the same without opening a session:

```bash
claude plugin marketplace add karanb192/claude-code-hooks
claude plugin install guard-pack@claude-code-hooks --scope user
claude plugin install subagent-spawn-cap@claude-code-hooks --scope user
```

Manual alternative: copy the script into `~/.claude/hooks/` and register it in `~/.claude/settings.json` (not the project one). Project settings add to user settings, so a user hook runs everywhere.

Then:

- Restart Claude Code and check with `/hooks` in a new session.
- Install between sessions, not mid-task ([step 20](20-prompt-cache-discipline.md)).
- Need a project without a hook? Disable that plugin there with `/plugin`.

## PDF extraction

Native PDF read costs 1,500–3,000 tokens per page. When you only need the text:

```bash
python scripts/extract_pdf.py document.pdf output.txt
```

Requires `pypdf` (`pip install pypdf`). The script extracts text page by page, reports blank pages, and exits with code 3 if the PDF is image-only (needs OCR instead).

## Screenshot OCR

Screenshots of text, logs or code should be OCR'd locally, not sent to the vision model:

```bash
python scripts/extract_image_ocr.py screenshot.png output.txt
```

Requires `tesseract` installed and in PATH. Uses Italian + English by default.

## Video subtitles

The model can't watch a video, and a cloud session usually can't fetch it: YouTube blocks data-center IPs ("Sign in to confirm you're not a bot"). Fetch the subtitles on your own machine and paste the text:

```bash
python scripts/fetch_subtitles.py https://youtu.be/VIDEO_ID output.txt --lang it
```

Requires `yt-dlp` (`pip install yt-dlp`). The script takes manual or auto-generated subtitles, removes timestamps, tags and the repeated lines of auto-captions, and writes plain text. If YouTube still asks for a login, add `--browser chrome` (or `firefox`, `edge`) to use your browser's cookies. Exit code 3 means the video has no subtitles in that language.

## Visual exception

When charts, UI mockups or diagrams need to be **seen** (not just read as text), use the model's native image reading. The scripts above are only for text content in images.
