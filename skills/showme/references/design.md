# Design direction

The user says how it should look. Your job is to turn those words into a concrete, coherent
system *before* building slides — and then not deviate from it. A deck that changes its mind
about its own look is the thing that reads as "made by a machine".

## Decide the look first, and write it down

Put the decision in `meta.json` and state it back to the user in one line: preset, accent,
motif, and why. If they said nothing about style, choose deliberately from the audience and
occasion and say what you chose. Silence is not permission to default — it is a decision you
are making on their behalf, so make it out loud.

```json
"theme": { "preset": "swiss", "motif": "rule", "tokens": { "accent": "#e2231a" } }
```

## Presets

`assets/themes.json` ships fifteen complete looks, each with a `use` line describing the room
it belongs in. Read that file and pick the nearest one; it is faster and better than inventing
a palette, and every token is already contrast-checked against its background.

| Preset | The room it belongs in |
|---|---|
| `keynote-dark` | Product launches, tech keynotes, a stage with the lights down |
| `swiss` | Strategy and design work that should read as rigorous and unfussy |
| `startup-pitch` | Investors and sales — bright, confident, generous whitespace |
| `corporate-clean` | Board updates, client reports, quarterly reviews |
| `editorial` | Talks with a point of view; brand and culture decks |
| `academic` | Conference talks, thesis defences, lectures |
| `brutalist` | Manifestos and provocations; internal decks that need to wake the room |
| `midnight-data` | Analytics reviews where the charts are the argument |
| `terminal` | Engineering deep-dives, security briefings, developer talks |
| `soft-pastel` | Workshops, teaching, anything for a non-expert audience |
| `forest` | Sustainability, health, public sector, research with a human face |
| `noir` | Awards, film, fashion — gravity rather than energy |
| `mono-print` | Anything that will be printed, photocopied, or read on paper |
| `neon-gradient` | Consumer launches, hackathons — loud on purpose, wrong for a board |
| `clinical` | Medicine, safety, incident reviews, regulated industries |

Start from a preset in almost every case. A preset plus one or two overridden tokens is a
custom look; a palette invented from scratch is usually four hours of small mistakes.

Two of these are chosen for a constraint rather than a mood, and that makes them easy to
forget. Reach for `mono-print` the moment someone says the deck will be handed out or
photocopied — it is the only preset where every distinction survives losing colour. Reach for
`clinical` when being wrong has consequences: it holds red back so that a red number means
something, which no other light preset does.

## Turning words into tokens

Style briefs arrive as adjectives. Each one has a concrete meaning:

| They say | It means, concretely |
|---|---|
| clean, minimal, simple | White background, one accent used rarely, no motif or a thin rule, generous margins, one type family |
| bold, punchy, high-energy | Heavier display weight, tighter tracking, larger type, saturated accent, `block` or `corner` motif |
| premium, luxury, high-end | Dark or warm-neutral background, serif or wide-tracked display, restrained accent, more whitespace, small type at large scale |
| friendly, approachable, warm | Warm background, rounded radius, softer palette, rounded sans, more colour variety |
| serious, institutional, trustworthy | Cool neutrals, navy or deep accent, `rule` motif, conventional layout, nothing playful |
| technical, engineering | Mono for anything data-shaped, dark background, cool accent, denser grids |
| playful, fun | Higher-chroma multi-colour, rounded radius, more illustration, looser layout |
| editorial, magazine | Serif display, off-white paper, asymmetric layouts, big pull quotes |
| retro, vintage | Muted or period palette, slab or geometric type, flat colour, no shadows |
| futuristic, modern | Dark, cool accent, `glow` or `grid` motif, thin weights at large sizes |
| hand-made, human | Warm paper, serif or humanist sans, irregular rhythm, real photographs over icons |

Two or three of these usually combine cleanly ("clean but bold"). Four is a brief that is
fighting itself — pick the two that matter most and say which you dropped.

## When they name a reference

"Like an Apple keynote", "like a McKinsey deck", "like our website". Extract the *attributes*,
not the identity:

- What is the background doing? Dark, white, paper, image?
- What carries the emphasis — type weight, colour, or space?
- How much lives on one slide?
- What is the one recurring visual gesture?

Then build that with your own tokens. Do not reproduce another organisation's logo, wordmark,
or exact brand palette in a deck presented as the user's own — an homage to the *shape* is
what they want, and it is also the only version that is theirs to use. If they hand you their
own brand colours and fonts, use those exactly; that is different, and it is the best case.

## The rules that decide whether it looks designed

1. **One accent, used rarely.** An accent that appears on every element is not an accent.
   Reserve it for the thing you want looked at first on each slide.
2. **Don't centre everything.** Centred type on every slide reads as a default. Pick a strong
   left (or start) edge and hold it; centre deliberately, for statement and section slides.
3. **Hold the margins.** The same left edge on every slide is most of what "designed" means.
   The layouts do this for you — the way to break it is with inline styles, so don't.
4. **Type scale, not type soup.** Use the sizes the layouts define. If something needs a size
   that doesn't exist, the layout is wrong for the content.
5. **Whitespace is not waste.** A slide with one sentence and a lot of air is a slide that got
   edited. Resist filling the bottom third.
6. **No decoration that carries no meaning.** Gradients on everything, drop shadows on every
   card, an icon beside every heading, emoji as bullets in a serious deck — each one adds noise
   and subtracts credibility. A motif is one gesture, repeated; that is enough.
7. **Vary the layout, not the look.** Layouts should change slide to slide; palette, type and
   margins should never change.
8. **Colour must survive the room.** Pale-on-pale looks refined on a laptop and vanishes on a
   projector in daylight. If you can't read it at arm's length at half size, it fails.
9. **Dark decks for dark rooms, light decks for lit rooms.** A dark deck in a bright meeting
   room is washed out; a white deck in a dark auditorium is a flashbulb. If you don't know the
   room, light wins for meetings, dark wins for stages.

## Making a custom theme

Override tokens rather than writing a whole set:

```json
"theme": { "preset": "corporate-clean",
           "motif": "block",
           "tokens": { "accent": "#0f8a5f", "accent-2": "#0f1c2e", "radius": "4px" } }
```

If you must define a theme from nothing, define every token in the contract at the top of
`themes.json` and then check three things: body text against `bg`, `accent-ink` against
`accent`, and the six chart colours against each other and against `bg`. Anything that fails,
darken or lighten until it doesn't. Also check that `c1`–`c6` stay distinguishable in greyscale
— decks get printed, and some of your audience is colour-blind.

## Their own brand

When they supply a logo, put its path (relative to the deck directory) in `meta.json`:

```json
"logo": "brand/logo.svg"
```

assemble inlines it into every running footer and the top corner of the title slide — the
deck stays one file. Prefer SVG or a small PNG on a transparent background; check it against
the theme's `bg` in both the grid and present views, and pick a preset whose background the
logo was designed for rather than recolouring someone's mark. Their brand colours go into
`tokens.accent` and `accent-2`; verify their accent against `accent-ink` for contrast, since
brand colours are chosen for logos, not for text on a projector.

Never add a logo they did not give you, and never add another organisation's.

## Fonts

The deck is one offline file, so the default is system stacks — themes pick faces that are
already on the machine and fall back cleanly across scripts. That is the right default and it
never breaks.

If the user asks for a specific typeface, `meta.json` can carry `fonts.url` for a webfont, and
the deck will then need the network the first time it opens. Tell them that trade-off in one
sentence rather than silently making their offline deck online.
