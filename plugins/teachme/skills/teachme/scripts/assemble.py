#!/usr/bin/env python3
"""Assemble a TeachMe course: shell.html + parts/*.html -> index.html

Usage:  python3 assemble.py <course-dir> [--shell PATH] [--i18n PATH]

<course-dir> must contain:
    meta.json     {"course_id","title","subtitle","lang", "dir"?, "ui"? {...overrides}}
    parts/*.html  chapter fragments, assembled in filename sort order

`lang` is a BCP-47 code ("th", "ja", "pt-BR"). If it has no preset in assets/i18n.json,
supply every UI string under "ui" in meta.json — the build refuses to ship a half-translated
interface and prints the exact template you need.
"""
import json, sys, re, pathlib

RTL = {"ar", "he", "fa", "ur", "ps", "sd", "yi", "dv", "ckb"}
HERE = pathlib.Path(__file__).resolve().parent.parent

def die(msg): sys.exit("assemble: " + msg)

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).resolve()
    def opt(flag, default):
        return pathlib.Path(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default
    shell = opt("--shell", HERE / "assets" / "shell.html")
    i18n_path = opt("--i18n", HERE / "assets" / "i18n.json")

    meta_file = d / "meta.json"
    if not meta_file.exists(): die(f"{meta_file} not found")
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    for req in ("title", "lang"):
        if not meta.get(req): die(f'meta.json needs "{req}"')

    i18n = json.loads(i18n_path.read_text(encoding="utf-8"))
    keys = i18n["_keys"]
    lang = str(meta["lang"])
    base = lang.split("-")[0].lower()
    preset = i18n.get(lang) or i18n.get(base)

    ui = dict(i18n["en"])
    if preset: ui.update(preset)
    ui.update(meta.get("ui", {}))

    if not preset:
        missing = [k for k in keys if k not in meta.get("ui", {})]
        if missing:
            tmpl = json.dumps({k: i18n["en"][k] for k in missing}, ensure_ascii=False, indent=2)
            die(f'language "{lang}" has no preset in {i18n_path.name}.\n'
                f'Translate these into {lang} and put them under "ui" in meta.json '
                f'(or add a "{base}" block to i18n.json so every future course gets it):\n\n{tmpl}\n')

    parts_dir = d / "parts"
    parts = sorted(parts_dir.glob("*.html"))
    if not parts: die(f"no chapter parts found in {parts_dir}")
    body = "\n\n".join(p.read_text(encoding="utf-8").rstrip() for p in parts)

    out = shell.read_text(encoding="utf-8")
    repl = {
        "LANG": lang,
        "DIR": meta.get("dir") or ("rtl" if base in RTL else "ltr"),
        "TITLE": meta["title"],
        "SUBTITLE": meta.get("subtitle", ""),
        "COURSE_ID": meta.get("course_id", "teachme"),
    }
    for k in keys: repl["T_" + k.upper()] = ui[k]

    out = out.replace("<!--@@CHAPTERS@@-->", body)
    for k, v in repl.items():
        out = out.replace("@@%s@@" % k, str(v))

    left = sorted(set(re.findall(r"@@([A-Z_]+)@@", out)))
    if left: die("unresolved placeholders: " + ", ".join(left))

    dest = d / "index.html"
    dest.write_text(out, encoding="utf-8")
    n_ch = len(re.findall(r'class="chapter[" ]', out))
    words = len(re.sub(r"<[^>]+>", " ", out).split())
    print(f"built {dest}")
    print(f"  lang={lang} dir={repl['DIR']}"
          f"{'' if preset else ' (ui from meta.json)'}   "
          f"{len(parts)} parts -> {n_ch} chapters, {len(out)/1024:.0f} KB, {words:,} words")

if __name__ == "__main__":
    main()
