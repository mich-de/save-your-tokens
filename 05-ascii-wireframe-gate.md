# 5. ASCII Wireframe Gate

Before any graphic output, front-end code (HTML, CSS, Tailwind, React), whiteboard layout or mobile view:

1. **Produce a lightweight ASCII diagram** of the layout.
2. **Iterate on the diagram only** — changes are cheap in ASCII, expensive in production code.
3. **Write production code after explicit user confirmation.**

## Why

- An ASCII sketch costs ~50 tokens. A React component costs 200–500.
- Iterating on code burns tokens on every revision cycle (read old code + write new code + re-read).
- The user can redirect the layout before a single line of CSS is written.

## Example

```
+----------------------------------+
| Header          [Logo]   [Menu]  |
+----------------------------------+
| Sidebar  | Main content          |
| - Nav 1  |                       |
| - Nav 2  | +--card--+ +--card--+ |
| - Nav 3  | | Title  | | Title  | |
|          | | Body   | | Body   | |
+----------+----------+-----------+
| Footer                           |
+----------------------------------+
```

Only after the user says "go" does the code get written.
