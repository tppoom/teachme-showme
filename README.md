# claude-skills

Two Claude Code skills that turn a request into **one self-contained HTML file** — no build
step, no dependencies, no network. Open it, keep it, send it.

| Skill | Produces | Use it when |
|---|---|---|
| **[TeachMe](plugins/teachme)** | A complete course you study from | You want to actually learn something, not get an answer |
| **[ShowMe](plugins/showme)** | A deck you present from | You have to present to a room |

They are siblings with opposite disciplines. TeachMe's gate fails a chapter that says **too
little**. ShowMe's gate fails a slide that says **too much**. Both refuse to ship placeholder
text, invented citations, or content promised in the outline and never written.

## Install

```bash
claude plugin marketplace add tppoom/claude-skills
```

```bash
claude plugin install teachme
```

```bash
claude plugin install showme
```

Then start a new Claude Code session and type `/teachme` or `/showme` — or just describe what
you need and the skill triggers itself.

Updating later:

```bash
claude plugin marketplace update tppoom-skills
```

### Without the plugin system

Copy either skill folder into `~/.claude/skills/`:

```bash
cp -R plugins/teachme/skills/teachme plugins/showme/skills/showme ~/.claude/skills/
```

## Requirements

`python3` (already present on macOS and Linux) for the assemble and verify scripts. Nothing else.

## What "self-contained" means

The output is a single `.html` file. No CDN, no `<script src>`, no remote images, no chart
library. Diagrams are hand-authored SVG or CSS, charts are drawn from a real `<table>` in the
page, images are inlined as data URIs, formulas use native MathML. It opens on a plane, it
still opens in five years, and you can email it to someone who has none of this installed.

## Languages

Both ship complete interface translations for **en · th · ja · zh · ko · es · fr · de · pt ·
ru · id · vi · hi · ar**, with automatic RTL layout. Word counts are script-aware, so a
Japanese or Thai course is not mistaken for a stub. Code, commands, error messages and quoted
sources are never translated.

## Licence

MIT
