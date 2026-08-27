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

## Before you build

Three decisions, made in your first message rather than discovered by correction later.

**Where it goes.** The user named a place → use it. Otherwise `./<slug>/` in the current
working directory — **except** when the cwd is a repo you were not asked to modify; use the
parent or `~/Desktop/` and say which. State the path up front.

Scaffold it rather than hand-building the shape:
```bash
python3 $SKILL/scripts/new.py <dir> --title "…" --lang th --theme swiss --minutes 20
```

**How long.** Roughly 1–2 minutes per main slide, and the gate checks it against `minutes`.

| Slot | Main slides |
|---|---|
| 5 min, lightning | 5–8 |
| 10 min | 8–14 |
| 20 min | 12–22 |
| 45 min lecture or workshop | 25–45, with a section divider every 6–8 |
| No slot — sent to be read | 10–20; the notes carry proportionally more |

Backup slides do not count against the slot. When the material genuinely needs more than the
slot allows, the answer is the appendix, not a faster delivery — say which slides you moved
there and why.

**New or existing.** If a deck directory already exists, you are editing — jump to
*Restyling and changing a deck*.

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
A FAIL means move content into the notes or the appendix, split the slide, or cut it — never
loosen the check. What "done" means is in *Handing it over* below; a passing gate is only the
first of its five steps.

## Surviving a long build

A deck is less text than a course but more design decisions, and it fails the same way: the
first six slides are considered, the last six are bullet lists because the model is trying to
finish. Beat it with process.

- **Write slides straight to their part files**, four to six per turn. Never draft slides in
  your reply and then save them.
- **`STORYLINE.md` is the source of truth.** Re-read it for the next claim instead of
  remembering the plan.
- **Checkpoint after every batch** with assemble + `verify.py --wip`.
- **If your context is compacted mid-build**, recovery is mechanical: read `STORYLINE.md`,
  `ls <dir>/parts/`, resume at the first slide id with no file.
- **Look at the overview grid before you call it done.** Press `O`. A deck that reads fine
  slide by slide and looks monotonous as a grid is monotonous — the grid is the only view that
  shows you what the audience experiences over twenty minutes.
- **If you catch yourself reaching for bullets to finish faster, stop** and say how many slides
  are done. Half a considered deck plus an honest outline beats a whole generic one.

## Restyling and changing a deck

- **`parts/` exists** → for a restyle, change the `theme` block in `meta.json` and re-assemble.
  That is the entire job: slides are theme-independent by construction, which is why the theme
  lives in one place. For a content change, edit the one part file.
- **Only `index.html` exists** — built by hand, or by someone else, or by an earlier session
  whose parts are gone → you can re-theme by replacing the token block, but say plainly what
  you can and cannot preserve before touching it, and offer to reconstruct `parts/` from it so
  future edits are cheap.
- **A .pptx, .key or .pdf** → this skill builds a new deck from the content; it does not
  convert files and will not preserve their layout. Extract the content, run the normal
  workflow, and say that is what you did rather than implying a conversion.
- **Never hand-edit `index.html`** — it is generated and the next assemble overwrites it.
  Keep `deck_id` stable so "resume where you were" survives.

## Handing it over

Done means all of this, in order — not "the files exist".

1. `verify.py` passes **without** `--wip`
2. You opened `index.html`, pressed `O`, and looked at the whole deck as a grid
3. You stepped through two or three slides in present mode and checked a chart rendered
4. You sent the file with `SendUserFile`, or gave the exact path if you cannot
5. You reported the real shape — slides, appendix slides, estimated minutes, theme — and named
   anything you moved to the appendix or left out, with the reason

Then one line of controls: `←/→` navigate, `O` overview, `N` speaker notes and timer, `F`
fullscreen, `P` to save a PDF. Do not narrate the build.

## What a run looks like

> **User:** ทำสไลด์เสนอโปรเจกต์ให้อาจารย์หน่อย 15 นาที เอาแบบสะอาดๆ ไม่ต้องหวือหวา

1. **Brief** — audience is one advisor who knows the field; spine is "the pipeline is the
   contribution, not the UI"; 15 minutes → about 12 main slides; "สะอาดๆ ไม่หวือหวา" → `swiss`,
   rule motif. Say all of that back in two lines and start.
2. **Storyline** — 12 claims + 3 appendix slides for the questions an advisor always asks
   (dataset size, evaluation, what is novel). Show the claim list.
3. **Design** — scaffold with `--theme swiss --minutes 15`.
4. **Build** — `parts/01-open.html` … four to six slides per turn, `--wip` after each batch.
5. **Final gate** — clean, press `O`, fix the two bullet slides sitting next to each other.
6. **Hand over** — `SendUserFile` + *"12 สไลด์ + ภาคผนวก 3 · ธีม swiss · ~15 นาที · กด N ดูโน้ต
   ผู้พูดพร้อมจับเวลา"*

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
| Scaffold a deck directory | `scripts/new.py <dir> --title … --theme … --minutes …` |
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
