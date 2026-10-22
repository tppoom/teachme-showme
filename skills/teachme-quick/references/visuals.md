# Visuals

Draw when a picture shows something the prose would need a paragraph to build in the
reader's head. Don't draw decoration: a bullet list in boxes, an icon by a heading, or a
restatement of the sentence above it costs attention and teaches nothing.

**A visual is owed when** you are about to write "imagine / picture / think of it as"; when
something happens over time, in parallel, or in an order that isn't the code order; when
things point at, contain or wait for each other; when a number only means something compared
with another.

## Which form

| The idea is… | Use (markup in `assets/blocks.html`) |
|---|---|
| A pipeline, request path, lifecycle, state machine | `.flow` (`.v` for vertical) |
| Layers — "where my code sits" | `.stack` |
| Arrays, buffers, memory, bit patterns | `.cells` |
| Files, hierarchies, trees | `.tree` |
| Who talks to whom, in what order | `.seq` |
| Things happening at the same time | `.lanes` |
| Numbers that only mean something compared | `.bars` |
| Events in time | `.timeline` inside `figure.viz` |
| Right vs wrong, before vs after | `.cmp` |
| Code whose execution order ≠ line order | `.walk` (3–6 steps) |
| Named parts of one example (sentence, formula, clause) | `.annot` |
| Anything geometric the blocks can't express | inline `<svg>` with `.d-*` classes |
| A real UI or photo | `scripts/embed-image.py` (inlined data URI) |

## Rules

1. **Caption = the takeaway**, not the label: "Why the program waits for its slowest worker",
   not "Goroutine timing". Figures are numbered automatically.
2. **One thing highlighted** (`.hi`); the rest neutral.
3. **Label the arrows** with the verb or the payload.
4. **Four boxes that matter, not fourteen that exist.** Fits on one screen.
5. **Never hard-code colours** — use `.d-*` classes / block modifiers so dark mode works.
6. **Accessibility:** every `<svg>` has `role="img"` and an `aria-label`.

## Inline SVG

- **`viewBox="0 0 480 H"` or narrower** — it shows at about its own size on a laptop and shrinks
  into a phone column with labels still readable. Go up to 640 only for a drawing that truly
  needs the width: on a phone it then scrolls sideways inside its frame, and `look.js` reports
  it. Often the better answer is a taller drawing, or an HTML block (`.flow`, `.steps`,
  `.lanes`) that stacks on a phone by itself. Keep every `x`/`y` inside the viewBox (anything
  outside is silently clipped).
- Classes: `.d-box` (`.hi .ok .bad .dim`), `.d-line` (`.dim`), `.d-arrow` (`.dim`, arrowheads
  are built in), `.d-fill`, `.d-dim` (muted text), `.d-accent`, `.d-ok`, `.d-bad`, `.d-mono`,
  `.d-sm`.
- Text: `text-anchor="middle"`, `y` = box centre + 5. Boxes `rx="9"`. Straight path segments
  (`M x y H x2 V y2`) over curves.
- Ids are document-wide: prefix with the chapter (`ch3-tail`).
