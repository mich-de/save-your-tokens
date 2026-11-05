# 12. Anti-Patterns and Output Style

## Anti-patterns

| Don't | Do instead |
|---|---|
| Use `/compact` or auto-compact | Write `HANDOFF.md` + `/clear` |
| Skip the checkpoint handoff | Always write `HANDOFF.md` at milestones |
| Send raw screenshots of text to the model | Run `extract_image_ocr.py` first |
| Read text PDFs natively | Run `extract_pdf.py` first |
| Write ultra-short ambiguous prompts when delegating | Write complete prompts with full context |
| Stack corrective prompts after errors | Use `/rewind` |
| Chain long tasks without checkpoints | Break at milestones, `/clear` between them |

## Output style

- **Concise**: lead with the result, skip preamble and narration.
- **No ceremony**: no "Sure!", "Let me", "I'll now", "Hope this helps".
- **Answer first**: result, then reasoning, then next step.
- **Caveman mode** (optional): the user can enable it for maximum compression. Technical substance stays, only fluff dies. If the user chose it, respect it.
