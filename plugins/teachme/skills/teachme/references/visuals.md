# Visuals

A course that is only prose is a course the learner has to render in their head. This file
decides **when** a picture earns its place and **which** form to reach for.

## The test a visual must pass

> Does this show a **mechanism, shape, or relationship** that the prose would need three
> paragraphs to convey — and that the reader would otherwise have to build in their head?

If yes, draw it. If it is a bullet list wearing boxes, an icon next to a heading, or a
restatement of the sentence above it, delete it. **Decorative diagrams are worse than none**:
they cost the reader attention and pay nothing back.

Signals that a visual is owed:
- You are about to write "imagine", "picture", "think of it as", "in memory this looks like"
- Something happens **over time**, **in parallel**, or **in an order that isn't the code order**
- Two or more things **point at**, **contain**, or **wait for** each other
- A number only means something **compared to another number**
- The learner must hold **more than three things at once** to follow the paragraph

## Requirement

**Every chapter ships at least one visual.** `verify.py` fails a chapter with none.
If a chapter genuinely has nothing to draw — a naming-conventions chapter, say — declare it:

```html
<section class="chapter" id="ch-9" data-title="Conventions" data-novisual="pure prose: naming rules">
```

That is a deliberate decision on the record, not an oversight. Reach for it rarely; most
chapters that "have nothing to draw" have a comparison, a flow, or a before/after hiding in them.

## Choosing the form

| The idea is… | Use | Notes |
|---|---|---|
| A pipeline, request path, lifecycle | `.flow` | add `.v` for vertical when labels are long |
| A state machine | `.flow` with `.node.round` + `.arrow.back` | more than ~5 states → inline SVG |
| Layers, abstraction levels, "where my code sits" | `.stack` | mark the learner's layer `.hi` |
| Arrays, buffers, memory, slices, bit patterns | `.cells` | `<i>` index above, `<b>` pointer below |
| Directory layouts, hierarchies, ASTs, DOM | `.tree` | preformatted; `<u>` the one that matters |
| Who talks to whom, in what order | `.seq` | auth flows, protocols, round trips |
| Things happening at the same time | `.lanes` | concurrency, async, pipeline stages, request timing |
| A number that only means something compared | `.bars` | benchmarks, sizes, complexity growth |
| Events in chronological order | `.timeline` | history, project status, disease course, a case |
| Named parts of one example | `.annot` | sentence structure, a formula, a legal clause, an equation |
| Anything genuinely geometric | inline `<svg>` + `.d-*` classes | last resort, most effort, most control |
| A real UI you are teaching someone to navigate | `scripts/embed-image.py` | inline data URI; crop hard |
| A mechanism unfolding step by step | `.walk` | **see below** |
| The same thing done two or three ways | `.tabs` | languages, libraries, approaches |

Exact markup for all of them: `assets/blocks.html`.

## `.walk` — use it more than you think

`.walk` steps through one code block, highlighting the lines under discussion as the
explanation advances. It is the closest thing on a static page to a person pointing at a
screen, and it is the highest-value block in the library.

Reach for it whenever **the order of execution is not the order of the lines**:

- tracing a request from route to database and back
- recursion, event loops, async/await, callbacks resolving out of order
- an algorithm mutating state (sorting, tree traversal, diffing)
- git operations changing what refs point at
- a build or deploy pipeline
- "why does this print `undefined`?"

One `.code` inside; each `.walk-step` names the lines it is about with `data-hl="4-6"`.
Three to seven steps. Each step is a claim about what is true *at that moment*, not a
paraphrase of the line.

## Craft rules

1. **Caption every figure with the takeaway, not the label.** "Fig 3.2 — Why the program takes
   as long as its slowest worker, not the sum" beats "Fig 3.2 — Goroutine timing". Figures are
   auto-numbered; write the caption without a number.
2. **Highlight the subject.** Every diagram has one thing the reader should look at first —
   mark it `.hi` and leave the rest neutral. A diagram where everything is emphasised
   emphasises nothing.
3. **Show the wrong version too.** For anything people get wrong, draw the broken state next to
   the correct one (`.cmp`, or two figures). Misconceptions are corrected by contrast.
4. **Label the arrows.** An unlabelled arrow means "related somehow", which teaches nothing.
   Put the verb, the message name, or the payload on it.
5. **Never hard-code colours.** Use the `.d-*` classes and the CSS variables — a hex value
   will be invisible in one of the two themes. Check both.
6. **Keep it under a screen.** If a diagram needs scrolling, it is two diagrams.
7. **Accessibility.** `role="img"` and a real `aria-label` on every `<svg>`. The caption must
   carry the point in text, so the figure is never the only place the information exists.
8. **Simplify ruthlessly.** Draw the four boxes that matter, not the fourteen that exist.
   A diagram is an argument, not an inventory.

## Inline SVG conventions

Reach for SVG only when no block above fits. Then:

- `viewBox="0 0 640 H"` — 640 fills the column at every width; pick `H` to fit the content.
- Classes, never inline colours: `.d-box` (`.hi`, `.ok`, `.bad`, `.dim`), `.d-line` (`.dim`),
  `.d-arrow` (`.dim`), `.d-fill`, `.d-dim` for muted text, `.d-accent`, `.d-ok`, `.d-bad`,
  `.d-mono`, `.d-sm`. These are what make the drawing survive the dark theme; a hard-coded
  `fill="#333"` is invisible on half the page views your course will ever get.
- Arrowheads are already defined document-wide — `.d-arrow` picks them up, no `<defs>` needed.
- Text: `text-anchor="middle"`, centre it on the box (`y` = box centre + ~5).
- Boxes: `rx="9"` to match the page's radius.
- Build paths from straight segments (`M x y H x2 V y2`) rather than curves; they are easier
  to get right and read cleanly at any size.

**Two failure modes that produce no error and no visible symptom while you are writing:**

- **Anything outside the viewBox is clipped.** The SVG does not grow to contain a stray label,
  so a caption at `x="700"` in a 640-wide viewBox simply is not there. Keep every `x`, `y`,
  `cx` and `cy` inside the box, and leave a margin for text that extends past its anchor.
  `verify.py` warns on coordinates it can see outside the box.
- **Every `id` you define is document-wide.** Chapters are concatenated into one file, so a
  `<clipPath id="tail">` in chapter 3 captures every `url(#tail)` in chapter 11 as well.
  Prefix them with the chapter: `id="ch3-tail"`. `verify.py` fails on duplicates.

A worked figure using both rules — a clipped region reusing the same path rather than a second
hand-drawn one — is in `assets/examples/concept-chapter.html`.

## Where visuals go in a chapter

- **The mental-model figure comes early**, right after "why it exists" — it is the frame
  everything else hangs on.
- **A `.walk`** goes where the worked example is, replacing a static code block.
- **A comparison figure** (`.bars`, `.cmp`) goes where you make the trade-off argument.
- **The architecture/flow figure** goes before the code that implements it, never after.

Two to five visuals in a typical chapter. More than that and they stop being signposts.
