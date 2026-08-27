# Atlas → Syllabus

How "what they asked" becomes "everything they have to know".

## The five expansion axes

Start from the destination the user named. Expand along all five axes. Stop an axis only
when the next node is genuinely already known to this learner — not when the list feels long.

| Axis | Question | Example — "teach me goroutines" |
|---|---|---|
| **1 · Upstream** | What must be understood *before* this makes sense? Recurse until you hit the learner's level. | processes vs threads, blocking I/O, why concurrency ≠ parallelism, Go functions & closures |
| **2 · Core** | Decompose the destination into atomic teachable ideas. One idea = one thing that can be wrong on its own. | `go` statement, the scheduler, stack growth, lifetime vs `main`, panics across goroutines |
| **3 · Mechanics** | Full surface: syntax, every parameter, return values, defaults, error values, exact messages, versions. | `sync.WaitGroup` API, `GOMAXPROCS`, `runtime.NumGoroutine`, `-race`, `fatal error: all goroutines are asleep` |
| **4 · Practice** | How it is really used: idioms, patterns, anti-patterns, pitfalls, debugging, testing, performance. | worker pools, fan-in/fan-out, loop-variable capture, leak detection, `context` cancellation |
| **5 · Lateral & downstream** | Ecosystem, tooling, alternatives, when NOT to use it, what to learn next, how it connects to what they already do. | channels vs mutexes, `errgroup`, structured concurrency, when a plain loop is better |

Axis 1 and axis 5 are the two the learner cannot ask for, because they don't know they're
missing. They are the reason this skill exists. Never trim them first.

### Stopping rule
An axis is finished when the next node is something this specific learner demonstrably
already knows. If you are unsure, **include it** — a short chapter on something known costs
five minutes of reading; a missing prerequisite costs the whole course.

## Clustering into chapters

- One chapter ≈ one sitting (10–25 min read). Split anything longer.
- Order strictly by dependency: nothing may be used before it is taught. Walk the atlas
  topologically; a forward reference is a bug in the syllabus.
- A node with its own failure modes deserves its own chapter, even if it is small.
- **Never merge two nodes to shorten the course.** Merging is how content disappears.

**Typical size** — Topic course: 10–20 chapters. Programming language: 14–22.
Document digest: at least one chapter per source section. Codebase: 7–14.
These are floors set by the atlas, not targets. If the atlas says 26, write 26.

## Check the atlas against the shapes of knowledge

Walk the atlas and ask of each node what *kind* of thing it is — a procedure, a concept, a
relationship, a mechanism, a fact to hold, a skill, a judgment call, a claim about the world
(`teaching.md`). Each shape has something it is easy to leave out: a relationship taught with no
derivation, a skill taught with no production practice, a claim taught with no source, a
procedure taught with no failure recovery. None of these look wrong in a syllabus; all of them
show up the moment a learner tries to use the course.

## Mode-specific shapes

These are the *input* shapes — where the material came from. What each chapter must contain
comes from the shape of its ideas, in `teaching.md`.

### Topic
`Why this exists & what it's for` → `Prerequisites` (as many chapters as axis 1 demands) →
`Setup / first working thing` → core concepts in dependency order → `Putting it together`
(one realistic end-to-end build) → `Debugging & common errors` → `Performance & trade-offs` →
`Ecosystem & alternatives` → `Where to go next` → appendix.

### Digest (their slides / PDFs / notes)
One chapter per source section, in the source's order — then **the chapters the source
skipped**. Slides are headings; the course is what the lecturer said around them. For every
slide bullet, ask "what would a student have to already know for this line to make sense?"
and add that as a chapter or a section. Cite the source location (`Lecture 4, slide 12`)
in the chapter description so the user can cross-check.

### Codebase
Non-negotiable chapters, on top of the per-module ones:

1. **What this project is** — the problem it solves, in user terms, and the one-paragraph pitch
2. **Prerequisite stack** — every framework/library/pattern used, taught, not just listed
3. **Architecture** — the map, with an inline-SVG diagram; where a request/action actually goes
4. **Data model** — every table/collection/type and what it means
5. **Module by module** — one chapter per meaningful directory: what it does, its public surface,
   its dependencies, file paths for everything you claim
6. **The critical flows** — trace 2–4 real end-to-end paths line by line, file by file
7. **Conventions** — naming, error handling, testing style, what the team clearly cares about
8. **How to run, test, debug it** — actual commands, verified to exist in the repo
9. **Where the project stands** — done / in progress / stubbed / broken / TODO, each with the
   file path and the evidence (a `TODO`, a failing test, an empty handler, a recent commit).
   Include what is *deliberately* not done.
10. **How to make the five most common changes** — step by step, naming the files to touch
11. **Traps** — the things that will bite someone who assumes the obvious

Evidence rule: every factual claim about the codebase names a file, and preferably a line.
If you did not read it, do not claim it. If something is genuinely unclear, say so in the
chapter as an open question — an honest unknown is content; a confident guess is damage.

## SYLLABUS.md format

`verify.py` parses this file. Keep the shape.

```markdown
# <Course title>

**Destination:** what the user asked for, in one line
**Learner level assumed:** …
**Language:** …

## Chapters

- `ch-1` — Why concurrency exists — *must know because every later chapter assumes the problem*
- `ch-2` — Processes, threads and the scheduler — *prerequisite, axis 1*
- `ch-3` — Your first goroutine — *core*
…
- `ch-appendix` — Glossary, cheat sheet, what to learn next

## Coverage ledger

Every concept found in the source material (or demanded by the atlas) maps to a chapter.
Nothing here may stay unchecked at hand-over.

- [x] Lecture 3, slide 8 — "goroutines are cheap" → `ch-3`
- [x] Lecture 3, slide 9–14 — channel syntax → `ch-6`
- [x] axis-1 gap: student has never seen a thread → `ch-2`
- [x] `lib/ai/pipeline.ts` five-stage generation → `ch-7`

## Deliberately out of scope

- Distributed tracing — belongs to a different course; named in `ch-appendix` under what's next
```

Anything you decide to drop goes under **Deliberately out of scope** with a reason, and gets
a mention in the "what to learn next" appendix. Dropping silently is the failure mode this
whole document exists to prevent.

## Show the syllabus before authoring

Print the chapter list to the user and start writing. Do not wait for approval unless they
asked to review it — but if they trim it, record the trim under *Deliberately out of scope*
rather than deleting the line.
