# TeachMe

> **TEACH me everything I HAVE to know.**

One self-contained HTML course that teaches a subject completely — not just what you asked,
but everything you need in order to understand what you asked.

```bash
claude plugin install teachme
```

## Why

Ask an AI to teach you something and you get an answer: short, correct, and full of holes you
cannot see. It skips what you needed to know first, and it never tells you what to learn next.
Paid courses stop halfway. Lecture slides are headings without the lecture.

TeachMe treats the request as a **destination, not a scope**. It expands along five axes —
what you must know first, the subject itself, the full mechanical detail, how it is really
used, and what surrounds it — writes that out as a syllabus, and then treats the syllabus as a
contract that a script enforces.

## What you get

A single HTML file with a sidebar table of contents, per-chapter completion saved in your
browser, a progress bar, full-text search, light/dark, and offline reading. Inside the
chapters: diagrams, sequence and timing charts, step-through walkthroughs that highlight the
code line under discussion, MathML formulas with symbol legends and derivations, vocabulary
tables with ruby readings, flashcard decks, persistent checklists, exercises with revealed
solutions, and checkpoint quizzes with explained answers.

## The discipline

`scripts/verify.py` fails the build on any of these, and the fix is always to write the
missing content rather than relax the check:

- a chapter under 600 words of prose (script-aware, so CJK and Thai count correctly)
- a chapter with no visual, unless it declares `data-novisual="reason"`
- a missing objective, recap, exercise or checkpoint quiz
- a quiz answer with no explanation
- a concept in the source material with no chapter mapped to it
- the words `TODO`, "similar to the above", "and so on"

## Three modes

**Topic** — "teach me Rust from zero, I know Python."
**Digest** — turn slides, PDFs or notes into a course, *plus the chapters the source skipped*.
**Codebase** — what a project is, how it works, and **where it actually stands**: done, in
progress, stubbed, broken, TODO — each with the file path and the evidence.

## Layout

```
skills/teachme/
├── SKILL.md              workflow, the iron law, what it refuses to do
├── references/
│   ├── atlas.md          five expansion axes, syllabus shapes, coverage ledger
│   ├── teaching.md       how people understand things; shapes of knowledge; accuracy
│   ├── authoring.md      chapter anatomy, prose and example standards, language
│   └── visuals.md        when a picture earns its place, and which form
├── assets/
│   ├── shell.html        the reader app: CSS, JS, every component
│   ├── blocks.html       every block, copy-paste ready
│   └── i18n.json         14 interface languages
└── scripts/              assemble.py · verify.py · embed-image.py
```

MIT
