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

### Without the plugin system (Claude Code)

Copy either skill folder into `~/.claude/skills/`:

```bash
cp -R plugins/teachme/skills/teachme plugins/showme/skills/showme ~/.claude/skills/
```

## Install in Antigravity (AGY)

### In this workspace / project
Both skills are already configured in `.agents/` and will be automatically discovered by
Antigravity whenever you work in this repository. `.agents/` only points at
`plugins/*/skills/` — there is one copy of each skill in this repo, not two.

### Globally across all projects
Copy the skills into your global Antigravity / Gemini configuration directory:

```bash
mkdir -p ~/.gemini/config/skills
cp -R plugins/teachme/skills/teachme plugins/showme/skills/showme ~/.gemini/config/skills/
```

Or as plugins:

```bash
mkdir -p ~/.gemini/config/plugins
cp -R plugins/teachme plugins/showme ~/.gemini/config/plugins/
```

## Requirements

`python3` (already present on macOS and Linux) for the assemble and verify scripts. Nothing else.

## What each skill ships

**TeachMe** — topic, digest, codebase and exam modes; a sidebar with scroll-spy, per-chapter completion saved in `localStorage`, a
reading-progress bar, full-text search over the whole course, light/dark, copy-and-highlight
code, step-through `.walk` explanations, interactive quizzes with scoring, flashcard decks,
persistent checklists, MathML formulas with symbol legends and derivations, and print styles.
Two complete worked chapters in `assets/examples/` show the depth the gate demands.

**ShowMe** — a fixed canvas that scales to any screen, keyboard and touch navigation,
progressive builds, an overview grid, a presenter window synced to the projector with notes,
next slide, timer and pace clock, a black screen, a read-it-alone mode, auto-advance and
looping, print-to-PDF at the exact slide size, and SVG charts — bar, stacked, horizontal,
line, area, donut — drawn from a real `<table>` in the page, or straight from a CSV. Fifteen
themes, your own logo, a playbook for every kind of occasion, and thirty working slides in
`assets/layouts.html` that pass the gate as written.

Both runtimes auto-fit or wrap anything that would otherwise be clipped, so a long headline in
Thai or a translated label cannot silently lose its last line.

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
