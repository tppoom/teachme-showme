# Teaching

What makes anything understandable, and how to tell what a given piece of material needs.

Nothing here is tied to a subject. A programming language, a legal doctrine, a chord voicing and
a sauce all become understandable through the same moves — and courses fail through the same
handful of omissions regardless of what they are about. Reach for the shape of the knowledge,
not a label for the field.

## The moves that make things land

1. **Motivation before mechanism.** Open every idea with the problem it solves and what life
   was like without it. An idea introduced as a rule is memorised; an idea introduced as an
   answer is understood. If you cannot say what goes wrong without it, you do not yet
   understand it well enough to teach it.
2. **Concrete before abstract.** One real example first, then the general rule, then a second
   example that stretches it. The reverse order — rule first — is how textbooks lose people,
   and it is the default an AI falls into unless it decides otherwise.
3. **Name the wrong intuition.** Most subjects have a natural, sensible, incorrect belief
   sitting exactly where the learner is standing. Say it out loud, then show why it fails.
   Misconceptions are corrected by contrast, never by assertion.
4. **Show the reasoning, not only the result.** Whatever "derivation" means in this material —
   a proof, a diagnosis, a design decision, a translation choice, why the dough is rested —
   the learner should be able to reconstruct it. A result they cannot rebuild is a fact, not
   understanding.
5. **Production over recognition.** Recognising the right answer feels like learning and isn't.
   Every chapter asks the learner to *make* something: write the sentence, solve the problem,
   run the command, cook the thing, take the position and defend it.
6. **Give a checkable criterion.** "Do it for eight minutes" fails on a different stove;
   "until the edges lift and the centre is matte" transfers. Whatever the subject, say how the
   learner can tell that they got it right — and what the common near-miss looks like.
7. **Close the loop back to why.** End where you started: now that they can do it, restate what
   it was for. That is what makes the knowledge stay attached to something.

## Reading the material: what shape is each idea?

Instead of classifying the subject, classify each thing you have to teach. The shape tells you
what the chapter needs and which blocks to reach for.

| The idea is… | The chapter must contain | Blocks |
|---|---|---|
| **A procedure** — a thing done in order | Every step, timings, what it looks like when it's going right, and how to recover when it isn't | `.steps` with time badges, `.check`, `.cmp` right/wrong |
| **A concept** — a thing that is | A definition, the boundary cases, and the contrast with its nearest neighbour (the thing people confuse it with) | `.formal defn`, `.grid` cards, `.cmp`, a mental-model figure |
| **A relationship** — a formula, rule, or law | What every symbol or term means, where the relationship comes from, and where it stops being true | `.math` + `.where`, `.derive`, `.callout warn` for the limits |
| **A mechanism** — how something works inside | The parts, the flow between them, and one trace end to end | inline SVG, `.flow`, `.seq`, `.lanes`, `.walk` |
| **A fact to hold** — vocabulary, names, values | Retrieval practice, not re-reading, plus one real use of each item | `.vocab`, `.cards`, typed-answer quiz |
| **A skill** — something the hands or the tongue do | Do it now, with a criterion for judging the attempt and a diagnosis for each common failure | `.ex`, `.check`, `.dlg`, `.annot` |
| **A judgment call** — when to choose what | Worked examples of the decision itself, the criteria made explicit, and a case where the usual answer is wrong | `.cmp`, `.tw` decision table, `.ex` with a defended answer |
| **A claim about the world** — history, findings, doctrine | The evidence, the source, and the disagreement | `.quote` with `<cite>`, `.timeline`, `.cmp` of interpretations |

Most chapters mix two or three of these. Ask the question per idea, not per course.

## An example that actually teaches

The single most common failure in AI-written courses is an example that demonstrates syntax
rather than understanding. A teaching example is:

- **Complete.** It runs, compiles, cooks, parses, resolves. Not a fragment with an ellipsis.
- **Real.** `invoice`, `patient`, `ผู้เช่า` — never `foo`, `thing`, `X`. Fake names make the
  learner translate twice.
- **Shown working.** The output, the result, the finished thing. If it produces something, show
  what it produced.
- **Annotated on the why.** Comments and asides explain the decision, never restate the line.
- **Followed by a variation.** Change one thing and show what changes. That is where the rule
  becomes visible.
- **Followed by a breakage.** Show it wrong, with the literal error, the smell, the wrong
  answer — and the fix. Learners meet the broken version far more often than the perfect one.

One example built this way beats five that only show the happy path.

## Accuracy and responsibility

The course is a document the learner will trust and keep. That raises the bar above chat.

- **Say the vintage.** Anything that changes — a law, a price, an API, a guideline, a version,
  a "current best practice" — carries its date and, where it matters, its jurisdiction.
- **Cite what can be checked, and never invent a citation.** No fabricated case names,
  statistics, page numbers, papers, or quotes. If you are unsure of the reference, state the
  claim and say the source needs checking. A confident wrong citation is worse than no citation.
- **Uncertainty is content.** "There are two positions here and this is what separates them"
  teaches more than false confidence. The same goes for a codebase: "this part is unclear to me;
  here is what I established and what I could not" is an honest, useful chapter.
- **Stay on the education side of the line.** Where the subject touches medicine, law, finance,
  safety or mental health: teach the mechanism, the vocabulary and how to read the primary
  sources; do not diagnose, do not advise on a specific case, and name who the learner should
  actually consult. One sentence in the chapter — not an apology, and not a refusal to teach.
- **Do not simplify away the complication.** If the honest answer is that it depends, teach what
  it depends on. Flattening a real difficulty is the fastest way to produce a course that feels
  clear and leaves the learner unable to do anything.
