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

## Who is reading

The prose standards above assume an adult learning on purpose. Adjust the register — never the
completeness — to the actual reader.

| Reader | What changes |
|---|---|
| **A child (roughly 8–12)** | Short sentences, one new idea per paragraph, concrete things they can see or hold before any symbol. Analogies from their world, not yours. More visuals, more small exercises, quizzes that are encouraging in their feedback. Chapters of 10–15 minutes. Say it to a parent if the subject needs an adult nearby (chemistry, knives, electricity). |
| **A teenager / exam student** | Direct, never condescending. Tie every idea to where it turns up in the exam and in something they care about. Worked examples at exam difficulty. |
| **A professional short on time** | Lead each chapter with the decision or the task it unlocks. Assume competence in adjacent fields, and say which. Denser prose is fine; skipped prerequisites are not. |
| **A class, or a team you hand it to** | No "you told me" references to the conversation. Everything the requester explained to you in chat goes into the course, because the other readers were not there. |
| **Someone who struggles with the subject** | Smaller steps, more worked examples before any exercise, and explicit reassurance that the common mistake is common. Never cut the hard part — slow down in front of it. |

Set the chapter tag (`beginner`, `intermediate`, `advanced`) honestly; it is how a mixed class
finds its place.

## Writing a quiz that tests understanding

A quiz is where a course proves it taught something, and generated quizzes fail in
recognisable ways. `verify.py` warns on the two it can measure.

- **Vary the position of the right answer.** Put it first, last, and in between across a
  chapter. A learner who notices "it's usually B" stops reading the options.
- **Make every option the same length and the same precision.** The correct option is the
  one you were careful with, so it tends to be the longest and most qualified. Write each
  distractor with the same care — a specific, confident, wrong claim.
- **Build distractors from real misconceptions**, the ones named in the chapter. "The
  runtime panics" is a guess someone would actually make; "the computer explodes" is not
  an option, it is a joke that turns a four-way choice into a three-way one.
- **No "all of the above", "none of the above", or negatives** ("which is NOT…") unless
  the exam being prepared for uses them.
- **Ask for application, not recall.** "What does this print?", "which change fixes it?",
  "what would you expect to see if…" — not "what is the name of…".
- **Feedback names the answer by its content, never by its position** ("the conditional
  one", not "the second"). Position-based feedback breaks the moment options are reordered.

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
screenshot it, and click one quiz answer and one mark-complete button. Then send the file
(`SendUserFile` with `display: "render"` where that tool exists) or give its absolute path.

## Editing an existing course

Edit the part file, re-run assemble + verify. Never hand-edit `index.html` — it is generated,
and the next assemble overwrites it. Keep `course_id` unchanged so saved progress survives.
