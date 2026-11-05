# 9. Graph Navigation

Code graphs help navigate large codebases but have overhead. Use them only when they save more than they cost.

## Rules

| Codebase size | Action |
|---|---|
| Below 500 files | No graph — it costs more than it saves. Use `Grep` and `Glob`. |
| Above 500 files, software repo | CodeGraph: `npm i -g @colbymchenry/codegraph`, then `codegraph install` and `codegraph init` in the repo root. |
| Above 500 files, notes/docs/PDF/images | `graphify` skill (`/graphify`). |
