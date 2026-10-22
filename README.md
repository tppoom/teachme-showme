# teachme-showme

Two agent skills that turn a request into **one self-contained HTML file** — no build step, no
dependencies, no network. Open it, keep it, send it.

| Skill | Produces | Use it when |
|---|---|---|
| **[TeachMe](skills/teachme-quick)** | A short course that makes you understand, fast | You want to actually get something, not just an answer |
| **[ShowMe](skills/showme-quick)** | A deck you present from | You have to present to a room |

Both share one discipline: **words go where understanding is made.** TeachMe teaches each
idea through a concrete worked example, spends its words on the part the reader finds hard —
the mechanism, the *why*, the step beginners get wrong — and keeps run logs, ids and every-option
lists out of the way; its gate fails a chapter with no example and warns on padding,
figure-dense prose and note-like bullets. ShowMe puts one claim and one piece of evidence on each slide, and its gate fails a
slide that says too much and warns on the patterns that make a deck look machine-made. Both
gates also fail anything that would render broken — stray Markdown, code swallowed as tags,
clipped or overflowing content — and both refuse placeholder text and invented numbers.

Both follow the open [Agent Skills](https://agentskills.io) format (`SKILL.md` + `scripts/` +
`references/` + `assets/`), so they work the same in **Claude Code**, **Codex CLI** and
**Antigravity** — anything that reads that format.

## Two ways to run each

| | Full — `/teachme`, `/showme` | Quick — `teachme-quick`, `showme-quick` |
|---|---|---|
| **Start it** | `/teachme <topic>`, `/showme <talk>` | `/teachme-quick`, `/showme-quick` — or just describe what you need |
| **How it works** | **Command → Agent → Skill**: an orchestrator command interviews you, a planner agent writes the contract (`SYLLABUS.md` / `STORYLINE.md` + a shared `BRIEF.md`), author agents write chapters or slide batches **in parallel, each with a fresh context**, a reader agent with fresh context goes through it cold as the learner/audience and sends weak chapters or slides back, and a reviewer makes it one piece | One session follows the skill end to end — no subagents, fewer tokens, faster |
| **Best for** | Big jobs and the most careful result — deep courses, long lectures and workshops, heavy source material | Explainers, short courses, decks up to ~20 slides |
| **Asks you** | Once: the brief and only what would change the result; the plan is re-asked only if it departs from it | Once: the brief it understood and only what would change the result |
| **Works in** | Claude Code | Claude Code, Codex CLI, Antigravity |

The full mode follows the pattern from
[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
(orchestration workflow): the command owns user interaction, each agent preloads the skill as
its standard via `skills:` in its frontmatter, and the skill holds the method, scripts and
gate both modes share (that is why the skills carry the `-quick` name: a skill and a command
cannot share one). Agents: `teachme-planner` · `teachme-author` · `teachme-reader` ·
`teachme-reviewer` and `showme-storyliner` · `showme-builder` · `showme-audience` ·
`showme-reviewer`.

## Fitting the output to the request

Both gates read `meta.json`, so "I just want a short explainer" or "no speaker notes" is a
setting, not a fight with the checker. The user's explicit wishes beat the skill's defaults.

| | Setting | Values |
|---|---|---|
| TeachMe | `"depth"` | `quick` (1–4 chapters) · `standard` (3–8, default) · `deep` (6–16, a full course) |
| TeachMe | `"omit"` | `quiz` `exercise` `visual` `appendix` |
| ShowMe | `"delivery"` | `live` · `remote` (video call) · `read` (emailed — ~1.8× words per slide) · `kiosk` (loop, no notes) |
| ShowMe | `"density"` | `sparse` · `normal` · `dense` |
| ShowMe | `"omit"` | `notes` `title` `closing` |

Both `verify.py` scripts also take `--part parts/NN-slug.html` to check one chapter or slide
batch on its own — which is what lets the `/teachme` and `/showme` agents work in parallel without assembling.

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
those you have installed — plus, for Claude Code, the `/teachme` and `/showme` commands into `~/.claude/commands/`
and the agents into `~/.claude/agents/` (skip those with `./install.sh --skills-only`). Safe to re-run; `git pull` here keeps every install current since
they're symlinks, not copies. See the header comment in `install.sh` for exactly what it
touches; to undo, just delete the symlink it created — nothing else was written.

### Claude Code, via the plugin marketplace

If you'd rather manage it through Claude Code's own plugin system (versioned, one-line update):

```bash
claude plugin marketplace add tppoom/teachme-showme
claude plugin install teachme
claude plugin install showme
```

Then start a new session and type `/teachme` or `/showme` for the full build (namespaced as
`/teachme:teachme` and `/showme:showme` if another plugin uses the same name), or
`/teachme-quick` / `/showme-quick` for the quick one — or just describe what you need and the
quick skill triggers itself. Update later with:

```bash
claude plugin marketplace update teachme-showme
```

### Manual copy (any tool, no symlinks)

Every skill is a self-contained folder — copy it wherever your tool reads skills from:

```bash
cp -R skills/teachme-quick skills/showme-quick ~/.claude/skills/   # Claude Code, personal
cp cas/*/commands/*.md ~/.claude/commands/               # Claude Code, /teachme and /showme
cp cas/*/agents/*.md   ~/.claude/agents/
cp -R skills/teachme-quick skills/showme-quick ~/.agents/skills/   # Codex CLI, personal
```

For Antigravity's current global path, check `antigravity.google/docs/` — it has moved more
than once as the product evolves; the project-level `.agents/skills/` in this repo is the
reliable one and needs no configuration.

## Requirements

`python3` (already present on macOS and Linux) for the assemble and verify scripts. Nothing else.

## What each skill ships

**TeachMe** — short, example-first chapters from a topic, your notes/slides, a codebase or an
exam blueprint; worked-example blocks, a sidebar with scroll-spy, per-chapter completion saved
in `localStorage`, a reading-progress bar, full-text search, light/dark, copy-and-highlight
code, step-through `.walk` explanations, optional quick-check quizzes that explain each wrong
answer, flashcards, checklists, MathML formulas with symbol legends, and print styles. One
chapter in `assets/examples/` shows the target style.

**ShowMe** — a fixed canvas that scales to any screen, keyboard, swipe and tap navigation,
progressive builds, an overview grid, a presenter window synced to the projector with notes,
next slide, timer and pace clock, a black screen, a read-it-alone mode, auto-advance and
looping, print-to-PDF at the exact slide size, and SVG charts — bar, stacked, horizontal,
line, area, donut — drawn from a real `<table>` in the page, or straight from a CSV. Fifteen
themes, your own logo, a playbook for every kind of occasion, and thirty working slides in
`assets/layouts.html` that pass the gate as written.

Both runtimes auto-fit or wrap anything that would otherwise be clipped, so a long headline in
a script without spaces or a translated label cannot silently lose its last line.

## What "self-contained" means

The output is a single `.html` file. No CDN, no `<script src>`, no remote images, no chart
library. Diagrams are hand-authored SVG or CSS, charts are drawn from a real `<table>` in the
page, images are inlined as data URIs, formulas use native MathML. It opens on a plane, it
still opens in five years, and you can email it to someone who has none of this installed.

## Languages

Both write in the language you ask in — or whichever one you ask for — and the interface
follows it: fourteen languages ship complete translations in each skill's `assets/i18n.json`,
any other is one translated key block away, and right-to-left languages mirror the layout
automatically. Word counts are script-aware, so a course in a language written without spaces
is not mistaken for a stub. Code, commands, error messages and quoted
sources are never translated.

## Layout

```
teachme-showme/
├── skills/                the real content — one copy of each skill, everything else
│   ├── teachme-quick/     points here via a symlink
│   └── showme-quick/
├── cas/                   the full mode (Claude Code): one orchestrator command + three agents each
│   ├── teachme/           commands/teachme.md · agents/teachme-{planner,author,reviewer}.md
│   └── showme/            commands/showme.md · agents/showme-{storyliner,builder,reviewer}.md
├── .claude/skills/        symlinks → skills/*   (Claude Code, this repo open as a project)
├── .claude/commands/      symlinks → cas/*/commands/*.md
├── .claude/agents/        symlinks → cas/*/agents/*.md
├── .agents/skills/        symlinks → skills/*   (Codex CLI, Antigravity — same open standard)
├── plugins/               Claude Code plugin packaging (marketplace install)
│   ├── teachme/           plugin.json + skills/teachme-quick → ../../../skills/teachme-quick,
│   │                      commands/ → ../../cas/teachme/commands, agents/ → ../../cas/teachme/agents
│   └── showme/
├── install.sh             personal/global install for whichever agents you have
└── .claude-plugin/marketplace.json
```

One real copy of each skill, at `skills/<name>/`, and of each command and agent, at `cas/`. Everything else — the plugin folders, the
project-level agent directories — is a symlink to it, so there is nothing to keep in sync by
hand and no risk of one copy silently drifting from another.

## Licence

MIT
