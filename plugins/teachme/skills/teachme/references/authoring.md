# Authoring a chapter

The depth floor, the prose standards, and the mechanics of writing one `parts/NN-slug.html`.

## Setup, once per course

```
<course-dir>/
  meta.json        {"course_id":"nihongo-n5","lang":"th","title":"…","subtitle":"…"}
  SYLLABUS.md
  parts/           01-why-concurrency.html, 02-threads.html, …
  index.html       generated — never edit by hand
```

`course_id` namespaces the reader's saved progress in `localStorage` — chapter ticks, checklists
and flashcard decks. Keep it stable across rebuilds or the learner loses everything.

`lang` swaps the entire interface. `assets/i18n.json` ships **en th ja zh ko es fr de pt ru id
vi hi ar**; RTL languages also flip the layout automatically. For any other language, assemble
prints the key template and you translate it into `"ui"` — the build will not ship a
half-translated page. Override a single string the same way: `"ui": {"mark": "…"}`.

## Chapter anatomy — every item is required

| # | Block | What it must actually do |
|---|---|---|
| 1 | `.objective` | 2–4 items, each starting with a verb the learner can perform afterwards. Not "understand X" — "predict what X does when Y". |
| 2 | **Why it exists** | The problem it solves and what life was like without it. Motivation before mechanism, always. |
| 3 | **Mental model** | One analogy **and the chapter's key figure** — the picture everything else hangs on. Say where the analogy breaks. |
| 4 | **The thing itself** | The complete explanation. Full syntax, every parameter, defaults, return values, versions. This is the bulk. |
| 5 | **Worked example** | Real and runnable, commented on the *why*, with `.code-out` showing actual output. Not a fragment. Use `.walk` instead of a plain block whenever execution order ≠ line order. |
| 6 | **Variations / edge cases** | What changes when the input is empty, huge, concurrent, wrong, or old. |
| 7 | **Common mistakes** | `.callout pitfall` with the *literal error message* the learner will see, and the fix. |
| 8 | `.ex` exercise | A task they can do now, with the solution in `<details>` **and an explanation of why it works**. |
| 9 | `.recap` | 3–6 bullets. The chapter compressed, not replaced. |
| 10 | `.quiz` | 2–4 questions. Test understanding, not recall. Every `.fb` explains why the right answer is right *and* why the tempting wrong one is tempting. |

Items 2–7 interleave freely under `<h2>` sections — the order above is the default, not a cage.
Items 1, 9, 10 are fixed at top, bottom, bottom.

Which of these matter most, and which extra blocks a chapter needs, depends on the subject —
read `teaching.md` — it maps the shape of each idea to what the chapter must contain.

**At least one visual per chapter is mandatory** (`verify.py` enforces it). Two to five is
typical: the mental-model figure early, a `.walk` at the worked example, a comparison figure
at the trade-off argument. See `visuals.md` for which form fits which idea — reaching for the
wrong one is most of what makes diagrams useless.

**600 words of prose is the floor, not the target.** A real chapter usually lands at
900–2000. If a chapter comes in short, it is either two chapters merged (split it) or
half-written (finish it).

## Prose standards

- **Second person, present tense.** "You call `wg.Add(1)` before the goroutine starts."
- **Define every term the first time**, inline, in `<strong>`. Then add it to the glossary.
- **Motivation before mechanism.** Never open a section with syntax.
- **No forward references.** If you need a concept that has no chapter yet, the syllabus order
  is wrong — fix the syllabus, don't apologise in the text.
- **Say the quiet part.** Why this design and not the obvious one. What the docs assume.
  What experienced people know that nobody writes down. This is the value the user is paying
  attention for.
- **Concrete over abstract.** Real names, real numbers, real file paths, real error strings.
- **No filler.** "It's important to note that", "as we discussed", "in this section we will".
  Delete and state the thing.
- **Never write** "etc.", "and so on", "similar to the above", "left as an exercise for the
  reader", "see the documentation for the rest". `verify.py` fails the build on these, because
  each one is a piece of the course that silently didn't get written.

## Example standards

- Every code block compiles/runs as shown, or is explicitly marked as a fragment in the prose.
- Comments explain **why**, never what the next line obviously does.
- Show output in `.code-out` whenever the code produces any.
- Use `data-file="path/to/file.ext"` so the learner knows where the code lives.
- Prefer one realistic example over three toy ones. `user`, `order`, `invoice` — not `foo`, `bar`.
- Wrong-then-right beats right-only: use `.cmp` with `.bad` / `.good` for anything people get wrong.
- In codebase mode, examples are **real excerpts from the repo**, quoted accurately, with the path.

## Visuals

No external libraries — the file must open offline, so no Mermaid, no chart CDN. The shell
ships a full visual system instead: `.flow` `.stack` `.cells` `.tree` `.seq` `.lanes` `.bars`,
themed inline-SVG classes, `.walk` step-throughs and `.tabs`. Markup: `assets/blocks.html`.
Judgment — when a picture earns its place and which form to reach for: `visuals.md`.

Two rules worth repeating here: never hard-code a colour (it will vanish in one of the two
themes — use the `.d-*` classes), and write the caption as the **takeaway**, not the label.
Figures are numbered automatically.

Real screenshots must be inlined:

```bash
python3 $SKILL/scripts/embed-image.py shot.png "The settings page" >> parts/07-ui.html
```

## Language standards

Write the course in the language the user is writing to you in, unless they ask otherwise, and
set `lang` so the interface matches. Half a page in one language and half in another is the
single most visible quality failure.

**Never translate:** code, identifiers, CLI commands, file paths, library and product names,
error messages, chemical formulas, and legal provisions quoted verbatim. A translated error
message cannot be searched for; a translated statute is no longer the statute.

**Introduce a term in its original form, then gloss it once:**
`**goroutine** (ฟังก์ชันที่รันแบบขนานภายใต้ Go runtime)`. After that, use the original term.
Add every glossed term to the appendix glossary.

**Write it properly, not translated-sounding.** Use the register a good teacher in that language
would use — the natural technical vocabulary of that language, its own sentence rhythm, its own
politeness level. Do not calque English structure. If a language has an established local term
(Thai *ตัวแปร* for variable), use it and give the English alongside on first use, because that
is what the learner will meet in documentation.

**Mark up mixed-language content.** Put `lang="ja"` on the span or block when a passage is in a
language other than the page's, so pronunciation, font selection and screen readers behave.
Use `<ruby>` for readings. In RTL courses, put `dir="ltr"` on any block whose content is
inherently left-to-right and is not already covered (code and formulas are handled for you).

## Working rhythm

One chapter per response. After writing `parts/NN-*.html`:

```bash
python3 $SKILL/scripts/assemble.py <course-dir> \
  && python3 $SKILL/scripts/verify.py <course-dir> --wip
```

Fix what it reports before starting the next chapter — thin chapters compound, and a broken
tag at chapter 3 is trivial to find now and miserable at chapter 18.

Before hand-over, run `verify.py` **without** `--wip`, open `index.html` in the browser,
screenshot it, and click one quiz answer and one mark-complete button. Then `SendUserFile`
with `display: "render"`.

## Editing an existing course

Edit the part file, re-run assemble + verify. Never hand-edit `index.html` — it is generated,
and the next assemble overwrites it. Keep `course_id` unchanged so saved progress survives.
