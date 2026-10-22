# Writing chapters that land

The goal of every chapter: the reader understands **one idea** well enough to use it and
explain it. Everything in this file serves that.

## Spend words where understanding is made

This is the rule that decides whether a course is worth reading. **Depth follows difficulty,
not data.** A chapter gets long where the idea is hard for *this* reader, and stays short
everywhere else, however many facts you happen to have about those parts.

Courses fail in two directions at once, and usually in the same chapter:

- **Long where it should be short.** The run log narrated in prose (0.7761 → 0.7764, 104
  customers, 4,307 rows), file names and ids from the running example, library versions,
  every option and parameter range, a tokenizer quirk. The reader wades through it looking
  for the point.
- **Short where it should be long.** The idea the chapter exists for gets one clause in
  brackets — "vector store (ที่เก็บ embedding ที่ค้นได้เร็ว)" — or a bullet with no *because*.
  The reader finishes it able to repeat the words, not to explain them.

So before writing a chapter, settle three things (in your head or in `.work/`, not on the page):

1. **The takeaway** — the one sentence the reader should be able to say afterwards.
2. **The hard parts** — the one to three places where this reader will get stuck: a
   mechanism they can't picture, a *why* that isn't obvious, a step that looks wrong. These
   get the words.
3. **Everything else is supporting** — one line each, or cut.

| Give it room | Keep it to a line | Cut, or move to a `.more` |
|---|---|---|
| The mechanism behind the takeaway: what happens, step by step, on one concrete case | Setup: which data, which library, how to install | How the sample data was generated, seeds, run logs |
| Why it works — and why the obvious alternative doesn't | A term the reader will use but doesn't need to understand deeply | Library versions, ids, file paths (unless the reader types them) |
| The point where beginners go wrong, and how they'd notice | A fact that matters but needs no explaining | Every option, parameter range or alternative tool |
| The picture or analogy that makes it click — and where it breaks | A pointer to another chapter | Exact measurements beyond the one that makes the point |

### How to explain a hard part

Write it the way a good senior explains at a whiteboard — in full sentences, joined by the
words that carry the logic (*because, so, but, which means, unless* — in Thai เพราะ, จึง,
แต่, แปลว่า, ถ้า…ก็…). Bullets delete those words; that is why a chapter of bullets reads
like notes instead of teaching. A good explanation usually runs:

1. **The problem it solves**, in the reader's terms, before what it is.
2. **A mental model** — a plain-language picture or an analogy closer to the reader's life
   than the real thing.
3. **The real mechanism on one small case** — the actual steps, with the numbers that show
   it working.
4. **Why it works, and why not the obvious alternative** — answer the question the reader is
   about to ask ("แล้วทำไมไม่…?").
5. **Where the model breaks**, if an analogy was used.

Not every part needs all five. The takeaway's mechanism almost always needs 2–4.

Then close each hard part properly — these are the gaps a reader trial found in otherwise
good chapters:

- **State the rule exactly once you've explained it.** The intuition comes first, then the
  precise form the reader will need later — the formula (`precision = TP ÷ (TP + FP)`), the
  signature, the definition. Words are not a substitute for the formula; the formula is not a
  substitute for the words.
- **Never let the text lean on the picture.** Say in the prose what the axis is and which way
  "left" or "up" goes. On a phone the figure is small, or scrolled past.
- **A summary number says what it computes.** "PR-AUC is roughly the average precision as
  recall goes from 0 to 100%", not "it summarises precision and recall".
- **When you show two ways, say which to use.** The formula or the scan? The default or the
  tuned value? End with the rule a practitioner follows, and what it means when the two
  disagree.
- **Don't contradict your own advice.** A chapter that says "open the test set once" cannot
  run its calibration check on the test set without saying why that one look is allowed.
- **Cutting the options is not cutting the default.** "Measure it" needs a place to start:
  give the usual starting value (chunks of ~200–500 tokens, k of 3–8) and what makes you move
  it, even when every other option is cut.
- **Code the reader may copy runs as shown**, or says in a comment where its setup comes
  from (`# client and MODEL as set up in บทที่ 10`). A line that looks odd
  (`token_pattern=None`) gets its reason, in a comment or a sentence.
- **Every flag and new command in a block the reader will run is explained where it first
  appears** — `-t myapp .`, `-it`, `--build` — in a comment or a sentence. If it isn't worth
  explaining, it isn't in the block.
- **Say when you're showing the toy version.** A development server, a password in a file, a
  shortcut that only works on one machine: one line on what to use for real.
- **Numbers earn their place when the comparison is the point.** "The off-topic question
  scores 0.24, the right paragraph only 0.22 — no cut-off separates them" makes the point in
  one line; the same idea without the two numbers asks the reader to take it on trust.

### Numbers

A number is there to make a point visible. Keep the one that does; drop the rest.

- **One or two numbers per point.** "สองตัวที่ต่างกันแค่จังหวัดได้คะแนนห่างกันเกือบ 0.08" — not
  five figures in a row.
- **Round in prose** to what the reader can hold: 0.776 → about 0.78, 33.5% → about a third.
  Exact values stay where they came from: the code output, a table, a worked `.eg`.
- **Never narrate a log.** If the output block already shows it, the prose says what it
  *means*, not what it *says*.

### The running example is a backdrop

Reusing one scenario across chapters is good; making the reader track its inventory is not.
Refer to it in plain words ("นโยบายคืนสินค้า", "ลูกค้าที่ซื้อบ่อย"), not by its ids
(`returns.md#2`, `c26`, order 100247) — ids belong in code. Point to another chapter only
when the reader should actually go back to it; a chapter studded with "บทที่ N" sends the
reader away instead of teaching them here.

### The same passage, done badly and done well

```html
<!-- before: the ids, the tokenizer and the library version get the room;
     the idea the section exists for (why embedding search finds meaning) gets one clause -->
<p>ชิ้นที่ตอบได้คือ returns.md#2 แต่มันหลุดจาก top-3 เพราะการค้นด้วยคำเห็นแค่ตัวอักษร</p>
<ul>
  <li><strong>คำต่างกัน:</strong> "พัง" กับ "ชำรุด"</li>
  <li><strong>ตัดคำไม่ตรง:</strong> ตัวตัดคำแยก "ขนส่ง" กับ "การขนส่ง" เป็นสอง token</li>
</ul>
<p>embedding แก้จุดนี้ได้ เพราะประโยคความหมายใกล้กันได้เวกเตอร์ใกล้กัน ระบบจริงเก็บไว้ใน vector store
(ที่เก็บ embedding ที่ค้นได้เร็ว) ตัวอย่างนี้ใช้ chromadb 1.5</p>

<!-- after: the problem in the reader's terms, then the mechanism, with its why -->
<p>ลูกค้าพิมพ์ว่า "ของพังมาจากขนส่ง" แต่เอกสารของร้านเขียนว่า "สินค้าชำรุดจากการขนส่ง" การค้นด้วยคำ
เทียบตัวอักษรตรงๆ เมื่อไม่มีคำว่า "พัง" ในเอกสาร ย่อหน้าที่ถูกจึงได้คะแนนต่ำจนหลุดอันดับ ทั้งที่คนอ่าน
รู้ทันทีว่าพูดเรื่องเดียวกัน</p>
<p><strong>embedding</strong> แก้ตรงนี้ เพราะมันไม่ได้เก็บตัวอักษร แต่แปลงความหมายของประโยคเป็นตัวเลขชุดหนึ่ง
โมเดลที่สร้างตัวเลขนี้ถูกฝึกจากข้อความจำนวนมาก จนเห็นว่า "พัง" กับ "ชำรุด" ถูกใช้ในบริบทเดียวกัน
ประโยคที่พูดเรื่องเดียวกันจึงได้ตัวเลขใกล้กัน แม้ไม่มีคำซ้ำกันสักคำ</p>
<p>การค้นจึงเปลี่ยนจาก "หาย่อหน้าที่มีคำเดียวกับคำถาม" เป็น "หาย่อหน้าที่ตัวเลขใกล้กับคำถามที่สุด"
ที่เก็บตัวเลขพวกนี้และหาตัวที่ใกล้ที่สุดได้เร็วเรียกว่า <strong>vector store</strong></p>
```

The "after" is longer where the idea is, and has no ids, no tokenizer detail and no version.

## The chapter recipe

```
<section class="chapter" id="ch-N" data-title="Short title">
  header: title + .ch-desc (one sentence: what the reader can do after this)
  1. The hook        1–3 sentences: the question or problem, in the reader's terms
  2. The example     a concrete case, worked through, that shows the problem or the idea
  3. The idea        the takeaway explained — this is where the chapter's words go
  4. The picture     a figure, if the idea is a flow, shape, comparison or change over time
  5. Using it        how it is applied for real: the code, the steps, the decision
  6. The trap        the one mistake people actually make, and how to spot it
  7. Quick check     optional: 1–3 questions that need the idea, not the wording
</section>
```

- **150–700 words of prose** (see the depth table in SKILL.md). A chapter that needs more is
  two ideas — split it — or carries supporting detail that should be cut.
- **0–3 `<h2>`**, each a short phrase that says the point ("Why the tail, not the point"),
  never a label ("Overview", "Introduction", "Summary").
- The hook needs no heading; the first paragraph *is* the hook.
- **End on the takeaway** in one memorable line when it helps — a rule of thumb the reader
  can act on ("ตอบผิดเมื่อไร ดูขั้นค้นก่อนเปลี่ยนโมเดล"), not a recap paragraph.

## Shape: prose reasons, structure holds parallel things

Explanation is **prose** — short paragraphs of two to four sentences, one point each, the
point first. Structure is for content that really has that shape:

| When the text holds… | Write it as |
|---|---|
| a *because* — A, so B, so C | prose |
| 3+ separate options, symptoms, checks — each a complete thought | a list |
| an order (do this, then this) | `.steps` or `<ol>` |
| items compared on the same attributes | a table (≤ 4 columns) |
| right vs wrong, before vs after | `.cmp` |
| a number being worked out | `.eg`, one line per step |
| optional depth only some readers want | `.more` (collapsed), at most two per chapter |

- **Paragraphs stay under ~60 words** (Thai, Lao, Khmer and Burmese count 5 characters as a
  word, so ~300 characters). Three short paragraphs in a row are fine; a run of long ones
  needs the example, the code or the figure between them.
- **No "label: fragment" bullets for a story.** "ที่เห็น: … / สาเหตุ: … / แก้: …" chops one
  chain of reasoning into notes and deletes the *because*. Write it as two or three sentences.
- **A list item is a complete thought**, not a key phrase with a number after a colon.
- **`.more` is not a dumping ground.** Most detail should simply go. Use it for depth a
  motivated reader will want (how to choose the parameter, the edge case, the formal
  version) — never for the takeaway itself.

**One home per point.** Explaining fully is not explaining twice. Once a paragraph has made a
point, the caption says what to look at in the figure, not the point again; no callout
repeats it; the quiz asks the reader to apply it, not to recall the sentence above. A rule
stated three times — in the text, a caption and a box — is the most common padding in a
chapter that otherwise explains well.

`verify.py` warns past a ceiling — paragraphs over ~60 words, long runs of paragraphs,
chapters dense with figures in prose, "label:" lists, many chapter references — so passing
the gate is not the target; reading well is.

There is no objectives box, no recap and no glossary unless they earn their place: a recap is
worth it after a long `deep` chapter; a glossary appendix is worth it when the course coins
more than ~10 terms. A chapter that already says something clearly does not need a box that
says it again.

## Examples are the explanation

A reader who sees the idea work once understands it; a reader given only a definition
memorises words.

A good example is:

- **Concrete.** Real numbers, real names, real output: "a ฿1,200 bill split 3 ways", an
  `order` table, an actual error message — never `foo`, `X`, "some value".
- **Small enough to hold in your head.** Three rows, not thirty. Numbers you can check.
- **Worked, not just stated.** Show the steps and the result. For code, show the output in
  `.code-out`. For a calculation, show each line.
- **Followed by one variation.** Change one thing and show what changes — that is where the
  rule becomes visible.
- **Talked through.** After the output, say what it shows and why — the reader should not
  have to reverse-engineer the lesson from a printout.

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
| Prose that re-reads the code output aloud | Say what it means, once. |
| A run log in prose: every measured value, count and decimal | Keep the number that makes the point. |
| Ids, file names, versions and seeds of the running example in prose | They belong in code; say it in plain words. |
| Every option, parameter range or alternative tool | Teach the default and when to change it; the rest is docs. |
| Lists of terms or features with one-line glosses | An index is not a lesson. Teach the two that matter. |
| Background/history that doesn't explain *why* it works this way | Cut, or one sentence. |
| Generic advice ("practise regularly", "read the docs", "ฝึกฝนอย่างสม่ำเสมอ") | Not specific to this idea. |
| Hedging stacks ("may potentially in some cases") | One qualifier, where it is true. |
| Three callouts in a row | A page of boxes has no emphasis. Max two per chapter. |
| "etc.", "and so on", "เป็นต้น" closing a list that matters | Finish the list, or say the list is open and why. |

## Prose

- **Second person, present tense, plain words.** "You call `fetch` and get a promise back."
- **Bold** the term being defined, once, and in a table the one figure the reader should
  look at. Nothing else.
- **Introduce a central term properly** — what problem it solves, what it is, one concrete
  instance — in a sentence or three, where it is first used. A bracketed gloss is only for
  terms the reader needs to recognise, not understand. Original term first when the course
  is not in English: `**closure** (ฟังก์ชันที่จำตัวแปรรอบตัวไว้ได้)` — then keep using the original.
- A table when items share attributes — at most 4 short columns, or it scrolls sideways on a
  phone. Define a term before the table that uses it as a header. A figure when the point is a
  shape. A diagram that flows left to right stacks vertically on a phone; keep it to 3–5 boxes.
- One closing line that bridges to the next chapter is fine; a paragraph previewing it is not.
- Never say "left" / "right" / "above" about a `.cmp`, `.flow` or table: on a phone they stack.
  Name the box instead ("the http:// box").
- A URL, a filename or one line someone sees goes in inline `<code>` (it wraps). A `.code`
  block is for real code or output of several lines.
- Never translate code, commands, file paths, error messages or product names.
- **Write the language natively** — its own rhythm, register and established technical
  terms — not English sentence structure in another language. In Thai: complete sentences
  with a subject and a verb, the way a senior colleague explains out loud; keep the English
  for terms the field really uses (embedding, prompt, API) and say everything else in Thai —
  not "ห่อ chunk ด้วย id แล้ว retrieve top-k" but "แนบหมายเลขกำกับแต่ละชิ้น แล้วดึงชิ้นที่ใกล้ที่สุด
  สามชิ้น". Give the English once in brackets for a Thai term, and don't open paragraphs with
  stacked connectors (นอกจากนี้ / อย่างไรก็ตาม / ดังนั้น) by habit. The Thai target style is
  `assets/examples/example-chapter-th.html`.
- **Every label in the course language** — example titles, box titles, `.cmp` headings. Leave
  `.quiz-h` and `.ch-label` empty; the page fills them. Thai, Lao, Burmese and Khmer take no
  full stop: end a Thai sentence with a space, or start a new paragraph.

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
  the question's words, or is the paragraph just above restated, rewrite it.
- Every wrong option is a mistake someone would really make, and carries `data-why` — one
  sentence on why it is tempting and where it breaks.
- Options of similar length and tone. The page shuffles them; never write "all of the above"
  or refer to option letters.
- `.fb` explains the right answer in one or two sentences — the reasoning, not a measured
  decimal.

An exercise (`.ex`) is better than a quiz when the skill is *doing* something (write the
query, solve the problem). Put the solution in `<details>` with one line on why it works.

## Input types

**A topic** ("teach me X"): what it is for (the hook of chapter 1) → the core idea with the
best example → the 1–3 ideas that build on it → how it is used for real / the common traps.
A course on a tool the reader will use at work ends with a one-screen recipe for their own
case — the steps and commands in order, each pointing back to the chapter that explains it.

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

**Security and privacy topics:** explain the mechanism in general terms — no real bank,
company or person as the bad example, no exact figures you cannot source, and say plainly what
the protection does *not* cover.

**Explaining to a non-specialist:** an everyday analogy first if it helps, then the real
mechanism in one small worked example (small numbers, a real error message), then where the
analogy breaks. Keep the real thing — it is what makes the analogy trustworthy — but keep it
small.

**No sources and no way to check?** Then current legal limits, official rates and fees are not
yours to state — they change by notice and memory is out of date. Teach the mechanism with a
figure labelled as an example ("สมมติดอกเบี้ย 16% ต่อปี"), compute every number from it, and
tell the reader exactly where the real value is (their statement, the contract, the
regulator's site).
