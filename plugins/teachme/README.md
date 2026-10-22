# TeachMe

> **Teach me so I get it — fast.**

One self-contained HTML course that makes you understand a subject quickly: short chapters,
each about one idea, each built around a concrete example you can see working.

```bash
claude plugin install teachme
```

**Two ways to run it.** `/teachme` runs the full build: a planner, parallel chapter authors
with fresh context, a reader who goes through every chapter cold and sends weak ones back,
and a reviewer. `/teachme-quick` (or just
describe what you need) builds it in one session — faster, fewer tokens, right for short
courses and explainers.

## Why

AI-written courses tend to fail the same way: too many chapters, paragraphs that circle the
idea without landing it, boxes that repeat the prose, and almost no examples. You finish a
chapter and still couldn't explain it to anyone.

TeachMe is built the other way round:

- **Sized to the request.** "Explain X" is 1–4 chapters; a full course only when you ask for one.
- **Example first, then the idea.** Every chapter opens on a real case — numbers, a snippet,
  a situation — and names the rule once you've seen it work.
- **Depth where it's hard.** The words go to the part you'd get stuck on — the mechanism, the
  *why*, the step beginners get wrong — in full sentences. Setup, run logs and every-option
  lists get a line or nothing.
- **Pictures for mechanisms** — flows, sequences, timelines, comparisons, step-through code.
- **No filler.** No "in this chapter we will", no restating, no objectives-recap-glossary
  ceremony unless it earns its place.

## What you get

A single HTML file that reads like a well-made book: a contents page grouped into parts, one
chapter on screen at a time with a clear way on to the next, a Thai-and-Latin reading font
built in (it looks the same offline), progress saved in your browser, search, light/dark and
print styles. Inside the chapters: worked examples, diagrams,
step-through walkthroughs that highlight the code line under discussion, MathML formulas with
symbol legends, vocabulary tables, flashcards, checklists, and optional quick checks that
explain why each wrong answer is tempting.

## The gate

`scripts/verify.py` checks the course before it is handed over:

- **Fails** anything that would render broken — Markdown left in the HTML, code swallowed as
  tags, unbalanced markup, external resources, duplicate ids, malformed quizzes and widgets.
- **Fails** a chapter with no concrete example (worked example, code with output, figure,
  comparison or table).
- **Warns** on padding — chapters past their length budget, filler phrases (English and Thai),
  stacked boxes, too many chapters for the depth, and paragraphs left in the wrong language.

## Inputs

**A topic** — "explain how HTTPS works". **Your material** — slides, PDFs or notes turned into
chapters that say what the lecturer would say. **A codebase** — what it does, the flows that
matter traced through real files, and where it stands. **An exam** — chapters weighted by marks,
practice in the exam's own format.

## Layout

```
skills/teachme-quick/
├── SKILL.md              workflow and sizing
├── references/
│   ├── writing.md        chapter recipe, examples, the cut list, quizzes, input types
│   └── visuals.md        which visual for which idea; SVG rules
├── assets/
│   ├── shell.html        the reader app: CSS, JS, every component
│   ├── blocks.html       every block's markup
│   ├── examples/         one chapter in the target style
│   └── i18n.json         14 interface languages
└── scripts/              new.py · assemble.py · verify.py · embed-image.py
```

MIT
