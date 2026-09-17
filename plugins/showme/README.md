# ShowMe

> **SHOW only what matters — and have everything else ready.**

One self-contained HTML deck that behaves like real presentation software.

```bash
claude plugin install showme
```

## Why

Most generated decks fail the same way: everything the presenter knows gets poured onto the
slide, the audience starts reading, and they stop listening. Reading and listening compete for
the same channel.

ShowMe treats a deck as an **argument, not an outline**. Every slide carries one claim — a
sentence someone could disagree with — and the claims are written and ordered *before* any
slide exists. Nothing is cut; it is moved. The slide holds the claim and the one thing that
proves it, the speaker notes hold everything you would actually say, and the appendix holds the
answer you flip to when someone asks.

## The runtime

Fixed 1280×720 canvas scaled to fit any screen, so the layout is identical everywhere.
Keyboard and touch navigation, progressive builds, an overview grid, a **presenter window**
(`S`) that stays in step with the projector — notes, next slide, timer and a **pace clock**
that says how far ahead or behind your slot you are — a black screen (`B`), a **read mode** for
when the deck gets emailed instead of presented, print-to-PDF at exact slide size, deep links,
resume-where-you-were, and **auto-advance** with looping for Pecha Kucha and unattended screens.

Charts are SVG drawn from a real `<table>` in the page — bar, stacked, horizontal, line, area,
donut — with axes rounded to sensible values and bars that always start at zero.
`chart-table.py` turns a CSV straight into that table, so no number is ever retyped. Diagrams: flow, layers, 2×2
matrix, timeline, funnel, comparison. Sixteen inline SVG icons. Real images inline as data
URIs; when there is no image, an honest placeholder that says what belongs there.

## Looks like what you asked for

Fifteen complete themes — `keynote-dark`, `swiss`, `startup-pitch`, `corporate-clean`,
`editorial`, `academic`, `brutalist`, `midnight-data`, `terminal`, `soft-pastel`, `forest`,
`noir`, `mono-print`, `neon-gradient`, `clinical` — your own logo inlined into every footer,
and a reference that maps
style words ("clean", "premium", "punchy", "like an Apple keynote") onto concrete design
tokens, plus the rules that keep a deck from looking generated: one accent, one type scale, one
margin held across the whole deck, and layout that varies while the look never does.

## The discipline

`scripts/verify.py` fails the build on:

- a slide with no `data-claim`, or a claim that is really a topic
- a slide over its word ceiling for that layout
- more than five bullets, or a bullet longer than fourteen words
- a content slide with no speaker notes
- four slides in a row with the same shape
- a chart with more series than a room can read, or a stub image
- a slide promised in `STORYLINE.md` and never written
- a deck whose length does not fit the time slot it declares
- a `WRITE:` placeholder left behind by the chart helper

## Any occasion

Investor and sales pitches, thesis defences, conference talks, lectures, workshops, status
updates and board meetings, post-incident reviews, all-hands, launches, job-interview cases,
lightning talks, decks sent to be read, and unattended loops — each with a playbook: the spine
the room expects, the questions it always asks (built into the appendix), and the trap that
catches most decks made for it.

## Layout

```
skills/showme/
├── SKILL.md              workflow, the iron law, what it refuses to do
├── references/
│   ├── storyline.md      finding the argument; the claim ladder; moves; occasions
│   ├── slides.md         slide craft, layout choice, charts, images, builds
│   └── design.md         style brief → theme; the anti-generic rules
├── assets/
│   ├── shell.html        the deck runtime
│   ├── layouts.html      every layout and diagram, copy-paste ready
│   ├── themes.json       fifteen looks + the token contract
│   └── i18n.json         14 chrome languages, RTL handled
└── scripts/              new.py · assemble.py · verify.py · embed-image.py · chart-table.py
```

MIT
