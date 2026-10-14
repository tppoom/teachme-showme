---
name: teachme
description: Builds study material as one self-contained HTML course — short chapters that each teach one idea through a concrete example, with diagrams, optional quick checks, progress tracking, search and offline reading. Use when someone wants to understand something rather than get a one-line answer — "teach me X", "explain Y so I get it", "explain this codebase / onboard me", "turn these slides/PDFs/notes into something I can learn from", "help me prepare for the exam" — or when a chat reply would be too thin. Scales from a 1-chapter explainer to a full course.
---

# TeachMe

> **Teach me so I get it — fast.**

Produce **one self-contained HTML file** that makes the reader understand a subject quickly
and well enough to use it: short chapters, each built around a concrete example they can see,
inside a reader app with navigation, progress, search, light/dark and offline reading.

The measure of success is simple: **someone reads a chapter once and can explain the idea to a
friend.** Not "the course mentions everything", not "it is long". A short chapter with one
excellent example beats a long one that circles the idea.

## What good output looks like

- **Few chapters, each about one idea.** Size the course to what the reader needs, not to
  everything adjacent to the topic.
- **Example first, then the idea.** Every chapter opens on a real case — numbers, a snippet,
  a situation — and names the rule only once the reader has seen it work.
- **Pictures for mechanisms.** If the idea is a flow, a shape, a comparison or something
  that changes over time, draw it.
- **No filler.** No "in this chapter we will", no restating, no generic advice, no boxes that
  repeat the paragraph above. Every sentence either explains, shows or warns.
- **Clean, bug-free page.** The gate fails anything that renders wrong (stray markdown, code
  eaten as tags, broken markup, overflowing figures).

## Size it to the request

| Request | Depth (`meta.json` → `"depth"`) | Chapters | Words per chapter |
|---|---|---|---|
| "Explain X", one concept, one sitting | `quick` | 1–4 | 150–500 |
| A tool, a library, a codebase, a set of notes | `standard` (default) | 3–8 | 250–700 |
| "A full course", a whole field, exam prep | `deep` | 6–16 | 400–1,200 |

Start at the **lowest depth that answers the request.** Only go deeper when the user asks for a
full course or the sources demand it. If the honest size is much bigger than they seem to
expect, say so in one line and offer the short version first.

Prerequisites are **not** chapters by default. Explain a missing term in one sentence where it
is first used. Give a prerequisite its own chapter only if it is a genuinely separate,
non-trivial skill the reader lacks.

`"omit"` (`quiz`, `exercise`, `visual`, `appendix`) records blocks the user asked to drop.
The user's explicit wishes beat every default here.

## Two ways to run it

- **This skill in the current session** — the default, for almost everything.
- **`/teachme-cas`** (Claude Code) — parallel chapter authors with fresh context. Only worth it
  for `deep` courses over ~10 chapters. Mention it then; never default to it.

## Workflow

`$SKILL` = the folder this file is in (absolute path). Keep the process light — the reader's
time and the user's tokens both matter.

### 1 · Understand the request
Read every file, URL or directory the user gave you. Decide: the reader and their level, the
language (default: the language the user writes in), depth, and where to save
(the path they named, else `./<slug>/`; if the cwd is a repo you were not asked to change, use
its parent).

If something would really change the result and the request doesn't settle it (usually the
reader's level), ask **once**, at most two questions, each with your recommended answer.
Otherwise state your plan in two or three lines and start.

```bash
python3 $SKILL/scripts/new.py <dir> --title "…" --lang <code> --depth standard
```

### 2 · Plan the chapters
Fill `SYLLABUS.md`: one line per chapter — `ch-N`, title, and what the reader can do after it.
Order so nothing is used before it is explained. Then check the plan against the request:
**could any two chapters be one? Is any chapter there only because the topic "should be
covered"?** Merge or cut those.

Source material (slides, PDFs, notes, a codebase): every important point in the source must
land in some chapter — add a `## Coverage` list mapping source points to chapter ids. Shape
for each input type is in `references/writing.md` → *Input types*.

### 3 · Write the chapters
Read **`references/writing.md`** once (the chapter recipe, examples, the cut list) and look at
**`assets/examples/example-chapter.html`** (the target style). Copy block markup from
`assets/blocks.html` — grep it for the block you need rather than reading it whole. Choose
visuals with `references/visuals.md` only when you are drawing something non-trivial.

Write each chapter to `<dir>/parts/NN-slug.html`, then check it:
```bash
python3 $SKILL/scripts/verify.py <dir> --part parts/NN-slug.html
```
Fix every FAIL and WARN before moving on.

### 4 · Build, check, look
```bash
python3 $SKILL/scripts/assemble.py <dir>
python3 $SKILL/scripts/verify.py  <dir>
```
If you can open a browser (Playwright or similar), look at the cover and one chapter at
desktop and phone width, in light and dark. Fix anything that looks wrong in `parts/` —
`index.html` is generated.

### 5 · Hand over
Send the file (`SendUserFile` where it exists) or give the absolute path. Report in two or
three lines: chapters, total reading time, anything you left out and why. Keep `parts/` so
later edits are cheap.

## Changing it later

Edit or add the one part file, re-assemble, re-verify. Keep `course_id` in `meta.json` stable
so the reader keeps their progress. Given only an `index.html`, say so and offer to rebuild the
parts from it.

## Gotchas

| The thought | Do this instead |
|---|---|
| "Cover everything around the topic to be safe" | Teach what the request needs. Name what is left out in one line at hand-over. |
| "Start with background / history / definitions" | Start with the example. Background only if it explains *why*. |
| "Explain it abstractly first, then give an example" | Reverse it. The example is the explanation. |
| "Add an objectives box, a key-points box and a recap" | One home per idea. Boxes are for the one thing the reader must not miss. |
| "Picture this / imagine…" | That's a figure you haven't drawn. Draw it. |
| "Pad the chapter so it feels substantial" | Short and clear is the goal. The gate warns on length, not brevity. |
| "Write it in Markdown inside the HTML" | Markdown does not render here. `**x**` shows as asterisks — use `<strong>`. |
| "Paste the code as is" | Escape `<`, `>` and `&` inside `<code>`, or the browser eats them as tags. |

Hard rules the gate checks: one self-contained file (no CDN, `<script src>` or remote images —
inline screenshots with `scripts/embed-image.py`); every chapter has a concrete example;
diagrams use the `.d-*` classes so both themes work; no placeholders or "etc." standing in for
content. For law, medicine, finance and history: date what changes, cite what can be checked,
never invent a source.

## Quick reference

| Need | Where |
|---|---|
| Chapter recipe, examples, cut list, quizzes, input types, languages | `references/writing.md` |
| Which visual for which idea; SVG rules | `references/visuals.md` |
| Every block's markup | `assets/blocks.html` (grep it) |
| The target style, one whole chapter | `assets/examples/example-chapter.html` |
| Scaffold · check one chapter · build · gate | `new.py` · `verify.py --part` · `assemble.py` · `verify.py` |
| Inline an image | `scripts/embed-image.py <img> "caption"` |
