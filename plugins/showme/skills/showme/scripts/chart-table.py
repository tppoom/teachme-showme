#!/usr/bin/env python3
"""Turn a CSV (or TSV) into a ready-to-paste .chart block, so the numbers on a slide are
the numbers in the file — never retyped, never rounded by eye.

Usage:
  python3 chart-table.py data.csv --type bar|line|area|stack|hbar|donut
         [--x COLUMN] [--series "Col A,Col B"] [--unit k] [--scale 1000]
         [--top 5] [--other "Other"] [--sort] [--hi "Label"] [--decimals 1]
         [--src "System, date range, what it excludes"]

The CSV is read the way spreadsheets are laid out: one row per category (Q1, Q2 … or one
row per country), one column per series. --x picks the category column (default: the first),
--series picks which numeric columns to draw (default: all numeric ones).

  --scale 1000 --unit k   divide by 1000 and label as "k" (rounding happens once, here)
  --top 5                 keep the 5 largest categories, sum the rest into --other.
                          Beyond ~5 a chart is a table with extra steps — that is why.
  --sort                  largest first (sensible for hbar and donut, wrong for time)
  --hi "Nobody followed up"  grey every bar except this one (hbar)

Prints the block to stdout and a one-line summary to stderr. Without --src it prints a
reminder instead of a source line: a number with no source is the one the room interrogates.
"""
import csv, sys, html, argparse, pathlib, re

def num(v):
    v = (v or "").strip().replace(",", "").replace("%", "").replace("$", "").replace("£", "").replace("€", "").replace("฿", "")
    if v in ("", "-", "—"): return None
    try: return float(v)
    except ValueError: return None

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--type", default="bar", choices=["bar", "line", "area", "stack", "hbar", "donut"])
    ap.add_argument("--x"); ap.add_argument("--series"); ap.add_argument("--unit", default="")
    ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--decimals", type=int)
    ap.add_argument("--top", type=int); ap.add_argument("--other", default="Other")
    ap.add_argument("--sort", action="store_true"); ap.add_argument("--hi"); ap.add_argument("--src")
    a = ap.parse_args()

    p = pathlib.Path(a.file)
    text = p.read_text(encoding="utf-8-sig")
    dialect = csv.excel_tab if p.suffix.lower() in (".tsv", ".tab") or text.count("\t") > text.count(",") else csv.excel
    rows = [r for r in csv.reader(text.splitlines(), dialect) if any(c.strip() for c in r)]
    if len(rows) < 2: sys.exit("chart-table: the file needs a header row and at least one data row")
    head, data = [h.strip() for h in rows[0]], rows[1:]

    if a.x and a.x not in head: sys.exit(f"chart-table: no column {a.x!r}. Columns: {', '.join(head)}")
    xi = head.index(a.x) if a.x else 0
    if a.series:
        names = [s.strip() for s in a.series.split(",")]
        bad = [n for n in names if n not in head]
        if bad: sys.exit(f"chart-table: no column {', '.join(bad)}. Columns: {', '.join(head)}")
        cols = [head.index(n) for n in names]
    else:
        cols = [i for i in range(len(head)) if i != xi and all(num(r[i]) is not None for r in data if i < len(r) and r[i].strip())
                and any(i < len(r) and num(r[i]) is not None for r in data)]
    if not cols: sys.exit("chart-table: found no numeric columns to draw")
    if a.type in ("hbar", "donut") and len(cols) > 1:
        print(f"chart-table: note — {a.type} draws one series; using {head[cols[0]]!r} "
              f"and ignoring {', '.join(head[c] for c in cols[1:])}", file=sys.stderr)
        cols = cols[:1]

    cats = [(r[xi].strip(), [num(r[c]) if c < len(r) else None for c in cols]) for r in data]
    if a.sort or a.top:
        cats.sort(key=lambda c: -(c[1][0] or 0))
    if a.top and len(cats) > a.top:
        keep, rest = cats[:a.top], cats[a.top:]
        other = [sum((c[1][k] or 0) for c in rest) for k in range(len(cols))]
        cats = keep + [(f"{a.other} ({len(rest)})", other)]

    def fmt(v):
        if v is None: return ""
        v = v / a.scale
        d = a.decimals if a.decimals is not None else (0 if abs(v) >= 100 else 1 if abs(v) >= 1 else 2)
        s = f"{v:.{d}f}"
        return re.sub(r"\.0+$", "", s) if "." in s else s

    attrs = f' data-type="{a.type}"' + (f' data-unit="{html.escape(a.unit)}"' if a.unit else "")
    if a.hi:
        idx = [k for k, c in enumerate(cats) if c[0] == a.hi]
        if not idx: sys.exit(f"chart-table: --hi {a.hi!r} is not a category. Categories: {', '.join(c[0] for c in cats)}")
        attrs += f' data-hi="{idx[0]}"'
    e = html.escape
    out = [f'<div class="chart"{attrs}>', "  <table>",
           "    <tr><th></th>" + "".join(f"<th>{e(c[0])}</th>" for c in cats) + "</tr>"]
    for k, c in enumerate(cols):
        out.append(f"    <tr><th>{e(head[c])}</th>" + "".join(f"<td>{fmt(v[1][k])}</td>" for v in cats) + "</tr>")
    out += ["  </table>", "</div>", '<div class="take">WRITE: what this chart proves, in one line.</div>']
    out.append(f'<p class="src">{e(a.src)}</p>' if a.src else
               f'<p class="src">WRITE: {e(p.name)} — the system it came from, the date range, and what it excludes.</p>')
    print("\n".join(out))
    if len(cats) > 7:
        print(f"chart-table: warning — {len(cats)} categories. Use --top 5 or show a table on purpose.", file=sys.stderr)
    print(f"chart-table: {len(cats)} categories × {len(cols)} series from {p.name}"
          + (f", scaled ÷{a.scale:g}" if a.scale != 1 else ""), file=sys.stderr)

if __name__ == "__main__":
    main()
