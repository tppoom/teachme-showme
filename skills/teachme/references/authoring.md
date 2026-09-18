# Authoring a chapter

What a chapter must contain, how to keep it worth reading, and the mechanics of writing one `parts/NN-slug.html`.

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

## Make it worth reading

Completeness is measured in **ideas the learner can now use**, not in words. A chapter that says
everything once, plainly, beats one that says it three times in three boxes. Learners abandon
padded courses; then nothing in them was taught. Before writing, decide the chapter's *one
sentence* — what the learner can do at the end — and let everything either serve it or go.

**Budget.** Typically **400–900 words of prose**, hard ceiling around 1,200 before the quiz (past
that, split it or cut repetition). **2–4 `<h2>` sections.** No `<h3>`, no `<h4>` (except the recap's own). Each
`<h2>` is a short phrase that names the point, not a label ("Why the tail, not the point", not
"Section 2: Overview"). The opening needs no heading — the first paragraph *is* the why.

**Say it once.** Each idea gets exactly one home: the block that carries it best. If a
comparison table exists, do not also write the comparison as a paragraph and again as a recap
bullet. If the figure shows the mechanism, the prose points at it and adds only what the
picture cannot. When you notice you are restating, delete the weaker version.

**One block, one job.** Callouts are for the two or three things a reader must not miss —
**at most 3 per chapter**, and only one of them a `pitfall` unless the chapter is genuinely
about pitfalls. A page where everything is boxed has no emphasis left. Prefer a plain paragraph;
promote to a block only when the block does something the paragraph cannot (compare, sequence,
step through, let the learner try).

**Shape of the prose.**
- Lead with the answer, then the reason. Not "In this section we will look at…".
- Paragraphs of 2–4 sentences, one idea each. A paragraph over ~110 words is two paragraphs.
- Bold only the term being defined, the one thing that must not be missed. If a paragraph has
  three bold spans, it has none.
- Bullets for genuinely parallel items (≤ 6). Never bullets that are secretly a paragraph, and
  never a bullet list of names that stands in for an explanation.
- A table when items share attributes; a figure when the point is a shape or a flow; prose when
  the point is a *because*.
- Cut the scaffolding: no "as we saw", no "it is important to note", no closing paragraph that
  restates the section just read.

**Depth still comes from specifics, not volume.** One real, complete example with its output;
one honest edge case; the real error message. That is what makes a short chapter deep. What to
cut is repetition, hedging and ceremony — never a step the learner needs in order to do the
thing, and never a syllabus node.

## Chapter anatomy

Required: 1, 5, 8, 9, 10 (objective, worked example, exercise, recap, quiz) plus a visual.
Everything else is content the chapter must *cover*, not a section it must *have* — fold 2, 3, 4, 6
and 7 into 2–4 `<h2>` sections rather than giving each its own.

| # | Block | What it must actually do |
|---|---|---|
| 1 | `.objective` | 2–3 items, each starting with a verb the learner can perform afterwards. Not "understand X" — "predict what X does when Y". |
| 2 | **Why it exists** | The problem it solves, in the opening paragraph or two — no heading of its own. Motivation before mechanism. |
| 3 | **Mental model** | The chapter's key figure — the picture everything else hangs on. An analogy only if it is better than the figure; say where it breaks. |
| 4 | **The thing itself** | The complete explanation of what the learner needs to use it: the parameters that matter, the defaults that surprise, the version differences that bite. This is the bulk. |
| 5 | **Worked example** | Real and runnable, commented on the *why*, with `.code-out` showing actual output. Not a fragment. Use `.walk` instead of a plain block whenever execution order ≠ line order. |
| 6 | **Variations / edge cases** | The one or two that change behaviour: empty, huge, concurrent, wrong, old. Not a catalogue. |
| 7 | **Common mistake** | The one people actually hit — a `.callout pitfall` (or `.cmp`) with the *literal error message* and the fix. |
| 8 | `.ex` exercise | A task they can do now, with the solution in `<details>` **and an explanation of why it works**. |
| 9 | `.recap` | 2–4 bullets. The chapter compressed, not replaced. |
| 10 | `.quiz` | 3–4 questions of mixed kinds, at least one on a case not in the chapter. Every wrong option carries a `data-why`; `.fb` explains why the right answer is right. See *Writing a quiz* below. |

Items 2–7 interleave freely under the `<h2>` sections — the order above is the default, not a cage.
Items 1, 9, 10 are fixed at top, bottom, bottom.

Which of these matter most, and which extra blocks a chapter needs, depends on the subject —
read `teaching.md` — it maps the shape of each idea to what the chapter must contain.

**At least one visual per chapter is mandatory** (`verify.py` enforces it). Two to five is
typical: the mental-model figure early, a `.walk` at the worked example, a comparison figure
at the trade-off argument. See `visuals.md` for which form fits which idea — reaching for the
wrong one is most of what makes diagrams useless.

**The floor is 300 words** — below that `verify.py` calls it a stub. That is a tripwire, not a
target: aim for the 400–900 in *Make it worth reading*. A chapter that lands under 300 is missing
a worked example or an explanation; one that lands over 1,200 is two chapters or repeats itself.

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

A quiz is where a course proves it taught something. Generated quizzes fail in one way above
all others: they ask what the chapter *said* instead of what the learner can now *do*, and pad
the options with jokes. A learner who can answer from the question's wording alone has learned
nothing and knows it — after that they skip every quiz.

**3–4 questions per chapter, and they must not all be the same kind.** Mix these:

| Kind | Looks like | Why it works |
|---|---|---|
| **Predict** | "What does this print / return / cost?" with a short new snippet or situation | Forces them to run the mental model |
| **Diagnose** | "This fails with `<real error>`. What is wrong?" | Mirrors what they will actually meet |
| **Decide** | A realistic scenario, "which approach and why?" where the usual answer is wrong | Tests judgement, the hard part |
| **Recall a precise fact** | A typed answer (`data-answer`) — a value, term, command | Production beats recognition |

At least one question per chapter must use a **case that is not in the chapter** — a new
snippet, a new number, a new scenario built on the same idea. If the question can be answered
by finding the sentence in the text, it tests search, not understanding.

**Write the wrong answers first.** Every distractor is a specific, confident claim that someone
who half-understands would actually make — ideally a misconception the chapter names. Then
give each one a `data-why` on its `<button>`: one sentence saying what that person is
thinking and where it breaks. The page shows exactly that line when the learner picks it, so a
wrong answer teaches instead of merely scoring. A distractor you cannot write a `data-why`
for is a filler option; replace it.

- **4 options, 3 at minimum.** Never fewer than 3; a joke option turns a four-way choice into
  a three-way one ("the computer explodes").
- **Same length, same precision, same tone** as the right answer. The correct option is the one
  you were careful with, so it drifts longer and more qualified; make each wrong one as careful.
- **Do not worry about where the right answer sits** — the page shuffles options on every load
  and after every retry. That also means feedback must name the answer by its content ("the
  conditional one"), never its position or letter, and options must not refer to each other
  ("both of the above"). If the options have a natural order (a scale, steps), add
  `data-order="fixed"` to the `.q`.
- **No "all / none of the above", no negatives** ("which is NOT…") unless the exam being
  prepared for uses them.
- **One idea per question.** If two things must both be true to pick the answer, split it.
- **The stem carries the situation, the options carry the difference.** Put shared wording in
  the question so each option is short and the contrast is visible.
- **`.fb` states the right answer's reason in one or two sentences** and the general principle,
  not a restatement of the option. The wrong-answer reasons live in `data-why`.
- Typed answers: list every acceptable spelling in `data-answer` split by `|` (`9.8|9.81|9,8`).

`verify.py` fails a question with a missing correct answer or explanation, and warns on options
with no `data-why`, fewer than 3 options, an obviously-longest right answer, and quizzes that
are all one kind.

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
