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

## Before you build

Three decisions, made in your first message rather than discovered by correction later.

**Where it goes.** The user named a place → use it. Otherwise `./<slug>/` in the current
working directory — **except** when the cwd is the codebase you were asked to explain, or any
repo you were not asked to modify. Dropping a course folder inside someone's source tree is a
mess they have to clean up: use the parent directory or `~/Desktop/`, and say which. State the
path up front, always.

Scaffold it rather than hand-building the shape — assemble will reject a wrong one anyway:
```bash
python3 $SKILL/scripts/new.py <dir> --title "…" --lang th
```

**How big.** The atlas sets the floor, the request sets the ceiling, and they often disagree.

| The request | Chapters |
|---|---|
| One concept done properly — "explain Python decorators" | 4–8 |
| A tool, a library, a bounded skill | 8–14 |
| A whole language or field, replacing a paid course | 14–24 |
| A digest of supplied material | one per source section, plus the gaps the source assumed |
| A codebase | 7–14, sized to the modules that actually exist |

If the atlas demands materially more than the request implies, **say so before authoring**:
*"ครบจริงต้องประมาณ 18 บท อ่านราว 3 ชั่วโมง เอาเต็มเลยไหม หรือเอา 8 บทแรกก่อนแล้วค่อยต่อ"*.
That question costs one message. Eighteen unwanted chapters cost an hour.

**New or existing.** If a course directory already exists for this topic, you are editing, not
rebuilding — jump to *Changing it later*.

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
python3 $SKILL/scripts/verify.py <course-dir> --wip    # after every chapter
python3 $SKILL/scripts/verify.py <course-dir>          # final gate, no --wip
```
A FAIL is an instruction to write the missing thing, never a reason to loosen the check.
What "done" means is in *Handing it over* below — it is more than a passing gate.

Keep `parts/` unless the user asks you to remove it; editing one chapter later is far cheaper
than regenerating a course.

## Surviving a long build

A complete course is more output than fits comfortably in one context, and most failed runs
fail here in a specific, recognisable way: the model starts strong, feels the length, and
begins compressing. The last third arrives as bullet points. That is the exact failure the
user came to this skill to escape, so beat it with process rather than willpower.

- **Write each chapter straight to its file**, one chapter per turn. Never draft a chapter in
  your reply and then save it — that pays double the tokens for nothing.
- **Never hold the course in your head.** `SYLLABUS.md` is the source of truth. Re-read it to
  find what comes next instead of remembering.
- **Checkpoint after every chapter** with assemble + `verify.py --wip`. One second each, and it
  is what stops a broken tag in chapter 3 from surfacing at chapter 18.
- **Never re-emit a chapter you already wrote.** To change one, edit that one file.
- **If your context is compacted mid-build**, recovery is mechanical rather than lossy: read
  `SYLLABUS.md`, run `ls <dir>/parts/`, resume at the first chapter id with no file. Nothing is
  lost, because nothing was ever only in memory.
- **If you catch yourself shortening chapters to reach the end, stop.** Say how many are done
  and ask whether to continue now or in a fresh session. "12 of 18 done, the rest needs another
  pass" is worth far more to this user than 18 thin chapters — thin chapters are the product
  they are already unhappy with everywhere else.

## Handing it over

Done means all of this, in order — not "the files exist".

1. `verify.py` passes **without** `--wip`
2. You opened `index.html` in a browser and actually looked: the cover, one chapter, one visual
3. You clicked one quiz answer and one Mark-complete, and both behaved
4. You sent the file with `SendUserFile`, or gave the exact path if you cannot
5. You reported real numbers — chapters, words, visuals, quiz questions — and named anything
   you deliberately left out, with the reason

Then two lines on how to use it: everything is in the one file and works offline, tick each
chapter as you finish it, `/` searches. Do not narrate the build; they want the course.

## Changing it later

"Chapter 5 is too fast", "add a chapter on X", "make it Thai instead":

- Edit the one part file, or add one, then re-assemble and re-verify. Never rebuild the whole
  course, and never hand-edit `index.html` — it is generated, and the next assemble overwrites
  it.
- Keep `course_id` unchanged, or the learner loses every tick, checklist and flashcard they saved.
- If they hand you an `index.html` with no `parts/` beside it, say so and offer to reconstruct
  the parts from it. Silently regenerating a course they have already annotated is worse than
  asking.

## What a run looks like

> **User:** สอน Rust ให้หน่อย ผมเขียน Python เป็นแล้ว

1. **Intake** — topic mode, Thai, learner knows Python but has never managed memory. Nothing
   here needs a question; state the assumption and move.
2. **Atlas → syllabus** — axis 1 stops at "knows functions, types, loops" but *includes* stack
   vs heap and what a pointer is, because Python never made them think about either. 17
   chapters. Scaffold, write `SYLLABUS.md`, show the list: *"17 บท อ่านราว 3 ชม. เริ่มเลยนะครับ"*
3. **Author** — `parts/01-why-rust-exists.html`, one per turn, assemble + `--wip` after each.
4. **Final gate** — `verify.py` clean, open it, click a quiz, look at it.
5. **Hand over** — `SendUserFile` + *"17 บท 24,000 คำ 41 ภาพ 44 ข้อ · ตัด async ออก ไปอยู่ใน
   หัวข้อเรียนอะไรต่อแทน"*

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
| Scaffold a course directory | `scripts/new.py <dir> --title … --lang …` |
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
