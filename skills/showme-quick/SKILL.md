---
name: showme-quick
description: Quick ShowMe — builds the deck in this one session, no subagents. Builds a presentation as one self-contained HTML deck — fullscreen slides, builds, speaker notes with presenter view and timer, overview grid, read mode, print-to-PDF, charts from real data, fifteen themes. Use whenever someone has to present to an audience — "make me a deck", "slides for X", "turn this report/project/paper into a presentation", "I'm pitching on Friday", a defence, lecture, workshop, board or status update, incident review, lightning talk — or describes a room they must convince or brief without saying "slides". Also for decks that get emailed and read, looped on a screen, or restyled to a described look. For a long deck built by parallel agents with a reviewer, the user runs the /showme command.
---

# ShowMe — quick

> **SHOW only what matters — and have everything else ready.**

Produce **one self-contained HTML file** that presents like real presentation software:
a fixed canvas that fits any screen, keyboard/touch navigation, progressive builds, an
overview grid, a presenter window with notes, next slide and pace clock, read mode for decks
that get emailed, and clean print-to-PDF. Charts are drawn from data in the page, in a theme
chosen to match how the user said it should look.

Every occasion — a pitch, a thesis defence, an incident review, a cooking demo — is the same
problem: an audience, a limited number of minutes, and one thing they should leave with.

## What the user asked for comes first

The deck should look like **a good designer made it for this person, for this room** — not
like a template, and not like a machine. That means:

- **Their words decide.** The content they want in, the look they described ("minimal",
  "like our website", a colour, a reference deck), the length, the language, the tone. When
  their request and a default in this skill disagree, the request wins — record it in
  `meta.json` so the gate agrees.
- **Professional means fitting, not formal.** A wedding toast, a class for teenagers and a
  board review each have a right look. Choose it from the audience and occasion, and say what
  you chose.
- **Nothing generated-looking.** No icon on every card, no emoji, no label headlines
  ("Overview", "สรุป", "Thank you"), no gradients-on-everything, no invented numbers, no
  buzzwords. The full list and the alternatives: `references/design.md` → *The tells*.
- **No rendering bugs.** Nothing clipped, overlapping or wrapping mid-number; check the
  overview grid before handing over.

## The rule

```
THE SLIDE IS NOT THE DOCUMENT.
```

Reading and listening compete for the same channel, so the slide carries the **claim** and
the single thing that proves it. Everything else is *moved*, never deleted:

- **The slide** — the claim as the headline, plus one piece of evidence.
- **The speaker notes** — everything you would actually say.
- **The appendix** — the answer you flip to when someone asks.

`scripts/verify.py` enforces both directions: word ceilings on slides, a word floor on notes.
A FAIL means move content to the notes or appendix, split the slide, or cut it.

## Fit the deck to the request

The defaults serve a live talk. **The user's explicit wishes beat every default here** — do
what they asked, and record it in `meta.json` so the gate agrees.

**Delivery** (`meta.json` → `"delivery"`; scaffold with `--delivery`):

| Delivery | When | What changes |
|---|---|---|
| `live` (default) | presented in a room | standard ceilings (~55 words, 5 bullets) |
| `remote` | presented over a video call | same ceilings; bigger type, ≤ 3 builds per slide |
| `read` | emailed, pre-read, "send me the deck" | slides may carry ~1.8× the words; headlines must carry the argument alone; notes are written as prose paragraphs |
| `kiosk` | lobby loop, booth, event screen | notes optional; `"advance"` + `"loop": true`; one message per slide, readable in five seconds |

`"density": "sparse" | "normal" | "dense"` overrides the ceiling multiplier directly when the
user wants a different density than the delivery implies ("I want consulting-style dense
slides" → `dense`).

**Omit** (`meta.json` → `"omit"`): `notes`, `title`, `closing` — only when the user asked
("no speaker notes", "no title slide"). Each switches off its check.

**Slot** — roughly 1–2 minutes per main slide; put it in `"minutes"` and the gate checks it:

| Slot | Main slides |
|---|---|
| 5 min, lightning | 5–8 |
| 10 min | 8–14 |
| 20 min | 12–22 |
| 45 min lecture / workshop | 25–45, section divider every 6–8 |
| Pecha Kucha / Ignite | exactly 20, `"advance": 20` (or 15) |
| Kiosk loop | 6–12, `"advance"` 8–15, `"loop": true` |
| No slot (read) | 10–20 |

Backup slides do not count against the slot. When the material needs more than the slot
allows, move slides to the appendix and say which.

**Editable .pptx / Keynote / Google Slides required** (mandatory company template, colleagues
will edit) → this HTML output is the wrong format. Say so in one line and use a pptx skill if
one exists; still write `STORYLINE.md` first — the method here applies either way.

## Two ways to run it

- **This skill (`showme-quick`)** — one session, no subagents. Works in Claude Code, Codex and
  Antigravity. Fast and cheap; best for decks up to ~20 slides.
- **`/showme` (Claude Code command)** — the full build: a storyliner agent writes
  the claim ladder and picks the theme, builder agents write slide batches in parallel, and a
  reviewer agent checks the whole deck as the audience would see it. Best for long decks
  (lectures, workshops) and heavy source material. Suggest it for those when it is available.

## Workflow

`$SKILL` = the folder this SKILL.md lives in. Resolve it to an absolute path once (Claude Code
prints it when the skill loads; elsewhere, it is this file's directory) and call the scripts
from there. Track one todo per stage, plus one per slide batch in stage 4.

### 1 · Brief
Read everything they gave you, completely. Then settle these — from the request where it
says so, by deliberate choice where it doesn't — and state the ones you chose:

| | |
|---|---|
| **What they asked for** | their exact wishes — content that must be in, length, look, tone, anything they said no to. Quote them to yourself; every later choice is checked against this |
| **Audience** | who is in the room and what they already believe |
| **Spine** | the one sentence they repeat tomorrow |
| **Occasion** | what kind of event — find its row in `references/storyline.md` → *Occasions* |
| **Delivery + slot** | live / remote / read / kiosk, and minutes |
| **Look** | their style words, or your choice and why (`references/design.md`) |

**Confirm before writing the storyline — one round, then build.** Send one short message and
wait for the reply:

- **The brief, in at most five lines:** audience, the spine you intend, occasion, delivery and
  slot, look, language, where it will be saved, and anything you plan to leave out.
- **Questions only where the answer changes the deck** and neither the request nor the sources
  settle it — at most three, each with your recommended answer first. Use `AskUserQuestion`
  (or your environment's question tool); otherwise a numbered list. Usually: who is in the
  room, how it will be delivered, the look.
- **Nothing open?** Then it is a single choice: *start* / *adjust something*.

Skip it only when the user already said to go ahead without questions, or when you are
restyling or editing an existing deck. This is the one planned stop: after it, decide the rest
yourself and say what you chose.

**Where it goes:** the path they named; otherwise `./<slug>/` — or the parent / `~/Desktop/`
when the cwd is a repo you were not asked to modify. State the path. Then scaffold:
```bash
python3 $SKILL/scripts/new.py <dir> --title "…" --lang <code> --theme swiss --minutes 20 [--delivery read]
```
If a deck directory already exists, you are editing — see *Restyling and changing a deck*.

### 2 · Storyline
Write `STORYLINE.md`: the spine, then one **claim** per slide — a full sentence someone could
disagree with — each tagged with the layout that fits its shape. Method, narrative moves,
occasion playbooks and file format: **`references/storyline.md`**.

Done when: the claims read top to bottom as an argument, each layout is chosen from the shape
of its idea (`references/slides.md` → *Picking the layout*), no more than three in a row share
a shape, and the appendix holds the questions this room always asks. Show the claim list to
the user and continue — stop for approval only if they asked to review it, or the spine
changed from the one they confirmed.

### 3 · Design direction
Pick the theme from `assets/themes.json` using `references/design.md` (style words →
tokens, anti-generic rules), put it in `meta.json` with any logo path, and say the choice back
in one line.

### 4 · Build — batches of 4–6 slides
```
<dir>/parts/01-opening.html, 02-evidence.html, …
```
Copy layouts from **`assets/layouts.html`** (thirty working slides; the only class names the
runtime knows) and replace the content — grep it for the layouts the storyline names rather
than reading all of it. Craft — headline-as-claim, word ceilings, charts,
images, builds, notes: **`references/slides.md`**. Each slide needs an `id` matching
`STORYLINE.md`, a `data-claim`, and `.notes` (unless omitted).

Numbers from a file go through the script so they stay exactly as in the file:
```bash
python3 $SKILL/scripts/chart-table.py data.csv --type hbar --series share --unit % --top 5 --src "…"
```
Write each batch straight to its file, then check it:
```bash
python3 $SKILL/scripts/verify.py <dir> --part parts/NN-slug.html
```

### 5 · Assemble, gate, review, hand over
```bash
python3 $SKILL/scripts/assemble.py <dir>
python3 $SKILL/scripts/verify.py  <dir>          # final gate — no --wip
```
Then look at it — the gate cannot see layout:
```bash
node $SKILL/scripts/look.js <dir>      # every slide + grid.png; spills, auto-shrunk slides, tiny text
```
Fix every `LOOK` line in `parts/`. Then review as the audience: open `grid.png` from it (or
press `O` in the deck) — a deck that looks monotonous as a grid *is* monotonous — step
through two or three slides, and check one chart rendered. Look for anything clipped,
overlapping or wrapping badly, and for any of the generated-deck tells. Read only the
headlines in order: they should tell the whole argument. Then ask: is this what the user
asked for — their content, their look, their length?

Hand over: send the file (`SendUserFile` where it exists) or give the absolute path; report
slides, appendix slides, estimated minutes, theme, and anything moved to the appendix or left
out and why. Then the controls in one line: `←/→` navigate, `S` presenter window (drag the
original onto the projector, press `F` there), `N` notes, `B` black, `O` overview, `P` PDF.

## Surviving a long build

Decks fail like courses: the first six slides are considered, the last six are bullets.

- **`STORYLINE.md` and `parts/` are the memory.** After a compaction, read the storyline,
  `ls parts/`, resume at the first slide id with no file.
- **When you notice yourself reaching for bullets to finish faster, stop** and report how many
  slides are done. Half a considered deck beats a whole generic one.

## Restyling and changing a deck

- **`parts/` exists** → a restyle is a change to `theme` in `meta.json` plus re-assemble;
  slides are theme-independent by construction. A content change edits one part file.
- **Only `index.html` exists** → say plainly what you can preserve, offer to reconstruct
  `parts/` first, then re-theme.
- **A .pptx / .key / .pdf** → extract the content and build a new deck with the normal
  workflow; say that is what you did rather than implying a conversion.
- `index.html` is generated — edit `parts/`. Keep `deck_id` stable.

## Gotchas

| The thought | What to do instead |
|---|---|
| "Put the detail on the slide so they don't miss it" | They'll read instead of listen. Detail goes in notes and appendix. |
| "This slide needs six bullets" | Two slides, or four of the bullets become notes. |
| "The headline should name the topic" | Write the claim: "Growth came from the base, not the funnel". |
| "Bullets are fine here" | Ask what shape the idea is first — `slides.md` has the table. |
| "They didn't say how it should look" | You are choosing. Choose from audience and occasion, and say so. |
| "A colour per section" | One accent, one type scale, one margin. Vary layout, never look. |
| "The chart needs all twelve categories" | Top five plus "Other", or a table on purpose. |
| "A placeholder chart with plausible numbers" | Real numbers or the honest `.ph` placeholder — invented data is this skill's worst failure. |
| "Thank you / Questions? to close" | The closing slide states the ask: the decision, the action, or the idea to keep. |
| "Three cards with an icon each looks polished" | It looks generated. Pick the layout from the idea; icons only when they mean something. |
| "Add a stat row to make it look data-driven" | Only numbers from the source, each with its `.src`. |
| "My default style is fine — they didn't object" | Use what they described. If they described nothing, choose for the room and say why. |

Hard rules: one self-contained file (inline SVG and data URIs; the only network exception is
`fonts.url` when the user asked for a typeface — say it then needs the network); no
fabricated numbers, screenshots, quotes or citations; take the *attributes* of a reference
brand, never its logo or exact palette; slides in the user's language with `lang` set, names
and code left as they are.

## Quick reference

| Need | Where |
|---|---|
| The argument, claim ladder, narrative moves, occasion playbooks | `references/storyline.md` |
| Slide craft, layout choice, charts, images, builds, notes | `references/slides.md` |
| Style words → theme; anti-generic rules; brand; fonts | `references/design.md` |
| Every layout as a working slide | `assets/layouts.html` |
| Fifteen looks + token contract | `assets/themes.json` |
| Scaffold | `scripts/new.py <dir> --title … --theme … --minutes … [--delivery …]` |
| Check one batch / build / gate / look | `verify.py --part`, `assemble.py`, `verify.py`, `node look.js` |
| Chart from CSV, values untouched | `scripts/chart-table.py data.csv --type …` |
| Inline an image | `scripts/embed-image.py <img> "alt"` |

The runtime already provides — compose `layouts.html`, never rebuild: canvas scaling,
keyboard/swipe nav, builds, overview grid, presenter window synced across windows, pace
clock, notes panel, black screen, read mode, print-to-PDF, deep links, resume, auto-advance
and loop, logo, SVG charts (bar, stacked, hbar, line, area, donut) from a `<table>`, and
auto-fit for overflowing slides (a backstop — the gate still fails a slide that needed it).
