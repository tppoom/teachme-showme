---
name: showme
description: Use whenever someone has to present something to an audience — "make me a deck", "slides for X", "turn this into a presentation", "I'm pitching on Friday", "present this project/report/paper" — and also when they describe a room they must convince, brief, or report to without ever saying the word "slides". Covers any subject and any occasion. Use it too when they want an existing deck restyled to a look they describe.
---

# ShowMe

> **SHOW only what matters — and have everything else ready.**

## Overview

Produce **one self-contained HTML file** that presents like real presentation software:
fullscreen slides on a fixed canvas that fits any screen, keyboard and touch navigation,
progressive builds, an overview grid, a speaker-notes panel with a timer and next-slide
preview, a read-it-alone mode for when the deck gets emailed instead of presented, and clean
print-to-PDF. Charts and diagrams are drawn from data you can check, in a theme chosen to match
how the user said it should look.

**Nothing here is specific to a kind of talk or a kind of subject.** A thesis defence, a sales
pitch, a post-incident review and a cooking demo are the same problem: an audience, a limited
number of minutes, and one thing they should leave with.

## The Iron Law

```
THE SLIDE IS NOT THE DOCUMENT.
```

TeachMe's danger is a chapter that says too little. A deck's danger is the opposite and it is
the reason most decks are bad: everything the presenter knows gets poured onto the slide, the
audience starts reading, and they stop listening. Reading and listening compete for the same
channel.

So the discipline is subtraction on the slide and completeness underneath it:

- **The slide** carries the claim and the single thing that proves it.
- **The speaker notes** carry everything you would actually say. Every slide has them.
- **The appendix** carries the answer you flip to when someone asks.

Nothing is lost — it is *moved*. A deck with clean slides and empty notes is not a finished
deck; it is a deck whose content was deleted instead of relocated. `scripts/verify.py` enforces
both directions: word ceilings on slides, and a word floor on notes.

## When to use

- Any request for slides, a deck, a presentation, a pitch, a talk, a briefing, a readout
- Turning a document, report, paper, dataset or project into something presentable
- Restyling or rebuilding an existing deck to a described look
- Someone describes an audience they must convince or brief, without naming a format

**Do NOT use for:** teaching material meant to be studied alone (that is `teachme`), a written
document, or a question answerable in the chat. This skill produces a file to stand in front of.

## Workflow

Announce it, then run all five stages. One TodoWrite item per stage, plus one per slide batch
at stage 4.

### 1 · Brief
Read everything they gave you — completely. Then settle five things, from the request if it
says so and by choosing deliberately if it doesn't. State the ones you chose:

| | |
|---|---|
| **Audience** | who is in the room and what they already believe |
| **Spine** | the one sentence they repeat tomorrow |
| **Occasion** | present live, send to read, or both (the deck does all three; it changes the notes) |
| **Slot** | minutes — put it in `meta.json` as `"minutes"` |
| **Look** | what they said about style, or what you chose and why (`references/design.md`) |

Ask at most one round of questions, and only where the answer changes the deck. Everything else
you decide and say out loud.

### 2 · Storyline
Write `<deck-dir>/STORYLINE.md` — the claim ladder, before any slide exists. One claim per
slide, each a sentence someone could disagree with. Read the claims top to bottom: if they
don't argue, the deck won't either. **`references/storyline.md`** has the method, the composable
narrative moves, and the file format `verify.py` reads.

Show the user the claim list. It is far cheaper to fix the argument here than in HTML.

### 3 · Design direction
Pick the theme and write it into `meta.json` before building. `assets/themes.json` ships ten
complete looks; `references/design.md` maps style words ("clean", "premium", "punchy", "like an
Apple keynote") onto concrete tokens, and carries the rules that separate a designed deck from a
generic one. Say the choice back to the user in one line.

### 4 · Build — batches of slides, never the whole deck at once
```
<deck-dir>/parts/01-opening.html, 02-evidence.html, …
```
Markup contract: `assets/layouts.html` — every layout, every diagram, every chart, copy-paste
ready. Craft rules — headline-as-claim, word ceilings, picking the layout from the shape of the
idea, builds, images, notes: **`references/slides.md`**.

Slide `id` must match `STORYLINE.md`. `data-claim` is required. `.notes` is required.

### 5 · Assemble, verify, hand over
Claude Code prints **the skill's base directory** when it loads this skill — call the
scripts relative to that (`$SKILL/scripts/…`), so the skill works both from `~/.claude/skills/`
and from a plugin install. Substitute the real path when you run them.

```bash
python3 $SKILL/scripts/assemble.py <deck-dir>
python3 $SKILL/scripts/verify.py  <deck-dir> --wip   # after each batch
python3 $SKILL/scripts/verify.py  <deck-dir>         # final gate
```
Then open `index.html`, screenshot a few slides, press `O` for the overview and look at the
deck as a whole — that view is where a monotonous deck becomes obvious. Only then send it.
Tell them the shortcuts: `←/→` navigate, `O` overview, `N` notes, `F` fullscreen, `P` PDF.

## What each stage refuses to do

| The thought | The reality |
|---|---|
| "I'll put the detail on the slide so they don't miss it" | They will miss it — they will be reading it instead of listening. Notes and appendix exist for this. |
| "This slide needs six bullets" | Then it is two slides, or four of the bullets are notes. |
| "The headline should say the topic" | A topic makes the audience work out why they're looking. A claim hands them the point. |
| "Bullets are fine here" | Bullets are the fallback. Ask what shape the idea is and use `slides.md`'s table first. |
| "They didn't say how it should look" | Then you are choosing. Choose deliberately, from audience and occasion, and say so. |
| "I'll pick a nice colour for each section" | One accent, one type scale, one margin, held across the whole deck. Variety belongs in layout, not in look. |
| "A chart needs all twelve categories" | Beyond about five it is a table with extra steps. Aggregate or switch to a table on purpose. |
| "I'll make a placeholder chart with plausible numbers" | Never. Invented data in a deck someone will present is the worst failure mode this skill has. Use real numbers or the honest `.ph` placeholder. |
| "Speaker notes are optional" | They are where the completeness lives. Without them the deck is half-delivered. |
| "One more slide won't hurt the timing" | A 20-minute slot is about 10–20 slides. Past that you are choosing which slides to rush. |

## Red flags — stop and go back to the storyline

- A slide you cannot write a one-sentence claim for
- Four content slides in a row that look the same
- A headline that is a noun phrase
- Any number on a slide you have not verified, or any chart drawn from numbers you invented
- Reaching for a bullet list because the idea was hard to draw
- An empty `.notes`
- Relaxing `verify.py` instead of moving content into the notes

## Quick reference

| Need | Where |
|---|---|
| Finding the argument, the claim ladder, narrative moves | `references/storyline.md` |
| Slide craft, layout choice, charts, images, builds | `references/slides.md` |
| Turning a style brief into a theme; anti-generic rules | `references/design.md` |
| Every layout and diagram, copy-paste ready | `assets/layouts.html` |
| Ten complete looks + the token contract | `assets/themes.json` |
| Deck chrome in 14 languages (RTL handled) | `assets/i18n.json` |
| Build / gate | `scripts/assemble.py`, `scripts/verify.py` |
| Inline a real image as a data URI | `scripts/embed-image.py <img> "alt"` |

The runtime already provides: fixed-canvas scaling to any screen, `←/→/space` and swipe
navigation, progressive builds, overview grid, speaker-notes panel with timer and next-slide
preview, read mode, print-to-PDF at exact slide size, deep links (`#7`), resume where you left
off, and SVG charts drawn from a real `<table>`. **Do not rebuild these and do not invent class
names** — compose what is in `layouts.html`.

## Common mistakes

- **Building slides before the storyline exists.** You end up with a slide per topic instead of
  a slide per claim, and no amount of design fixes that.
- **Emitting the whole deck in one pass.** Quality collapses halfway. Batches of 4–6 slides.
- **External assets.** No CDN, no remote images, no chart library. Inline SVG and data URIs;
  the one allowed exception is `fonts.url` when the user asked for a specific typeface — and
  say out loud that it makes the deck need the network on first open.
- **Inventing evidence.** No fabricated numbers, no fake screenshots, no made-up quotes or
  citations. If the data isn't there, the slide says what is missing.
- **Presenting someone else's brand as the user's.** Take the attributes of a reference deck,
  never its logo, wordmark, or exact palette.
- **Wrong language.** Write the slides in the language the user is writing in and set `lang` so
  the chrome matches. Keep names, code, commands and quoted sources in their original form.
