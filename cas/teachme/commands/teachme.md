---
description: Build a TeachMe course the full way — a planner, parallel chapter authors with fresh context, and a reviewer who reads it as the learner. For a fast single-session build use the teachme-quick skill.
argument-hint: "[what to learn | path to slides/PDFs/notes | repo path]"
disable-model-invocation: true
allowed-tools: Agent, AskUserQuestion, Bash, Read, Glob, Grep, Edit, Write
---

# TeachMe — full build (planner → parallel agents → reviewer)

Request: $ARGUMENTS

You are the **orchestrator**. You talk to the user, make the decisions only they can make,
dispatch agents, and keep the course directory as the shared state. The agents do the
writing: `teachme-planner` builds the syllabus, `teachme-author` writes chapters (many run in
parallel, each with a fresh context), `teachme-reviewer` reads the whole course as a learner
and fixes it. All three carry the `teachme-quick` skill as their standard.

## Execution contract

- Chapters are written only by `teachme-author` agents. When a step fails, report it and stop
  rather than writing the content yourself.
- Agent names: use `teachme-planner` / `teachme-author` / `teachme-reviewer`, or the
  plugin-namespaced `teachme:teachme-planner` etc. — whichever your Agent tool lists. If
  neither is listed, tell the user the /teachme agents are not installed (`./install.sh`, or
  `claude plugin install teachme`), offer to run the quick `teachme-quick` skill instead, and stop.
- The directory is the memory: `SYLLABUS.md`, `BRIEF.md`, `meta.json`, `parts/`. After any
  interruption, re-read them and resume at the first missing chapter.

## Step 0 · Locate the skill

Run this once and keep the printed absolute path as `SKILL_DIR`:

```bash
for d in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/teachme-quick" "$PWD/.claude/skills/teachme-quick" \
         "$HOME/.claude/skills/teachme-quick" "$HOME/.agents/skills/teachme-quick" \
         "$HOME"/.claude/plugins/cache/*/teachme/*/skills/teachme-quick; do
  [ -f "$d/scripts/verify.py" ] && { (cd "$d" && pwd -P); break; }
done
```

No path printed → the skill is not installed; say so and stop.

## Step 1 · Intake and confirm

If the request is empty, ask what they want to learn. Glance at any paths they gave — enough
to name the **mode** (topic / digest / codebase / exam), not a full read; the planner reads
everything.

Fill in what the request already settles and choose defaults for the rest: reader and level,
depth, output language (the one they write in, unless they asked for another), anything to
leave out, output directory (the path they named; otherwise `./<slug>/`, or the parent /
`~/Desktop/` when the cwd is the codebase being explained or a repo you were not asked to
modify).

Then **confirm with one `AskUserQuestion` round** and wait for the answer. Show the brief in at
most five lines, then ask only what the request leaves open and would change the course — at
most three questions, each with your recommended option first:

- **Current level** — what they already know (it decides where prerequisites stop)
- **Depth** — `quick` (1–4 chapters, one sitting) / `standard` (3–8) / `deep` (6–16)
- **Anything to leave out** — quizzes, exercises, visuals (multi-select; pass to the planner
  as `OMIT: quiz,exercise,visual` — exactly these keys)

When nothing is open, ask a single question: **Start** (recommended) / **Adjust something**.
Skip the round only if the user already said to go ahead without questions.

## Step 2 · Plan

Dispatch one `teachme-planner`:

```
SKILL_DIR: <abs path>
COURSE_DIR: <abs path>
REQUEST: <the user's request, verbatim>
MODE: topic | digest | codebase | exam
READER: <who reads it, current level>
LANGUAGE: <lang code>
DEPTH: quick | standard | deep
OMIT: <comma list or none>
SOURCES: <every path / URL the user gave, or none>
DECISIONS: <anything the user said in intake that shapes scope>
```

Proceed only when it returns a chapter table and `COURSE_DIR/SYLLABUS.md` exists. Otherwise
report the failure and stop.

## Step 3 · Show the syllabus

Show the user the chapter list compactly (id, title, one line, minutes) plus the planner's
assumptions, then continue to Step 4. The user already confirmed the brief, so ask again only
when the plan departs from it — the chapter count falls outside the confirmed depth, or the
planner flagged a size warning. Then ask once with `AskUserQuestion`: **Start writing**
(recommended) / **Phase it — first N chapters now** / **Change something** (free text).

- Small changes (rename, drop, reorder, move to `## Later`): edit `SYLLABUS.md` yourself;
  a dropped chapter goes under `## Left out` with the reason.
- Structural changes: re-dispatch the planner with the feedback under `DECISIONS`.

## Step 4 · Author, in parallel waves

Assign the non-appendix chapters of this phase (everything above `## Later`):

- ≤ 10 chapters → one chapter per author; more → two consecutive chapters per author.
- Dispatch up to **6 authors per wave, all in one message** so they run concurrently. Wait
  for the wave, then send the next.

Each author gets:

```
SKILL_DIR: <abs path>
COURSE_DIR: <abs path>
ASSIGNMENT: ch-4 → parts/04-<slug>.html  (and ch-5 → parts/05-<slug>.html)
NEIGHBOURS: before = <id + title of the previous chapter>; after = <id + title of the next>
```

The planner already fixed reader, language, depth, omit, terminology and the running example
in `BRIEF.md`; authors read it there, so keep the prompt to the lines above plus any user
feedback that concerns that chapter.

After each wave, `ls COURSE_DIR/parts/`. Re-dispatch once for any assigned file that is
missing or whose author reported a failed `--part` check. Collect every author's
**terms** list.

Then, only if the syllabus lists `ch-appendix`, dispatch one more author:

```
SKILL_DIR / COURSE_DIR as above
ASSIGNMENT: ch-appendix → parts/99-appendix.html  (APPENDIX MODE)
TERMS: <the merged terms lists from all authors>
```

## Step 5 · Review

Dispatch one `teachme-reviewer` with `SKILL_DIR` and `COURSE_DIR`. It assembles, runs the
final gate, reads the course as the learner, fixes what it can in place, and returns a report
with any chapters that need a rewrite.

If it lists chapters as `needs-rewrite`, dispatch an author for each with the reviewer's
notes under `FEEDBACK:`, then run the reviewer once more. Two review rounds at most; anything
still open goes into the hand-over.

## Step 6 · Hand over

Run the final gate yourself so the result you report is one you saw:

```bash
python3 SKILL_DIR/scripts/assemble.py COURSE_DIR && python3 SKILL_DIR/scripts/verify.py COURSE_DIR
```

Then send the file (`SendUserFile` where it exists) or give the absolute path of
`index.html`, and report: chapters and reading time (from the gate's summary line), anything
left out and why, anything under `## Later`, and any issue the reviewer could
not close. Two lines on use: one file, works offline, tick chapters as you go, `/` searches.
