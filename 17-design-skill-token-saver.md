# 17. Design Skill in Token-Saver Mode

Use one design skill, load it only for UI work, and spend tokens on the decision, not on iterations.

## Which skill

**`frontend-design`** (Anthropic's official skill) is the most installed design skill for Claude Code. Aggregators report roughly 560k to 790k installs, far ahead of the alternatives. Exact numbers differ by source and date, so treat them as approximate.

| Skill | Role | Use when |
|---|---|---|
| `frontend-design` | Default. Pushes distinctive typography, color, layout and motion instead of generic AI output. | Any new page, component or layout. |
| `ui-ux-pro-max` | Data banks of styles, palettes, fonts and UX rules. | You need a palette or style choice backed by data. |
| `impeccable` | Heavier pipeline with reviewers and asset producers. | A large build that needs a final quality review. |

Default to `frontend-design`. Add a second skill only when the first cannot answer the question.

## Token-saver rules

1. **Wireframe first.** Follow [step 5](05-ascii-wireframe-gate.md): draw the ASCII layout and wait for confirmation before any HTML, CSS or React.
2. **Load on demand.** Invoke the design skill only when the task is UI. Never keep it loaded for backend or data work.
3. **Decide the direction once.** State palette, font pair, spacing scale and tone in 5 lines at the start. Write them to a short `DESIGN.md` and reuse it in later sessions instead of re-deriving them.
4. **One pass, then targeted edits.** Generate the full page once. Fix problems with small edits to the affected block, never by regenerating the page.
5. **No variant fishing.** Ask for one design, not three options. Variants triple the cost and rarely beat a good first brief.
6. **Look at the output once.** One screenshot after the build, one after the fixes. Screenshot loops burn context fast.
7. **Mid-tier model, medium effort.** Design implementation does not need the top model. See [step 2](02-model-routing.md).
8. **Tokens in a file.** Keep colors, fonts and spacing as CSS variables in one place, so later edits touch one file and not every component.
9. **Stop at "good".** Define done in the brief (for example: responsive at phone width, readable contrast, no layout shift). Stop when those hold.

## Minimal brief template

```
Task: <page or component>
Skill: frontend-design
Direction: <tone>, <palette>, <font pair>, <spacing scale>
Constraints: mobile first, contrast AA, no extra dependencies
Wireframe: <approved ASCII from step 5>
Done when: <3 checks>
```

## Sources

- [Skillselion design hub](https://skillselion.com/design)
- [frontend-design guide](https://skillselion.com/guides/frontend-design-skill-claude-code-guide)
- [ui-ux-pro-max guide](https://skillselion.com/guides/how-to-use-ui-ux-pro-max-skill)
