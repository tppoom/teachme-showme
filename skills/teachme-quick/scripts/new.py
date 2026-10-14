#!/usr/bin/env python3
"""Scaffold a course directory so the shape is right before you write a word.

Usage:
  python3 new.py <dir> --title "…" --lang <code> [--depth quick|standard|deep]
                 [--omit quiz,exercise] [--subtitle "…"] [--id slug]

Creates <dir>/{meta.json, SYLLABUS.md, parts/} and prints the next command.
Safe to re-run: it never overwrites a file that already exists.
"""
import json, sys, re, pathlib

SCRIPTS = pathlib.Path(__file__).resolve().parent

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"): sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).expanduser().resolve()
    title = arg("--title") or d.name.replace("-", " ").title()
    lang = arg("--lang") or "en"
    cid = arg("--id") or re.sub(r"[^a-z0-9]+", "-", d.name.lower()).strip("-") or "course"

    depth = arg("--depth", "standard")
    if depth not in ("quick", "standard", "deep"):
        sys.exit(f'--depth must be quick, standard or deep (got "{depth}")')
    allowed = {"quiz", "exercise", "objective", "recap", "visual", "appendix", "ledger"}
    alias = {"quizzes": "quiz", "exercises": "exercise", "objectives": "objective",
             "recaps": "recap", "visuals": "visual", "diagrams": "visual", "glossary": "appendix"}
    omit = []
    for x in arg("--omit", "").split(","):
        x = x.strip().lower()
        if not x: continue
        x = alias.get(x, x)
        if x not in allowed:
            sys.exit(f'--omit "{x}" is not one of: {", ".join(sorted(allowed))}')
        if x not in omit: omit.append(x)

    (d / "parts").mkdir(parents=True, exist_ok=True)
    made = []

    mf = d / "meta.json"
    if not mf.exists():
        meta = {"course_id": cid, "lang": lang, "title": title,
                "subtitle": arg("--subtitle", ""), "depth": depth}
        if omit: meta["omit"] = omit
        mf.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made.append("meta.json")

    sf = d / "SYLLABUS.md"
    if not sf.exists():
        sf.write_text(f"""# {title}

**Request:** what the user asked for, in one line
**Reader:** who reads it and what they already know
**Language:** {lang} · **Depth:** {depth}{(" · omitted at the user's request: " + ", ".join(omit)) if omit else ""}

## Chapters

- `ch-1` — Title — *after this you can …*
- `ch-2` — Title — *after this you can …*

## Left out

- … — why (say this in one line at hand-over too)
""", encoding="utf-8")
        made.append("SYLLABUS.md")

    print(f"scaffolded {d}")
    print("  created: " + (", ".join(made) if made else "nothing new — files already existed"))
    print(f"  next:    fill in SYLLABUS.md, then write parts/01-<slug>.html")
    print(f"  check:   python3 {SCRIPTS}/verify.py {d} --part parts/01-<slug>.html")
    print(f"  build:   python3 {SCRIPTS}/assemble.py {d} && "
          f"python3 {SCRIPTS}/verify.py {d} --wip")

if __name__ == "__main__":
    main()
