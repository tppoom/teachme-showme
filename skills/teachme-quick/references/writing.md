# Writing chapters that land

The goal of every chapter: the reader understands **one idea** quickly and could use it or
explain it. Everything in this file serves that.

## The chapter recipe

```
<section class="chapter" id="ch-N" data-title="Short title">
  header: title + .ch-desc (one sentence: what the reader can do after this)
  1. The hook        1–3 sentences: the question or problem, in the reader's terms
  2. The example     a concrete case, worked through, with real numbers or real output
  3. The idea        now name the rule — it should feel obvious after the example
  4. The picture     a figure, if the idea is a flow, shape, comparison or change over time
  5. The trap        the one mistake people actually make, and how to spot it
  6. Quick check     optional: 1–3 questions that need the idea, not the wording
</section>
```

- **150–700 words of prose** (see the depth table in SKILL.md). A chapter that needs more is
  two ideas — split it, or cut what repeats.
- **0–3 `<h2>`**, each a short phrase that says the point ("Why the tail, not the point"),
  never a label ("Overview", "Introduction", "Summary").
- **Paragraphs of 1–4 sentences.** Lead with the answer, then the reason.
- The hook needs no heading; the first paragraph *is* the hook.

There is no objectives box, no recap and no glossary unless they earn their place: a recap is
worth it after a long `deep` chapter; a glossary appendix is worth it when the course coins
more than ~10 terms. A chapter that already says something clearly does not need a box that
says it again.

## Examples are the explanation

The single most important thing in a chapter. A reader who sees the idea work once
understands it; a reader given only a definition memorises words.

A good example is:

- **Concrete.** Real numbers, real names, real output: "a ฿1,200 bill split 3 ways", an
  `order` table, an actual error message — never `foo`, `X`, "some value".
- **Small enough to hold in your head.** Three rows, not thirty. Numbers you can check.
- **Worked, not just stated.** Show the steps and the result. For code, show the output in
  `.code-out`. For a calculation, show each line.
- **Followed by one variation.** Change one thing and show what changes — that is where the
  rule becomes visible.

Use the `.eg` block for a worked example that is not just a code block:

```html
<div class="eg">
  <span class="eg-h">Example — splitting a ฿1,200 dinner, one person had no drinks</span>
  <p>Food ฿900, drinks ฿300 shared by two of the three.</p>
  <ol><li>Food: 900 ÷ 3 = ฿300 each</li><li>Drinks: 300 ÷ 2 = ฿150 for the two drinkers</li></ol>
  <span class="res">Non-drinker pays ฿300; the other two pay ฿450 each.</span>
</div>
```

Good example forms by subject: code → runnable snippet + output (`.code`, `.walk` when the
execution order is not the line order); maths/finance/science → a worked calculation with
real numbers (`.eg`, `.math` + `.where`); concepts → a before/after or right/wrong pair
(`.cmp`); processes → steps with what you see at each (`.steps`); language → a real sentence
broken into parts (`.annot`, `.dlg`); history/law → the actual event or clause (`.quote`,
`.timeline`). Analogies are allowed only when they are closer to the reader's life than the
real thing — and say where the analogy breaks.

## The cut list

Delete on sight. The gate warns on many of these.

| Cut | Why |
|---|---|
| "In this chapter we will…", "Let's dive into…", "ในบทนี้เราจะมาเรียนรู้…" | Just start. |
| "It is important to note that…", "สิ่งสำคัญที่ควรรู้คือ…", "เป็นเรื่องที่สำคัญมาก" | If it matters, say it plainly; the reader can tell. |
| "In today's fast-moving world…", "ในยุคปัจจุบัน…", "ในโลกยุคดิจิทัล…" | Says nothing. |
| "As we saw earlier…", "อย่างที่กล่าวไปแล้ว…" | Either it is needed (say it) or it isn't (cut it). |
| A closing paragraph that restates the section | The reader just read it. |
| Lists of terms or features with one-line glosses | An index is not a lesson. Teach the two that matter. |
| Background/history that doesn't explain *why* it works this way | Cut, or one sentence. |
| Generic advice ("practise regularly", "read the docs", "ฝึกฝนอย่างสม่ำเสมอ") | Not specific to this idea. |
| Hedging stacks ("may potentially in some cases") | One qualifier, where it is true. |
| Three callouts in a row | A page of boxes has no emphasis. Max two per chapter. |
| "etc.", "and so on", "เป็นต้น" closing a list that matters | Finish the list, or say the list is open and why. |

## Prose

- **Second person, present tense, plain words.** "You call `fetch` and get a promise back."
- **Bold** only the term being defined, once.
- **Define a term where it is first used**, in one clause. Original term first when the course
  is not in English: `**closure** (ฟังก์ชันที่จำตัวแปรรอบตัวไว้ได้)` — then keep using the original.
- Bullets only for genuinely parallel items (≤ 6). A list that is secretly a paragraph is a
  paragraph.
- A table when items share attributes. A figure when the point is a shape. Prose when the
  point is a *because*.
- Never translate code, commands, file paths, error messages or product names.
- Write the language natively — its own rhythm, register and established technical terms —
  not English sentence structure in another language. In Thai, prefer short sentences, use
  the common Thai term where one exists and give the English once in brackets, and don't
  open paragraphs with stacked connectors (นอกจากนี้ / อย่างไรก็ตาม / ดังนั้น) by habit.

## Markup traps that show up as bugs

- This is **HTML, not Markdown.** `**bold**`, `# Heading`, `` `code` `` and ``` fences
  render literally. Use `<strong>`, `<h2>`, `<code>`, `<div class="code"><pre><code>`.
- Inside `<code>`, write `&lt;` `&gt;` `&amp;`. A raw `<div>` or `List<String>` in code is
  swallowed by the browser and silently disappears.
- One chapter per file, one `<section class="chapter">` per file, every tag closed.
- SVG ids are document-wide: prefix them with the chapter (`id="ch3-clip"`).
- Never hard-code colours in diagrams; use the `.d-*` classes or the block library, so dark
  mode works.

## Quick checks (optional quiz)

Use a quiz when the idea can be misapplied — 1–3 questions per chapter, never more than 4.

- Ask the reader to **apply** the idea to a **new case**: predict an output, spot the bug,
  pick the right option for a situation. If the answer can be found by searching the text for
  the question's words, rewrite it.
- Every wrong option is a mistake someone would really make, and carries `data-why` — one
  sentence on why it is tempting and where it breaks.
- Options of similar length and tone. The page shuffles them; never write "all of the above"
  or refer to option letters.
- `.fb` explains the right answer in one or two sentences.

An exercise (`.ex`) is better than a quiz when the skill is *doing* something (write the
query, solve the problem). Put the solution in `<details>` with one line on why it works.

## Input types

**A topic** ("teach me X"): what it is for (the hook of chapter 1) → the core idea with the
best example → the 1–3 ideas that build on it → how it is used for real / the common traps.

**Source material** (slides, PDF, notes): follow the source's order, one chapter per major
section, but write what the lecturer would *say* around each slide — slides are headings.
Cover every important point (track them under `## Coverage` in SYLLABUS.md); merge thin
sections; fill gaps the source assumes in a sentence where needed.

**A codebase**: what it does (in user terms) → the architecture as one figure → the 2–3 flows
that matter, traced through real files with paths → how to run and change it → where it stands
(done / in progress / broken, each with the file and the evidence). Every claim names a file;
if you didn't read it, don't claim it.

**An exam**: one chapter per exam domain, weighted by marks; practice in the exam's own
question format; the traps the examiners set; a short strategy chapter. Write original
questions — never copy past papers.

## Accuracy

Date anything that changes (laws, prices, versions, guidelines). Cite what can be checked;
never invent a statistic, case or quote — say the source needs checking instead. For health,
law and money, teach how things work and name who to consult; don't advise on a specific case.
