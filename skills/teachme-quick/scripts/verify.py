#!/usr/bin/env python3
"""Quality gate for a TeachMe course.

Usage:  python3 verify.py <course-dir> [--wip]
        python3 verify.py <course-dir> --part parts/03-slug.html

--wip  = mid-build: chapters the syllabus lists but that are not written yet only warn.
--part = check one chapter file on its own, without assembling (implies --wip).

What it enforces, in order of importance:
  1. Nothing renders broken — stray Markdown, code swallowed as HTML tags, unbalanced
     markup, external resources, duplicate ids, malformed blocks.
  2. Every chapter teaches through something concrete — a worked example, code with
     output, a figure, a comparison, a table — not prose alone.
  3. No padding — chapters past the length budget, filler phrases, box-stacking and
     chapter counts beyond the depth all warn.
  4. Whatever SYLLABUS.md lists is actually written.

meta.json tunes it:
  "depth": "quick" | "standard" (default) | "deep"
  "omit":  ["quiz", "exercise", "visual", "appendix"]  — blocks the user asked to drop

Fix every FAIL and WARN. A FAIL is a bug or a missing piece; a WARN is usually padding.
"""
import sys, re, json, pathlib, html

#            floor  ceiling  max chapters (warn above)
PROFILES = {
    "quick":    (80,   650,     4),
    "standard": (120,  900,    10),
    "deep":     (200,  1500,   24),
}
OMITTABLE = {"quiz", "exercise", "visual", "appendix", "objective", "recap", "ledger"}

LAZY = [
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bPLACEHOLDER\b", r"Lorem ipsum",
    r"coming soon", r"\[\.\.\.\]", r"\(\.\.\.\)", r"left as an exercise for the reader",
    r"similar to (?:the )?above", r"the rest (?:is|are) (?:similar|analogous)",
    r"ดูด้านบน", r"ทำนองเดียวกันกับด้านบน",
]
# Phrases that carry no information. Each one is a sentence the reader has to read for nothing.
FILLER = [
    r"\bin this (?:chapter|section|lesson),? (?:we will|we'll|you will|you'll)\b",
    r"\blet'?s (?:dive|delve|take a (?:closer|deep) look)", r"\bdive (?:deep )?into\b", r"\bdelve\b",
    r"\bit(?: is|'s) (?:important|worth|crucial) (?:to note|noting|to remember|to understand)\b",
    r"\bin today'?s (?:fast-paced|digital|modern|ever-changing)\b", r"\bin the (?:world|realm) of\b",
    r"\bplays? a (?:crucial|vital|pivotal|key) role\b", r"\bas (?:we have|we've) (?:seen|discussed|learned)\b",
    r"\bin conclusion\b", r"\bin summary\b", r"\bwithout further ado\b", r"\bat the end of the day\b",
    r"\bneedless to say\b", r"\bit goes without saying\b", r"\bunlock (?:the|your) (?:power|potential)\b",
    r"ในบทนี้(?:เรา)?จะ(?:มา)?(?:เรียนรู้|ศึกษา|ทำความรู้จัก|พูดถึง|อธิบาย)",
    r"(?:สิ่ง|เรื่อง)(?:ที่)?สำคัญ(?:ที่)?(?:ควร|ต้อง)(?:ทราบ|รู้|จำ)(?:ไว้)?(?:ก็)?คือ",
    r"เป็น(?:สิ่ง|เรื่อง)ที่สำคัญ(?:อย่าง)?มาก", r"ในยุค(?:ปัจจุบัน|ดิจิทัล|นี้)", r"ในโลกยุค",
    r"อย่างที่(?:ได้)?(?:กล่าว|อธิบาย|เห็น)(?:ไป)?(?:แล้ว|ข้างต้น)", r"กล่าวโดยสรุป", r"โดยสรุปแล้ว",
    r"มีบทบาท(?:สำคัญ)?(?:อย่างมาก|เป็นอย่างมาก)", r"ไม่ว่าจะเป็น.{0,40}ก็ตาม",
]
BLOCK_TAGS = ["section", "div", "ul", "ol", "li", "table", "tbody", "thead",
              "tr", "td", "th", "pre", "details", "figure", "dl", "dt", "dd", "p", "code", "span"]
# what counts as "showing, not telling" — at least one per chapter
CONCRETE = [r'class="eg"', r'<figure[^>]*class="(?:viz|diagram)', r'class="walk"', r'class="code"',
            r'class="cmp"', r'class="tw"', r'class="math"', r'class="ex"', r'class="dlg"',
            r'class="annot"', r'class="vocab"', r'class="steps"', r'<img\b', r'<svg\b', r'class="derive"']

fails, warns = [], []
def fail(m): fails.append(m)
def warn(m): warns.append(m)

def text_of(frag):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", frag, flags=re.I)
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)

CJK  = "぀-ヿ㐀-䶿一-鿿豈-﫿ｦ-ﾟ가-힯"
NOSP = "฀-๿຀-໿က-႟ក-៿"   # Thai Lao Myanmar Khmer

def count_words(t):
    n_cjk  = len(re.findall(f"[{CJK}]", t))
    n_nosp = len(re.findall(f"[{NOSP}]", t))
    rest   = re.sub(f"[{CJK}{NOSP}]", " ", t)
    return len(rest.split()) + round(n_cjk / 2.5) + round(n_nosp / 5)

def words(frag): return count_words(text_of(frag))

def strip_code(frag):
    return re.sub(r"<(pre|code|math|svg)\b[\s\S]*?</\1>", " ", frag, flags=re.I)

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

    mf = d / "meta.json"
    meta = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    depth = str(meta.get("depth", "standard")).lower()
    if depth not in PROFILES:
        sys.exit(f'FAIL: meta.json depth "{depth}" is not one of {", ".join(PROFILES)}')
    floor, ceiling, max_ch = PROFILES[depth]
    omit = {str(x).lower() for x in meta.get("omit", [])}
    bad = omit - OMITTABLE
    if bad: sys.exit(f"FAIL: meta.json omit has unknown item(s) {sorted(bad)} — allowed: {sorted(OMITTABLE)}")
    lang = str(meta.get("lang", "en")).split("-")[0].lower()

    if part_file is not None:
        if not part_file.is_absolute():
            part_file = (d / part_file) if (d / part_file).exists() else part_file.resolve()
        if not part_file.exists(): sys.exit(f"FAIL: {part_file} not found")
        doc = part_file.read_text(encoding="utf-8")
    else:
        idx = d / "index.html"
        if not idx.exists(): sys.exit(f"FAIL: {idx} not built yet — run assemble.py first")
        doc = idx.read_text(encoding="utf-8")
        lang = (re.search(r'<html[^>]*\blang="([^"]*)"', doc) or [None, lang])[1].split("-")[0].lower()

    # ---- 1. self-containment -------------------------------------------------
    for pat, msg in [(r"<script[^>]+\bsrc=", "external <script src>"),
                     (r'<link[^>]+rel=["\']?stylesheet', "external stylesheet <link>"),
                     (r"@import\s", "CSS @import"),
                     (r'<img[^>]+src=["\'](?!data:)', "<img> that is not an inlined data: URI")]:
        if re.search(pat, doc, re.I): fail(f"not self-contained: {msg} found")
    if re.search(r"@@[A-Z_]+@@", doc): fail("unresolved @@PLACEHOLDER@@ left in the page")

    # ---- 2. syllabus ---------------------------------------------------------
    syl = d / "SYLLABUS.md"
    syl_ids, later_ids, cov_ids, unchecked = [], [], [], []
    if syl.exists():
        s = syl.read_text(encoding="utf-8")
        lp = re.split(r"^##\s+Later\b.*$", s, maxsplit=1, flags=re.M | re.I)
        later_ids = re.findall(r"^\s*[-*]\s*`?(ch-[\w-]+)`?", lp[1].split("\n## ", 1)[0], re.M) if len(lp) > 1 else []
        chap_sec = re.split(r"^##\s+Chapters\b.*$", s, maxsplit=1, flags=re.M | re.I)
        chap_txt = chap_sec[1].split("\n## ", 1)[0] if len(chap_sec) > 1 else s
        syl_ids = [i for i in re.findall(r"^\s*[-*]\s*(?:\[[ x]\]\s*)?`?(ch-[\w-]+)`?", chap_txt, re.M)
                   if i not in later_ids]
        cov = re.split(r"^##\s+(?:Coverage(?: ledger)?)\b.*$", s, maxsplit=1, flags=re.M | re.I)
        if len(cov) > 1:
            ct = cov[1].split("\n## ", 1)[0]
            cov_ids = [i for i in re.findall(r"(ch-[\w-]+)", ct) if i not in later_ids]
            unchecked = [u for u in re.findall(r"^\s*[-*]\s*\[ \]\s*(.+)$", ct, re.M)
                         if not any(l in u for l in later_ids)]
    elif part_file is None:
        warn("no SYLLABUS.md — keep the chapter plan there so the course can be edited later")
    for u in ([] if part_file is not None else unchecked):
        (warn if wip else fail)(f"coverage item still unchecked: {u.strip()[:90]}")

    # ---- 3. chapters ---------------------------------------------------------
    CH = r'<section\b[^>]*\bclass="[^"]*\bchapter\b'
    def cut(c):
        e = c.find("</section>")
        return c if e < 0 else c[:e + len("</section>")]
    live = re.sub(r"<!--[\s\S]*?-->", "", doc)       # commented-out markup is not content
    chaps = [cut(c) for c in re.split(f"(?={CH})", live) if re.match(CH, c)]
    if not chaps: fail("no <section class=\"chapter\"> found")
    if part_file is not None and len(chaps) > 1 and not all("appendix" in c.split(">", 1)[0] for c in chaps[1:]):
        warn(f"{part_file.name} holds {len(chaps)} chapters — one chapter per part file keeps edits cheap")
    seen = []
    for c in chaps:
        head = c.split(">", 1)[0]
        cid = (re.search(r'\bid="([^"]+)"', head) or [None, "?"])[1]
        seen.append(cid)
        tag = f"[{cid}]"
        body = c.split('class="ch-body"', 1)[-1]
        if not re.search(r'data-title="[^"]+"', head): fail(f"{tag} missing data-title (the sidebar entry would be blank)")
        if not re.search(r'class="ch-title"', c): fail(f"{tag} missing <h1 class=\"ch-title\">")
        if 'class="ch-desc"' not in c: warn(f"{tag} has no .ch-desc — one sentence on what the reader can do after it")
        if 'class="ch-body"' not in c: fail(f"{tag} has no <div class=\"ch-body\"> — content will be unstyled")
        appendix = "appendix" in head

        # --- rendering bugs ---
        prose = strip_code(body)
        ptxt = text_of(prose)
        md = []
        if re.search(r"(?<![*\w])\*\*[^*\n]{1,80}\*\*(?!\*)", ptxt): md.append("**bold**")
        if re.search(r"(?m)^\s{0,3}#{1,4}\s+\S", ptxt): md.append("# heading")
        if "```" in ptxt: md.append("``` fence")
        if re.search(r"(?<![\w`])`[^`\n]{1,60}`(?![\w`])", ptxt): md.append("`code`")
        if re.search(r"\[[^\]\n]{1,80}\]\((?:https?://|#|\.?/)[^)\s]*\)", ptxt): md.append("[link](url)")
        if md: fail(f"{tag} Markdown in HTML renders literally: {', '.join(md)} — use <strong>, <h2>, <code>, <a>")
        if re.search(r"\\n|\\t", ptxt): fail(f"{tag} a literal \\n or \\t shows up in the text")
        for code in re.findall(r"<code\b[^>]*>([\s\S]*?)</code>", c):
            m = re.search(r"<(?!/?(?:span|b|i|em|strong|mark|u|br)\b)[/!]?[A-Za-z][^>]*>?", code)
            if m:
                fail(f"{tag} unescaped '<' in <code>: {m.group(0)[:40]!r} — the browser eats it as a tag; write &lt;")
                break
        if re.search(r"<p>\s*</p>|<h2[^>]*>\s*</h2>|<li>\s*</li>", body):
            warn(f"{tag} has an empty <p>, <h2> or <li> — leaves a visible gap")
        if re.search(r'style="[^"]*(?:width|min-width)\s*:\s*(?:[8-9]\d\d|\d{4,})px', c):
            warn(f"{tag} an inline width over 800px will overflow on phones")
        for sv in re.findall(r"<svg[^>]*>", c):
            if 'role="img"' not in sv or "aria-label" not in sv:
                fail(f"{tag} an <svg> is missing role=\"img\" or aria-label")
            if "viewBox" not in sv and "width=\"0\"" not in sv:
                warn(f"{tag} an <svg> has no viewBox — it will not scale with the column")
        for sv in re.findall(r"<svg[^>]*viewBox=\"[^\"]*\"[\s\S]*?</svg>", c):
            vb = re.search(r'viewBox="\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', sv)
            if not vb: continue
            x0, y0, vw, vh = (float(g) for g in vb.groups())
            for el in re.findall(r"<(?:text|rect|circle|image|use)\b[^>]*>", sv):
                cx = re.search(r'\b(?:x|cx)="([-\d.]+)"', el)
                cy = re.search(r'\b(?:y|cy)="([-\d.]+)"', el)
                if cx and not (x0 - 1 <= float(cx.group(1)) <= x0 + vw + 1):
                    warn(f"{tag} an SVG element at x={cx.group(1)} is outside the viewBox — it will be clipped")
                if cy and not (y0 - 1 <= float(cy.group(1)) <= y0 + vh + 1):
                    warn(f"{tag} an SVG element at y={cy.group(1)} is outside the viewBox — it will be clipped")
        if re.search(r'<(?:rect|path|circle|line|text|polygon|ellipse)[^>]*(?:fill|stroke)="#', c) or \
           re.search(r'<svg[^>]*style="[^"]*(?:fill|stroke)\s*:\s*#', c):
            warn(f"{tag} a diagram hard-codes a colour — it will vanish in one theme; use the .d-* classes")
        for fg in re.findall(r'<figure[^>]*class="(?:viz|diagram)"[\s\S]*?</figure>', c):
            if "<figcaption" not in fg:
                warn(f"{tag} a figure has no <figcaption> — the caption carries the takeaway")
        for w in re.findall(r'<div class="walk"[\s\S]*?(?=<div class="walk"|<div class="quiz"|</div>\s*</section>|\Z)', c):
            n_st = len(re.findall(r'class="walk-step"', w))
            if n_st < 2: fail(f"{tag} a .walk has {n_st} step(s) — it needs at least 2")
            if 'class="code"' not in w: fail(f"{tag} a .walk has no .code block to step through")
            else:
                code_txt = re.search(r"<code[^>]*>([\s\S]*?)</code>", w)
                nlines = len(code_txt.group(1).strip("\n").split("\n")) if code_txt else 0
                for hl in re.findall(r'data-hl="([^"]+)"', w.split('class="walk-steps"', 1)[-1]):
                    for part in hl.split(","):
                        try: hi = int(part.strip().split("-")[-1])
                        except ValueError: continue
                        if nlines and hi > nlines:
                            fail(f"{tag} a .walk step highlights line {hi} but the code has {nlines}")
        for m in re.findall(r'<div class="seq-msg[^"]*"[^>]*>', c):
            if "data-from" not in m or "data-to" not in m: fail(f"{tag} a .seq-msg is missing data-from/data-to")
        for t in re.findall(r'<div class="tab"[^>]*>', c):
            if "data-title" not in t: fail(f"{tag} a .tab has no data-title — its button will read 'Tab N'")
        for sg in re.findall(r'<span class="seg[^"]*"[^>]*>', c):
            if "--s:" not in sg or "--w:" not in sg: fail(f"{tag} a .lane .seg is missing style=\"--s:N;--w:N\"")
        for dk in re.findall(r'<div class="cards"[\s\S]*?(?=<div class="(?:cards|quiz)"|</div>\s*</section>|\Z)', c):
            if "data-id" not in dk.split(">", 1)[0]: fail(f"{tag} a .cards deck has no data-id — progress cannot be saved")
            n_fc = len(re.findall(r'<div class="fc"', dk))
            if n_fc < 2: fail(f"{tag} a .cards deck has {n_fc} card(s) — it needs at least 2")
            if len(re.findall(r'class="fc-f"', dk)) != n_fc or len(re.findall(r'class="fc-b"', dk)) != n_fc:
                fail(f"{tag} a flashcard is missing its .fc-f front or .fc-b back")
        for ck in re.findall(r'<ul class="check"[^>]*>', c):
            if "data-id" not in ck: fail(f"{tag} a .check list has no data-id — ticks cannot be saved")
        for tl in re.findall(r'<li[^>]*>(?:(?!</li>)[\s\S])*?</li>', "".join(re.findall(r'<ol class="timeline">[\s\S]*?</ol>', c))):
            if 'class="when"' not in tl: fail(f"{tag} a .timeline entry has no <span class=\"when\">")
        if 'class="math"' in body and 'class="where"' not in body:
            warn(f"{tag} has a formula but no .where legend — say what every symbol means")

        # --- quiz validity ---
        for q in re.split(r'(?=<div class="q"[ >])', body):
            if not q.startswith('<div class="q"'): continue
            qhead = q.split(">", 1)[0]
            if 'class="fb"' not in q: fail(f"{tag} a quiz question has no .fb explanation")
            if "data-answer" in qhead:
                if not re.search(r'data-answer="[^"]*\S[^"]*"', qhead): fail(f"{tag} a typed-answer question has an empty data-answer")
                continue
            n_ok = len(re.findall(r'data-correct="true"', q))
            if n_ok != 1: fail(f"{tag} a quiz question has {n_ok} correct answers (must be exactly 1)")
            opts = re.findall(r'<button class="opt"([^>]*)>([\s\S]*?)</button>', q)
            if 0 < len(opts) < 3: warn(f"{tag} a question has only {len(opts)} options — give at least 3 plausible ones")
            if any("data-why" not in a for a, _ in opts if 'data-correct="true"' not in a):
                warn(f"{tag} a wrong option has no data-why — that line is what teaches the reader who picks it")
            ot = text_of(" ".join(t for _, t in opts))
            if re.search(r"\b(?:all|none|both) of the (?:above|below)\b|ถูกทุกข้อ|ไม่มีข้อใดถูก|ทั้งหมดข้างต้น", ot, re.I) \
               and "fixed" not in qhead:
                fail(f"{tag} an option says 'all/none of the above' — the page shuffles options")
        n_q = len(re.findall(r'<div class="q"[ >]', body))
        if n_q > 4: warn(f"{tag} has {n_q} quiz questions — 1-3 is a quick check; more is a test")

        if appendix: continue

        # --- teaches through something concrete ---
        if not any(re.search(p, body) for p in CONCRETE):
            fail(f"{tag} has no concrete example — add a worked .eg, code with output, a figure, a "
                 f"comparison or a table. A chapter of prose alone is the thing readers skim and forget")
        elif not re.search(r'class="eg"|class="code"|class="walk"|class="ex"|class="cmp"|class="dlg"|class="annot"|class="derive"', body) \
             and "visual" not in omit and depth != "quick":
            warn(f"{tag} has a figure or table but no worked example (.eg, code, .cmp) — show one case worked through")

        # --- length & padding ---
        # the budget is for prose: code and its output are read differently and are not padding
        w_read = words(re.sub(r"<pre\b[\s\S]*?</pre>|<div class=\"code-out\">[\s\S]*?</div>", " ",
                              re.sub(r'<div class="quiz">[\s\S]*$', "", body)))
        if w_read < floor:
            warn(f"{tag} is only {w_read} words — check the example is worked through, not just named")
        if w_read > ceiling:
            warn(f"{tag} is {w_read} words (budget ~{ceiling} at depth={depth}) — cut what repeats, or split it")
        n_h2 = len(re.findall(r"<h2\b", body))
        if n_h2 > 4: warn(f"{tag} has {n_h2} <h2> sections — a chapter is one idea; merge or split")
        if re.search(r"<h3\b", body): warn(f"{tag} uses <h3> — fold it into the section above")
        n_box = len(re.findall(r'<div class="(?:callout|objective|recap)\b', body))
        if n_box > 2: warn(f"{tag} has {n_box} boxes (callout/objective/recap) — keep the one or two that matter")
        # walls of text: the reader skims first, so long or stacked paragraphs hide the point
        def snip(f): return " ".join(text_of(f).split())[:40]
        long_p = [p for p in re.findall(r"<p\b[^>]*>([\s\S]*?)</p>", body) if count_words(text_of(p)) > 60]
        if long_p: warn(f"{tag} has {len(long_p)} paragraph(s) over ~60 words, e.g. {snip(long_p[0])!r}… — "
                        "split it, or turn its reasons/options/numbers into a list or table")
        walls = [r for r in re.findall(r"(?:<p\b[^>]*>[\s\S]*?</p>\s*){3,}", body) if words(r) > 100]
        if walls: warn(f"{tag} has {len(walls)} run(s) of 3+ paragraphs in a row, e.g. from {snip(walls[0])!r}… — "
                       "break each with a list, table, code, figure or .eg")
        long_li = [li for li in re.findall(r"<li\b[^>]*>([\s\S]*?)</li>", body)
                   if 'class="opt"' not in li and count_words(text_of(li)) > 45]
        if long_li: warn(f"{tag} has {len(long_li)} list item(s) over ~45 words, e.g. {snip(long_li[0])!r}… — "
                         "lead with the key phrase, keep the rest to a line")
        hits = []
        for pat in FILLER:
            for m in re.finditer(pat, ptxt, re.I):
                hits.append(m.group(0))
        if hits:
            warn(f"{tag} filler that says nothing: " + ", ".join(repr(h) for h in hits[:4]) +
                 (f" (+{len(hits)-4} more)" if len(hits) > 4 else "") + " — delete and state the point")

        # --- one language ---
        if lang in ("th", "lo", "my", "km"):
            # a dot after a 1-3 letter run is an abbreviation (ก.ย., พ.ศ., ธปท.), which is correct
            dots = re.findall(r"(?<![\u0e00-\u0eff.])[\u0e00-\u0eff]{4,}\.(?=\s|<|$)", text_of(prose))
            if dots:
                warn(f"{tag} {len(dots)} English full stop(s) after {lang} text — the script does not use them; delete")
        if lang not in ("en",) and lang.isalpha():
            for lab in re.findall(r'<(?:div class="quiz-h"|span class="eg-h"|div class="ct"|h5)[^>]*>([\s\S]*?)</(?:div|span|h5)>', body):
                lt = text_of(lab).strip()
                if lt and re.fullmatch(r"[A-Za-z][A-Za-z '’!?.:,-]{2,40}", lt) and lt.lower() not in ("api", "json", "git"):
                    warn(f"{tag} label {lt!r} is in English but the course is lang={lang} — translate it "
                         f"(an empty <div class=\"quiz-h\"></div> gets the interface's own word)")
        if lang in ("th", "ja", "zh", "ko", "ar", "he", "ru", "hi", "el", "uk", "fa"):
            for p in re.findall(r"<p\b[^>]*>([\s\S]*?)</p>", prose):
                t = text_of(p)
                if count_words(t) >= 25 and not re.search(r"[^\x00-ɏ -⁯₠-⃏←-⋿]", t):
                    warn(f"{tag} a paragraph is entirely in English but the course is lang={lang}: "
                         f"{t.strip()[:60]!r}…")
                    break

    real = [c for c in chaps if "appendix" not in c.split(">", 1)[0]]
    if part_file is None and len(real) > max_ch:
        warn(f"{len(real)} chapters at depth={depth} (aim for at most {max_ch}) — merge chapters that "
             f"share an idea, or confirm the user wants a course this long")

    dupes = {i for i in seen if seen.count(i) > 1}
    if dupes: fail("duplicate chapter ids: " + ", ".join(sorted(dupes)))
    for i in ([] if part_file is not None else syl_ids):
        if i not in seen: (warn if wip else fail)(f"SYLLABUS.md lists {i} but it is not in the page — write it or remove it")
    for i in seen:
        if syl_ids and i not in syl_ids and i not in later_ids:
            warn(f"{i} is in the page but not in SYLLABUS.md — update the syllabus")
    for i in ([] if part_file is not None else set(cov_ids)):
        if i not in seen: (warn if wip else fail)(f"coverage list points at {i}, which does not exist")

    ids = re.findall(r'<(?:div class="cards"|ul class="check")[^>]*data-id="([^"]+)"', doc)
    for i in {x for x in ids if ids.count(x) > 1}:
        fail(f'data-id "{i}" is used twice — the two widgets would share saved progress')
    svg_ids = re.findall(r'<(?:clipPath|linearGradient|radialGradient|marker|mask|pattern|filter|symbol)\b[^>]*\bid="([^"]+)"', doc)
    for i in sorted({x for x in svg_ids if svg_ids.count(x) > 1}):
        fail(f'SVG id "{i}" is defined more than once — prefix ids with the chapter (id="ch7-{i}")')

    # ---- 4. leftovers --------------------------------------------------------
    plain = text_of(strip_code(doc))
    for pat in LAZY:
        flags = 0 if re.fullmatch(r"\\b[A-Z+]+:?(?:\\b)?", pat) else re.I
        for m in re.finditer(pat, plain, flags):
            fail(f"unfinished content {m.group(0)!r} at …{plain[max(0,m.start()-50):m.end()+30].strip()[:90]}…")

    # ---- 5. markup balance ---------------------------------------------------
    stripped = re.sub(r"<(script|style)[\s\S]*?</\1>", "", doc, flags=re.I)
    stripped = re.sub(r"<!--[\s\S]*?-->", "", stripped)
    for t in BLOCK_TAGS:
        o = len(re.findall(r"<%s\b" % t, stripped, re.I))
        cl = len(re.findall(r"</%s\s*>" % t, stripped, re.I))
        if o != cl:
            (warn if t == "p" else fail)(f"<{t}> open/close mismatch: {o} open vs {cl} close")

    # ---- 6. report -----------------------------------------------------------
    def prose_words(c):
        b = re.sub(r'<div class="quiz">[\s\S]*$', "", c.split('class="ch-body"', 1)[-1])
        return words(re.sub(r"<pre\b[\s\S]*?</pre>|<div class=\"code-out\">[\s\S]*?</div>", " ", b))
    tw = sum(prose_words(c) for c in chaps)
    n_eg = len(re.findall(r'class="eg"', doc))
    n_code = len(re.findall(r'class="code"', doc))
    n_viz = len(re.findall(r'<figure[^>]*class="(?:viz|diagram)', doc)) + len(re.findall(r'class="walk"', doc))
    n_q = len(re.findall(r'<div class="q"[ >]', doc))
    prof = f"depth={depth}" + (f" omit={','.join(sorted(omit))}" if omit else "")
    if part_file is not None: print(f"part: {part_file.name}")
    print(f"{prof}   lang={lang}   chapters: {len(chaps)}   prose words: {tw:,}   "
          f"worked examples: {n_eg}   code: {n_code}   visuals: {n_viz}   quiz questions: {n_q}")
    for w in warns: print("WARN  " + w)
    for f in fails: print("FAIL  " + f)
    if fails:
        print(f"\n{len(fails)} failure(s). Fix them in parts/, re-assemble, re-run.")
        sys.exit(1)
    if later_ids: print(f"LATER {len(later_ids)} chapter(s) planned for a later phase: {', '.join(later_ids)}")
    if part_file is not None: print("\nPASS (this chapter)"); return
    print("\nPASS (work in progress)" if wip else "\nPASS" + (" — fix the WARN lines too" if warns else ""))

if __name__ == "__main__":
    main()
