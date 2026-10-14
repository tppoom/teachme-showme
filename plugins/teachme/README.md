# TeachMe

> **Teach me so I get it — fast.**

One self-contained HTML course that makes you understand a subject quickly: short chapters,
each about one idea, each built around a concrete example you can see working.

```bash
claude plugin install teachme
```

**Two ways to run it.** `/teachme` (or just describe what you need) runs the skill in your
session — right for almost everything. `/teachme-cas` runs CAS mode (a planner, parallel
chapter authors and a reviewer) for big `deep` courses only.

## Why

AI-written courses tend to fail the same way: too many chapters, paragraphs that circle the
idea without landing it, boxes that repeat the prose, and almost no examples. You finish a
chapter and still couldn't explain it to anyone.

TeachMe is built the other way round:

- **Sized to the request.** "Explain X" is 1–4 chapters; a full course only when you ask for one.
- **Example first, then the idea.** Every chapter opens on a real case — numbers, a snippet,
  a situation — and names the rule once you've seen it work.
- **Pictures for mechanisms** — flows, sequences, timelines, comparisons, step-through code.
- **No filler.** No "in this chapter we will", no restating, no objectives-recap-glossary
  ceremony unless it earns its place.

## What you get

A single HTML file with a sidebar table of contents, progress saved in your browser, search,
light/dark, offline reading and print styles. Inside the chapters: worked examples, diagrams,
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
skills/teachme/
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
