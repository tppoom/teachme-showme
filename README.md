# teachme-showme

Two agent skills that turn a request into **one self-contained HTML file** — no build step, no
dependencies, no network. Open it, keep it, send it.

| Skill | Produces | Use it when |
|---|---|---|
| **[TeachMe](skills/teachme)** | A complete course you study from | You want to actually learn something, not get an answer |
| **[ShowMe](skills/showme)** | A deck you present from | You have to present to a room |

They are siblings with opposite disciplines. TeachMe's gate fails a chapter that says **too
little**. ShowMe's gate fails a slide that says **too much**. Both refuse to ship placeholder
text, invented citations, or content promised in the outline and never written.

Both follow the open [Agent Skills](https://agentskills.io) format (`SKILL.md` + `scripts/` +
`references/` + `assets/`), so they work the same in **Claude Code**, **Codex CLI** and
**Antigravity** — anything that reads that format.

## Install

**Just want to try them?** Clone this repo and open the folder in Claude Code, Codex or
Antigravity. Nothing else to do — `.claude/skills/` and `.agents/skills/` in this checkout
already point at the real skill folders, so both tools discover TeachMe and ShowMe the moment
they open the project.

```bash
git clone https://github.com/tppoom/teachme-showme.git
cd teachme-showme
```

**Want them in every project, not just this one?** Run the installer once:

```bash
./install.sh
```

It links `~/.claude/skills/`, `~/.agents/skills/` (Codex, and any other tool that reads the
shared personal path) and Antigravity's global skills folder to this checkout, whichever of
those you have installed. Safe to re-run; `git pull` here keeps every install current since
they're symlinks, not copies. See the header comment in `install.sh` for exactly what it
touches; to undo, just delete the symlink it created — nothing else was written.

### Claude Code, via the plugin marketplace

If you'd rather manage it through Claude Code's own plugin system (versioned, one-line update):

```bash
claude plugin marketplace add tppoom/teachme-showme
claude plugin install teachme
claude plugin install showme
```

Then start a new session and type `/teachme` or `/showme` — or just describe what you need and
the skill triggers itself. Update later with:

```bash
claude plugin marketplace update teachme-showme
```

### Manual copy (any tool, no symlinks)

Every skill is a self-contained folder — copy it wherever your tool reads skills from:

```bash
cp -R skills/teachme skills/showme ~/.claude/skills/     # Claude Code, personal
cp -R skills/teachme skills/showme ~/.agents/skills/     # Codex CLI, personal
```

For Antigravity's current global path, check `antigravity.google/docs/` — it has moved more
than once as the product evolves; the project-level `.agents/skills/` in this repo is the
reliable one and needs no configuration.

## Requirements

`python3` (already present on macOS and Linux) for the assemble and verify scripts. Nothing else.

## What each skill ships

**TeachMe** — topic, digest, codebase and exam modes; a sidebar with scroll-spy, per-chapter
completion saved in `localStorage`, a reading-progress bar, full-text search over the whole
course, light/dark, copy-and-highlight code, step-through `.walk` explanations, interactive
quizzes with scoring, flashcard decks, persistent checklists, MathML formulas with symbol
legends and derivations, and print styles. Two complete worked chapters in `assets/examples/`
show the depth the gate demands.

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

## Layout

```
teachme-showme/
├── skills/                the real content — one copy of each skill, everything else
│   ├── teachme/           points here via a symlink
│   └── showme/
├── .claude/skills/        symlinks → skills/*   (Claude Code, this repo open as a project)
├── .agents/skills/        symlinks → skills/*   (Codex CLI, Antigravity — same open standard)
├── plugins/               Claude Code plugin packaging (marketplace install)
│   ├── teachme/           plugin.json + skills/teachme → symlink → ../../../skills/teachme
│   └── showme/
├── install.sh             personal/global install for whichever agents you have
└── .claude-plugin/marketplace.json
```

One real copy of each skill, at `skills/<name>/`. Everything else — the plugin folders, the
project-level agent directories — is a symlink to it, so there is nothing to keep in sync by
hand and no risk of one copy silently drifting from another.

## Licence

MIT
