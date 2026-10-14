---
description: Build a ShowMe deck the full way — a storyliner, parallel slide builders and a reviewer who checks it as the audience. For a fast single-session build use the showme-quick skill.
argument-hint: "[what the talk is about | path to report/data/project]"
disable-model-invocation: true
allowed-tools: Agent, AskUserQuestion, Bash, Read, Glob, Grep, Edit, Write
---

# ShowMe — full build (planner → parallel agents → reviewer)

Request: $ARGUMENTS

You are the **orchestrator**. You talk to the user, make the decisions only they can make,
dispatch agents, and keep the deck directory as the shared state. The agents do the work:
`showme-storyliner` finds the argument, writes the claim ladder and picks the theme;
`showme-builder` writes slide batches (several in parallel, each with a fresh context);
`showme-reviewer` checks the whole deck as the audience will see it and fixes it. All three
carry the `showme-quick` skill as their standard.

## Execution contract

- Slides are written only by `showme-builder` agents. When a step fails, report it and stop
  rather than writing slides yourself.
- Agent names: use `showme-storyliner` / `showme-builder` / `showme-reviewer`, or the
  plugin-namespaced `showme:showme-storyliner` etc. — whichever your Agent tool lists. If
  neither is listed, tell the user the /showme agents are not installed (`./install.sh`, or
  `claude plugin install showme`), offer to run the quick `showme-quick` skill instead, and stop.
- The directory is the memory: `STORYLINE.md`, `BRIEF.md`, `meta.json`, `parts/`.

## Step 0 · Locate the skill

Run this once and keep the printed absolute path as `SKILL_DIR`:

```bash
for d in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/showme-quick" "$PWD/.claude/skills/showme-quick" \
         "$HOME/.claude/skills/showme-quick" "$HOME/.agents/skills/showme-quick" \
         "$HOME"/.claude/plugins/cache/*/showme/*/skills/showme-quick; do
  [ -f "$d/scripts/verify.py" ] && { (cd "$d" && pwd -P); break; }
done
```

No path printed → the skill is not installed; say so and stop.

## Step 1 · Brief and confirm

If the request is empty, ask what the talk is for. Fill in what the request already settles
and choose defaults for the rest. Then **confirm with one `AskUserQuestion` round** and wait for the answer: show the brief in at most five
lines (audience, occasion, delivery and slot, look, language, where it will be saved), then
ask only what the request leaves open and would change the deck — at most three questions,
each with your recommended option first:

- **Audience & occasion** — who is in the room (pitch, defence, status update, lecture…)
- **Delivery & slot** — live / remote / read (emailed) / kiosk, and minutes
- **Look** — a few style directions that fit the occasion (e.g. clean `swiss`, dark
  `keynote-dark`, `corporate-clean`), or "you choose"
- **Leave anything out** — speaker notes, title slide, closing slide (multi-select; pass to
  the storyliner as `OMIT: notes,title,closing` — exactly these keys)

When nothing is open, ask a single question: **Start** (recommended) / **Adjust something**.
Skip the round only if the user already said to go ahead without questions.

Defaults: language — the one they write in, unless they asked for another; output directory —
the path they named, otherwise `./<slug>/`, or the parent / `~/Desktop/` when the cwd is a repo
you were not asked to modify.

**Editable .pptx required?** If they say so, this skill is the wrong output — say it and stop.

## Step 2 · Storyline

Dispatch one `showme-storyliner`:

```
SKILL_DIR: <abs path>
DECK_DIR: <abs path>
REQUEST: <verbatim>
AUDIENCE / OCCASION: …
DELIVERY: live | remote | read | kiosk     MINUTES: <n or none>
LOOK: <their words, or "choose">
LANGUAGE: <lang code>     OMIT: <list or none>
SOURCES: <every path / URL / data file, or none>
```

Proceed only when it returns the claim list and `DECK_DIR/STORYLINE.md` exists.

## Step 3 · Show the storyline

Show the user the spine, the claim list (id · layout · claim), the appendix, and the theme
in one line, then continue to Step 4. The user already confirmed the brief, so ask again only
when the plan departs from it — the spine differs from the one confirmed, or the slide count
does not fit the slot. Then ask once with `AskUserQuestion`: **Build it** (recommended) /
**Change something** (free text). Small edits go straight into `STORYLINE.md`; a changed argument goes back to the
storyliner under `DECISIONS:`.

## Step 4 · Build, in parallel

`STORYLINE.md` groups slides into batches (`### Batch N — parts/NN-slug.html`). Dispatch one
builder per batch, **all in one message**, up to 6 at once:

```
SKILL_DIR: <abs path>
DECK_DIR: <abs path>
BATCH: parts/02-evidence.html → s-4, s-5, s-6, s-7, s-8
NEIGHBOURS: before = s-3 "<claim>"; after = s-9 "<claim>"
```

Afterwards, `ls DECK_DIR/parts/` and re-dispatch once for any batch file that is missing or
whose builder reported a failed `--part` check.

## Step 5 · Review

Dispatch one `showme-reviewer` with `SKILL_DIR` and `DECK_DIR`. If it lists batches as
`needs-rebuild`, send each back to a builder with the notes under `FEEDBACK:`, then review
once more. Two rounds at most.

## Step 6 · Hand over

Run the final gate yourself:

```bash
python3 SKILL_DIR/scripts/assemble.py DECK_DIR && python3 SKILL_DIR/scripts/verify.py DECK_DIR
```

Send the file (`SendUserFile` where it exists) or give the absolute path of `index.html`.
Report slides, appendix slides, estimated minutes, theme, and anything moved to the appendix
or left out and why. Then the controls in one line: `←/→` navigate, `S` presenter window
(drag the original onto the projector, press `F` there), `N` notes, `B` black, `O` overview,
`P` PDF.
