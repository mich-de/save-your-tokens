# 14. OpenCode Free Models

When running in OpenCode, list free models with a deterministic query — never by browsing.

## Commands

### Bash
```bash
opencode models --refresh | grep -iE "free|opencode/"
```

Or for models with explicit $0 pricing:
```bash
opencode models --verbose | grep -B 5 -A 5 -E '"input":\s*0(\.0+)?\b'
```

### PowerShell
```powershell
opencode models | Select-String -Pattern "free"
```

### Python (exact $0/$0 from models.dev)
```bash
python scripts/list_free_models.py
```

This script reads `https://models.dev/api.json` and keeps only models where `cost.input == 0` and `cost.output == 0`. It separates models with "free" in the name from those that just report zero cost (which may mean local, BYOK, or unpublished pricing).

### Interactive
In OpenCode: `/models`, filter by `free`.

## Quota limits

Free-tier limits are real. At 90% of the session quota, warn the user and stop heavy work.
