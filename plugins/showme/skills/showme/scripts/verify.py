#!/usr/bin/env python3
"""Quality gate for a built ShowMe deck.

Usage:  python3 verify.py <deck-dir> [--wip]

Where TeachMe's gate catches chapters that are too thin, this one catches slides that are
too full — the way decks actually fail. Every FAIL means move something into the speaker
notes or the appendix, split the slide, or cut it. It never means relax the check.

--wip = mid-build run: slides the storyline promises but that aren't written yet are
        warnings instead of failures. Never pass it on the final check.
"""
import sys, re, html, pathlib
from collections import Counter

# Reading and listening compete for the same channel, so these are ceilings, not targets.
CEIL = {"statement": 25, "title": 45, "section": 30, "quote": 45, "closing": 45, "_default": 55}
MAX_BULLETS, MAX_BULLET_WORDS = 5, 14
NOTE_MIN, NOTE_MAX = 20, 220
MAX_RUN = 3            # consecutive slides with the same layout signature
MAX_SHARE = 0.42       # share of the deck any one layout may take
MIN_PER_SLIDE, MAX_PER_SLIDE = 0.6, 3.0   # minutes

LAZY = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bPLACEHOLDER\b", r"Lorem ipsum",
        r"\bXX+\b", r"\[insert", r"coming soon", r"\bplaceholder text\b"]
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

def layout_of(cls):
    known = ["title", "section", "statement", "quote", "closing", "bignum", "imgfull", "code", "appendix"]
    for k in known:
        if re.search(rf"\b{k}\b", cls): return k
    return "content"

def main():
    d = pathlib.Path(sys.argv[1]).resolve()
    wip = "--wip" in sys.argv
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
    chunks = [cut(c) for c in re.split(f"(?={SL})", doc) if re.match(SL, c)]
    if not chunks: fail("no slides found")
    layouts, ids, main_n, apx_n = [], [], 0, 0
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
        if lay not in ("title",):
            if not nt: fail(f"{tag} has no speaker notes — that is where the detail is supposed to live")
            elif nw < NOTE_MIN:
                fail(f"{tag} notes are {nw} words — say what you would actually say (aim {NOTE_MIN}-{NOTE_MAX})")
            elif nw > NOTE_MAX: warn(f"{tag} notes are {nw} words — long enough that you will not read them live")

        # chart data is drawn, not read, and code is measured in lines — neither is prose
        prose = re.sub(r'<div class="chart"[\s\S]*?</table>', " ", body)
        prose = re.sub(r"<pre[\s\S]*?</pre>", " ", prose)
        w = wc(text_of(prose))
        ceil = CEIL.get(lay, CEIL["_default"])
        if w > ceil:
            fail(f"{tag} has {w} words on the slide (ceiling {ceil} for {lay}) — "
                 f"move it to the notes, split the slide, or cut it")

        for ul in re.findall(r'<ul class="pts">[\s\S]*?</ul>', body):
            lis = re.findall(r"<li[\s\S]*?</li>", ul)
            if len(lis) > MAX_BULLETS:
                fail(f"{tag} has {len(lis)} bullets (max {MAX_BULLETS}) — the room stops reading after five")
            for li in lis:
                lw = wc(text_of(li))
                if lw > MAX_BULLET_WORDS:
                    fail(f"{tag} a bullet is {lw} words (max {MAX_BULLET_WORDS}) — bullets are labels, not sentences")

        for ch in re.findall(r'<div class="chart"[\s\S]*?</div>\s*(?=<div class="(?:take|notes)"|</section>|<div class="cols)', c):
            if "<table" not in ch: fail(f"{tag} a .chart has no <table> of data to draw from")
            rows = len(re.findall(r"<tr", ch))
            if rows > 7: warn(f"{tag} a chart has {rows-1} series/rows — beyond ~5 it is a table with extra steps")
        if 'class="chart"' in c and 'class="take"' not in c and lay != "appendix":
            warn(f"{tag} has a chart but no .take line — say what the data proves")

        for img in re.findall(r"<img[^>]*>", c):
            if "alt=" not in img: fail(f"{tag} an <img> has no alt text")
        if re.search(r'src="data:image/[^;]+;base64,\s*(?:…|\.\.\.)', c):
            fail(f"{tag} an image src is a stub — inline a real image or use the .ph placeholder")

        for pre in re.findall(r"<pre[\s\S]*?</pre>", body):
            lines = len(text_of(pre).strip().split("\n"))
            if lines > 12:
                fail(f"{tag} a code block is {lines} lines — nobody reads past about 12 on a slide")
        if len(re.findall(r"data-build", body)) > 5:
            warn(f"{tag} has more than 5 build steps — that is more than one slide")

        sig = lay + ("|pts" if 'class="pts"' in body else "")
        run = run + 1 if sig == prev_sig else 1
        if run == MAX_RUN + 1 and lay == "content":
            fail(f"{tag} is the {MAX_RUN+1}th slide in a row with the same shape — "
                 f"change what the evidence looks like or the room stops looking up")
        prev_sig = sig

    # ---- 4. deck shape -------------------------------------------------------
    n = len(chunks)
    if layouts and layouts[0] != "title": fail("the deck does not open on a title slide")
    if n > 6 and "closing" not in layouts:
        fail("the deck has no closing slide — the last thirty seconds are where the ask goes")
    if main_n > 10 and "section" not in layouts:
        warn(f"{main_n} main slides and no section dividers — the audience has nowhere to breathe")
    for lay, k in Counter(layouts).most_common(1):
        if n >= 8 and k / n > MAX_SHARE and lay == "content":
            warn(f"{int(k/n*100)}% of the deck is the same layout — vary the shape of the evidence")
    dupes = {i for i in ids if ids.count(i) > 1 and not i.startswith("#")}
    if dupes: fail("duplicate slide ids: " + ", ".join(sorted(dupes)))
    for p in promised:
        if p not in ids:
            (warn if wip else fail)(f"STORYLINE.md promises {p} but it is not in the deck")

    mins = None
    mf = d / "meta.json"
    if mf.exists():
        import json
        mins = json.loads(mf.read_text(encoding="utf-8")).get("minutes")
    if mins:
        lo, hi = mins / MAX_PER_SLIDE, mins / MIN_PER_SLIDE
        if not (lo <= main_n <= hi):
            warn(f"{main_n} main slides for a {mins}-minute slot — that slot fits roughly "
                 f"{int(lo)}-{int(hi)}. Cut, or move slides to the appendix")

    # ---- 5. laziness ---------------------------------------------------------
    plain = text_of(doc)
    for pat in LAZY:
        for m in re.finditer(pat, plain, re.I):
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
    print(f"{n} slides ({main_n} main + {apx_n} appendix)   lang={lang}   "
          f"charts: {n_chart}   slides with notes: {n_note}/{n}   size: {len(doc)/1024:.0f} KB")
    if spine: print(f"spine: {spine[:96]}")
    print("shapes: " + ", ".join(f"{k}×{v}" for k, v in Counter(layouts).most_common()))
    for x in notes: print("NOTE  " + x)
    for x in warns: print("WARN  " + x)
    for x in fails: print("FAIL  " + x)
    if fails:
        print(f"\n{len(fails)} failure(s). Fix by moving content to the notes or the appendix, "
              f"splitting slides, or cutting — not by relaxing the gate.")
        sys.exit(1)
    print("\nPASS (work in progress)" if wip else "\nPASS — the deck is presentable.")

if __name__ == "__main__":
    main()
