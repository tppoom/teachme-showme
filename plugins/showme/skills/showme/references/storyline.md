# Storyline

A deck is an **argument**, not an outline. This file is how you find the argument — for any
subject, any audience, any length. Nothing here is specific to a kind of talk, because the
thing that makes a deck good is the same everywhere: someone should leave able to repeat your
point to a person who wasn't there.

## Three questions before any slide exists

1. **Who is in the room, and what do they already believe?** You are not filling a blank mind;
   you are moving an existing one. Name the belief you are changing.
2. **What should be different afterwards?** Something they *know*, something they *feel*, or
   something they *do*. Usually one dominates — pick it.
3. **What is the one sentence they repeat tomorrow?** Write it out. That is the **spine**.

If you cannot write the spine, you are not ready to build slides — and the honest move is to
say so and ask, not to produce a deck that wanders. When the user's brief doesn't settle it,
write the spine you believe is right, put it at the top of `STORYLINE.md`, and say so plainly.

## The claim ladder

Every slide carries exactly one **claim**: a full sentence, with a verb, that someone could
disagree with.

- Topic: "Q4 revenue" — that is a heading, not a claim, and it teaches the room nothing.
- Claim: "Growth came from the base, not the funnel." — now the slide has a job.

Write the claims first, all of them, in order, in `STORYLINE.md`. Then read them top to bottom
with nothing else. Three tests:

- **Does it argue?** Each claim should follow from the ones before it.
- **Is anything load-bearing missing?** A step the audience needs but you skipped.
- **Would anything survive being cut?** If removing a claim doesn't weaken the argument, cut it.

The claim goes on the slide as `data-claim` and becomes the headline. `verify.py` fails any
slide without one, because a slide without a claim is a slide nobody needed.

## Moves, not templates

These compose. Pick one spine, then use the others inside sections. They work for a product
launch, a thesis defence, a safety briefing, or a class — because they are shapes of reasoning,
not genres.

| Move | Shape | Use it when |
|---|---|---|
| **Situation → Complication → Question → Answer** | the classic spine | Almost any deck. Establish the shared world, break it, name the question, answer it. |
| **Claim → Evidence → Implication** | one section | Every section, always. Never leave evidence without the "so what". |
| **Before → After → Bridge** | change | You are proposing to move from one state to another. |
| **Problem → Why it persists → What breaks it** | persuasion | The audience already knows the problem and has stopped believing it is solvable. |
| **What / So what / Now what** | briefing | Status updates, incident reviews, research findings. |
| **Options → Criteria → Recommendation** | decision | You need a choice made in the room. Show the losing options honestly. |

A deck that is just "topic, topic, topic" is the failure these prevent.

## Where completeness goes

The audience's attention is the constraint, but leaving things out is not an option — so put
them somewhere other than the slide. Three tiers, and the discipline is knowing which is which:

| Tier | Holds | Rule |
|---|---|---|
| **The slide** | The claim and the single thing that proves it | If it isn't the claim or the proof, it isn't on the slide |
| **Speaker notes** | Everything you'd actually say — the nuance, the number behind the number, the objection you expect and your answer, the transition into the next slide | Every slide gets them. This is where the depth lives |
| **Appendix** | The backup slide you flip to when someone asks | Detail that would derail the main line but that you must have ready |

This is why the deck can be sparse and complete at the same time, and why `verify.py` requires
speaker notes on every content slide. A deck with clean slides and empty notes is not a finished
deck — it is a deck whose content was deleted rather than moved.

## Structure and pacing

- **Open by earning attention**, in one slide. A tension, a number nobody expected, a question
  the room actually has. Never open on an agenda — an agenda answers "how long is this",
  which is not a reason to listen. Put the agenda second if the deck is long enough to need one.
- **Signpost with section dividers** once the deck passes ~10 slides. They give the audience a
  place to breathe and a place to re-enter if they drifted.
- **Land the point, then stop.** The closing slide states the ask: the decision you want, the
  action you want, or the single idea you want kept. "Thank you / Questions?" is not a closer;
  it is a slide that throws away your last thirty seconds.
- **Pace: roughly 1–2 minutes per main slide.** Put the time budget in `meta.json` as
  `"minutes"` and `verify.py` will tell you when the deck and the slot disagree. A 10-minute
  slot with 40 slides is not a fast deck, it is an unfinished edit.

## The cut list

Before you build, delete from the storyline:

- Any slide whose claim restates the previous claim
- Any slide that exists because the topic "should be covered" rather than because the argument
  needs it — that material belongs in the appendix or the notes
- Anything you would skip if you were running short. You *will* run short. Cut it now, while
  you can redistribute what it was carrying.

## STORYLINE.md

`verify.py` reads this file. Keep the shape.

```markdown
# <Deck title>

**Spine:** the one sentence they repeat tomorrow
**Audience:** who they are, what they already believe
**They should leave:** knowing / feeling / doing …
**Slot:** 20 minutes + 10 Q&A

## Slides

- `s-1` — title — *We grew 41% and still lost the enterprise deal*
- `s-2` — agenda — *Three questions, and the third needs a decision today*
- `s-3` — section — *Part one: did the growth thesis hold?*
- `s-4` — bignum — *Revenue grew 41%, ahead of the 30% plan*
- `s-5` — chart — *Growth came from the base, not the funnel*
…
- `s-20` — closing — *Fund two enterprise engineers in Q1, or stop selling to enterprise*

## Appendix

- `s-a1` — CAC by channel — *for the "what about acquisition cost" question*

## Deliberately not in this deck

- The pricing rework — real, but it is a different argument and would cost four slides.
  Mentioned in the notes on `s-18` in case it comes up.
```

Anything you decide to leave out goes in that last section with a reason. Cutting is good;
cutting silently means nobody — including you, next week — can tell what was considered.
