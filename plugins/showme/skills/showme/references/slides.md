# Slides

One idea per slide, shown rather than listed. This file is the craft layer: what goes on a
slide, which layout the idea wants, and how to keep it legible from the back of the room.
Markup for everything named here: `assets/layouts.html`.

## The headline is the claim

The single change that improves a deck more than any other:

| Topic headline | Claim headline |
|---|---|
| Q4 revenue | Growth came from the base, not the funnel |
| Methodology | Two of the three methods gave the same answer |
| Timeline | We lose the window if we start after March |
| User feedback | People aren't confused — they don't trust it |

A topic headline makes the audience do the work of figuring out why they're looking at this.
A claim headline hands them the point and lets the evidence confirm it. It also makes the deck
skimmable later, which is how most decks are actually consumed.

## Anatomy of a content slide

```
eyebrow      where we are (section, phase) — optional, quiet
headline     the claim, as a sentence
evidence     ONE thing: a chart, a diagram, an image, a short list, a number
takeaway     the "so what", one line, when the evidence doesn't speak for itself
notes        everything you'd actually say
```

Not every slide needs all of it. Every slide needs a headline and one piece of evidence.

**Word ceilings** — `verify.py` enforces these, and they are not arbitrary. Reading and
listening compete for the same channel: a slide the audience is still reading is a slide during
which nobody heard you.

| | Ceiling |
|---|---|
| A statement slide | ~25 words |
| A normal content slide | ~55 words |
| A bullet list | 5 bullets, ~12 words each |
| Speaker notes | no ceiling — this is where it all goes |

## Picking the layout from the shape of the idea

Not from the subject. A cooking deck, a physics lecture and a board update all use `bignum`
when there is one number that matters.

| The idea is… | Reach for |
|---|---|
| One number that changes the conversation | `bignum` |
| Three or four numbers worth comparing | `stats` row |
| Change over time | `chart` line / area |
| Ranking or comparison of amounts | `chart` bar |
| One measure across many or long-named categories | `chart` hbar, with `data-hi` on the one that matters |
| How each column is composed, when the total means something | `chart` stack |
| Parts of a whole (3–5 parts, no more) | `chart` donut |
| Two things in tension | `cmp` (this vs that, before vs after, wrong vs right) |
| A sequence of steps or a path something takes | `flow`, or `pts.num` |
| Events across time | `tline` |
| Things stacked on things | `layers` |
| Two axes of choice | `matrix` |
| Narrowing at each stage | `funnel` |
| How far along four workstreams are | `prog` |
| What shipped and what didn't | `checks` |
| The terms of a proposal — cost, date, who, judged on what | `kv` |
| Short labels meant to be scanned, not read | `chips` |
| A claim strong enough to stand alone | `statement` |
| Someone's actual words | `quote` |
| Something you have to see to believe | `imgfull` / `split` / `fig` |
| Parallel options of equal weight | `cols c3` with `card`s |
| Exact values people will check | `table` — sparingly |
| A worked example, code, a formula, a passage | `code` slide |
| A pause between arguments | `section` |

If the idea doesn't fit any of these, it is usually two ideas. Split it.

Three of these exist for the readout rather than the pitch, and a status update that reaches
for bullets instead of them is the most common way this skill gets used badly. "Where the
project stands" is `prog` plus `checks`; "what we are asking for" is `kv`. A room being
briefed needs to see state, not read about it.

**Vary the layout.** Three bullet slides in a row and the room stops looking up. `verify.py`
flags runs of the same layout and any single layout used for more than about 40% of the deck —
not for variety's sake, but because a change in shape is how the audience knows a new kind of
thing is being said.

## Evidence that is actually evidence

- **Label the point, not the axis.** A chart's title should say what the chart proves.
  The `take` line under it says what to do about it.
- **Bars start at zero. Lines don't have to.** The runtime enforces the first and gives lines a
  tight, honest frame automatically. Truncating a bar axis is the most common way a deck lies
  by accident.
- **Three to five categories.** Beyond that, a chart becomes a table with extra steps — either
  aggregate the tail into "other" or use a table on purpose.
- **One focal point per slide.** Highlight the series, node, row or quadrant you are talking
  about (`hi`) and let everything else sit back. A slide where everything is emphasised
  emphasises nothing.
- **Kill chartjunk.** No 3D, no shadows on bars, no gradient fills carrying no meaning, no
  legend when one series is self-evident from the title.
- **Round numbers on slides, exact ones in the appendix.** "£1.2m" on the slide; the ledger
  behind it in the backup.
- **Say where the number came from.** A `.src` line under a chart or table — the system, the
  date range, and what it excludes — costs one quiet line and is the difference between a
  number the room accepts and a number the room interrogates. Put it on anything a reasonable
  person could ask "says who?" about, and put the exclusions in it before someone finds them.
- **One measure, one colour.** Colouring every bar of a single series differently tells the
  audience "these are different things", which the labels already told them, and it spends the
  one signal you have. Grey the field and colour the bar you are talking about (`data-hi`).

## Images

- Use a real one, or use `ph` — the honest placeholder that says what belongs there and what
  size. Never describe an image you don't have as if it exists, and never generate a fake
  screenshot, chart, or photo of something real. A placeholder the user fills in is worth more
  than a convincing lie.
- Inline them as data URIs with `scripts/embed-image.py`, so the deck stays one file.
- Full-bleed (`imgfull`) when the image *is* the argument; `fig` beside text when it supports it.
- Crop hard. An image at 1280×720 that needs squinting is decoration.
- Every image gets real `alt` text — it is also what you'll read from if the projector fails.

## Builds

`data-build="1"`, `"2"`, `"3"` reveal elements on successive presses.

Use them when **the order of understanding matters**: a number, then what it means, then why it
is surprising. Or three points where the third only lands after the first two.

Don't use them to hide a list from an audience who could have read it in two seconds — that is
theatre that costs you clicks and risks stranding you mid-slide. If a slide has more than about
four build steps, it is more than one slide.

## Legible from the back of the room

The runtime does the scaling; you control the rest.

- Body text on a slide is never below ~20px on the 1280×720 canvas. If something has to be
  smaller to fit, it doesn't fit.
- Don't put text on the busy part of an image; use the overlay (`imgfull` has one) or move it.
- Keep contrast high — pale grey on white looks refined on your laptop and disappears on a
  projector in a lit room.
- Two type sizes per slide is usually enough; three is the maximum before it reads as noise.
- Line length for anything paragraph-shaped: 24–34 characters at display sizes. The layouts
  already cap this; don't override it.

## Speaker notes are part of the deliverable

Write what you would actually say, not a summary of the slide. Good notes contain:

- the sentence you open the slide with, and the one that hands off to the next slide
- the number behind the number, the caveat, the thing you'd say only if asked
- the objection you expect from this specific audience, and your answer
- what to cut if you are running short

They are also what makes the deck useful to someone reading it alone — the runtime shows them
in Read mode. Roughly 40–120 words per slide. `verify.py` fails a content slide with none,
because an empty note means the thinking either didn't happen or got left on the slide.
