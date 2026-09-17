#!/usr/bin/env python3
"""Scaffold a course directory so the shape is right before you write a word.

Usage:
  python3 new.py <dir> --title "…" --lang th [--subtitle "…"] [--id slug]

Creates <dir>/{meta.json, SYLLABUS.md, parts/} and prints the next command.
Safe to re-run: it never overwrites a file that already exists.
"""
import json, sys, re, pathlib

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"): sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).expanduser().resolve()
    title = arg("--title") or d.name.replace("-", " ").title()
    lang = arg("--lang") or "en"
    cid = arg("--id") or re.sub(r"[^a-z0-9]+", "-", d.name.lower()).strip("-") or "course"

    (d / "parts").mkdir(parents=True, exist_ok=True)
    made = []

    mf = d / "meta.json"
    if not mf.exists():
        mf.write_text(json.dumps({
            "course_id": cid, "lang": lang, "title": title,
            "subtitle": arg("--subtitle", "")
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made.append("meta.json")

    sf = d / "SYLLABUS.md"
    if not sf.exists():
        sf.write_text(f"""# {title}

**Destination:** what the learner asked for, in one line
**Learner level assumed:** what they already know — be specific, it sets where axis 1 stops
**Language:** {lang}

## Chapters

- `ch-1` — … — *must know because …*
- `ch-2` — … — *prerequisite, axis 1*
- `ch-appendix` — Glossary, cheat sheet, what to learn next

## Coverage ledger

Every concept in the source material, and every gap the atlas demands, maps to a chapter.
Nothing here may still be unchecked at hand-over.

- [ ] … → `ch-1`

## Later

Chapters planned for a later phase, when the course is too big for one session. They stay in
the syllabus; the final gate reports them as still owed instead of failing on them.

## Deliberately out of scope

- … — why, and where it is mentioned instead
""", encoding="utf-8")
        made.append("SYLLABUS.md")

    print(f"scaffolded {d}")
    print("  created: " + (", ".join(made) if made else "nothing new — files already existed"))
    print(f"  next:    fill in SYLLABUS.md, then write parts/01-<slug>.html")
    print(f"  build:   python3 $SKILL/scripts/assemble.py {d} && "
          f"python3 $SKILL/scripts/verify.py {d} --wip")

if __name__ == "__main__":
    main()
