# 4. HANDOFF.md Protocol

`HANDOFF.md` is the file that carries state between sessions. It lives in the project root and has 6 mandatory sections.

## Sections

### 1. Objective
The goal of the session and the current checkpoint.

### 2. Current State
The exact point reached — what works, what's deployed, what's been verified.

### 3. Failed Attempts & Problems Solved
What did not work, and the exact fixes. This prevents the next session from re-trying dead ends.

### 4. Decisions Taken
Architecture choices, logic decisions, reversing findings, style conventions. Anything the next session needs to respect.

### 5. Files Touched
Created or modified paths in this session.

### 6. Next Steps
Actionable queue for after `/clear`. Ordered by priority.

## Example

```markdown
# HANDOFF — project name (2026-11-05)

## 1. Objective
Build the admin panel for the dashboard app.

## 2. Current State
- Auth middleware done and tested.
- Dashboard layout skeleton pushed to `main`.
- API routes for `/api/users` and `/api/settings` working.

## 3. Failed attempts / problems solved
- NextAuth v5 beta had a CSRF bug with the custom adapter — downgraded to v4.
- `prisma generate` failed on Windows due to path length — moved `.prisma` to a shorter path.

## 4. Decisions taken
- Prisma over Drizzle (team already uses it).
- Server components for all data-fetching pages; client components only for interactive forms.

## 5. Files touched
`src/middleware.ts`, `src/app/admin/layout.tsx`, `prisma/schema.prisma`, `src/app/api/users/route.ts`

## 6. Next steps
1. Build the user list table with pagination.
2. Add role-based access to admin routes.
3. Write tests for the auth middleware.
```

## When to write it

- At every completed milestone.
- When context hits 40–50%.
- Before any `/clear`.
- The agent writes it autonomously — the user should never have to ask.
