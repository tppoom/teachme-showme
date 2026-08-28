#!/usr/bin/env python3
"""Coverage + quality gate for a built TeachMe course.

Usage:  python3 verify.py <course-dir> [--min-words 600] [--wip]

--wip = mid-build run: chapters the syllabus promises but that are not written yet
        are warnings instead of failures. NEVER pass --wip on the final check.

Fails (exit 1) if the course is thin, incomplete, or drifted from SYLLABUS.md.
Read every FAIL line as "go write the missing content", never as "loosen the check".
"""
import sys, re, json, pathlib, html

MIN_WORDS = 600
LAZY = [
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bPLACEHOLDER\b", r"Lorem ipsum",
    r"coming soon", r"\[\.\.\.\]", r"\(\.\.\.\)", r"left as an exercise for the reader",
    r"similar to (?:the )?above", r"see above for (?:the )?details?",
    r"same (?:idea|pattern) as (?:the )?(?:previous|above)",
    r"\b(?:and )?so on(?:\.|,|$)", r"the rest (?:is|are) (?:similar|analogous)",
    r"เช่นเดิม(?:กับ)?ด้านบน", r"ดูด้านบน", r"ทำนองเดียวกันกับด้านบน",
]
BLOCK_TAGS = ["section", "div", "ul", "ol", "li", "table", "tbody", "thead",
              "tr", "td", "th", "pre", "details", "figure", "dl", "dt", "dd", "p"]

fails, warns = [], []
def fail(m): fails.append(m)
def warn(m): warns.append(m)

def text_of(frag):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", frag, flags=re.I)
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)

# Languages without spaces need character-based counting or every CJK/Thai course
# looks like a stub. Ratios are reading-time equivalents to one English word.
CJK  = "\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f\uac00-\ud7af"
NOSP = "\u0e00-\u0e7f\u0e80-\u0eff\u1000-\u109f\u1780-\u17ff"   # Thai Lao Myanmar Khmer

def count_words(t):
    n_cjk  = len(re.findall(f"[{CJK}]", t))
    n_nosp = len(re.findall(f"[{NOSP}]", t))
    rest   = re.sub(f"[{CJK}{NOSP}]", " ", t)
    return len(rest.split()) + round(n_cjk / 2.5) + round(n_nosp / 5)

def words(frag): return count_words(text_of(frag))

def main():
    d = pathlib.Path(sys.argv[1]).resolve()
    minw = int(sys.argv[sys.argv.index("--min-words") + 1]) if "--min-words" in sys.argv else MIN_WORDS
    wip = "--wip" in sys.argv
    idx = d / "index.html"
    if not idx.exists(): sys.exit(f"FAIL: {idx} not built yet — run assemble.py first")
    doc = idx.read_text(encoding="utf-8")

    # ---- 1. self-containment -------------------------------------------------
    for pat, msg in [(r"<script[^>]+\bsrc=", "external <script src>"),
                     (r'<link[^>]+rel=["\']?stylesheet', "external stylesheet <link>"),
                     (r"@import\s", "CSS @import"),
                     (r'<img[^>]+src=["\']https?:', "remote <img>")]:
        if re.search(pat, doc, re.I): fail(f"not self-contained: {msg} found")

    # ---- 2. syllabus contract ------------------------------------------------
    syl = d / "SYLLABUS.md"
    if not syl.exists():
        fail("SYLLABUS.md missing — the syllabus is the contract; write it before authoring")
        syl_ids, ledger_ids, unchecked = [], [], []
    else:
        s = syl.read_text(encoding="utf-8")
        syl_ids = re.findall(r"^\s*(?:[-*]\s*)?(?:\[[ x]\]\s*)?`?(ch-[\w-]+)`?", s, re.M)
        ledger = s.split("## Coverage ledger", 1)
        if len(ledger) < 2:
            fail("SYLLABUS.md has no '## Coverage ledger' section "
                 "(every concept in the source material must map to a chapter id)")
            ledger_ids, unchecked = [], []
        else:
            ledger_ids = re.findall(r"(ch-[\w-]+)", ledger[1])
            unchecked = re.findall(r"^\s*[-*]\s*\[ \]\s*(.+)$", ledger[1], re.M)
        for u in unchecked:
            (warn if wip else fail)(f"coverage ledger item still unchecked: {u.strip()[:90]}")

    # ---- 3. chapters ---------------------------------------------------------
    # attribute order is the author's choice, and each chunk must stop at its own
    # </section> — otherwise the last chapter absorbs the page chrome and the script,
    # which would let a thin final chapter pass the word floor on borrowed words
    CH = r'<section\b[^>]*\bclass="[^"]*\bchapter\b'
    def cut(c):
        e = c.find("</section>")
        return c if e < 0 else c[:e + len("</section>")]
    chaps = [cut(c) for c in re.split(f"(?={CH})", doc) if re.match(CH, c)]
    if not chaps: fail("no chapters found in index.html")
    seen = []
    for c in chaps:
        cid = (re.search(r'id="([^"]+)"', c) or [None, "?"])[1]
        seen.append(cid)
        body = c.split('class="ch-body"', 1)[-1]
        title = (re.search(r'data-title="([^"]*)"', c) or [None, ""])[1]
        tag = f"[{cid}]"
        if not title: fail(f"{tag} missing data-title (sidebar entry will be blank)")
        if 'class="ch-desc"' not in c: fail(f"{tag} missing .ch-desc one-liner")
        if "appendix" in c.split(">", 1)[0]:
            continue
        if 'class="objective"' not in body: fail(f"{tag} missing .objective block")
        if 'class="recap"' not in body: fail(f"{tag} missing .recap block")
        qz = re.findall(r'class="q"', body)
        if not qz: fail(f"{tag} missing checkpoint .quiz")
        elif len(qz) < 2: warn(f"{tag} quiz has only {len(qz)} question (aim for 2-4)")
        for q in re.split(r'(?=<div class="q">)', body):
            if not q.startswith('<div class="q">'): continue
            n_ok = len(re.findall(r'data-correct="true"', q))
            if n_ok != 1: fail(f"{tag} a quiz question has {n_ok} correct answers (must be exactly 1)")
            if 'class="fb"' not in q: fail(f"{tag} a quiz question has no .fb explanation")
        n_viz = (len(re.findall(r'<figure[^>]*class="(?:viz|diagram)', c))
                 + len(re.findall(r'class="walk"', c)))
        if not n_viz and "data-novisual" not in c:
            fail(f"{tag} has no visual — every chapter needs one "
                 f"(or an explicit data-novisual=\"reason\" on the <section>)")
        for fg in re.findall(r'<figure[^>]*class="(?:viz|diagram)"[\s\S]*?</figure>', c):
            if "<figcaption" not in fg:
                fail(f"{tag} a figure has no <figcaption> — the caption carries the takeaway")
            elif len(text_of(fg.split("<figcaption",1)[1]).split()) < 4:
                warn(f"{tag} a figcaption is too short to state a takeaway")
        for sv in re.findall(r"<svg[^>]*>", c):
            if 'role="img"' not in sv or "aria-label" not in sv:
                fail(f"{tag} an <svg> is missing role=\"img\" or aria-label")
        # Anything drawn outside the viewBox is clipped with no error and no visible
        # symptom on the authoring machine — the SVG does not grow to contain it.
        for sv in re.findall(r"<svg[^>]*viewBox=\"[^\"]*\"[\s\S]*?</svg>", c):
            vb = re.search(r'viewBox="\s*([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)', sv)
            if not vb: continue
            x0, y0, vw, vh = (float(g) for g in vb.groups())
            for el in re.findall(r"<(?:text|rect|circle|image|use)\b[^>]*>", sv):
                cx = re.search(r'\b(?:x|cx)="([-\d.]+)"', el)
                cy = re.search(r'\b(?:y|cy)="([-\d.]+)"', el)
                if cx and not (x0 - 1 <= float(cx.group(1)) <= x0 + vw + 1):
                    warn(f"{tag} an SVG element sits at x={cx.group(1)} but the viewBox is "
                         f"{x0:g}..{x0+vw:g} wide — it will be clipped, invisibly")
                if cy and not (y0 - 1 <= float(cy.group(1)) <= y0 + vh + 1):
                    warn(f"{tag} an SVG element sits at y={cy.group(1)} but the viewBox is "
                         f"{y0:g}..{y0+vh:g} tall — it will be clipped, invisibly")
        if re.search(r'<svg[^>]*style="[^"]*(?:fill|stroke)\s*:\s*#', c) or re.search(r'<(?:rect|path|circle|line|text)[^>]*(?:fill|stroke)="#', c):
            warn(f"{tag} a diagram hard-codes a colour — use the .d-* classes so both themes work")
        for w in re.findall(r'<div class="walk"[\s\S]*?(?=<div class="walk"|<div class="quiz"|<div class="recap"|</div>\s*</section>|\Z)', c):
            n_st = len(re.findall(r'class="walk-step"', w))
            if n_st < 2: fail(f"{tag} a .walk has {n_st} step(s) — it needs at least 2 to be a walkthrough")
            if 'class="code"' not in w: fail(f"{tag} a .walk has no .code block to step through")
            else:
                code_txt = re.search(r"<code[^>]*>([\s\S]*?)</code>", w)
                nlines = len(code_txt.group(1).strip("\n").split("\n")) if code_txt else 0
                steps_only = w.split('class="walk-steps"', 1)[-1]
                for hl in re.findall(r'data-hl="([^"]+)"', steps_only):
                    for part in hl.split(","):
                        try: hi = int(part.strip().split("-")[-1])
                        except ValueError: continue
                        if nlines and hi > nlines:
                            fail(f"{tag} a .walk step highlights line {hi} but the code has {nlines}")
        for m in re.findall(r'<div class="seq-msg[^"]*"[^>]*>', c):
            if "data-from" not in m or "data-to" not in m:
                fail(f"{tag} a .seq-msg is missing data-from/data-to")
        for t in re.findall(r'<div class="tab"[^>]*>', c):
            if "data-title" not in t: fail(f"{tag} a .tab has no data-title — its button will read 'Tab N'")
        for sg in re.findall(r'<span class="seg[^"]*"[^>]*>', c):
            if "--s:" not in sg or "--w:" not in sg:
                fail(f"{tag} a .lane .seg is missing style=\"--s:N;--w:N\"")
        # --- subject blocks ---
        for dk in re.findall(r'<div class="cards"[\s\S]*?(?=<div class="(?:cards|quiz|recap)"|</div>\s*</section>|\Z)', c):
            if "data-id" not in dk.split(">", 1)[0]:
                fail(f"{tag} a .cards deck has no data-id — its progress cannot be saved")
            n_fc = len(re.findall(r'<div class="fc"', dk))
            if n_fc < 2: fail(f"{tag} a .cards deck has {n_fc} card(s) — a deck needs at least 2")
            if len(re.findall(r'class="fc-f"', dk)) != n_fc or len(re.findall(r'class="fc-b"', dk)) != n_fc:
                fail(f"{tag} a flashcard is missing its .fc-f front or .fc-b back")
        for ck in re.findall(r'<ul class="check"[^>]*>', c):
            if "data-id" not in ck: fail(f"{tag} a .check list has no data-id — its ticks cannot be saved")
        for fm in re.findall(r'<div class="formal[^"]*"[\s\S]{0,400}?</div>', c):
            if 'class="fl"' not in fm: fail(f"{tag} a .formal block has no .fl label")
        for q in re.split(r'(?=<div class="q")', body):
            if not q.startswith('<div class="q"') or "data-answer" not in q.split(">", 1)[0]: continue
            ansv = re.search(r'data-answer="([^"]*)"', q)
            if not ansv or not ansv.group(1).strip():
                fail(f"{tag} a typed-answer question has an empty data-answer")
            if 'class="fb"' not in q:
                fail(f"{tag} a typed-answer question has no .fb explanation")
        if 'class="math"' in body and 'class="where"' not in body:
            warn(f"{tag} has formulas but no .where legend — every symbol needs its meaning")
        for tl in re.findall(r'<li[^>]*>(?:(?!</li>)[\s\S])*?</li>', "".join(re.findall(r'<ol class="timeline">[\s\S]*?</ol>', c))):
            if 'class="when"' not in tl: fail(f"{tag} a .timeline entry has no <span class=\"when\">")
        for vr in re.findall(r'<div class="vr">[\s\S]*?</div>\s*</div>', c):
            if 'class="vx"' not in vr:
                warn(f"{tag} a .vocab entry has no example sentence (.vx) — a word without a sentence is unusable")
        for qt in re.findall(r'<blockquote class="quote">[\s\S]*?</blockquote>', c):
            if "<cite" not in qt: warn(f"{tag} a .quote has no <cite> — an uncited source cannot be checked")
        if len(re.findall(r"<h2\b", body)) < 2:
            warn(f"{tag} has fewer than 2 <h2> sections — is it really a whole chapter?")
        w = words(body)
        if w < minw: fail(f"{tag} only {w} words of content (floor is {minw}) — this is a summary, not a lesson")
        if 'class="ex"' not in body: warn(f"{tag} has no .ex exercise")

    dupes = {i for i in seen if seen.count(i) > 1}
    if dupes: fail("duplicate chapter ids: " + ", ".join(sorted(dupes)))
    for i in syl_ids:
        if i not in seen:
            (warn if wip else fail)(f"SYLLABUS.md promises {i} but it is not in index.html — write it")
    for i in seen:
        if syl_ids and i not in syl_ids: warn(f"{i} is in the page but not in SYLLABUS.md — update the syllabus")
    for i in set(ledger_ids):
        if i not in seen:
            (warn if wip else fail)(f"coverage ledger points at {i}, which does not exist")

    ids = re.findall(r'<(?:div class="cards"|ul class="check")[^>]*data-id="([^"]+)"', doc)
    for i in {x for x in ids if ids.count(x) > 1}:
        fail(f'data-id "{i}" is used twice — the two widgets would share saved progress')

    # Every chapter lands in ONE document, so an SVG id defined in chapter 3 silently wins
    # every url(#…) reference in chapter 11. Prefix them with the chapter id.
    svg_ids = re.findall(r'<(?:clipPath|linearGradient|radialGradient|marker|mask|pattern|filter|symbol)\b[^>]*\bid="([^"]+)"', doc)
    for i in sorted({x for x in svg_ids if svg_ids.count(x) > 1}):
        fail(f'SVG id "{i}" is defined more than once — references resolve to the first '
             f'definition in the document, so later figures silently pick up the wrong one. '
             f'Prefix ids with the chapter (id="ch7-{i}")')

    # ---- 4. laziness markers -------------------------------------------------
    plain = text_of(doc)
    for pat in LAZY:
        for m in re.finditer(pat, plain, re.I):
            fail(f"laziness marker {m.group(0)!r} at …{plain[max(0,m.start()-60):m.end()+40].strip()[:110]}…")

    # ---- 5. structural balance ----------------------------------------------
    stripped = re.sub(r"<(script|style)[\s\S]*?</\1>", "", doc, flags=re.I)
    stripped = re.sub(r"<!--[\s\S]*?-->", "", stripped)
    for t in BLOCK_TAGS:
        o = len(re.findall(r"<%s\b" % t, stripped, re.I))
        c = len(re.findall(r"</%s\s*>" % t, stripped, re.I))
        if t == "p" and o != c: warn(f"<p> open/close mismatch ({o}/{c}) — usually harmless")
        elif t != "p" and o != c: fail(f"<{t}> open/close mismatch: {o} open vs {c} close")

    # ---- 6. report -----------------------------------------------------------
    tw = words(doc)
    n_code = len(re.findall(r'class="code"', doc))
    n_q    = len(re.findall(r'class="q"', doc))
    n_viz  = len(re.findall(r'<figure[^>]*class="(?:viz|diagram)', doc))
    n_walk = len(re.findall(r'class="walk"', doc))
    extras = []
    for label, pat in (("formulas", r'class="math"'), ("flashcards", r'<div class="fc"'),
                       ("vocab entries", r'<div class="vr">'), ("checklists", r'<ul class="check"')):
        n = len(re.findall(pat, doc))
        if n: extras.append(f"{n} {label}")
    lang = (re.search(r'<html[^>]*\blang="([^"]*)"', doc) or [None, "?"])[1]
    dirn = (re.search(r'<html[^>]*\bdir="([^"]*)"', doc) or [None, "ltr"])[1]
    print(f"lang={lang} dir={dirn}   chapters: {len(chaps)}   "
          f"visuals: {n_viz} figures + {n_walk} walkthroughs   code blocks: {n_code}   "
          f"quiz questions: {n_q}   words: {tw:,}   size: {len(doc)/1024:.0f} KB"
          + (("\n" + "   " + " · ".join(extras)) if extras else ""))
    for w in warns: print("WARN  " + w)
    for f in fails: print("FAIL  " + f)
    if fails:
        print(f"\n{len(fails)} failure(s). Fix by writing the missing content — not by relaxing the gate.")
        sys.exit(1)
    print("\nPASS (work in progress)" if wip else "\nPASS — course is complete against its syllabus.")

if __name__ == "__main__":
    main()
