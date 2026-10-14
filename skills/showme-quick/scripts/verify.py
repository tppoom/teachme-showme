#!/usr/bin/env python3
"""Quality gate for a built ShowMe deck.

Usage:  python3 verify.py <deck-dir> [--wip]
        python3 verify.py <deck-dir> --part parts/02-evidence.html

Where TeachMe's gate catches chapters that are too thin, this one catches slides that are
too full — the way decks actually fail. Every FAIL means move something into the speaker
notes or the appendix, split the slide, or cut it. It never means relax the check.

--wip  = mid-build run: slides the storyline promises but that aren't written yet are
         warnings instead of failures. Never pass it on the final check.
--part = check one part file on its own, without assembling. Safe while other batches are
         being written in parallel (implies --wip, skips deck-wide checks).

meta.json tunes the gate to how the deck will be used:
  "delivery": "live" (default) | "remote" | "read" | "kiosk"
      read   — emailed / read alone: slides may carry ~1.8x the words, notes become prose
      remote — over a video call: same ceilings, warns on builds that need a pointer
      kiosk  — unattended loop: notes not required (same as "advance" + "loop")
  "density": "sparse" | "normal" | "dense"   — overrides the ceiling multiplier directly
  "omit": ["notes", "title", "closing"]      — what the USER asked to leave out
"""
import sys, re, html, pathlib, math
from collections import Counter

# Reading and listening compete for the same channel, so these are ceilings, not targets.
CEIL = {"statement": 25, "title": 45, "section": 30, "quote": 45, "closing": 45, "_default": 55}
MAX_BULLETS, MAX_BULLET_WORDS = 5, 14
NOTE_MIN, NOTE_MAX = 20, 220
MAX_RUN = 3            # consecutive slides with the same layout signature
MAX_SHARE = 0.42       # share of the deck any one layout may take
MIN_PER_SLIDE, MAX_PER_SLIDE = 0.6, 3.0   # minutes

LAZY = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bPLACEHOLDER\b", r"Lorem ipsum",
        r"\bXX+\b", r"\[insert", r"\bWRITE:", r"coming soon", r"\bplaceholder text\b"]
CJK  = "぀-ヿ㐀-䶿一-鿿豈-﫿ｦ-ﾟ가-힯"
NOSP = "฀-๿຀-໿က-႟ក-៿"

fails, warns, notes = [], [], []
def fail(m): fails.append(m)
def warn(m): warns.append(m)

def text_of(frag):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", frag, flags=re.I)
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))

def wc(t):
    a = len(re.findall(f"[{CJK}]", t)); b = len(re.findall(f"[{NOSP}]", t))
    return len(re.sub(f"[{CJK}{NOSP}]", " ", t).split()) + round(a / 2.5) + round(b / 5)

def cut(chunk):
    end = chunk.find("</section>")
    return chunk if end < 0 else chunk[:end + len("</section>")]

# What the evidence on a content slide LOOKS like. A bar chart, a flow and a 2x2 are all
# "content" by class, but to the room they are three different shapes — the monotony
# check has to compare what is drawn, not what the section is called.
EVIDENCE = [("chart", r'<div class="chart"[^>]*data-type="(\w+)"'), ("stats", r'class="stats"'),
            ("cmp", r'class="cmp'), ("flow", r'class="flow'), ("tline", r'class="tline'),
            ("layers", r'class="layers'), ("matrix", r'class="matrix'), ("funnel", r'class="funnel'),
            ("prog", r'class="prog'), ("checks", r'class="checks'), ("kv", r'class="kv'),
            ("chips", r'class="chips'), ("agenda", r'class="agenda'), ("cards", r'class="card\b'),
            ("table", r"<table"), ("image", r'<img\b|class="ph"|class="fig'), ("pts", r'class="pts')]

def shape_of(lay, body):
    if lay != "content": return lay
    body = re.sub(r'<div class="chart"[\s\S]*?</table>', lambda m: m.group(0).split("<table")[0], body)
    kinds = []
    for name, pat in EVIDENCE:
        m = re.search(pat, body)
        if m: kinds.append(name + ("-" + m.group(1) if m.groups() else ""))
    return "+".join(kinds) or "text"

def layout_of(cls):
    known = ["title", "section", "statement", "quote", "closing", "bignum", "imgfull", "code", "appendix"]
    for k in known:
        if re.search(rf"\b{k}\b", cls): return k
    return "content"

DELIVERY = {"live": "normal", "remote": "normal", "read": "dense", "kiosk": "sparse"}
DENSITY = {"sparse": 0.8, "normal": 1.0, "dense": 1.8}
OMITTABLE = {"notes", "title", "closing"}

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"): sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1]).resolve()
    part_file = None
    if "--part" in sys.argv:
        i = sys.argv.index("--part") + 1
        if i >= len(sys.argv) or sys.argv[i].startswith("-"):
            sys.exit("FAIL: --part needs a file, e.g. --part parts/03-slug.html")
        part_file = pathlib.Path(sys.argv[i])
    wip = "--wip" in sys.argv or part_file is not None

    import json
    mf = d / "meta.json"
    meta = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    delivery = str(meta.get("delivery", "live")).lower()
    if delivery not in DELIVERY: sys.exit(f'FAIL: meta.json delivery "{delivery}" is not one of {", ".join(DELIVERY)}')
    density = str(meta.get("density", DELIVERY[delivery])).lower()
    if density not in DENSITY: sys.exit(f'FAIL: meta.json density "{density}" is not one of {", ".join(DENSITY)}')
    mult = DENSITY[density]
    ceil_of = {key: round(v * mult) for key, v in CEIL.items()}
    max_bullets = MAX_BULLETS + (2 if density == "dense" else 0)
    max_bullet_words = round(MAX_BULLET_WORDS * mult)
    max_code = 12 if density != "dense" else 18
    note_max = NOTE_MAX * (2 if delivery == "read" else 1)
    omit = {str(x).lower() for x in meta.get("omit", [])}
    bad = omit - OMITTABLE
    if bad: sys.exit(f"FAIL: meta.json omit has unknown item(s) {sorted(bad)} — allowed: {sorted(OMITTABLE)}")
    advance = meta.get("advance") or 0
    # a kiosk loop: nobody is there to speak, so notes are not the deliverable
    unattended = bool(advance and meta.get("loop")) or delivery == "kiosk"
    need_notes = not unattended and "notes" not in omit
    if delivery == "kiosk" and not (advance and meta.get("loop")):
        warn('delivery is "kiosk" but meta.json has no "advance" + "loop": true — '
             'nobody is there to press next, so the deck will sit on slide 1')

    if part_file is not None:
        if not part_file.is_absolute():
            part_file = (d / part_file) if (d / part_file).exists() else part_file.resolve()
        if not part_file.exists(): sys.exit(f"FAIL: {part_file} not found")
        doc = part_file.read_text(encoding="utf-8")
    else:
        idx = d / "index.html"
        if not idx.exists(): sys.exit(f"FAIL: {idx} not built — run assemble.py first")
        doc = idx.read_text(encoding="utf-8")

    # ---- 1. self-contained ---------------------------------------------------
    for pat, msg in [(r"<script[^>]+\bsrc=", "external <script src>"),
                     (r"@import\s", "CSS @import"),
                     (r'<img[^>]+src=["\']https?:', "remote <img> — inline it with embed-image.py")]:
        if re.search(pat, doc, re.I): fail("not self-contained: " + msg)
    ext = re.findall(r'<link[^>]+href="(https?://[^"]+)"', doc)
    for u in ext:
        if "fonts.googleapis" in u or "fonts.gstatic" in u:
            notes.append(f"webfont linked ({u.split('?')[0]}) — the deck needs the network on first open")
        else: fail(f"external stylesheet: {u}")

    # ---- 2. storyline contract ----------------------------------------------
    stf = d / "STORYLINE.md"
    promised, spine = [], ""
    if not stf.exists():
        fail("STORYLINE.md missing — write the claim ladder before building slides")
    else:
        st = stf.read_text(encoding="utf-8")
        m = re.search(r"\*\*Spine:\*\*\s*(.+)", st)
        spine = m.group(1).strip() if m else ""
        if not spine: fail("STORYLINE.md has no **Spine:** line — the one sentence they repeat tomorrow")
        promised = re.findall(r"^\s*[-*]\s*`?(s-[\w-]+)`?", st, re.M)

    # ---- 3. slides -----------------------------------------------------------
    # authors write the attributes in whatever order feels natural — match either
    SL = r'<section\b[^>]*\bclass="[^"]*\bslide\b'
    # cut each chunk at its own </section>; otherwise the last slide swallows the
    # page chrome and the script, and gets measured against words it does not contain
    # commented-out markup is not on any slide — a template comment must not count as one
    live = re.sub(r"<!--[\s\S]*?-->", "", doc)
    chunks = [cut(c) for c in re.split(f"(?={SL})", live) if re.match(SL, c)]
    if not chunks: fail("no slides found")
    layouts, shapes, ids, main_n, apx_n = [], [], [], 0, 0
    prev_sig, run = None, 0

    for pos, c in enumerate(chunks, 1):
        head = c.split(">", 1)[0]
        cls = (re.search(r'class="([^"]*)"', head) or [None, ""])[1]
        sid = (re.search(r'\bid="([^"]+)"', head) or [None, f"#{pos}"])[1]
        ids.append(sid)
        lay = layout_of(cls); layouts.append(lay)
        is_apx = "appendix" in cls
        apx_n += is_apx; main_n += not is_apx
        tag = f"[slide {pos}]"

        claim = (re.search(r'data-claim="([^"]*)"', head) or [None, ""])[1].strip()
        if not claim:
            fail(f"{tag} has no data-claim — a slide without a claim is a slide nobody needed")
        else:
            if len(claim) > 150: warn(f"{tag} claim is {len(claim)} chars — sharpen it to one sentence")
            if not re.search(r"[a-zA-Z฀-๿぀-鿿]", claim):
                fail(f"{tag} claim is not a sentence")
            if claim.rstrip().endswith(":") or wc(claim) < 3:
                fail(f"{tag} claim reads as a topic, not a claim: {claim[:70]!r}")

        nt = re.search(r'<div class="notes">([\s\S]*?)</div>\s*(?=</section>)', c)
        body = re.sub(r'<div class="notes">[\s\S]*?</div>\s*(?=</section>)', "", c)
        nw = wc(text_of(nt.group(1))) if nt else 0
        if lay not in ("title",) and need_notes:
            if not nt: fail(f"{tag} has no speaker notes — that is where the detail is supposed to live")
            elif nw < NOTE_MIN:
                fail(f"{tag} notes are {nw} words — say what you would actually say (aim {NOTE_MIN}-{NOTE_MAX})")
            elif nw > note_max: warn(f"{tag} notes are {nw} words — long enough that you will not read them live")

        # chart data is drawn, not read, and code is measured in lines — neither is prose
        prose = re.sub(r'<div class="chart"[\s\S]*?</table>', " ", body)
        prose = re.sub(r"<pre[\s\S]*?</pre>", " ", prose)
        w = wc(text_of(prose))
        ceil = ceil_of.get(lay, ceil_of["_default"])
        if w > ceil:
            fail(f"{tag} has {w} words on the slide (ceiling {ceil} for {lay}) — "
                 f"move it to the notes, split the slide, or cut it")

        for ul in re.findall(r'<ul class="pts">[\s\S]*?</ul>', body):
            lis = re.findall(r"<li[\s\S]*?</li>", ul)
            if len(lis) > max_bullets:
                fail(f"{tag} has {len(lis)} bullets (max {max_bullets}) — past that nobody reads them")
            for li in lis:
                lw = wc(text_of(li))
                if lw > max_bullet_words:
                    fail(f"{tag} a bullet is {lw} words (max {max_bullet_words}) — bullets are labels, not sentences")

        for ch in re.findall(r'<div class="chart"[\s\S]*?</div>\s*(?=<div class="(?:take|notes)"|</section>|<div class="cols)', c):
            if "<table" not in ch: fail(f"{tag} a .chart has no <table> of data to draw from")
            rows = len(re.findall(r"<tr", ch))
            if rows > 7: warn(f"{tag} a chart has {rows-1} series/rows — beyond ~5 it is a table with extra steps")
        if 'class="chart"' in c and 'class="take"' not in c and lay != "appendix":
            warn(f"{tag} has a chart but no .take line — say what the data proves")
        has_numbers = 'class="chart"' in c or any(re.search(r"\d", text_of(t)) for t in re.findall(r"<table[\s\S]*?</table>", body))
        if has_numbers and 'class="src"' not in c:
            warn(f"{tag} shows numbers with no <p class=\"src\"> line — say where they came "
                 f"from and what they exclude, before someone in the room asks")
        for pr in re.findall(r'<div class="pr[^"]*"[\s\S]*?</div>\s*</div>', body):
            if "--p:" not in pr:
                fail(f"{tag} a .prog bar has no style=\"--p:N%\" — it would render empty")
        for fs in re.findall(r'<div class="fs"[^>]*>', body):
            if "--w:" not in fs:
                fail(f"{tag} a .funnel stage has no style=\"--w:N%\" — it would render full width")

        for img in re.findall(r"<img[^>]*>", c):
            if "alt=" not in img: fail(f"{tag} an <img> has no alt text")
        if re.search(r'src="data:image/[^;]+;base64,\s*(?:…|\.\.\.)', c):
            fail(f"{tag} an image src is a stub — inline a real image or use the .ph placeholder")

        for pre in re.findall(r"<pre[\s\S]*?</pre>", body):
            lines = len(text_of(pre).strip().split("\n"))
            if lines > max_code:
                fail(f"{tag} a code block is {lines} lines — nobody reads past about {max_code} on a slide")
        n_build = len(re.findall(r"data-build", body))
        if n_build > 5:
            warn(f"{tag} has more than 5 build steps — that is more than one slide")
        elif delivery == "remote" and n_build > 3:
            warn(f"{tag} has {n_build} build steps — on a video call nobody sees you point; keep builds to 3")
        elif delivery == "read" and n_build:
            notes.append(f"{tag} uses builds, but a deck that is read shows every step at once")

        # --- things that render wrong ---
        vis = re.sub(r"<(pre|code|svg|table|script)\b[\s\S]*?</\1>", " ", body, flags=re.I)
        vtxt = text_of(vis)
        md = []
        if re.search(r"(?<![*\w])\*\*[^*\n]{1,80}\*\*(?!\*)", vtxt): md.append("**bold**")
        if re.search(r"(?m)^\s{0,3}#{1,4}\s+\S", vtxt): md.append("# heading")
        if "```" in vtxt: md.append("``` fence")
        if re.search(r"(?<![\w`])`[^`\n]{1,60}`(?![\w`])", vtxt): md.append("`code`")
        if md: fail(f"{tag} Markdown renders literally on the slide: {', '.join(md)} — use <strong>, <code>")
        for code in re.findall(r"<code\b[^>]*>([\s\S]*?)</code>", body):
            m = re.search(r"<(?!/?(?:span|b|i|em|strong|mark|u|br)\b)[/!]?[A-Za-z][^>]*>?", code)
            if m:
                fail(f"{tag} unescaped '<' in code: {m.group(0)[:40]!r} — the browser eats it; write &lt;")
                break
        if re.search(r'style="[^"]*(?:color|background)\s*:\s*#', body):
            warn(f"{tag} an inline colour bypasses the theme — use the theme tokens or classes")
        # --- the tells that make a deck read as generated ---
        emo = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]\ufe0f?", vtxt)
        emo = [e for e in emo if e not in "✓✔✕✗★☆→←↑↓▲▼●○"]
        if emo:
            warn(f"{tag} emoji on the slide ({''.join(emo[:4])}) — decorative emoji read as machine-made; "
                 f"use the icon set or nothing")
        for h in re.findall(r"<h[12][^>]*>([\s\S]*?)</h[12]>", body):
            ht = text_of(h).strip().lower().rstrip(".!?:")
            if wc(text_of(h)) > 16 and lay not in ("statement", "quote"):
                warn(f"{tag} headline is {wc(text_of(h))} words — keep it to two lines (~8-14 words); "
                     f"the rest goes in the evidence or the notes")
            if re.fullmatch(r"(?:overview|introduction|intro|agenda|summary|conclusions?|key takeaways?|"
                            r"background|next steps|thank you|thanks|questions|any questions|q ?& ?a|"
                            r"ภาพรวม|บทนำ|สรุป|สรุปผล|ขอบคุณ|ขอบคุณครับ|ขอบคุณค่ะ|คำถาม|มีคำถามไหม|ถาม-ตอบ)", ht):
                (fail if lay == "closing" else warn)(
                    f"{tag} headline {text_of(h).strip()!r} is a label — write the point as a sentence"
                    + (" (the closing slide states the ask)" if lay == "closing" else ""))
        buzz = re.findall(r"\b(?:unlock(?:ing)?|leverag(?:e|ing)|seamless(?:ly)?|game[- ]chang\w*|revolutioni[sz]\w*|"
                          r"cutting[- ]edge|synerg\w*|delve|holistic|robust solution|next[- ]level|supercharge\w*|"
                          r"in today'?s (?:fast-paced|digital) world)\b", vtxt, re.I)
        if buzz:
            warn(f"{tag} buzzwords on the slide ({', '.join(sorted(set(b.lower() for b in buzz))[:3])}) — "
                 f"say the specific thing instead")

        sig = shape_of(lay, body); shapes.append(sig)
        run = run + 1 if sig == prev_sig else 1
        if run == MAX_RUN + 1 and lay == "content":
            fail(f"{tag} is the {MAX_RUN+1}th slide in a row with the same shape — "
                 f"change what the evidence looks like or the room stops looking up")
        prev_sig = sig

    # ---- 4. deck shape -------------------------------------------------------
    n = len(chunks)
    whole = part_file is None
    if whole and "title" not in omit and layouts and layouts[0] != "title":
        fail("the deck does not open on a title slide")
    if whole and "closing" not in omit and n > 6 and "closing" not in layouts:
        fail("the deck has no closing slide — the last thirty seconds are where the ask goes")
    if whole and main_n > 10 and "section" not in layouts:
        warn(f"{main_n} main slides and no section dividers — the audience has nowhere to breathe")
    for shp, k in Counter(shapes).most_common(1):
        if whole and n >= 8 and k / n > MAX_SHARE and shp not in ("title", "section", "appendix"):
            warn(f"{int(k/n*100)}% of the deck is {shp} slides — vary the shape of the evidence")
    dupes = {i for i in ids if ids.count(i) > 1 and not i.startswith("#")}
    if dupes: fail("duplicate slide ids: " + ", ".join(sorted(dupes)))
    for p in (promised if whole else []):
        if p not in ids:
            (warn if wip else fail)(f"STORYLINE.md promises {p} but it is not in the deck")

    mins = meta.get("minutes") if whole else None
    if not whole: pass
    elif advance and not meta.get("loop"):
        auto = sum(float(re.search(r'data-advance="([\d.]+)"', c.split(">", 1)[0]).group(1))
                   if 'data-advance="' in c.split(">", 1)[0] else advance
                   for c, lay in zip(chunks, layouts) if "appendix" not in c.split(">", 1)[0]) / 60
        if mins and abs(auto - mins) > max(0.5, mins * 0.1):
            warn(f"auto-advance runs {auto:.1f} minutes but the slot is {mins} — "
                 f"change \"advance\" or the slide count")
    elif mins:
        lo, hi = mins / MAX_PER_SLIDE, mins / MIN_PER_SLIDE
        if not (lo <= main_n <= hi):
            warn(f"{main_n} main slides for a {mins}-minute slot — that slot fits roughly "
                 f"{math.ceil(lo)}-{int(hi)}. Cut, or move slides to the appendix")

    # ---- 5. laziness ---------------------------------------------------------
    # Marker words (TODO, FIXME…) are author shorthand, so they only count in capitals — the
    # ordinary word "placeholder" in a sentence about placeholders is prose, not a leftover.
    # Code is quoted material: a real repo excerpt may legitimately contain "# TODO".
    plain = text_of(re.sub(r"<(pre|code)\b[\s\S]*?</\1>", " ", doc, flags=re.I))
    for pat in LAZY:
        flags = 0 if re.fullmatch(r"\\b[A-Z+]+:?(?:\\b)?", pat) else re.I
        for m in re.finditer(pat, plain, flags):
            fail(f"placeholder text {m.group(0)!r} at …{plain[max(0,m.start()-50):m.end()+30].strip()[:100]}…")

    # ---- 6. structure --------------------------------------------------------
    stripped = re.sub(r"<(script|style)[\s\S]*?</\1>", "", doc, flags=re.I)
    stripped = re.sub(r"<!--[\s\S]*?-->", "", stripped)
    for t in ["section", "div", "ul", "ol", "li", "table", "tr", "td", "th", "figure", "blockquote", "pre"]:
        o = len(re.findall(rf"<{t}\b", stripped, re.I)); c = len(re.findall(rf"</{t}\s*>", stripped, re.I))
        if o != c: fail(f"<{t}> open/close mismatch: {o} open vs {c} close")

    # ---- report --------------------------------------------------------------
    lang = (re.search(r'<html[^>]*\blang="([^"]*)"', doc) or [None, "?"])[1]
    n_chart = len(re.findall(r'class="chart"', doc))
    n_note  = len(re.findall(r'class="notes"', doc))
    prof = f"delivery={delivery} density={density}" + (f" omit={','.join(sorted(omit))}" if omit else "")
    if not whole: print(f"part check: {part_file.name}   ({prof})")
    else: print(prof)
    print(f"{n} slides ({main_n} main + {apx_n} appendix)   lang={lang}   "
          f"charts: {n_chart}   slides with notes: {n_note}/{n}   size: {len(doc)/1024:.0f} KB")
    if spine: print(f"spine: {spine[:96]}")
    print("shapes: " + ", ".join(f"{k}×{v}" for k, v in Counter(shapes).most_common()))
    for x in notes: print("NOTE  " + x)
    for x in warns: print("WARN  " + x)
    for x in fails: print("FAIL  " + x)
    if fails:
        print(f"\n{len(fails)} failure(s). Fix by moving content to the notes or the appendix, "
              f"splitting slides, or cutting — not by relaxing the gate.")
        sys.exit(1)
    if not whole:
        print("\nPASS (this batch) — assemble + full verify once every batch is written"); return
    print("\nPASS (work in progress)" if wip else "\nPASS — the deck is presentable.")

if __name__ == "__main__":
    main()
