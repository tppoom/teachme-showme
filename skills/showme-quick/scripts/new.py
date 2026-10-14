#!/usr/bin/env python3
"""Scaffold a deck directory so the shape is right before you write a slide.

Usage:
  python3 new.py <dir> --title "…" --lang <code> --theme swiss --minutes 20
                 [--delivery live|remote|read|kiosk] [--omit notes]
                 [--subtitle "…"] [--ratio 16:9] [--id slug]

Creates <dir>/{meta.json, STORYLINE.md, parts/} and prints the next command.
Safe to re-run: it never overwrites a file that already exists.
"""
import json, sys, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 2)
    if sys.argv[1].startswith("-"): sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).expanduser().resolve()
    title = arg("--title") or d.name.replace("-", " ").title()
    lang = arg("--lang") or "en"
    theme = arg("--theme") or "keynote-dark"
    did = arg("--id") or re.sub(r"[^a-z0-9]+", "-", d.name.lower()).strip("-") or "deck"

    themes = json.loads((HERE / "assets" / "themes.json").read_text(encoding="utf-8"))
    if theme not in themes:
        sys.exit(f'unknown theme "{theme}". Available: '
                 + ", ".join(k for k in themes if not k.startswith("_")))

    delivery = arg("--delivery", "live")
    if delivery not in ("live", "remote", "read", "kiosk"):
        sys.exit(f'--delivery must be live, remote, read or kiosk (got "{delivery}")')
    allowed = {"notes", "title", "closing"}
    alias = {"speaker notes": "notes", "speaker-notes": "notes", "title slide": "title",
             "closing slide": "closing"}
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
        meta = {"deck_id": did, "lang": lang, "title": title,
                "subtitle": arg("--subtitle", ""), "ratio": arg("--ratio", "16:9"),
                "theme": {"preset": theme}}
        if arg("--minutes"): meta["minutes"] = int(arg("--minutes"))
        if delivery != "live": meta["delivery"] = delivery
        if delivery == "kiosk": meta.update({"advance": 10, "loop": True})
        if omit: meta["omit"] = omit
        mf.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made.append("meta.json")

    sf = d / "STORYLINE.md"
    if not sf.exists():
        mins = arg("--minutes", "20")
        sf.write_text(f"""# {title}

**Spine:** the one sentence they repeat to someone who wasn't in the room
**Audience:** who they are, and what they already believe
**They should leave:** knowing / feeling / doing …
**Slot:** {mins} minutes
**Delivery:** {delivery}

## Slides

- `s-1` — title — *…*
- `s-2` — … — *…*
- `s-N` — closing — *the ask*

## Appendix

- `s-a1` — … — *for the "…" question*

## Deliberately not in this deck

- … — why, and where it is mentioned instead
""", encoding="utf-8")
        made.append("STORYLINE.md")

    print(f"scaffolded {d}  (theme: {theme} — {themes[theme]['use'][:70]}…)")
    print("  created: " + (", ".join(made) if made else "nothing new — files already existed"))
    print("  next:    write the claim ladder in STORYLINE.md, then parts/01-<slug>.html")
    sc = HERE / "scripts"
    print(f"  check:   python3 {sc}/verify.py {d} --part parts/01-<slug>.html")
    print(f"  build:   python3 {sc}/assemble.py {d} && python3 {sc}/verify.py {d} --wip")

if __name__ == "__main__":
    main()
