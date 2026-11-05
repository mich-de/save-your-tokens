# 10. Deterministic Code Conversion

> "AI is for judgment; everything else is repeatable execution, and repeatable execution must be code."

## Principle

Keep LLM calls only where **semantic judgment** is needed — deciding what to do, understanding ambiguous requirements, reviewing code for correctness.

Turn everything else into Python/Bash scripts and hooks:

- Data transformation → script
- File renaming/moving → script
- "Always do X when Y" → hook
- Formatting, linting → pre-commit hook
- Deployment steps → CI/CD pipeline
- Repeated checks → scheduled script

## Why

- A script runs the same way every time. A prompt might not.
- A script costs zero tokens. A prompt costs tokens on every run.
- A script is testable and version-controlled. A prompt lives only in conversation.

## Example

Bad: asking the model to reformat 50 JSON files every time.

Good: writing `scripts/reformat_json.py` once and running it from a hook or CI.
