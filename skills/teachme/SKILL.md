---
name: teachme
description: Builds study material as one self-contained HTML course — prerequisites, mechanisms, worked examples, diagrams, exercises and quizzes, with progress tracking, search and offline reading. Use when someone wants to learn something rather than get an answer — "teach me X", "I want to understand Y properly", "explain this codebase and where the project stands", "onboard me onto this project", "turn these slides/PDFs/notes into a course", "help me prepare for the exam/certification" — or when a chat reply would be too short, skip prerequisites, or drop parts of the source. Scales from a one-sitting explainer to a full course.
---

# TeachMe

> **TEACH me everything I HAVE to know.**

Produce **one self-contained HTML file** that teaches a subject — code, maths, a language,
law, history, cooking, an exam syllabus, a codebase — so the reader can actually *do* the
thing afterwards. Prose plus pictures (diagrams, sequence charts, step-through `.walk`
walkthroughs), exercises and checkpoint quizzes, inside a reader app that tracks progress,
searches and works offline.

The request names a **destination, not a scope**. "Teach me goroutines" means goroutines
*plus* everything required to understand and use them. Whatever the reader would have to go
find elsewhere is a hole, and holes are the failure this skill exists to prevent.

## The contract

```
THE SYLLABUS IS A CONTRACT. EVERY NODE SHIPS AS A COMPLETE CHAPTER.
```

- Whatever is listed in `SYLLABUS.md` gets written in full. To drop a node, move it to
  *Deliberately out of scope* with the reason — every promise is either paid or withdrawn
  on the record.
- **Complete, not long.** Every idea taught well enough to use, said once, in the block that
  carries it best. Padding loses the reader as surely as a gap does.
- `scripts/verify.py` enforces the contract. A FAIL means *write the missing content*.

## Fit the course to the request

The skill's defaults serve the typical case. **The user's explicit wishes beat every default
here** — when they ask for something different, do that, and record it in `meta.json` so the
gate agrees with them instead of fighting them.

**Depth** (`meta.json` → `"depth"`; scaffold with `--depth`):

| Depth | When | Chapters | Gate |
|---|---|---|---|
| `quick` | one concept, one sitting, "just explain X properly", time-boxed | 1–4 | 150-word floor; missing quiz/recap/visual only warn; no appendix needed |
| `standard` | a tool, a library, a bounded skill, a codebase, a digest | 5–16 | 300-word floor; objective, visual, recap, quiz required |
| `deep` | a whole language or field, replacing a paid course, exam prep | 14–24+ | 400-word floor; chapters may run to ~1,800 words |

Rough sizing: one concept → 4–8 chapters at `standard`; a codebase → 7–14 sized to the
modules that exist; a digest → one chapter per source section plus the gaps it assumed;
exam → one per blueprint domain weighted by marks, plus strategy and a mock exam.

**Omit** (`meta.json` → `"omit"`; scaffold with `--omit quiz,exercise`): blocks the user
asked to leave out — `quiz`, `exercise`, `objective`, `recap`, `visual`, `appendix`,
`ledger`. Each switches off its check. Write the reason under the `**Depth:**` line in
`SYLLABUS.md`. Omit only what the user asked for or the depth plainly implies.

**Other adaptations that need no flag:** the reader (a child, a class, new hires — see
*Who is reading* in `references/authoring.md`), the language, the tone, chapter count within
the depth band, and which blocks each chapter uses.

**When the atlas wants far more than the request implies**, say so before authoring, in one
message — roughly *"done properly this is ~18 chapters, about 3 hours of reading; all of it, or
the first 8 now?"*, in the user's language. If they
want less, choose a lower depth or ship in **phases** — keep the whole syllabus, move later
chapters under `## Later` in `SYLLABUS.md`; the gate passes honestly for this phase and lists
what is still owed.

## Two ways to run it

- **This skill, in the current session** — the default. Works in Claude Code, Codex and
  Antigravity. Best for `quick` and `standard` courses.
- **`/teachme-cas` (Claude Code only)** — Command → Agent → Skill: a planner agent builds the
  syllabus, author agents write chapters in parallel with fresh context each, and a reviewer
  agent reads the whole course as a learner and fixes it. Best for `deep` courses and anything
  over ~10 chapters, where one context starts compressing the last third. Suggest it when the
  course is that big and the command is available.

## Workflow

`$SKILL` = the folder this SKILL.md lives in. Resolve it to an absolute path once (Claude Code
prints it when the skill loads; elsewhere, it is this file's directory) and call the scripts
from there.

Track one todo per stage, plus one per chapter during stage 3.

### 1 · Intake
Settle: destination, the reader's current level, **who will read it**, output language
(default: the language the user writes in), depth, hard scope edges, and for exams the
**exam date** and the official blueprint version.

Read **every** file, URL and directory they gave you, completely. Codebase mode: entry points,
config, tests, git log, TODO/FIXME markers. A video you cannot access is not a source — ask for
the transcript.

**Confirm before planning — one round, then build.** A misread request is cheapest to catch
here, before an hour of chapters. Send one short message and wait for the reply:

- **The brief, in at most five lines:** what the course covers, who it is for and their level,
  depth, language, where it will be saved, and anything you plan to leave out.
- **Questions only where the answer changes the course** and neither the request nor the
  sources settle it — at most three, each with your recommended answer first. Use
  `AskUserQuestion` (or your environment's question tool); otherwise a numbered list. Usually:
  their current level, the depth, anything to skip.
- **Nothing open?** Then it is a single choice: *start* / *adjust something*.

Skip it only when the user already said to go ahead without questions, or when you are editing
an existing course. This is the one planned stop: after it, decide the rest yourself and state
each assumption in one line.

**Where it goes:** the path they named; otherwise `./<slug>/` — but when the cwd is the
codebase being explained, or any repo you were not asked to modify, use its parent or
`~/Desktop/`. State the path up front. Then scaffold:
```bash
python3 $SKILL/scripts/new.py <dir> --title "…" --lang <code> --depth standard
```
If a course directory for this topic already exists, you are editing — see *Changing it later*.

### 2 · Atlas → Syllabus
Expand the destination along the five axes, cluster into chapters in dependency order, and
write `SYLLABUS.md` with its coverage ledger. Read **`references/atlas.md`** (axes, mode
shapes for topic / digest / codebase / exam, ledger format) and **`references/teaching.md`**
(the shape of each idea decides what its chapter must contain).

Done when: every concept in the source and every gap the atlas found maps to a chapter id in
the ledger, and nothing is used before the chapter that teaches it. Show the chapter list to
the user and continue — stop for approval only if they asked to review it, or the size came
out materially different from what they confirmed.

### 3 · Author — one chapter per file, one at a time
```
<dir>/parts/01-<slug>.html, 02-…, …
```
Before the first chapter, read **`references/authoring.md`** (start with *Make it worth
reading*), **`assets/blocks.html`** (the only class names the shell knows) and one whole
worked example: `assets/examples/concept-chapter.html`, or `status-chapter.html` for
codebase mode's "where the project stands". Pick visuals with `references/visuals.md`.

The default chapter arc: objective → why it exists (opening paragraph) → mental-model figure
→ the explanation → worked example with real output → the mistake people actually make →
exercise with explained solution → recap → checkpoint quiz with explained answers. Drop what
`omit` removed; reorder the middle freely.

Target 400–900 words, 2–4 `<h2>`, paragraphs of 2–4 sentences, ≤ 3 callouts. Write each
chapter straight to its file, then check it:
```bash
python3 $SKILL/scripts/verify.py <dir> --part parts/NN-slug.html
```
Fix every FAIL and WARN it prints before starting the next chapter.

Close with an appendix chapter (`class="chapter appendix"`): glossary of every term used,
cheat sheet, what to learn next — unless `depth` is `quick` or `appendix` is omitted.

### 4 · Assemble + gate
```bash
python3 $SKILL/scripts/assemble.py <dir>     # meta.json + parts/*.html → index.html
python3 $SKILL/scripts/verify.py  <dir>      # final gate — no --wip
```
Set `lang` to the course's language; the interface follows it (presets live in
`assets/i18n.json`, RTL is automatic). For a language without a preset, assemble prints the
key template to translate into `meta.json` → `"ui"`.

### 5 · Review as the reader — then hand over
A passing gate proves structure, not teaching. Re-read the course as the person it is for:

- Could they do every objective using only this course? Fix the first chapter where they couldn't.
- Is any term used before it is defined, or defined twice? Does any chapter repeat another?
- Does every example show real output, and every quiz have one question on an unseen case?
- Open `index.html` in a browser (Playwright or similar, if available): the cover, one chapter,
  one visual; click one quiz answer and one *Mark complete*.

Then hand over: send the file (`SendUserFile` where it exists) or give the absolute path;
report real numbers — chapters, words, visuals, quiz questions — plus anything left out and
why, and anything under `## Later`. Two lines on use: one file, works offline, tick chapters
as you go, `/` searches. Keep `parts/` so later edits stay cheap.

## Surviving a long build

Long builds fail one way: strong first chapters, then compression — the last third arrives as
bullets. Beat it with process:

- **`SYLLABUS.md` and `parts/` are the memory.** After a compaction or a break, read the
  syllabus, `ls parts/`, and resume at the first chapter id with no file.
- **Each chapter is written once, to its file.** To change one, edit that file.
- **When you notice chapters shrinking to reach the end, stop** and report: *"12 of 18 done —
  continue now, or in a fresh session / with `/teachme-cas`?"* Twelve real chapters beat
  eighteen thin ones.

## Changing it later

"Chapter 5 is too fast", "add a chapter on X", "write it in another language": edit or add the one part file,
re-assemble, re-verify. `index.html` is generated — edit `parts/`, never the output. Keep
`course_id` unchanged so the reader keeps their ticks, checklists and flashcards. Given only
an `index.html` with no `parts/`, say so and offer to reconstruct the parts first.

## Gotchas

Each of these has produced a bad course before:

| The thought | What to do instead |
|---|---|
| "They only asked about X" | They asked to *understand* X — teach the prerequisites the atlas found. |
| "This part is basic" | Basic to you. A short chapter costs minutes; a gap costs the course. |
| "I'll cover the rest in a summary table" | Names are an index, not a lesson. Give each node its chapter, or withdraw it on the record. |
| "Merge these to shorten it" | Merging is how content disappears. Lower the depth or phase it instead. |
| "More detail is safer" | Say it once, with a real example, and stop. Watch the ~1,200-word warning. |
| "Imagine / picture this / in memory it looks like…" | That sentence is a figure you haven't drawn. Draw it. |
| "The slides don't cover this" | Slides are headings; the course is what the lecturer said around them. |
| "I'll note the codebase's TODOs briefly" | "Where the project stands" is a full chapter with file paths and evidence. |
| "I'll state the theorem and move on" | Show the derivation so they can rebuild it. |
| "A vocabulary list is enough" | Every word needs a sentence that uses it. |

Hard rules the gate also checks: one self-contained file (no CDN, no `<script src>`, no
remote images — screenshots go through `scripts/embed-image.py`); diagrams use the `.d-*`
classes so both themes render; SVG ids are prefixed with the chapter; no `TODO`, "etc.",
"and so on", "similar to above". In law, medicine, finance and history, cite what can be
checked, date what changes, and leave unknown references unstated rather than invented
(`references/teaching.md` → *Accuracy*).

## Quick reference

| Need | Where |
|---|---|
| Expansion axes, mode shapes (topic/digest/codebase/exam), ledger, phases | `references/atlas.md` |
| How people understand things; shapes of knowledge; accuracy | `references/teaching.md` |
| Chapter anatomy, prose, quizzes, readers' age, language | `references/authoring.md` |
| Which visual for which idea; SVG rules | `references/visuals.md` |
| Every block, copy-paste ready | `assets/blocks.html` |
| Two complete chapters at the standard | `assets/examples/` |
| Scaffold | `scripts/new.py <dir> --title … --lang … [--depth …] [--omit …]` |
| Check one chapter / build / gate | `verify.py --part`, `assemble.py`, `verify.py` |
| Inline an image | `scripts/embed-image.py <img> "caption"` |

The shell already provides — compose `blocks.html`, never rebuild: sidebar TOC with
scroll-spy, saved progress, search, light/dark, code copy and line highlighting, quizzes
with scoring and shuffled options, keyboard nav, print styles, `.flow .stack .cells .tree
.seq .lanes .bars .timeline`, `.walk`, `.tabs`, MathML with `.where` legends, `<ruby>`,
vocabulary and dialogue blocks, checklists, flashcards, typed-answer questions.
