---
name: teachme
description: Use when someone wants to actually learn something end to end rather than get an answer — "teach me X", "explain this codebase and where the project stands", "turn these slides/PDFs into a real course", "I want to understand Y properly", "I don't want to pay for a course" — or when a chat reply would be too short, skip prerequisites, or quietly drop parts of the source material. Also when they want study material they can keep, read offline, and track progress through.
---

# TeachMe

> **TEACH me everything I HAVE to know.**

## Overview

Produce **one self-contained HTML file** that teaches *any* subject completely — code, maths,
a language, history, law, cooking, an exam syllabus — with prerequisites,
the subject itself, the details, the practice, and what comes next — explained in prose
**and in pictures**: diagrams, sequence and timing charts, and step-through walkthroughs that
highlight the code line under discussion. With progress tracking, search, exercises and
checkpoint quizzes. Readable on any device, offline, forever.

**The distinction that defines this skill:** the request names a *destination*, not a *scope*.
"Teach me goroutines" is answered by teaching goroutines **plus** everything required to
actually understand and use them. Anything the learner would have to go somewhere else to
get is a hole in the course, and a hole in the course is a failure.

## The Iron Law

```
THE SYLLABUS IS A CONTRACT. EVERY NODE SHIPS AS A FULL CHAPTER.
```

Nothing in the atlas may be merged away, compressed into a bullet, listed by name only,
or deferred to "further reading". If you wrote it in `SYLLABUS.md`, you write it in full.
If you decide something genuinely does not belong, **delete it from the syllabus and say why** —
never leave a promise unpaid.

`scripts/verify.py` enforces this mechanically. A FAIL means *go write the missing content*.
It never means loosen the check.

## When to use

- "teach me / explain / I want to understand X" where X is bigger than one answer
- Replacing a paid course, a textbook chapter, or a scattered set of tutorials
- Turning lecture slides, PDFs, docs, transcripts or a spec into real study material
- Onboarding onto a codebase: what it is, how it works, what is done, what is left
- The user already got a short AI answer and wants the whole thing

**Do NOT use for:** a single factual question, a quick how-do-I, a code change, or anything
the user wants as a conversational reply. This skill produces a document, not a chat turn.

## Two independent axes

**Mode — where the material comes from:**

| Mode | Input | The course must additionally cover |
|---|---|---|
| **Topic** | "teach me Rust / OAuth / linear algebra / Japanese" | The whole practising path: setup, tooling, idioms, debugging, what to learn next |
| **Digest** | slides, PDFs, notes, transcripts, links | Every section of every source **plus** what the source assumed you already knew |
| **Codebase** | a repo or directory | Architecture, data flow, every module, conventions, how to run and test it, **current status: done / in progress / TODO / known broken**, and where to make the common changes |

**Shape — what kind of thing each idea is:** a procedure, a concept, a relationship, a
mechanism, a fact to hold, a skill, a judgment call, a claim about the world. This is asked per
idea, not per subject, and it decides what the chapter must contain and which blocks to use.
**Read `references/teaching.md` before the syllabus** — it also carries the moves that make
anything understandable, what an example that actually teaches looks like, and the accuracy
rules for material someone will trust and keep.

## Workflow

Announce the mode, then run all five stages. Create a TodoWrite item per stage,
plus one per chapter at stage 3.

### 1 · Intake
Establish, from the request or by reading: the destination, the learner's current level,
**the output language**, and any hard scope edges.
Write in the language the user is writing to you in unless they say otherwise. Read **every** file, URL and directory
they gave you — completely, not the first 100 lines. For codebase mode, read the entry
points, the config, the tests, the git log and the TODO/FIXME markers.

Ask at most one round of questions, only where the answer changes the syllabus
(typically: current level, and depth vs. breadth). Otherwise assume and state the assumption.

### 2 · Atlas → Syllabus
Build the concept atlas, then cluster it into chapters. **See `references/atlas.md`** for the
five expansion axes, the mode-specific syllabus shapes, and the coverage-ledger format —
and `references/teaching.md` for the shapes of knowledge the atlas must not leave unaddressed.

Write `<course-dir>/SYLLABUS.md` and show the user the chapter list before authoring.
Every concept found in the source material must appear in the ledger, checked, pointing at a chapter.

### 3 · Author — one chapter per file, one at a time
```
<course-dir>/parts/01-<slug>.html, 02-…, 03-…
```
**Never emit the whole course in one pass.** Writing chapter-at-a-time is the mechanism that
prevents the collapse into summary that the user is trying to escape. One file, complete, then
the next. Markup contract: `assets/blocks.html`. Depth floor and prose standards:
`references/authoring.md`.

Every chapter carries: objective → why it exists → **mental-model figure** → the full
explanation → worked example with output → variations and edge cases → common mistakes with
the real error message → exercise with revealed solution → recap → checkpoint quiz with
explained answers. Minimum 600 words of prose. A chapter that fits in 600 words is two
chapters merged or one chapter half-written.

**Every chapter ships at least one visual**, and `verify.py` fails a chapter without one.
Reach for `.walk` — a step-through that highlights the lines it is explaining — whenever the
order of execution is not the order of the lines. Which form suits which idea, and when a
picture is decoration rather than teaching: `references/visuals.md`.

Close with an appendix chapter: glossary of every term used, cheat sheet, and what to learn next.

### 4 · Assemble
Claude Code prints **the skill's base directory** when it loads this skill — call the
scripts relative to that (`$SKILL/scripts/…`), so the skill works both from `~/.claude/skills/`
and from a plugin install. Substitute the real path when you run them.

```bash
python3 $SKILL/scripts/assemble.py <course-dir>
```
Needs `meta.json` (`course_id`, `title`, `subtitle`, `lang`, optional `dir` and `ui`) and
`parts/*.html`. Writes `index.html`.

`assets/i18n.json` ships complete interface translations for **en th ja zh ko es fr de pt ru
id vi hi ar** — set `"lang": "ja"` and the whole page speaks Japanese. For any other language
the build **refuses to ship a half-translated interface**: it prints the exact key template,
which you translate into `meta.json`'s `"ui"` (or add to `i18n.json` so every future course
gets it). RTL languages get `dir="rtl"` automatically and the layout mirrors; code, formulas
and technical diagrams stay left-to-right.

### 5 · Verify — then hand over
```bash
python3 $SKILL/scripts/verify.py <course-dir>          # final gate
python3 $SKILL/scripts/verify.py <course-dir> --wip    # mid-build
```
Run it after every chapter with `--wip`; run it without `--wip` before you hand anything over.
Then open `index.html` in the browser, screenshot it, click a quiz option and the
mark-complete button, and only then send it with `SendUserFile`. Report the real numbers:
chapters, words, examples, quiz questions.

Delete `parts/` only if the user asks; keep it, editing one chapter later is far cheaper.

## Rationalizations — every one of these means "keep writing"

| The thought | The reality |
|---|---|
| "They only asked about X" | They asked to *understand* X. A missing prerequisite means they don't. |
| "This part is basic" | Basic to you. The learner is why the course exists. One short chapter costs nothing; a gap costs comprehension. |
| "I'll cover the rest in a summary table" | A table of names teaches nobody. Names are an index, not a lesson. |
| "The file is getting huge" | Length is the deliverable. That is the whole point. Build in parts. |
| "Similar to the previous chapter" | Then write it out, with its own example. The learner cannot infer it. |
| "Already mentioned in the overview" | An overview is a map. A chapter is the territory. |
| "The slides don't cover this" | Slides are headings. The course is what the slides assumed. |
| "Good enough to start reading" | Ship complete, or state exactly what is missing and why. |
| "They can look this up" | Looking it up elsewhere is the problem they came here to solve. |
| "I'll note the codebase's TODOs briefly" | "Where the project stands" is a chapter, with file paths and evidence. |
| "Fewer, longer chapters are cleaner" | Merging chapters is how content disappears. Follow the atlas. |
| "The prose explains it fine" | If they have to build the picture in their head, you left work undone. Draw it. |
| "This isn't a programming topic, so there's less to teach" | Every subject has prerequisites, mechanisms and practice. Ask what shape each idea is — `teaching.md`. |
| "A vocabulary list is enough" | A word without a sentence is a word they cannot use. A theorem without a derivation is a fact they cannot rebuild. |
| "I'll state the theorem and move on" | If they can't reconstruct it, you didn't teach it. Show the derivation, justify each step. |
| "A diagram would take too long" | The mechanism diagram is the chapter's single highest-value object. Ten minutes. |

## Red flags — stop and go back to the syllabus

- A chapter under 600 words · no code/worked example · **no visual** · no exercise · no quiz
- Writing "imagine", "picture this", "in memory it looks like" — that sentence is a figure you didn't draw
- The words "etc.", "and so on", "similar to above", "left as an exercise for the reader"
- A syllabus node with no chapter · a source section with no ledger entry
- Reaching for a summary because the output feels long
- Answering in chat instead of building the file
- Relaxing `verify.py` instead of writing what it asked for

## Quick reference

| Need | Where |
|---|---|
| Scope expansion, syllabus shapes, coverage ledger | `references/atlas.md` |
| Chapter anatomy, prose/example standards, language | `references/authoring.md` |
| When to draw, which visual form, SVG conventions | `references/visuals.md` |
| How people understand things; shapes of knowledge; accuracy | `references/teaching.md` |
| Every allowed HTML block, copy-paste ready | `assets/blocks.html` |
| The page itself (CSS/JS, placeholders) | `assets/shell.html` |
| Build / gate | `scripts/assemble.py`, `scripts/verify.py` |
| Inline a screenshot as a data URI | `scripts/embed-image.py <img> "caption"` |
| Interface translations (14 languages) | `assets/i18n.json` |

The shell already provides, with no work from you: sidebar TOC with scroll-spy, per-chapter
completion persisted in `localStorage`, progress bar, resume, full-text search, light/dark,
code copy + line numbers + line highlighting, interactive quizzes with scoring, keyboard nav
(`/ j k m t`), mobile drawer, print styles — plus the visual system: `.flow` `.stack` `.cells`
`.tree` `.seq` `.lanes` `.bars` `.timeline`, themed inline-SVG classes with shared arrowheads,
auto-numbered figures and equations, `.walk` step-throughs and `.tabs` — plus MathML formulas
with symbol legends and derivations, `<ruby>` readings, vocabulary and dialogue blocks,
labelled-part annotation, cited quotes, persistent checklists, flashcard decks with their own
progress, and typed-answer quiz questions.
**Do not rebuild these and do not invent class names** — compose the blocks in `blocks.html`.

## Common mistakes

- **Authoring before the syllabus exists.** The contract has to exist before it can be kept.
- **Emitting all chapters in one response.** Quality falls off a cliff halfway down. One file at a time.
- **External assets.** No CDN, no `<script src>`, no remote images, no Mermaid. Inline SVG only;
  real screenshots go through `scripts/embed-image.py`.
- **Decorative diagrams.** A boxed bullet list teaches nothing and costs attention. A visual
  must show a mechanism, a shape, or a relationship — otherwise cut it.
- **Placeholder content.** `TODO`, `…`, "coming soon" — `verify.py` fails the build on these.
- **Teaching the syllabus instead of the subject.** Chapter titles are not chapters.
- **Writing every subject like a programming course.** Ask what shape each idea is, then pick
  the blocks — `teaching.md`. A vocabulary list, a theorem and a recipe each need something different.
- **Wrong language.** Write in the language the user is writing in, unless they say otherwise —
  and set `lang` so the interface matches. Keep code, identifiers, commands and error messages
  in their original form; a translated error message cannot be searched for.
- **Unsourced claims in a subject that needs sources.** Law, medicine, history, science: cite,
  date, and never invent a reference. See the accuracy rules at the end of `teaching.md`.
