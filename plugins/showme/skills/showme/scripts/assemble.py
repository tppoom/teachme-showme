#!/usr/bin/env python3
"""Assemble a ShowMe deck: shell.html + parts/*.html -> index.html

Usage:  python3 assemble.py <deck-dir> [--shell PATH] [--themes PATH] [--i18n PATH]

<deck-dir> must contain:
    meta.json     see below
    parts/*.html  slide fragments, assembled in filename sort order

meta.json
    {
      "deck_id":   "acme-seriesa",          // namespaces "resume where you were"
      "title":     "…",                     // browser tab + slide footer
      "subtitle":  "…",
      "lang":      "th",                    // deck chrome language
      "dir":       "rtl",                   // optional, inferred from lang
      "ratio":     "16:9",                  // 16:9 (default) | 16:10 | 4:3 | "1600x900"
      "theme": {
        "preset": "swiss",                  // a key in themes.json
        "motif":  "rule",                   // optional override
        "tokens": {"accent": "#ff5a1f"}     // optional per-token overrides
      },
      "fonts": {"url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"}
    }

`fonts.url` is the ONE thing that can break offline use — the deck will need the network the
first time it opens. Only add it when the user asked for a specific typeface.
"""
import json, sys, re, pathlib

RTL = {"ar", "he", "fa", "ur", "ps", "sd", "yi", "dv", "ckb"}
RATIOS = {"16:9": (1280, 720), "16:10": (1280, 800), "4:3": (1024, 768), "3:2": (1200, 800)}
FALLBACK = ('"Noto Sans Thai","IBM Plex Sans Thai",Sarabun,"Hiragino Sans","Yu Gothic UI",'
            '"Noto Sans JP","PingFang SC","Microsoft YaHei","Apple SD Gothic Neo","Malgun Gothic",'
            '"Noto Sans Arabic","Noto Sans Hebrew","Noto Sans Devanagari","Noto Color Emoji"')
HERE = pathlib.Path(__file__).resolve().parent.parent

def die(m): sys.exit("assemble: " + m)

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).resolve()
    def opt(flag, dflt):
        return pathlib.Path(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else dflt
    shell = opt("--shell", HERE / "assets" / "shell.html")
    themes = json.loads(opt("--themes", HERE / "assets" / "themes.json").read_text(encoding="utf-8"))
    i18n = json.loads(opt("--i18n", HERE / "assets" / "i18n.json").read_text(encoding="utf-8"))

    mf = d / "meta.json"
    if not mf.exists(): die(f"{mf} not found")
    meta = json.loads(mf.read_text(encoding="utf-8"))
    for req in ("title", "lang"): 
        if not meta.get(req): die(f'meta.json needs "{req}"')

    # ---- theme ----------------------------------------------------------
    tspec = meta.get("theme", {})
    if isinstance(tspec, str): tspec = {"preset": tspec}
    preset = tspec.get("preset", "keynote-dark")
    if preset not in themes:
        die(f'unknown theme "{preset}". Available: ' +
            ", ".join(k for k in themes if not k.startswith("_")) +
            '\nOr define every token yourself under theme.tokens.')
    base = themes[preset]
    tokens = dict(base["tokens"]); tokens.update(tspec.get("tokens", {}))
    missing = [t for t in themes["_contract"]["tokens"] if t not in tokens]
    if missing: die(f"theme is missing tokens: {', '.join(missing)}")
    for f in ("font-display", "font-body", "font-mono"):
        if FALLBACK.split(",")[0] not in tokens[f]:
            tokens[f] = tokens[f].rstrip().rstrip(",") + "," + FALLBACK
    theme_css = "\n".join(f"  --{k}:{v};" for k, v in tokens.items())
    motif = tspec.get("motif", base.get("motif", "none"))

    # ---- geometry -------------------------------------------------------
    ratio = str(meta.get("ratio", "16:9"))
    if ratio in RATIOS: W, H = RATIOS[ratio]
    elif re.fullmatch(r"\d+x\d+", ratio): W, H = map(int, ratio.split("x"))
    else: die(f'ratio "{ratio}" not recognised — use one of {", ".join(RATIOS)} or WIDTHxHEIGHT')

    # ---- language -------------------------------------------------------
    lang = str(meta["lang"]); baselang = lang.split("-")[0].lower()
    ui = dict(i18n["en"]); ui.update(i18n.get(lang) or i18n.get(baselang) or {})
    if not (i18n.get(lang) or i18n.get(baselang)):
        print(f'assemble: note — no deck-chrome translation for "{lang}", '
              f'using English for the {len(i18n["_keys"])} UI labels. '
              f'Add a "{baselang}" block to assets/i18n.json to fix that.', file=sys.stderr)

    # ---- slides ---------------------------------------------------------
    parts = sorted((d / "parts").glob("*.html"))
    if not parts: die(f"no slide parts found in {d/'parts'}")
    body = "\n\n".join(p.read_text(encoding="utf-8").rstrip() for p in parts)

    fonts = ""
    if meta.get("fonts", {}).get("url"):
        u = meta["fonts"]["url"]
        fonts = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                 f'<link rel="stylesheet" href="{u}">')

    out = shell.read_text(encoding="utf-8")
    repl = {"LANG": lang, "DIR": meta.get("dir") or ("rtl" if baselang in RTL else "ltr"),
            "TITLE": meta["title"], "SUBTITLE": meta.get("subtitle", ""),
            "DECK_ID": meta.get("deck_id", "showme"), "THEME_CSS": theme_css,
            "MOTIF": motif, "W": W, "H": H, "FONTS": fonts}
    for k, v in ui.items():
        repl["T_" + re.sub(r"([A-Z])", r"_\1", k).upper()] = v

    out = out.replace("<!--@@SLIDES@@-->", body)
    for k, v in repl.items(): out = out.replace("@@%s@@" % k, str(v))
    left = sorted(set(re.findall(r"@@([A-Z_]+)@@", out)))
    if left: die("unresolved placeholders: " + ", ".join(left))

    dest = d / "index.html"
    dest.write_text(out, encoding="utf-8")
    n = len(re.findall(r'class="[^"]*\bslide\b', out))
    apx = len(re.findall(r'class="[^"]*\bappendix\b', out))
    print(f"built {dest}")
    print(f"  theme={preset} motif={motif}  {W}x{H} ({ratio})  lang={lang} dir={repl['DIR']}")
    print(f"  {len(parts)} part files -> {n} slides ({n-apx} main + {apx} appendix), "
          f"{len(out)/1024:.0f} KB" + ("  [needs network for fonts]" if fonts else ""))

if __name__ == "__main__":
    main()
